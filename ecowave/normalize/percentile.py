from __future__ import annotations

import pandas as pd
import numpy as np


def percentile_stress(series: pd.Series, reference: pd.Series) -> pd.Series:
    ref = reference.dropna().sort_values().to_numpy()
    if len(ref) == 0:
        return pd.Series([None] * len(series), index=series.index)
    values = []
    for value in series:
        if pd.isna(value):
            values.append(None)
        else:
            values.append(float(np.searchsorted(ref, value, side="right") / len(ref) * 100.0))
    return pd.Series(values, index=series.index)
