"""AR(1) bootstrap null test — Gate 1 of the CPV protocol.

For each (group, indicator, band), the band-power of the band-passed series
must exceed the (1-α) quantile of band-power computed from B simulated AR(1)
red-noise paths with the same mean / variance / persistence as the input.

Source: Torrence & Compo (1998), "A Practical Guide to Wavelet Analysis";
Grinsted et al. (2004), "Application of the cross wavelet transform". Both
use AR(1) as the canonical null because pure red noise has no preferred
frequency — a band-power that rises above red noise is evidence of an actual
cyclic component at that frequency.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ecowave.cycles.decompose import cf_bandpass


@dataclass(frozen=True)
class NullResult:
    real_band_power: float
    p_value: float
    reject_cycle: bool
    n_surrogates: int
    method: str = "AR(1) bootstrap on CF band-power"


def _fit_ar1(y: np.ndarray) -> tuple[float, float, float]:
    """Return (phi, sigma_noise, mu) for y = mu + phi*(y_{t-1} - mu) + eps."""
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


def _simulate_ar1(phi: float, sigma: float, mu: float, n: int,
                  rng: np.random.Generator) -> np.ndarray:
    eps = rng.normal(loc=0.0, scale=sigma, size=n)
    y = np.empty(n, dtype=float)
    y[0] = mu + eps[0] / max(np.sqrt(1.0 - phi ** 2), 1e-9)
    for t in range(1, n):
        y[t] = mu + phi * (y[t - 1] - mu) + eps[t]
    return y


def ar1_bootstrap_null(series: pd.Series, lo_years: float, hi_years: float,
                       samples_per_year: float = 1.0,
                       n_surrogates: int = 1000, alpha: float = 0.05,
                       seed: int = 0) -> NullResult:
    """Test: does the band [lo_years, hi_years] carry more power than AR(1)?

    Returns NullResult with the real band-power, p-value, and a boolean
    ``reject_cycle`` flag (True ⇔ the cycle is not separable from red noise,
    i.e. Gate 1 fails). Reproducible with the given seed.
    """
    y = series.dropna().astype(float).to_numpy()
    if y.size < 8:
        return NullResult(real_band_power=np.nan, p_value=1.0,
                          reject_cycle=True, n_surrogates=0)

    real_cycle = cf_bandpass(pd.Series(y), lo_years, hi_years,
                             samples_per_year=samples_per_year).dropna().to_numpy()
    real_power = float(np.sum(real_cycle ** 2))

    phi, sigma, mu = _fit_ar1(y)
    rng = np.random.default_rng(seed)
    n_geq = 0
    for _ in range(n_surrogates):
        surrogate = _simulate_ar1(phi, sigma, mu, y.size, rng)
        surr_cycle = cf_bandpass(pd.Series(surrogate), lo_years, hi_years,
                                 samples_per_year=samples_per_year).dropna().to_numpy()
        if np.sum(surr_cycle ** 2) >= real_power:
            n_geq += 1
    p_value = (n_geq + 1) / (n_surrogates + 1)
    return NullResult(real_band_power=real_power, p_value=p_value,
                      reject_cycle=p_value >= alpha, n_surrogates=n_surrogates)
