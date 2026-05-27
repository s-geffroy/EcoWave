from __future__ import annotations

import pandas as pd


def to_month(date_like: str) -> str:
    return pd.Period(date_like, freq="M").strftime("%Y-%m")
