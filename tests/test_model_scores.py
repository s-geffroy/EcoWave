from __future__ import annotations

import pandas as pd

from ecowave.scoring.model_scores import (
    QUALITATIVE,
    _verdict_for,
    compute_model_scores,
    db_insertable_rows,
    model_verdicts,
)

MONTHS = [f"{y}-{m:02d}" for y in range(2007, 2013) for m in range(1, 13)]


def _regime_panel() -> pd.DataFrame:
    """Clean two-regime shift at 2010-01 — aligned with Model B's cycle boundary.

    Calm (low stress) 2007-2009, crisis (high stress) 2010-2012, across four
    curves. Model B's boundary captures this; a random segmentation does not.
    """
    rows = []
    for code in ["E1", "E2", "D1", "L1", "S1"]:
        for month in MONTHS:
            stress = 90.0 if month >= "2010-01" else 10.0
            rows.append({
                "month": month, "variable_code": code, "raw_value": 1.0,
                "z_precrisis": 0.0, "stress_precrisis": stress,
                "z_structural": 0.0, "stress_structural": stress,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    return pd.DataFrame(rows)


def test_qualitative_criteria_blocked():
    scores = compute_model_scores(_regime_panel(), n_draws=150)
    blocked = scores[scores["criterion_code"].isin(QUALITATIVE)]
    assert (blocked["status"] == "blocked").all()
    assert blocked["raw_score"].isna().all()


def test_c1_confirms_structured_curves():
    scores = compute_model_scores(_regime_panel(), n_draws=150)
    c1 = scores[(scores["model_code"] == "B") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["status"] == "computed"
    # B's boundary aligns with the regime change -> several curves beat the null.
    assert c1["raw_score"] >= 2


def test_db_rows_only_computed():
    scores = compute_model_scores(_regime_panel(), n_draws=150)
    rows = db_insertable_rows(scores)
    assert all(r["criterion_code"] in {"C1", "C3"} for r in rows)
    assert all(isinstance(r["raw_score"], int) for r in rows)


def test_all_models_blocked_verdict_without_annotations():
    scores = compute_model_scores(_regime_panel(), n_draws=150)
    verdicts = model_verdicts(scores)
    assert (verdicts["verdict"] == "blocked").all()


def test_c1_zero_when_no_data():
    empty = pd.DataFrame([
        {"month": "2008-09", "variable_code": "E1", "raw_value": None,
         "z_precrisis": None, "stress_precrisis": None, "z_structural": None,
         "stress_structural": None, "status": "missing", "source": None,
         "confidence": None, "notes": ""}
    ])
    scores = compute_model_scores(empty, n_draws=50)
    c1 = scores[(scores["model_code"] == "B") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["raw_score"] == 0


def _crit(c1, c2, c3, c4, c5, c6):
    return {"C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5, "C6": c6}


def test_verdict_thresholds_recalibrated():
    # Solid computed evidence + strong narrative -> strong.
    assert _verdict_for(_crit(3, 3, 2, 3, 3, 3))[1] == "strong"
    # Strong narrative but weak falsifiable evidence (C3=1) cannot be strong.
    assert _verdict_for(_crit(2, 3, 1, 3, 3, 3))[1] == "usable"
    # Mid-range -> usable.
    assert _verdict_for(_crit(2, 2, 2, 2, 2, 2))[1] == "usable"
    # Low total -> fragile.
    assert _verdict_for(_crit(2, 1, 1, 1, 1, 1))[1] == "fragile"
    # Falsifiable evidence in one curve -> rejected.
    assert _verdict_for(_crit(1, 3, 3, 3, 3, 3))[1] == "rejected"


def test_uniform_crisis_does_not_confirm():
    """A uniformly high-stress window has no phase structure -> C1 must be low."""
    rows = []
    for code in ["E1", "E2", "D1", "L1"]:
        for month in MONTHS:
            rows.append({
                "month": month, "variable_code": code, "raw_value": 1.0,
                "z_precrisis": 3.0, "stress_precrisis": 95.0,
                "z_structural": 3.0, "stress_structural": 95.0,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    scores = compute_model_scores(pd.DataFrame(rows), n_draws=100)
    c1 = scores[(scores["model_code"] == "B") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["raw_score"] <= 1  # not distinguishable from chance
