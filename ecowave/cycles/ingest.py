"""Ingestion of the CPV panel: WB indicators per country, then aggregated
to group level (WLD, OECD, income groups, G7/G20/BRICS).

For built-in WB aggregates (WLD, OED, HIC/UMC/LMC/LIC) the API already returns
a single GDP-weighted series — we just call the WB endpoint with the aggregate
code. For G7/G20/BRICS we fetch each country and recompute a GDP-weighted
average on the annual grid.
"""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path

import pandas as pd
import requests

from ecowave.cycles.bands import GROUPS
from ecowave.cycles.manifest import CycleSpec
from ecowave.db import upsert_cycle_observation, upsert_source

GDP_INDICATOR_FOR_WEIGHTING = "NY.GDP.MKTP.CD"  # GDP in current USD


def _fetch_wb(country: str, indicator: str, api_base: str,
              max_retries: int = 3, backoff: float = 1.5) -> pd.DataFrame:
    """Fetch a WB indicator for a country/aggregate. Returns DataFrame[year, value]."""
    if not api_base:
        raise ValueError("WORLD_BANK_API_BASE is required.")
    url = f"{api_base.rstrip('/')}/country/{country}/indicator/{indicator}"
    last_exc: Exception | None = None
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params={"format": "json", "per_page": 20000},
                                    timeout=60)
            response.raise_for_status()
            data = response.json()
            rows = data[1] if isinstance(data, list) and len(data) > 1 else []
            if not rows:
                return pd.DataFrame(columns=["year", "value"])
            df = pd.DataFrame(rows)
            out = pd.DataFrame({
                "year": pd.to_numeric(df["date"], errors="coerce").astype("Int64"),
                "value": pd.to_numeric(df["value"], errors="coerce"),
            }).dropna(subset=["year"])
            return out.sort_values("year").reset_index(drop=True)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(backoff ** attempt)
    raise RuntimeError(f"WB fetch failed for {country}/{indicator}: {last_exc}")


def fetch_country_series(country: str, indicator: str, api_base: str,
                         data_raw_dir: Path, con: sqlite3.Connection,
                         run_id: int, variable_code: str,
                         dataset_name: str, license_notes: str = "") -> tuple[pd.Series, int]:
    """Fetch + persist raw CSV + register provenance. Returns (annual Series, source_id).

    Cycle ingestion writes raw CSVs to disk under data_raw/worldbank_cycles/ and
    persists provenance via ``sources`` only. It does NOT use the legacy
    ``raw_files`` table (whose FK on ``variables`` is incompatible with the
    CY_* indicator codes — cycle observations live in their own table).
    """
    target_dir = data_raw_dir / "worldbank_cycles"
    target_dir.mkdir(parents=True, exist_ok=True)

    raw = _fetch_wb(country, indicator, api_base)
    raw_path = target_dir / f"{country}_{indicator}_run{run_id}.csv"
    raw.to_csv(raw_path, index=False)

    source_id = upsert_source(
        con, provider="WORLD_BANK", dataset_name=dataset_name,
        series_id=f"{country}/{indicator}",
        url=f"{api_base.rstrip('/')}/country/{country}/indicator/{indicator}",
        license_notes=license_notes, access_method="api_json",
    )

    if raw.empty:
        return pd.Series(dtype=float, name=f"{country}/{indicator}"), source_id
    series = pd.Series(raw["value"].values, index=raw["year"].astype(int).values,
                       name=f"{country}/{indicator}")
    return series.sort_index(), source_id


