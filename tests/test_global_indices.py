from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from ecowave.scoring.global_indices import (
    CURVES,
    MIN_CURVES_SCORED,
    apply_hp_filter,
    apply_ma3,
    compute_diffusion,
    compute_global_indices,
    compute_intensity,
    equal_weights,
    favar_weights,
    pca_weights,
)


def _months(n: int, start: str = "2005-01") -> list[str]:
    return [str(d.to_period("M")) for d in pd.date_range(start, periods=n, freq="MS")]


# ---------------------------------------------------------------------------
# Weights
# ---------------------------------------------------------------------------

def test_equal_weights_sum_to_one_and_are_uniform():
    w = equal_weights()
    assert set(w) == set(CURVES)
    assert pytest.approx(sum(w.values()), abs=1e-9) == 1.0
    assert all(abs(v - 0.2) < 1e-9 for v in w.values())


def test_pca_weights_returns_none_on_degenerate_panel():
    months = _months(60)
    flat = pd.DataFrame({c: 50.0 for c in CURVES}, index=months)
    assert pca_weights(flat) is None


def test_pca_weights_returns_normalised_loadings_with_variance():
    rng = np.random.default_rng(7)
    months = _months(60)
    common = rng.normal(50, 10, size=60)
    panel = pd.DataFrame(
        {c: common + rng.normal(0, 1, size=60) for c in CURVES},
        index=months,
    )
    w = pca_weights(panel)
    assert w is not None
    assert pytest.approx(sum(w.values()), abs=1e-9) == 1.0
    assert all(v >= 0 for v in w.values())


def test_pca_weights_too_short_returns_none():
    panel = pd.DataFrame({c: [1.0, 2.0, 3.0] for c in CURVES}, index=_months(3))
    assert pca_weights(panel) is None


def test_favar_weights_identifies_predictive_curve():
    rng = np.random.default_rng(11)
    months = _months(60)
    anchor = pd.Series(rng.normal(0, 1, size=60), index=months)
    # D is highly predictive (D_t ~ anchor_{t+6}); others are noise.
    shifted = anchor.shift(-6).fillna(0.0).to_numpy()
    panel = pd.DataFrame({
        "E": rng.normal(50, 5, size=60),
        "D": 50 + 10 * shifted + rng.normal(0, 0.5, size=60),
        "S": rng.normal(50, 5, size=60),
        "L": rng.normal(50, 5, size=60),
        "I": rng.normal(50, 5, size=60),
    }, index=months)
    w = favar_weights(panel, anchor)
    assert w is not None
    assert pytest.approx(sum(w.values()), abs=1e-9) == 1.0
    assert w["D"] > 0.5, w


def test_favar_weights_returns_none_without_anchor():
    panel = pd.DataFrame({c: np.linspace(0, 100, 60) for c in CURVES}, index=_months(60))
    assert favar_weights(panel, pd.Series(dtype=float)) is None


# ---------------------------------------------------------------------------
# Index primitives
# ---------------------------------------------------------------------------

def test_compute_intensity_equal_weights_returns_mean():
    row = pd.Series({"E": 50, "D": 50, "S": 50, "L": 50, "I": 50})
    assert compute_intensity(row, equal_weights()) == pytest.approx(50.0)


def test_compute_intensity_weighted_mixture():
    row = pd.Series({"E": 90, "D": 90, "S": 90, "L": 90, "I": 10})
    assert compute_intensity(row, equal_weights()) == pytest.approx(74.0)


def test_compute_intensity_returns_none_if_too_few_curves():
    row = pd.Series({"E": 70, "D": np.nan, "S": np.nan, "L": np.nan, "I": np.nan})
    assert compute_intensity(row, equal_weights()) is None


def test_compute_intensity_renormalises_weights_over_available_curves():
    # When the missing curve was carrying part of the weight, the surviving
    # weights are renormalised to sum to 1 over the available curves. This
    # preserves the user's intent (don't fall back to equal silently).
    weights = {"E": 0.5, "D": 0.3, "S": 0.1, "L": 0.05, "I": 0.05}
    row = pd.Series({"E": 80, "D": np.nan, "S": 40, "L": 40, "I": 40})
    expected = (0.5 * 80 + 0.1 * 40 + 0.05 * 40 + 0.05 * 40) / (0.5 + 0.1 + 0.05 + 0.05)
    assert compute_intensity(row, weights) == pytest.approx(expected)


