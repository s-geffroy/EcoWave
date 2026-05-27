from __future__ import annotations

import sqlite3
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

from ecowave.db import register_raw_file, upsert_source
from ecowave.ingest.manifest import IngestionSpec
from ecowave.normalize.monthly import daily_to_monthly


def fetch_ecb_sdmx(api_base: str, series_key: str) -> pd.DataFrame:
    """Fetch an ECB Data Portal SDMX series as CSV.

    series_key form: '<DATAFLOW>/<KEY>' e.g. 'CISS/D.U2.Z0Z.4F.EC.SS_CIN.IDX'.
    Returns a DataFrame with columns [date, value].
    """
    if not api_base:
        raise ValueError("ECB_API_BASE is required.")
    if "/" not in series_key:
        raise ValueError("series_key must be '<DATAFLOW>/<KEY>'")
    dataflow, key = series_key.split("/", 1)
    url = f"{api_base.rstrip('/')}/data/{dataflow}/{key}"
    response = requests.get(url, params={"format": "csvdata"}, timeout=60,
                            headers={"Accept": "text/csv"})
    response.raise_for_status()
    frame = pd.read_csv(StringIO(response.text))
    # ECB CSV uses TIME_PERIOD and OBS_VALUE columns.
    date_col = "TIME_PERIOD" if "TIME_PERIOD" in frame.columns else frame.columns[-2]
    value_col = "OBS_VALUE" if "OBS_VALUE" in frame.columns else frame.columns[-1]
    out = pd.DataFrame({
        "date": pd.to_datetime(frame[date_col], errors="coerce"),
        "value": pd.to_numeric(frame[value_col], errors="coerce"),
    })
    return out.dropna().reset_index(drop=True)


def ingest_ecb_variable(spec: IngestionSpec, api_base: str, data_raw_dir: Path,
                        con: sqlite3.Connection, run_id: int) -> tuple[pd.Series, int]:
    target_dir = data_raw_dir / "ecb"
    target_dir.mkdir(parents=True, exist_ok=True)

    raw = fetch_ecb_sdmx(api_base, spec.series_key)
    safe_name = spec.series_key.replace("/", "_").replace(".", "_")
    raw_path = target_dir / f"{safe_name}_run{run_id}.csv"
    raw.to_csv(raw_path, index=False)
    register_raw_file(con, run_id, spec.variable_code, raw_path)

    source_id = upsert_source(
        con, provider="ECB", dataset_name=spec.dataset_name, series_id=spec.series_key,
        url=f"{api_base.rstrip('/')}/data/{spec.series_key}",
        license_notes=spec.license_notes, access_method="sdmx_csv",
    )

    monthly = daily_to_monthly(raw)
    column = {"avg": "monthly_avg", "max": "monthly_max", "min": "monthly_min", "last": "monthly_last"}.get(spec.monthly_agg, "monthly_avg")
    return monthly.set_index("month")[column], source_id
