"""Tests for the Benjamini-Hochberg FDR adjustment utility."""
from __future__ import annotations

import numpy as np

from ecowave.cycles.surrogate import benjamini_hochberg_adjust


def test_empty_input():
    out = benjamini_hochberg_adjust([])
    assert out["p_adjusted"].size == 0
    assert out["rejected"].size == 0
    assert out["threshold"] == 0.0


def test_all_significant():
    p = [0.001, 0.002, 0.003, 0.004, 0.005]
    out = benjamini_hochberg_adjust(p, alpha=0.05)
    assert out["rejected"].all()


def test_none_significant():
    p = [0.5, 0.6, 0.7, 0.8, 0.9]
    out = benjamini_hochberg_adjust(p, alpha=0.05)
    assert not out["rejected"].any()


def test_mixed_p_values_textbook_example():
    """Benjamini-Hochberg (1995) Table 1 example with n=5 and alpha=0.05.

    Raw p-values: 0.005, 0.011, 0.022, 0.041, 0.072.
    Critical values k/n * alpha: 0.010, 0.020, 0.030, 0.040, 0.050.
    Comparison: 0.005<0.010 (pass), 0.011<0.020 (pass), 0.022<0.030 (pass),
    0.041>0.040 (fail), 0.072>0.050 (fail). The step-up procedure rejects
    the first 3 hypotheses (the largest k with p_(k) <= k/n*alpha is 3).
    """
    p = [0.005, 0.011, 0.022, 0.041, 0.072]
    out = benjamini_hochberg_adjust(p, alpha=0.05)
    assert out["rejected"].tolist() == [True, True, True, False, False]
    assert abs(out["threshold"] - 0.022) < 1e-9


def test_adjusted_p_values_monotone_after_sort():
    """BH-adjusted p-values must be monotone non-decreasing when sorted."""
    rng = np.random.default_rng(0)
    p = rng.uniform(0, 1, size=200)
    out = benjamini_hochberg_adjust(p, alpha=0.05)
    sorted_idx = np.argsort(p)
    adj_sorted = out["p_adjusted"][sorted_idx]
    assert np.all(np.diff(adj_sorted) >= -1e-12)


def test_preserves_input_order():
    """The output arrays must align with the input order, not be sorted."""
    p = [0.5, 0.001, 0.7, 0.002, 0.9]
    out = benjamini_hochberg_adjust(p, alpha=0.05)
    # 0.001 and 0.002 are the two smallest. Under BH they should be
    # rejected; positions 1 and 3 in the input.
    assert out["rejected"][1] and out["rejected"][3]
    assert not out["rejected"][0]


def test_input_unchanged():
    """The input array must not be mutated."""
    p = np.array([0.01, 0.02, 0.5, 0.9])
    p_copy = p.copy()
    benjamini_hochberg_adjust(p, alpha=0.05)
    assert np.array_equal(p, p_copy)