def test_compute_intensity_falls_back_to_equal_when_all_weights_zero():
    # Pathological case: original weights are all zero on the available curves.
    # The function silently restores equal weighting so we still get a number.
    weights = {"E": 0.0, "D": 1.0, "S": 0.0, "L": 0.0, "I": 0.0}
    row = pd.Series({"E": 80, "D": np.nan, "S": 40, "L": 40, "I": 40})
    assert compute_intensity(row, weights) == pytest.approx((80 + 40 + 40 + 40) / 4)


def test_compute_diffusion_counts_above_threshold():
    row = pd.Series({"E": 90, "D": 81, "S": 50, "L": 30, "I": 100})
    assert compute_diffusion(row) == 3


def test_apply_ma3_smooths_input():
    s = pd.Series([0.0, 10.0, 20.0, 30.0, 40.0])
    ma = apply_ma3(s)
    assert ma.iloc[1] == pytest.approx(10.0)
    assert ma.iloc[2] == pytest.approx(20.0)


def test_apply_hp_filter_decomposes_into_trend_plus_cycle():
    rng = np.random.default_rng(3)
    n = 120
    months = _months(n)
    trend_true = np.linspace(20, 80, n)
    cycle_true = 5 * np.sin(np.linspace(0, 4 * np.pi, n))
    series = pd.Series(trend_true + cycle_true + rng.normal(0, 0.5, n), index=months)
    trend, cycle = apply_hp_filter(series)
    assert (trend + cycle).iloc[10:-10].sub(series.iloc[10:-10]).abs().max() < 1e-6


# ---------------------------------------------------------------------------
# End-to-end: compute_global_indices
# ---------------------------------------------------------------------------

def _make_curve_scores(months: list[str]) -> pd.DataFrame:
    rng = np.random.default_rng(13)
    rows = []
    for m in months:
        for c in CURVES:
            rows.append({
                "month": m,
                "curve": c,
                "stress_precrisis": float(rng.uniform(20, 80)),
                "stress_structural": float(rng.uniform(20, 80)),
                "variables_available": 1,
                "variables_expected": 1,
                "status": "scored",
                "notes": "",
            })
    return pd.DataFrame(rows)


def test_compute_global_indices_long_format_and_required_columns():
    months = _months(48)
    curves = _make_curve_scores(months)
    out = compute_global_indices(curves, anchor=None)
    expected_cols = {
        "month", "ref", "weighting", "weighting_actual", "intensity",
        "intensity_ma3", "intensity_hp_cycle", "intensity_hp_trend",
        "diffusion", "curves_scored", "weights_json", "status",
    }
    assert expected_cols.issubset(out.columns)
    assert set(out["weighting"]) == {"equal", "pca", "favar"}
    assert set(out["ref"]) == {"precrisis", "structural"}
    # Diffusion is 0..5
    assert int(out["diffusion"].min()) >= 0
    assert int(out["diffusion"].max()) <= 5
    # No anchor -> FAVAR should fall back.
    favar_actual = set(out[out["weighting"] == "favar"]["weighting_actual"])
    assert all("favar" not in v or v != "favar" for v in favar_actual) or "favar" not in favar_actual


def test_min_curves_threshold_blocks_intensity():
    months = _months(36)
    rows = []
    for m in months:
        # Only 2 curves available -> below MIN_CURVES_SCORED=3 -> blocked.
        for c in CURVES[:2]:
            rows.append({
                "month": m, "curve": c, "stress_precrisis": 50.0,
                "stress_structural": 50.0,
                "variables_available": 1, "variables_expected": 1,
                "status": "scored", "notes": "",
            })
    curves = pd.DataFrame(rows)
    out = compute_global_indices(curves, anchor=None)
    blocked = out[out["status"] == "blocked"]
    assert not blocked.empty
    assert blocked["intensity"].isna().all()


def test_min_curves_constant_matches_design():
    assert MIN_CURVES_SCORED == 3
