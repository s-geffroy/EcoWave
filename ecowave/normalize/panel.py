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


def _normalize_one(monthly_series: pd.Series, value_transform: str, orientation: str,
                   manifest: Manifest, panel_months: list[str]) -> dict[str, pd.Series]:
    """Normalize a single series and return panel-indexed feature/z/stress columns."""
    monthly_series = monthly_series.sort_index()
    feature = apply_value_transform(monthly_series, value_transform)
    oriented = orient_stress(feature, orientation)

    pre_ref = _window(oriented, manifest.precrisis.start, manifest.precrisis.end).dropna()
    str_ref = _window(oriented, manifest.structural.start, manifest.structural.end).dropna()

    panel_oriented = oriented.reindex(panel_months)
    return {
        "raw": monthly_series.reindex(panel_months),
        "feature": feature.reindex(panel_months),
        "z_pre": zscore(panel_oriented, pre_ref),
        "z_str": zscore(panel_oriented, str_ref),
        "stress_pre": percentile_stress(panel_oriented, pre_ref),
        "stress_str": percentile_stress(panel_oriented, str_ref),
    }


def build_variable_rows(spec: IngestionSpec, monthly_series: pd.Series, manifest: Manifest,
                        source_label: str) -> list[dict]:
    panel_months = month_range(manifest.panel_start, manifest.panel_end)
    cols = _normalize_one(monthly_series, spec.value_transform, spec.stress_orientation, manifest, panel_months)

    rows: list[dict] = []
    for month in panel_months:
        raw_value = cols["raw"].get(month)
        sp = cols["stress_pre"].get(month)
        ss = cols["stress_str"].get(month)
        if raw_value is None or pd.isna(raw_value):
            status, note = "missing", f"no monthly value for {month}"
        elif (sp is None or pd.isna(sp)) and (ss is None or pd.isna(ss)):
            status, note = "partial", "value present but reference window unavailable (no normalization)"
        else:
            status, note = "available", f"transform={spec.value_transform}; orientation={spec.stress_orientation}"
        rows.append({
            "month": month,
            "variable_code": spec.variable_code,
            "raw_value": _clean(raw_value),
            "z_precrisis": _clean(cols["z_pre"].get(month)),
            "stress_precrisis": _clean(sp),
            "z_structural": _clean(cols["z_str"].get(month)),
            "stress_structural": _clean(ss),
            "status": status,
            "source": source_label,
            "confidence": spec.confidence,
            "notes": note,
        })
    return rows


def build_composite_variable_rows(spec: IngestionSpec, components: list[tuple[str, pd.Series]],
                                  manifest: Manifest, source_label: str) -> list[dict]:
    """Normalize each component against its own windows, then average stress/z across components."""
    panel_months = month_range(manifest.panel_start, manifest.panel_end)
    normalized = [
        _normalize_one(series, transform, spec.stress_orientation, manifest, panel_months)
        for transform, series in components
    ]
    n_components = len(normalized)

    rows: list[dict] = []
    for month in panel_months:
        def avg(key: str):
            vals = [c[key].get(month) for c in normalized]
            vals = [v for v in vals if v is not None and not pd.isna(v)]
            return sum(vals) / len(vals) if vals else None

        n_with_stress = sum(
            1 for c in normalized
            if (c["stress_pre"].get(month) is not None and not pd.isna(c["stress_pre"].get(month)))
            or (c["stress_str"].get(month) is not None and not pd.isna(c["stress_str"].get(month)))
        )
        raw_value = avg("feature")
        if raw_value is None:
            status, note = "missing", f"no component value for {month}"
        elif n_with_stress == 0:
            status, note = "partial", "components present but no reference window"
        else:
            status = "available"
            note = f"composite of {n_with_stress}/{n_components} components; orientation={spec.stress_orientation}"
        rows.append({
            "month": month,
            "variable_code": spec.variable_code,
            "raw_value": _clean(raw_value),
            "z_precrisis": _clean(avg("z_pre")),
            "stress_precrisis": _clean(avg("stress_pre")),
            "z_structural": _clean(avg("z_str")),
            "stress_structural": _clean(avg("stress_str")),
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
