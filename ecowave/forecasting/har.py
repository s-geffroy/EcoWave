"""Heterogeneous Autoregressive model — :ref:`Corsi (2009)
<corsi-2009>`.

HAR is the workhorse benchmark for the long-memory-by-aggregation
hypothesis. Instead of modelling the autocorrelation function with a
fractional integration parameter, Corsi aggregates the series itself
into short-horizon, medium-horizon, and long-horizon means and runs
OLS on the three. The resulting predictive density has a non-trivial
long memory structure even though each component is an MA: the
aggregation creates the slowly-decaying autocorrelation tail that
matches family C of the CPV cluster.

Why HAR matters as a baseline. It is trivially cheap to fit (OLS), it
has a closed-form predictive distribution under Gaussian residuals, and
it is the working horse on which more sophisticated models (MSM,
ARFIMA+RS) must improve in order to claim any operational value. If MSM
fails to beat HAR on out-of-sample CRPS, MSM is theoretically
satisfying but operationally redundant.

Default lag horizons. Following Corsi's original calibration on daily
realised volatility (1, 5, 22), the defaults here are ``(1, k, l)``
where ``k`` and ``l`` are passed by the caller — for monthly data the
canonical choice is ``(1, 3, 12)`` and for quarterly ``(1, 2, 4)``. The
defaults below assume monthly cadence; the benchmark pipeline (PR D)
will pass the correct ``lag_horizons`` per panel.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ecowave.forecasting.types import ProbabilisticForecast


@dataclass(frozen=True)
class HARLagConfig:
    """Definition of the three aggregation horizons (short, medium, long).

    Each element is the number of past observations averaged to build
    the corresponding regressor.
    """

    short: int = 1
    medium: int = 3
    long: int = 12

    def __post_init__(self) -> None:
        if not (0 < self.short < self.medium < self.long):
            raise ValueError(
                f"HAR lags must satisfy 0 < short < medium < long; got "
                f"({self.short}, {self.medium}, {self.long})"
            )


def _aggregate_lag(series: np.ndarray, window: int) -> np.ndarray:
    """Return the trailing rolling mean over ``window`` for use as a lagged regressor.

    For a 1-D ``series`` of length ``T``, the output at index ``t`` is
    ``mean(series[t - window + 1 : t + 1])`` for ``t >= window - 1`` and
    ``np.nan`` elsewhere. Aligns with Corsi's convention of taking the
    average of past observations ending at the current time.
    """
    if window <= 0:
        raise ValueError(f"window must be positive; got {window}")
    cumulative_sum = np.cumsum(series, dtype=float)
    rolling = np.empty_like(series, dtype=float)
    rolling[:] = np.nan
    if series.size < window:
        return rolling
    rolling[window - 1] = cumulative_sum[window - 1] / window
    rolling[window:] = (cumulative_sum[window:] - cumulative_sum[:-window]) / window
    return rolling


def _build_design_matrix(
    series: np.ndarray, config: HARLagConfig
) -> tuple[np.ndarray, np.ndarray, int]:
    """Return ``(design, target, first_usable_index)`` for the HAR regression."""
    short_lag = _aggregate_lag(series, config.short)
    medium_lag = _aggregate_lag(series, config.medium)
    long_lag = _aggregate_lag(series, config.long)
    # Each lag is observed at index t and used to predict t + 1; shift by 1.
    shifted_short = np.concatenate([[np.nan], short_lag[:-1]])
    shifted_medium = np.concatenate([[np.nan], medium_lag[:-1]])
    shifted_long = np.concatenate([[np.nan], long_lag[:-1]])
    intercept = np.ones_like(series, dtype=float)
    full_design = np.column_stack([intercept, shifted_short, shifted_medium, shifted_long])
    finite_mask = np.all(np.isfinite(full_design), axis=1)
    first_index = int(np.argmax(finite_mask)) if finite_mask.any() else series.size
    return full_design[finite_mask], series[finite_mask], first_index


def har_forecast(
    history: np.ndarray,
    horizons: list[int] | tuple[int, ...],
    n_samples: int = 1000,
    seed: int = 0,
    lag_config: HARLagConfig | None = None,
) -> ProbabilisticForecast:
    """HAR(1) probabilistic forecast with Gaussian-residual sampling.

    Fits ``y_t = c + b_s · S_{t-1} + b_m · M_{t-1} + b_l · L_{t-1} + eps_t``
    on the in-sample history then iterates forward by recomputing the
    three aggregated lags from each path's growing tail. Innovations
    are i.i.d. Gaussian with variance equal to the OLS residual variance.

    Parameters
    ----------
    history:
        1-D history of length ≥ ``lag_config.long + 4`` for OLS
        identification.
    horizons:
        Forecast horizons in cadence steps.
    n_samples:
        Number of Monte Carlo paths.
    seed:
        RNG seed.
    lag_config:
        Three aggregation horizons; defaults to monthly cadence
        ``(1, 3, 12)``.
    """
    config = lag_config or HARLagConfig()
    history_arr = np.asarray(history, dtype=float).ravel()
    if not np.all(np.isfinite(history_arr)):
        raise ValueError("history contains non-finite values")
    minimum_length = config.long + 4
    if history_arr.size < minimum_length:
        raise ValueError(
            f"HAR requires history of length ≥ {minimum_length}; got {history_arr.size}"
        )
    horizons_tuple = tuple(int(horizon) for horizon in horizons)
    if not horizons_tuple or any(horizon <= 0 for horizon in horizons_tuple):
        raise ValueError(f"horizons must be positive; got {horizons_tuple}")

    design, target, _ = _build_design_matrix(history_arr, config)
    if design.shape[0] < 4:
        raise ValueError(
            f"HAR design matrix has only {design.shape[0]} usable rows after "
            "lag construction (need ≥ 4)"
        )
    coefficients, *_ = np.linalg.lstsq(design, target, rcond=None)
    residuals = target - design @ coefficients
    sigma = float(np.std(residuals, ddof=4)) if residuals.size > 4 else 0.0

    rng = np.random.default_rng(seed)
    max_horizon = max(horizons_tuple)
    paths = np.empty((n_samples, max_horizon), dtype=float)
    for sample_index in range(n_samples):
        extended = np.concatenate([history_arr, np.empty(max_horizon, dtype=float)])
        for step_offset in range(max_horizon):
            tail_end = history_arr.size + step_offset
            short_mean = extended[tail_end - config.short : tail_end].mean()
            medium_mean = extended[tail_end - config.medium : tail_end].mean()
            long_mean = extended[tail_end - config.long : tail_end].mean()
            point = (
                coefficients[0]
                + coefficients[1] * short_mean
                + coefficients[2] * medium_mean
                + coefficients[3] * long_mean
            )
            innovation = float(rng.standard_normal()) * sigma
            extended[tail_end] = point + innovation
        paths[sample_index, :] = extended[history_arr.size : history_arr.size + max_horizon]

    samples = paths[:, [horizon - 1 for horizon in horizons_tuple]]
    return ProbabilisticForecast(
        horizons=horizons_tuple,
        samples=samples,
        model_name="har",
        metadata={
            "intercept": float(coefficients[0]),
            "beta_short": float(coefficients[1]),
            "beta_medium": float(coefficients[2]),
            "beta_long": float(coefficients[3]),
            "sigma_residual": sigma,
            "lag_config": (config.short, config.medium, config.long),
        },
    )
