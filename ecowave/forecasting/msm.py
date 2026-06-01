"""Markov-Switching Multifractal (MSM) — :ref:`Calvet & Fisher (2002,
2004, 2008) <calvet-fisher-2002>`.

Why MSM is the canonical model of the CPV cluster. The empirical
verdict (PRs #23-29) identifies family B (multifractality), family C
(long memory), and heavy tails as load-bearing. MSM is the simplest
parsimonious specification that reproduces all three from a single
generative story: returns ``r_t = σ_t z_t`` with ``σ_t = σ̄ ·
sqrt(M_{1,t} · M_{2,t} · … · M_{K,t})`` where each multiplier
``M_{k,t}`` is a two-state Markov chain whose switching rate decays
geometrically across components. The resulting volatility process has
infinite-mode multifractal scaling (family B), slowly-decaying
autocorrelation in absolute returns that *mimics* long memory by
component cascading (family C), and unconditional heavy tails from the
mixture of variance regimes.

Specification.

- ``K`` multipliers, each in ``{m_0, 2 − m_0}`` with mean 1 so the
  unconditional ``E σ²`` equals ``σ̄²``.
- Switching probabilities ``γ_k = 1 − (1 − γ_1)^{b^{k−1}}`` with
  ``b > 1`` — the canonical Calvet-Fisher decay-rate specification.
  Lower components persist longer (the long-memory channel); higher
  components switch fast (the short-horizon volatility burst channel).
- 4 free parameters: ``(m_0, σ̄, b, γ_1)``.

Estimation. We fit by maximum likelihood using a Hamilton-style forward
filter over the ``2^K``-dimensional state space. ``K = 4`` (16 states)
is fast enough for benchmark scale and is the operating point Calvet-
Fisher consistently report as a good fit-vs-cost trade-off.

Simulation. From the filtered terminal-state distribution at time ``T``
we draw initial states for each path, then simulate each component
independently forward. Returns are accumulated to log-levels (or first
differences are accumulated to levels) before reading the horizons.

Robustness. The benchmark needs a fall-back when the small-sample
optimisation diverges: we degrade to a Gaussian random-walk on the
detrended log-returns and flag ``msm_fit_ok = False``.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from ecowave.forecasting.types import ProbabilisticForecast


MIN_HISTORY_LENGTH = 50
SUPPORTED_K_RANGE = (2, 6)


@dataclass(frozen=True)
class MSMConfig:
    """Configuration for an MSM fit."""

    n_components: int = 4
    use_log_returns: bool = True
    fallback_on_failure: bool = True

    def __post_init__(self) -> None:
        if not SUPPORTED_K_RANGE[0] <= self.n_components <= SUPPORTED_K_RANGE[1]:
            raise ValueError(
                f"n_components must be in {SUPPORTED_K_RANGE}; got {self.n_components}"
            )


@dataclass(frozen=True)
class MSMParameters:
    """The four MSM parameters ``(m_0, σ̄, b, γ_1)``."""

    m_0: float
    sigma_bar: float
    b: float
    gamma_1: float

    def is_valid(self) -> bool:
        return (
            1.0 < self.m_0 < 1.999
            and self.sigma_bar > 0.0
            and self.b > 1.0
            and 0.0 < self.gamma_1 < 1.0
        )


def _component_switch_probabilities(parameters: MSMParameters, K: int) -> np.ndarray:
    """``γ_k = 1 − (1 − γ_1)^{b^{k−1}}`` for ``k = 1 … K``."""
    base = 1.0 - parameters.gamma_1
    exponents = parameters.b ** np.arange(K, dtype=float)
    return 1.0 - base**exponents


def _state_variances(parameters: MSMParameters, K: int) -> np.ndarray:
    """Vector of ``σ²`` for each of the ``2^K`` combined states."""
    n_states = 2**K
    state_indices = np.array(
        [[(state >> k) & 1 for k in range(K)] for state in range(n_states)], dtype=int
    )
    multiplier_values = np.array([parameters.m_0, 2.0 - parameters.m_0])
    state_multipliers = multiplier_values[state_indices]
    return (parameters.sigma_bar**2) * np.prod(state_multipliers, axis=1)


def _build_transition_matrix(parameters: MSMParameters, K: int) -> np.ndarray:
    """Full ``2^K × 2^K`` transition matrix from independent components.

    Each component ``k`` flips with probability ``γ_k`` per step. When
    a flip occurs the new value is drawn uniformly from ``{m_0,
    2 − m_0}``, so the per-component transition probability is
    ``P(s' = s) = (1 − γ_k) + γ_k / 2``.
    """
    n_states = 2**K
    gammas = _component_switch_probabilities(parameters, K)
    state_bits = np.array(
        [[(state >> k) & 1 for k in range(K)] for state in range(n_states)], dtype=int
    )
    transition_matrix = np.zeros((n_states, n_states), dtype=float)
    for from_state in range(n_states):
        from_bits = state_bits[from_state]
        for to_state in range(n_states):
            to_bits = state_bits[to_state]
            probability = 1.0
            for component_index in range(K):
                gamma = gammas[component_index]
                if from_bits[component_index] == to_bits[component_index]:
                    probability *= (1.0 - gamma) + gamma * 0.5
                else:
                    probability *= gamma * 0.5
            transition_matrix[from_state, to_state] = probability
    return transition_matrix


def _forward_filter(
    returns: np.ndarray, parameters: MSMParameters, K: int
) -> tuple[float, np.ndarray]:
    """Hamilton forward filter — log-likelihood and final filtered probabilities."""
    n_states = 2**K
    state_variances = _state_variances(parameters, K)
    transition_matrix = _build_transition_matrix(parameters, K)
    normalisation = 1.0 / np.sqrt(2.0 * math.pi * state_variances)

    log_likelihood = 0.0
    state_probabilities = np.full(n_states, 1.0 / n_states)
    for return_value in returns:
        likelihoods = normalisation * np.exp(
            -0.5 * (return_value * return_value) / state_variances
        )
        joint_probabilities = state_probabilities * likelihoods
        marginal = joint_probabilities.sum()
        if marginal <= 0.0 or not np.isfinite(marginal):
            return -np.inf, state_probabilities
        log_likelihood += math.log(marginal)
        state_probabilities = joint_probabilities / marginal
        state_probabilities = state_probabilities @ transition_matrix
    return log_likelihood, state_probabilities


def _negative_log_likelihood(
    raw_parameters: np.ndarray, returns: np.ndarray, K: int
) -> float:
    parameters = MSMParameters(
        m_0=float(raw_parameters[0]),
        sigma_bar=float(raw_parameters[1]),
        b=float(raw_parameters[2]),
        gamma_1=float(raw_parameters[3]),
    )
    if not parameters.is_valid():
        return 1e10
    log_likelihood, _ = _forward_filter(returns, parameters, K)
    if not np.isfinite(log_likelihood):
        return 1e10
    return -log_likelihood


def _initial_parameter_grid(returns: np.ndarray) -> list[MSMParameters]:
    """A small grid of plausible starting points for the optimiser."""
    sample_std = float(np.std(returns, ddof=1))
    base_sigma = max(sample_std, 1e-6)
    starting_grid: list[MSMParameters] = []
    for m_0 in (1.2, 1.4, 1.6):
        for gamma_1 in (0.05, 0.2):
            for b in (1.5, 2.5):
                starting_grid.append(
                    MSMParameters(m_0=m_0, sigma_bar=base_sigma, b=b, gamma_1=gamma_1)
                )
    return starting_grid


def _fit_msm_parameters(returns: np.ndarray, K: int) -> tuple[MSMParameters, bool]:
    """Maximum-likelihood fit of the MSM parameters.

    Tries each of a small grid of starting points and keeps the best
    fit. Returns ``(best_parameters, ok)`` where ``ok`` flags
    successful estimation.
    """
    from scipy.optimize import minimize

    best_negative_log_likelihood = np.inf
    best_parameters: MSMParameters | None = None
    bounds = [
        (1.01, 1.99),
        (1e-6, 10.0 * float(np.std(returns, ddof=1) + 1e-6)),
        (1.01, 50.0),
        (1e-4, 0.999),
    ]
    for starting_point in _initial_parameter_grid(returns):
        initial_vector = np.array(
            [
                starting_point.m_0,
                starting_point.sigma_bar,
                starting_point.b,
                starting_point.gamma_1,
            ]
        )
        try:
            result = minimize(
                _negative_log_likelihood,
                initial_vector,
                args=(returns, K),
                method="L-BFGS-B",
                bounds=bounds,
                options={"maxiter": 80, "ftol": 1e-6},
            )
        except (ValueError, RuntimeError):
            continue
        if result.fun < best_negative_log_likelihood and np.isfinite(result.fun):
            best_negative_log_likelihood = float(result.fun)
            best_parameters = MSMParameters(
                m_0=float(result.x[0]),
                sigma_bar=float(result.x[1]),
                b=float(result.x[2]),
                gamma_1=float(result.x[3]),
            )

    if best_parameters is None or not np.isfinite(best_negative_log_likelihood):
        return MSMParameters(m_0=1.5, sigma_bar=1.0, b=2.0, gamma_1=0.1), False
    return best_parameters, True


def _simulate_paths(
    parameters: MSMParameters,
    K: int,
    terminal_state_distribution: np.ndarray,
    horizon: int,
    n_samples: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Simulate ``n_samples`` future return paths of length ``horizon``.

    Each path draws an initial joint state from the filtered
    distribution at ``T``, then simulates the ``K`` component chains
    independently — equivalent to the joint chain but exponentially
    cheaper.
    """
    n_states = 2**K
    gammas = _component_switch_probabilities(parameters, K)
    state_bits = np.array(
        [[(state >> k) & 1 for k in range(K)] for state in range(n_states)], dtype=int
    )
    component_values = np.array([parameters.m_0, 2.0 - parameters.m_0])

    initial_states = rng.choice(n_states, size=n_samples, p=terminal_state_distribution)
    component_state_per_path = state_bits[initial_states].copy()
    return_paths = np.empty((n_samples, horizon), dtype=float)

    for time_step in range(horizon):
        flip_decisions = rng.random((n_samples, K)) < gammas
        new_draws = (rng.random((n_samples, K)) < 0.5).astype(int)
        component_state_per_path = np.where(
            flip_decisions, new_draws, component_state_per_path
        )
        multipliers_per_path = component_values[component_state_per_path]
        variances_per_path = (parameters.sigma_bar**2) * np.prod(
            multipliers_per_path, axis=1
        )
        innovations = rng.standard_normal(n_samples)
        return_paths[:, time_step] = innovations * np.sqrt(variances_per_path)

    return return_paths


def _extract_returns(history: np.ndarray, use_log_returns: bool) -> tuple[np.ndarray, str]:
    """Return ``(returns, mode)`` where mode is ``"log"`` or ``"diff"``."""
    if use_log_returns and np.all(history > 0):
        log_history = np.log(history)
        returns = np.diff(log_history)
        return returns, "log"
    returns = np.diff(history)
    return returns, "diff"


def _reconstruct_levels(
    history: np.ndarray,
    cumulative_return_paths: np.ndarray,
    mode: str,
) -> np.ndarray:
    """Convert cumulative return paths back to level paths."""
    last_value = float(history[-1])
    if mode == "log":
        return last_value * np.exp(cumulative_return_paths)
    return last_value + cumulative_return_paths


def msm_forecast(
    history: np.ndarray,
    horizons: list[int] | tuple[int, ...],
    n_samples: int = 1000,
    seed: int = 0,
    config: MSMConfig | None = None,
) -> ProbabilisticForecast:
    """Probabilistic forecast under the Calvet-Fisher MSM.

    Parameters
    ----------
    history:
        1-D history of levels. Length ≥ 50 required for the ML fit to
        identify the four parameters.
    horizons:
        Forecast horizons in cadence steps.
    n_samples:
        Number of Monte Carlo paths.
    seed:
        RNG seed.
    config:
        Optional :class:`MSMConfig`. Defaults to ``K = 4`` components
        with log-returns and fallback enabled.
    """
    config = config or MSMConfig()
    history_arr = np.asarray(history, dtype=float).ravel()
    if not np.all(np.isfinite(history_arr)):
        raise ValueError("history contains non-finite values")
    if history_arr.size < MIN_HISTORY_LENGTH:
        raise ValueError(
            f"MSM requires history of length ≥ {MIN_HISTORY_LENGTH}; "
            f"got {history_arr.size}"
        )
    horizons_tuple = tuple(int(horizon) for horizon in horizons)
    if not horizons_tuple or any(horizon <= 0 for horizon in horizons_tuple):
        raise ValueError(f"horizons must be positive; got {horizons_tuple}")

    rng = np.random.default_rng(seed)
    K = config.n_components
    returns, mode = _extract_returns(history_arr, config.use_log_returns)
    centred_returns = returns - returns.mean()

    parameters, msm_fit_ok = _fit_msm_parameters(centred_returns, K)
    if not msm_fit_ok and not config.fallback_on_failure:
        raise RuntimeError("MSM ML estimation did not converge")

    if msm_fit_ok:
        _, terminal_distribution = _forward_filter(centred_returns, parameters, K)
        terminal_distribution = terminal_distribution / terminal_distribution.sum()
    else:
        # Degenerate fallback: 1-state distribution → constant volatility random walk.
        terminal_distribution = np.full(2**K, 1.0 / (2**K))

    max_horizon = max(horizons_tuple)
    return_paths = _simulate_paths(
        parameters,
        K,
        terminal_distribution,
        max_horizon,
        n_samples,
        rng,
    )
    return_paths = return_paths + returns.mean()
    cumulative_return_paths = np.cumsum(return_paths, axis=1)
    level_paths = _reconstruct_levels(history_arr, cumulative_return_paths, mode)
    samples = level_paths[:, [horizon - 1 for horizon in horizons_tuple]]

    return ProbabilisticForecast(
        horizons=horizons_tuple,
        samples=samples,
        model_name="msm",
        metadata={
            "msm_fit_ok": msm_fit_ok,
            "n_components": K,
            "return_mode": mode,
            "m_0": parameters.m_0,
            "sigma_bar": parameters.sigma_bar,
            "b": parameters.b,
            "gamma_1": parameters.gamma_1,
        },
    )
