from __future__ import annotations

import pandas as pd


def orient_stress(series: pd.Series, orientation: str) -> pd.Series:
    if orientation == "higher_is_stress":
        return series
    if orientation in {"lower_growth_is_stress", "contraction_is_stress"}:
        return -series
    if orientation in {"drawdown_is_stress", "negative_tone_is_stress"}:
        return -series
    if orientation in {"extreme_deviation_is_stress", "extreme_move_is_stress"}:
        return series.abs()
    raise ValueError(f"Unknown stress orientation: {orientation}")
