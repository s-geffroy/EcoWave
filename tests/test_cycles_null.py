"""AR(1) bootstrap surrogate null — falsifiability gate."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.cycles.surrogate import ar1_bootstrap_null


def _ar1(phi: float, sigma: float, n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = phi * y[t - 1] + rng.normal(scale=sigma)
    return y


def test_red_noise_is_rejected():
    """Pure AR(1) red noise has no cycle — null must NOT reject the null."""
    y = _ar1(phi=0.7, sigma=1.0, n=200, seed=0)
    series = pd.Series(y, index=np.arange(200))
    null = ar1_bootstrap_null(series, lo_years=7, hi_years=11,
                              samples_per_year=1.0, n_surrogates=200, seed=42)
    assert null.reject_cycle, f"Red noise should fail Gate 1, got p={null.p_value:.3f}"


def test_clean_juglar_signal_passes_gate1():
    """A clean Juglar sinusoid embedded in red noise must beat the AR(1) null."""
    n = 200
    t = np.arange(n)
    rng = np.random.default_rng(0)
    juglar = 3.0 * np.sin(2.0 * np.pi * t / 8.0)
    noise = _ar1(phi=0.3, sigma=0.5, n=n, seed=1)
    series = pd.Series(juglar + noise, index=t)
    null = ar1_bootstrap_null(series, lo_years=7, hi_years=11,
                              samples_per_year=1.0, n_surrogates=300, seed=7)
    assert not null.reject_cycle, f"Juglar+red should pass Gate 1, p={null.p_value:.3f}"
    assert null.p_value < 0.05


def test_seed_reproducibility():
    n = 80
    rng = np.random.default_rng(123)
    series = pd.Series(np.sin(2.0 * np.pi * np.arange(n) / 8.0) + rng.normal(scale=0.3, size=n),
                       index=np.arange(n))
    a = ar1_bootstrap_null(series, lo_years=7, hi_years=11,
                            samples_per_year=1.0, n_surrogates=100, seed=42)
    b = ar1_bootstrap_null(series, lo_years=7, hi_years=11,
                            samples_per_year=1.0, n_surrogates=100, seed=42)
    assert abs(a.p_value - b.p_value) < 1e-12


def test_too_short_series_rejects_by_default():
    short = pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2])
    null = ar1_bootstrap_null(short, lo_years=7, hi_years=11,
                              samples_per_year=1.0, n_surrogates=10, seed=0)
    assert null.reject_cycle
    assert null.n_surrogates == 0
