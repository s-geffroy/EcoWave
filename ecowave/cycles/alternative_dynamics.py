"""Non-cyclical diagnostics — Tier 1 of the "beyond cycles" panorama.

The composite Gate-1 stack (``runner.py``) and per-variable Gate-1
(``evidence.py``) both rejected the canonical 4 cycles on the CPV data
panels: 100 % of cells fail dual-null AR(1) + phase-scramble after the
Roadmap #14 safeguard. Per the panoramic survey
(``docs/methodology_beyond_cycles.md``), the macro series are *not* white
noise — they show long memory (ACF lag-1 ≈ 1), volatility clustering,
heavy-tailed crashes, persistent trends — but the structure is not
periodic. This module implements the Tier 1 diagnostic toolkit that maps
each variable onto 10 non-cyclical statistical signatures spanning 11
families (A SOC, B multifractality, C long memory, E critical slowdown,
G RMT, I information, J Lévy flights, P K41 turbulence, R anomalous
diffusion, T Tsallis non-extensivity).

Each per-variable diagnostic is scored against an AR(1) or phase-scramble
null (Theiler 1992), keeping the CPV Gate-1 philosophy: a statistic alone
is not a verdict; it is significant only when it beats a structured null
at α = 0.05. Panel-level RMT (Marchenko-Pastur fit) is run separately
because it operates on the covariance matrix of a whole group, not on a
single series.

Outputs:

- ``reports/dx_diagnostics_{as_of}_{horizon}.json`` — one record per
  (group, variable, diagnostic) with statistic, p_value, null_method,
  reject_null and diagnostic-specific metadata.
- ``reports/dx_rmt_{as_of}_{horizon}.json`` — one record per (horizon,
  group) with eigenvalues, Marchenko-Pastur band, n_deviating modes.
- ``docs/dx_diagnostics.md`` — consolidated heatmaps with the
  universality cluster synthesis (Family Q meta).

Item #15 of the methodology roadmap; cf. ``methodology/feuille_de_route.md``.
"""
from __future__ import annotations

import json
import math
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
import pandas as pd

try:
    import nolds  # type: ignore
    _HAS_NOLDS = True
except ImportError:  # pragma: no cover - lazy fallback
    _HAS_NOLDS = False

try:
    import antropy  # type: ignore
    _HAS_ANTROPY = True
except ImportError:  # pragma: no cover - lazy fallback
    _HAS_ANTROPY = False

from ecowave.cycles.evidence import (
    HORIZON_VARIABLE_SOURCE,
    _load_annual_panel,
    _load_quarterly_panel,
    _load_variable_codes,
)
from ecowave.cycles.surrogate_generators import (
    ar1_surrogate_series,
    phase_scramble_surrogate_series,
)


MIN_SERIES_LENGTH = 32
DEFAULT_ALPHA = 0.05
DEFAULT_N_SURROGATES = 200


@dataclass(frozen=True)
class DiagnosticResult:
    """One diagnostic applied to one z-scored series, with null test verdict."""
    statistic: float | None
    p_value: float | None
    null_method: str
    n_surrogates: int
    reject_null: bool
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Null test wrapper — reused by every per-variable diagnostic
# ---------------------------------------------------------------------------

def _two_sided_p_value(real: float, surrogate_stats: list[float]) -> float:
    """Empirical two-sided p-value for *real* against the surrogate sample.

    Returns the probability of seeing a surrogate as extreme as *real* under
    the two-sided test. NaN-safe: surrogate NaNs are filtered out.
    """
    finite = [s for s in surrogate_stats if s is not None and np.isfinite(s)]
    if not finite or not np.isfinite(real):
        return 1.0
    arr = np.asarray(finite, dtype=float)
    median = float(np.median(arr))
    distance = abs(real - median)
    n_extreme = int(np.sum(np.abs(arr - median) >= distance))
    return (n_extreme + 1) / (len(arr) + 1)


def _upper_tail_p_value(real: float, surrogate_stats: list[float]) -> float:
    """Empirical right-tail p-value — for statistics where 'larger = more
    structured than null' (Hurst, Δα, β, Kendall τ, K41 scaling)."""
    finite = [s for s in surrogate_stats if s is not None and np.isfinite(s)]
    if not finite or not np.isfinite(real):
        return 1.0
    arr = np.asarray(finite, dtype=float)
    n_geq = int(np.sum(arr >= real))
    return (n_geq + 1) / (len(arr) + 1)


def _lower_tail_p_value(real: float, surrogate_stats: list[float]) -> float:
    """Empirical left-tail p-value — for statistics where 'smaller = more
    structured than null' (permutation entropy, Lévy α, q-Gaussian distance
    from Gaussian)."""
    finite = [s for s in surrogate_stats if s is not None and np.isfinite(s)]
    if not finite or not np.isfinite(real):
        return 1.0
    arr = np.asarray(finite, dtype=float)
    n_leq = int(np.sum(arr <= real))
    return (n_leq + 1) / (len(arr) + 1)


def _run_null_test(
    z: np.ndarray,
    statistic_fn: Callable[[np.ndarray], float],
    null_method: str,
    n_surrogates: int,
    seed: int,
    tail: str = "upper",
) -> tuple[float, int]:
    """Compute p-value of statistic_fn(z) against n_surrogates surrogates.

    Returns (p_value, effective n_surrogates). The null is either ``"ar1"``
    or ``"phase_scramble"``. The *tail* argument selects the tail used to
    compute the p-value: ``"upper"`` (default), ``"lower"`` or ``"two-sided"``.
    """
    if null_method == "ar1":
        generator = ar1_surrogate_series(z, n_surrogates, seed)
    elif null_method == "phase_scramble":
        generator = phase_scramble_surrogate_series(z, n_surrogates, seed)
    else:
        raise ValueError(f"unknown null_method: {null_method}")
    real_stat = statistic_fn(z)
    surrogate_stats: list[float] = []
    for surrogate in generator:
        try:
            surrogate_stats.append(float(statistic_fn(surrogate)))
        except Exception:  # noqa: BLE001 — diagnostic robustness
            surrogate_stats.append(float("nan"))
    if tail == "upper":
        p = _upper_tail_p_value(real_stat, surrogate_stats)
    elif tail == "lower":
        p = _lower_tail_p_value(real_stat, surrogate_stats)
    else:
        p = _two_sided_p_value(real_stat, surrogate_stats)
    return p, len(surrogate_stats)


# ---------------------------------------------------------------------------
# 1. DFA / Hurst exponent — family C (long memory)
# ---------------------------------------------------------------------------

