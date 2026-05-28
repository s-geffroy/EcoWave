from __future__ import annotations

import pandas as pd

from ecowave.scoring.model_scores import (
    _verdict_for,
    compute_model_scores,
    db_insertable_rows,
    model_verdicts,
)

MONTHS = [f"{y}-{m:02d}" for y in range(2007, 2013) for m in range(1, 13)]

# Two-phase test model aligned with a clean regime shift at 2010-01.
TEST_MODEL = {
    "candidate_phases": [
        ("calm", MONTHS[0], "2009-12"),
        ("crisis", "2010-01", MONTHS[-1]),
    ],
}
MODELS = {"D": TEST_MODEL}


def _regime_panel() -> pd.DataFrame:
    """Calm (low stress) 2007-2009, crisis (high stress) 2010-2012."""
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


def test_c1_confirms_structured_curves():
    scores = compute_model_scores(_regime_panel(), models=MODELS, n_draws=150)
    c1 = scores[(scores["model_code"] == "D") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["status"] == "computed"
    assert c1["raw_score"] >= 2


def test_db_rows_only_c1_c3():
    scores = compute_model_scores(_regime_panel(), models=MODELS, n_draws=150)
    rows = db_insertable_rows(scores)
    assert all(r["criterion_code"] in {"C1", "C3"} for r in rows)
    assert all(isinstance(r["raw_score"], int) for r in rows)


def test_verdict_complete_with_only_c1_c3():
    """CPV verdicts close when C1 + C3 are scored — no analyst layer required."""
    scores = compute_model_scores(_regime_panel(), models=MODELS, n_draws=150)
    verdicts = model_verdicts(scores)
    assert bool(verdicts["complete"].all())
    assert (verdicts["verdict"] != "blocked").all()


def test_c1_zero_when_no_data():
    empty = pd.DataFrame([
        {"month": "2008-09", "variable_code": "E1", "raw_value": None,
         "z_precrisis": None, "stress_precrisis": None, "z_structural": None,
         "stress_structural": None, "status": "missing", "source": None,
         "confidence": None, "notes": ""}
    ])
    scores = compute_model_scores(empty, models=MODELS, n_draws=50)
    c1 = scores[(scores["model_code"] == "D") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["raw_score"] == 0


def _crit(c1, c3):
    return {"C1": c1, "C3": c3}


def test_verdict_thresholds():
    # Solid evidence: C1≥2 and C3≥2 → strong (total = 2.5).
    assert _verdict_for(_crit(3, 2))[1] == "strong"
    # Weak C3 → falls to rejected.
    assert _verdict_for(_crit(2, 0))[1] == "rejected"
    # Mid total without strong C1/C3 minima → usable.
    assert _verdict_for(_crit(2, 2))[1] == "usable"
    # C1 ≤ 1 → rejected.
    assert _verdict_for(_crit(1, 3))[1] == "rejected"


def test_uniform_crisis_does_not_confirm():
    """A uniformly high-stress window has no phase structure → C1 must be low."""
    rows = []
    for code in ["E1", "E2", "D1", "L1"]:
        for month in MONTHS:
            rows.append({
                "month": month, "variable_code": code, "raw_value": 1.0,
                "z_precrisis": 3.0, "stress_precrisis": 95.0,
                "z_structural": 3.0, "stress_structural": 95.0,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    scores = compute_model_scores(pd.DataFrame(rows), models=MODELS, n_draws=100)
    c1 = scores[(scores["model_code"] == "D") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["raw_score"] <= 1
