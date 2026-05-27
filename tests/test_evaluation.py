from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.evaluation import evaluate_pilot, label_crisis_months, monthly_signal, roc_auc
from ecowave.pilots import Pilot

MONTHS = [f"2008-{m:02d}" for m in range(1, 13)]


def test_roc_auc_perfect_and_inverse():
    y = np.array([0, 0, 1, 1])
    assert roc_auc(y, np.array([0.1, 0.2, 0.8, 0.9])) == 1.0
    assert roc_auc(y, np.array([0.9, 0.8, 0.2, 0.1])) == 0.0


def test_roc_auc_ties_are_half():
    y = np.array([0, 0, 1, 1])
    assert roc_auc(y, np.array([0.5, 0.5, 0.5, 0.5])) == 0.5


def test_label_crisis_months():
    labels = label_crisis_months(MONTHS, (("2008-07", "2008-09"),))
    assert labels.sum() == 3
    assert labels[MONTHS.index("2008-08")] == 1
    assert labels[MONTHS.index("2008-01")] == 0


def _panel() -> pd.DataFrame:
    rows = []
    for code in ["E1", "D1", "L1"]:
        for month in MONTHS:
            stress = 95.0 if month >= "2008-07" else 15.0
            rows.append({
                "month": month, "variable_code": code, "raw_value": 1.0,
                "z_precrisis": 0.0, "stress_precrisis": stress,
                "z_structural": 0.0, "stress_structural": stress,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    return pd.DataFrame(rows)


def test_monthly_signal_and_evaluate_pilot():
    panel = _panel()
    sig = monthly_signal(panel)
    assert set(sig.columns) >= {"month", "mean_stress", "curve_count"}
    pilot = Pilot(code="t", title="t", panel_start="2008-01", panel_end="2008-12",
                  dow_context="", champion="B", models={},
                  crisis_months=(("2008-07", "2008-12"),))
    result = evaluate_pilot(panel, pilot)
    # Stress is high exactly in the labelled crisis months -> perfect separation.
    assert result.auroc_mean_stress == 1.0
    assert result.n_crisis == 6 and result.n_calm == 6
