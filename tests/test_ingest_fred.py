from __future__ import annotations

import pandas as pd
import pytest

import ecowave.ingest.fred as fred
from ecowave.db import connect, start_ingestion_run
from ecowave.ingest.manifest import IngestionSpec


def test_fetch_fred_parses_missing_dots(monkeypatch):
    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"observations": [
                {"date": "2008-01-01", "value": "20.5"},
                {"date": "2008-01-02", "value": "."},
            ]}

    monkeypatch.setattr(fred.requests, "get", lambda *a, **k: FakeResp())
    df = fred.fetch_fred_series("VIXCLS", "real-key")
    assert list(df.columns) == ["date", "value"]
    assert len(df) == 1  # the '.' row is dropped


def test_fetch_fred_requires_key():
    with pytest.raises(ValueError):
        fred.fetch_fred_series("VIXCLS", "replace_me")


def test_ingest_fred_variable_persists_raw(monkeypatch, initialized_db, tmp_path):
    daily = pd.DataFrame({
        "date": pd.to_datetime(["2008-01-02", "2008-01-15", "2008-02-10"]),
        "value": [20.0, 30.0, 25.0],
    })
    monkeypatch.setattr(fred, "fetch_fred_series", lambda *a, **k: daily)

    con = connect(initialized_db)
    try:
        run_id = start_ingestion_run(con, mode="strict")
        spec = IngestionSpec(
            variable_code="E1", provider="FRED", dataset_name="VIX", monthly_agg="avg",
            value_transform="level", stress_orientation="higher_is_stress", confidence="A",
            series_id="VIXCLS",
        )
        series, source_id = fred.ingest_fred_variable(spec, "real-key", tmp_path, con, run_id)
        raw_files = con.execute("SELECT path FROM raw_files WHERE ingestion_run_id=?", (run_id,)).fetchall()
    finally:
        con.close()

    assert series["2008-01"] == 25.0  # mean of 20 and 30
    assert source_id > 0
    assert len(raw_files) == 1
    assert (tmp_path / "fred" / f"VIXCLS_run{run_id}.csv").exists()
