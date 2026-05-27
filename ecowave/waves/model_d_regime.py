"""Model D — a non-Elliott benchmark whose phases are derived from the data.

A/B/C are three hand-drawn Elliott segmentations. Model D removes the analyst
from the loop: it runs multivariate change-point detection (PELT, Killick et al.
2012) on the curve-level stress matrix and turns the detected regimes into
`candidate_phases` in the exact same format as the Elliott models. It is then
scored by the same pipeline. If D matches or beats the Elliott champion on the
auto-computed criteria (C1/C3), that is the publishable result: Elliott adds
nothing over an automatic regime detector.

Alternative (documented, not enabled): Markov-switching on an aggregate stress
index via statsmodels' MarkovRegression.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import ruptures as rpt

CURVES = ["E", "D", "S", "L", "I"]
MIN_SIZE = 3  # minimum regime length, in months


def _curve_stress_matrix(panel: pd.DataFrame) -> tuple[list[str], pd.DataFrame]:
    """Mean pre-crisis stress per curve (columns) and month (rows)."""
    months = sorted(panel["month"].astype(str).unique())
    available = panel[panel["status"] == "available"].copy()
    if available.empty:
        return months, pd.DataFrame(index=months)
    available["curve"] = available["variable_code"].str[0]
    mat = (available.groupby(["month", "curve"])["stress_precrisis"].mean()
           .unstack("curve").reindex(index=months))
    return months, mat


def _impute(mat: pd.DataFrame) -> np.ndarray:
    """Column-mean impute, standardize each column (PELT/L2 expects comparable scales)."""
    filled = mat.apply(lambda col: col.fillna(col.mean())).fillna(0.0)
    signal = filled.to_numpy(dtype=float)
    centered = signal - signal.mean(axis=0)
    std = signal.std(axis=0)
    std[std == 0] = 1.0
    return centered / std


def fit_model_d(panel: pd.DataFrame, min_size: int = MIN_SIZE,
                penalty: float | None = None) -> dict:
    """Detect stress regimes by PELT and return a model dict (A/B/C-compatible).

    The penalty defaults to the BIC-like value log(n) * n_features on the
    standardized signal; pass `penalty` to override.
    """
    months, mat = _curve_stress_matrix(panel)
    n = len(months)
    single_phase = [("regime_1", months[0], months[-1])] if months else []

    if mat.empty or mat.dropna(how="all").empty or n < 2 * min_size:
        return {
            "name": "Auto-detected regimes (PELT, non-Elliott)",
            "hypothesis": "Crisis structure is whatever an automatic change-point "
                          "detector finds — no Elliott grammar imposed.",
            "candidate_phases": single_phase,
            "method": "PELT(l2)", "penalty": None,
        }

    signal = _impute(mat)
    dim = signal.shape[1]
    pen = float(penalty) if penalty is not None else float(np.log(n) * dim)

    try:
        bkps = rpt.Pelt(model="l2", min_size=min_size, jump=1).fit(signal).predict(pen=pen)
    except Exception:  # noqa: BLE001 — impossible-segmentation guard -> single regime
        bkps = [n]
    if not bkps or bkps[-1] != n:
        bkps = [*[b for b in bkps if b < n], n]

    bounds = [0, *bkps]
    phases = [
        (f"regime_{i + 1}", months[bounds[i]], months[min(bounds[i + 1] - 1, n - 1)])
        for i in range(len(bkps))
    ]
    return {
        "name": f"Auto-detected regimes (PELT, {len(phases)} segments)",
        "hypothesis": "Crisis structure is whatever an automatic change-point "
                      "detector finds — no Elliott grammar imposed.",
        "candidate_phases": phases,
        "method": "PELT(l2)", "penalty": pen,
    }
