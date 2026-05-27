from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import requests

from ecowave.db import register_raw_file, upsert_source
from ecowave.ingest.manifest import IngestionSpec

DEFAULT_COUNTRY = "WLD"  # World aggregate


def fetch_worldbank_indicator(country: str, indicator: str, api_base: str) -> pd.DataFrame:
    """Fetch a World Bank indicator as a [date, value] DataFrame (annual)."""
    if not api_base:
        raise ValueError("WORLD_BANK_API_BASE is required.")
    url = f"{api_base.rstrip('/')}/country/{country}/indicator/{indicator}"
    response = requests.get(url, params={"format": "json", "per_page": 20000}, timeout=60)
    response.raise_for_status()
    data = response.json()
    rows = data[1] if isinstance(data, list) and len(data) > 1 else []
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=["date", "value"])
    out = pd.DataFrame({
        "date": df["date"].astype(str),
        "value": pd.to_numeric(df["value"], errors="coerce"),
    })
    return out.dropna().reset_index(drop=True)


def ingest_worldbank_variable(spec: IngestionSpec, api_base: str, data_raw_dir: Path,
                              con: sqlite3.Connection, run_id: int,
                              country: str = DEFAULT_COUNTRY) -> tuple[pd.Series, int]:
    """Fetch a World Bank indicator, persist the raw payload and return an annual
    month-indexed Series (each year mapped to its December)."""
    target_dir = data_raw_dir / "worldbank"
    target_dir.mkdir(parents=True, exist_ok=True)

    raw = fetch_worldbank_indicator(country, spec.series_id, api_base)
    raw_path = target_dir / f"{country}_{spec.series_id}_run{run_id}.csv"
    raw.to_csv(raw_path, index=False)
    register_raw_file(con, run_id, spec.variable_code, raw_path)

    source_id = upsert_source(
        con, provider="WORLD_BANK", dataset_name=spec.dataset_name,
        series_id=f"{country}/{spec.series_id}",
        url=f"{api_base.rstrip('/')}/country/{country}/indicator/{spec.series_id}",
        license_notes=spec.license_notes, access_method="api_json",
    )

    # Annual values: map each year Y to month "Y-12" so pct_change/z-score work on a
    # consistent monthly index (sparse, like quarterly GDP).
    series = pd.Series(raw["value"].values, index=[f"{y}-12" for y in raw["date"]])
    series = series[~series.index.duplicated(keep="last")].sort_index()
    return series, source_id
