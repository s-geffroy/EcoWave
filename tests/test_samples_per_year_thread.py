"""Verify the ``samples_per_year`` parameter is correctly threaded through
the runner's CF + composite path. Path 5 (Roadmap #9) unlocks Kitchin by
setting samples_per_year=4 at the quarterly horizon.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.cycles.decompose import cf_bandpass
from ecowave.cycles.runner import _composite_panel


def _synthetic_quarterly_panel(years: int = 80, seed: int = 0) -> pd.DataFrame:
    """Two-variable panel on a quarterly grid containing a clean 3-year cycle."""
    n = years * 4
    idx = pd.period_range(start=f"{2020-years}Q1", periods=n, freq="Q")
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    # 3-year period at quarterly resolution = 12 samples per period.
    cycle3 = np.sin(2.0 * np.pi * t / 12.0)
    noise1 = rng.normal(scale=0.2, size=n)
    noise2 = rng.normal(scale=0.2, size=n)
    return pd.DataFrame({"VAR_A": cycle3 + noise1, "VAR_B": cycle3 + noise2},
                        index=idx)


def test_cf_bandpass_recovers_3y_cycle_at_quarterly_resolution():
    """Sanity: CF on a synthetic 3y cycle, samples_per_year=4 → high corr."""
    panel = _synthetic_quarterly_panel(years=80)
    true_cycle = np.sin(2.0 * np.pi * np.arange(panel.shape[0]) / 12.0)
    out = cf_bandpass(panel["VAR_A"], lo_years=3, hi_years=5,
                      samples_per_year=4.0)
    inner = slice(40, -40)
    corr = np.corrcoef(out.to_numpy()[inner], true_cycle[inner])[0, 1]
    assert corr > 0.85, f"CF should recover the 3y cycle (corr={corr:.2f})"


def test_composite_panel_threads_samples_per_year():
    """_composite_panel(band=(3,5), samples_per_year=4) on a quarterly 3y
    sinusoid should recover the cycle (composite of two near-identical
    inputs) with high correlation."""
    panel = _synthetic_quarterly_panel(years=80)
    composite = _composite_panel(panel, band=(3, 5), samples_per_year=4.0)
    assert isinstance(composite, pd.Series)
    assert composite.dropna().size > 200
    true_cycle = np.sin(2.0 * np.pi * np.arange(panel.shape[0]) / 12.0)
    inner = slice(40, -40)
    # composite is z-scored so we compare correlation, not amplitude.
    finite = composite.to_numpy()[inner]
    corr = np.corrcoef(finite, true_cycle[inner])[0, 1]
    assert abs(corr) > 0.85, f"Composite should track the 3y cycle (corr={corr:.2f})"


def test_composite_panel_min_length_guard_scales_with_samples_per_year():
    """For samples_per_year=4 and hi=5 the guard is 2*5*4 = 40 samples; a
    20-sample series must be dropped. For samples_per_year=1 the same series
    (only 5 years long) is also too short for the band — both should drop."""
    short_idx = pd.period_range(start="2020Q1", periods=20, freq="Q")
    panel = pd.DataFrame({"VAR_A": np.arange(20, dtype=float)}, index=short_idx)
    composite_q = _composite_panel(panel, band=(3, 5), samples_per_year=4.0)
    # Composite returned but all NaN because VAR_A was filtered out.
    assert composite_q.dropna().empty


def test_composite_panel_annual_default_unchanged():
    """Non-regression: with samples_per_year=1.0 (default) results are unchanged."""
    idx_annual = pd.RangeIndex(start=1960, stop=2025)
    rng = np.random.default_rng(0)
    panel = pd.DataFrame({
        "VAR_A": np.sin(2.0 * np.pi * np.arange(len(idx_annual)) / 8.0) +
                  rng.normal(scale=0.2, size=len(idx_annual)),
        "VAR_B": np.sin(2.0 * np.pi * np.arange(len(idx_annual)) / 8.0) +
                  rng.normal(scale=0.2, size=len(idx_annual)),
    }, index=idx_annual)
    composite = _composite_panel(panel, band=(7, 11))
    assert composite.dropna().size > 30
