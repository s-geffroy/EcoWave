from __future__ import annotations

import pandas as pd

import ecowave.ingest.worldbank as wb
from ecowave.db import connect, start_ingestion_run
from ecowave.ingest.manifest import IngestionSpec


def _spec() -> IngestionSpec:
    return IngestionSpec(
        variable_code="L2", provider="WORLD_BANK", dataset_name="World imports volume",
        monthly_agg="last", value_transform="pct_change", stress_orientation="contraction_is_stress",
        confidence="B", series_id="NE.IMP.GNFS.KD",
    )


def test_fetch_worldbank_parses_json(monkeypatch):
    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return [
                {"page": 1},
                [
                    {"date": "2009", "value": "95.0"},
                    {"date": "2008", "value": "100.0"},
                    {"date": "2007", "value": None},
                ],
            ]

    monkeypatch.setattr(wb.requests, "get", lambda *a, **k: FakeResp())
    df = wb.fetch_worldbank_indicator("WLD", "NE.IMP.GNFS.KD", "https://api.worldbank.org/v2")
    assert list(df.columns) == ["date", "value"]
    assert len(df) == 2  # null dropped


def test_ingest_worldbank_maps_years_to_december(monkeypatch, initialized_db, tmp_path):
    raw = pd.DataFrame({"date": ["2008", "2009"], "value": [100.0, 95.0]})
    monkeypatch.setattr(wb, "fetch_worldbank_indicator", lambda *a, **k: raw)

    con = connect(initialized_db)
    try:
        run_id = start_ingestion_run(con, mode="strict")
        series, source_id = wb.ingest_worldbank_variable(_spec(), "https://api.worldbank.org/v2",
                                                         tmp_path, con, run_id)
        files = con.execute("SELECT path FROM raw_files WHERE ingestion_run_id=?", (run_id,)).fetchall()
    finally:
        con.close()

    assert series["2009-12"] == 95.0
    assert "2008-12" in series.index
    assert source_id > 0
    assert len(files) == 1
    assert (tmp_path / "worldbank" / f"WLD_NE.IMP.GNFS.KD_run{run_id}.csv").exists()
