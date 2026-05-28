from __future__ import annotations

from ecowave.db import (
    connect,
    finish_ingestion_run,
    get_schema_version,
    register_raw_file,
    start_ingestion_run,
)


def test_schema_initialized(initialized_db):
    assert get_schema_version(initialized_db) == "0.2.0"


def test_variables_seeded(initialized_db):
    con = connect(initialized_db)
    try:
        count = con.execute("SELECT COUNT(*) AS n FROM variables").fetchone()["n"]
    finally:
        con.close()
    assert count == 15


def test_ingestion_run_lifecycle(initialized_db, tmp_path):
    con = connect(initialized_db)
    try:
        run_id = start_ingestion_run(con, mode="exploratory", notes="test")
        raw = tmp_path / "sample.csv"
        raw.write_text("date,value\n2008-01-01,1.0\n", encoding="utf-8")
        register_raw_file(con, run_id, "E1", raw)
        finish_ingestion_run(con, run_id, "success")

        run = con.execute("SELECT status, finished_at FROM ingestion_runs WHERE id=?", (run_id,)).fetchone()
        files = con.execute("SELECT checksum_sha256 FROM raw_files WHERE ingestion_run_id=?", (run_id,)).fetchall()
    finally:
        con.close()
    assert run["status"] == "success"
    assert run["finished_at"] is not None
    assert len(files) == 1 and len(files[0]["checksum_sha256"]) == 64
