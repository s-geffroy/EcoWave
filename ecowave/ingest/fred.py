from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import requests

from ecowave.config import is_placeholder
from ecowave.db import register_raw_file, upsert_source
from ecowave.ingest.manifest import IngestionSpec
from ecowave.normalize.monthly import daily_to_monthly

FRED_OBSERVATIONS_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_fred_series(series_id: str, api_key: str, observation_start: str = "1990-01-01") -> pd.DataFrame:
    if is_placeholder(api_key):
        raise ValueError("FRED_API_KEY is required.")
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": observation_start,
    }
    response = requests.get(FRED_OBSERVATIONS_URL, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()
    observations = payload.get("observations", [])
    df = pd.DataFrame(observations)
    if df.empty:
        return pd.DataFrame(columns=["date", "value"])
    df["value"] = pd.to_numeric(df["value"].replace(".", None), errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    return df[["date", "value"]].dropna(subset=["value"]).reset_index(drop=True)


def _monthly_value(daily_or_periodic: pd.DataFrame, agg: str) -> pd.Series:
    """Return a month-indexed Series for the requested aggregation."""
    monthly = daily_to_monthly(daily_or_periodic)
    column = {"avg": "monthly_avg", "max": "monthly_max", "min": "monthly_min", "last": "monthly_last"}.get(agg, "monthly_avg")
    return monthly.set_index("month")[column]


def ingest_fred_variable(spec: IngestionSpec, api_key: str, data_raw_dir: Path,
                         con: sqlite3.Connection, run_id: int,
                         observation_start: str = "1990-01-01") -> tuple[pd.Series, int]:
    """Fetch, persist raw payload (versioned by run_id) and return (monthly Series, source_id)."""
    target_dir = data_raw_dir / "fred"
    target_dir.mkdir(parents=True, exist_ok=True)

    raw = fetch_fred_series(spec.series_id, api_key, observation_start)
    raw_path = target_dir / f"{spec.series_id}_run{run_id}.csv"
    raw.to_csv(raw_path, index=False)
    register_raw_file(con, run_id, spec.variable_code, raw_path)

    source_id = upsert_source(
        con, provider="FRED", dataset_name=spec.dataset_name, series_id=spec.series_id,
        url=f"{FRED_OBSERVATIONS_URL}?series_id={spec.series_id}",
        license_notes=spec.license_notes, access_method="api_json",
    )

    if spec.provider == "FRED_SPREAD" and spec.minus_series_id:
        minus_raw = fetch_fred_series(spec.minus_series_id, api_key, observation_start)
        minus_path = target_dir / f"{spec.minus_series_id}_run{run_id}.csv"
        minus_raw.to_csv(minus_path, index=False)
        register_raw_file(con, run_id, spec.variable_code, minus_path)
        left = _monthly_value(raw, spec.monthly_agg)
        right = _monthly_value(minus_raw, spec.monthly_agg)
        series = (left - right).dropna()
        return series, source_id

    return _monthly_value(raw, spec.monthly_agg), source_id
