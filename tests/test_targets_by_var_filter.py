"""Per-band variable filtering via `targets_by_var` in `_analyse_and_render`.

When the manifest pre-registers each variable's `cycle_targets`, the runner
restricts the band composite to columns that target the band — feeding the
Kondratieff composite with Q_HPI (a strict Kuznets variable in the
manifest) would z-score Q_HPI's near-zero K-band content to unit variance
and dilute the K-wave SNR of the genuine K-targeting columns.

These tests pin: (1) when ``targets_by_var`` is supplied the band-specific
composite uses only the subset that targets the band, (2) when it is
``None`` the full panel is used (legacy path), (3) when a band has no
targeting columns the runner falls back to the full panel.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from ecowave.cycles import runner as runner_module
from ecowave.cycles.runner import _analyse_and_render


def _settings(tmp_path):
    s = SimpleNamespace(
        db_path=tmp_path / "ecowave.db",
        figures_dir=tmp_path / "figures",
        reports_dir=tmp_path / "reports",
        data_raw_dir=tmp_path / "data_raw",
    )
    s.figures_dir.mkdir(parents=True, exist_ok=True)
    s.reports_dir.mkdir(parents=True, exist_ok=True)
    return s


def _panel(samples_per_year: int = 4) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    n = 200
    idx = pd.period_range(start="1970Q1", periods=n, freq="Q")
    return pd.DataFrame({
        "VAR_KITCHIN": np.sin(2 * np.pi * np.arange(n) / 12) +
                        rng.normal(scale=0.3, size=n),
        "VAR_KONDRATIEFF": np.sin(2 * np.pi * np.arange(n) / 200) +
                            rng.normal(scale=0.3, size=n),
        "VAR_BOTH": (np.sin(2 * np.pi * np.arange(n) / 12) +
                      np.sin(2 * np.pi * np.arange(n) / 200) +
                      rng.normal(scale=0.3, size=n)),
    }, index=idx)


def _stub_persistence(monkeypatch):
    for name in ("replace_cycle_positions", "replace_cycle_consensus",
                 "replace_cycle_universality", "finish_ingestion_run"):
        monkeypatch.setattr(runner_module, name, lambda *a, **kw: None)
    monkeypatch.setattr(runner_module, "_run_gate1",
                        lambda *a, **kw: SimpleNamespace(reject_cycle=False,
                                                          p_value=0.01))


def test_targets_by_var_restricts_composite_panel_columns(monkeypatch, tmp_path):
    """Capture the per-band composite call to verify column filtering."""
    panel = _panel()
    composite = panel.mean(axis=1)
    seen_columns: list[list[str]] = []
    real_cp = runner_module._composite_panel

    def spy(p, *, band=None, samples_per_year=1.0, differencing=False):
        seen_columns.append(list(p.columns))
        return real_cp(p, band=band, samples_per_year=samples_per_year,
                        differencing=differencing)

    monkeypatch.setattr(runner_module, "_composite_panel", spy)
    _stub_persistence(monkeypatch)

    targets = {
        "VAR_KITCHIN":     ("kitchin",),
        "VAR_KONDRATIEFF": ("kondratieff",),
        "VAR_BOTH":        ("kitchin", "kondratieff"),
    }
    con = sqlite3.connect(":memory:")
    _analyse_and_render(
        settings=_settings(tmp_path), as_of="2026-05",
        con=con, run_id=0, mode="exploratory",
        groups=["USA"], composite_by_group={"USA": composite},
        panels_by_group={"USA": panel},
        n_surrogates=10, seed=0, null="ar1",
        horizon_label="test", wavelet_group="USA",
        samples_per_year=4.0, report_suffix="test",
        targets_by_var=targets,
    )
    # The first call per band has band=(lo, hi); we collect only those.
    band_calls = [c for c in seen_columns if c]  # all non-empty
    # Kitchin: VAR_KITCHIN + VAR_BOTH
    assert {"VAR_KITCHIN", "VAR_BOTH"} <= set(band_calls[0])
    assert "VAR_KONDRATIEFF" not in band_calls[0]
    # Kondratieff: VAR_KONDRATIEFF + VAR_BOTH (last band in iteration order)
    assert {"VAR_KONDRATIEFF", "VAR_BOTH"} <= set(band_calls[-1])
    assert "VAR_KITCHIN" not in band_calls[-1]


def test_targets_by_var_none_uses_full_panel(monkeypatch, tmp_path):
    """Backwards-compat: when targets_by_var is omitted the full panel
    feeds every band composite."""
    panel = _panel()
    composite = panel.mean(axis=1)
    seen_columns: list[list[str]] = []
    real_cp = runner_module._composite_panel

    def spy(p, *, band=None, samples_per_year=1.0, differencing=False):
        seen_columns.append(list(p.columns))
        return real_cp(p, band=band, samples_per_year=samples_per_year,
                        differencing=differencing)

    monkeypatch.setattr(runner_module, "_composite_panel", spy)
    _stub_persistence(monkeypatch)

    con = sqlite3.connect(":memory:")
    _analyse_and_render(
        settings=_settings(tmp_path), as_of="2026-05",
        con=con, run_id=0, mode="exploratory",
        groups=["USA"], composite_by_group={"USA": composite},
        panels_by_group={"USA": panel},
        n_surrogates=10, seed=0, null="ar1",
        horizon_label="test", wavelet_group="USA",
        samples_per_year=4.0, report_suffix="test",
        # targets_by_var omitted
    )
    # Every band call should receive the full 3-column panel.
    for cols in seen_columns:
        assert cols == ["VAR_KITCHIN", "VAR_KONDRATIEFF", "VAR_BOTH"]


def test_targets_by_var_falls_back_when_no_matching_columns(monkeypatch, tmp_path):
    """If no manifest variable targets a band, the runner falls back to
    the full panel rather than producing an empty composite."""
    panel = _panel()
    composite = panel.mean(axis=1)
    seen_columns: list[list[str]] = []
    real_cp = runner_module._composite_panel

    def spy(p, *, band=None, samples_per_year=1.0, differencing=False):
        seen_columns.append(list(p.columns))
        return real_cp(p, band=band, samples_per_year=samples_per_year,
                        differencing=differencing)

    monkeypatch.setattr(runner_module, "_composite_panel", spy)
    _stub_persistence(monkeypatch)

    # No variable targets juglar — the juglar band must fall back.
    targets = {
        "VAR_KITCHIN":     ("kitchin",),
        "VAR_KONDRATIEFF": ("kondratieff",),
        "VAR_BOTH":        ("kitchin", "kondratieff"),
    }
    con = sqlite3.connect(":memory:")
    _analyse_and_render(
        settings=_settings(tmp_path), as_of="2026-05",
        con=con, run_id=0, mode="exploratory",
        groups=["USA"], composite_by_group={"USA": composite},
        panels_by_group={"USA": panel},
        n_surrogates=10, seed=0, null="ar1",
        horizon_label="test", wavelet_group="USA",
        samples_per_year=4.0, report_suffix="test",
        targets_by_var=targets,
    )
    # The juglar call (no targeting var) should see the full panel.
    juglar_calls = [c for c in seen_columns
                    if set(c) == {"VAR_KITCHIN", "VAR_KONDRATIEFF", "VAR_BOTH"}]
    assert juglar_calls, "Juglar should fall back to the full panel"
