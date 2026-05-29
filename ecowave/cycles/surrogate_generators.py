"""Surrogate path generators — building blocks for null hypothesis testing.

This module factors out the surrogate **generation** step that was previously
inlined inside ``ecowave.cycles.surrogate``. The Gate 1 helpers
(``ar1_bootstrap_null``, ``phase_scramble_null``) keep their public API but
delegate path generation here, and the new non-cyclical diagnostics
(``ecowave.cycles.alternative_dynamics``) consume the same generators to test
arbitrary statistics (Hurst, MF-DFA Δα, 1/f^β slope, etc.) against the same
nulls.

Two surrogate families, both standard in non-linear time-series analysis:

- **AR(1) bootstrap** (Torrence & Compo 1998 ; Grinsted *et al.* 2004) :
  fit (φ, σ, μ) on the input, simulate red-noise paths with the same
  persistence. Sensitive to spectral concentration *above* red noise.
- **Phase-scramble** (Theiler *et al.* 1992) : preserve the empirical
  power spectrum exactly, randomise phases. Tests whether band-power
  concentrations are locally coherent or spectrum-explained.

Non-regression contract: ``ar1_surrogate_series(y, n, seed)`` must produce
the **same RNG sequence** as the inlined loop used by ``surrogate.py``
before this refactor — covered by ``tests/test_surrogate_generators.py``.
"""
from __future__ import annotations

from typing import Iterator

import numpy as np


def fit_ar1(y: np.ndarray) -> tuple[float, float, float]:
    """Return (phi, sigma_noise, mu) for y = mu + phi*(y_{t-1} - mu) + eps.

    The lag-1 coefficient is clipped to [-0.99, 0.99] to keep simulated
    paths bounded; sigma is floored at 1e-9 to guard against degenerate
    constant inputs.
    """
    if y.size < 4:
        return 0.0, 1.0, 0.0
    mu = float(np.nanmean(y))
    centered = y - mu
    num = float(np.nansum(centered[:-1] * centered[1:]))
    den = float(np.nansum(centered[:-1] ** 2))
    phi = max(min(num / den if den > 0 else 0.0, 0.99), -0.99)
    residuals = centered[1:] - phi * centered[:-1]
    sigma = float(np.nanstd(residuals)) if residuals.size else 1.0
    return phi, max(sigma, 1e-9), mu


def simulate_ar1(phi: float, sigma: float, mu: float, n: int,
                 rng: np.random.Generator) -> np.ndarray:
    """Simulate one AR(1) path of length n with the supplied generator."""
    eps = rng.normal(loc=0.0, scale=sigma, size=n)
    y = np.empty(n, dtype=float)
    y[0] = mu + eps[0] / max(np.sqrt(1.0 - phi ** 2), 1e-9)
    for t in range(1, n):
        y[t] = mu + phi * (y[t - 1] - mu) + eps[t]
    return y


def ar1_surrogate_series(y: np.ndarray, n_surrogates: int,
                         seed: int = 0) -> Iterator[np.ndarray]:
    """Yield ``n_surrogates`` AR(1) surrogate paths preserving (φ, σ, μ).

    The RNG is seeded once at the outset and advanced sequentially so that
    each surrogate consumes a fixed slice of the stream. This guarantees
    reproducibility for any consumer (Gate 1 band-power, Hurst diagnostic,
    multifractal spectrum, etc.) — equivalent to the inlined loop in the
    pre-refactor ``ar1_bootstrap_null``.
    """
    phi, sigma, mu = fit_ar1(y)
    rng = np.random.default_rng(seed)
    for _ in range(n_surrogates):
        yield simulate_ar1(phi, sigma, mu, y.size, rng)


def phase_scramble_surrogate_series(y: np.ndarray, n_surrogates: int,
                                    seed: int = 0) -> Iterator[np.ndarray]:
    """Yield ``n_surrogates`` phase-scrambled surrogates (Theiler 1992).

    Computes the rFFT once, then randomises phase for each surrogate while
    preserving the conjugate-symmetric structure so the inverse transform
    remains real-valued. The zero-frequency phase is pinned at 0 and, for
    even-length inputs, the Nyquist phase is pinned too — both required for
    a real-valued ``irfft`` output.
    """
    n = y.size
    spectrum = np.fft.rfft(y - y.mean())
    magnitude = np.abs(spectrum)
    mean_y = float(y.mean())
    rng = np.random.default_rng(seed)
    for _ in range(n_surrogates):
        random_phase = rng.uniform(-np.pi, np.pi, size=spectrum.size)
        random_phase[0] = 0.0
        if n % 2 == 0:
            random_phase[-1] = 0.0
        scrambled = magnitude * np.exp(1j * random_phase)
        yield np.fft.irfft(scrambled, n=n) + mean_y
