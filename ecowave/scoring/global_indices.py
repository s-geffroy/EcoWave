"""Global synthetic indicators on top of the 5 EcoWave curves (E/D/S/L/I).

Produces an intensity index (continuous, used for Elliott analysis) and a
diffusion index (count of curves above the 80th percentile, used as a
confirmation filter). Three weighting variants are computed in parallel:

- equal  : 0.20 per curve (audit / publication default).
- pca    : weights derived from |loading on PC1| of a rolling PCA window.
- favar  : weights from predictive content (R^2) of each curve for a future
           exogenous activity anchor (FAVAR-flavoured anchor regression).

Smoothings exposed for downstream Elliott detection: raw, MA3, and the
Hodrick-Prescott cycle/trend pair (lambda=129600 monthly).
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import spsolve

CURVES = ("E", "D", "S", "L", "I")
DIFFUSION_THRESHOLD = 80.0
MIN_CURVES_SCORED = 3
HP_LAMBDA_MONTHLY = 129_600.0


@dataclass(frozen=True)
class WeightingResult:
    weights: dict[str, float]
    method: str  # 'equal', 'pca', 'favar', or fallback chain like 'favar->pca'


# ---------------------------------------------------------------------------
# Weight estimators
# ---------------------------------------------------------------------------

def equal_weights(curves: tuple[str, ...] = CURVES) -> dict[str, float]:
    n = len(curves)
    return {c: 1.0 / n for c in curves}


def pca_weights(panel: pd.DataFrame, window: int = 60, min_window: int = 36) -> dict[str, float] | None:
    """Loadings of PC1 on a rolling window terminating at the last row of `panel`.

    `panel` : DataFrame with one column per curve (E,D,S,L,I), indexed by month.
    Returns absolute-valued normalised loadings, or None if degenerate / insufficient.
    """
    cols = [c for c in CURVES if c in panel.columns]
    if not cols:
        return None
    w = min(window, len(panel))
    if w < min_window:
        return None
    sub = panel[cols].iloc[-w:].dropna(how="any")
    if len(sub) < min_window:
        return None
    X = sub.to_numpy(dtype=float)
    X = X - X.mean(axis=0, keepdims=True)
    cov = (X.T @ X) / max(len(X) - 1, 1)
    if not np.isfinite(cov).all():
        return None
    eigvals, eigvecs = np.linalg.eigh(cov)
    # eigh returns ascending; PC1 = last column
    pc1 = eigvecs[:, -1]
    if eigvals[-1] <= 1e-12:
        return None
    abs_loadings = np.abs(pc1)
    total = abs_loadings.sum()
    if total <= 1e-12:
        return None
    weights = {c: float(abs_loadings[i] / total) for i, c in enumerate(cols)}
    # Fill missing curves with 0 (still ok, they'll be renormalised on-the-fly).
    for c in CURVES:
        weights.setdefault(c, 0.0)
    return weights


def favar_weights(panel: pd.DataFrame, anchor: pd.Series, window: int = 60,
                  min_window: int = 36, horizon: int = 6, lags: int = 2) -> dict[str, float] | None:
    """Predictive-content weights for an exogenous activity anchor.

    For each curve d, fit OLS:   anchor_{t+h} = a + sum_k b_k * stress_{d,t-k} + e
    on a trailing window of length `window` (or down to `min_window`). Weight is
    proportional to in-sample R^2 (clipped at 0). Returns None to trigger fallback
    when no curve has predictive content or the window is too short.
    """
    cols = [c for c in CURVES if c in panel.columns]
    if not cols or anchor is None or anchor.empty:
        return None
    df = panel[cols].join(anchor.rename("anchor"), how="left")
    df = df.sort_index()
    df["anchor_future"] = df["anchor"].shift(-horizon)
    w = min(window, len(df))
    if w < min_window:
        return None
    sub = df.iloc[-w:]
    sub = sub.dropna(subset=["anchor_future"])
    if len(sub) < min_window:
        return None

    r2: dict[str, float] = {}
    for d in cols:
        if sub[d].isna().all():
            r2[d] = 0.0
            continue
        feature_lags = [sub[d].shift(k) for k in range(lags + 1)]
        X = pd.concat(feature_lags, axis=1)
        joined = X.join(sub["anchor_future"]).dropna()
        if len(joined) < 24:  # safety floor: need at least 2 years of monthly data
            r2[d] = 0.0
            continue
        y = joined["anchor_future"].to_numpy(dtype=float)
        X_mat = joined.drop(columns=["anchor_future"]).to_numpy(dtype=float)
        X_mat = np.column_stack([np.ones(len(X_mat)), X_mat])
        try:
            beta, *_ = np.linalg.lstsq(X_mat, y, rcond=None)
        except np.linalg.LinAlgError:
            r2[d] = 0.0
            continue
        y_hat = X_mat @ beta
        ss_res = float(np.sum((y - y_hat) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        r2[d] = max(0.0, 1.0 - ss_res / ss_tot) if ss_tot > 1e-12 else 0.0

    total = sum(r2.values())
    if total <= 1e-12:
        return None
    weights = {c: r2[c] / total for c in cols}
    for c in CURVES:
        weights.setdefault(c, 0.0)
    return weights


# ---------------------------------------------------------------------------
# Index computation primitives
# ---------------------------------------------------------------------------

def compute_intensity(curve_row: pd.Series, weights: dict[str, float]) -> float | None:
    """Weighted mean of available curve stress for a single month, renormalised.

    `curve_row` indexed by curve code with possibly NaN entries.
    """
    avail = [c for c in CURVES if c in curve_row.index and pd.notna(curve_row[c])]
    if len(avail) < MIN_CURVES_SCORED:
        return None
    w = np.array([weights.get(c, 0.0) for c in avail], dtype=float)
    s = w.sum()
    if s <= 1e-12:
        # All-zero weights on available curves -> fall back to equal weighting.
        w = np.ones(len(avail)) / len(avail)
    else:
        w = w / s
    vals = np.array([curve_row[c] for c in avail], dtype=float)
    return float(np.sum(w * vals))


def compute_diffusion(curve_row: pd.Series, threshold: float = DIFFUSION_THRESHOLD) -> int:
    avail = [c for c in CURVES if c in curve_row.index and pd.notna(curve_row[c])]
    return int(sum(1 for c in avail if curve_row[c] > threshold))


def apply_ma3(series: pd.Series) -> pd.Series:
    """Centered 3-month moving average. NaNs propagate at the edges."""
    return series.rolling(window=3, center=True, min_periods=2).mean()


def apply_hp_filter(series: pd.Series, lam: float = HP_LAMBDA_MONTHLY) -> tuple[pd.Series, pd.Series]:
    """Hodrick-Prescott trend/cycle decomposition. Returns (trend, cycle).

    Closed-form solve: trend = (I + lam * D2' D2)^{-1} y, where D2 is the
    second-difference operator. Implemented with scipy.sparse to handle 100s of
    monthly points cheaply and to avoid pulling in statsmodels.
    """
    y = series.to_numpy(dtype=float)
    mask = ~np.isnan(y)
    if mask.sum() < 4:
        nan = pd.Series(np.nan, index=series.index)
        return nan, nan
    y_clean = y[mask]
    n = len(y_clean)
    diag = np.ones(n)
    D2 = sparse.diags(
        diagonals=[diag[:-2], -2 * diag[:-2], diag[:-2]],
        offsets=[0, 1, 2],
        shape=(n - 2, n),
        format="csc",
    )
    eye = sparse.eye(n, format="csc")
    trend_clean = spsolve(eye + lam * (D2.T @ D2), y_clean)
    cycle_clean = y_clean - trend_clean
    trend = np.full_like(y, np.nan)
    cycle = np.full_like(y, np.nan)
    trend[mask] = trend_clean
    cycle[mask] = cycle_clean
    return pd.Series(trend, index=series.index), pd.Series(cycle, index=series.index)


# ---------------------------------------------------------------------------
# Pivot helpers + main entry point
# ---------------------------------------------------------------------------

def _pivot_curves(curve_scores: pd.DataFrame, value_col: str) -> pd.DataFrame:
    pivot = curve_scores.pivot(index="month", columns="curve", values=value_col).sort_index()
    for c in CURVES:
        if c not in pivot.columns:
            pivot[c] = np.nan
    return pivot[list(CURVES)]


def _resolve_weights_for_month(panel_up_to_t: pd.DataFrame, anchor: pd.Series | None,
                               weighting: str) -> WeightingResult:
    if weighting == "equal":
        return WeightingResult(equal_weights(), "equal")
    if weighting == "pca":
        w = pca_weights(panel_up_to_t)
        if w is None:
            return WeightingResult(equal_weights(), "pca->equal")
        return WeightingResult(w, "pca")
    if weighting == "favar":
        if anchor is None:
            return WeightingResult(equal_weights(), "favar->pca->equal") \
                if pca_weights(panel_up_to_t) is None \
                else WeightingResult(pca_weights(panel_up_to_t), "favar->pca")
        w = favar_weights(panel_up_to_t, anchor)
        if w is not None:
            return WeightingResult(w, "favar")
        w = pca_weights(panel_up_to_t)
        if w is not None:
            return WeightingResult(w, "favar->pca")
        return WeightingResult(equal_weights(), "favar->pca->equal")
    raise ValueError(f"Unknown weighting: {weighting}")


def compute_global_indices(curve_scores: pd.DataFrame, anchor: pd.Series | None = None,
                           weightings: tuple[str, ...] = ("equal", "pca", "favar"),
                           refs: tuple[str, ...] = ("precrisis", "structural")) -> pd.DataFrame:
    """Build the global_indices table from curve-level scores.

    Long format: one row per (month, ref, weighting). Smoothings (MA3, HP cycle
    & trend) are computed per (ref, weighting) over the full panel window.
    """
    cols = ["month", "ref", "weighting", "weighting_actual", "intensity",
            "intensity_ma3", "intensity_hp_cycle", "intensity_hp_trend",
            "diffusion", "curves_scored", "weights_json", "status"]
    if curve_scores.empty:
        return pd.DataFrame(columns=cols)

    pivots = {ref: _pivot_curves(curve_scores, f"stress_{ref}") for ref in refs}
    if anchor is not None:
        anchor = anchor.copy()
        anchor.index = anchor.index.astype(str)

    frames: list[pd.DataFrame] = []
    for ref, pivot in pivots.items():
        months = list(pivot.index)
        diffusion_series = pd.Series(
            [compute_diffusion(pivot.loc[m]) for m in months], index=months, dtype=int,
        )
        curves_scored_series = pivot.notna().sum(axis=1).astype(int)
        for weighting in weightings:
            intensities: list[float | None] = []
            methods: list[str] = []
            weights_json: list[str] = []
            for i, month in enumerate(months):
                panel_up_to_t = pivot.iloc[: i + 1]
                wres = _resolve_weights_for_month(panel_up_to_t, anchor, weighting)
                intensities.append(compute_intensity(pivot.loc[month], wres.weights))
                methods.append(wres.method)
                weights_json.append(json.dumps({k: round(v, 6) for k, v in wres.weights.items()}))
            intensity = pd.Series(intensities, index=months, dtype=float)
            ma3 = apply_ma3(intensity)
            trend, cycle = apply_hp_filter(intensity)
            frame = pd.DataFrame({
                "month": months,
                "ref": ref,
                "weighting": weighting,
                "weighting_actual": methods,
                "intensity": intensity.values,
                "intensity_ma3": ma3.values,
                "intensity_hp_cycle": cycle.values,
                "intensity_hp_trend": trend.values,
                "diffusion": diffusion_series.values,
                "curves_scored": curves_scored_series.values,
                "weights_json": weights_json,
                "status": np.where(curves_scored_series.values >= MIN_CURVES_SCORED, "scored", "blocked"),
            })
            frames.append(frame)
    return pd.concat(frames, ignore_index=True)[cols]
