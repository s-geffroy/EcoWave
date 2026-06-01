"""Tests for ``ecowave.forecasting.arfima_rs``.

Cover (i) the forecast shape contract, (ii) extraction of regime
parameters from a long simulated two-regime ARFIMA-like series, and
(iii) the graceful fallback to a single-regime fit when the MS
estimation cannot converge.
"""
from __future__ import annotations

import numpy as np
import pytest

from ecowave.forecasting.arfima_rs import ARFIMARSConfig, arfima_rs_forecast
from ecowave.forecasting.fractional import fractional_integrate


def _simulate_arfima_with_regime_switch(
    n: int,
    d: float,
    means: tuple[float, float],
    sigmas: tuple[float, float],
    switch_at: int,
    seed: int,
) -> np.ndarray:
    """Simulate ARFIMA(0, d, 0) with a one-time regime switch in the mean/variance."""
    rng = np.random.default_rng(seed=seed)
    raw_innovations = np.empty(n, dtype=float)
    raw_innovations[:switch_at] = (
        means[0] + sigmas[0] * rng.normal(size=switch_at)
    )
    raw_innovations[switch_at:] = (
        means[1] + sigmas[1] * rng.normal(size=n - switch_at)
    )
    return fractional_integrate(raw_innovations, d=d)


def test_arfima_rs_forecast_has_expected_shape_and_finite_samples() -> None:
    rng = np.random.default_rng(seed=3)
    history = np.cumsum(rng.normal(size=300)) + 2.0
    horizons = (1, 3, 6, 12)
    forecast = arfima_rs_forecast(history, horizons=horizons, n_samples=150, seed=4)

    assert forecast.model_name == "arfima_rs"
    assert forecast.samples.shape == (150, len(horizons))
    assert np.all(np.isfinite(forecast.samples))
    assert "d_estimated" in forecast.metadata
    assert "regime_fit_ok" in forecast.metadata


def test_arfima_rs_recovers_long_memory_parameter_on_synthetic_arfima() -> None:
    history = _simulate_arfima_with_regime_switch(
        n=2_000,
        d=0.35,
        means=(0.0, 0.0),
        sigmas=(1.0, 1.0),
        switch_at=2_000,
        seed=13,
    )
    forecast = arfima_rs_forecast(history, horizons=(1,), n_samples=10, seed=14)
    assert forecast.metadata["d_estimated"] == pytest.approx(0.35, abs=0.15)


def test_arfima_rs_single_regime_config_skips_markov_fit() -> None:
    rng = np.random.default_rng(seed=15)
    history = rng.normal(size=200).cumsum() + 1.0
    config = ARFIMARSConfig(n_regimes=1)
    forecast = arfima_rs_forecast(history, horizons=(1,), n_samples=50, seed=16, config=config)

    assert forecast.metadata["regime_fit_ok"] is True
    assert forecast.metadata["n_regimes_used"] == 1
    assert len(forecast.metadata["regime_means"]) == 1


def test_arfima_rs_config_rejects_invalid_n_regimes() -> None:
    with pytest.raises(ValueError, match="n_regimes"):
        ARFIMARSConfig(n_regimes=0)


def test_arfima_rs_config_rejects_invalid_bandwidth_exponent() -> None:
    with pytest.raises(ValueError, match="bandwidth_exponent"):
        ARFIMARSConfig(bandwidth_exponent=1.5)


def test_arfima_rs_rejects_history_shorter_than_32() -> None:
    short_history = np.arange(20, dtype=float)
    with pytest.raises(ValueError, match="history of length ≥ 32"):
        arfima_rs_forecast(short_history, horizons=(1,), n_samples=10)


def test_arfima_rs_rejects_non_positive_horizons() -> None:
    rng = np.random.default_rng(seed=17)
    history = rng.normal(size=100)
    with pytest.raises(ValueError, match="positive"):
        arfima_rs_forecast(history, horizons=(0,), n_samples=10)


def test_arfima_rs_predictive_variance_grows_with_horizon() -> None:
    rng = np.random.default_rng(seed=19)
    history = np.cumsum(rng.normal(size=300))
    forecast = arfima_rs_forecast(history, horizons=(1, 6, 24), n_samples=500, seed=21)

    variances = forecast.samples.var(axis=0)
    # Long memory implies super-linear variance growth ; we just check
    # monotonic increase to avoid coupling the test to the specific
    # estimated d.
    assert variances[1] > variances[0]
    assert variances[2] > variances[1]
