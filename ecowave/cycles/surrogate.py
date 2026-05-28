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

    def __bool__(self) -> bool:
        return not self.reject_cycle


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


def phase_scramble_null(series: pd.Series, lo_years: float, hi_years: float,
                        samples_per_year: float = 1.0,
                        n_surrogates: int = 1000, alpha: float = 0.05,
                        seed: int = 0) -> NullResult:
    """Phase-randomised Fourier surrogate (Theiler et al. 1992).

    Preserves the full power spectrum but randomises the phases — i.e. it
    asks "is the band-power concentration *locally coherent in time* (a real
    cycle), or just an artefact of spectral content with random phases?"

    The AR(1) null and the phase-scrambling null are complementary:

    - **AR(1)** asks whether the band stands out *above red noise* of the
      same persistence — sensitive to spectral concentration relative to a
      smooth red-noise baseline.
    - **Phase-scrambling** preserves the spectrum exactly, so the surrogate
      has the *same* band-power on average as the real series. It rejects
      when the real series has unusually large CF-band-power *given its own
      spectrum* — typically because cyclical phases are aligned in a way
      pure-random phases are not.

    The two are run side-by-side as a dual-null test (`surrogate.dual_null`).
    Source: Theiler, J., Eubank, S., Longtin, A., Galdrikian, B., & Farmer,
    J. D. (1992). Testing for nonlinearity in time series: the method of
    surrogate data. Physica D, 58, 77–94.
    """
    y = series.dropna().astype(float).to_numpy()
    if y.size < 8:
        return NullResult(real_band_power=np.nan, p_value=1.0,
                          reject_cycle=True, n_surrogates=0,
                          method="phase-scramble (Theiler 1992)")

    real_cycle = cf_bandpass(pd.Series(y), lo_years, hi_years,
                              samples_per_year=samples_per_year).dropna().to_numpy()
    real_power = float(np.sum(real_cycle ** 2))

    # FFT once; scramble phases for each surrogate. We preserve conjugate
    # symmetry so the inverse transform stays real-valued.
    spectrum = np.fft.rfft(y - y.mean())
    magnitude = np.abs(spectrum)
    rng = np.random.default_rng(seed)
    n = y.size
    n_geq = 0
    for _ in range(n_surrogates):
        random_phase = rng.uniform(-np.pi, np.pi, size=spectrum.size)
        random_phase[0] = 0.0
        if n % 2 == 0:
            random_phase[-1] = 0.0
        scrambled = magnitude * np.exp(1j * random_phase)
        surrogate = np.fft.irfft(scrambled, n=n) + y.mean()
        surr_cycle = cf_bandpass(pd.Series(surrogate), lo_years, hi_years,
                                  samples_per_year=samples_per_year).dropna().to_numpy()
        if np.sum(surr_cycle ** 2) >= real_power:
            n_geq += 1
    p_value = (n_geq + 1) / (n_surrogates + 1)
    return NullResult(real_band_power=real_power, p_value=p_value,
                      reject_cycle=p_value >= alpha, n_surrogates=n_surrogates,
                      method="phase-scramble (Theiler 1992)")


def wavelet_bandpower_null(series: pd.Series, lo_years: float, hi_years: float,
                            samples_per_year: float = 1.0,
                            n_surrogates: int = 500, alpha: float = 0.05,
                            seed: int = 0) -> NullResult:
    """AR(1) null using **wavelet** band-power as the statistic.

    Identical to ``ar1_bootstrap_null`` except the test statistic is the
    sum of the Morlet wavelet scaleogram |W(s,t)|² integrated over the
    in-band scales. Wavelet band-power is less endpoint-sensitive than CF
    band-power (CF has explicit asymmetric edge weights; wavelet has the
    cone of influence but its in-band power is more localised), so this
    null tends to be easier to beat at the right boundary of the panel.

    Heavier than the CF version (CWT per surrogate). Defaults to 500
    surrogates instead of 1000 for tractability.
    """
    from ecowave.cycles.decompose import morlet_wavelet

    y = series.dropna().astype(float).to_numpy()
    if y.size < 16:
        return NullResult(real_band_power=np.nan, p_value=1.0,
                          reject_cycle=True, n_surrogates=0,
                          method="AR(1) bootstrap on wavelet band-power")

    real_wav = morlet_wavelet(pd.Series(y), lo_years, hi_years,
                               samples_per_year=samples_per_year)
    bp = real_wav.get("band_power_series")
    real_power = float(np.nansum(bp.to_numpy())) if bp is not None else 0.0
    if real_power <= 0.0:
        return NullResult(real_band_power=0.0, p_value=1.0,
                          reject_cycle=True, n_surrogates=0,
                          method="AR(1) bootstrap on wavelet band-power")

    phi, sigma, mu = _fit_ar1(y)
    rng = np.random.default_rng(seed)
    n_geq = 0
    for _ in range(n_surrogates):
        surrogate = _simulate_ar1(phi, sigma, mu, y.size, rng)
        surr_wav = morlet_wavelet(pd.Series(surrogate), lo_years, hi_years,
                                   samples_per_year=samples_per_year)
        surr_bp = surr_wav.get("band_power_series")
        surr_power = float(np.nansum(surr_bp.to_numpy())) if surr_bp is not None else 0.0
        if surr_power >= real_power:
            n_geq += 1
    p_value = (n_geq + 1) / (n_surrogates + 1)
    return NullResult(real_band_power=real_power, p_value=p_value,
                      reject_cycle=p_value >= alpha, n_surrogates=n_surrogates,
                      method="AR(1) bootstrap on wavelet band-power")


def dual_null(series: pd.Series, lo_years: float, hi_years: float,
              samples_per_year: float = 1.0,
              n_surrogates: int = 1000, alpha: float = 0.05,
              seed: int = 0) -> dict:
    """Run both AR(1) and phase-scrambling nulls; return combined verdict.

    A cell passes Gate 1 only when **both** nulls reject. Returns a dict
    with the two NullResult, the conservative ``reject_cycle`` flag
    (True iff EITHER null fails — strict dual-null protocol), and the
    larger of the two p-values as ``p_value`` (the bottleneck).
    """
    ar1 = ar1_bootstrap_null(series, lo_years, hi_years, samples_per_year,
                              n_surrogates, alpha, seed)
    psr = phase_scramble_null(series, lo_years, hi_years, samples_per_year,
                               n_surrogates, alpha, seed + 1)
    reject = ar1.reject_cycle or psr.reject_cycle
    return {
        "ar1": ar1,
        "phase_scramble": psr,
        "reject_cycle": reject,
        "p_value": max(ar1.p_value, psr.p_value),
        "binding_null": "ar1" if ar1.p_value >= psr.p_value else "phase_scramble",
    }