def _dfa_hurst_custom(z: np.ndarray) -> float:
    """Custom DFA fallback (Peng et al. 1994). Used when ``nolds`` absent
    or fails on the input shape."""
    z = np.asarray(z, dtype=float)
    n = z.size
    if n < MIN_SERIES_LENGTH:
        return float("nan")
    y = np.cumsum(z - np.mean(z))
    scales = np.unique(np.round(np.logspace(
        np.log10(4), np.log10(n // 4), num=12)).astype(int))
    scales = scales[(scales >= 4) & (scales <= n // 4)]
    if scales.size < 4:
        return float("nan")
    fluctuations = []
    for s in scales:
        n_segments = n // s
        if n_segments < 1:
            continue
        segments = y[: n_segments * s].reshape(n_segments, s)
        rms = []
        x = np.arange(s)
        for seg in segments:
            coeffs = np.polyfit(x, seg, deg=1)
            trend = np.polyval(coeffs, x)
            rms.append(np.sqrt(np.mean((seg - trend) ** 2)))
        fluctuations.append(np.mean(rms))
    if len(fluctuations) < 4:
        return float("nan")
    log_scales = np.log(scales[: len(fluctuations)])
    log_f = np.log(np.array(fluctuations) + 1e-12)
    slope, _ = np.polyfit(log_scales, log_f, deg=1)
    return float(slope)


def _dfa_hurst(z: np.ndarray) -> float:
    """DFA Hurst exponent. Prefers nolds (peer-reviewed) when available.

    White noise → 0.5; long memory → > 0.5; mean-reverting → < 0.5.
    """
    z = np.asarray(z, dtype=float)
    if z.size < MIN_SERIES_LENGTH:
        return float("nan")
    if _HAS_NOLDS:
        try:
            return float(nolds.dfa(z))
        except Exception:  # noqa: BLE001 - fallback
            pass
    return _dfa_hurst_custom(z)


def hurst_dfa(series: pd.Series, n_surrogates: int = DEFAULT_N_SURROGATES,
              seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < MIN_SERIES_LENGTH:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    h = _dfa_hurst(z)
    if not np.isfinite(h):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "DFA fit degenerate"})
    p, n_eff = _run_null_test(z, _dfa_hurst, "ar1", n_surrogates, seed,
                              tail="upper")
    return DiagnosticResult(
        statistic=h, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"interpretation":
                  "H > 0.5: long memory; H ≈ 0.5: random walk; "
                  "H < 0.5: mean reversion"})


# ---------------------------------------------------------------------------
# 2. MF-DFA spectrum — family B (multifractality)
# ---------------------------------------------------------------------------

_MFDFA_Q_RANGE = (-5.0, -3.0, -1.0, 1.0, 3.0, 5.0)


def _mfdfa_spectrum_width(z: np.ndarray) -> float:
    """Multifractal DFA (Kantelhardt et al. 2002). Returns Δα = α_max - α_min.

    Δα measures the width of the singularity spectrum f(α). For
    monofractal signals (AR(1), fBm) Δα ≈ 0; for multifractals Δα > 0.
    """
    z = np.asarray(z, dtype=float)
    n = z.size
    if n < MIN_SERIES_LENGTH:
        return float("nan")
    y = np.cumsum(z - np.mean(z))
    scales = np.unique(np.round(np.logspace(
        np.log10(8), np.log10(n // 4), num=10)).astype(int))
    scales = scales[(scales >= 8) & (scales <= n // 4)]
    if scales.size < 4:
        return float("nan")
    h_q: list[float] = []
    for q in _MFDFA_Q_RANGE:
        fq: list[float] = []
        for s in scales:
            n_segments = n // s
            if n_segments < 1:
                continue
            segments = y[: n_segments * s].reshape(n_segments, s)
            x = np.arange(s)
            var_seg: list[float] = []
            for seg in segments:
                coeffs = np.polyfit(x, seg, deg=1)
                trend = np.polyval(coeffs, x)
                var_seg.append(np.mean((seg - trend) ** 2))
            var_arr = np.asarray(var_seg)
            if q == 0:
                fq.append(np.exp(0.5 * np.mean(np.log(var_arr + 1e-12))))
            else:
                fq.append(np.mean(var_arr ** (q / 2.0)) ** (1.0 / q))
        if len(fq) < 4:
            return float("nan")
        log_scales = np.log(scales[: len(fq)])
        log_fq = np.log(np.array(fq) + 1e-12)
        slope, _ = np.polyfit(log_scales, log_fq, deg=1)
        h_q.append(float(slope))
    h_arr = np.asarray(h_q)
    q_arr = np.asarray(_MFDFA_Q_RANGE)
    tau = q_arr * h_arr - 1.0
    alpha = np.gradient(tau, q_arr)
    return float(alpha.max() - alpha.min())


def mfdfa_spectrum(series: pd.Series, n_surrogates: int = DEFAULT_N_SURROGATES,
                   seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < MIN_SERIES_LENGTH * 2:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short for MF-DFA"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    delta_alpha = _mfdfa_spectrum_width(z)
    if not np.isfinite(delta_alpha):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "MF-DFA fit degenerate"})
    p, n_eff = _run_null_test(z, _mfdfa_spectrum_width, "ar1",
                              n_surrogates, seed, tail="upper")
    return DiagnosticResult(
        statistic=delta_alpha, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"q_range": list(_MFDFA_Q_RANGE),
                  "interpretation": "Δα > 0: multifractal; Δα ≈ 0: monofractal"})


# ---------------------------------------------------------------------------
# 3. Spectrum slope — family A (SOC, 1/f^β)
# ---------------------------------------------------------------------------

def _spectrum_slope(z: np.ndarray) -> float:
    """Log-log slope of the periodogram (1/f^β). White noise → 0;
    Brownian → -2; SOC → -1 typically."""
    z = np.asarray(z, dtype=float)
    n = z.size
    if n < MIN_SERIES_LENGTH:
        return float("nan")
    spectrum = np.fft.rfft(z - z.mean())
    psd = np.abs(spectrum) ** 2
    freqs = np.fft.rfftfreq(n, d=1.0)
    mask = (freqs > 0) & (psd > 0)
    if mask.sum() < 4:
        return float("nan")
    log_f = np.log(freqs[mask])
    log_p = np.log(psd[mask])
    slope, _ = np.polyfit(log_f, log_p, deg=1)
    return float(-slope)  # 1/f^β convention: β > 0 for red noise


def spectrum_slope(series: pd.Series, n_surrogates: int = DEFAULT_N_SURROGATES,
                   seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < MIN_SERIES_LENGTH:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    beta = _spectrum_slope(z)
    if not np.isfinite(beta):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "PSD fit degenerate"})
    p, n_eff = _run_null_test(z, _spectrum_slope, "ar1", n_surrogates,
                              seed, tail="upper")
    return DiagnosticResult(
        statistic=beta, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"interpretation":
                  "β ≈ 0: white noise; β ≈ 1: SOC / 1/f; β ≈ 2: Brownian"})


# ---------------------------------------------------------------------------
# 4. Hill tail exponent — family A (power-law tails)
# ---------------------------------------------------------------------------

def _hill_tail_exponent(z: np.ndarray, k_frac: float = 0.1) -> float:
    """Hill estimator (1975) for the right-tail exponent of |z|.

    Returns α_Hill on the order-statistics of |z|: small α_Hill → heavy
    tail (Pareto-like, characteristic of SOC and crash distributions);
    large α_Hill → light tail (Gaussian, exponential).
    """
    abs_z = np.abs(np.asarray(z, dtype=float))
    abs_z = abs_z[abs_z > 0]
    n = abs_z.size
    if n < MIN_SERIES_LENGTH:
        return float("nan")
    sorted_desc = np.sort(abs_z)[::-1]
    k = max(int(np.floor(k_frac * n)), 8)
    k = min(k, n - 1)
    top = sorted_desc[: k + 1]
    threshold = sorted_desc[k]
    if threshold <= 0:
        return float("nan")
    log_ratios = np.log(top[:-1] / threshold)
    mean_log = float(np.mean(log_ratios))
    if mean_log <= 0:
        return float("nan")
    return 1.0 / mean_log


def hill_tail_exponent(series: pd.Series,
                       n_surrogates: int = DEFAULT_N_SURROGATES,
                       seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < MIN_SERIES_LENGTH:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    alpha_hill = _hill_tail_exponent(z)
    if not np.isfinite(alpha_hill):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "Hill fit degenerate"})
    p, n_eff = _run_null_test(z, _hill_tail_exponent, "ar1",
                              n_surrogates, seed, tail="lower")
    return DiagnosticResult(
        statistic=alpha_hill, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"k_fraction": 0.1,
                  "interpretation":
                  "α_Hill < 3: heavy-tailed (Pareto, SOC); "
                  "α_Hill > 5: light-tailed (Gaussian-like)"})


# ---------------------------------------------------------------------------
# 5. Permutation entropy + statistical complexity — family I (information)
# ---------------------------------------------------------------------------

def _permutation_distribution(z: np.ndarray, order: int = 3) -> np.ndarray:
    """Empirical distribution of ordinal patterns (Bandt-Pompe 2002)."""
    z = np.asarray(z, dtype=float)
    n = z.size - order + 1
    if n <= 1:
        return np.array([])
    factorial_order = math.factorial(order)
    counts = np.zeros(factorial_order, dtype=int)
    pattern_index = {p: i for i, p in
                     enumerate(_permutations_of(tuple(range(order))))}
    for i in range(n):
        window = z[i: i + order]
        pattern = tuple(int(r) for r in np.argsort(window))
        counts[pattern_index[pattern]] += 1
    return counts / counts.sum()


def _permutations_of(seq: tuple) -> Iterable[tuple]:
    """Yield all permutations of *seq* in lexicographic order."""
    from itertools import permutations
    return permutations(seq)


def _permutation_entropy_normalised(z: np.ndarray, order: int = 3) -> float:
    """Normalised Shannon entropy of the ordinal pattern distribution.

    Returns H in [0, 1] : 1 = max randomness, 0 = perfect predictability.
    Prefers antropy.perm_entropy when available (peer-reviewed).
    """
    z = np.asarray(z, dtype=float)
    if z.size < order + 1:
        return float("nan")
    if _HAS_ANTROPY:
        try:
            return float(antropy.perm_entropy(z, order=order, normalize=True))
        except Exception:  # noqa: BLE001 - fallback
            pass
    p = _permutation_distribution(z, order)
    if p.size == 0:
        return float("nan")
    nonzero = p[p > 0]
    entropy = -float(np.sum(nonzero * np.log(nonzero)))
    return entropy / math.log(math.factorial(order))


def _lmc_complexity(z: np.ndarray, order: int = 3) -> float:
    """López-Ruiz-Mancini-Calbet statistical complexity (1995).

    C = H_norm * D_jensen-shannon(p, uniform). Maximal at intermediate
    entropy regimes (structured but not periodic).
    """
    p = _permutation_distribution(z, order)
    if p.size == 0:
        return float("nan")
    n_patterns = p.size
    uniform = np.full(n_patterns, 1.0 / n_patterns)
    h_norm = _permutation_entropy_normalised(z, order)
    if not np.isfinite(h_norm):
        return float("nan")
    mix = 0.5 * (p + uniform)
    nonzero_mix = mix > 0
    entropy_mix = -float(np.sum(mix[nonzero_mix] * np.log(mix[nonzero_mix])))
    nonzero_p = p > 0
    entropy_p = -float(np.sum(p[nonzero_p] * np.log(p[nonzero_p])))
    entropy_u = math.log(n_patterns)
    js_div = entropy_mix - 0.5 * (entropy_p + entropy_u)
    # Normalise JS divergence to [0, 1]
    max_js = -((n_patterns + 1) / n_patterns *
               math.log(n_patterns + 1) - 2 * math.log(2 * n_patterns)
               + math.log(n_patterns)) / 2.0
    if max_js <= 0:
        return float("nan")
    return h_norm * (js_div / max_js)


def permutation_entropy_complexity(
        series: pd.Series, order: int = 3,
        n_surrogates: int = DEFAULT_N_SURROGATES,
        seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < MIN_SERIES_LENGTH:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    h_perm = _permutation_entropy_normalised(z, order)
    c_stat = _lmc_complexity(z, order)
    if not (np.isfinite(h_perm) and np.isfinite(c_stat)):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "ordinal counts degenerate"})
    p, n_eff = _run_null_test(
        z, lambda y: _permutation_entropy_normalised(y, order),
        "ar1", n_surrogates, seed, tail="lower")
    return DiagnosticResult(
        statistic=h_perm, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"order": order, "complexity_C": c_stat,
                  "interpretation":
                  "H_perm < 1 with C > 0.3: structured but non-periodic "
                  "(edge of chaos, family I)"})


# ---------------------------------------------------------------------------
# 6. Critical slowdown — family E (tipping points)
# ---------------------------------------------------------------------------

def _kendall_tau_trend(values: np.ndarray) -> float:
    """Kendall τ of *values* vs index (no scipy import for surrogate speed)."""
    n = values.size
    if n < 4:
        return float("nan")
    concordant = 0
    discordant = 0
    for i in range(n - 1):
        diff = values[i + 1:] - values[i]
        concordant += int(np.sum(diff > 0))
        discordant += int(np.sum(diff < 0))
    total = n * (n - 1) // 2
    if total == 0:
        return float("nan")
    return (concordant - discordant) / total


def _rolling_variance_trend(z: np.ndarray, window: int = 30) -> float:
    """Kendall τ of rolling variance — positive → CSD signature."""
    z = np.asarray(z, dtype=float)
    n = z.size
    if n < window * 2:
        return float("nan")
    rolling = np.array([z[i: i + window].var(ddof=1)
                        for i in range(n - window + 1)])
    return _kendall_tau_trend(rolling)


def critical_slowdown(series: pd.Series, window: int = 30,
                      n_surrogates: int = DEFAULT_N_SURROGATES,
                      seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < window * 2:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series shorter than 2× window"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    tau_var = _rolling_variance_trend(z, window)
    if not np.isfinite(tau_var):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "rolling variance degenerate"})
    p, n_eff = _run_null_test(
        z, lambda y: _rolling_variance_trend(y, window),
        "ar1", n_surrogates, seed, tail="upper")
    return DiagnosticResult(
        statistic=tau_var, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"window": window,
                  "interpretation":
                  "τ_var > 0 + p < 0.05: variance rising → approaching "
                  "tipping point (Dakos 2008)"})


