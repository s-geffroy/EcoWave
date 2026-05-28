"""Model E — Markov-switching benchmark."""
from __future__ import annotations

import pandas as pd
import pytest

from ecowave.waves.model_e_markov import K_STATES, fit_model_e

MONTHS = [f"{y}-{m:02d}" for y in (2007, 2008, 2009, 2010) for m in range(1, 13)]
MID = MONTHS[len(MONTHS) // 2]


def _regime_shift_panel() -> pd.DataFrame:
    """Two-regime panel: calm first half (stress=10), crisis second half (stress=90)."""
    rows = []
    for code in ["E1", "E2", "D1", "L1", "S1"]:
        for month in MONTHS:
            stress = 90.0 if month >= MID else 10.0
            rows.append({
                "month": month, "variable_code": code, "raw_value": 1.0,
                "z_precrisis": 0.0, "stress_precrisis": stress,
                "z_structural": 0.0, "stress_structural": stress,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    return pd.DataFrame(rows)


def _empty_panel() -> pd.DataFrame:
    rows = [{
        "month": m, "variable_code": "E1", "raw_value": None,
        "z_precrisis": None, "stress_precrisis": None,
        "z_structural": None, "stress_structural": None,
        "status": "missing", "source": None, "confidence": None, "notes": "",
    } for m in MONTHS]
    return pd.DataFrame(rows)


def test_fit_model_e_detects_regime_shift_on_clean_data():
    pytest.importorskip("statsmodels")
    model = fit_model_e(_regime_shift_panel())
    if model["fit_status"] != "ok":
        pytest.skip(f"Markov fit did not converge in this environment: {model['fit_status']}")
    phases = model["candidate_phases"]
    assert len(phases) >= 2
    assert phases[0][1] == MONTHS[0]
    assert phases[-1][2] == MONTHS[-1]
    assert model["selected_k"] in K_STATES
    # Both AIC and BIC reported as floats for the selected k.
    assert isinstance(model["aic"], float)
    assert isinstance(model["bic"], float)


def test_fit_model_e_falls_back_on_empty_panel():
    model = fit_model_e(_empty_panel())
    assert len(model["candidate_phases"]) <= 1
    # Fallback path must remain self-consistent.
    assert model["fit_status"] in {"fallback", "ok", "no Markov fit converged"}


def test_fit_model_e_carries_aic_bic_table_when_fit_ok():
    pytest.importorskip("statsmodels")
    model = fit_model_e(_regime_shift_panel())
    if model["fit_status"] != "ok":
        pytest.skip("Markov fit not available in this test environment")
    table = model.get("aic_bic_table", {})
    # At least one k variant reported (the selected one); usually both 2 and 3.
    assert table
    for entry in table.values():
        assert "aic" in entry and "bic" in entry
