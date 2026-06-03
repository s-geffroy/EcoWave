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


# ---------------------------------------------------------------------------
# ARFIMA(0, d, 0) null — Granger & Joyeux 1980 ; Hosking 1981
# Used as a long-memory-aware complement to the AR(1) null for Gate 1.
# ---------------------------------------------------------------------------

def estimate_d_gph(y: np.ndarray, m: int | None = None) -> float:
    """Geweke--Porter-Hudak (1983) log-periodogram estimator of d.

    Fits log I(lambda_j) = c - d * log(4 sin^2(lambda_j / 2)) + eps_j
    over the m lowest non-zero Fourier frequencies, with the conventional
    choice m = floor(T^0.5). Returns d clipped to [-0.49, 0.49].
    """
    n = y.size
    if n < 16:
        return 0.0
    if m is None:
        m = max(2, int(round(np.sqrt(n))))
    m = min(m, n // 2 - 1)
    y_demean = y - float(np.mean(y))
    spectrum = np.fft.rfft(y_demean)
    periodogram = (np.abs(spectrum) ** 2) / n
    # Drop the zero-frequency bin; keep the m lowest non-zero.
    periodogram = periodogram[1:m + 1]
    lam = 2.0 * np.pi * np.arange(1, m + 1) / n
    x = np.log(4.0 * np.sin(lam / 2.0) ** 2)
    y_reg = np.log(periodogram + 1e-300)
    # OLS slope of y_reg on x: d_hat = -slope.
    x_centered = x - x.mean()
    y_centered = y_reg - y_reg.mean()
    denom = float(np.sum(x_centered ** 2))
    if denom <= 0.0:
        return 0.0
    slope = float(np.sum(x_centered * y_centered) / denom)
    d_hat = -slope
    return float(max(-0.49, min(0.49, d_hat)))


def _hosking_coeffs(d: float, n: int) -> np.ndarray:
    """Hosking (1981) MA coefficients of the fractional-difference filter
    (1-L)^{-d} = sum_k psi_k L^k, with psi_0 = 1 and the recursion
    psi_k = psi_{k-1} * (k - 1 + d) / k.
    """
    coeffs = np.empty(n, dtype=float)
    coeffs[0] = 1.0
    for k in range(1, n):
        coeffs[k] = coeffs[k - 1] * (k - 1 + d) / k
    return coeffs


def simulate_arfima(d: float, sigma: float, mu: float, n: int,
                    rng: np.random.Generator) -> np.ndarray:
    """Simulate one ARFIMA(0, d, 0) path of length n via Hosking convolution.

    For d in (-0.5, 0.5), draws white-noise eps ~ N(0, sigma^2) of length
    n and convolves with the truncated psi_k coefficients.
    """
    eps = rng.normal(loc=0.0, scale=sigma, size=n)
    psi = _hosking_coeffs(d, n)
    # Convolve: y_t = sum_{k=0}^{t} psi_k * eps_{t-k}; equivalent to full
    # convolution truncated to the first n entries.
    y = np.convolve(eps, psi, mode="full")[:n]
    return y + mu


def fit_arfima_d_sigma(y: np.ndarray) -> tuple[float, float, float]:
    """Return (d_hat, sigma_noise, mu) for an ARFIMA(0, d, 0) fit.

    d_hat is the GPH estimate; sigma is the residual std after applying
    the (1-L)^{d_hat} fractional difference to the demeaned series.
    """
    if y.size < 16:
        return 0.0, 1.0, 0.0
    mu = float(np.mean(y))
    d_hat = estimate_d_gph(y)
    # Apply fractional difference (1-L)^d_hat: coefficients pi_k with
    # pi_0 = 1 and pi_k = pi_{k-1} * (k - 1 - d) / k.
    n = y.size
    pi_coeffs = np.empty(n, dtype=float)
    pi_coeffs[0] = 1.0
    for k in range(1, n):
        pi_coeffs[k] = pi_coeffs[k - 1] * (k - 1 - d_hat) / k
    centered = y - mu
    residuals = np.empty(n, dtype=float)
    for t in range(n):
        # residual_t = sum_{k=0}^{t} pi_k * centered_{t-k}
        residuals[t] = float(np.dot(pi_coeffs[:t + 1], centered[t::-1]))
    sigma = float(np.std(residuals[max(1, n // 10):]))
    return d_hat, max(sigma, 1e-9), mu


def arfima_surrogate_series(y: np.ndarray, n_surrogates: int,
                            seed: int = 0,
                            d_override: float | None = None) -> Iterator[np.ndarray]:
    """Yield ``n_surrogates`` ARFIMA(0, d_hat, 0) surrogate paths.

    Estimates d once via GPH (or uses ``d_override`` if supplied), then
    simulates surrogate paths via Hosking convolution. Conserves the
    empirical (mu, residual sigma). The GPH d_hat is clipped to
    [-0.49, 0.49] for stationarity.
    """
    d_hat, sigma, mu = fit_arfima_d_sigma(y)
    if d_override is not None:
        d_hat = float(max(-0.49, min(0.49, d_override)))
    rng = np.random.default_rng(seed)
    for _ in range(n_surrogates):
        yield simulate_arfima(d_hat, sigma, mu, y.size, rng)
