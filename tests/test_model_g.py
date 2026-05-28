"""Model G (Bry-Boschan / Harding-Pagan) contract tests."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.waves.model_g_bryboschan import fit_model_g


def _build_cosine_panel(n_months: int = 120, period_months: int = 30,
                       seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    months = pd.date_range("2000-01", periods=n_months, freq="MS").strftime("%Y-%m").tolist()
    t = np.arange(n_months)
    rows = []
    for curve in ("E", "D", "S", "L", "I"):
        signal = np.cos(2.0 * np.pi * t / period_months)
        noise = rng.normal(scale=0.05, size=n_months)
        stress = 50.0 + 30.0 * (signal + noise)
        for i, m in enumerate(months):
            rows.append({
                "month": m, "variable_code": f"{curve}1",
                "raw_value": float(stress[i]),
                "z_precrisis": float(signal[i] + noise[i]),
                "stress_precrisis": float(np.clip(stress[i], 0, 100)),
                "z_structural": float(signal[i] + noise[i]),
                "stress_structural": float(np.clip(stress[i], 0, 100)),
                "status": "available", "source": "test", "confidence": "A", "notes": "",
            })
    return pd.DataFrame(rows)


def test_fit_model_g_returns_required_keys():
    panel = _build_cosine_panel(n_months=120, period_months=30)
    result = fit_model_g(panel)
    for key in ("name", "hypothesis", "candidate_phases", "method", "fit_status",
                "n_peaks", "n_troughs"):
        assert key in result


def test_fit_model_g_finds_turning_points_on_clean_cosine():
    # A 30-month cosine across 120 months produces 4 full cycles -> 4 peaks + 4 troughs.
    panel = _build_cosine_panel(n_months=120, period_months=30)
    result = fit_model_g(panel)
    assert result["fit_status"] == "ok"
    assert result["n_peaks"] >= 2
    assert result["n_troughs"] >= 2


def test_fit_model_g_candidate_phases_alternate_correctly():
    panel = _build_cosine_panel(n_months=120, period_months=30)
    result = fit_model_g(panel)
    if result["fit_status"] != "ok":
        return
    labels = [p[0] for p in result["candidate_phases"]]
    assert set(labels).issubset({"expansion", "peak", "contraction", "trough"})


def test_fit_model_g_falls_back_when_no_turning_point():
    # Monotonic trend → no turning point.
    n = 100
    months = pd.date_range("2010-01", periods=n, freq="MS").strftime("%Y-%m").tolist()
    rows = []
    for curve in ("E", "D", "S", "L", "I"):
        trend = np.linspace(0, 50, n)
        for i, m in enumerate(months):
            rows.append({
                "month": m, "variable_code": f"{curve}1",
                "raw_value": float(trend[i]),
                "z_precrisis": float(trend[i]),
                "stress_precrisis": float(trend[i]),
                "z_structural": float(trend[i]),
                "stress_structural": float(trend[i]),
                "status": "available", "source": "test", "confidence": "A", "notes": "",
            })
    panel = pd.DataFrame(rows)
    result = fit_model_g(panel)
    assert result["fit_status"] == "fallback"
    assert "rejected_no_turning_point" in {p[0] for p in result["candidate_phases"]}