# ---------------------------------------------------------------------------
# 7. Lévy stable fit — family J (heavy tails, Lévy flights)
# ---------------------------------------------------------------------------

def _levy_alpha_mcculloch(z: np.ndarray) -> float:
    """McCulloch (1986) quantile estimator for Lévy stable α index.

    α = 2: Gaussian; α < 2: heavy-tailed Lévy. Fast (~50 µs) — used as the
    statistic for the null test (scipy.stats.levy_stable.fit is too slow
    for 200 surrogates per variable).
    """
    z = np.asarray(z, dtype=float)
    z = z[np.isfinite(z)]
    if z.size < MIN_SERIES_LENGTH:
        return float("nan")
    q05, q25, q50, q75, q95 = np.percentile(z, [5, 25, 50, 75, 95])
    iqr = q75 - q25
    if iqr <= 0:
        return float("nan")
    v_alpha = (q95 - q05) / iqr
    # Inverse map from v_alpha to α (McCulloch table, monotonic on [1, 2.5])
    # Linear interpolation on coarse points.
    table_v = [2.439, 2.500, 2.600, 2.700, 2.800, 2.918, 3.079, 3.244,
               3.413, 3.587, 3.766, 3.948, 4.135, 4.326, 4.521, 4.722]
    table_a = [2.000, 1.916, 1.808, 1.729, 1.664, 1.563, 1.484, 1.412,
               1.346, 1.284, 1.227, 1.173, 1.123, 1.075, 1.029, 0.986]
    if v_alpha <= table_v[0]:
        return 2.0
    if v_alpha >= table_v[-1]:
        return 0.5
    for i in range(len(table_v) - 1):
        if table_v[i] <= v_alpha <= table_v[i + 1]:
            t = (v_alpha - table_v[i]) / (table_v[i + 1] - table_v[i])
            return float(table_a[i] + t * (table_a[i + 1] - table_a[i]))
    return float("nan")


def levy_stable_fit(series: pd.Series,
                    n_surrogates: int = DEFAULT_N_SURROGATES,
                    seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < MIN_SERIES_LENGTH:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    alpha = _levy_alpha_mcculloch(z)
    if not np.isfinite(alpha):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "quantile spread degenerate"})
    p, n_eff = _run_null_test(z, _levy_alpha_mcculloch, "ar1",
                              n_surrogates, seed, tail="lower")
    return DiagnosticResult(
        statistic=alpha, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"estimator": "McCulloch 1986 quantile",
                  "interpretation":
                  "α = 2: Gaussian; α ≈ 1.5: Lévy heavy-tailed; "
                  "α < 1: Cauchy-like"})


# ---------------------------------------------------------------------------
# 8. K41 scaling — family P (turbulence, Kolmogorov 1941)
# ---------------------------------------------------------------------------

