from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WaveCandidate:
    model_code: str
    wave_label: str
    start_month: str
    end_month: str
    supporting_curves: list[str]
    robustness_score: str
    notes: str
