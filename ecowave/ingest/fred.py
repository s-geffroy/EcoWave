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


def ingest_fred_monthly(series_id: str, api_key: str, agg: str, variable_code: str,
                        data_raw_dir: Path, con: sqlite3.Connection, run_id: int,
                        observation_start: str = "1990-01-01") -> pd.Series:
    """Fetch one FRED series, persist its raw payload (versioned by run_id) and return monthly values."""
    target_dir = data_raw_dir / "fred"
    target_dir.mkdir(parents=True, exist_ok=True)
    raw = fetch_fred_series(series_id, api_key, observation_start)
    raw_path = target_dir / f"{series_id}_run{run_id}.csv"
    raw.to_csv(raw_path, index=False)
    register_raw_file(con, run_id, variable_code, raw_path)
    return _monthly_value(raw, agg)


def ingest_fred_spread(series_id: str, minus_series_id: str, api_key: str, agg: str,
                       variable_code: str, data_raw_dir: Path, con: sqlite3.Connection,
                       run_id: int, observation_start: str = "1990-01-01") -> pd.Series:
    """Ingest two FRED series and return their monthly difference (series_id - minus_series_id)."""
    left = ingest_fred_monthly(series_id, api_key, agg, variable_code, data_raw_dir, con, run_id, observation_start)
    right = ingest_fred_monthly(minus_series_id, api_key, agg, variable_code, data_raw_dir, con, run_id, observation_start)
    return (left - right).dropna()


def ingest_fred_variable(spec: IngestionSpec, api_key: str, data_raw_dir: Path,
                         con: sqlite3.Connection, run_id: int,
                         observation_start: str = "1990-01-01") -> tuple[pd.Series, int]:
    """Fetch, persist raw payload (versioned by run_id) and return (monthly Series, source_id)."""
    source_id = upsert_source(
        con, provider="FRED", dataset_name=spec.dataset_name, series_id=spec.series_id,
        url=f"{FRED_OBSERVATIONS_URL}?series_id={spec.series_id}",
        license_notes=spec.license_notes, access_method="api_json",
    )

    if spec.provider == "FRED_SPREAD" and spec.minus_series_id:
        series = ingest_fred_spread(spec.series_id, spec.minus_series_id, api_key, spec.monthly_agg,
                                    spec.variable_code, data_raw_dir, con, run_id, observation_start)
        return series, source_id

    series = ingest_fred_monthly(spec.series_id, api_key, spec.monthly_agg, spec.variable_code,
                                 data_raw_dir, con, run_id, observation_start)
    return series, source_id


def ingest_fred_components(spec: IngestionSpec, api_key: str, data_raw_dir: Path,
                           con: sqlite3.Connection, run_id: int,
                           observation_start: str = "1990-01-01") -> tuple[list[tuple[str, pd.Series]], int]:
    """Ingest a composite variable: return [(value_transform, monthly Series), ...] and a source_id."""
    source_id = upsert_source(
        con, provider="FRED", dataset_name=spec.dataset_name, series_id=spec.variable_code,
        url=FRED_OBSERVATIONS_URL, license_notes=spec.license_notes, access_method="api_json_composite",
    )
    components: list[tuple[str, pd.Series]] = []
    for comp in spec.components:
        if comp.minus_series_id:
            series = ingest_fred_spread(comp.series_id, comp.minus_series_id, api_key, spec.monthly_agg,
                                        spec.variable_code, data_raw_dir, con, run_id, observation_start)
        else:
            series = ingest_fred_monthly(comp.series_id, api_key, spec.monthly_agg, spec.variable_code,
                                         data_raw_dir, con, run_id, observation_start)
        components.append((comp.value_transform, series))
    return components, source_id