def _k41_zeta_ratio(z: np.ndarray) -> float:
    """Ratio ζ(6) / ζ(3) of structure function exponents (K41 predicts 2).

    Computes log-log slope of <|z(t+τ) - z(t)|^p> vs τ for p = 3 and p = 6,
    then returns ζ(6)/ζ(3). K41 monofractal scaling: ratio = 2. Anomalous
    multiscaling (She-Levêque, Frisch 1995): ratio < 2.
    """
    z = np.asarray(z, dtype=float)
    n = z.size
    if n < 64:
        return float("nan")
    tau_range = [1, 2, 4, 8, 16, 32]
    tau_range = [t for t in tau_range if t < n // 4]
    if len(tau_range) < 3:
        return float("nan")
    s3, s6 = [], []
    for tau in tau_range:
        inc = z[tau:] - z[:-tau]
        s3.append(np.mean(np.abs(inc) ** 3))
        s6.append(np.mean(np.abs(inc) ** 6))
    if not (np.all(np.array(s3) > 0) and np.all(np.array(s6) > 0)):
        return float("nan")
    log_tau = np.log(tau_range)
    z3, _ = np.polyfit(log_tau, np.log(s3), deg=1)
    z6, _ = np.polyfit(log_tau, np.log(s6), deg=1)
    if z3 == 0:
        return float("nan")
    return float(z6 / z3)


def k41_scaling(series: pd.Series, n_surrogates: int = DEFAULT_N_SURROGATES,
                seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < 64:
        return DiagnosticResult(None, None, "phase_scramble", 0, False,
                                {"reason": "series too short for K41"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    ratio = _k41_zeta_ratio(z)
    if not np.isfinite(ratio):
        return DiagnosticResult(None, None, "phase_scramble", 0, False,
                                {"reason": "K41 fit degenerate"})
    p, n_eff = _run_null_test(z, _k41_zeta_ratio, "phase_scramble",
                              n_surrogates, seed, tail="lower")
    return DiagnosticResult(
        statistic=ratio, p_value=p, null_method="phase_scramble",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"interpretation":
                  "ζ(6)/ζ(3) = 2: K41 monofractal; < 2: She-Levêque "
                  "anomalous scaling (multifractal turbulence)"})


# ---------------------------------------------------------------------------
# 9. MSD log-log scaling — family R (anomalous diffusion)
# ---------------------------------------------------------------------------

def _msd_exponent(z: np.ndarray) -> float:
    """Slope of log <(z(t+τ) - z(t))²> vs log τ.

    The input series *z* is treated as the trajectory itself (consistent
    with how macro variables are stored : the values *are* the position,
    not the increments). Returns γ : 1 = normal Brownian diffusion ;
    < 1 = subdiffusion (caging, traps) ; > 1 = superdiffusion (Lévy walks).
    """
    z = np.asarray(z, dtype=float)
    n = z.size
    if n < 64:
        return float("nan")
    x = z - z.mean()
    tau_range = np.unique(np.round(np.logspace(
        0, np.log10(n // 4), num=12)).astype(int))
    tau_range = tau_range[(tau_range >= 1) & (tau_range <= n // 4)]
    if tau_range.size < 4:
        return float("nan")
    msd = []
    for tau in tau_range:
        diffs = x[tau:] - x[:-tau]
        msd.append(np.mean(diffs ** 2))
    if not np.all(np.array(msd) > 0):
        return float("nan")
    slope, _ = np.polyfit(np.log(tau_range), np.log(msd), deg=1)
    return float(slope)


def msd_log_log(series: pd.Series, n_surrogates: int = DEFAULT_N_SURROGATES,
                seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < 64:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short for MSD"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    gamma = _msd_exponent(z)
    if not np.isfinite(gamma):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "MSD fit degenerate"})
    p, n_eff = _run_null_test(z, _msd_exponent, "ar1", n_surrogates,
                              seed, tail="two-sided")
    return DiagnosticResult(
        statistic=gamma, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"interpretation":
                  "γ ≈ 1: normal diffusion; γ < 1: subdiffusion; "
                  "γ > 1: superdiffusion (Lévy walk)"})


# ---------------------------------------------------------------------------
# 10. Tsallis q-Gaussian fit — family T (non-extensive statistics)
# ---------------------------------------------------------------------------

def _tsallis_q_index(z: np.ndarray) -> float:
    """Estimate the Tsallis entropic index q from the empirical kurtosis.

    For a q-Gaussian (Tsallis 1988 ; Tsallis 2009 *Introduction to
    Nonextensive Statistical Mechanics*), the kurtosis κ at q = 1 (pure
    Gaussian) equals 3 and increases monotonically with q. We use the
    bounded proxy q = 1 + (κ - 3) / (κ + 1), which satisfies q(3) = 1
    and saturates at q → 2 as κ → ∞. This is a fast moment-based
    estimator suitable for surrogate testing — not a full MLE on the
    q-Gaussian likelihood.
    """
    z = np.asarray(z, dtype=float)
    z = z[np.isfinite(z)]
    if z.size < MIN_SERIES_LENGTH:
        return float("nan")
    mu = np.mean(z)
    sigma = np.std(z)
    if sigma <= 0:
        return float("nan")
    standardised = (z - mu) / sigma
    kappa = float(np.mean(standardised ** 4))
    if kappa <= 1.0:
        return float("nan")
    return 1.0 + (kappa - 3.0) / (kappa + 1.0)


def tsallis_q_gaussian(series: pd.Series,
                       n_surrogates: int = DEFAULT_N_SURROGATES,
                       seed: int = 0) -> DiagnosticResult:
    z = series.dropna().astype(float).to_numpy()
    if z.size < MIN_SERIES_LENGTH:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    q = _tsallis_q_index(z)
    if not np.isfinite(q):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "kurtosis degenerate"})
    p, n_eff = _run_null_test(z, _tsallis_q_index, "ar1", n_surrogates,
                              seed, tail="upper")
    return DiagnosticResult(
        statistic=q, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"interpretation":
                  "q = 1: Gaussian (Boltzmann-Gibbs); q > 1.3: heavy-tailed "
                  "q-Gaussian (non-extensive Tsallis statistics)"})


# ---------------------------------------------------------------------------
# 11. Reflexivity drift — family S (transversal Soros + Friston)
# ---------------------------------------------------------------------------

def _ks_two_sample(a: np.ndarray, b: np.ndarray) -> float:
    """Two-sample Kolmogorov-Smirnov statistic without scipy dependency.

    Returns sup_x |F_a(x) - F_b(x)| where F_a, F_b are empirical CDFs.
    Used to detect a shift in the marginal distribution between the first
    and second half of the observation window — the *empirical* signature
    of a cognitive regime change (reflexivity à la Soros 1987 ;
    Akerlof-Shiller 2009).
    """
    a = np.sort(np.asarray(a, dtype=float))
    b = np.sort(np.asarray(b, dtype=float))
    if a.size == 0 or b.size == 0:
        return float("nan")
    combined = np.sort(np.concatenate([a, b]))
    cdf_a = np.searchsorted(a, combined, side="right") / a.size
    cdf_b = np.searchsorted(b, combined, side="right") / b.size
    return float(np.max(np.abs(cdf_a - cdf_b)))


def _reflexivity_drift(z: np.ndarray) -> float:
    """KS-based reflexivity drift between first and second half of *z*."""
    z = np.asarray(z, dtype=float)
    if z.size < MIN_SERIES_LENGTH:
        return float("nan")
    mid = z.size // 2
    first, second = z[:mid], z[mid:]
    return _ks_two_sample(first, second)


def reflexivity_drift(series: pd.Series,
                      n_surrogates: int = DEFAULT_N_SURROGATES,
                      seed: int = 0) -> DiagnosticResult:
    """Family S (réflexivité transversale) — does the marginal distribution
    drift between the first and second half of the window?

    A stationary AR(1) null has KS ≈ 0. A reflexive system with a cognitive
    regime change (1971 Nixon shock, 1980 Volcker disinflation, 2008 GFC,
    post-COVID monetary regime) will reject the null. This diagnostic is
    *transversal* in the panorama : every other Tier 1 result should be
    read jointly with this one — when reflexivity_drift rejects, the
    9 other statistics are valid only on the analysed window, not as
    universal structural laws.
    """
    z = series.dropna().astype(float).to_numpy()
    if z.size < MIN_SERIES_LENGTH:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    ks = _reflexivity_drift(z)
    if not np.isfinite(ks):
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "KS degenerate"})
    p, n_eff = _run_null_test(z, _reflexivity_drift, "ar1",
                              n_surrogates, seed, tail="upper")
    return DiagnosticResult(
        statistic=ks, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"interpretation":
                  "KS > 0 + p < 0.05: distribution drift between halves → "
                  "cognitive regime change (Soros 1987, Akerlof-Shiller 2009) "
                  "— the 10 other diagnostics are valid only on the "
                  "analysed window"})


# ---------------------------------------------------------------------------
# 12. Lyapunov exponent — family D (deterministic chaos)
# ---------------------------------------------------------------------------

def _lyapunov_rosenstein(z: np.ndarray, m: int = 4, tau: int = 1,
                         max_t: int = 16) -> float:
    """Largest Lyapunov exponent (Rosenstein, Collins, De Luca 1993).

    Embed in m dimensions with lag τ; for each point find its nearest
    neighbour; track how the distance grows with time. The slope of
    log<distance(t)> vs t is the largest Lyapunov exponent λ. λ > 0
    → sensitive dependence on initial conditions (chaos signature).
    Prefers nolds.lyap_r when available.
    """
    z = np.asarray(z, dtype=float)
    n = z.size
    if n < 4 * m + max_t + 10:
        return float("nan")
    if _HAS_NOLDS:
        try:
            return float(nolds.lyap_r(z, emb_dim=m, lag=tau,
                                       min_tsep=10, trajectory_len=max_t))
        except Exception:  # noqa: BLE001 - fallback
            pass
    n_embedded = n - (m - 1) * tau
    if n_embedded < max_t + 4:
        return float("nan")
    embedded = np.array([
        z[i: i + n_embedded] for i in range(0, m * tau, tau)
    ]).T
    distances_log: list[float] = [0.0 for _ in range(max_t)]
    counts = [0 for _ in range(max_t)]
    for i in range(n_embedded - max_t):
        ref = embedded[i]
        d = np.linalg.norm(embedded - ref, axis=1)
        d[max(i - 5, 0): i + 5] = np.inf  # exclude temporal neighbours
        j = int(np.argmin(d))
        if not np.isfinite(d[j]) or d[j] == 0:
            continue
        for t in range(max_t):
            if i + t >= n_embedded or j + t >= n_embedded:
                break
            dist_t = np.linalg.norm(embedded[i + t] - embedded[j + t])
            if dist_t > 0:
                distances_log[t] += math.log(dist_t)
                counts[t] += 1
    avg_logs = [distances_log[t] / counts[t] if counts[t] else float("nan")
                for t in range(max_t)]
    valid = [(t, v) for t, v in enumerate(avg_logs) if np.isfinite(v)]
    if len(valid) < 4:
        return float("nan")
    ts = np.array([t for t, _ in valid])
    vs = np.array([v for _, v in valid])
    slope, _ = np.polyfit(ts, vs, deg=1)
    return float(slope)


def lyapunov_exponent(series: pd.Series,
                      n_surrogates: int = DEFAULT_N_SURROGATES // 2,
                      seed: int = 0) -> DiagnosticResult:
    """Largest Lyapunov exponent — chaos signature (family D)."""
    z = series.dropna().astype(float).to_numpy()
    if z.size < 64:
        return DiagnosticResult(None, None, "phase_scramble", 0, False,
                                {"reason": "series too short for Lyapunov"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    lam = _lyapunov_rosenstein(z)
    if not np.isfinite(lam):
        return DiagnosticResult(None, None, "phase_scramble", 0, False,
                                {"reason": "Lyapunov fit degenerate"})
    p, n_eff = _run_null_test(z, _lyapunov_rosenstein, "phase_scramble",
                              n_surrogates, seed, tail="upper")
    return DiagnosticResult(
        statistic=lam, p_value=p, null_method="phase_scramble",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"interpretation":
                  "λ > 0 + p < 0.05: deterministic chaos signature "
                  "(Rosenstein-Collins-De Luca 1993, family D)"})


# ---------------------------------------------------------------------------
# 13. BDS independence test — family D (nonlinearity)
# ---------------------------------------------------------------------------

def _bds_statistic(z: np.ndarray, m: int = 2, eps: float | None = None) -> float:
    """BDS test statistic (Brock-Dechert-Scheinkman 1996).

    Tests whether *z* is IID against the alternative of nonlinear
    dependence. Returns the standardised statistic — under IID null,
    BDS ~ N(0, 1); strong dependence → large |BDS|.
    """
    z = np.asarray(z, dtype=float)
    n = z.size
    if n < 32:
        return float("nan")
    if eps is None:
        eps = float(0.7 * np.std(z))
    if eps <= 0:
        return float("nan")
    # Correlation integral: fraction of (i, j) pairs with |z_i - z_j| < eps
    def _corr_integral(arr: np.ndarray, dim: int) -> float:
        if dim == 1:
            x = arr
        else:
            x = np.column_stack([arr[i:n - dim + 1 + i] for i in range(dim)])
        n_x = x.shape[0]
        if n_x < 2:
            return float("nan")
        count = 0
        for i in range(n_x):
            diff = np.max(np.abs(x[i + 1:] - x[i]), axis=1) if dim > 1 \
                else np.abs(x[i + 1:] - x[i])
            count += int(np.sum(diff < eps))
        return 2.0 * count / (n_x * (n_x - 1))
    c1 = _corr_integral(z, 1)
    cm = _corr_integral(z, m)
    if not (np.isfinite(c1) and np.isfinite(cm)) or c1 <= 0:
        return float("nan")
    bds_raw = cm - c1 ** m
    # Asymptotic variance (Theiler 1990 approximation, simplified)
    sigma_sq = max(1e-9, (cm * (1 - cm)) / n)
    return float(bds_raw / math.sqrt(sigma_sq))


def bds_independence(series: pd.Series,
                     n_surrogates: int = DEFAULT_N_SURROGATES,
                     seed: int = 0) -> DiagnosticResult:
    """BDS test for IID vs nonlinear structure (family D)."""
    z = series.dropna().astype(float).to_numpy()
    if z.size < 32:
        return DiagnosticResult(None, None, "phase_scramble", 0, False,
                                {"reason": "series too short for BDS"})
    z = (z - z.mean()) / (z.std() if z.std() > 0 else 1.0)
    bds = _bds_statistic(z)
    if not np.isfinite(bds):
        return DiagnosticResult(None, None, "phase_scramble", 0, False,
                                {"reason": "BDS degenerate"})
    p, n_eff = _run_null_test(z, _bds_statistic, "phase_scramble",
                              n_surrogates, seed, tail="upper")
    return DiagnosticResult(
        statistic=bds, p_value=p, null_method="phase_scramble",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"embedding_dim": 2,
                  "interpretation":
                  "|BDS| > 2 + p < 0.05: nonlinear dependence rejecting "
                  "IID (Brock-Dechert-Scheinkman 1996)"})


# ---------------------------------------------------------------------------
# 14. Multi-window reflexivity — extends family S
# ---------------------------------------------------------------------------

# Pre-registered macroeconomic regime change candidates (monetary, financial,
# geopolitical inflection points). Each tuple = (year, label). The diagnostic
# splits the series at each candidate year and tests for KS drift on either
# side. Results are reported as a multi-row table per variable.
PRE_REGISTERED_REGIME_CHANGES: tuple[tuple[int, str], ...] = (
    (1929, "Great Depression"),
    (1944, "Bretton Woods"),
    (1971, "Nixon shock / floating FX"),
    (1979, "Volcker disinflation"),
    (2008, "Global financial crisis"),
    (2020, "COVID-19 monetary regime"),
)


def reflexivity_multi_window(series: pd.Series,
                              regime_changes: tuple[tuple[int, str], ...]
                              = PRE_REGISTERED_REGIME_CHANGES,
                              n_surrogates: int = DEFAULT_N_SURROGATES,
                              seed: int = 0) -> DiagnosticResult:
    """Multi-window reflexivity: test KS drift at each pre-registered year.

    Returns the maximum KS statistic over all valid split points + p-value
    against AR(1) null. The metadata field 'per_window' lists the KS at
    every candidate year — useful for identifying *which* regime change
    dominates the empirical signature.
    """
    clean = series.dropna().astype(float)
    n = clean.size
    if n < MIN_SERIES_LENGTH * 2:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "series too short for multi-window"})
    values = clean.to_numpy()
    values = (values - values.mean()) / (values.std() if values.std() > 0 else 1.0)
    index_years: list[int] = []
    for idx in clean.index:
        if hasattr(idx, "year"):
            index_years.append(int(idx.year))
        else:
            try:
                index_years.append(int(idx))
            except (ValueError, TypeError):
                index_years.append(0)
    per_window: dict[str, float] = {}
    max_ks = -np.inf
    max_label = "none"
    for year, label in regime_changes:
        try:
            split_pos = next(i for i, y in enumerate(index_years) if y >= year)
        except StopIteration:
            continue
        if split_pos < MIN_SERIES_LENGTH or split_pos > n - MIN_SERIES_LENGTH:
            continue
        ks = _ks_two_sample(values[:split_pos], values[split_pos:])
        if not np.isfinite(ks):
            continue
        per_window[label] = float(ks)
        if ks > max_ks:
            max_ks = float(ks)
            max_label = label
    if not per_window:
        return DiagnosticResult(None, None, "ar1", 0, False,
                                {"reason": "no valid split point",
                                 "per_window": {}})

    def _max_ks_stat(arr: np.ndarray) -> float:
        max_val = -np.inf
        for year, _ in regime_changes:
            try:
                split_pos = next(i for i, y in enumerate(index_years)
                                  if y >= year)
            except StopIteration:
                continue
            if split_pos < MIN_SERIES_LENGTH or \
                    split_pos > arr.size - MIN_SERIES_LENGTH:
                continue
            val = _ks_two_sample(arr[:split_pos], arr[split_pos:])
            if np.isfinite(val) and val > max_val:
                max_val = val
        return max_val if max_val > -np.inf else float("nan")

    p, n_eff = _run_null_test(values, _max_ks_stat, "ar1",
                              n_surrogates, seed, tail="upper")
    return DiagnosticResult(
        statistic=max_ks, p_value=p, null_method="ar1",
        n_surrogates=n_eff, reject_null=bool(p < DEFAULT_ALPHA),
        metadata={"per_window": per_window,
                  "dominant_regime": max_label,
                  "interpretation":
                  "Per-window KS table identifies the dominant cognitive "
                  "regime change in the series ; max-statistic null test "
                  "controls multiple-comparison family-wise error"})


