from __future__ import annotations

import pandas as pd
import pytest

from ecowave.scoring.annotations import load_annotations
from ecowave.scoring.model_scores import (
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
    assert "Champion provisoire" in champion_challenger(scores, verdicts)


def test_auto_rejection_when_c5_zero(tmp_path):
    body = ""
    for m in ["A", "B", "C"]:
        for c in ["C2", "C4", "C6"]:
            body += f"{m},{c},lbl,3,ok,me,2026-01-01\n"
        body += f"{m},C5,lbl,0,no added value,me,2026-01-01\n"
    ann = load_annotations(_write(tmp_path / "a.csv", body))
    verdicts = model_verdicts(compute_model_scores(_panel_high_stress(), ann))
    assert (verdicts["verdict"] == "rejected").all()
