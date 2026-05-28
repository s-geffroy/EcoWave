"""Quarterly cycle ingestion: FRED + Eurostat + OECD QNA.

This is the "quarterly horizon" data path used by ``position-cycles --horizon
quarterly``. It complements (does not replace) the WB annual panel and the
Maddison + JST long-history panel:

- WB annual         → Kitchin (3-5 y) is **rejected** everywhere (Nyquist).
- Long-history annual → 154 y deep, but still annual; same Kitchin limit.
- **Quarterly (here)** → samples_per_year = 4. The Christiano-Fitzgerald
  filter on the full Kitchin band 3-5 y now sees 12-20 samples per period —
  well above the practical Nyquist threshold. This unlocks Item #9 of the
  methodology roadmap (``methodology/feuille_de_route.md``).

Data sources (v1, three variables)
----------------------------------
- ``Q_GDP``    — FRED ``GDPC1`` for US; Eurostat ``namq_10_gdp`` for the
  Euro Area aggregate (EA20, 1995+) and for DE/FR/IT; OECD QNA
  (``B1_GE/VOBARSA``) for JPN/GBR/CAN.
- ``Q_CPI``    — FRED ``CPIAUCSL`` (monthly → quarterly mean) for US;
  Eurostat ``prc_hicp_mmor`` for the EA aggregate; OECD ``CPI_T/IXOB`` for
  JPN/GBR.
- ``Q_UNRATE`` — FRED ``UNRATE`` (monthly → quarterly mean) for US;
  Eurostat ``une_rt_q`` for EA; OECD ``LRHUTTTT/STSA`` for JPN/GBR.

Raw payloads are cached under ``data_raw/{fred,eurostat,oecd}/`` versioned
by ``run_id`` and registered as ``sources`` rows for provenance.
"""
from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

import numpy as np
import pandas as pd
import requests

from ecowave.ingest.fred import fetch_fred_series

# Country sets eligible for the quarterly panel: each member must publish
# real GDP at quarterly frequency continuously since 1960 (USA, JPN, GBR,
# CAN, DEU, FRA, ITA), since 1995 for the Euro Area aggregate (EA20), or
# since 1970+ for the OECD-extended set (ESP, AUS, KOR, NLD, …).
QUARTERLY_GROUPS = MappingProxyType({
    "USA":   ("USA",),
    "EA":    ("EA",),
    "JPN":   ("JPN",),
    "GBR":   ("GBR",),
    "G7Q":   ("USA", "GBR", "CAN", "JPN", "DEU", "FRA", "ITA"),
    "OECDQ": ("USA", "GBR", "CAN", "JPN", "DEU", "FRA", "ITA",
              "ESP", "AUS", "KOR", "NLD", "BEL", "SWE",
              "CHE", "NOR", "DNK", "FIN", "AUT"),
})

EUROSTAT_BASE = (
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
)
OECD_BASE = "https://sdmx.oecd.org/public/rest/data"


@dataclass(frozen=True)
class QuarterlyDataset:
    fred_dir: Path
    eurostat_dir: Path
    oecd_dir: Path

    @classmethod
    def default(cls, data_raw_dir: Path) -> "QuarterlyDataset":
        return cls(
            fred_dir=data_raw_dir / "fred",
            eurostat_dir=data_raw_dir / "eurostat",
            oecd_dir=data_raw_dir / "oecd",
        )

    def ensure_dirs(self) -> None:
        for p in (self.fred_dir, self.eurostat_dir, self.oecd_dir):
            p.mkdir(parents=True, exist_ok=True)


# --- Provider fetchers --------------------------------------------------