def aggregate_to_group(country_series: dict[str, pd.Series],
                       gdp_weights: dict[str, pd.Series] | None,
                       method: str = "gdp_weighted") -> pd.Series:
    """Aggregate a dict of country → annual Series into a single group series.

    For ``method == "gdp_weighted"`` we need per-country annual GDP (current USD)
    in ``gdp_weights``. If a country lacks a GDP value for a year, it's excluded
    from that year's weighting. Falls back to equal-weighting if no weights
    are available.
    """
    if not country_series:
        return pd.Series(dtype=float)
    df = pd.DataFrame(country_series)
    if method == "gdp_weighted" and gdp_weights:
        w_df = pd.DataFrame(gdp_weights).reindex_like(df)
        mask = df.notna() & w_df.notna() & (w_df > 0)
        w_eff = w_df.where(mask, other=0.0)
        v_eff = df.where(mask, other=0.0)
        denom = w_eff.sum(axis=1)
        numer = (v_eff * w_eff).sum(axis=1)
        out = (numer / denom).where(denom > 0, other=pd.NA)
        return out.astype(float)
    # Equal-weight fallback (or method == "equal").
    return df.mean(axis=1, skipna=True)


def value_transform(series: pd.Series, transform: str) -> pd.Series:
    """Apply a pre-registered transform: level / pct_change / log / log_diff."""
    import numpy as np
    if transform == "pct_change":
        return series.pct_change()
    if transform == "log":
        return pd.Series(np.log(series.astype(float)), index=series.index)
    if transform == "log_diff":
        return pd.Series(np.log(series.astype(float)), index=series.index).diff()
    return series


def build_group_panel(specs: list[CycleSpec], group_code: str, api_base: str,
                      data_raw_dir: Path, con: sqlite3.Connection,
                      run_id: int, start_year: int = 1960) -> pd.DataFrame:
    """Build the per-group annual panel: rows=year, columns=variable_code (post-transform).

    Also persists raw values into ``cycle_observations`` (post-transform values
    are NOT persisted there — that table holds the raw signal so transforms can
    be replayed downstream).
    """
    if group_code not in GROUPS:
        raise ValueError(f"Unknown group_code {group_code}")
    countries = GROUPS[group_code]

    gdp_per_country: dict[str, pd.Series] = {}
    panels: dict[str, pd.Series] = {}

    # 1) GDP weights — only fetched when we have to aggregate across countries.
    if len(countries) > 1:
        for c in countries:
            try:
                gdp_series, _src = fetch_country_series(
                    c, GDP_INDICATOR_FOR_WEIGHTING, api_base, data_raw_dir,
                    con, run_id, variable_code="CY_GDP_W",
                    dataset_name="GDP (current USD) — aggregation weight",
                )
                gdp_per_country[c] = gdp_series
            except Exception:  # noqa: BLE001
                gdp_per_country[c] = pd.Series(dtype=float)

    # 2) For each variable, fetch per-country and aggregate to the group.
    for spec in specs:
        country_series: dict[str, pd.Series] = {}
        for c in countries:
            try:
                series, source_id = fetch_country_series(
                    c, spec.series_id, api_base, data_raw_dir, con, run_id,
                    variable_code=spec.variable_code,
                    dataset_name=spec.dataset_name,
                    license_notes=spec.license_notes,
                )
                # Persist raw observations under the group_code that was requested
                # (one country contributes — keyed by year). For multi-country
                # groups, we persist the per-country values too so downstream
                # synthesis can replay.
                effective_group = group_code if len(countries) == 1 else f"{group_code}:{c}"
                for year, value in series.items():
                    if year < start_year:
                        continue
                    upsert_cycle_observation(
                        con, effective_group, spec.variable_code,
                        int(year), float(value) if pd.notna(value) else None, source_id,
                    )
                country_series[c] = series
            except Exception:  # noqa: BLE001
                country_series[c] = pd.Series(dtype=float)
        if len(countries) == 1:
            group_series = next(iter(country_series.values()))
        else:
            group_series = aggregate_to_group(country_series, gdp_per_country,
                                              method="gdp_weighted")
            # Persist the aggregated series too.
            for year, value in group_series.items():
                if year < start_year or pd.isna(value):
                    continue
                upsert_cycle_observation(con, group_code, spec.variable_code,
                                          int(year), float(value), None)
        panels[spec.variable_code] = value_transform(group_series, spec.value_transform)

    con.commit()
    if not panels:
        return pd.DataFrame()
    df = pd.DataFrame(panels)
    df = df[df.index >= start_year].sort_index()
    return df
