from __future__ import annotations

import pandas as pd
import pytest

from ecowave.pilots import PILOTS, get_pilot
from ecowave.scoring.model_scores import champion_challenger, compute_model_scores, model_verdicts


def test_two_pilots_registered():
    assert set(PILOTS) == {"2008", "2016"}
    assert get_pilot("2016").panel_start == "2011-01"
    assert get_pilot("2016").panel_end == "2016-12"


def test_unknown_pilot_raises():
    with pytest.raises(ValueError, match="Unknown pilot"):
        get_pilot("1999")


def _panel_for(start_year: int, end_year: int) -> pd.DataFrame:
    rows = []
    months = [f"{y}-{m:02d}" for y in range(start_year, end_year + 1) for m in range(1, 13)]
    for code in ["E1", "E2", "D1", "L1", "S1"]:
        for mth in months:
            rows.append({
                "month": mth, "variable_code": code, "raw_value": 1.0,
                "z_precrisis": 3.0, "stress_precrisis": 95.0,
                "z_structural": 3.0, "stress_structural": 90.0,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    return pd.DataFrame(rows)


def test_2016_models_scored_on_their_window():
    pilot = get_pilot("2016")
    scores = compute_model_scores(_panel_for(2011, 2016), models=pilot.models)
    # C1 computed for the 2016 models using their candidate windows.
    c1 = scores[(scores["model_code"] == "B") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["status"] == "computed"
    assert c1["raw_score"] >= 1
    verdicts = model_verdicts(scores)
    # No annotations -> blocked, and champion text mentions the pilot champion B.
    assert (verdicts["verdict"] == "blocked").all()
    assert "non tranché" in champion_challenger(scores, verdicts, pilot.champion)
