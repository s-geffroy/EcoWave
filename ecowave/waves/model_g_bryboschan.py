"""Model G — Bry-Boschan / Harding-Pagan turning-point dating.

Deterministic, parameter-free phase dating from the canonical NBER algorithm
(Bry & Boschan 1971; Harding & Pagan 2002): turning points are local extrema
under minimal-phase-duration and minimal-cycle-duration constraints. The
resulting peaks/troughs define alternating expansion/contraction segments,
which we then refine with a peak/trough fringe to also expose ``peak`` and
``trough`` labels around the extrema.

Pre-registered rules (Harding & Pagan 2002 conventions on monthly data):
  - Minimum phase duration: 6 months
  - Minimum cycle duration: 15 months
  - Censoring: turning points within ``min_phase`` of the panel boundary are
    discarded.
  - Peak/trough fringe: 1 month either side of the extremum is labelled
    ``peak`` / ``trough``; the remaining samples between extrema are
    ``expansion`` (rising) or ``contraction`` (falling).

Model G is one of the 4 votant methods in the CPV consensus gate. It is
deterministic and exposes the cleanest rejection criterion: if no turning
point is found in the panel, the verdict is ``rejected_no_turning_point``.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.waves.model_e_markov import _equal_intensity_ma3

MIN_PHASE_MONTHS = 6
MIN_CYCLE_MONTHS = 15
FRINGE_MONTHS = 1


def _detect_turning_points(y: np.ndarray, k: int = 5) -> tuple[list[int], list[int]]:
    """Locate peaks and troughs using the symmetric k-window rule.

    A peak at i requires y[i] strictly greater than y[i-k..i-1] and y[i+1..i+k].
    Troughs symmetrically.
    """
    peaks: list[int] = []
    troughs: list[int] = []
    n = y.size
    for i in range(k, n - k):
        window_left = y[i - k:i]
        window_right = y[i + 1:i + k + 1]
        if not (np.isfinite(y[i]) and np.all(np.isfinite(window_left))
                and np.all(np.isfinite(window_right))):
            continue
        if y[i] > window_left.max() and y[i] > window_right.max():
            peaks.append(i)
        elif y[i] < window_left.min() and y[i] < window_right.min():
            troughs.append(i)
    return peaks, troughs


def _enforce_alternation(peaks: list[int], troughs: list[int]) -> list[tuple[int, str]]:
    """Merge peaks and troughs into a single alternating sequence."""
    combined = sorted([(i, "peak") for i in peaks] + [(i, "trough") for i in troughs])
    out: list[tuple[int, str]] = []
    for idx, kind in combined:
        if not out:
            out.append((idx, kind))
            continue
        if out[-1][1] == kind:
            # Consecutive same-type turning point: keep the more extreme one.
            if kind == "peak":
                out[-1] = max(out[-1], (idx, kind), key=lambda t: t[0])
            else:
                out[-1] = min(out[-1], (idx, kind), key=lambda t: t[0])
        else:
            out.append((idx, kind))
    return out


def _enforce_min_durations(turning_points: list[tuple[int, str]],
                           min_phase: int, min_cycle: int) -> list[tuple[int, str]]:
    """Drop turning points that violate min-phase or min-cycle constraints."""
    if not turning_points:
        return []
    filtered: list[tuple[int, str]] = [turning_points[0]]
    for idx, kind in turning_points[1:]:
        last_idx, _ = filtered[-1]
        if idx - last_idx < min_phase:
            continue  # too close to previous turning point
        # min_cycle: peak-to-peak or trough-to-trough must be >= min_cycle.
        same_kind = [t for t in filtered if t[1] == kind]
        if same_kind and (idx - same_kind[-1][0]) < min_cycle:
            continue
        filtered.append((idx, kind))
    return filtered


def _label_segments(n: int, turning_points: list[tuple[int, str]],
                    fringe: int) -> list[str]:
    """Build the per-sample phase label vector."""
    labels = ["expansion"] * n
    if not turning_points:
        return labels
    # Decide initial direction from first turning point: before a peak we're
    # expanding; before a trough we're contracting.
    first_idx, first_kind = turning_points[0]
    direction = "expansion" if first_kind == "peak" else "contraction"
    cursor = 0
    for idx, kind in turning_points:
        for i in range(cursor, idx):
            labels[i] = direction
        # Fringe: mark fringe samples either side of the turning point with
        # the appropriate "peak" or "trough" label.
        for j in range(max(0, idx - fringe), min(n, idx + fringe + 1)):
            labels[j] = kind
        direction = "contraction" if kind == "peak" else "expansion"
        cursor = min(n, idx + fringe + 1)
    for i in range(cursor, n):
        labels[i] = direction
    return labels


def _labels_to_phases(months: list[str],
                      labels: list[str]) -> list[tuple[str, str, str]]:
    if not months:
        return []
    phases: list[list] = [[labels[0], months[0], months[0]]]
    for i in range(1, len(months)):
        if labels[i] == phases[-1][0]:
            phases[-1][2] = months[i]
        else:
            phases.append([labels[i], months[i], months[i]])
    return [(p[0], p[1], p[2]) for p in phases]


def fit_model_g(panel: pd.DataFrame, min_phase: int = MIN_PHASE_MONTHS,
                min_cycle: int = MIN_CYCLE_MONTHS, fringe: int = FRINGE_MONTHS,
                k_window: int = 5) -> dict:
    """Fit Model G (Bry-Boschan / Harding-Pagan dating) on the MA3 intensity.

    Returns a dict matching the Model D/E contract.
    """
    intensity = _equal_intensity_ma3(panel).dropna()
    months = list(intensity.index.astype(str))
    base = {
        "name": "Bry-Boschan dating (fallback — no turning point)",
        "hypothesis": "Crisis structure is the alternation of peaks/troughs "
                      "identified by the Bry-Boschan algorithm — degenerate case.",
        "candidate_phases": [("rejected_no_turning_point", months[0], months[-1])]
                            if months else [],
        "method": "Bry-Boschan (Harding & Pagan 2002)",
        "fit_status": "fallback", "n_peaks": 0, "n_troughs": 0,
    }
    if len(intensity) < 2 * min_cycle:
        return base

    y = intensity.to_numpy(dtype=float)
    peaks, troughs = _detect_turning_points(y, k=k_window)
    turning_points = _enforce_alternation(peaks, troughs)
    turning_points = _enforce_min_durations(turning_points, min_phase=min_phase,
                                            min_cycle=min_cycle)
    if not turning_points:
        return base

    labels = _label_segments(len(months), turning_points, fringe=fringe)
    phases = _labels_to_phases(months, labels)
    return {
        "name": f"Bry-Boschan dating ({len(turning_points)} turning point(s))",
        "hypothesis": "Crisis structure is the alternation of peaks/troughs "
                      "identified by the Bry-Boschan algorithm (Harding & Pagan 2002).",
        "candidate_phases": phases,
        "method": f"Bry-Boschan k={k_window} min_phase={min_phase}m "
                  f"min_cycle={min_cycle}m",
        "fit_status": "ok",
        "n_peaks": sum(1 for _, k in turning_points if k == "peak"),
        "n_troughs": sum(1 for _, k in turning_points if k == "trough"),
    }
