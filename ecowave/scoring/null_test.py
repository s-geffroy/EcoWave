"""Null / surrogate test on the champion's phase-separation evidence.

The falsifiability gate. The discriminating statistic is the champion's mean
phase-separation (eta-squared across curves, pre-crisis stress) — the same
quantity that drives the redefined C1/C3 (see scoring/segmentation.py). We
compare it to two nulls:

- `random_segmentation_null`: same phase count and covered span, boundaries drawn
  at random. Tests whether the champion's *boundary placement* matters.
- `circular_shift_surrogate`: the champion's real boundaries, but each curve's
  stress series circularly shifted by an independent random offset (preserves
  each curve's marginal/autocorrelation, destroys alignment with the boundaries).
  Tests whether the cross-curve structure at the boundaries is more than chance.

A red flag is raised when the champion is not distinguishable from a null at
alpha (p >= 0.05). Only auto-computed evidence is surrogated; the analyst
criteria C2/C4/C5/C6 cannot be and are excluded by design.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ecowave.scoring.segmentation import (
    aggregate_eta,
    curve_stress_matrix,
    phase_labels,
    random_labels,
)

DEFAULT_DRAWS = 500
RED_FLAG_ALPHA = 0.05


@dataclass(frozen=True)
class NullResult:
    method: str
    statistic: str
    real: float
    null_mean: float
    percentile: float   # share of the null strictly below the real value (0-100)
    p_value: float      # P(null >= real), add-one smoothed
    n_draws: int


def random_segmentation_null(panel: pd.DataFrame, model: dict,
                             n_draws: int = DEFAULT_DRAWS, seed: int = 0) -> np.ndarray:
    """Mean phase-separation (eta-squared) for random segmentations of the same shape."""
    rng = np.random.default_rng(seed)
    months, mat = curve_stress_matrix(panel, "stress_precrisis")
    out = np.empty(n_draws, dtype=float)
    for i in range(n_draws):
        out[i] = aggregate_eta(mat, random_labels(months, model, rng))
    return out


def circular_shift_surrogate(panel: pd.DataFrame, model: dict,
                             n_draws: int = DEFAULT_DRAWS, seed: int = 0) -> np.ndarray:
    """Mean phase-separation under per-curve circular shifts on the real boundaries."""
    rng = np.random.default_rng(seed)
    months, mat = curve_stress_matrix(panel, "stress_precrisis")
    labels = phase_labels(months, model)
    n = len(months)
    out = np.empty(n_draws, dtype=float)
    for i in range(n_draws):
        shifted = mat.copy()
        for curve in mat.columns:
            k = int(rng.integers(1, n)) if n > 1 else 0
            shifted[curve] = np.roll(mat[curve].to_numpy(), k)
        out[i] = aggregate_eta(shifted, labels)
    return out


def null_pvalue(real: float, null_dist: np.ndarray) -> tuple[float, float]:
    """Return (percentile, p_value) of `real` against a 1-D null distribution."""
    null = np.asarray(null_dist, dtype=float)
    n = null.size
    percentile = float((null < real).mean() * 100.0) if n else float("nan")
    p_value = float((np.count_nonzero(null >= real) + 1) / (n + 1)) if n else float("nan")
    return percentile, p_value


def champion_null_report(panel: pd.DataFrame, model: dict,
                         n_draws: int = DEFAULT_DRAWS, seed: int = 0) -> dict:
    """Test whether the champion's mean phase-separation beats both nulls.

    `flag_random`/`flag_shift` are True when the champion is NOT distinguishable
    from the null at alpha=0.05 (a red flag for the report).
    """
    months, mat = curve_stress_matrix(panel, "stress_precrisis")
    real = aggregate_eta(mat, phase_labels(months, model))

    seg = random_segmentation_null(panel, model, n_draws=n_draws, seed=seed)
    shift = circular_shift_surrogate(panel, model, n_draws=n_draws, seed=seed + 1)
    seg_pct, seg_p = null_pvalue(real, seg)
    shift_pct, shift_p = null_pvalue(real, shift)

    results = [
        NullResult("random_segmentation", "mean eta^2", real, float(seg.mean()),
                   seg_pct, seg_p, n_draws),
        NullResult("circular_shift", "mean eta^2", real, float(shift.mean()),
                   shift_pct, shift_p, n_draws),
    ]
    return {
        "real": real,
        "results": results,
        "flag_random": seg_p >= RED_FLAG_ALPHA,
        "flag_shift": shift_p >= RED_FLAG_ALPHA,
        "alpha": RED_FLAG_ALPHA,
    }
