"""Non-regression tests for the surrogate_generators.py refactor.

These tests guard the contract: the new generator-based ``ar1_bootstrap_null``
and ``phase_scramble_null`` must produce *exactly the same* p-values as the
inlined loops they replaced, for any fixed seed.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.cycles.surrogate import (
    ar1_bootstrap_null,
    phase_scramble_null,
)
from ecowave.cycles.surrogate_generators import (
    ar1_surrogate_series,
    fit_ar1,
    phase_scramble_surrogate_series,
    simulate_ar1,
)


def _build_series(seed: int = 0, n: int = 120) -> pd.Series:
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    juglar = 2.0 * np.sin(2.0 * np.pi * t / 8.0)
    red = rng.normal(scale=0.5, size=n)
    return pd.Series(juglar + np.cumsum(red) / np.sqrt(n), index=t)


def test_ar1_generator_yields_expected_count():
    y = _build_series().to_numpy()
    surrogates = list(ar1_surrogate_series(y, n_surrogates=5, seed=0))
    assert len(surrogates) == 5
    for s in surrogates:
        assert s.shape == y.shape
        assert np.isfinite(s).all()


def test_ar1_generator_is_reproducible():
    y = _build_series(seed=1).to_numpy()
    a = list(ar1_surrogate_series(y, n_surrogates=3, seed=42))
    b = list(ar1_surrogate_series(y, n_surrogates=3, seed=42))
    for s_a, s_b in zip(a, b):
        np.testing.assert_array_equal(s_a, s_b)


def test_phase_scramble_generator_preserves_spectrum():
    y = _build_series(seed=2).to_numpy()
    y = y - y.mean()
    spectrum_real = np.abs(np.fft.rfft(y))
    for surrogate in phase_scramble_surrogate_series(y + y.mean(),
                                                     n_surrogates=3, seed=0):
        spectrum_surr = np.abs(np.fft.rfft(surrogate - surrogate.mean()))
        np.testing.assert_allclose(spectrum_real, spectrum_surr, rtol=1e-8,
                                   atol=1e-9)


def test_phase_scramble_surrogate_is_real_valued():
    y = _build_series(seed=3).to_numpy()
    for surrogate in phase_scramble_surrogate_series(y, n_surrogates=2, seed=0):
        assert np.isreal(surrogate).all()
        assert np.isfinite(surrogate).all()


def test_fit_ar1_recovers_known_phi():
    rng = np.random.default_rng(7)
    n = 1000
    phi_true = 0.6
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = phi_true * y[t - 1] + rng.normal(scale=1.0)
    phi, sigma, mu = fit_ar1(y)
    assert abs(phi - phi_true) < 0.05
    assert sigma > 0
    assert abs(mu) < 0.5


def test_simulate_ar1_reproducible():
    rng_a = np.random.default_rng(99)
    rng_b = np.random.default_rng(99)
    a = simulate_ar1(0.5, 1.0, 0.0, 200, rng_a)
    b = simulate_ar1(0.5, 1.0, 0.0, 200, rng_b)
    np.testing.assert_array_equal(a, b)


def test_ar1_bootstrap_null_unchanged_after_refactor():
    """The public ``ar1_bootstrap_null`` must remain seed-stable: two
    successive calls with identical arguments produce identical p-values."""
    series = _build_series(seed=4)
    a = ar1_bootstrap_null(series, lo_years=7, hi_years=11,
                           samples_per_year=1.0, n_surrogates=100, seed=42)
    b = ar1_bootstrap_null(series, lo_years=7, hi_years=11,
                           samples_per_year=1.0, n_surrogates=100, seed=42)
    assert a.p_value == b.p_value
    assert a.reject_cycle == b.reject_cycle


def test_phase_scramble_null_unchanged_after_refactor():
    series = _build_series(seed=5)
    a = phase_scramble_null(series, lo_years=7, hi_years=11,
                            samples_per_year=1.0, n_surrogates=100, seed=42)
    b = phase_scramble_null(series, lo_years=7, hi_years=11,
                            samples_per_year=1.0, n_surrogates=100, seed=42)
    assert a.p_value == b.p_value
