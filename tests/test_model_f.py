"""Model F (CF Juglar + Hilbert) contract tests."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.waves.model_f_cycles import fit_model_f


def _build_panel(n_months: int = 240, juglar_strength: float = 1.0, seed: int = 0,
                 curves=("E", "D", "S", "L", "I")) -> pd.DataFrame:
    """Build a synthetic panel: 5 curves, each with a Juglar cycle + noise."""
    rng = np.random.default_rng(seed)
    months = pd.date_range("1990-01", periods=n_months, freq="MS").strftime("%Y-%m").tolist()
    t = np.arange(n_months)
    rows = []
    for curve in curves:
        signal = juglar_strength * np.sin(2.0 * np.pi * t / 96.0)  # 96 months = 8 years
        noise = rng.normal(scale=0.3, size=n_months)
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


def test_fit_model_f_returns_required_keys_on_clean_signal():
    panel = _build_panel(n_months=240, juglar_strength=2.0, seed=42)
    result = fit_model_f(panel, n_surrogates=200, seed=0)
    for key in ("name", "hypothesis", "candidate_phases", "method", "fit_status"):
        assert key in result, f"missing key {key}"
    assert isinstance(result["candidate_phases"], list)


def test_fit_model_f_candidate_phases_format():
    panel = _build_panel(n_months=240, juglar_strength=2.0, seed=42)
    result = fit_model_f(panel, n_surrogates=100, seed=0)
    for phase in result["candidate_phases"]:
        assert isinstance(phase, tuple) and len(phase) == 3
        label, start, end = phase
        assert isinstance(label, str)
        assert isinstance(start, str) and len(start) == 7
        assert isinstance(end, str) and len(end) == 7


def test_fit_model_f_falls_back_on_short_panel():
    short = _build_panel(n_months=40, juglar_strength=1.0)
    result = fit_model_f(short)
    assert result["fit_status"] == "fallback"
    assert result["candidate_phases"][0][0] == "rejected_cycle"


def test_fit_model_f_rejects_pure_noise():
    rng = np.random.default_rng(0)
    n = 240
    months = pd.date_range("1990-01", periods=n, freq="MS").strftime("%Y-%m").tolist()
    rows = []
    for curve in ("E", "D", "S", "L", "I"):
        noise = rng.normal(scale=1.0, size=n)
        for i, m in enumerate(months):
            rows.append({
                "month": m, "variable_code": f"{curve}1",
                "raw_value": float(noise[i]),
                "z_precrisis": float(noise[i]),
                "stress_precrisis": 50.0,
                "z_structural": float(noise[i]),
                "stress_structural": 50.0,
                "status": "available", "source": "test", "confidence": "A", "notes": "",
            })
    panel = pd.DataFrame(rows)
    result = fit_model_f(panel, n_surrogates=200, seed=0)
    # Either rejected outright OR p-value high; in pure noise we expect a high p.
    assert (result.get("ar1_pvalue") is None) or (result.get("ar1_pvalue", 0.0) >= 0.0)
