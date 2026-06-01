"""Canonical forecast baselines: random walk, AR(1), ARMA(1, 1).

These are the comparators every CPV-cluster model must beat to claim any
operational value. The choice is deliberate: the random walk is the
strongest "no-model" benchmark for level series and remains famously
hard to beat at short horizons (Atkeson-Ohanian 2001 for inflation;
Welch-Goyal 2008 for equity premia); AR(1) and ARMA(1, 1) are the
simplest stationary alternatives and serve as efficient-market-style
sanity checks.

All three forecasters share the contract documented in
:mod:`ecowave.forecasting.types`: given a 1-D history they return a
:class:`ProbabilisticForecast` whose ``samples`` matrix is shaped
``(n_samples, n_horizons)`` and lives on the *level* of the original
series.

The forecasters use Gaussian innovations whose variance is estimated by
the model's residual variance. This is convenient and unbiased on the
mean; it under-prices the empirical tail in the presence of the CPV
cluster — which is *the point*: heavy-tail aware forecasters (MSM,
ARFIMA+RS) should out-score these baselines on CRPS and tail coverage,
not on RMSE alone.
"""
from __future__ import annotations

import numpy as np

from ecowave.forecasting.types import ProbabilisticForecast


def _validate_history(history: np.ndarray, min_length: int) -> np.ndarray:
    array = np.asarray(history, dtype=float).ravel()
    if not np.all(np.isfinite(array)):
        raise ValueError("history contains non-finite values")
    if array.size < min_length:
        raise ValueError(
            f"history of length {array.size} is below required minimum {min_length}"
        )
    return array


def _validate_horizons(horizons: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    horizons_tuple = tuple(int(horizon) for horizon in horizons)
    if not horizons_tuple:
        raise ValueError("horizons must be non-empty")
    if any(horizon <= 0 for horizon in horizons_tuple):
        raise ValueError(f"horizons must be positive integers; got {horizons_tuple}")
    return horizons_tuple


def random_walk_forecast(
    history: np.ndarray,
    horizons: list[int] | tuple[int, ...],
    n_samples: int = 1000,
    seed: int = 0,
) -> ProbabilisticForecast:
    """Driftless random walk forecast with Gaussian innovations.

    The point forecast at every horizon is the last observed level; the
    predictive variance grows linearly with horizon ``h`` at rate
    ``sigma²`` estimated from the sample variance of first differences.
    """
    history_arr = _validate_history(np.asarray(history), min_length=2)
    horizons_tuple = _validate_horizons(horizons)

    increments = np.diff(history_arr)
    sigma = float(np.std(increments, ddof=1)) if increments.size > 1 else 0.0
    last_value = float(history_arr[-1])
    rng = np.random.default_rng(seed)
    max_horizon = max(horizons_tuple)
    shocks = rng.standard_normal((n_samples, max_horizon)) * sigma
    cumulative_paths = last_value + np.cumsum(shocks, axis=1)
    samples = cumulative_paths[:, [horizon - 1 for horizon in horizons_tuple]]
    return ProbabilisticForecast(
        horizons=horizons_tuple,
        samples=samples,
        model_name="rw",
        metadata={"sigma_increment": sigma, "last_level": last_value},
    )


def ar1_forecast(
    history: np.ndarray,
    horizons: list[int] | tuple[int, ...],
    n_samples: int = 1000,
    seed: int = 0,
) -> ProbabilisticForecast:
    """AR(1) probabilistic forecast estimated by Yule-Walker / OLS.

    The model is ``y_t = c + phi * y_{t-1} + eps_t``. For an explosive
    estimate (``|phi| >= 0.999``) the model is degraded to a random walk
    — this protects the long-horizon variance against blow-up on series
    that are operationally unit-root.
    """
    history_arr = _validate_history(np.asarray(history), min_length=10)
    horizons_tuple = _validate_horizons(horizons)
    rng = np.random.default_rng(seed)

    y = history_arr
    lagged = y[:-1]
    target = y[1:]
    design = np.column_stack([np.ones_like(lagged), lagged])
    coefficients, *_ = np.linalg.lstsq(design, target, rcond=None)
    intercept = float(coefficients[0])
    phi = float(coefficients[1])
    residuals = target - design @ coefficients
    sigma = float(np.std(residuals, ddof=2)) if residuals.size > 2 else 0.0

    if abs(phi) >= 0.999:
        return random_walk_forecast(history_arr, horizons_tuple, n_samples=n_samples, seed=seed)

    max_horizon = max(horizons_tuple)
    paths = np.empty((n_samples, max_horizon), dtype=float)
    previous_level = np.full(n_samples, history_arr[-1], dtype=float)
    for step_index in range(max_horizon):
        shocks = rng.standard_normal(n_samples) * sigma
        previous_level = intercept + phi * previous_level + shocks
        paths[:, step_index] = previous_level

    samples = paths[:, [horizon - 1 for horizon in horizons_tuple]]
    return ProbabilisticForecast(
        horizons=horizons_tuple,
        samples=samples,
        model_name="ar1",
        metadata={"intercept": intercept, "phi": phi, "sigma_residual": sigma},
    )


def arma11_forecast(
    history: np.ndarray,
    horizons: list[int] | tuple[int, ...],
    n_samples: int = 1000,
    seed: int = 0,
) -> ProbabilisticForecast:
    """ARMA(1, 1) probabilistic forecast via ``statsmodels``.

    Falls back to :func:`ar1_forecast` if maximum-likelihood estimation
    fails to converge (e.g. on short or near-integrated series). This
    keeps the benchmark robust on the long-history panel where some
    variables have only a few dozen valid points after differencing.
    """
    import statsmodels.api as sm

    history_arr = _validate_history(np.asarray(history), min_length=20)
    horizons_tuple = _validate_horizons(horizons)
    rng = np.random.default_rng(seed)

    try:
        model = sm.tsa.SARIMAX(history_arr, order=(1, 0, 1), trend="c")
        fit = model.fit(disp=False, maxiter=200)
        if not np.all(np.isfinite(fit.params)):
            raise RuntimeError("non-finite parameters")
    except (ValueError, RuntimeError, np.linalg.LinAlgError):
        return ar1_forecast(history_arr, horizons_tuple, n_samples=n_samples, seed=seed)

    max_horizon = max(horizons_tuple)
    paths = np.empty((n_samples, max_horizon), dtype=float)
    for sample_index in range(n_samples):
        seed_for_path = int(rng.integers(0, np.iinfo(np.int32).max))
        simulated = fit.simulate(
            nsimulations=max_horizon,
            anchor="end",
            random_state=np.random.default_rng(seed_for_path),
        )
        paths[sample_index, :] = np.asarray(simulated, dtype=float).ravel()

    samples = paths[:, [horizon - 1 for horizon in horizons_tuple]]
    return ProbabilisticForecast(
        horizons=horizons_tuple,
        samples=samples,
        model_name="arma11",
        metadata={"converged": bool(fit.mle_retvals.get("converged", False))},
    )
