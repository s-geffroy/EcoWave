from __future__ import annotations

import pandas as pd

from ecowave.waves.model_d_regime import fit_model_d

MONTHS = [f"{y}-{m:02d}" for y in (2007, 2008, 2009) for m in range(1, 13)]
MID = MONTHS[len(MONTHS) // 2]


def _regime_shift_panel() -> pd.DataFrame:
    """Calm first half, high-stress second half — one obvious change point."""
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


def test_detects_regime_change():
    model = fit_model_d(_regime_shift_panel())
    phases = model["candidate_phases"]
    assert len(phases) >= 2  # at least one break detected
    # Phases are (label, start, end) and cover the whole window in order.
    assert phases[0][1] == MONTHS[0]
    assert phases[-1][2] == MONTHS[-1]
    for _, start, end in phases:
        assert start <= end


def test_empty_panel_single_phase():
    months = MONTHS
    rows = [{
        "month": m, "variable_code": "E1", "raw_value": None,
        "z_precrisis": None, "stress_precrisis": None,
        "z_structural": None, "stress_structural": None,
        "status": "missing", "source": None, "confidence": None, "notes": "",
    } for m in months]
    model = fit_model_d(pd.DataFrame(rows))
    assert len(model["candidate_phases"]) == 1
