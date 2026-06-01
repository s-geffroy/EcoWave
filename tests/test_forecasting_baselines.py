"""Tests for ``ecowave.forecasting.baselines``.

Cover the recovery of generative parameters on synthetic series and the
calibration of the predictive variance against horizon ``h``.
"""
from __future__ import annotations

import numpy as np
import pytest

from ecowave.forecasting.baselines import (
    ar1_forecast,
    arma11_forecast,
    random_walk_forecast,
)


def test_random_walk_point_forecast_is_last_observed_level() -> None:
    rng = np.random.default_rng(seed=0)
    history = np.cumsum(rng.normal(size=200)) + 5.0
    forecast = random_walk_forecast(history, horizons=(1, 3, 12), n_samples=2_000, seed=1)

    assert forecast.mean[0] == pytest.approx(history[-1], abs=0.2)
    assert forecast.mean[1] == pytest.approx(history[-1], abs=0.4)
    assert forecast.mean[2] == pytest.approx(history[-1], abs=0.8)


def test_random_walk_predictive_variance_grows_linearly_with_horizon() -> None:
    rng = np.random.default_rng(seed=2)
    history = np.cumsum(rng.normal(scale=1.0, size=500)) + 10.0
    forecast = random_walk_forecast(history, horizons=(1, 4, 16), n_samples=5_000, seed=3)

    variances = forecast.samples.var(axis=0)
    ratio_4_to_1 = variances[1] / variances[0]
    ratio_16_to_1 = variances[2] / variances[0]
    assert ratio_4_to_1 == pytest.approx(4.0, rel=0.15)
    assert ratio_16_to_1 == pytest.approx(16.0, rel=0.15)


def test_ar1_recovers_known_persistence() -> None:
    rng = np.random.default_rng(seed=4)
    true_phi = 0.7
    length = 1_000
    sample_series = np.empty(length, dtype=float)
    sample_series[0] = 0.0
    for index in range(1, length):
        sample_series[index] = true_phi * sample_series[index - 1] + rng.normal()
    forecast = ar1_forecast(sample_series, horizons=(1,), n_samples=10, seed=5)

    assert forecast.metadata["phi"] == pytest.approx(true_phi, abs=0.05)


def test_ar1_falls_back_to_random_walk_when_explosive() -> None:
    rng = np.random.default_rng(seed=6)
    unit_root_history = np.cumsum(rng.normal(size=200))
    forecast = ar1_forecast(unit_root_history, horizons=(1, 3), n_samples=500, seed=7)
    assert forecast.model_name in {"ar1", "rw"}
    if forecast.model_name == "ar1":
        assert abs(forecast.metadata["phi"]) < 0.999


def test_arma11_forecast_returns_well_shaped_samples() -> None:
    rng = np.random.default_rng(seed=8)
    history = np.cumsum(rng.normal(size=400)) + 1.0
    horizons = (1, 3, 6, 12)
    forecast = arma11_forecast(history, horizons=horizons, n_samples=200, seed=9)

    assert forecast.samples.shape == (200, len(horizons))
    assert np.all(np.isfinite(forecast.samples))


def test_random_walk_rejects_non_finite_history() -> None:
    with pytest.raises(ValueError, match="non-finite"):
        random_walk_forecast(np.array([1.0, np.nan]), horizons=(1,), n_samples=10)


def test_random_walk_rejects_non_positive_horizons() -> None:
    with pytest.raises(ValueError, match="positive"):
        random_walk_forecast(np.array([1.0, 2.0, 3.0]), horizons=(0,), n_samples=10)
