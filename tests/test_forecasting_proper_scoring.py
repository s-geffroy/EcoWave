"""Tests for ``ecowave.forecasting.proper_scoring``.

Covers:

- Empirical CRPS matches the Gaussian closed-form ``sigma * (1/sqrt(pi)
  - 2 * phi(z) - z * (2 * Phi(z) - 1))`` at the predictive mean (Gneiting-
  Raftery 2007 eq. 5) to within Monte-Carlo tolerance.
- CRPS at a point mass reduces to MAE.
- Coverage indicator agrees with direct quantile check.
- Tail coverage flips polarity (left/right) correctly.
- Mincer-Zarnowitz recovers (alpha, beta) ≈ (0, 1) on an unbiased
  forecast and rejects on a biased one.
"""
from __future__ import annotations

import math

import numpy as np
import pytest

from ecowave.forecasting.proper_scoring import (
    coverage_indicator,
    empirical_crps,
    mincer_zarnowitz,
    score_forecast,
    tail_coverage_indicator,
)


def _gaussian_crps_closed_form(mean: float, sigma: float, observation: float) -> float:
    """Closed-form CRPS for ``N(mean, sigma^2)`` at ``observation``."""
    from scipy.stats import norm

    standardised = (observation - mean) / sigma
    return float(
        sigma
        * (
            standardised * (2.0 * norm.cdf(standardised) - 1.0)
            + 2.0 * norm.pdf(standardised)
            - 1.0 / math.sqrt(math.pi)
        )
    )


def test_empirical_crps_matches_gaussian_closed_form() -> None:
    rng = np.random.default_rng(seed=42)
    mean, sigma = 1.5, 0.7
    samples = rng.normal(loc=mean, scale=sigma, size=20_000)
    observation = 2.1

    empirical = empirical_crps(samples, observation)
    closed_form = _gaussian_crps_closed_form(mean, sigma, observation)

    assert empirical == pytest.approx(closed_form, rel=0.05)


def test_empirical_crps_reduces_to_absolute_residual_for_point_mass() -> None:
    point_samples = np.full(50, 3.0)
    observation = 5.25
    assert empirical_crps(point_samples, observation) == pytest.approx(abs(5.25 - 3.0))


def test_coverage_indicator_inside_and_outside_central_interval() -> None:
    rng = np.random.default_rng(seed=7)
    samples = rng.normal(loc=0.0, scale=1.0, size=10_000)
    assert coverage_indicator(samples, observation=0.0, level=0.95) == 1
    assert coverage_indicator(samples, observation=5.0, level=0.95) == 0


def test_tail_coverage_indicator_left_and_right() -> None:
    rng = np.random.default_rng(seed=11)
    samples = rng.normal(loc=0.0, scale=1.0, size=10_000)
    assert tail_coverage_indicator(samples, observation=-3.0, alpha=0.05, tail="left") == 1
    assert tail_coverage_indicator(samples, observation=3.0, alpha=0.05, tail="right") == 1
    assert tail_coverage_indicator(samples, observation=0.0, alpha=0.05, tail="left") == 0
    assert tail_coverage_indicator(samples, observation=0.0, alpha=0.05, tail="right") == 0


def test_tail_coverage_rejects_invalid_tail_argument() -> None:
    samples = np.array([0.0, 1.0, 2.0])
    with pytest.raises(ValueError, match="tail"):
        tail_coverage_indicator(samples, observation=1.0, tail="upper")


def test_score_forecast_packages_all_metrics() -> None:
    rng = np.random.default_rng(seed=13)
    samples = rng.normal(loc=0.5, scale=0.2, size=5_000)
    scores = score_forecast(samples, observation=0.5)

    assert scores.bias == pytest.approx(samples.mean() - 0.5)
    assert scores.crps >= 0.0
    assert scores.coverage_95 == 1.0  # mean inside 95% central interval


def test_mincer_zarnowitz_unbiased_forecast_does_not_reject() -> None:
    rng = np.random.default_rng(seed=17)
    realisations = rng.normal(loc=0.0, scale=1.0, size=200)
    predictions = realisations + rng.normal(scale=0.1, size=200)

    result = mincer_zarnowitz(predictions, realisations)
    assert result.alpha == pytest.approx(0.0, abs=0.15)
    assert result.beta == pytest.approx(1.0, abs=0.1)
    assert result.p_value > 0.05


def test_mincer_zarnowitz_biased_forecast_rejects() -> None:
    rng = np.random.default_rng(seed=19)
    realisations = rng.normal(loc=0.0, scale=1.0, size=500)
    biased_predictions = 0.5 * realisations + 1.0  # alpha = 1, beta = 0.5

    result = mincer_zarnowitz(biased_predictions, realisations)
    assert result.p_value < 0.01
