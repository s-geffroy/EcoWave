"""ARFIMA(0, d, 0) with a Markov regime-switching mean — Roadmap #20.

Why this model. The CPV cluster identifies *both* family C (long memory)
and family S (reflexive regime drift). ARFIMA captures C by an explicit
fractional integration parameter ``d`` ; bolting a Markov-switching
regression on top of the fractionally-differenced series captures S as
a latent regime that shifts the mean (and optionally the variance) of
the short-memory innovations. The pair ``(d, regime structure)`` is the
minimal generative story consistent with both pillars of the cluster.
This is the framing of :ref:`Bhardwaj & Swanson (2006)
<bhardwaj-swanson-2006>` who tested 21 macro series.

Pipeline.

1. Estimate ``d`` by GPH log-periodogram regression
   (:func:`.fractional.gph_estimate_d`). Clipped to the stationarity
   range.
2. Compute the fractionally-differenced series
   ``Y_t = (1 − L)^d X_t`` via the truncated Hosking expansion.
3. Fit a two-regime ``MarkovRegression`` (statsmodels) on ``Y`` with
   switching constant and switching variance. The regime is a binary
   latent state with smoothed transition matrix ``P``.
4. For each Monte Carlo path:
    - Draw an initial regime from the filtered probability at ``T``.
    - Roll a Markov chain forward to horizon ``h``.
    - Simulate ``Y_{T+1}, …, Y_{T+h}`` as regime-conditional Gaussian
      draws ``μ(s_t) + σ(s_t) · z_t``.
    - Reconstruct the level by the recursive inversion
      ``X_t = Y_t − Σ_{k=1}^{L} ψ_k X_{t−k}`` where ``ψ_k`` are the
      Hosking coefficients of ``(1 − L)^d``. The recursion uses the
      observed history of ``X`` before ``T`` and the simulated values
      after.
5. Read the levels at the requested horizons.

Fallback. If ``MarkovRegression`` fails to converge — common on short
or near-stationary series — the model degrades to a single-regime
ARFIMA(0, d, 0) and emits a metadata flag ``regime_fit_ok=False``. The
downstream benchmark (PR D) will record this.
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np

from ecowave.forecasting.fractional import (
    fractional_difference,
    gph_estimate_d,
    hosking_coefficients,
)
from ecowave.forecasting.types import ProbabilisticForecast


@dataclass(frozen=True)
class ARFIMARSConfig:
    """Knobs for ARFIMA + regime-switching estimation."""

    n_regimes: int = 2
    bandwidth_exponent: float = 0.5
    hosking_truncate: int | None = None  # None = full history
    switching_variance: bool = True

    def __post_init__(self) -> None:
        if self.n_regimes < 1:
            raise ValueError(f"n_regimes must be ≥ 1; got {self.n_regimes}")
        if not 0.1 < self.bandwidth_exponent < 1.0:
            raise ValueError(
                f"bandwidth_exponent must be in (0.1, 1.0); got {self.bandwidth_exponent}"
            )


def _fit_markov_switching(
    differenced: np.ndarray, config: ARFIMARSConfig
) -> tuple[object, bool]:
    """Fit a Markov-switching regression on the fractionally-differenced series.

    Returns ``(fitted_results, ok)`` where ``ok`` flags successful
    convergence. On failure (non-convergence, ill-conditioning), returns
    a degenerate single-regime fit and ``ok = False``.
    """
    if config.n_regimes == 1:
        mean = float(differenced.mean())
        sigma = float(differenced.std(ddof=1)) if differenced.size > 1 else 1.0
        return ({"means": [mean], "sigmas": [sigma]}, True)

    import statsmodels.api as sm

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = sm.tsa.MarkovRegression(
                endog=differenced,
                k_regimes=config.n_regimes,
                trend="c",
                switching_variance=config.switching_variance,
            )
            fit = model.fit(disp=False, maxiter=200)
        if not np.all(np.isfinite(fit.params)):
            raise RuntimeError("non-finite MS parameters")
        return (fit, True)
    except (ValueError, RuntimeError, np.linalg.LinAlgError):
        mean = float(differenced.mean())
        sigma = float(differenced.std(ddof=1)) if differenced.size > 1 else 1.0
        return ({"means": [mean], "sigmas": [sigma]}, False)


def _extract_regime_parameters(
    fit: object, n_regimes: int, switching_variance: bool
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Pull regime means, sigmas, transition matrix, filtered probabilities.

    Handles both the statsmodels fit object and the dict-shaped
    fallback returned when convergence fails.
    """
    if isinstance(fit, dict):
        means = np.asarray(fit["means"], dtype=float)
        sigmas = np.asarray(fit["sigmas"], dtype=float)
        transitions = np.ones((1, 1), dtype=float)
        initial_probabilities = np.ones(1, dtype=float)
        return means, sigmas, transitions, initial_probabilities

    # ``fit.params`` is a positional numpy array; map by name through
    # ``fit.model.param_names`` to be robust to statsmodels' parameter
    # ordering. The transition probabilities come first, followed by
    # the regression constants and then the variances.
    param_names = list(fit.model.param_names)
    param_index = {name: idx for idx, name in enumerate(param_names)}
    params_array = np.asarray(fit.params, dtype=float)

    means = np.array(
        [
            float(params_array[param_index[f"const[{regime}]"]])
            for regime in range(n_regimes)
        ],
        dtype=float,
    )
    if switching_variance:
        sigmas = np.sqrt(
            np.array(
                [
                    float(params_array[param_index[f"sigma2[{regime}]"]])
                    for regime in range(n_regimes)
                ],
                dtype=float,
            )
        )
    else:
        single_variance = float(params_array[param_index["sigma2"]])
        sigmas = np.full(n_regimes, np.sqrt(single_variance), dtype=float)

    # statsmodels parameterises transitions as ``p[source->dest]`` for
    # ``dest = 0, …, k_regimes − 2`` — the last column of each row is
    # implied by the unit simplex constraint.
    transitions = np.empty((n_regimes, n_regimes), dtype=float)
    for source_regime in range(n_regimes):
        row_sum_so_far = 0.0
        for destination_regime in range(n_regimes - 1):
            key = f"p[{source_regime}->{destination_regime}]"
            probability = float(params_array[param_index[key]])
            transitions[source_regime, destination_regime] = probability
            row_sum_so_far += probability
        transitions[source_regime, n_regimes - 1] = 1.0 - row_sum_so_far
    transitions = np.clip(transitions, 0.0, 1.0)
    transitions = transitions / transitions.sum(axis=1, keepdims=True)

    filtered = np.asarray(fit.filtered_marginal_probabilities, dtype=float)
    if filtered.ndim == 1:
        filtered = filtered[:, np.newaxis]
    initial_probabilities = filtered[-1]
    initial_probabilities = initial_probabilities / initial_probabilities.sum()
    return means, sigmas, transitions, initial_probabilities


