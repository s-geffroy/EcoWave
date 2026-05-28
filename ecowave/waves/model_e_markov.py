"""Model E — Markov-switching regimes on the composite intensity.

Where Model D uses PELT change-point detection on the multivariate curve panel,
Model E fits a Markov-switching autoregression (Hamilton 1989) on the equal-
weighted, MA3-smoothed intensity index. The two embed different generative
assumptions:

- PELT (D) treats the series as piecewise-constant with abrupt L2-cost breaks.
- Markov-switching (E) treats it as a hidden two- or three-state Markov chain
  emitting AR(1) Gaussian observations whose mean and variance switch with the
  state.

One of the four CPV votant methods (D/E/F/G); the consensus across the four
embeds robustness against any single method's generative bias.

Reference: Hamilton, J. (1989). A New Approach to the Economic Analysis of
Nonstationary Time Series and the Business Cycle. Econometrica. Implemented
via ``statsmodels.tsa.regime_switching.MarkovRegression``.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ecowave.scoring.global_indices import (
    CURVES,
    MIN_CURVES_SCORED,
    apply_ma3,
    compute_diffusion,
    compute_intensity,
    equal_weights,
)

K_STATES = (2, 3)
MIN_REGIME_MONTHS = 3


def _equal_intensity_ma3(panel: pd.DataFrame) -> pd.Series:
    """Equal-weight MA3 intensity, mirrored from ``compute_global_indices``.

    Self-contained so model_e doesn't need the full global_indices DataFrame
    (which the pipeline computes separately for persistence + figures).
    """
    available = panel[panel["status"] == "available"].copy()
    if available.empty:
        return pd.Series(dtype=float)
    available["curve"] = available["variable_code"].str[0]
    pivot = (available.groupby(["month", "curve"])["stress_precrisis"].mean()
             .unstack("curve")
             .reindex(columns=list(CURVES))
             .sort_index())
    if pivot.empty:
        return pd.Series(dtype=float)
    weights = equal_weights()
    intensities = {}
    for month, row in pivot.iterrows():
        avail = [c for c in CURVES if c in row.index and pd.notna(row[c])]
        if len(avail) < MIN_CURVES_SCORED:
            continue
        intensities[month] = compute_intensity(row, weights)
    series = pd.Series(intensities, dtype=float).sort_index()
    return apply_ma3(series)


def _regimes_to_phases(months: list[str], regimes: np.ndarray,
                       min_regime_months: int) -> list[tuple[str, str, str]]:
    """Group contiguous same-label months into ``(label, start, end)`` phases.

    Short runs (< ``min_regime_months``) are merged into the preceding regime;
    this stops the Markov-switching from over-fragmenting and makes the regime
    set comparable in granularity to PELT's output.
    """
    if not len(months):
        return []
    phases: list[list] = []
    current = [int(regimes[0]), months[0], months[0]]
    for i in range(1, len(months)):
        if int(regimes[i]) == current[0]:
            current[2] = months[i]
        else:
            phases.append(current)
            current = [int(regimes[i]), months[i], months[i]]
    phases.append(current)

    merged: list[list] = []
    for ph in phases:
        if merged and (months.index(ph[2]) - months.index(ph[1]) + 1) < min_regime_months:
            merged[-1][2] = ph[2]
        else:
            merged.append(ph)
    # Relabel regimes in order of appearance so the labels read sequentially.
    labels = {}
    out: list[tuple[str, str, str]] = []
    for state, start, end in merged:
        if state not in labels:
            labels[state] = f"regime_{len(labels) + 1}"
        out.append((labels[state], start, end))
    return out


def fit_model_e(panel: pd.DataFrame, k_states: tuple[int, ...] = K_STATES,
                min_regime_months: int = MIN_REGIME_MONTHS) -> dict:
    """Fit Markov-switching regimes on the MA3 equal-weighted intensity.

    Picks the K (in ``k_states``) that minimises BIC; reports AIC/BIC for both.
    On a degenerate series or import/convergence failure, returns a single-
    regime fallback whose ``candidate_phases`` covers the panel window.
    """
    intensity = _equal_intensity_ma3(panel).dropna()
    months = list(intensity.index.astype(str))
    fallback = {
        "name": "Markov-switching (single regime, fallback)",
        "hypothesis": "Crisis structure is whatever a Markov-switching AR(1) "
                      "infers on the equal-weighted intensity — degenerate case "
                      "with one regime.",
        "candidate_phases": [("regime_1", months[0], months[-1])] if months else [],
        "method": "MarkovRegression(AR1)", "selected_k": None,
        "aic": None, "bic": None, "fit_status": "fallback",
    }
    if len(intensity) < 2 * max(k_states) * min_regime_months:
        return fallback

    try:
        from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
    except Exception as exc:  # noqa: BLE001 — optional dependency at import time
        fallback["fit_status"] = f"statsmodels unavailable: {exc}"
        return fallback

    y = intensity.to_numpy(dtype=float)
    results: list[tuple[int, float, float, np.ndarray]] = []
    for k in k_states:
        try:
            model = MarkovRegression(y, k_regimes=k, trend="c",
                                     switching_variance=True)
            fit = model.fit(disp=False, search_reps=10)
            smoothed = fit.smoothed_marginal_probabilities
            if hasattr(smoothed, "values"):
                smoothed = smoothed.values
            regimes = np.argmax(np.asarray(smoothed), axis=1)
            results.append((k, float(fit.aic), float(fit.bic), regimes))
        except Exception:  # noqa: BLE001 — non-convergence -> skip this k
            continue

    if not results:
        fallback["fit_status"] = "no Markov fit converged"
        return fallback

    selected = min(results, key=lambda r: r[2])  # lowest BIC
    k, aic, bic, regimes = selected
    phases = _regimes_to_phases(months, regimes, min_regime_months=min_regime_months)
    if not phases:
        return fallback

    aic_bic = {f"k={kk}": {"aic": round(a, 2), "bic": round(b, 2)}
               for kk, a, b, _ in results}
    return {
        "name": f"Markov-switching ({len(phases)} regime(s), k={k} selected by BIC)",
        "hypothesis": "Crisis structure is whatever a Markov-switching AR(1) "
                      "infers on the equal-weighted intensity.",
        "candidate_phases": phases,
        "method": "MarkovRegression(AR1, switching variance)",
        "selected_k": k, "aic": aic, "bic": bic,
        "fit_status": "ok", "aic_bic_table": aic_bic,
    }


def _curve_stress_matrix(panel: pd.DataFrame) -> tuple[list[str], pd.DataFrame]:
    """Mirror Model D helper for tests that probe the same panel shape."""
    months = sorted(panel["month"].astype(str).unique())
    available = panel[panel["status"] == "available"].copy()
    if available.empty:
        return months, pd.DataFrame(index=months)
    available["curve"] = available["variable_code"].str[0]
    mat = (available.groupby(["month", "curve"])["stress_precrisis"].mean()
           .unstack("curve").reindex(index=months))
    return months, mat


def compute_diffusion_series(panel: pd.DataFrame) -> pd.Series:
    """Diffusion (count of curves > 80) per month — used by cross-curve confirmation in tests."""
    months, mat = _curve_stress_matrix(panel)
    return pd.Series(
        [compute_diffusion(mat.loc[m]) if m in mat.index else 0 for m in months],
        index=months, dtype=int,
    )