def fetch_fred_quarterly(series_id: str, api_key: str, cache_dir: Path,
                         run_id: int,
                         observation_start: str = "1947-01-01") -> pd.Series:
    """Fetch a FRED series and return a quarterly Series.

    Monthly series (CPIAUCSL, UNRATE) are resampled to Q via mean; native
    quarterly series (GDPC1) keep their period. Output index is
    ``PeriodIndex(freq="Q")``.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    raw = fetch_fred_series(series_id, api_key, observation_start)
    raw_path = cache_dir / f"{series_id}_run{run_id}.csv"
    raw.to_csv(raw_path, index=False)
    if raw.empty:
        return pd.Series(dtype=float, name=series_id)
    s = pd.Series(raw["value"].values,
                  index=pd.to_datetime(raw["date"]).values, name=series_id)
    # mean over the months that fall in each quarter; native-quarterly
    # series have one observation per quarter so mean is a no-op.
    q = s.resample("QE").mean()
    q.index = q.index.to_period("Q")
    return q


def _eurostat_url(dataset: str, dims: dict[str, str]) -> str:
    """Build a JSON-stat 2.0 URL for an Eurostat dataset query.

    The ``statistics/1.0/data`` REST endpoint accepts named filters and
    returns a JSON-stat 2.0 document — much simpler than the SDMX 2.1
    positional-key path. Returns the full URL with ``?format=JSON``.
    """
    parts = [f"{k}={v}" for k, v in dims.items()]
    parts.append("format=JSON")
    return f"{EUROSTAT_BASE}/{dataset}?{'&'.join(parts)}"


def _eurostat_extract(payload: dict) -> pd.DataFrame:
    """Convert an Eurostat JSON-stat 2.0 payload into DataFrame[period, value].

    Eurostat's ``statistics/1.0/data`` endpoint returns JSON-stat 2.0:
    ``value`` is either a sparse dict ``{"0": 1.23, "12": 4.56, …}`` or a
    dense list ``[1.23, null, 4.56, …]``; the keys/positions decode against
    ``dimension.time.category.index``. For univariate time-series queries
    (the only kind this module submits), only the ``time`` dimension varies,
    so the cell index *is* the time index.
    """
    if not payload or "value" not in payload:
        return pd.DataFrame(columns=["period", "value"])
    dim = payload.get("dimension", {})
    time_dim = dim.get("time", {}).get("category", {})
    time_labels = time_dim.get("index", {})
    # `time_labels` is {"1995Q1": 0, "1995Q2": 1, …}; invert it.
    idx_to_label = {v: k for k, v in time_labels.items()}
    values = payload["value"]
    if isinstance(values, dict):
        pairs = [(int(k), v) for k, v in values.items()]
    else:
        pairs = [(i, v) for i, v in enumerate(values) if v is not None]
    rows = [(idx_to_label[i], v) for i, v in pairs if i in idx_to_label]
    df = pd.DataFrame(rows, columns=["period", "value"])
    return df.sort_values("period").reset_index(drop=True)


def fetch_eurostat_qna(dataset: str, dims: dict[str, str], cache_dir: Path,
                       run_id: int, max_retries: int = 3,
                       backoff: float = 1.5) -> pd.Series:
    """Fetch one Eurostat quarterly series and return a Series with PeriodIndex(Q).

    ``dims`` is the SDMX dimension filter (e.g. ``{"geo": "EA20", "na_item":
    "B1GQ", "unit": "CLV10_MEUR", "s_adj": "SCA"}``). Raw JSON is cached
    versioned by run_id under ``cache_dir``.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    url = _eurostat_url(dataset, dims)
    last_exc: Exception | None = None
    payload: dict | None = None
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            payload = response.json()
            break
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(backoff ** attempt)
    if payload is None:
        raise RuntimeError(
            f"Eurostat fetch failed for {dataset} {dims}: {last_exc}"
        )
    tag = f"{dataset}_{'_'.join(dims.values())}"
    (cache_dir / f"{tag}_run{run_id}.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )
    df = _eurostat_extract(payload)
    if df.empty:
        return pd.Series(dtype=float, name=tag)
    # Eurostat encodes quarters as "1995Q1", "1995Q2", …
    period = pd.PeriodIndex(df["period"], freq="Q")
    return pd.Series(df["value"].astype(float).values, index=period, name=tag)


def _oecd_extract(payload: dict) -> pd.DataFrame:
    """Tidy extractor for OECD SDMX-JSON v2 payloads (sdmx.oecd.org).

    When several series match the key (wildcards in unknown dimensions), we
    return the row-stacked frame and let the caller pick — typically by
    longest history or by dropping series with all-NaN values.
    """
    if not payload:
        return pd.DataFrame(columns=["series", "period", "value"])
    try:
        series = payload["data"]["dataSets"][0]["series"]
        time_dim = payload["data"]["structure"]["dimensions"]["observation"][0]
        time_values = [v["id"] for v in time_dim["values"]]
    except (KeyError, IndexError):
        return pd.DataFrame(columns=["series", "period", "value"])
    rows: list[tuple[str, str, float]] = []
    for series_key, ser in series.items():
        for k, obs in ser.get("observations", {}).items():
            idx = int(k)
            if 0 <= idx < len(time_values):
                rows.append((series_key, time_values[idx], float(obs[0])))
    return pd.DataFrame(rows, columns=["series", "period", "value"]).sort_values(
        ["series", "period"]
    ).reset_index(drop=True)


def _oecd_dsd_dimensions(dataflow: str, cache_dir: Path) -> list[str]:
    """Discover the positional dimension order of an OECD DSD.

    OECD's SDMX 2.1 endpoint at ``sdmx.oecd.org`` requires the data key
    to be a dot-separated positional list of dim values in the exact order
    of the DSD. The order is dataflow-specific and changes occasionally —
    so instead of hard-coding it (which breaks every time OECD restructures
    a codelist), we fetch the DSD once and parse the dimension list.

    Cached on disk under ``cache_dir`` to avoid re-fetching on every call.
    """
    # The OECD dataflow ref ``agency,DSD_X@DF_Y,version`` packs both the
    # DSD id (DSD_X) and the dataflow id (DF_Y) into one comma-separated
    # string. Two endpoints can carry the DSD:
    #   1. ``/structure/dataflow/{agency}/{id}/{version}?references=descendants``
    #   2. ``/dataflow/{agency}/{id}/{version}?references=descendants``
    # The OECD installation exposes both at different times — we probe (1)
    # first and fall back to (2) on 404/empty. The structure payload then
    # lives under either ``data.dataStructures`` (SDMX-JSON 1.0) or
    # ``Structure.Structures.DataStructures`` (SDMX-ML-style 2.0). We try
    # both shapes before raising.
    parts = dataflow.split(",")
    agency = parts[0]
    raw_dsd = parts[1] if len(parts) > 1 else "DSD_NAMAIN1@DF_QNA"
    if "@" in raw_dsd:
        dsd_id, dataflow_id = raw_dsd.split("@", 1)
    else:
        dsd_id, dataflow_id = raw_dsd, raw_dsd
    version = parts[2] if len(parts) > 2 else "1.0"

    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"dsd_{agency}_{dataflow_id}_{version}.json"
    if cache_file.exists():
        payload = json.loads(cache_file.read_text(encoding="utf-8"))
    else:
        candidate_urls = [
            (f"https://sdmx.oecd.org/public/rest/dataflow/{agency}"
             f"/{dataflow_id}/{version}?references=descendants"),
            (f"https://sdmx.oecd.org/public/rest/structure/dataflow/{agency}"
             f"/{dataflow_id}/{version}?references=descendants"),
            (f"https://sdmx.oecd.org/public/rest/datastructure/{agency}"
             f"/{dsd_id}/{version}?references=descendants"),
        ]
        payload = None
        last_status = None
        for url in candidate_urls:
            response = requests.get(
                url, headers={"Accept": "application/json"}, timeout=60,
            )
            last_status = response.status_code
            if response.status_code == 200:
                candidate = response.json()
                # Reject the empty-resource sentinel that some OECD endpoints
                # return when the ID exists at the route but resolves to no
                # structure (``{"resources": [], "references": {}}``).
                if (candidate.get("dataStructures")
                        or "data" in candidate
                        or "Structure" in candidate
                        or candidate.get("resources")):
                    payload = candidate
                    break
        if payload is None:
            raise RuntimeError(
                f"OECD structure registry returned no DSD for {dataflow} "
                f"(last HTTP status: {last_status}). Tried "
                f"{len(candidate_urls)} endpoint variants."
            )
        cache_file.write_text(json.dumps(payload), encoding="utf-8")

    # Walk a small set of known SDMX-JSON shapes to find the dimension list.
    candidates: list = []
    body_data = payload.get("data", payload)
    candidates.extend(body_data.get("dataStructures", []))
    # SDMX-ML-style nested under ``Structure.Structures.DataStructures``
    sml_root = (payload.get("Structure", {}).get("Structures", {})
                .get("DataStructures", {}))
    if isinstance(sml_root, dict):
        candidates.extend(sml_root.get("DataStructure", []) or [])

    dim_list = None
    for ds in candidates:
        comps = (ds.get("dataStructureComponents")
                 or ds.get("DataStructureComponents") or {})
        dim_block = (comps.get("dimensionList")
                     or comps.get("DimensionList") or {})
        dim_list = dim_block.get("dimensions") or dim_block.get("Dimension")
        if dim_list:
            break
    if not dim_list:
        raise RuntimeError(
            f"Unexpected OECD DSD payload for {dataflow}: "
            f"no dimension list in any known SDMX-JSON shape."
        )
    # Each dimension has an integer ``position`` (1-indexed) and an ``id``.
    ordered = sorted(
        dim_list,
        key=lambda d: int(d.get("position", d.get("Position", 999))),
    )
    return [d.get("id") or d.get("Id") or d.get("@id") for d in ordered]


def _build_oecd_key(dataflow: str, dims: dict[str, str],
                    cache_dir: Path) -> tuple[str, list[str]]:
    """Build the positional SDMX key from a {dim_id: value} dict.

    Unknown dimensions in ``dims`` are left as wildcards (empty segments)
    which the OECD endpoint interprets as "any value". Returns
    ``(key, dim_order)`` where ``dim_order`` is the discovered DSD order so
    callers can decode response series keys.
    """
    dim_order = _oecd_dsd_dimensions(dataflow, cache_dir)
    parts = [dims.get(d, "") for d in dim_order]
    return ".".join(parts), dim_order


def fetch_oecd_qna(dims: dict[str, str], cache_dir: Path, run_id: int,
                   dataflow: str = "OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA,1.0",
                   max_retries: int = 3, backoff: float = 1.5) -> pd.Series:
    """Fetch one OECD QNA series and return a Series with PeriodIndex(Q).

    Uses the SDMX 2.1 REST endpoint at ``sdmx.oecd.org`` (the legacy
    ``stats.oecd.org`` was deprecated in 2024). ``dims`` is a dict of
    dimension ID → value, e.g. ``{"REF_AREA": "JPN", "MEASURE": "B1GQ",
    "FREQ": "Q", "PRICE_BASE": "L"}``. The positional key is built
    automatically from the DSD's discovered dimension order.

    If the wildcarded key returns several series, the one with the longest
    non-NaN history is selected.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    key, _dim_order = _build_oecd_key(dataflow, dims, cache_dir)
    url = (f"{OECD_BASE}/{dataflow}/{key}"
           "?dimensionAtObservation=AllDimensions")
    last_exc: Exception | None = None
    payload: dict | None = None
    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                headers={"Accept": "application/vnd.sdmx.data+json;version=1.0.0"},
                timeout=60,
            )
            response.raise_for_status()
            payload = response.json()
            break
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(backoff ** attempt)
    if payload is None:
        raise RuntimeError(
            f"OECD QNA fetch failed for dims={dims}: {last_exc}"
        )
    tag = "_".join(f"{k}={v}" for k, v in dims.items())
    (cache_dir / f"{tag}_run{run_id}.json".replace("/", "_")).write_text(
        json.dumps(payload), encoding="utf-8"
    )
    df = _oecd_extract(payload)
    if df.empty:
        return pd.Series(dtype=float, name=tag)
    # Multiple series may match wildcards — keep the longest one.
    counts = df.groupby("series")["value"].count()
    best = counts.idxmax()
    sub = df[df["series"] == best]
    period = pd.PeriodIndex(sub["period"], freq="Q")
    return pd.Series(sub["value"].astype(float).values, index=period, name=tag)


# --- Transform + aggregation -------------------------------------------

def value_transform_q(series: pd.Series, transform: str) -> pd.Series:
    """Pre-registered quarterly transforms.

    - ``level``      — pass-through (already stationary, e.g. UNRATE).
    - ``pct_change_q`` — quarter-on-quarter growth.
    - ``log_diff_q`` — annualised log-difference (4 × Δlog), the standard
      stationarising transform for real GDP and CPI on quarterly grids.
    """
    if transform == "pct_change_q":
        return series.pct_change()
    if transform == "log_diff_q":
        return np.log(series.astype(float)).diff() * 4.0
    return series


def _gdp_weighted_aggregate(per_country: dict[str, pd.Series],
                            gdp_weights: dict[str, pd.Series] | None,
                            ) -> pd.Series:
    """GDP-weighted group aggregation on the quarterly grid.

    Falls back to equal-weighting if no GDP weights are available. Quarters
    missing a country's value (or a weight) drop that country from the
    weighting for that quarter only.
    """
    if not per_country:
        return pd.Series(dtype=float)
    df = pd.DataFrame(per_country)
    if gdp_weights:
        w_df = pd.DataFrame(gdp_weights).reindex_like(df)
        mask = df.notna() & w_df.notna() & (w_df > 0)
        w_eff = w_df.where(mask, other=0.0)
        v_eff = df.where(mask, other=0.0)
        denom = w_eff.sum(axis=1)
        numer = (v_eff * w_eff).sum(axis=1)
        out = (numer / denom).where(denom > 0, other=pd.NA)
        return out.astype(float)
    return df.mean(axis=1, skipna=True)


def _dispatch_fetch(provider_cfg: dict, country: str, dataset: QuarterlyDataset,
                    fred_api_key: str, run_id: int) -> pd.Series:
    """Resolve one (country, variable) → quarterly Series via the right provider.

    ``provider_cfg`` is the per-country dict from the manifest, e.g.
    ``{"src": "FRED", "series": "GDPC1"}``.
    """
    src = provider_cfg["src"]
    if src == "FRED":
        return fetch_fred_quarterly(
            provider_cfg["series"], fred_api_key, dataset.fred_dir, run_id,
        )
    if src == "EUROSTAT":
        dims = {k: v for k, v in provider_cfg.items()
                if k not in {"src", "dataset"}}
        return fetch_eurostat_qna(
            provider_cfg["dataset"], dims, dataset.eurostat_dir, run_id,
        )
    if src == "OECD":
        dims = dict(provider_cfg.get("dims", {}))
        # Convenience: when REF_AREA isn't pinned in the manifest, fill it
        # from the per-country position so a single provider entry can serve
        # multiple countries by overriding REF_AREA at dispatch time.
        dims.setdefault("REF_AREA", country)
        return fetch_oecd_qna(
            dims, dataset.oecd_dir, run_id,
            dataflow=provider_cfg.get(
                "dataflow", "OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA,1.0",
            ),
        )
    raise ValueError(f"Unknown provider src: {src}")


def build_quarterly_panel(group_code: str,
                          variable_specs: list[dict],
                          dataset: QuarterlyDataset,
                          fred_api_key: str,
                          start_year: int = 1960,
                          run_id: int = 0,
                          persist: dict | None = None,
                          gdp_variable: str = "Q_GDP") -> pd.DataFrame:
    """Build the per-group quarterly panel.

    Returns DataFrame indexed by ``PeriodIndex(freq="Q")``, one column per
    ``variable_code``. Each column is the GDP-weighted aggregate across the
    countries in the group (or the single-country series for ``USA``,
    ``EA``, ``JPN``, ``GBR``).

    ``variable_specs`` is the ``variable_codes`` list from the manifest;
    each spec must carry a ``providers`` map keyed by ISO3 country code
    (plus the special ``EA`` aggregate).

    ``persist`` (optional) — when provided with ``{"con": sqlite3.Connection,
    "source_id": int|None}``, the aggregated group-level series is upserted
    into ``cycle_observations_quarterly``.
    """
    if group_code not in QUARTERLY_GROUPS:
        raise ValueError(
            f"Unknown quarterly group {group_code}; "
            f"available: {list(QUARTERLY_GROUPS)}"
        )
    dataset.ensure_dirs()
    countries = QUARTERLY_GROUPS[group_code]

    # 1) Fetch every (variable, country) — including GDP for weighting.
    raw_per_var: dict[str, dict[str, pd.Series]] = {}
    fetch_failures: list[tuple[str, str, str]] = []
    for spec in variable_specs:
        var = spec["variable_code"]
        providers = spec.get("providers", {})
        per_country: dict[str, pd.Series] = {}
        for country in countries:
            cfg = providers.get(country)
            if cfg is None:
                continue
            try:
                series = _dispatch_fetch(cfg, country, dataset,
                                          fred_api_key, run_id)
            except Exception as exc:  # noqa: BLE001
                series = pd.Series(dtype=float)
                fetch_failures.append((var, country, str(exc)[:120]))
            per_country[country] = series
        raw_per_var[var] = per_country

    if fetch_failures:
        import sys
        print(
            f"  [quarterly] {group_code}: {len(fetch_failures)} fetch failures "
            f"(group still built from the remaining countries).",
            file=sys.stderr,
        )
        for var, country, msg in fetch_failures[:6]:
            print(f"    - {var}/{country}: {msg}", file=sys.stderr)

    # 2) GDP-level weights = the GDP series itself (we already fetched it).
    gdp_raw = raw_per_var.get(gdp_variable, {})

    # 3) Apply per-variable transform, then aggregate to the group.
    panel: dict[str, pd.Series] = {}
    for spec in variable_specs:
        var = spec["variable_code"]
        transform = spec.get("transform", "level")
        transformed = {c: value_transform_q(s, transform)
                       for c, s in raw_per_var[var].items()}
        weights = gdp_raw if len(countries) > 1 else None
        group_series = _gdp_weighted_aggregate(transformed, weights)
        panel[var] = group_series

    if not panel:
        return pd.DataFrame()
    df = pd.DataFrame(panel)
    # Restrict to start_year-Q1 onwards.
    if not df.empty and isinstance(df.index, pd.PeriodIndex):
        df = df[df.index.year >= start_year].sort_index()

    # 4) Persist the group-level aggregated panel.
    if persist is not None and "con" in persist and not df.empty:
        from ecowave.db import upsert_cycle_observation_quarterly
        con: sqlite3.Connection = persist["con"]
        source_id = persist.get("source_id")
        for period, row in df.iterrows():
            for var, value in row.items():
                if pd.notna(value):
                    upsert_cycle_observation_quarterly(
                        con, group_code, var,
                        int(period.year), int(period.quarter),
                        float(value), source_id,
                    )
        con.commit()

    return df


def load_quarterly_manifest(path: Path) -> dict:
    """Parse the quarterly manifest JSON, returning the raw dict.

    Schema is documented in the project root ``quarterly_manifest.json``.
    """
    return json.loads(path.read_text(encoding="utf-8"))
