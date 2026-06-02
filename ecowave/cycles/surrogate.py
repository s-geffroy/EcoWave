"""AR(1) bootstrap null test — Gate 1 of the CPV protocol.

For each (group, indicator, band), the band-power of the band-passed series
must exceed the (1-α) quantile of band-power computed from B simulated AR(1)
red-noise paths with the same mean / variance / persistence as the input.

Source: Torrence & Compo (1998), "A Practical Guide to Wavelet Analysis";
Grinsted et al. (2004), "Application of the cross wavelet transform". Both
use AR(1) as the canonical null because pure red noise has no preferred
frequency — a band-power that rises above red noise is evidence of an actual
cyclic component at that frequency.

Note on phase-scramble (Schreiber & Schmitz 2000) — the Theiler surrogate
preserves the empirical Fourier amplitudes exactly. Testing CF band-power
against a phase-scrambled surrogate is therefore degenerate by Parseval:
the surrogate band-power equals the real band-power. The phase-scramble
null here tests a different statistic — the **stability of the instantaneous
frequency** inside the band — which is destroyed by phase randomisation
even when the spectrum is preserved. This corresponds to the
"coherence" interpretation of Null~2 in the companion paper.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.signal import hilbert as _hilbert

from ecowave.cycles.decompose import cf_bandpass
from ecowave.cycles.surrogate_generators import (
    ar1_surrogate_series,
    fit_ar1 as _fit_ar1,
    phase_scramble_surrogate_series,
    simulate_ar1 as _simulate_ar1,
)


def phase_coherence_in_band(series: pd.Series, lo_years: float,
                             hi_years: float,
                             samples_per_year: float = 1.0) -> float:
    """Stability of the instantaneous frequency inside the canonical band.

    Bandpass-filters ``series`` to the band ``[lo_years, hi_years]``, takes
    the Hilbert transform to obtain the analytic signal, computes the
    instantaneous frequency from the unwrapped phase, and returns a
    coherence score in [0, 1]:

    The coherence score ``C`` is ``1 / (1 + CV(f_t))``

    where ``CV`` is the coefficient of variation (std / mean) of the
    instantaneous frequency ``f_t = (1/2π)·dφ/dt``. A pure cosine yields
    ``CV → 0`` and ``C → 1``; uniformly-distributed phase noise yields
    ``CV ≫ 1`` and ``C → 0``.

    The score is the test statistic of :func:`phase_scramble_null` —
    phase-randomised surrogates have a destabilised instantaneous
    frequency by construction, even when the spectrum is preserved, so
    the score distinguishes a true cyclical band from a noisy spectrum
    that happens to peak there.
    """
    y = series.dropna().astype(float).to_numpy()
    if y.size < 16:
        return 0.0
    bp = cf_bandpass(pd.Series(y), lo_years, hi_years,
                     samples_per_year=samples_per_year).dropna().to_numpy()
    if bp.size < 4:
        return 0.0
    analytic = _hilbert(bp)
    phase = np.unwrap(np.angle(analytic))
    if phase.size < 2:
        return 0.0
    inst_freq = np.diff(phase) / (2.0 * np.pi)
    mean_f = np.abs(np.mean(inst_freq))
    std_f = float(np.std(inst_freq))
    if mean_f < 1e-12:
        return 0.0
    cv = std_f / mean_f
    return 1.0 / (1.0 + cv)


@dataclass(frozen=True)
class NullResult:
    real_band_power: float
    p_value: float
    reject_cycle: bool
    n_surrogates: int
    method: str = "AR(1) bootstrap on CF band-power"

    def __bool__(self) -> bool:
        return not self.reject_cycle


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

    n_geq = 0
    for surrogate in ar1_surrogate_series(y, n_surrogates, seed):
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
    """Phase-randomised Fourier surrogate (Theiler et al. 1992) — coherence test.

    Tests whether the **stability of the instantaneous frequency** inside
    the canonical band is greater than expected under a phase-randomised
    surrogate that preserves the empirical Fourier amplitudes exactly.

    The test statistic is :func:`phase_coherence_in_band`. It is *not*
    band-power: by Parseval's theorem the band-power of any
    amplitude-preserving phase randomisation equals the band-power of the
    original series, so band-power against this surrogate is degenerate
    (cf. Schreiber & Schmitz 2000 for the canonical discussion). The
    coherence-based statistic, by contrast, is destroyed by phase
    randomisation even when the spectrum is preserved: a stable
    instantaneous frequency is a phase-dependent property.

    The AR(1) null (:func:`ar1_bootstrap_null`) tests cycle *existence*
    against red noise. This null tests phase *coherence* — they are
    complementary aspects of the data and are reported separately by
    :func:`dual_null`.

    Reference: Theiler et al. (1992) Physica D 58, 77–94 ; the limitation
    of band-power against phase-randomised surrogates is discussed in
    Schreiber & Schmitz (2000) Physica D 142, 346–382.
    """
    y = series.dropna().astype(float).to_numpy()
    if y.size < 16:
        return NullResult(real_band_power=np.nan, p_value=1.0,
                          reject_cycle=True, n_surrogates=0,
                          method="phase-scramble coherence (Theiler 1992)")

    real_coherence = phase_coherence_in_band(pd.Series(y), lo_years, hi_years,
                                              samples_per_year=samples_per_year)
    if real_coherence <= 0.0:
        return NullResult(real_band_power=0.0, p_value=1.0,
                          reject_cycle=True, n_surrogates=0,
                          method="phase-scramble coherence (Theiler 1992)")

    # FFT once; scramble phases for each surrogate. Conjugate symmetry
    # preserves the inverse transform real-valued.
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
        surr_coherence = phase_coherence_in_band(pd.Series(surrogate),
                                                  lo_years, hi_years,
                                                  samples_per_year=samples_per_year)
        if surr_coherence >= real_coherence:
            n_geq += 1
    p_value = (n_geq + 1) / (n_surrogates + 1)
    return NullResult(real_band_power=real_coherence, p_value=p_value,
                      reject_cycle=p_value >= alpha, n_surrogates=n_surrogates,
                      method="phase-scramble coherence (Theiler 1992)")


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
    """Run both AR(1) and phase-scrambling nulls; return both verdicts.

    Empirical calibration (see ``scripts/calibrate_dual_null.py`` and
    ``reports/calibration_v1.json``) shows that the AR(1) bootstrap is
    highly powerful against AR(1)+cosine alternatives and is the
    load-bearing test for cycle *existence*. The phase-scramble
    coherence null is reported alongside as a complementary
    *coherence* diagnostic — it tests a different property (stability
    of the instantaneous frequency under spectrum preservation), and
    is informative on broadband non-Gaussian data but degenerate on
    clean single-frequency Gaussian alternatives.

    The returned dict contains both NullResult and two booleans:

    - ``reject_cycle``  (the existence verdict, equal to the AR(1)
      null's ``reject_cycle`` flag);
    - ``reject_existence_and_coherence`` (the strict conjunction —
      cell only admitted if BOTH nulls pass; useful as a robustness
      check but should not be used as the primary gate because the
      coherence statistic is conservative against simple Gaussian
      cycles).
    """
    ar1 = ar1_bootstrap_null(series, lo_years, hi_years, samples_per_year,
                              n_surrogates, alpha, seed)
    psr = phase_scramble_null(series, lo_years, hi_years, samples_per_year,
                               n_surrogates, alpha, seed + 1)
    return {
        "ar1": ar1,
        "phase_scramble": psr,
        "reject_cycle": ar1.reject_cycle,
        "reject_existence_and_coherence": ar1.reject_cycle or psr.reject_cycle,
        "p_value": ar1.p_value,
        "binding_null": "ar1",
    }