# ---------------------------------------------------------------------------
# Registry of per-variable diagnostics
# ---------------------------------------------------------------------------

DIAGNOSTICS_REGISTRY: dict[str, Callable[..., DiagnosticResult]] = {
    "hurst_dfa": hurst_dfa,
    "mfdfa_spectrum": mfdfa_spectrum,
    "spectrum_slope": spectrum_slope,
    "hill_tail_exponent": hill_tail_exponent,
    "permutation_entropy_complexity": permutation_entropy_complexity,
    "critical_slowdown": critical_slowdown,
    "levy_stable_fit": levy_stable_fit,
    "k41_scaling": k41_scaling,
    "msd_log_log": msd_log_log,
    "tsallis_q_gaussian": tsallis_q_gaussian,
    "reflexivity_drift": reflexivity_drift,
    "lyapunov_exponent": lyapunov_exponent,
    "bds_independence": bds_independence,
    "reflexivity_multi_window": reflexivity_multi_window,
}

DIAGNOSTIC_TO_FAMILY: dict[str, str] = {
    "hurst_dfa": "C — longue mémoire",
    "mfdfa_spectrum": "B — multifractalité",
    "spectrum_slope": "A — SOC (1/f^β)",
    "hill_tail_exponent": "A — queues de loi de puissance",
    "permutation_entropy_complexity": "I — information",
    "critical_slowdown": "E — tipping point",
    "levy_stable_fit": "J — vols de Lévy",
    "k41_scaling": "P — cascades K41",
    "msd_log_log": "R — diffusion anormale",
    "tsallis_q_gaussian": "T — non-extensivité",
    "reflexivity_drift": "S — réflexivité (transversal)",
    "lyapunov_exponent": "D — chaos déterministe (Tier 2)",
    "bds_independence": "D — non-linéarité IID (Tier 2)",
    "reflexivity_multi_window": "S — réflexivité multi-régime (Tier 2)",
}

