"""Smoke test for the full quarterly pipeline end-to-end.

Mocks ``build_quarterly_panel`` (so no network is hit) and runs
``run_position_cycles(..., horizon='quarterly', ...)`` from a clean DB.

Acceptance signals:
- A report `cycle_position_<as_of>_q.md` lands in `settings.reports_dir`.
- The new ``cycle_observations_quarterly`` table exists (schema 0.5.1).
- At least one cycle row is persisted in ``cycle_positions`` for the run.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from ecowave.cycles import runner as runner_module
from ecowave.cycles.runner import run_position_cycles


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "db" / "schema.sql"
SEED_PATH = REPO_ROOT / "db" / "seed_variables.sql"


def _settings_with_dirs(tmp_path) -> SimpleNamespace:
    s = SimpleNamespace(
        mode="exploratory",
        fred_api_key="dummy",
        db_path=tmp_path / "ecowave.db",
        figures_dir=tmp_path / "figures",
        reports_dir=tmp_path / "reports",
        data_raw_dir=tmp_path / "data_raw",
    )
    s.figures_dir.mkdir(parents=True, exist_ok=True)
    s.reports_dir.mkdir(parents=True, exist_ok=True)
    s.data_raw_dir.mkdir(parents=True, exist_ok=True)
    return s


def _synthetic_q_panel(years: int = 80, seed: int = 0) -> pd.DataFrame:
    """Composite panel with a clean 3-year Kitchin signal at quarterly grid."""
    n = years * 4
    idx = pd.period_range(start=f"{2026-years}Q1", periods=n, freq="Q")
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    cycle3 = np.sin(2.0 * np.pi * t / 12.0)
    juglar = 0.5 * np.sin(2.0 * np.pi * t / 32.0)  # 8-year
    noise = lambda: rng.normal(scale=0.15, size=n)
    return pd.DataFrame({
        "Q_GDP":    cycle3 + juglar + noise(),
        "Q_CPI":    cycle3 + noise(),
        "Q_UNRATE": -cycle3 + noise(),
    }, index=idx)


def test_quarterly_runner_writes_q_report(monkeypatch, tmp_path):
    settings = _settings_with_dirs(tmp_path)

    # Stub the quarterly ingestion to inject our synthetic panel for USA.
    def fake_build(group_code, *_args, **_kwargs):
        if group_code == "USA":
            return _synthetic_q_panel(years=80)
        return pd.DataFrame()

    monkeypatch.setattr(runner_module, "build_quarterly_panel", fake_build)

    manifest_path = REPO_ROOT / "quarterly_manifest.json"
    out_path = run_position_cycles(
        settings=settings, as_of="2026-05",
        manifest_path=manifest_path,
        groups=["USA"], mode="exploratory",
        n_surrogates=50, seed=0,
        horizon="quarterly", null="ar1",
    )
    assert out_path.exists(), f"quarterly report not written at {out_path}"
    assert out_path.name.endswith("_q.md"), (
        f"quarterly report should use the _q suffix; got {out_path.name}"
    )

    # The new quarterly table exists in the freshly initialised DB.
    con = sqlite3.connect(settings.db_path)
    try:
        tables = {r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()}
        assert "cycle_observations_quarterly" in tables
        row = con.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()
        assert row[0] == "0.5.1"
        pos_rows = con.execute(
            "SELECT cycle, phase FROM cycle_positions WHERE as_of_month='2026-05'"
        ).fetchall()
    finally:
        con.close()

    # At least one Kitchin row was published (with whatever phase).
    cycles = {r[0] for r in pos_rows}
    assert "kitchin" in cycles


def test_db_migration_from_0_5_0_to_0_5_1(tmp_path):
    """Round-trip: an existing 0.5.0 DB is migrated in place to 0.5.1, the
    new quarterly table is created, and schema_meta reflects the bump."""
    db_path = tmp_path / "old.db"

    # Build the schema text and rewind the version back to 0.5.0 to mimic an
    # existing DB. We splice it manually since SQLite needs schema_meta seeded
    # at the right value before migrate_db runs.
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    schema_sql_old = schema_sql.replace(
        "('schema_version', '0.5.1')", "('schema_version', '0.5.0')"
    )
    # Strip the new quarterly table so the migration genuinely creates it.
    marker = "CREATE TABLE IF NOT EXISTS cycle_observations_quarterly"
    if marker in schema_sql_old:
        schema_sql_old = schema_sql_old.split(marker, 1)[0]

    con = sqlite3.connect(db_path)
    try:
        con.executescript(schema_sql_old)
        con.commit()
        tables_before = {r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()}
        assert "cycle_observations_quarterly" not in tables_before
    finally:
        con.close()

    from ecowave.db import migrate_db
    migrate_db(db_path)

    con = sqlite3.connect(db_path)
    try:
        tables_after = {r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()}
        version = con.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0]
    finally:
        con.close()
    assert "cycle_observations_quarterly" in tables_after
    assert version == "0.5.1"
