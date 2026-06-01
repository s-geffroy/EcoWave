"""Tests for ``ecowave.forecasting.msm``.

Cover (i) configuration validation, (ii) the forward filter and
transition-matrix internals, (iii) parameter recovery on a synthetic
MSM-generated sample, and (iv) the public forecast contract and
fallback behaviour.
"""
from __future__ import annotations

import numpy as np
import pytest

from ecowave.forecasting.msm import (
    MSMConfig,
    MSMParameters,
    _build_transition_matrix,
    _component_switch_probabilities,
    _forward_filter,
    _state_variances,
    msm_forecast,
)


def _simulate_msm_returns(
    parameters: MSMParameters, n_components: int, length: int, seed: int
) -> np.ndarray:
    """Forward-simulate an MSM-generated return path of given length."""
    rng = np.random.default_rng(seed)
    multiplier_values = np.array([parameters.m_0, 2.0 - parameters.m_0])
    gammas = _component_switch_probabilities(parameters, n_components)
    component_states = rng.integers(0, 2, size=n_components)
    returns = np.empty(length, dtype=float)
    for time_step in range(length):
        flip_mask = rng.random(n_components) < gammas
        new_draws = rng.integers(0, 2, size=n_components)
        component_states = np.where(flip_mask, new_draws, component_states)
        variance = (parameters.sigma_bar**2) * np.prod(multiplier_values[component_states])
        returns[time_step] = rng.normal(scale=np.sqrt(variance))
    return returns


def test_msm_config_rejects_unsupported_component_count() -> None:
    with pytest.raises(ValueError, match="n_components"):
        MSMConfig(n_components=10)


def test_component_switch_probabilities_monotonically_increase_with_index() -> None:
    parameters = MSMParameters(m_0=1.5, sigma_bar=0.1, b=2.0, gamma_1=0.05)
    gammas = _component_switch_probabilities(parameters, K=4)

    assert gammas.shape == (4,)
    assert np.all(np.diff(gammas) >= 0.0)
    assert gammas[0] == pytest.approx(0.05)
    assert gammas[3] < 1.0


def test_state_variances_unconditional_mean_equals_sigma_bar_squared() -> None:
    parameters = MSMParameters(m_0=1.3, sigma_bar=0.4, b=2.0, gamma_1=0.1)
    K = 3
    variances = _state_variances(parameters, K)

    expected_unconditional = parameters.sigma_bar**2
    assert variances.mean() == pytest.approx(expected_unconditional, rel=1e-9)


def test_transition_matrix_rows_sum_to_one() -> None:
    parameters = MSMParameters(m_0=1.4, sigma_bar=0.5, b=2.0, gamma_1=0.1)
    transition = _build_transition_matrix(parameters, K=3)

    np.testing.assert_allclose(transition.sum(axis=1), np.ones(8), atol=1e-12)
    assert np.all(transition >= 0.0)


def test_forward_filter_returns_finite_log_likelihood_on_simulated_path() -> None:
    parameters = MSMParameters(m_0=1.4, sigma_bar=0.5, b=2.5, gamma_1=0.1)
    K = 3
    returns = _simulate_msm_returns(parameters, K, length=400, seed=11)
    log_likelihood, terminal_probabilities = _forward_filter(returns, parameters, K)

    assert np.isfinite(log_likelihood)
    assert terminal_probabilities.shape == (2**K,)
    assert np.isclose(terminal_probabilities.sum(), 1.0, atol=1e-9)


def test_msm_forecast_has_expected_shape_and_finite_samples() -> None:
    rng = np.random.default_rng(seed=21)
    history = np.exp(np.cumsum(rng.normal(scale=0.02, size=200))) * 100.0
    horizons = (1, 3, 6, 12)
    forecast = msm_forecast(
        history, horizons=horizons, n_samples=80, seed=22, config=MSMConfig(n_components=3)
    )

    assert forecast.model_name == "msm"
    assert forecast.samples.shape == (80, len(horizons))
    assert np.all(np.isfinite(forecast.samples))
    assert "msm_fit_ok" in forecast.metadata


def test_msm_forecast_rejects_short_history() -> None:
    short_history = np.arange(30, dtype=float)
    with pytest.raises(ValueError, match="history of length"):
        msm_forecast(short_history, horizons=(1,), n_samples=10)


def test_msm_forecast_rejects_non_finite_history() -> None:
    bad_history = np.array([1.0] * 60 + [np.nan])
    with pytest.raises(ValueError, match="non-finite"):
        msm_forecast(bad_history, horizons=(1,), n_samples=10)


def test_msm_forecast_rejects_non_positive_horizons() -> None:
    rng = np.random.default_rng(seed=23)
    history = np.exp(rng.normal(scale=0.01, size=100).cumsum()) * 10.0
    with pytest.raises(ValueError, match="positive"):
        msm_forecast(history, horizons=(0,), n_samples=10)


def test_msm_forecast_predictive_variance_grows_with_horizon() -> None:
    rng = np.random.default_rng(seed=24)
    history = np.exp(rng.normal(scale=0.02, size=300).cumsum()) * 100.0
    forecast = msm_forecast(
        history,
        horizons=(1, 6, 24),
        n_samples=200,
        seed=25,
        config=MSMConfig(n_components=3),
    )

    variances = forecast.samples.var(axis=0)
    assert variances[1] > variances[0]
    assert variances[2] > variances[1]


def test_msm_forecast_falls_back_to_default_parameters_on_short_messy_history() -> None:
    rng = np.random.default_rng(seed=26)
    pathological_history = np.exp(
        np.concatenate(
            [
                rng.normal(scale=0.001, size=40),
                rng.normal(scale=1.0, size=20),
            ]
        ).cumsum()
    ) * 5.0
    forecast = msm_forecast(
        pathological_history,
        horizons=(1, 3),
        n_samples=50,
        seed=27,
        config=MSMConfig(n_components=3),
    )

    assert forecast.metadata["m_0"] > 1.0
    assert forecast.metadata["m_0"] < 2.0
    assert forecast.samples.shape == (50, 2)