def _simulate_markov_paths(
    transitions: np.ndarray,
    initial_probabilities: np.ndarray,
    horizon: int,
    n_samples: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Roll Markov chains forward and return regime indices.

    Output shape ``(n_samples, horizon)`` of integer regime indices.
    """
    n_regimes = transitions.shape[0]
    paths = np.empty((n_samples, horizon), dtype=np.int64)
    current_regimes = rng.choice(n_regimes, size=n_samples, p=initial_probabilities)
    for time_step in range(horizon):
        next_regimes = np.empty(n_samples, dtype=np.int64)
        for regime_index in range(n_regimes):
            mask = current_regimes == regime_index
            count = int(mask.sum())
            if count == 0:
                continue
            next_regimes[mask] = rng.choice(
                n_regimes, size=count, p=transitions[regime_index]
            )
        paths[:, time_step] = next_regimes
        current_regimes = next_regimes
    return paths


def _reconstruct_levels(
    history: np.ndarray,
    differenced_history: np.ndarray,
    simulated_differenced_paths: np.ndarray,
    d: float,
    truncate: int | None,
) -> np.ndarray:
    """Reconstruct ``X`` levels from simulated ``Y`` increments.

    Uses the recursion ``X_t = Y_t − Σ_{k=1}^{L} ψ_k X_{t−k}`` where
    ``ψ_k`` are the Hosking coefficients of ``(1 − L)^d``. The recursion
    is seeded by the observed history of ``X``.
    """
    n_history = history.size
    n_samples, max_horizon = simulated_differenced_paths.shape
    effective_truncate = (
        n_history + max_horizon if truncate is None else min(int(truncate), n_history + max_horizon)
    )
    coefficients = hosking_coefficients(d, effective_truncate)
    # Build per-sample level arrays — small overhead but readable.
    levels = np.empty((n_samples, max_horizon), dtype=float)
    for sample_index in range(n_samples):
        # Concatenate observed history + buffer for the horizon.
        extended_levels = np.empty(n_history + max_horizon, dtype=float)
        extended_levels[:n_history] = history
        for time_offset in range(max_horizon):
            current_index = n_history + time_offset
            lag_count = min(current_index, effective_truncate - 1)
            past_levels_reversed = extended_levels[
                current_index - 1 :: -1
            ][:lag_count]
            lag_contribution = float(
                np.dot(coefficients[1 : lag_count + 1], past_levels_reversed)
            )
            extended_levels[current_index] = (
                float(simulated_differenced_paths[sample_index, time_offset])
                - lag_contribution
            )
        levels[sample_index, :] = extended_levels[n_history:]
    return levels


def arfima_rs_forecast(
    history: np.ndarray,
    horizons: list[int] | tuple[int, ...],
    n_samples: int = 1000,
    seed: int = 0,
    config: ARFIMARSConfig | None = None,
) -> ProbabilisticForecast:
    """ARFIMA(0, d, 0) with Markov regime-switching mean and variance.

    Parameters
    ----------
    history:
        1-D history of levels. Length ≥ 32 recommended for GPH
        bandwidth ``≥ 4``.
    horizons:
        Forecast horizons in cadence steps.
    n_samples:
        Number of Monte Carlo paths.
    seed:
        RNG seed.
    config:
        Optional :class:`ARFIMARSConfig`. Defaults: two regimes with
        switching variance, GPH bandwidth exponent ``0.5``.
    """
    config = config or ARFIMARSConfig()
    history_arr = np.asarray(history, dtype=float).ravel()
    if not np.all(np.isfinite(history_arr)):
        raise ValueError("history contains non-finite values")
    if history_arr.size < 32:
        raise ValueError(
            f"ARFIMA+RS requires history of length ≥ 32; got {history_arr.size}"
        )
    horizons_tuple = tuple(int(horizon) for horizon in horizons)
    if not horizons_tuple or any(horizon <= 0 for horizon in horizons_tuple):
        raise ValueError(f"horizons must be positive; got {horizons_tuple}")

    rng = np.random.default_rng(seed)
    estimated_d = gph_estimate_d(history_arr, bandwidth_exponent=config.bandwidth_exponent)
    differenced_history = fractional_difference(
        history_arr, estimated_d, truncate=config.hosking_truncate
    )

    fit, regime_fit_ok = _fit_markov_switching(differenced_history, config)
    n_regimes_used = config.n_regimes if regime_fit_ok else 1
    means, sigmas, transitions, initial_probabilities = _extract_regime_parameters(
        fit, n_regimes_used, config.switching_variance
    )

    max_horizon = max(horizons_tuple)
    regime_paths = _simulate_markov_paths(
        transitions, initial_probabilities, max_horizon, n_samples, rng
    )
    innovations = rng.standard_normal(size=(n_samples, max_horizon))
    simulated_differenced_paths = (
        means[regime_paths] + sigmas[regime_paths] * innovations
    )

    level_paths = _reconstruct_levels(
        history_arr,
        differenced_history,
        simulated_differenced_paths,
        estimated_d,
        config.hosking_truncate,
    )
    samples = level_paths[:, [horizon - 1 for horizon in horizons_tuple]]

    return ProbabilisticForecast(
        horizons=horizons_tuple,
        samples=samples,
        model_name="arfima_rs",
        metadata={
            "d_estimated": estimated_d,
            "regime_fit_ok": regime_fit_ok,
            "n_regimes_used": int(n_regimes_used),
            "regime_means": means.tolist(),
            "regime_sigmas": sigmas.tolist(),
            "transition_matrix": transitions.tolist(),
            "bandwidth_exponent": config.bandwidth_exponent,
        },
    )
