"""Phase-separation statistics that beat the surrogate null.

The original C1/C3 counted high-stress months, so in a crisis-dominated window
*any* segmentation scored well and the champion was indistinguishable from chance
(null test p=1.0). These primitives replace "is there stress here?" with "do the
model's phase boundaries explain the stress structure better than a random
segmentation of the same shape?".

The core statistic is eta-squared: the share of a curve's stress variance
explained by the phase partition. A random contiguous segmentation of a uniform
crisis window explains almost nothing; a segmentation whose boundaries fall on
real regime changes explains a lot. The null is calibrated per phase-count, so a
model cannot win simply by using more phases (more groups inflate eta-squared for
the random baseline too).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

CURVES = ["E", "D", "S", "L", "I"]
OUTSIDE = "OUT"


def curve_stress_matrix(panel: pd.DataFrame, value_col: str) -> tuple[list[str], pd.DataFrame]:
    """Mean stress per curve (columns) and month (rows), available observations only."""
    months = sorted(panel["month"].astype(str).unique())
    available = panel[panel["status"] == "available"].copy()
    if available.empty:
        return months, pd.DataFrame(index=months)
    available["curve"] = available["variable_code"].str[0]
    mat = (available.groupby(["month", "curve"])[value_col].mean()
           .unstack("curve").reindex(index=months))
    return months, mat


def phase_labels(months: list[str], model: dict) -> np.ndarray:
    """Label each month with its phase name, or OUTSIDE if no phase covers it."""
    labels = np.full(len(months), OUTSIDE, dtype=object)
    for i, month in enumerate(months):
        for name, start, end in model["candidate_phases"]:
            if str(start) <= month <= str(end):
                labels[i] = name
                break
    return labels


def eta_squared(values: np.ndarray, labels: np.ndarray) -> float:
    """Between-group share of variance (one-way), ignoring NaN. 0 if undefined."""
    v = np.asarray(values, dtype=float)
    keep = ~np.isnan(v)
    v, lab = v[keep], np.asarray(labels)[keep]
    groups = set(lab.tolist())
    if v.size < 3 or len(groups) < 2:
        return 0.0
    grand = v.mean()
    ss_total = float(((v - grand) ** 2).sum())
    if ss_total == 0.0:
        return 0.0
    ss_between = float(sum(
        (v[lab == g].size) * (v[lab == g].mean() - grand) ** 2 for g in groups
    ))
    return ss_between / ss_total


def per_curve_eta(mat: pd.DataFrame, labels: np.ndarray) -> dict[str, float]:
    return {curve: eta_squared(mat[curve].to_numpy(), labels) for curve in mat.columns}


def aggregate_eta(mat: pd.DataFrame, labels: np.ndarray) -> float:
    """Mean eta-squared across curves that carry data."""
    per = [v for v in per_curve_eta(mat, labels).values()]
    return float(np.mean(per)) if per else 0.0


def random_labels(months: list[str], model: dict, rng: np.random.Generator) -> np.ndarray:
    """A random contiguous segmentation with the same phase count and covered span."""
    n = len(months)
    n_phases = len(model["candidate_phases"])
    covered = int(np.count_nonzero(phase_labels(months, model) != OUTSIDE))
    labels = np.full(n, OUTSIDE, dtype=object)
    if n_phases <= 1:
        span = max(1, covered)
        start = int(rng.integers(0, max(1, n - span + 1)))
        labels[start:start + span] = "p0"
        return labels
    cuts = sorted(int(c) for c in rng.choice(range(1, n), size=n_phases - 1, replace=False))
    bounds = [0, *cuts, n]
    for i in range(n_phases):
        labels[bounds[i]:bounds[i + 1]] = f"p{i}"
    return labels


def _null_percentiles(mat: pd.DataFrame, months: list[str], model: dict,
                      n_draws: int, seed: int, alpha: float) -> dict[str, float]:
    """(1-alpha) percentile of per-curve eta under random segmentations."""
    rng = np.random.default_rng(seed)
    draws = {curve: np.empty(n_draws) for curve in mat.columns}
    for d in range(n_draws):
        lab = random_labels(months, model, rng)
        for curve, value in per_curve_eta(mat, lab).items():
            draws[curve][d] = value
    return {curve: float(np.percentile(draws[curve], 100 * (1 - alpha)))
            for curve in mat.columns}


def confirming_curves(panel: pd.DataFrame, model: dict, n_draws: int = 500,
                      seed: int = 0, alpha: float = 0.05) -> dict:
    """Curves whose phase-separation beats the null, on the pre-crisis and both windows.

    Returns confirm_pre (synchronisation, C1), robust_both (dual-window, C3),
    the real per-curve eta, and the aggregate pre-crisis eta with its null mean.
    """
    months, mat_pre = curve_stress_matrix(panel, "stress_precrisis")
    _, mat_str = curve_stress_matrix(panel, "stress_structural")
    if mat_pre.empty:
        return {"confirm_pre": [], "robust_both": [], "eta_pre": {}, "n_curves": 0,
                "agg_real": 0.0, "agg_null_mean": 0.0}

    real_pre = per_curve_eta(mat_pre, phase_labels(months, model))
    real_str = per_curve_eta(mat_str, phase_labels(months, model))
    thr_pre = _null_percentiles(mat_pre, months, model, n_draws, seed, alpha)
    thr_str = _null_percentiles(mat_str, months, model, n_draws, seed + 1, alpha)

    confirm_pre = [c for c in mat_pre.columns if real_pre[c] >= thr_pre[c] and real_pre[c] > 0]
    robust_both = [c for c in confirm_pre
                   if c in mat_str.columns and real_str.get(c, 0.0) >= thr_str.get(c, 1.0)
                   and real_str.get(c, 0.0) > 0]
    return {
        "confirm_pre": confirm_pre,
        "robust_both": robust_both,
        "eta_pre": real_pre,
        "n_curves": int(mat_pre.shape[1]),
        "agg_real": aggregate_eta(mat_pre, phase_labels(months, model)),
        "agg_null_mean": float(np.mean(list(thr_pre.values()))) if thr_pre else 0.0,
    }
