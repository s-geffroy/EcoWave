"""Tests for ``ecowave.forecasting.har``.

The HAR design matrix is the load-bearing piece — get the lag alignment
wrong and the model degenerates into a noisy random walk. These tests
pin (i) the lag construction, (ii) the recovery of a known cascade of
heterogeneous coefficients on synthetic data, and (iii) the basic shape
contract of the probabilistic forecast.
"""
from __future__ import annotations

import numpy as np
import pytest

from ecowave.forecasting.har import HARLagConfig, _aggregate_lag, har_forecast


def test_aggregate_lag_rolling_mean_matches_naive_implementation() -> None:
    series = np.arange(10, dtype=float)
    actual = _aggregate_lag(series, window=3)
    expected_prefix_nans = np.isnan(actual[:2])
    assert expected_prefix_nans.all()
    assert actual[2] == pytest.approx(1.0)  # mean(0, 1, 2)
    assert actual[3] == pytest.approx(2.0)  # mean(1, 2, 3)
    assert actual[9] == pytest.approx(8.0)  # mean(7, 8, 9)


def test_har_lag_config_rejects_invalid_ordering() -> None:
    with pytest.raises(ValueError, match="short < medium < long"):
        HARLagConfig(short=2, medium=2, long=5)
    with pytest.raises(ValueError, match="short < medium < long"):
        HARLagConfig(short=5, medium=3, long=10)


def test_har_recovers_dominant_short_coefficient_on_short_cascade() -> None:
    rng = np.random.default_rng(seed=21)
    length = 600
    series = np.empty(length, dtype=float)
    series[:12] = 0.0
    for index in range(12, length):
        short_mean = series[index - 1]
        medium_mean = series[index - 3 : index].mean()
        long_mean = series[index - 12 : index].mean()
        series[index] = (
            0.05
            + 0.8 * short_mean
            + 0.1 * medium_mean
            + 0.05 * long_mean
            + rng.normal(scale=0.5)
        )
    forecast = har_forecast(series, horizons=(1, 3, 12), n_samples=200, seed=22)

    assert forecast.metadata["beta_short"] == pytest.approx(0.8, abs=0.1)
    assert forecast.metadata["beta_medium"] == pytest.approx(0.1, abs=0.1)
    assert forecast.metadata["beta_long"] == pytest.approx(0.05, abs=0.1)


def test_har_forecast_samples_have_expected_shape_and_are_finite() -> None:
    rng = np.random.default_rng(seed=23)
    history = np.cumsum(rng.normal(size=300)) + 5.0
    horizons = (1, 3, 6, 12, 24)
    forecast = har_forecast(history, horizons=horizons, n_samples=150, seed=24)

    assert forecast.samples.shape == (150, len(horizons))
    assert np.all(np.isfinite(forecast.samples))
    assert forecast.model_name == "har"


def test_har_rejects_history_shorter_than_long_lag_plus_buffer() -> None:
    short_history = np.arange(10, dtype=float)
    with pytest.raises(ValueError, match="HAR requires history"):
        har_forecast(short_history, horizons=(1,), n_samples=10)