DIAGNOSTIC_REFERENCES: dict[str, list[str]] = {
    "hurst_dfa": ["Peng et al. 1994", "Hurst 1951", "Mandelbrot-Van Ness 1968"],
    "mfdfa_spectrum": ["Kantelhardt et al. 2002", "Bacry-Muzy-Delour 2001"],
    "spectrum_slope": ["Bak-Tang-Wiesenfeld 1987", "Bak 1996"],
    "hill_tail_exponent": ["Hill 1975", "Mantegna-Stanley 1999"],
    "permutation_entropy_complexity":
        ["Bandt-Pompe 2002", "López-Ruiz-Mancini-Calbet 1995"],
    "critical_slowdown": ["Scheffer et al. 2009", "Dakos et al. 2008"],
    "levy_stable_fit": ["McCulloch 1986", "Mantegna-Stanley 1999"],
    "k41_scaling": ["Kolmogorov 1941", "Frisch 1995", "Ghashghaie et al. 1996"],
    "msd_log_log": ["Metzler-Klafter 2000", "Mantegna-Stanley 1999"],
    "tsallis_q_gaussian": ["Tsallis 1988", "Tsallis 2009"],
    "reflexivity_drift":
        ["Soros 1987", "Akerlof-Shiller 2009", "Friston 2010"],
    "lyapunov_exponent": ["Rosenstein-Collins-De Luca 1993", "Wolf et al. 1985"],
    "bds_independence": ["Brock-Dechert-Scheinkman 1996"],
    "reflexivity_multi_window":
        ["Soros 1987", "Akerlof-Shiller 2009", "Friston 2010"],
}


def compute_per_variable_diagnostics(
        panels_by_group: dict[str, pd.DataFrame],
        n_surrogates: int = DEFAULT_N_SURROGATES,
        seed: int = 0) -> list[dict]:
    """Iterate (group → variable → diagnostic). No cycle axis (design
    decision item #15: diagnostics are band-agnostic; cf. plan)."""
    results: list[dict] = []
    for group, panel in panels_by_group.items():
        if panel is None or panel.empty:
            continue
        for variable in panel.columns:
            series = panel[variable].dropna()
            if series.size < MIN_SERIES_LENGTH:
                continue
            for name, fn in DIAGNOSTICS_REGISTRY.items():
                try:
                    res = fn(series, n_surrogates=n_surrogates, seed=seed)
                except Exception as exc:  # noqa: BLE001
                    res = DiagnosticResult(
                        None, None, "n/a", 0, False,
                        {"error": type(exc).__name__})
                results.append({
                    "group_code": group,
                    "variable_code": variable,
                    "diagnostic": name,
                    "family": DIAGNOSTIC_TO_FAMILY[name],
                    "statistic": res.statistic,
                    "p_value": res.p_value,
                    "null_method": res.null_method,
                    "n_surrogates": res.n_surrogates,
                    "reject_null": int(res.reject_null),
                    "metadata": res.metadata,
                    "n_observations": int(series.size),
                })
    return results


# ---------------------------------------------------------------------------
# RMT — Marchenko-Pastur on panel covariance (family G)
# ---------------------------------------------------------------------------

def _marchenko_pastur_band(n_obs: int, n_var: int,
                           sigma_sq: float = 1.0) -> tuple[float, float]:
    """Theoretical MP band [λ_min, λ_max] for a random covariance matrix."""
    q = n_var / n_obs
    lam_min = sigma_sq * (1.0 - np.sqrt(q)) ** 2
    lam_max = sigma_sq * (1.0 + np.sqrt(q)) ** 2
    return float(lam_min), float(lam_max)


def compute_rmt_per_group(panels_by_group: dict[str, pd.DataFrame],
                          ) -> list[dict]:
    """RMT spectrum on the covariance matrix of (variable × time) per group.

    Returns one record per group with eigenvalues, the theoretical MP band,
    and the count of eigenvalues that fall outside the bulk (significant
    factors of correlation).
    """
    results: list[dict] = []
    for group, panel in panels_by_group.items():
        if panel is None or panel.empty:
            continue
        clean = panel.dropna(axis=1, how="any")
        if clean.shape[1] < 2 or clean.shape[0] < 16:
            continue
        z = (clean - clean.mean()) / clean.std().replace(0, 1.0)
        z = z.dropna(how="any")
        if z.shape[0] < 16:
            continue
        cov = z.T.dot(z) / float(z.shape[0])
        try:
            eigvals = np.linalg.eigvalsh(cov.to_numpy())
        except np.linalg.LinAlgError:
            continue
        eigvals = np.sort(eigvals)[::-1]
        lam_min, lam_max = _marchenko_pastur_band(z.shape[0], z.shape[1])
        n_dev_upper = int(np.sum(eigvals > lam_max))
        n_dev_lower = int(np.sum(eigvals < lam_min))
        results.append({
            "group_code": group,
            "n_observations": int(z.shape[0]),
            "n_variables": int(z.shape[1]),
            "eigenvalues": eigvals.tolist(),
            "mp_band_min": lam_min,
            "mp_band_max": lam_max,
            "n_deviating_upper": n_dev_upper,
            "n_deviating_lower": n_dev_lower,
            "bulk_share": float(
                np.sum((eigvals >= lam_min) & (eigvals <= lam_max))
                / eigvals.size),
            "top_eigenvalue": float(eigvals[0]),
        })
    return results


