from __future__ import annotations

import pandas as pd


def aggregate_curve_scores(panel: pd.DataFrame) -> pd.DataFrame:
    """Aggregate variable stress scores into curve-level scores by month.

    Curve is derived from the first character of variable_code (E/D/S/L/I).
    A curve-month is 'scored' if at least one variable is 'available'.
    """
    work = panel.copy()
    if "curve" not in work.columns:
        work["curve"] = work["variable_code"].str[0]

    rows = []
    for (month, curve), group in work.groupby(["month", "curve"]):
        available = group["status"] == "available"
        rows.append({
            "month": month,
            "curve": curve,
            "stress_precrisis": group.loc[available, "stress_precrisis"].mean()
            if available.any() else None,
            "stress_structural": group.loc[available, "stress_structural"].mean()
            if available.any() else None,
            "variables_available": int(available.sum()),
            "variables_expected": len(group),
            "status": "scored" if available.any() else "blocked",
            "notes": "",
        })
    return pd.DataFrame(rows)
