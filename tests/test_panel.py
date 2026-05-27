from __future__ import annotations

import pandas as pd

from ecowave.ingest.manifest import IngestionSpec, Manifest, ReferenceWindow
from ecowave.normalize.panel import (
    apply_value_transform,
    build_composite_variable_rows,
    build_missing_rows,
    build_variable_rows,
)


def _manifest() -> Manifest:
    return Manifest(
        project="test",
        precrisis=ReferenceWindow("1990-01", "2006-12"),
        structural=ReferenceWindow("1990-01", "2019-12"),
        panel_start="2007-01",
        panel_end="2007-03",
        specs=[],
        not_automatable={},
    )


def _spec(transform="level", orientation="higher_is_stress") -> IngestionSpec:
    return IngestionSpec(
        variable_code="E1", provider="FRED", dataset_name="VIX", monthly_agg="avg",
        value_transform=transform, stress_orientation=orientation, confidence="A",
        series_id="VIXCLS",
    )


def test_transform_drawdown_is_non_positive():
    s = pd.Series([100, 120, 90, 60], index=["2007-01", "2007-02", "2007-03", "2007-04"])
    dd = apply_value_transform(s, "drawdown")
    assert (dd <= 0).all()
    assert dd["2007-04"] < dd["2007-02"]


def test_build_variable_rows_normalizes_against_precrisis():
    # Long calm pre-crisis history then a 2007 spike -> high stress percentile.
    idx = [f"{y}-{m:02d}" for y in range(1995, 2008) for m in range(1, 13)]
    values = [10.0] * len(idx)
    series = pd.Series(values, index=idx)
    series["2007-01"] = 80.0  # spike
    rows = build_variable_rows(_spec(), series, _manifest(), "FRED:VIXCLS")
    by_month = {r["month"]: r for r in rows}
    assert by_month["2007-01"]["status"] == "available"
    assert by_month["2007-01"]["stress_precrisis"] >= 90
    assert by_month["2007-01"]["raw_value"] == 80.0


def test_composite_averages_components():
    # Two components (e.g. US + EA), each calm pre-crisis then a spike in 2007-02.
    idx = [f"{y}-{m:02d}" for y in range(1995, 2008) for m in range(1, 13)]
    us = pd.Series([5.0] * len(idx), index=idx)
    ea = pd.Series([9.0] * len(idx), index=idx)
    us["2007-02"] = 40.0
    ea["2007-02"] = 50.0
    rows = build_composite_variable_rows(
        _spec(), [("level", us), ("level", ea)], _manifest(), "FRED:composite(2)"
    )
    by_month = {r["month"]: r for r in rows}
    assert by_month["2007-02"]["status"] == "available"
    assert "composite of 2/2" in by_month["2007-02"]["notes"]
    # raw_value is the mean of the two component features at the spike.
    assert by_month["2007-02"]["raw_value"] == 45.0
    assert by_month["2007-02"]["stress_precrisis"] >= 90


def test_missing_rows_marked_missing():
    rows = build_missing_rows("S2", "no source", _manifest())
    assert len(rows) == 3
    assert all(r["status"] == "missing" for r in rows)
    assert all(r["raw_value"] is None for r in rows)


def test_structural_window_covers_panel():
    # Structural window 1990-2019 includes 2007-2012: a crisis-only series still
    # normalizes against the structural window, while the pre-crisis window is empty.
    series = pd.Series([1.0, 2.0, 3.0], index=["2007-01", "2007-02", "2007-03"])
    rows = build_variable_rows(_spec(), series, _manifest(), "events")
    by_month = {r["month"]: r for r in rows}
    assert by_month["2007-03"]["status"] == "available"
    assert by_month["2007-03"]["stress_structural"] is not None
    assert by_month["2007-03"]["stress_precrisis"] is None
