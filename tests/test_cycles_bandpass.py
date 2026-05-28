"""CF band-pass and Morlet wavelet tests on synthetic signals."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.cycles.decompose import cf_bandpass, morlet_wavelet


def _build_two_cycle_signal(n_years: int = 200, seed: int = 0) -> pd.Series:
    rng = np.random.default_rng(seed)
    t = np.arange(n_years)
    juglar = np.sin(2.0 * np.pi * t / 8.0)
    kondratieff = np.sin(2.0 * np.pi * t / 50.0)
    noise = rng.normal(scale=0.2, size=n_years)
    return pd.Series(juglar + kondratieff + noise, index=t)


def test_cf_bandpass_recovers_juglar_component():
    signal = _build_two_cycle_signal()
    juglar_only = pd.Series(np.sin(2.0 * np.pi * signal.index.to_numpy() / 8.0),
                             index=signal.index)
    cycle = cf_bandpass(signal, lo_years=7, hi_years=11, samples_per_year=1.0)
    inner = signal.index[20:-20]  # avoid endpoint effects
    corr = np.corrcoef(cycle.loc[inner], juglar_only.loc[inner])[0, 1]
    assert corr > 0.85, f"CF should recover the 8y Juglar (corr={corr:.2f})"


def test_cf_bandpass_suppresses_kondratieff():
    signal = _build_two_cycle_signal()
    kondratieff_only = pd.Series(np.sin(2.0 * np.pi * signal.index.to_numpy() / 50.0),
                                  index=signal.index)
    cycle = cf_bandpass(signal, lo_years=7, hi_years=11, samples_per_year=1.0)
    inner = signal.index[20:-20]
    corr = np.corrcoef(cycle.loc[inner], kondratieff_only.loc[inner])[0, 1]
    assert abs(corr) < 0.4, f"Juglar band should not pass Kondratieff (corr={corr:.2f})"


def test_cf_bandpass_kondratieff_band_passes_kondratieff():
    signal = _build_two_cycle_signal()
    kondratieff_only = pd.Series(np.sin(2.0 * np.pi * signal.index.to_numpy() / 50.0),
                                  index=signal.index)
    cycle = cf_bandpass(signal, lo_years=40, hi_years=60, samples_per_year=1.0)
    inner = signal.index[40:-40]
    corr = np.corrcoef(cycle.loc[inner], kondratieff_only.loc[inner])[0, 1]
    assert corr > 0.85, f"K-band should recover Kondratieff (corr={corr:.2f})"


def test_cf_bandpass_handles_too_short_series():
    short = pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2])
    result = cf_bandpass(short, lo_years=7, hi_years=11)
    assert result.isna().all()


def test_morlet_wavelet_returns_band_power_for_inband_signal():
    signal = _build_two_cycle_signal()
    out = morlet_wavelet(signal, lo_years=7, hi_years=11, samples_per_year=1.0)
    assert out["power"].size > 0
    assert "band_power_series" in out
    # Inner samples should have non-NaN band power.
    inner = out["band_power_series"].iloc[20:-20]
    assert inner.notna().any()


def test_morlet_wavelet_handles_empty_input():
    empty = pd.Series(dtype=float)
    out = morlet_wavelet(empty, lo_years=7, hi_years=11)
    assert out["power"].size == 0
