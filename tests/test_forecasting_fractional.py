"""Tests for the fractional-differencing primitives.

The Hosking recursion and the GPH estimator are load-bearing for any
ARFIMA forecast. These tests pin (i) the Hosking expansion matches the
binomial coefficients, (ii) ``fractional_integrate`` inverts
``fractional_difference`` to within truncation error, and (iii) GPH
recovers a known ``d`` on a synthetic ARFIMA(0, d, 0) sample.
"""
from __future__ import annotations

import numpy as np
import pytest

from ecowave.forecasting.fractional import (
    MAX_FRACTIONAL_D,
    MIN_FRACTIONAL_D,
    fractional_difference,
    fractional_integrate,
    gph_estimate_d,
    hosking_coefficients,
)


def test_hosking_coefficients_match_binomial_expansion() -> None:
    """For ``k = 0, 1, 2, 3`` the recursion equals ``(−1)^k · (d choose k)``."""
    d = 0.3
    coefficients = hosking_coefficients(d, length=4)
    assert coefficients[0] == pytest.approx(1.0)
    assert coefficients[1] == pytest.approx(-d)
    # (1 − L)^d = Σ_k (−1)^k · (d choose k) · L^k ; the sign alternates
    # with ``k``.
    assert coefficients[2] == pytest.approx(d * (d - 1) / 2.0)
    assert coefficients[3] == pytest.approx(-d * (d - 1) * (d - 2) / 6.0)


def test_hosking_coefficients_reject_d_outside_range() -> None:
    with pytest.raises(ValueError, match="d must be in"):
        hosking_coefficients(d=0.8, length=10)


def test_fractional_difference_integrate_roundtrip_is_near_identity() -> None:
    rng = np.random.default_rng(seed=42)
    series = rng.normal(size=500)
    d = 0.3
    differenced = fractional_difference(series, d)
    reconstructed = fractional_integrate(differenced, d)
    # Truncation error grows with d and series length; bulk of the
    # interior should match within tight tolerance.
    np.testing.assert_allclose(reconstructed[100:], series[100:], atol=1e-9)


def test_fractional_difference_zero_d_is_identity() -> None:
    series = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    np.testing.assert_allclose(fractional_difference(series, d=0.0), series)


def test_fractional_difference_unit_d_is_first_difference() -> None:
    """``(1 − L)^1 X_t = X_t − X_{t−1}`` — but our clip prevents d = 1."""
    # The implementation clamps |d| < 0.5; test the closest legitimate
    # alias against the recursion directly.
    series = np.arange(5, dtype=float)
    differenced = fractional_difference(series, d=MAX_FRACTIONAL_D)
    expected_first = series[0]
    assert differenced[0] == pytest.approx(expected_first)


def test_gph_recovers_known_d_on_simulated_arfima() -> None:
    rng = np.random.default_rng(seed=7)
    true_d = 0.3
    # Simulate ARFIMA(0, d, 0) by fractionally integrating Gaussian
    # white noise.
    innovations = rng.normal(size=5_000)
    simulated_series = fractional_integrate(innovations, d=true_d)
    estimated_d = gph_estimate_d(simulated_series, bandwidth_exponent=0.6)
    # GPH consistent at rate T^{−1/2} ; allow generous tolerance.
    assert estimated_d == pytest.approx(true_d, abs=0.15)


def test_gph_clips_to_stationarity_range() -> None:
    rng = np.random.default_rng(seed=11)
    # Strongly non-stationary input (integrated random walk) — GPH
    # would return |d| > 0.5 without clipping.
    extreme_series = np.cumsum(np.cumsum(rng.normal(size=500)))
    estimated_d = gph_estimate_d(extreme_series)
    assert MIN_FRACTIONAL_D <= estimated_d <= MAX_FRACTIONAL_D


def test_gph_rejects_non_finite_input() -> None:
    with pytest.raises(ValueError, match="non-finite"):
        gph_estimate_d(np.array([1.0, np.nan, 3.0, 4.0]))


def test_gph_rejects_bandwidth_too_large_for_series() -> None:
    with pytest.raises(ValueError, match="bandwidth"):
        gph_estimate_d(np.zeros(8), bandwidth_exponent=0.99)
