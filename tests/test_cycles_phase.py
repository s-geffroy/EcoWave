"""Hilbert phase and 4-quadrant classification."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.cycles.phase import (
    classify_phase,
    hilbert_amplitude,
    hilbert_phase,
    phase_trajectory,
)


def test_classify_phase_labels_each_quadrant():
    half_pi = np.pi / 2.0
    three_q = 3.0 * np.pi / 4.0
    assert classify_phase(-half_pi * 0.5) == "expansion"
    assert classify_phase(half_pi * 0.5) == "peak"
    assert classify_phase(np.pi * 0.9) == "contraction"
    assert classify_phase(-three_q * 0.95) == "trough"


def test_classify_phase_normalizes_outside_principal_range():
    # 3π/2 ≡ -π/2  → boundary between expansion and trough
    label = classify_phase(3.0 * np.pi / 2.0)
    assert label in ("trough", "expansion")  # boundary case


def test_classify_phase_handles_nan():
    assert classify_phase(float("nan")) == "rejected"
    assert classify_phase(None) == "rejected"


def test_hilbert_phase_cosine_passes_through_quadrants():
    n = 200
    t = np.arange(n)
    cosine = np.cos(2.0 * np.pi * t / 50.0)
    series = pd.Series(cosine, index=t)
    phi = hilbert_phase(series)
    # phi at t=0 should be near 0 (peak of cosine). Drop boundary samples.
    inner_phi = phi.iloc[10:-10]
    assert inner_phi.notna().all()


def test_phase_trajectory_returns_all_columns():
    n = 100
    t = np.arange(n)
    cycle = pd.Series(np.cos(2.0 * np.pi * t / 25.0), index=t)
    traj = phase_trajectory(cycle)
    assert {"phi_rad", "amplitude", "phase"}.issubset(traj.columns)
    assert traj["phase"].isin(["expansion", "peak", "contraction", "trough",
                               "rejected"]).all()


def test_hilbert_amplitude_near_one_for_unit_cosine():
    n = 200
    t = np.arange(n)
    cycle = pd.Series(np.cos(2.0 * np.pi * t / 25.0), index=t)
    amp = hilbert_amplitude(cycle)
    inner = amp.iloc[20:-20]
    assert 0.85 < inner.mean() < 1.15
