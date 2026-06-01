"""Fractional differencing primitives.

Two pieces underpin ARFIMA-style forecasting:

1. **GPH (Geweke-Porter-Hudak) periodogram regression** for the long-
   memory parameter ``d``. The log-periodogram of a process with
   spectral density ``f(λ) ∝ λ^{−2d}`` near zero is asymptotically
   ``log I(λ) ≈ c − d · log(4 sin²(λ/2)) + noise``. Regressing
   ``log I`` on ``log(4 sin²(λ/2))`` over the low-frequency
   bandwidth ``m = T^bandwidth_exponent`` gives a consistent estimator
   for ``d`` at rate ``T^{−1/2}``. See :ref:`Geweke & Porter-Hudak
   (1983) <geweke-porter-hudak-1983>`.

2. **Hosking recursion** for the fractional difference operator
   ``(1 − L)^d`` and its inverse. The expansion coefficients are
   ``ψ_0 = 1`` and ``ψ_k = ψ_{k−1} · (k − 1 − d) / k``. With these,
   the fractionally differenced series and the inverse fractional
   integration share a single recursion — only the sign of ``d``
   changes between difference (``+d``) and integrate (``−d``). See
   :ref:`Hosking (1981) <hosking-1981>`.

The primitives below are deliberately self-contained — they take and
return numpy arrays and do not depend on the larger forecasting module.
This keeps the long-memory machinery testable in isolation.
"""
from __future__ import annotations

import numpy as np


MIN_GPH_FREQUENCIES = 4
MAX_FRACTIONAL_D = 0.499
MIN_FRACTIONAL_D = -0.499


def hosking_coefficients(d: float, length: int) -> np.ndarray:
    """Return ``length`` Hosking expansion coefficients of ``(1 − L)^d``.

    The output ``psi`` satisfies ``psi[0] = 1`` and
    ``psi[k] = psi[k − 1] · (k − 1 − d) / k`` for ``k ≥ 1``. This is the
    canonical recursion for the binomial expansion of ``(1 − L)^d``.

    Parameters
    ----------
    d:
        Fractional differencing parameter — must lie in ``(−0.5, 0.5)``
        for the process to be invertible/stationary.
    length:
        Number of coefficients to return (must be ≥ 1).
    """
    if length < 1:
        raise ValueError(f"length must be ≥ 1; got {length}")
    if not MIN_FRACTIONAL_D <= d <= MAX_FRACTIONAL_D:
        raise ValueError(
            f"d must be in [{MIN_FRACTIONAL_D}, {MAX_FRACTIONAL_D}]; got {d}"
        )
    coefficients = np.empty(length, dtype=float)
    coefficients[0] = 1.0
    for index in range(1, length):
        coefficients[index] = coefficients[index - 1] * (index - 1 - d) / index
    return coefficients


def fractional_difference(series: np.ndarray, d: float, truncate: int | None = None) -> np.ndarray:
    """Apply ``(1 − L)^d`` to ``series`` using the truncated Hosking expansion.

    Returns an array of the same length as ``series``. For each time
    ``t`` the differenced value is the convolution of the past values
    ``series[t], series[t−1], …`` with the Hosking coefficients of
    ``(1 − L)^d``, truncated at ``truncate`` lags.

    Parameters
    ----------
    series:
        1-D input.
    d:
        Fractional differencing parameter.
    truncate:
        Maximum lag retained in the convolution. Defaults to the length
        of the series — i.e. no truncation beyond the available
        history.
    """
    series_arr = np.asarray(series, dtype=float).ravel()
    if not np.all(np.isfinite(series_arr)):
        raise ValueError("series contains non-finite values")
    n = series_arr.size
    effective_truncate = n if truncate is None else min(int(truncate), n)
    coefficients = hosking_coefficients(d, effective_truncate)
    differenced = np.empty(n, dtype=float)
    for time_index in range(n):
        usable_lag = min(time_index + 1, effective_truncate)
        weights = coefficients[:usable_lag]
        differenced[time_index] = float(
            np.dot(weights, series_arr[time_index :: -1][:usable_lag])
        )
    return differenced


def fractional_integrate(series: np.ndarray, d: float, truncate: int | None = None) -> np.ndarray:
    """Apply ``(1 − L)^{−d}`` to ``series`` — inverse of :func:`fractional_difference`.

    Implementation simply calls :func:`fractional_difference` with
    ``−d``: by the same Hosking recursion, the inverse operator uses
    sign-flipped exponent.
    """
    return fractional_difference(series, -d, truncate=truncate)


def gph_estimate_d(series: np.ndarray, bandwidth_exponent: float = 0.5) -> float:
    """Geweke-Porter-Hudak log-periodogram regression estimator for ``d``.

    Demeans the series, computes its periodogram via FFT, and regresses
    ``log I(λ_j)`` on ``log(4 sin²(λ_j / 2))`` for the lowest ``m =
    floor(T^{bandwidth_exponent})`` non-zero Fourier frequencies. The
    OLS slope on the log-spectral-density regressor estimates ``−d`` —
    we negate to return ``d`` directly.

    The estimator is clipped to the stationarity range
    ``[MIN_FRACTIONAL_D, MAX_FRACTIONAL_D]``. Clipping is operationally
    necessary: GPH has non-negligible variance and can produce values
    just outside ``(−0.5, 0.5)`` on finite samples; the downstream
    Hosking recursion would diverge or become non-invertible.

    Parameters
    ----------
    series:
        1-D input of length ≥ ``2 / bandwidth_exponent`` so that
        ``m ≥ MIN_GPH_FREQUENCIES``.
    bandwidth_exponent:
        Power exponent for the bandwidth ``m = T^bandwidth_exponent``.
        Standard choices: ``0.5`` (Geweke-Porter-Hudak original),
        ``0.8`` (more efficient at the cost of bias near boundaries).
    """
    series_arr = np.asarray(series, dtype=float).ravel()
    if not np.all(np.isfinite(series_arr)):
        raise ValueError("series contains non-finite values")
    n = series_arr.size
    bandwidth = max(int(n**bandwidth_exponent), MIN_GPH_FREQUENCIES)
    if bandwidth >= n // 2:
        raise ValueError(
            f"bandwidth {bandwidth} too large vs series length {n} "
            "(would consume more than half the Fourier frequencies)"
        )

    demeaned = series_arr - series_arr.mean()
    fft_coefficients = np.fft.fft(demeaned)
    periodogram = (np.abs(fft_coefficients) ** 2) / n
    # Drop the DC term; the next ``bandwidth`` entries are the lowest
    # non-zero positive Fourier frequencies.
    frequencies = 2.0 * np.pi * np.arange(1, bandwidth + 1) / n
    spectral_regressor = np.log(4.0 * np.sin(frequencies / 2.0) ** 2)
    log_periodogram = np.log(periodogram[1 : bandwidth + 1])

    design_matrix = np.column_stack([np.ones(bandwidth), spectral_regressor])
    coefficients, *_ = np.linalg.lstsq(design_matrix, log_periodogram, rcond=None)
    estimated_d = float(-coefficients[1])
    return float(np.clip(estimated_d, MIN_FRACTIONAL_D, MAX_FRACTIONAL_D))
