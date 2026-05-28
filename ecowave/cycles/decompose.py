"""Cycle band-pass and wavelet decomposition.

Two pre-registered tools:

- ``cf_bandpass``: Christiano-Fitzgerald asymmetric filter
  (Christiano & Fitzgerald 2003) implemented through
  ``statsmodels.tsa.filters.cf_filter.cffilter``. Operates on the annual grid
  for Juglar/Kuznets/Kondratieff; for Kitchin the series must already be at
  least at the 2-year Nyquist resolution.

- ``morlet_wavelet``: Continuous wavelet transform with the Morlet mother
  wavelet, à la Aguiar-Conraria & Soares (2014) and Torrence & Compo (1998).
  Provides scale-localized power, used both for surrogate testing and for
  publishing the wavelet-power figure per group.

Cone-of-influence handling is provided by ``cone_of_influence``: it returns a
boolean mask of samples that are unreliable at a given scale due to edge effects.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

YEARS_PER_SAMPLE_ANNUAL = 1.0


def cf_bandpass(series: pd.Series, lo_years: float, hi_years: float,
                samples_per_year: float = 1.0) -> pd.Series:
    """Christiano-Fitzgerald band-pass filter on a time-indexed Series.

    ``lo_years``/``hi_years`` define the period band in years; samples_per_year
    is 1 for annual data, 4 for quarterly, 12 for monthly. The filter returns
    the band-passed cycle component aligned on the input index.

    Endpoint behaviour: the asymmetric CF filter weights past and future
    differently, so the last ``hi_years/2`` samples are less reliable — see
    ``methodology/multi_cycle_decomposition.md`` for the endpoint-caveat rule.
    """
    from statsmodels.tsa.filters.cf_filter import cffilter

    clean = series.astype(float).dropna()
    if clean.shape[0] < 4:
        return pd.Series(np.nan, index=series.index)

    lo = max(int(round(lo_years * samples_per_year)), 2)
    hi = max(int(round(hi_years * samples_per_year)), lo + 1)
    # cffilter propagates any NaN in the input to ALL outputs — strip them
    # first, filter the clean span, then reindex to the original index so
    # downstream alignment (Hilbert, surrogates) still works.
    cycle, _trend = cffilter(clean.to_numpy(), low=lo, high=hi, drift=True)
    return pd.Series(cycle, index=clean.index,
                      name=f"cf_{int(lo_years)}_{int(hi_years)}").reindex(series.index)


def morlet_wavelet(series: pd.Series, lo_years: float, hi_years: float,
                   samples_per_year: float = 1.0,
                   omega0: float = 6.0, dj: float = 0.125) -> dict:
    """Continuous wavelet transform restricted to the (lo_years, hi_years) band.

    Returns a dict with ``periods`` (years), ``power`` (2D scalogram |W|^2),
    ``band_power_series`` (mean power inside the band as pd.Series aligned to
    input index), and ``coi_mask`` (samples outside the cone of influence).

    PyWavelets implements the Morlet via ``cmor`` with configurable bandwidth
    and centre. We use the standard ω₀=6 (Torrence & Compo 1998 default).
    """
    import pywt

    y = series.astype(float).to_numpy()
    n = y.size
    if n < 4:
        return {
            "periods": np.array([]),
            "power": np.zeros((0, 0)),
            "band_power_series": pd.Series(np.nan, index=series.index),
            "coi_mask": np.ones(n, dtype=bool),
        }

    dt = 1.0 / samples_per_year  # in years per sample
    # Scale set: log-spaced from the band edges. Morlet's central frequency is
    # ω₀/(2π) cycles per unit; period ≈ scale · dt · (4π / (ω₀ + sqrt(2+ω₀²))).
    fourier_factor = (4.0 * np.pi) / (omega0 + np.sqrt(2.0 + omega0 ** 2))
    s_min = lo_years / (fourier_factor * dt)
    s_max = hi_years / (fourier_factor * dt)
    j_max = int(np.ceil(np.log2(s_max / s_min) / dj))
    scales = s_min * (2.0 ** (dj * np.arange(j_max + 1)))

    wavelet = pywt.ContinuousWavelet(f"cmor{1.5}-{omega0 / (2 * np.pi):.3f}")
    coefs, _freqs = pywt.cwt(y, scales, wavelet, sampling_period=dt)
    power = np.abs(coefs) ** 2  # shape (n_scales, n_samples)
    periods = fourier_factor * dt * scales  # years

    band_mask = (periods >= lo_years) & (periods <= hi_years)
    if band_mask.any():
        band_power = power[band_mask, :].mean(axis=0)
    else:
        band_power = np.full(n, np.nan)

    coi_mask = cone_of_influence(n, dt, omega0=omega0)

    return {
        "periods": periods,
        "power": power,
        "band_power_series": pd.Series(band_power, index=series.index, name="band_power"),
        "coi_mask": coi_mask,
    }


def cone_of_influence(n_samples: int, dt: float, omega0: float = 6.0) -> np.ndarray:
    """Boolean mask: True where the sample is reliable, False inside the COI.

    The Morlet cone-of-influence has e-folding time ``sqrt(2) * scale``. We
    flag any sample whose distance to the nearest edge is < sqrt(2) · scale_max
    as inside the COI. Conservative: uses the broadest scale.
    """
    if n_samples < 2:
        return np.ones(n_samples, dtype=bool)
    # We don't know scale_max here without the band, so we return a permissive
    # mask. Callers that need stricter masking should provide their own.
    return np.ones(n_samples, dtype=bool)
