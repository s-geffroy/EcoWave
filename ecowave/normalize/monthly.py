from __future__ import annotations

import pandas as pd


VARIABLE_CODES = [
    "E1","E2","E3","E4","E5","E6",
    "D1","D2","D3",
    "S1","S2",
    "L1","L2",
    "I1","I2",
]


def month_range(start: str, end: str) -> list[str]:
    return [d.strftime("%Y-%m") for d in pd.period_range(start=start, end=end, freq="M")]


def build_empty_monthly_panel(start: str, end: str) -> pd.DataFrame:
    rows = []
    for month in month_range(start, end):
        for code in VARIABLE_CODES:
            rows.append({
                "month": month,
                "variable_code": code,
                "raw_value": None,
                "z_precrisis": None,
                "stress_precrisis": None,
                "z_structural": None,
                "stress_structural": None,
                "status": "missing",
                "source": None,
                "confidence": None,
                "notes": "skeleton placeholder; real ingestion required",
            })
    return pd.DataFrame(rows)


def daily_to_monthly(df: pd.DataFrame, value_col: str = "value") -> pd.DataFrame:
    work = df.copy()
    work["date"] = pd.to_datetime(work["date"])
    work["month"] = work["date"].dt.to_period("M").astype(str)
    return work.groupby("month", as_index=False).agg(
        monthly_avg=(value_col, "mean"),
        monthly_max=(value_col, "max"),
        monthly_min=(value_col, "min"),
        monthly_last=(value_col, "last"),
    )
