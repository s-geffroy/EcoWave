"""Sectoral history — Phase 3 substitute for Mitchell IHS via open sources.

Roadmap #13 Phase 3 (2026-05). Tests Wen (2005)'s central claim that
Kitchin (3-5y) survives on sector-specific inventory / production series
but not on macro composites. Uses three open-source providers:

  - **FRED** (NBER Macrohistory + BLS PPI, CC0 public domain) for US series:
    WPI, industrial production, coal, steel, pig iron, rail freight, wheat,
    cotton — covering 50-160 years annual where the underlying source allows.
  - **OWID grapher** (CC BY 4.0) for world coal and oil production 1900+.
  - **OWID legacy GitHub** + DECC/BEIS for UK coal 1700-2019 (annual from 1913).

Springer Palgrave Mitchell IHS access is NOT required — all sources are
freely downloadable via the ``scripts/download_sectoral_history.sh``
bootstrap.

Three aggregate groups:
  - ``US_SH``    : 8 US sectoral variables
  - ``UK_SH``    : UK coal (BEIS 1913-2019)
  - ``WORLD_SH`` : world coal + oil (OWID 1900-2024)
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import typer

from ecowave.db import upsert_cycle_observation


SH_GROUPS: dict[str, tuple[str, ...]] = {
    "US_SH": ("USA",),
    "UK_SH": ("GBR",),
    "WORLD_SH": ("WLD",),
}

# Map each variable_code to its target group (each SH variable belongs to
# exactly one group — US/UK/World partition).
SH_VARIABLE_TO_GROUP: dict[str, str] = {
    "SH_US_WPI": "US_SH", "SH_US_INDPROD": "US_SH",
    "SH_US_COAL": "US_SH", "SH_US_STEEL": "US_SH",
    "SH_US_PIGIRON": "US_SH", "SH_US_RAILFREIGHT": "US_SH",
    "SH_US_WHEAT": "US_SH", "SH_US_COTTON": "US_SH",
    "SH_UK_COAL": "UK_SH",
    "SH_WORLD_COAL": "WORLD_SH", "SH_WORLD_OIL": "WORLD_SH",
}


@dataclass(frozen=True)
class SectoralHistoryDataset:
    """Path to the directory holding all Phase 3 CSV files."""
    csv_dir: Path

    @classmethod
    def default(cls, data_raw_dir: Path) -> "SectoralHistoryDataset":
        return cls(csv_dir=data_raw_dir / "sectoral_history")

    def assert_exists(self) -> None:
        if not self.csv_dir.exists():
            raise FileNotFoundError(
                f"Sectoral history dir not found at {self.csv_dir}.\n"
                "Run inside the container:\n"
                "  bash scripts/download_sectoral_history.sh"
            )


def _annualise(series: pd.Series, freq: str) -> pd.Series:
    """Aggregate monthly → annual by mean (default for level indices and
    flow series alike — preserves the within-year average even when the
    sample mixes months across years)."""
    if freq == "annual":
        return series
    df = series.copy()
    return df.groupby(df.index.year).mean()


def load_fred_csv(path: Path) -> pd.Series:
    """Read a FRED 2-column CSV (observation_date, series_id) → Series indexed
    by ``pd.Timestamp``."""
    df = pd.read_csv(path)
    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    df = df.dropna(subset=["observation_date"])
    val_col = [c for c in df.columns if c != "observation_date"][0]
    return pd.Series(
        pd.to_numeric(df[val_col], errors="coerce").values,
        index=df["observation_date"], name=val_col,
    ).dropna()


def load_owid_grapher_csv(path: Path, entity: str, value_col: str) -> pd.Series:
    """Read an OWID grapher CSV (Entity, Code, Year, Value) → annual Series."""
    df = pd.read_csv(path)
    df = df[df["Entity"] == entity]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["Year", value_col])
    return pd.Series(
        pd.to_numeric(df[value_col], errors="coerce").values,
        index=df["Year"].astype(int), name=value_col,
    ).dropna()


def load_owid_wide_csv(path: Path, entity: str, value_col: str) -> pd.Series:
    """Read an OWID legacy wide CSV (Entity, Year, <multiple value cols>)."""
    df = pd.read_csv(path)
    df = df[df["Entity"] == entity]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    if value_col not in df.columns:
        raise KeyError(f"value_col {value_col!r} not in {list(df.columns)}")
    df = df.dropna(subset=["Year", value_col])
    return pd.Series(
        pd.to_numeric(df[value_col], errors="coerce").values,
        index=df["Year"].astype(int), name=value_col,
    ).dropna()


def _load_one_variable(spec: dict, dataset: SectoralHistoryDataset) -> pd.Series:
    """Dispatch the right loader for one manifest entry and return an
    annual-indexed Series (year → value)."""
    loader = spec["loader"]
    files = [dataset.csv_dir / f for f in spec["files"]]
    freq = spec.get("freq", "annual")
    if loader == "fred":
        s = load_fred_csv(files[0])
        if freq != "annual":
            s = _annualise(s, freq)
        else:
            # FRED annual: index is yyyy-01-01 → take .year
            s = s.copy()
            s.index = s.index.year
        return s
    if loader == "fred_splice":
        # Multiple FRED CSVs — concatenate, annualise, keep last on duplicates.
        parts = []
        for f in files:
            s = load_fred_csv(f)
            # Each may be monthly or annual — annualise via mean.
            s = pd.Series(s.values, index=s.index)  # ensure Timestamp index
            s_ann = s.groupby(s.index.year).mean()
            parts.append(s_ann)
        combined = pd.concat(parts).sort_index()
        # Keep last value on duplicate years (later vintage wins).
        return combined.groupby(combined.index).last()
    if loader == "owid_grapher":
        return load_owid_grapher_csv(files[0], spec["entity"], spec["value_col"])
    if loader == "owid_wide":
        return load_owid_wide_csv(files[0], spec["entity"], spec["value_col"])
    raise ValueError(f"Unknown loader {loader!r} in spec {spec}")


def build_sh_panel(group_code: str, variable_specs: list[dict],
                   dataset: SectoralHistoryDataset, *,
                   start_year: int = 1850,
                   persist: dict | None = None) -> pd.DataFrame:
    """Build a wide-format (year × variable_code) panel for ``group_code``.

    Only variables mapped to ``group_code`` (via ``SH_VARIABLE_TO_GROUP``)
    are included. Series are aligned to a common annual integer index.
    Persists into ``cycle_observations`` so the per-variable evidence
    analysis can recompose without re-reading the CSVs.
    """
    if group_code not in SH_GROUPS:
        raise ValueError(f"Unknown SH group {group_code!r}; "
                          f"expected one of {sorted(SH_GROUPS)}.")
    dataset.assert_exists()

    cols: dict[str, pd.Series] = {}
    for spec in variable_specs:
        cpv_code = spec["variable_code"]
        if SH_VARIABLE_TO_GROUP.get(cpv_code) != group_code:
            continue
        try:
            series = _load_one_variable(spec, dataset)
        except Exception as exc:  # noqa: BLE001
            typer.echo(f"    {cpv_code}: load failed — {exc}", err=True)
            continue
        series = series[series.index >= start_year]
        if series.empty:
            typer.echo(f"    {cpv_code}: no data ≥ {start_year}", err=True)
            continue
        cols[cpv_code] = series
    if not cols:
        return pd.DataFrame()
    panel = pd.DataFrame(cols)
    panel.index.name = "year"
    panel = panel.sort_index()

    if persist is not None and "con" in persist:
        con = persist["con"]
        for cpv_code, ser in cols.items():
            for year, val in ser.items():
                if pd.notna(val):
                    upsert_cycle_observation(
                        con, group_code, cpv_code, int(year),
                        float(val), source_id=None,
                    )
        con.commit()
    return panel


def load_sh_manifest(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
