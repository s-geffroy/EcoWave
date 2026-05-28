"""Detect a 5-wave Elliott impulse + optional 3-wave correction on the
synthetic intensity index, with confirmation by the diffusion index.

The detector is intentionally simple and falsifiable:

1. Find local extrema (pivots) via scipy.signal.find_peaks on the smoothed
   intensity series and its negation.
2. Enumerate sequences of six alternating trough-peak pivots
   ``T0 P1 T2 P3 T4 P5`` and keep those that pass the canonical Elliott
   constraints (no overlap with wave 1, wave 3 not the shortest, wave 2 doesn't
   undercut the impulse start).
3. Pick the candidate with the largest total amplitude
   ``P5_value − T0_value``.
4. Confirm each wave by checking ``diffusion >= threshold`` at the terminal
   pivot (default 3).
5. If at least three further pivots are available after ``P5``, label them as
   the A/B/C correction and apply the same confirmation.

The output is a list of :class:`Wave` records. Empty list = no impulse passes
the constraints.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
from scipy.signal import find_peaks

PivotType = Literal["peak", "trough"]
Direction = Literal["up", "down"]


@dataclass(frozen=True)
class Wave:
    label: str
    direction: Direction
    start_month: str
    end_month: str
    start_value: float
    end_value: float
    diffusion_at_end: int
    confirmed: bool

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "direction": self.direction,
            "start_month": self.start_month,
            "end_month": self.end_month,
            "start_value": self.start_value,
            "end_value": self.end_value,
            "diffusion_at_end": self.diffusion_at_end,
            "confirmed": self.confirmed,
        }


def _find_pivots(series: pd.Series, min_distance: int) -> list[tuple[int, PivotType, float]]:
    y = series.to_numpy(dtype=float)
    peak_idx, _ = find_peaks(y, distance=min_distance)
    trough_idx, _ = find_peaks(-y, distance=min_distance)
    pivots: list[tuple[int, PivotType, float]] = []
    pivots.extend((int(i), "peak", float(y[i])) for i in peak_idx)
    pivots.extend((int(i), "trough", float(y[i])) for i in trough_idx)
    pivots.sort(key=lambda x: x[0])
    return pivots


def _passes_impulse_constraints(seq: list[tuple[int, PivotType, float]]) -> bool:
    """Sequence is T0 P1 T2 P3 T4 P5. Apply canonical Elliott constraints."""
    t0, p1, t2, p3, t4, p5 = (s[2] for s in seq)
    # Wave 2 does not retrace below the impulse start (T0).
    if t2 <= t0:
        return False
    # Wave 4 does not overlap wave 1 (T4 stays above P1).
    if t4 < p1:
        return False
    # Wave 3 is not the shortest of waves 1, 3, 5.
    w1 = p1 - t0
    w3 = p3 - t2
    w5 = p5 - t4
    if w3 <= 0 or w1 <= 0 or w5 <= 0:
        return False
    if w3 < w1 and w3 < w5:
        return False
    # Wave 5 makes a new high above P3.
    if p5 <= p3:
        return False
    return True


def _build_wave(label: str, direction: Direction,
                start_pivot: tuple[int, PivotType, float],
                end_pivot: tuple[int, PivotType, float],
                months: list[str], diffusion: pd.Series, threshold: int) -> Wave:
    end_month = months[end_pivot[0]]
    diff_at_end = int(diffusion.loc[end_month]) if end_month in diffusion.index else 0
    confirmed = diff_at_end >= threshold
    return Wave(
        label=label, direction=direction,
        start_month=months[start_pivot[0]], end_month=end_month,
        start_value=float(start_pivot[2]), end_value=float(end_pivot[2]),
        diffusion_at_end=diff_at_end, confirmed=confirmed,
    )


def detect_elliott_waves(intensity: pd.Series, diffusion: pd.Series,
                         threshold: int = 3, min_distance: int = 3) -> list[Wave]:
    """Detect the dominant 5-wave impulse on the intensity series.

    Parameters
    ----------
    intensity : pd.Series
        Smoothed intensity series indexed by ``YYYY-MM`` strings.
    diffusion : pd.Series
        Aligned diffusion series (int counts 0..5).
    threshold : int
        Minimum diffusion required to confirm a wave's terminal pivot.
    min_distance : int
        Minimum months between adjacent pivots, fed to ``find_peaks``.
    """
    clean = intensity.dropna()
    if len(clean) < 12:
        return []
    months = list(clean.index.astype(str))
    pivots = _find_pivots(clean, min_distance=min_distance)
    if len(pivots) < 6:
        return []

    best: list[tuple[int, PivotType, float]] | None = None
    best_score = 0.0
    for start in range(len(pivots) - 5):
        seq = pivots[start:start + 6]
        types = [p[1] for p in seq]
        if types != ["trough", "peak", "trough", "peak", "trough", "peak"]:
            continue
        if not _passes_impulse_constraints(seq):
            continue
        score = seq[-1][2] - seq[0][2]
        if score > best_score:
            best_score = score
            best = seq

    if best is None:
        return []

    diffusion_aligned = diffusion.reindex(intensity.index)
    impulse_legs = [
        ("1", "up", best[0], best[1]),
        ("2", "down", best[1], best[2]),
        ("3", "up", best[2], best[3]),
        ("4", "down", best[3], best[4]),
        ("5", "up", best[4], best[5]),
    ]
    waves: list[Wave] = [
        _build_wave(label, direction, start, end, months, diffusion_aligned, threshold)
        for label, direction, start, end in impulse_legs
    ]

    after = [p for p in pivots if p[0] > best[5][0]]
    if len(after) >= 3 and after[0][1] == "trough" and after[1][1] == "peak" and after[2][1] == "trough":
        correction_legs = [
            ("A", "down", best[5], after[0]),
            ("B", "up", after[0], after[1]),
            ("C", "down", after[1], after[2]),
        ]
        waves.extend(
            _build_wave(label, direction, start, end, months, diffusion_aligned, threshold)
            for label, direction, start, end in correction_legs
        )
    return waves


def waves_to_frame(waves: list[Wave]) -> pd.DataFrame:
    if not waves:
        return pd.DataFrame(columns=[
            "label", "direction", "start_month", "end_month",
            "start_value", "end_value", "diffusion_at_end", "confirmed",
        ])
    return pd.DataFrame([w.to_dict() for w in waves])
