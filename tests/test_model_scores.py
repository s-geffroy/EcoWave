from __future__ import annotations

import pandas as pd

from ecowave.scoring.model_scores import (
    QUALITATIVE,
    compute_model_scores,
    db_insertable_rows,
    model_verdicts,
)


def _panel_with_two_curves_high_stress() -> pd.DataFrame:
    rows = []
    months = ["2008-08", "2008-09", "2008-10", "2008-11"]
    for code in ["E1", "E2", "D1", "D2"]:  # E and D curves
        for m in months:
            rows.append({
                "month": m, "variable_code": code, "raw_value": 50.0,
                "z_precrisis": 3.0, "stress_precrisis": 95.0,
                "z_structural": 3.0, "stress_structural": 90.0,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    return pd.DataFrame(rows)


def test_qualitative_criteria_blocked():
    scores = compute_model_scores(_panel_with_two_curves_high_stress())
    blocked = scores[scores["criterion_code"].isin(QUALITATIVE)]
    assert (blocked["status"] == "blocked").all()
    assert blocked["raw_score"].isna().all()


def test_c1_counts_confirming_curves():
    scores = compute_model_scores(_panel_with_two_curves_high_stress())
    c1 = scores[(scores["model_code"] == "A") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["status"] == "computed"
    assert c1["raw_score"] == 2  # E and D confirm


def test_db_rows_only_computed():
    scores = compute_model_scores(_panel_with_two_curves_high_stress())
    rows = db_insertable_rows(scores)
    assert all(r["criterion_code"] in {"C1", "C3"} for r in rows)
    assert all(isinstance(r["raw_score"], int) for r in rows)


def test_all_models_blocked_verdict():
    scores = compute_model_scores(_panel_with_two_curves_high_stress())
    verdicts = model_verdicts(scores)
    assert (verdicts["verdict"] == "blocked").all()


def test_blocked_when_no_data():
    empty = pd.DataFrame([
        {"month": "2008-09", "variable_code": "E1", "raw_value": None,
         "z_precrisis": None, "stress_precrisis": None, "z_structural": None,
         "stress_structural": None, "status": "missing", "source": None,
         "confidence": None, "notes": ""}
    ])
    scores = compute_model_scores(empty)
    c1 = scores[(scores["model_code"] == "B") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["raw_score"] == 0
