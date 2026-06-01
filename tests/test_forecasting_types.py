"""Tests for the ``ProbabilisticForecast`` dataclass invariants."""
from __future__ import annotations

import numpy as np
import pytest

from ecowave.forecasting.types import ProbabilisticForecast


def test_probabilistic_forecast_rejects_non_2d_samples() -> None:
    with pytest.raises(ValueError, match="2-D"):
        ProbabilisticForecast(horizons=(1,), samples=np.zeros(5), model_name="x")


def test_probabilistic_forecast_rejects_shape_mismatch() -> None:
    with pytest.raises(ValueError, match="!= len"):
        ProbabilisticForecast(
            horizons=(1, 3), samples=np.zeros((10, 3)), model_name="x"
        )


def test_probabilistic_forecast_rejects_non_positive_horizons() -> None:
    with pytest.raises(ValueError, match="positive"):
        ProbabilisticForecast(
            horizons=(0,), samples=np.zeros((10, 1)), model_name="x"
        )


def test_mean_and_quantile_consistency() -> None:
    rng = np.random.default_rng(seed=0)
    samples = rng.normal(loc=2.0, scale=0.5, size=(5_000, 3))
    forecast = ProbabilisticForecast(
        horizons=(1, 3, 12), samples=samples, model_name="test"
    )

    assert forecast.mean.shape == (3,)
    assert forecast.mean[0] == pytest.approx(2.0, abs=0.05)
    median = forecast.quantile(0.5)
    assert median.shape == (3,)
    assert median[1] == pytest.approx(2.0, abs=0.05)


def test_at_returns_single_horizon_slice() -> None:
    samples = np.tile(np.array([10.0, 20.0, 30.0]), (4, 1))
    forecast = ProbabilisticForecast(
        horizons=(1, 6, 24), samples=samples, model_name="test"
    )
    np.testing.assert_array_equal(forecast.at(6), np.full(4, 20.0))


def test_at_raises_on_unknown_horizon() -> None:
    samples = np.zeros((3, 1))
    forecast = ProbabilisticForecast(horizons=(1,), samples=samples, model_name="x")
    with pytest.raises(KeyError):
        forecast.at(99)
