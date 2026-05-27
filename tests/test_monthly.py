from ecowave.normalize.monthly import month_range, build_empty_monthly_panel


def test_month_range():
    assert month_range("2007-01", "2007-03") == ["2007-01", "2007-02", "2007-03"]


def test_empty_panel_shape():
    df = build_empty_monthly_panel("2007-01", "2007-12")
    assert len(df) == 12 * 15
    assert {"month", "variable_code", "status"}.issubset(df.columns)
