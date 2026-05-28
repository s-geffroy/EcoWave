from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.scoring.elliott_on_composite import detect_elliott_waves, waves_to_frame


def _months(n: int, start: str = "2005-01") -> list[str]:
    return [str(d.to_period("M")) for d in pd.date_range(start, periods=n, freq="MS")]


def _synthetic_impulse(amplitudes: tuple[float, ...] = (15, -5, 25, -8, 18),
                       leg_lengths: tuple[int, ...] = (5, 4, 7, 4, 6),
                       baseline: float = 20.0,
                       lead: int = 3, trail: int = 3) -> pd.Series:
    """Build a piecewise-linear 5-wave Elliott impulse with lead/trail context.

    `lead` months of mild approach (so T0 is a true interior trough) and
    `trail` months of mild decline (so P5 is a true interior peak) ensure
    ``scipy.signal.find_peaks`` can detect every pivot.
    """
    pivot_values = [baseline]
    for a in amplitudes:
        pivot_values.append(pivot_values[-1] + a)
    values: list[float] = []
    # Lead-in: mild slope down to T0 (baseline + 2 -> baseline) so T0 is a real trough.
    for v in np.linspace(baseline + 2, baseline, lead, endpoint=False):
        values.append(float(v))
    # Pivot points are placed at the start of each leg; the last leg also emits
    # its endpoint so P5 sits explicitly in the series.
    for i, length in enumerate(leg_lengths):
        for v in np.linspace(pivot_values[i], pivot_values[i + 1], length, endpoint=False):
            values.append(float(v))
    values.append(pivot_values[-1])
    # Trail: mild decline after P5 so it is a real peak with neighbours on both sides.
    last_value = pivot_values[-1]
    for v in np.linspace(last_value - 1, last_value - trail, trail):
        values.append(float(v))
    months = _months(len(values))
    return pd.Series(values, index=months, dtype=float)


def test_detect_returns_empty_for_short_series():
    s = pd.Series([1.0, 2.0, 3.0], index=_months(3))
    d = pd.Series([0, 1, 2], index=_months(3))
    assert detect_elliott_waves(s, d) == []


def test_detect_finds_canonical_five_wave_impulse():
    intensity = _synthetic_impulse()
    diffusion = pd.Series(4, index=intensity.index)
    waves = detect_elliott_waves(intensity, diffusion, threshold=3, min_distance=2)
    labels = [w.label for w in waves]
    assert labels[:5] == ["1", "2", "3", "4", "5"]
    assert all(w.confirmed for w in waves[:5])


def test_diffusion_below_threshold_marks_wave_unconfirmed():
    intensity = _synthetic_impulse()
    diffusion = pd.Series(1, index=intensity.index)
    waves = detect_elliott_waves(intensity, diffusion, threshold=3, min_distance=2)
    assert waves, "expected an impulse to be detected on the synthetic series"
    assert all(not w.confirmed for w in waves)


def test_wave3_shortest_rejected():
    # Wave 3 is the smallest impulse leg -> canonical Elliott constraint violated.
    intensity = _synthetic_impulse(amplitudes=(20, -5, 5, -3, 18),
                                   leg_lengths=(5, 4, 4, 4, 6))
    diffusion = pd.Series(4, index=intensity.index)
    waves = detect_elliott_waves(intensity, diffusion, min_distance=2)
    assert waves == []


def test_wave4_overlap_rejected():
    # Wave 4 retraces below the peak of wave 1 -> overlap.
    intensity = _synthetic_impulse(amplitudes=(10, -5, 25, -27, 18),
                                   leg_lengths=(5, 4, 7, 4, 6))
    diffusion = pd.Series(4, index=intensity.index)
    waves = detect_elliott_waves(intensity, diffusion, min_distance=2)
    assert waves == []


def test_waves_to_frame_columns():
    intensity = _synthetic_impulse()
    diffusion = pd.Series(4, index=intensity.index)
    waves = detect_elliott_waves(intensity, diffusion, min_distance=2)
    df = waves_to_frame(waves)
    expected = {"label", "direction", "start_month", "end_month",
                "start_value", "end_value", "diffusion_at_end", "confirmed"}
    assert expected.issubset(df.columns)
