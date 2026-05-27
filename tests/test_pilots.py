from __future__ import annotations

import pandas as pd
import pytest

from ecowave.pilots import PILOTS, get_pilot
from ecowave.scoring.model_scores import champion_challenger, compute_model_scores, model_verdicts


def test_pilots_registered():
    assert {"2008", "2016", "2020", "2022", "2000"} <= set(PILOTS)
    assert get_pilot("2016").panel_start == "2011-01"
    assert get_pilot("2016").panel_end == "2016-12"


def test_holdout_pilots_preregistered():
    for code in ("2020", "2022"):
        pilot = get_pilot(code)
        assert pilot.holdout is True
        assert pilot.registered_at  # non-empty timestamp
        assert pilot.crisis_months  # has reference dating for AUROC


def test_2000_overrides_reference_windows():
    pilot = get_pilot("2000")
    assert pilot.precrisis == ("1990-01", "1998-12")  # clean pre-bust baseline


def test_unknown_pilot_raises():
    with pytest.raises(ValueError, match="Unknown pilot"):
        get_pilot("1999")


def _panel_for(start_year: int, end_year: int, shift: str) -> pd.DataFrame:
    """Two-regime panel with the change at `shift` (aligned to the pilot's B boundary)."""
    rows = []
    months = [f"{y}-{m:02d}" for y in range(start_year, end_year + 1) for m in range(1, 13)]
    for code in ["E1", "E2", "D1", "L1", "S1"]:
        for mth in months:
            stress = 90.0 if mth >= shift else 10.0
            rows.append({
                "month": mth, "variable_code": code, "raw_value": 1.0,
                "z_precrisis": 0.0, "stress_precrisis": stress,
                "z_structural": 0.0, "stress_structural": stress,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    return pd.DataFrame(rows)


def test_2016_models_scored_on_their_window():
    pilot = get_pilot("2016")
    # Model B (2016) splits at 2013-01; align the regime change there.
    scores = compute_model_scores(_panel_for(2011, 2016, "2013-01"), models=pilot.models,
                                  n_draws=150)
    c1 = scores[(scores["model_code"] == "B") & (scores["criterion_code"] == "C1")].iloc[0]
    assert c1["status"] == "computed"
    assert c1["raw_score"] >= 1
    verdicts = model_verdicts(scores)
    # No annotations -> blocked, and champion text mentions the pilot champion B.
    assert (verdicts["verdict"] == "blocked").all()
    assert "non tranché" in champion_challenger(scores, verdicts, pilot.champion)
