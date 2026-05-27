from __future__ import annotations

import pandas as pd
import pytest

from ecowave.scoring.annotations import load_annotations
from ecowave.scoring.model_scores import (
    WEIGHTS,
    champion_challenger,
    compute_model_scores,
    db_insertable_rows,
    model_verdicts,
)

HEADER = "model_code,criterion_code,criterion_label,raw_score,justification,analyst,date\n"


def _panel_high_stress() -> pd.DataFrame:
    rows = []
    for code in ["E1", "E2", "D1", "L1", "S1"]:
        for m in ["2008-08", "2008-09", "2008-10", "2008-11"]:
            rows.append({
                "month": m, "variable_code": code, "raw_value": 50.0,
                "z_precrisis": 3.0, "stress_precrisis": 95.0,
                "z_structural": 3.0, "stress_structural": 90.0,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    return pd.DataFrame(rows)


def _write(path, body: str):
    path.write_text(HEADER + body, encoding="utf-8")
    return path


def test_score_without_justification_is_rejected(tmp_path):
    p = _write(tmp_path / "a.csv", "A,C2,clarte,2,,me,2026-01-01\n")
    with pytest.raises(ValueError, match="without justification"):
        load_annotations(p)


def test_out_of_range_rejected(tmp_path):
    p = _write(tmp_path / "a.csv", "A,C2,clarte,5,because,me,2026-01-01\n")
    with pytest.raises(ValueError, match="out of range"):
        load_annotations(p)


def test_empty_score_stays_blocked(tmp_path):
    p = _write(tmp_path / "a.csv", "A,C2,clarte,,,,\n")
    assert load_annotations(p) == {}


def test_missing_file_returns_empty(tmp_path):
    assert load_annotations(tmp_path / "nope.csv") == {}


def test_full_annotation_unblocks_and_scores(tmp_path):
    body = "".join(
        f"{m},{c},lbl,3,justified,me,2026-01-01\n"
        for m in ["A", "B", "C"] for c in ["C2", "C4", "C5", "C6"]
    )
    ann = load_annotations(_write(tmp_path / "a.csv", body))
    scores = compute_model_scores(_panel_high_stress(), ann)
    # No blocked rows remain.
    assert (scores["status"] != "blocked").all()
    verdicts = model_verdicts(scores)
    assert verdicts["complete"].all()
    # C1=3 (4+ curves), C3 high, all qualitative=3 -> strong.
    assert (verdicts["verdict"] == "strong").all()
    # All six criteria are DB-insertable now.
    assert len(db_insertable_rows(scores)) == 18
    # All models tie at 3 on every criterion -> no challenger dethrones B.
    text = champion_challenger(scores, verdicts)
    assert "Champion provisoire: B (conservé)" in text


def test_relaxed_rule_dethrones_on_weighted_divergence():
    # C wins exactly 3/6 vs B but its weighted score diverges (+0.50) -> C dethrones B.
    raws = {
        "B": {"C1": 3, "C2": 2, "C3": 2, "C4": 2, "C5": 2, "C6": 2},
        "C": {"C1": 3, "C2": 3, "C3": 3, "C4": 3, "C5": 2, "C6": 2},
        "A": {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1},
    }
    rows = [{"model_code": m, "criterion_code": c, "raw_score": v, "status": "annotated"}
            for m, cr in raws.items() for c, v in cr.items()]
    scores = pd.DataFrame(rows)
    verdicts = pd.DataFrame([
        {"model_code": m, "weighted_score": round(sum(cr[c] * WEIGHTS[c] for c in cr), 4),
         "complete": True, "verdict": "x"}
        for m, cr in raws.items()
    ])
    text = champion_challenger(scores, verdicts, "B")
    assert "Champion provisoire: C (détrône B)" in text


def test_three_wins_without_divergence_keeps_champion():
    # C wins 3/6 (low-weight criteria) but loses C1, so the weighted margin (+0.10) < 0.30 -> B kept.
    raws = {
        "B": {"C1": 3, "C2": 2, "C3": 2, "C4": 2, "C5": 2, "C6": 2},
        "C": {"C1": 2, "C2": 2, "C3": 2, "C4": 3, "C5": 3, "C6": 3},
    }
    rows = [{"model_code": m, "criterion_code": c, "raw_score": v, "status": "annotated"}
            for m, cr in raws.items() for c, v in cr.items()]
    scores = pd.DataFrame(rows)
    verdicts = pd.DataFrame([
        {"model_code": m, "weighted_score": round(sum(cr[c] * WEIGHTS[c] for c in cr), 4),
         "complete": True, "verdict": "x"}
        for m, cr in raws.items()
    ])
    text = champion_challenger(scores, verdicts, "B")
    assert "Champion provisoire: B (conservé)" in text


def test_auto_rejection_when_c5_zero(tmp_path):
    body = ""
    for m in ["A", "B", "C"]:
        for c in ["C2", "C4", "C6"]:
            body += f"{m},{c},lbl,3,ok,me,2026-01-01\n"
        body += f"{m},C5,lbl,0,no added value,me,2026-01-01\n"
    ann = load_annotations(_write(tmp_path / "a.csv", body))
    verdicts = model_verdicts(compute_model_scores(_panel_high_stress(), ann))
    assert (verdicts["verdict"] == "rejected").all()
