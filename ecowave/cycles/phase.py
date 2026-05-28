"""Hilbert-transform instantaneous phase and 4-quadrant phase labelling.

Cosine convention: a sample is at the cycle's peak when its instantaneous
phase φ = 0 (positive crest). The four labels are pre-registered:

  φ ∈ [-π/2,    0  )  → expansion  (rising toward peak)
  φ ∈ [   0, π/2  )  → peak       (just past, slowing)
  φ ∈ [ π/2,    π  ] ∪ [-π, -3π/4)  → contraction (falling)
  φ ∈ [-3π/4, -π/2)  → trough     (just bottomed)
"""
from __future__ import annotations

import numpy as np
import pandas as pd

PHASE_LABELS = ("expansion", "peak", "contraction", "trough")


def hilbert_phase(cycle: pd.Series) -> pd.Series:
    """Instantaneous phase φ ∈ (-π, π] of a band-passed cycle, via Hilbert.

    NaN values are forward-filled before transform and re-introduced as NaN
    in the output to preserve the index alignment.
    """
    from scipy.signal import hilbert

    y = cycle.astype(float).to_numpy()
    mask_nan = np.isnan(y)
    if mask_nan.all() or y.size < 2:
        return pd.Series(np.nan, index=cycle.index, name="phi_rad")
    if mask_nan.any():
        # Replace NaNs with a centered constant so the FFT doesn't blow up.
        y = pd.Series(y).interpolate(limit_direction="both").to_numpy()
    analytic = hilbert(y)
    phi = np.angle(analytic)
    phi[mask_nan] = np.nan
    return pd.Series(phi, index=cycle.index, name="phi_rad")


def classify_phase(phi_rad: float) -> str:
    """Map instantaneous phase to one of the 4 cycle phases."""
    if phi_rad is None or (isinstance(phi_rad, float) and np.isnan(phi_rad)):
        return "rejected"
    # Normalize to (-π, π]
    phi = ((phi_rad + np.pi) % (2.0 * np.pi)) - np.pi
    half_pi = np.pi / 2.0
    three_q = 3.0 * np.pi / 4.0
    if -half_pi <= phi < 0.0:
        return "expansion"
    if 0.0 <= phi < half_pi:
        return "peak"
    if -three_q <= phi < -half_pi:
        return "trough"
    return "contraction"


def hilbert_amplitude(cycle: pd.Series) -> pd.Series:
    """Instantaneous amplitude |a(t)| of the analytic signal."""
    from scipy.signal import hilbert

    y = cycle.astype(float).to_numpy()
    if np.isnan(y).all() or y.size < 2:
        return pd.Series(np.nan, index=cycle.index, name="amplitude")
    y2 = pd.Series(y).interpolate(limit_direction="both").to_numpy()
    amp = np.abs(hilbert(y2))
    return pd.Series(amp, index=cycle.index, name="amplitude")


def phase_trajectory(cycle: pd.Series) -> pd.DataFrame:
    """Build a (date, phi, amplitude, phase_label) trajectory for a filtered cycle."""
    phi = hilbert_phase(cycle)
    amp = hilbert_amplitude(cycle)
    labels = [classify_phase(p) for p in phi.values]
    return pd.DataFrame({
        "phi_rad": phi.values,
        "amplitude": amp.values,
        "phase": labels,
    }, index=cycle.index)


def trend_from_phase(phi_rad: float) -> str:
    """Local trend direction from φ. Rising when φ ∈ (-π/2, π/2), falling otherwise.

    Cosine convention: derivative of cos(φ) is -sin(φ); when sin(φ) < 0 the
    series is rising. φ ∈ (-π, 0) → sin < 0 → rising; φ ∈ (0, π) → sin > 0 →
    falling. We use the open intervals so the extremum samples themselves
    (φ ≈ 0 or ±π) return a neutral label.
    """
    if phi_rad is None or (isinstance(phi_rad, float) and np.isnan(phi_rad)):
        return "—"
    phi = ((phi_rad + np.pi) % (2.0 * np.pi)) - np.pi
    if -np.pi / 2.0 < phi < 0.0:
        return "rising"
    if 0.0 < phi < np.pi / 2.0:
        return "rising (post-peak)"
    if np.pi / 2.0 <= phi <= np.pi or -np.pi <= phi < -3.0 * np.pi / 4.0:
        return "falling"
    if -3.0 * np.pi / 4.0 <= phi <= -np.pi / 2.0:
        return "rising (post-trough)"
    return "—"


def forecast_next_extremum(phi_rad: float, period_years: float) -> dict:
    """Estimate time-to-next-peak and time-to-next-trough from instantaneous φ.

    Cosine convention: peaks are at φ = 0, troughs at φ = ±π. Phase advances
    at rate ω = 2π / period (radians per year). Given current φ, the time
    until φ reaches the target is::

        Δt_peak   = ((0 - φ) mod 2π) / ω
        Δt_trough = ((π - φ) mod 2π) / ω

    Returns a dict with both ETAs (in years), the closer-of-the-two as
    ``next_kind`` ("max" or "min") and ``next_eta_years``.
    """
    if phi_rad is None or (isinstance(phi_rad, float) and np.isnan(phi_rad)):
        return {"eta_peak_years": None, "eta_trough_years": None,
                "next_kind": "—", "next_eta_years": None}
    if period_years <= 0:
        return {"eta_peak_years": None, "eta_trough_years": None,
                "next_kind": "—", "next_eta_years": None}
    phi = ((phi_rad + np.pi) % (2.0 * np.pi)) - np.pi
    omega = 2.0 * np.pi / period_years
    two_pi = 2.0 * np.pi
    eta_peak = ((0.0 - phi) % two_pi) / omega
    eta_trough = ((np.pi - phi) % two_pi) / omega
    if eta_peak <= eta_trough:
        return {"eta_peak_years": eta_peak, "eta_trough_years": eta_trough,
                "next_kind": "max", "next_eta_years": eta_peak}
    return {"eta_peak_years": eta_peak, "eta_trough_years": eta_trough,
            "next_kind": "min", "next_eta_years": eta_trough}
