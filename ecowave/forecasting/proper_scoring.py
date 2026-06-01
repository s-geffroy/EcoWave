"""Proper scoring rules and forecast-evaluation metrics.

Why proper scoring rules. The CPV cluster (long memory + multifractality
+ non-linearity + heavy tails) implies that mean-squared error and mean-
absolute error are *not* sufficient to rank competing probabilistic
forecasters: they reward models that predict the conditional mean well
but ignore predictive sharpness and tail calibration. The Continuous
Ranked Probability Score (CRPS), per :ref:`Gneiting & Raftery (2007)
<gneiting-raftery-2007>`, is a *strictly proper* scoring rule that
rewards a forecast distribution which is both sharp and well-calibrated
to the realisation — exactly what the CPV verdict says we need.

Empirical CRPS. For a forecast represented by ``M`` Monte Carlo samples
``x_1, …, x_M`` and an observation ``y``,

    CRPS(F, y) ≈ (1/M) Σ |x_m − y| − (1/(2 M²)) Σ_m Σ_{m'} |x_m − x_{m'}|

This is the unbiased sample estimator. For ``M = 1000`` the cost is
~1 M absolute differences per evaluation — acceptable for benchmark-
scale loops over tens of variables × five horizons.

Coverage. ``coverage_level(samples, y, level)`` returns 1 iff ``y``
falls inside the central ``level`` predictive interval, derived from
sample quantiles. ``tail_coverage`` checks the *one-sided* tail at
``alpha``: under heavy tails the symmetric coverage can be well-
calibrated yet tails systematically under-covered, so we track both.

Mincer-Zarnowitz. ``mincer_zarnowitz`` regresses ``y`` on the point
forecast and tests the joint hypothesis (α, β) = (0, 1) — the classical
test of forecast unbiasedness and efficiency.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class ForecastScores:
    """Bundle of scalar scores computed for one (forecast, realisation) pair."""

    rmse: float
    mae: float
    crps: float
    coverage_95: float
    tail_coverage_left_5pct: float
    tail_coverage_right_5pct: float
    bias: float


def empirical_crps(samples: np.ndarray, observation: float) -> float:
    """Sample-based estimate of the Continuous Ranked Probability Score.

    Uses the unbiased identity
    ``CRPS = E|X − y| − ½ E|X − X'|`` where ``X, X'`` are i.i.d. draws
    from the predictive distribution. Lower is better; CRPS reduces to
    MAE when the forecast is a point mass.

    Parameters
    ----------
    samples:
        1-D array of ``M`` samples from the predictive distribution.
    observation:
        Realised value.
    """
    samples = np.asarray(samples, dtype=float).ravel()
    if samples.size == 0:
        raise ValueError("samples must be non-empty")
    if not np.isfinite(observation):
        raise ValueError(f"observation must be finite; got {observation}")

    mean_abs_dev = np.abs(samples - observation).mean()
    n = samples.size
    sorted_samples = np.sort(samples)
    # E|X - X'| via the rank-based identity for the L1 Gini-mean-difference:
    #   E|X - X'| = (2 / n^2) Σ_i (2 i − n − 1) x_(i)   for i = 1 … n
    ranks = np.arange(1, n + 1, dtype=float)
    spread = (2.0 * (2.0 * ranks - n - 1.0) * sorted_samples).sum() / (n * n)
    return float(mean_abs_dev - 0.5 * spread)


def coverage_indicator(samples: np.ndarray, observation: float, level: float = 0.95) -> int:
    """Return 1 iff ``observation`` falls within the central ``level`` interval."""
    if not 0.0 < level < 1.0:
        raise ValueError(f"level must be in (0, 1); got {level}")
    samples = np.asarray(samples, dtype=float).ravel()
    alpha = (1.0 - level) / 2.0
    lower, upper = np.quantile(samples, [alpha, 1.0 - alpha])
    return int(lower <= observation <= upper)


def tail_coverage_indicator(
    samples: np.ndarray,
    observation: float,
    alpha: float = 0.05,
    tail: str = "right",
) -> int:
    """Return 1 iff ``observation`` falls in the predictive ``alpha`` tail.

    ``tail = "right"`` checks ``observation >= q_{1-alpha}`` ;
    ``tail = "left"`` checks ``observation <= q_alpha``. Under the CPV
    cluster, heavy tails matter: a well-calibrated forecast should match
    the empirical tail-exceedance rate at ``alpha``.
    """
    if tail not in {"left", "right"}:
        raise ValueError(f"tail must be 'left' or 'right'; got {tail!r}")
    samples = np.asarray(samples, dtype=float).ravel()
    if tail == "right":
        threshold = float(np.quantile(samples, 1.0 - alpha))
        return int(observation >= threshold)
    threshold = float(np.quantile(samples, alpha))
    return int(observation <= threshold)


def score_forecast(samples: np.ndarray, observation: float) -> ForecastScores:
    """Compute the bundle of scalar scores for one realised observation."""
    samples = np.asarray(samples, dtype=float).ravel()
    point = float(samples.mean())
    return ForecastScores(
        rmse=float(abs(point - observation)),  # one-shot pair: RMSE == |residual|
        mae=float(abs(point - observation)),
        crps=empirical_crps(samples, observation),
        coverage_95=float(coverage_indicator(samples, observation, level=0.95)),
        tail_coverage_left_5pct=float(
            tail_coverage_indicator(samples, observation, alpha=0.05, tail="left")
        ),
        tail_coverage_right_5pct=float(
            tail_coverage_indicator(samples, observation, alpha=0.05, tail="right")
        ),
        bias=float(point - observation),
    )


def aggregate_rmse(predictions: Sequence[float], realisations: Sequence[float]) -> float:
    """Root-mean-squared error across a sequence of (forecast, realised) pairs."""
    predictions_arr = np.asarray(predictions, dtype=float)
    realisations_arr = np.asarray(realisations, dtype=float)
    if predictions_arr.shape != realisations_arr.shape:
        raise ValueError(
            f"shape mismatch: predictions {predictions_arr.shape} vs "
            f"realisations {realisations_arr.shape}"
        )
    return float(np.sqrt(np.mean((predictions_arr - realisations_arr) ** 2)))


def aggregate_mae(predictions: Sequence[float], realisations: Sequence[float]) -> float:
    """Mean absolute error across a sequence of (forecast, realised) pairs."""
    predictions_arr = np.asarray(predictions, dtype=float)
    realisations_arr = np.asarray(realisations, dtype=float)
    if predictions_arr.shape != realisations_arr.shape:
        raise ValueError(
            f"shape mismatch: predictions {predictions_arr.shape} vs "
            f"realisations {realisations_arr.shape}"
        )
    return float(np.mean(np.abs(predictions_arr - realisations_arr)))


@dataclass(frozen=True)
class MincerZarnowitzResult:
    """Coefficients and joint test of unbiasedness/efficiency."""

    alpha: float
    beta: float
    f_statistic: float
    p_value: float
    n_observations: int


def mincer_zarnowitz(
    predictions: Sequence[float], realisations: Sequence[float]
) -> MincerZarnowitzResult:
    """Mincer-Zarnowitz regression of realisations on point forecasts.

    Estimates ``y = alpha + beta * y_hat + eps`` and reports an F-test of
    the joint null ``(alpha, beta) = (0, 1)``. A failure to reject is the
    classical Mincer-Zarnowitz pass: the forecast is unbiased and
    efficient.
    """
    import statsmodels.api as sm

    predictions_arr = np.asarray(predictions, dtype=float)
    realisations_arr = np.asarray(realisations, dtype=float)
    if predictions_arr.shape != realisations_arr.shape:
        raise ValueError(
            f"shape mismatch: predictions {predictions_arr.shape} vs "
            f"realisations {realisations_arr.shape}"
        )
    if predictions_arr.size < 3:
        raise ValueError(
            f"need ≥ 3 paired observations for MZ regression; got {predictions_arr.size}"
        )

    design = sm.add_constant(predictions_arr)
    model = sm.OLS(realisations_arr, design).fit()
    test = model.f_test("const = 0, x1 = 1")
    return MincerZarnowitzResult(
        alpha=float(model.params[0]),
        beta=float(model.params[1]),
        f_statistic=float(np.squeeze(test.fvalue)),
        p_value=float(np.squeeze(test.pvalue)),
        n_observations=int(predictions_arr.size),
    )
