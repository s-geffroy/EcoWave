"""Smoke tests for the per-variable Gate-1 evidence module.

End-to-end run is too expensive (~30 min total CPU); these tests cover the
SQL panel reconstruction, sidecar I/O and the rendered-page structure
using synthetic fixtures.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from ecowave.cycles.evidence import (
    _load_annual_panel,
    _load_quarterly_panel,
    _survival_count_by_variable,
    compute_per_variable_evidence,
    read_evidence_sidecar,
    render_evidence_per_variable_md,
    write_evidence_sidecar,
)


def _bootstrap_obs_tables(con: sqlite3.Connection) -> None:
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS cycle_observations (
          id INTEGER PRIMARY KEY,
          group_code TEXT NOT NULL,
          variable_code TEXT NOT NULL,
          year INTEGER NOT NULL,
          value REAL,
          source_id INTEGER,
          UNIQUE(group_code, variable_code, year)
        );
        CREATE TABLE IF NOT EXISTS cycle_observations_quarterly (
          id INTEGER PRIMARY KEY,
          group_code TEXT NOT NULL,
          variable_code TEXT NOT NULL,
          year INTEGER NOT NULL,
          quarter INTEGER NOT NULL CHECK(quarter BETWEEN 1 AND 4),
          value REAL,
          source_id INTEGER,
          UNIQUE(group_code, variable_code, year, quarter)
        );
        """
    )


def test_load_annual_panel_rebuilds_year_x_variable_grid(tmp_path):
    con = sqlite3.connect(":memory:")
    _bootstrap_obs_tables(con)
    rng = np.random.default_rng(0)
    for year in range(1960, 1980):
        for var in ("NY_GDP", "NE_INV"):
            con.execute(
                "INSERT INTO cycle_observations(group_code, variable_code, "
                "year, value) VALUES (?, ?, ?, ?)",
                ("WLD", var, year, float(rng.normal()))
            )
    con.commit()
    panel = _load_annual_panel(con, "WLD", ["NY_GDP", "NE_INV"])
    assert panel.shape == (20, 2)
    assert set(panel.columns) == {"NY_GDP", "NE_INV"}
    assert panel.index.min() == 1960 and panel.index.max() == 1979


def test_load_quarterly_panel_uses_periodindex(tmp_path):
    con = sqlite3.connect(":memory:")
    _bootstrap_obs_tables(con)
    rng = np.random.default_rng(1)
    for year in range(2000, 2010):
        for q in range(1, 5):
            con.execute(
                "INSERT INTO cycle_observations_quarterly("
                "group_code, variable_code, year, quarter, value) "
                "VALUES (?, ?, ?, ?, ?)",
                ("USA", "GDP_Q", year, q, float(rng.normal()))
            )
    con.commit()
    panel = _load_quarterly_panel(con, "USA", ["GDP_Q"])
    assert isinstance(panel.index, pd.PeriodIndex)
    assert panel.index.freq == "Q-DEC"
    assert panel.shape == (40, 1)


def test_evidence_sidecar_roundtrip_handles_nans(tmp_path):
    records = [
        {"group_code": "WLD", "variable_code": "NY_GDP", "cycle": "kitchin",
         "ar1_p_value": 0.003, "separable": 1, "n_observations": 65},
        {"group_code": "WLD", "variable_code": "NY_GDP", "cycle": "kondratieff",
         "ar1_p_value": float("nan"), "separable": 0, "n_observations": 65},
    ]
    path = tmp_path / "sidecar.json"
    write_evidence_sidecar(records, path)
    # JSON must NOT contain raw NaN (strict-mode parsers reject it).
    payload = path.read_text(encoding="utf-8")
    assert "NaN" not in payload
    # Read-back returns a DataFrame with None where NaN was.
    df = read_evidence_sidecar(path)
    assert len(df) == 2
    assert pd.isna(df.iloc[1]["ar1_p_value"])


def test_survival_count_by_variable_sorts_strongest_first():
    df = pd.DataFrame([
        # NE_INV: 3 survive of 4 — should rank first.
        dict(group_code="WLD", variable_code="NE_INV", cycle="kitchin",
             ar1_p_value=0.001, separable=1, n_observations=65),
        dict(group_code="G7", variable_code="NE_INV", cycle="kitchin",
             ar1_p_value=0.030, separable=1, n_observations=65),
        dict(group_code="OECD", variable_code="NE_INV", cycle="kitchin",
             ar1_p_value=0.040, separable=1, n_observations=65),
        dict(group_code="BRICS", variable_code="NE_INV", cycle="kitchin",
             ar1_p_value=0.500, separable=0, n_observations=65),
        # NY_GDP: 1 survive of 4 — should rank second.
        dict(group_code="WLD", variable_code="NY_GDP", cycle="kitchin",
             ar1_p_value=0.040, separable=1, n_observations=65),
        dict(group_code="G7", variable_code="NY_GDP", cycle="kitchin",
             ar1_p_value=0.300, separable=0, n_observations=65),
        dict(group_code="OECD", variable_code="NY_GDP", cycle="kitchin",
             ar1_p_value=0.400, separable=0, n_observations=65),
        dict(group_code="BRICS", variable_code="NY_GDP", cycle="kitchin",
             ar1_p_value=0.500, separable=0, n_observations=65),
    ])
    counts = _survival_count_by_variable(df, "kitchin",
                                          ["WLD", "G7", "OECD", "BRICS"])
    assert list(counts["variable_code"]) == ["NE_INV", "NY_GDP"]
    assert int(counts.iloc[0]["n_survive"]) == 3
    assert int(counts.iloc[1]["n_survive"]) == 1
    assert counts.iloc[0]["rate"] == 0.75


def test_render_evidence_page_links_each_cycle_to_its_critic(tmp_path):
    # One row per (group, variable, cycle) — synthetic.
    wb_df = pd.DataFrame([
        dict(group_code="WLD", variable_code="NE_INV", cycle="kitchin",
             ar1_p_value=0.002, separable=1, n_observations=65),
        dict(group_code="G7", variable_code="NE_INV", cycle="kitchin",
             ar1_p_value=0.020, separable=1, n_observations=65),
        dict(group_code="WLD", variable_code="NY_GDP", cycle="kitchin",
             ar1_p_value=0.400, separable=0, n_observations=65),
    ])
    out = tmp_path / "evidence.md"
    render_evidence_per_variable_md(
        evidence_by_horizon={"wb": wb_df},
        groups_by_horizon={"wb": ["WLD", "G7"], "q": [], "long": []},
        as_of="2026-05", out_path=out,
    )
    text = out.read_text(encoding="utf-8")
    # The page must link each cycle to its canonical critique reference
    # (central thesis: rejections confirm the modern empirical literature).
    assert "wen-2005" in text and "Kitchin" in text
    assert "solomou-1987" in text
    assert "maddison-1991" in text
    assert "garvy-1943" in text
    # NE_INV (3 survives) is listed.
    assert "`NE_INV`" in text
