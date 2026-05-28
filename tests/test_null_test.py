from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.scoring.null_test import (
    all_models_null_report,
    champion_null_report,
    circular_shift_surrogate,
    null_pvalue,
    random_segmentation_null,
)

MONTHS = [f"{y}-{m:02d}" for y in range(2007, 2013) for m in range(1, 13)]
SHIFT = "2010-01"  # regime change date


def _regime_panel() -> pd.DataFrame:
    """Calm then crisis, with the change exactly at the champion's cycle boundary."""
    rows = []
    for code in ["E1", "E2", "D1", "D2", "L1"]:
        for month in MONTHS:
            stress = 95.0 if month >= SHIFT else 10.0
            rows.append({
                "month": month, "variable_code": code, "raw_value": 1.0,
                "z_precrisis": 0.0, "stress_precrisis": stress,
                "z_structural": 0.0, "stress_structural": stress,
                "status": "available", "source": "x", "confidence": "A", "notes": "",
            })
    return pd.DataFrame(rows)


# Two-cycle champion whose boundary splits calm vs crisis.
CHAMPION = {"candidate_phases": [("calm", MONTHS[0], "2009-12"), ("crisis", SHIFT, MONTHS[-1])]}


def test_null_pvalue_extremes():
    null = np.arange(0, 100, dtype=float)
    pct_low, p_low = null_pvalue(200.0, null)
    pct_high, p_high = null_pvalue(-5.0, null)
    assert p_low < 0.05 and pct_low == 100.0
    assert p_high > 0.9 and pct_high == 0.0


def test_surrogate_shapes():
    panel = _regime_panel()
    seg = random_segmentation_null(panel, CHAMPION, n_draws=50, seed=1)
    shift = circular_shift_surrogate(panel, CHAMPION, n_draws=50, seed=1)
    assert seg.shape == (50,)
    assert shift.shape == (50,)


def test_champion_beats_null_on_structured_panel():
    report = champion_null_report(_regime_panel(), CHAMPION, n_draws=300, seed=7)
    assert report["real"] > 0.5  # the boundary explains most of the variance
    for r in report["results"]:
        assert r.real >= r.null_mean
    # Circular shift is the synchronisation test: a real boundary beats it.
    assert not report["flag_shift"]


def test_all_models_null_report_runs_per_model():
    # A: the correct two-cycle champion; B: same but mis-aligned by 6 months.
    model_a = CHAMPION
    model_b = {
        "candidate_phases": [("calm", MONTHS[0], "2010-06"), ("crisis", "2010-07", MONTHS[-1])]
    }
    reports = all_models_null_report(_regime_panel(), {"A": model_a, "B": model_b},
                                     n_draws=50, seed=3)
    assert set(reports) == {"A", "B"}
    # Correctly-aligned A should beat circular-shift null; B may not.
    assert not reports["A"]["flag_shift"]
    assert "real" in reports["A"] and "real" in reports["B"]


def test_all_models_null_report_skips_models_without_phases():
    reports = all_models_null_report(_regime_panel(), {"A": CHAMPION, "Z": {}}, n_draws=20)
    assert "A" in reports
    assert "Z" not in reports