# ---------------------------------------------------------------------------
# Serialization + rendering
# ---------------------------------------------------------------------------

def _json_safe(value):
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
    return value


def write_diagnostics_sidecar(results: list[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(results), ensure_ascii=False,
                               indent=2), encoding="utf-8")
    return path


def write_rmt_sidecar(results: list[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(results), ensure_ascii=False,
                               indent=2), encoding="utf-8")
    return path


def _p_to_emoji(p: float | None) -> str:
    if p is None or (isinstance(p, float) and (math.isnan(p) or math.isinf(p))):
        return "—"
    if p <= 0.01:
        return "🟢"
    if p <= 0.05:
        return "🟡"
    if p <= 0.10:
        return "🟠"
    return "🔴"


def _format_stat(stat: float | None) -> str:
    if stat is None or not np.isfinite(stat):
        return "—"
    return f"{stat:.2f}"


def render_dx_diagnostics_md(
        results_by_horizon: dict[str, list[dict]],
        rmt_by_horizon: dict[str, list[dict]],
        as_of: str, out_path: Path) -> Path:
    """Consolidated page : diagnostic × variable × horizon heatmaps + RMT."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines: list[str] = []
    lines.append("# Diagnostics non-cycliques — au-delà des cycles, "
                 "structure statistique du panel")
    lines.append("")
    lines.append("> **Pourquoi cette page existe.** Le pipeline CPV a "
                 "rejeté les 4 cycles canoniques (Kitchin, Juglar, Kuznets, "
                 "Kondratieff) sur 100 % des cellules après les garde-fous "
                 "Roadmap #14 — cf. [Évidence par variable](evidence_per_variable.md). "
                 "Cette défaite empirique posée, la question devient : "
                 "**si pas un cycle, quoi alors ?** La page panoramique "
                 "[Au-delà des cycles — cadres physiques alternatifs]("
                 "methodology_beyond_cycles.md) recense 21 familles ; "
                 "**la présente page implémente le Tier 1 — 10 diagnostics "
                 "couvrant 10 des 21 familles**, plus une famille de "
                 "panel-level (G — RMT). Chaque diagnostic est scoré contre "
                 "un null AR(1) ou phase-scramble pour reproduire la "
                 "philosophie Gate 1 sur le terrain non-cyclique.")
    lines.append("")
    lines.append("**Lecture de l'encart 🟢🟡🟠🔴.** 🟢 = p ≤ 0.01 "
                 "(diagnostic rejette le null avec haute confiance) · "
                 "🟡 = 0.01 < p ≤ 0.05 (rejet standard CPV) · "
                 "🟠 = 0.05 < p ≤ 0.10 (marginal) · "
                 "🔴 = p > 0.10 (compatible avec le null). "
                 "Statistique = valeur observée du diagnostic ; on en "
                 "tire l'orientation de la famille physique.")
    lines.append("")
    lines.append("!!! note \"Pas de découpage 4-cycles dans cette page\"")
    lines.append("    Par construction, les diagnostics Tier 1 mesurent des "
                 "propriétés **structurelles globales** de chaque série "
                 "(Hurst, multifractalité, slope 1/f, entropie, ralentissement "
                 "critique, queues lourdes, ζ(p) de turbulence, diffusion "
                 "anormale, non-extensivité Tsallis). Réintroduire un axe "
                 "`cycle ∈ {kitchin, juglar, kuznets, kondratieff}` reviendrait "
                 "à recréer le scaffold cyclique précisément falsifié. Pour "
                 "la lecture cyclique, voir les pages Gate 1.")
    lines.append("")

    # ---------------------------- Synthèse cross-horizon ----------------
    lines.append("## Synthèse cross-horizon")
    lines.append("")
    lines.append("Pour chaque diagnostic, taux de rejet du null sur "
                 "l'ensemble (variable × groupe × horizon). Le bloc Tier 1 "
                 "(11 diagnostics) couvre les familles A, B, C, E, G, I, J, "
                 "P, R, S, T du panorama ; Tier 2 ajoute D (Lyapunov + BDS) "
                 "et une variante multi-régime de S.")
    lines.append("")
    lines.append("| Diagnostic | Famille | Taux de rejet null | n cellules | Références |")
    lines.append("|---|---|---:|---:|---|")
    for diag in DIAGNOSTICS_REGISTRY.keys():
        family = DIAGNOSTIC_TO_FAMILY[diag]
        refs = DIAGNOSTIC_REFERENCES.get(diag, [])
        refs_str = "; ".join(refs) if refs else "—"
        cells = [r for results in results_by_horizon.values() for r in results
                 if r["diagnostic"] == diag]
        if not cells:
            lines.append(f"| `{diag}` | {family} | — | 0 | {refs_str} |")
            continue
        rejects = sum(int(c["reject_null"]) for c in cells)
        rate = rejects / len(cells) if cells else 0.0
        lines.append(f"| `{diag}` | {family} | "
                     f"{100.0 * rate:.0f}% | {len(cells)} | {refs_str} |")
    lines.append("")

    # ---------------------------- Détail par horizon --------------------
    horizon_labels = {
        "wb": "Panel Banque mondiale (1960-2024)",
        "q": "Panel trimestriel (Path 5)",
        "long": "Histoire longue (1870-2022)",
        "boe": "Bank of England Millennium (1700-2016)",
        "bis": "BIS macroprudential (EM + AE, 1970-2025)",
        "sh": "Sectoral history (FRED+OWID+BEIS, 1900-2024)",
    }
    for horizon, label in horizon_labels.items():
        results = results_by_horizon.get(horizon, [])
        if not results:
            continue
        lines.append(f"## {label}")
        lines.append("")
        df = pd.DataFrame(results)
        diagnostics = list(DIAGNOSTICS_REGISTRY.keys())
        variables = sorted(df["variable_code"].unique())
        groups = sorted(df["group_code"].unique())
        for group in groups:
            sub = df[df["group_code"] == group]
            if sub.empty:
                continue
            lines.append(f"### {group}")
            lines.append("")
            header = "| Variable | " + " | ".join(diagnostics) + " |"
            lines.append(header)
            lines.append("|---|" + "|".join([":---:"] * len(diagnostics)) + "|")
            for variable in variables:
                row = sub[sub["variable_code"] == variable]
                if row.empty:
                    continue
                cells = []
                for diag in diagnostics:
                    cell = row[row["diagnostic"] == diag]
                    if cell.empty:
                        cells.append("—")
                        continue
                    rec = cell.iloc[0]
                    p_value = rec["p_value"]
                    if isinstance(p_value, (int, float)) and not pd.isna(p_value):
                        p_value = float(p_value)
                    else:
                        p_value = None
                    emoji = _p_to_emoji(p_value)
                    stat_str = _format_stat(rec["statistic"])
                    cells.append(f"{emoji} {stat_str}")
                lines.append(f"| `{variable}` | " + " | ".join(cells) + " |")
            lines.append("")

    # ---------------------------- RMT par horizon -----------------------
    lines.append("## Spectre RMT (panel-level) — famille G")
    lines.append("")
    lines.append("Décomposition de la matrice de covariance des variables de "
                 "chaque groupe. Sous Marchenko-Pastur (matrice de Wishart), "
                 "les valeurs propres doivent rester dans [λ_min, λ_max]. "
                 "Les valeurs propres au-dessus de λ_max indiquent des "
                 "modes de corrélation **structurés** (signal RMT, "
                 "[Laloux 1999](bibliographie.md)).")
    lines.append("")
    lines.append("| Horizon | Groupe | n obs | n var | "
                 "λ_max théorique | λ top observé | Modes au-dessus | "
                 "% bulk |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for horizon, rmt_records in rmt_by_horizon.items():
        for rec in rmt_records:
            lines.append(
                f"| `{horizon}` | `{rec['group_code']}` | "
                f"{rec['n_observations']} | {rec['n_variables']} | "
                f"{rec['mp_band_max']:.2f} | {rec['top_eigenvalue']:.2f} | "
                f"{rec['n_deviating_upper']} | "
                f"{100.0 * rec['bulk_share']:.0f}% |"
            )
    lines.append("")

    # ---------------------------- Mapping vers panorama -----------------
    lines.append("## Mapping retour vers le panorama")
    lines.append("")
    lines.append("Pour chaque famille du panorama Tier 1, le diagnostic "
                 "implémenté ici qui la teste empiriquement.")
    lines.append("")
    lines.append("| Famille (panorama) | Diagnostic | Lecture |")
    lines.append("|---|---|---|")
    family_lookup = [
        ("A — SOC (1/f^β)", "spectrum_slope",
         "β > 0 statistiquement → spectre rouge structuré"),
        ("A — queues de loi de puissance", "hill_tail_exponent",
         "α_Hill < 3 → tail lourde compatible SOC"),
        ("B — Multifractalité", "mfdfa_spectrum",
         "Δα > 0 → spectre f(α) large (multifractal)"),
        ("C — Longue mémoire", "hurst_dfa",
         "H > 0.5 → persistance significative"),
        ("E — Critical slowing down", "critical_slowdown",
         "τ_var > 0 + p < 0.05 → variance qui monte → tipping en approche"),
        ("G — RMT", "rmt_panel",
         "λ_top > λ_max MP → mode de corrélation structurel"),
        ("I — Information", "permutation_entropy_complexity",
         "H_perm < 1 + C > 0.3 → structuré mais non-périodique"),
        ("J — Lévy flights", "levy_stable_fit",
         "α < 2 → distribution stable Lévy (non-Gaussienne)"),
        ("P — Cascades K41", "k41_scaling",
         "ζ(6)/ζ(3) < 2 → cascade multifractale (anomalous scaling)"),
        ("R — Diffusion anormale", "msd_log_log",
         "γ ≠ 1 → super- ou sub-diffusion"),
        ("T — Non-extensivité Tsallis", "tsallis_q_gaussian",
         "q > 1.3 → distribution q-Gaussienne (non-Boltzmann)"),
        ("S — Réflexivité (transversal)", "reflexivity_drift",
         "KS > 0 + p < 0.05 → distribution drift entre les deux moitiés "
         "→ changement de régime cognitif"),
    ]
    for family, diag, reading in family_lookup:
        lines.append(f"| {family} | `{diag}` | {reading} |")
    lines.append("")

    # ---------------------------- Transversal réflexivité (S) -----------
    lines.append("## Réflexivité (famille S) — lecture transversale")
    lines.append("")
    lines.append("Conformément à la décision design de PR #22 (panorama 21 "
                 "familles), la **famille S — réflexivité** "
                 "(Soros 1987 ; Friston 2010 ; Akerlof-Shiller 2009) "
                 "n'est pas un test isolé mais une **composante transversale "
                 "obligatoire**. Le diagnostic `reflexivity_drift` "
                 "(KS deux-échantillons entre les deux moitiés de chaque "
                 "série) sert d'**indicateur de validité** des 10 autres "
                 "diagnostics : quand il rejette le null AR(1), cela "
                 "signifie que la distribution marginale a dérivé sur la "
                 "fenêtre d'observation. Dans ce cas, les statistiques "
                 "structurelles (Hurst, β, Δα, etc.) sont valables "
                 "**uniquement sur la fenêtre analysée**, pas comme lois "
                 "universelles transhistoriques.")
    lines.append("")
    lines.append("**Variables où la réflexivité est statistiquement "
                 "significative** (drift rejette null AR(1) à α=0.05) : "
                 "les autres diagnostics sur ces variables doivent être "
                 "lus avec un encart \"valable sur 1960-2024\" (ou la "
                 "fenêtre concernée). Le rejet du null ici est *attendu* "
                 "sur les variables financières post-1980 (régime "
                 "néolibéral) et les variables d'inflation post-Volcker.")
    lines.append("")
    reflexivity_lines = []
    for horizon, results in results_by_horizon.items():
        if not results:
            continue
        df = pd.DataFrame(results)
        sub = df[(df["diagnostic"] == "reflexivity_drift") &
                  (df["reject_null"] == 1)]
        if sub.empty:
            continue
        for _, rec in sub.iterrows():
            reflexivity_lines.append(
                f"| `{horizon}` | `{rec['group_code']}` | "
                f"`{rec['variable_code']}` | "
                f"{rec['statistic']:.3f} | "
                f"{rec['p_value']:.3f} |"
            )
    if reflexivity_lines:
        lines.append("| Horizon | Groupe | Variable | KS | p-value |")
        lines.append("|---|---|---|---:|---:|")
        lines.extend(reflexivity_lines[:30])
        lines.append("")
        if len(reflexivity_lines) > 30:
            lines.append(f"_… et {len(reflexivity_lines) - 30} autres lignes._")
            lines.append("")
    else:
        lines.append("_Aucune variable ne présente de drift de "
                     "distribution significatif._")
        lines.append("")

    # ---------------------------- Universality cluster Q ----------------
    lines.append("## Synthèse Q méta — clusters d'universalité")
    lines.append("")
    lines.append("La famille Q (universalité / RG / MaxEnt) opère comme "
                 "méta-cadre : elle regroupe les variables par "
                 "**signature multi-diagnostique partagée**. Pour la "
                 "première livraison, on publie une heuristique simple : "
                 "pour chaque variable, compter combien de diagnostics "
                 "rejettent le null AR(1)/phase-scramble.")
    lines.append("")
    lines.append("| Horizon | Variable | Diagnostics rejetant | Famille dominante |")
    lines.append("|---|---|---:|---|")
    for horizon, results in results_by_horizon.items():
        if not results:
            continue
        df = pd.DataFrame(results)
        summary = (df.groupby("variable_code")
                   .agg(rejects=("reject_null", "sum"),
                        n=("reject_null", "count"))
                   .reset_index()
                   .sort_values("rejects", ascending=False))
        for _, row in summary.head(10).iterrows():
            top_diag = (df[(df["variable_code"] == row["variable_code"]) &
                          (df["reject_null"] == 1)]
                        .sort_values("p_value")
                        .head(1))
            family = (top_diag["family"].iloc[0]
                      if not top_diag.empty else "—")
            lines.append(
                f"| `{horizon}` | `{row['variable_code']}` | "
                f"{int(row['rejects'])} / {int(row['n'])} | {family} |"
            )
    lines.append("")

    # ---------------------------- Sign-off -----------------------------
    lines.append("## Sign-off")
    lines.append("")
    lines.append(f"- Date de la note : {now_iso}")
    lines.append(f"- As-of : {as_of}")
    lines.append("- Pipeline : `ecowave dx-diagnostics`")
    lines.append("- Nulls : AR(1) bootstrap (Torrence-Compo 1998) + "
                 "phase-scramble (Theiler 1992), α = 0.05")
    lines.append("- Diagnostics : Tier 1 du panorama "
                 "[Au-delà des cycles](methodology_beyond_cycles.md), "
                 "spec [feuille de route #15](methodology/feuille_de_route.md"
                 "#item-15-diagnostics-non-cycliques)")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# Driver: load panels from DB and run the toolkit
# ---------------------------------------------------------------------------

def load_panels_for_horizon(db_path: Path, horizon: str) -> dict[str, pd.DataFrame]:
    """Rebuild every (group → panel) for a given horizon from SQLite.

    Mirrors evidence.py's path: load variable codes from the manifest, then
    pivot the observations table per group.
    """
    manifest_path, frequency = HORIZON_VARIABLE_SOURCE.get(horizon, (None, None))
    if manifest_path is None:
        return {}
    variable_codes = _load_variable_codes(manifest_path)
    if not variable_codes:
        return {}
    panels: dict[str, pd.DataFrame] = {}
    con = sqlite3.connect(db_path)
    try:
        if frequency == "quarterly":
            rows = con.execute(
                "SELECT DISTINCT group_code FROM "
                "cycle_observations_quarterly"
            ).fetchall()
        else:
            rows = con.execute(
                "SELECT DISTINCT group_code FROM cycle_observations"
            ).fetchall()
        for (group_code,) in rows:
            if frequency == "quarterly":
                panel = _load_quarterly_panel(con, group_code, variable_codes)
            else:
                panel = _load_annual_panel(con, group_code, variable_codes)
            if not panel.empty:
                panels[group_code] = panel
    finally:
        con.close()
    return panels
