"""Tests for the phase-coherence statistic and the revised phase_scramble_null.

The phase-randomised null was redesigned (see surrogate.py) to use a
phase-coherence statistic — the stability of the instantaneous frequency
inside the canonical band — rather than band-power. Band-power against a
phase-randomised surrogate is degenerate by Parseval's theorem
(Schreiber & Schmitz 2000); phase coherence is destroyed by phase
randomisation even when the spectrum is preserved.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.cycles.surrogate import (
    phase_coherence_in_band,
    phase_scramble_null,
)


def _ar1(phi: float, sigma: float, n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = phi * y[t - 1] + rng.normal(scale=sigma)
    return y


def test_phase_coherence_high_on_pure_cosine():
    """A pure cosine in the band has a stable instantaneous frequency."""
    n = 200
    t = np.arange(n)
    y = np.cos(2.0 * np.pi * t / 8.0)
    series = pd.Series(y, index=t)
    coherence = phase_coherence_in_band(series, lo_years=7, hi_years=11)
    assert coherence > 0.7, f"pure cosine: coherence={coherence:.3f}"


def test_phase_coherence_returns_value_on_red_noise():
    """Red noise filtered through a narrow band yields an artificially
    coherent-looking signal. The phase-coherence statistic is therefore
    not very discriminative on Gaussian linear signals — this is a
    documented limit of the test and is why the AR(1) bootstrap, not
    the phase-coherence null, is the load-bearing Gate 1 statistic.
    The point of this test is to lock in the empirically observed
    behaviour so any future change to the statistic is conscious.
    """
    series = pd.Series(_ar1(phi=0.7, sigma=1.0, n=200, seed=0))
    coherence = phase_coherence_in_band(series, lo_years=7, hi_years=11)
    assert 0.0 <= coherence <= 1.0
    # Empirically observed on this seed: 0.81. Lock the regime.
    assert 0.5 < coherence < 0.95


def test_phase_coherence_in_band_is_bounded():
    """Statistic is always in [0, 1]."""
    rng = np.random.default_rng(42)
    for seed in range(5):
        y = rng.standard_normal(200)
        c = phase_coherence_in_band(pd.Series(y), lo_years=7, hi_years=11)
        assert 0.0 <= c <= 1.0


def test_phase_scramble_null_short_series_returns_safe_default():
    """Series shorter than 16 observations cannot be tested."""
    series = pd.Series(np.arange(10, dtype=float))
    result = phase_scramble_null(series, lo_years=7, hi_years=11,
                                  n_surrogates=10, seed=0)
    assert result.reject_cycle
    assert result.n_surrogates == 0


def test_phase_scramble_null_seed_reproducible():
    """Same seed must produce the same p-value (bit-for-bit)."""
    n = 80
    rng = np.random.default_rng(123)
    y = np.cos(2.0 * np.pi * np.arange(n) / 8.0) + rng.normal(scale=0.3, size=n)
    series = pd.Series(y, index=np.arange(n))
    a = phase_scramble_null(series, lo_years=7, hi_years=11,
                             n_surrogates=100, seed=42)
    b = phase_scramble_null(series, lo_years=7, hi_years=11,
                             n_surrogates=100, seed=42)
    assert abs(a.p_value - b.p_value) < 1e-12


def test_phase_scramble_returns_a_p_value():
    """Smoke test: the phase-scramble coherence null produces a well-defined
    p-value in [1/(B+1), 1] for any input long enough to be processed.
    The discriminative value of this null on Gaussian-linear signals is
    limited (see test_phase_coherence_returns_value_on_red_noise); the
    paper now uses the AR(1) bootstrap as the primary Gate 1 and reports
    the phase-coherence p-value as a complementary diagnostic.
    """
    n = 200
    t = np.arange(n)
    rng = np.random.default_rng(0)
    juglar = 3.0 * np.cos(2.0 * np.pi * t / 8.0)
    noise = _ar1(phi=0.3, sigma=0.5, n=n, seed=1)
    series = pd.Series(juglar + noise, index=t)
    result = phase_scramble_null(series, lo_years=7, hi_years=11,
                                  n_surrogates=200, seed=7)
    # P-value must be in the valid range; specific value depends on the
    # discriminative power of the statistic and is not asserted here.
    assert 1.0 / 201.0 <= result.p_value <= 1.0
