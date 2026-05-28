"""The Kitchin gate widens on the quarterly horizon (Roadmap #9).

On annual data (``samples_per_year <= 1``) the runner narrows Kitchin to its
upper edge (4-5 y). On the quarterly horizon (``samples_per_year=4``) the
full pre-registered 3-5 y band is used.

``cf_bandpass`` records its (lo, hi) in the output Series name as
``cf_{lo}_{hi}``. We read that back from ``cycles_by_group[group]["kitchin"]``
through a tiny harness against ``_analyse_and_render``.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from ecowave.cycles import runner as runner_module
from ecowave.cycles.runner import _analyse_and_render


def _settings(tmp_path):
    """Minimal Settings-like stand-in for the tests."""
    s = SimpleNamespace(
        db_path=tmp_path / "ecowave.db",
        figures_dir=tmp_path / "figures",
        reports_dir=tmp_path / "reports",
        data_raw_dir=tmp_path / "data_raw",
    )
    s.figures_dir.mkdir(parents=True, exist_ok=True)
    s.reports_dir.mkdir(parents=True, exist_ok=True)
    return s


def _make_panel(n: int, samples_per_year: int) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    if samples_per_year == 1:
        idx = pd.RangeIndex(start=1960, stop=1960 + n)
    else:
        idx = pd.period_range(start="1960Q1", periods=n, freq="Q")
    return pd.DataFrame({
        "X": np.sin(2.0 * np.pi * np.arange(n) / (4 * samples_per_year)) +
              rng.normal(scale=0.3, size=n),
        "Y": np.sin(2.0 * np.pi * np.arange(n) / (4 * samples_per_year)) +
              rng.normal(scale=0.3, size=n),
    }, index=idx)


def _spy_cf_lo_hi(monkeypatch):
    """Patch cf_bandpass everywhere it's called from runner.py to capture
    (lo, hi) per cycle. Returns a list of (lo, hi) tuples in call order."""
    seen: list[tuple[int, int]] = []
    real_cf = runner_module.cf_bandpass

    def spy(series, lo_years, hi_years, samples_per_year=1.0):
        seen.append((int(lo_years), int(hi_years)))
        return real_cf(series, lo_years=lo_years, hi_years=hi_years,
                       samples_per_year=samples_per_year)

    monkeypatch.setattr(runner_module, "cf_bandpass", spy)
    # Also short-circuit the surrogates and the per-method classifiers so the
    # test runs fast and deterministically.
    monkeypatch.setattr(runner_module, "_run_gate1",
                        lambda *a, **kw: SimpleNamespace(reject_cycle=True,
                                                          p_value=0.99))
    return seen


def _stub_persistence(monkeypatch):
    """Suppress the DB writes — we only care about the in-memory call trace."""
    for name in ("replace_cycle_positions", "replace_cycle_consensus",
                 "replace_cycle_universality", "finish_ingestion_run"):
        monkeypatch.setattr(runner_module, name, lambda *a, **kw: None)


def test_kitchin_narrows_to_4_5_when_annual(monkeypatch, tmp_path):
    seen = _spy_cf_lo_hi(monkeypatch)
    _stub_persistence(monkeypatch)
    panel = _make_panel(n=80, samples_per_year=1)
    composite = panel.mean(axis=1)
    con = sqlite3.connect(":memory:")
    _analyse_and_render(
        settings=_settings(tmp_path), as_of="2026-05",
        con=con, run_id=0, mode="exploratory",
        groups=["WLD"], composite_by_group={"WLD": composite},
        panels_by_group={"WLD": panel},
        n_surrogates=10, seed=0, null="ar1",
        horizon_label="test-annual", wavelet_group="WLD",
        samples_per_year=1.0, report_suffix="test",
    )
    # The Kitchin entry should be the 4-5 band on the annual horizon.
    assert (4, 5) in seen, f"Annual Kitchin should narrow to (4,5); saw {seen}"
    # And the full 3-5 should NOT have been attempted.
    assert (3, 5) not in seen, (
        f"Annual horizon must not run the full 3-5 Kitchin band; saw {seen}"
    )


def test_kitchin_uses_full_3_5_when_quarterly(monkeypatch, tmp_path):
    seen = _spy_cf_lo_hi(monkeypatch)
    _stub_persistence(monkeypatch)
    panel = _make_panel(n=200, samples_per_year=4)
    composite = panel.mean(axis=1)
    con = sqlite3.connect(":memory:")
    _analyse_and_render(
        settings=_settings(tmp_path), as_of="2026-05",
        con=con, run_id=0, mode="exploratory",
        groups=["USA"], composite_by_group={"USA": composite},
        panels_by_group={"USA": panel},
        n_surrogates=10, seed=0, null="ar1",
        horizon_label="test-quarterly", wavelet_group="USA",
        samples_per_year=4.0, report_suffix="test",
    )
    # The Kitchin entry should be the full 3-5 band on the quarterly horizon.
    assert (3, 5) in seen, f"Quarterly Kitchin should run (3,5); saw {seen}"
    # The narrow 4-5 attempt should NOT happen at the quarterly horizon.
    assert (4, 5) not in seen, (
        f"Quarterly horizon should not run the narrow 4-5 Kitchin; saw {seen}"
    )
