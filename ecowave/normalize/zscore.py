from __future__ import annotations

import pandas as pd


def zscore(series: pd.Series, reference: pd.Series) -> pd.Series:
    mean = reference.mean(skipna=True)
    std = reference.std(skipna=True)
    if std == 0 or pd.isna(std):
        return pd.Series([None] * len(series), index=series.index)
    return (series - mean) / std
