"""Tier-1 non-cyclical diagnostics — Roadmap #15.

Each diagnostic is exercised against (a) pure white noise (expected: null
not rejected), (b) a long-memory or heavy-tailed control (expected: null
rejected). The thresholds are loose because the diagnostics are
intentionally short-series friendly.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.cycles.alternative_dynamics import (
    DIAGNOSTICS_REGISTRY,
    DiagnosticResult,
    compute_per_variable_diagnostics,
    compute_rmt_per_group,
    critical_slowdown,
    hill_tail_exponent,
    hurst_dfa,
    k41_scaling,
    levy_stable_fit,
    mfdfa_spectrum,
    msd_log_log,
    permutation_entropy_complexity,
    reflexivity_drift,
    spectrum_slope,
    tsallis_q_gaussian,
)


N = 256
SEED = 0


def _white_noise(n: int = N, seed: int = SEED) -> pd.Series:
    rng = np.random.default_rng(seed)
    return pd.Series(rng.normal(size=n), index=np.arange(n))


def _random_walk(n: int = N, seed: int = SEED) -> pd.Series:
    rng = np.random.default_rng(seed)
    return pd.Series(np.cumsum(rng.normal(size=n)), index=np.arange(n))


def _heavy_tailed(n: int = N, seed: int = SEED) -> pd.Series:
    rng = np.random.default_rng(seed)
    # Symmetric Pareto-like: power-law tails on both sides
    raw = rng.pareto(1.5, size=n) * rng.choice([-1.0, 1.0], size=n)
    return pd.Series(raw, index=np.arange(n))


def _drifting_series(n: int = N, seed: int = SEED) -> pd.Series:
    rng = np.random.default_rng(seed)
    first = rng.normal(size=n // 2)
    second = rng.normal(loc=2.0, scale=2.0, size=n - n // 2)
    return pd.Series(np.concatenate([first, second]), index=np.arange(n))


# ---------- Per-diagnostic smoke tests --------------------------------------

def test_registry_count():
    # 11 Tier 1 + 3 Tier 2 (lyapunov, bds, multi-window reflexivity) = 14
    assert len(DIAGNOSTICS_REGISTRY) == 14


def test_hurst_white_noise_around_half():
    res = hurst_dfa(_white_noise(), n_surrogates=50, seed=1)
    assert isinstance(res, DiagnosticResult)
    assert res.statistic is not None
    assert 0.3 < res.statistic < 0.7


def test_hurst_random_walk_high():
    res = hurst_dfa(_random_walk(), n_surrogates=50, seed=1)
    assert res.statistic is not None
    assert res.statistic > 0.7


def test_mfdfa_returns_finite_delta_alpha():
    res = mfdfa_spectrum(_random_walk(n=512), n_surrogates=30, seed=2)
    assert res.statistic is None or np.isfinite(res.statistic)


def test_mfdfa_handles_zero_variance_segment():
    """Perfect linear ramp → linear detrend absorbs the trend → some
    segments have zero residual variance. Without the 1e-12 floor,
    ``0 ** (q/2)`` blows up for q < 0 and raises a RuntimeWarning."""
    import warnings
    ramp = pd.Series(np.arange(512, dtype=float) + np.sin(
        np.arange(512) * 2 * np.pi / 17), index=np.arange(512))
    with warnings.catch_warnings():
        warnings.simplefilter("error", category=RuntimeWarning)
        res = mfdfa_spectrum(ramp, n_surrogates=20, seed=99)
    assert res.statistic is None or np.isfinite(res.statistic)


def test_spectrum_slope_white_near_zero():
    res = spectrum_slope(_white_noise(n=512), n_surrogates=50, seed=3)
    assert res.statistic is not None
    assert abs(res.statistic) < 0.6


def test_spectrum_slope_random_walk_positive():
    res = spectrum_slope(_random_walk(n=512), n_surrogates=50, seed=3)
    assert res.statistic is not None
    assert res.statistic > 1.0  # ≈ 2 for a true Brownian motion


def test_hill_heavy_tailed_low_alpha():
    res = hill_tail_exponent(_heavy_tailed(n=512), n_surrogates=50, seed=4)
    assert res.statistic is not None
    assert res.statistic < 3.0  # heavy tail


def test_permutation_entropy_white_near_one():
    res = permutation_entropy_complexity(_white_noise(n=512), order=3,
                                         n_surrogates=50, seed=5)
    assert res.statistic is not None
    assert 0.85 < res.statistic <= 1.0  # near-maximal entropy


def test_critical_slowdown_stationary_not_rejected():
    res = critical_slowdown(_white_noise(n=200), window=30,
                            n_surrogates=80, seed=6)
    assert res.statistic is not None
    # Stationary noise should not show a strong upward trend → p > 0.05
    if res.p_value is not None:
        assert res.p_value > 0.01


def test_levy_white_alpha_near_two():
    res = levy_stable_fit(_white_noise(n=512), n_surrogates=40, seed=7)
    assert res.statistic is not None
    assert res.statistic > 1.7  # Gaussian → ≈ 2.0


def test_k41_returns_finite():
    res = k41_scaling(_random_walk(n=512), n_surrogates=30, seed=8)
    assert res.statistic is None or np.isfinite(res.statistic)


def test_msd_random_walk_slope_one():
    res = msd_log_log(_random_walk(n=512), n_surrogates=40, seed=9)
    assert res.statistic is not None
    assert 0.7 < res.statistic < 1.3


def test_tsallis_white_near_one():
    res = tsallis_q_gaussian(_white_noise(n=512), n_surrogates=40, seed=10)
    assert res.statistic is not None
    # Pure Gaussian → q ≈ 1.0
    assert abs(res.statistic - 1.0) < 0.6


def test_reflexivity_drift_detects_shift():
    res = reflexivity_drift(_drifting_series(n=256),
                            n_surrogates=100, seed=11)
    assert res.statistic is not None
    assert res.statistic > 0.3  # KS picks up the regime change


def test_reflexivity_drift_stationary_low():
    res = reflexivity_drift(_white_noise(n=256), n_surrogates=100, seed=12)
    assert res.statistic is not None
    assert res.statistic < 0.3


# ---------- Batch driver ----------------------------------------------------

def test_compute_per_variable_diagnostics_smoke():
    panel = pd.DataFrame({
        "A": _white_noise().values,
        "B": _random_walk().values,
    })
    records = compute_per_variable_diagnostics(
        {"TEST_GROUP": panel}, n_surrogates=30, seed=0)
    assert len(records) == 2 * len(DIAGNOSTICS_REGISTRY)
    for rec in records:
        assert {"group_code", "variable_code", "diagnostic", "family",
                "statistic", "p_value", "reject_null"}.issubset(rec)
        assert rec["group_code"] == "TEST_GROUP"


def test_compute_rmt_per_group_smoke():
    rng = np.random.default_rng(0)
    n_obs = 200
    n_var = 6
    panel = pd.DataFrame(
        rng.normal(size=(n_obs, n_var)),
        columns=[f"V{i}" for i in range(n_var)],
    )
    records = compute_rmt_per_group({"PANEL": panel})
    assert len(records) == 1
    rec = records[0]
    assert rec["n_variables"] == n_var
    assert rec["mp_band_max"] > rec["mp_band_min"]
    assert len(rec["eigenvalues"]) == n_var


# ---------- Result schema ---------------------------------------------------

def test_result_metadata_serializes():
    res = hurst_dfa(_white_noise(), n_surrogates=20, seed=0)
    d = res.to_dict()
    assert "statistic" in d
    assert "metadata" in d
    assert isinstance(d["metadata"], dict)
