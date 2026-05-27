from __future__ import annotations

import pandas as pd

from ecowave.ingest.manifest import IngestionSpec, Manifest
from ecowave.normalize.monthly import month_range
from ecowave.normalize.orientation import orient_stress
from ecowave.normalize.percentile import percentile_stress
from ecowave.normalize.zscore import zscore

PANEL_COLUMNS = [
    "month", "variable_code", "raw_value", "z_precrisis", "stress_precrisis",
    "z_structural", "stress_structural", "status", "source", "confidence", "notes",
]


def apply_value_transform(series: pd.Series, transform: str) -> pd.Series:
    """Return the stress-relevant feature derived from a month-indexed raw Series."""
    s = series.sort_index()
    if transform == "level":
        return s
    if transform == "drawdown":
        return (s / s.cummax() - 1.0) * 100.0
    if transform == "pct_change":
        return s.pct_change() * 100.0
    if transform == "infl_dev":
        return s.pct_change(12) * 100.0 - 2.0
    raise ValueError(f"Unknown value_transform: {transform}")


def _window(series: pd.Series, start: str, end: str) -> pd.Series:
    idx = series.index.astype(str)
    return series[(idx >= start) & (idx <= end)]


def build_variable_rows(spec: IngestionSpec, monthly_series: pd.Series, manifest: Manifest,
                        source_label: str) -> list[dict]:
    panel_months = month_range(manifest.panel_start, manifest.panel_end)
    monthly_series = monthly_series.sort_index()

    feature = apply_value_transform(monthly_series, spec.value_transform)
    oriented = orient_stress(feature, spec.stress_orientation)

    pre_ref = _window(oriented, manifest.precrisis.start, manifest.precrisis.end).dropna()
    str_ref = _window(oriented, manifest.structural.start, manifest.structural.end).dropna()

    panel_oriented = oriented.reindex(panel_months)
    raw_panel = monthly_series.reindex(panel_months)

    z_pre = zscore(panel_oriented, pre_ref)
    z_str = zscore(panel_oriented, str_ref)
    stress_pre = percentile_stress(panel_oriented, pre_ref)
    stress_str = percentile_stress(panel_oriented, str_ref)

    rows: list[dict] = []
    for month in panel_months:
        raw_value = raw_panel.get(month)
        sp = stress_pre.get(month)
        ss = stress_str.get(month)
        if raw_value is None or pd.isna(raw_value):
            status, note = "missing", f"no monthly value for {month}"
        elif (sp is None or pd.isna(sp)) and (ss is None or pd.isna(ss)):
            status, note = "partial", "value present but reference window unavailable (no normalization)"
        else:
            status, note = "available", f"transform={spec.value_transform}; orientation={spec.stress_orientation}"
        rows.append({
            "month": month,
            "variable_code": spec.variable_code,
            "raw_value": None if raw_value is None or pd.isna(raw_value) else float(raw_value),
            "z_precrisis": _clean(z_pre.get(month)),
            "stress_precrisis": _clean(sp),
            "z_structural": _clean(z_str.get(month)),
            "stress_structural": _clean(ss),
            "status": status,
            "source": source_label,
            "confidence": spec.confidence,
            "notes": note,
        })
    return rows


def build_missing_rows(variable_code: str, reason: str, manifest: Manifest) -> list[dict]:
    return [{
        "month": month,
        "variable_code": variable_code,
        "raw_value": None,
        "z_precrisis": None,
        "stress_precrisis": None,
        "z_structural": None,
        "stress_structural": None,
        "status": "missing",
        "source": None,
        "confidence": None,
        "notes": reason,
    } for month in month_range(manifest.panel_start, manifest.panel_end)]


def _clean(value):
    if value is None or pd.isna(value):
        return None
    return float(value)
