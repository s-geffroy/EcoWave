"""Quarterly panel construction (Roadmap #9 / Path 5).

Mocks the per-provider fetchers so the test stays offline. Verifies that:
- the panel is indexed by ``PeriodIndex(freq="Q")``,
- columns match the manifest variable codes,
- ``log_diff_q`` is applied where requested (4 * Δlog),
- multi-country groups GDP-weight-aggregate without exploding on missing data.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.cycles import quarterly as q_module
from ecowave.cycles.quarterly import (
    QUARTERLY_GROUPS,
    QuarterlyDataset,
    build_quarterly_panel,
    value_transform_q,
)


def _synthetic_gdp(start: str = "1960Q1", n: int = 260) -> pd.Series:
    """Geometric GDP level (~2 % real growth + noise) on a quarterly grid."""
    idx = pd.period_range(start=start, periods=n, freq="Q")
    rng = np.random.default_rng(42)
    growth_q = 0.005 + rng.normal(scale=0.002, size=n)
    level = 100.0 * np.exp(np.cumsum(growth_q))
    return pd.Series(level, index=idx, name="gdp")


def _synthetic_rate(start: str = "1960Q1", n: int = 260) -> pd.Series:
    """Stationary 5 ± 1 unemployment-like rate."""
    idx = pd.period_range(start=start, periods=n, freq="Q")
    rng = np.random.default_rng(7)
    return pd.Series(5.0 + rng.normal(scale=1.0, size=n), index=idx, name="rate")


def test_value_transform_log_diff_q_is_annualised_growth():
    s = pd.Series([100.0, 101.0, 102.01, 103.03], dtype=float)
    out = value_transform_q(s, "log_diff_q")
    assert np.isnan(out.iloc[0])
    # log(1.01) * 4 ≈ 0.0398
    assert abs(out.iloc[1] - np.log(1.01) * 4.0) < 1e-9


def test_value_transform_level_is_passthrough():
    s = pd.Series([5.0, 4.9, 5.1])
    out = value_transform_q(s, "level")
    pd.testing.assert_series_equal(out, s)


def test_build_quarterly_panel_single_country_usa(monkeypatch, tmp_path):
    """For USA (singleton group) the panel keeps the synthetic series shape."""
    gdp = _synthetic_gdp()
    unrate = _synthetic_rate()

    def fake_dispatch(provider_cfg, country, dataset, fred_api_key, run_id):
        return {"Q_GDP": gdp, "Q_UNRATE": unrate}[provider_cfg["_var"]]

    # We re-tag specs with `_var` so the fake dispatcher knows which to return.
    specs = [
        {"variable_code": "Q_GDP",    "transform": "log_diff_q",
         "providers": {"USA": {"src": "FRED", "_var": "Q_GDP"}}},
        {"variable_code": "Q_UNRATE", "transform": "level",
         "providers": {"USA": {"src": "FRED", "_var": "Q_UNRATE"}}},
    ]
    monkeypatch.setattr(q_module, "_dispatch_fetch", fake_dispatch)

    dataset = QuarterlyDataset.default(tmp_path)
    panel = build_quarterly_panel("USA", specs, dataset, fred_api_key="dummy",
                                  start_year=1960, run_id=1)

    assert isinstance(panel.index, pd.PeriodIndex)
    assert panel.index.freqstr.startswith("Q")
    assert set(panel.columns) == {"Q_GDP", "Q_UNRATE"}
    # log_diff_q drops the first observation (NaN); the rest should be finite.
    assert panel["Q_GDP"].iloc[1:].notna().all()
    # level transform: Q_UNRATE values should match the synthetic rates exactly.
    np.testing.assert_array_almost_equal(
        panel["Q_UNRATE"].to_numpy(), unrate.to_numpy()
    )


def test_build_quarterly_panel_multicountry_g7q_gdp_weighted(monkeypatch, tmp_path):
    """Two-country sub-group: aggregation weights the GDP series itself."""
    gdp_us = _synthetic_gdp() * 2.0     # bigger weight
    gdp_gb = _synthetic_gdp() * 1.0
    rate_us = _synthetic_rate()
    rate_gb = _synthetic_rate() + 1.0   # shift so the average is sensitive

    table = {
        ("USA", "Q_GDP"): gdp_us,    ("GBR", "Q_GDP"): gdp_gb,
        ("USA", "Q_UNRATE"): rate_us, ("GBR", "Q_UNRATE"): rate_gb,
    }

    def fake_dispatch(provider_cfg, country, dataset, fred_api_key, run_id):
        return table[(country, provider_cfg["_var"])]

    specs = [
        {"variable_code": "Q_GDP",    "transform": "log_diff_q",
         "providers": {
             "USA": {"src": "FRED", "_var": "Q_GDP"},
             "GBR": {"src": "OECD", "_var": "Q_GDP"},
         }},
        {"variable_code": "Q_UNRATE", "transform": "level",
         "providers": {
             "USA": {"src": "FRED", "_var": "Q_UNRATE"},
             "GBR": {"src": "OECD", "_var": "Q_UNRATE"},
         }},
    ]
    monkeypatch.setattr(q_module, "_dispatch_fetch", fake_dispatch)

    # Use a custom two-country group via a monkey-patched mapping (G7Q has 7).
    monkeypatch.setattr(q_module, "QUARTERLY_GROUPS",
                        {**QUARTERLY_GROUPS, "TEST2": ("USA", "GBR")})

    dataset = QuarterlyDataset.default(tmp_path)
    panel = build_quarterly_panel("TEST2", specs, dataset, fred_api_key="dummy",
                                  start_year=1960, run_id=2)

    assert isinstance(panel.index, pd.PeriodIndex)
    # Aggregated UNRATE should sit between US and GB after GDP-weighting, and
    # because US has 2× weight it should sit closer to US than to GB.
    avg = panel["Q_UNRATE"].mean()
    assert rate_us.mean() < avg < rate_gb.mean()
    assert abs(avg - rate_us.mean()) < abs(avg - rate_gb.mean())
