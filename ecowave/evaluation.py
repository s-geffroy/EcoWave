"""Out-of-sample EWS-style validation across pilots.

Translates the early-warning-system standard (ECB / Laeven-Valencia literature)
to EcoWave: does the panel's mean stress discriminate reference-dated crisis
months from calm months? We compute the AUROC of the monthly stress signal
against independent crisis dating (NBER recessions, CEPR/EABCN euro-area dating,
Laeven & Valencia banking-crisis database, ECB CISS), pooled across pilots and
per pilot. AUROC ~0.5 means the stress signal is no better than chance.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

from ecowave.config import Settings
from ecowave.pilots import PILOTS, Pilot

HIGH_STRESS = 75.0


@dataclass(frozen=True)
class PilotEval:
    pilot: str
    auroc_mean_stress: float
    auroc_curve_count: float
    n_crisis: int
    n_calm: int
    holdout: bool


def roc_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Tie-aware AUROC via the Mann-Whitney U statistic. NaN scores are dropped."""
    y = np.asarray(y_true, dtype=float)
    s = np.asarray(y_score, dtype=float)
    keep = ~np.isnan(s)
    y, s = y[keep], s[keep]
    n_pos = int((y == 1).sum())
    n_neg = int((y == 0).sum())
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    ranks = rankdata(s)
    return float((ranks[y == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def label_crisis_months(months: list[str], intervals: tuple[tuple[str, str], ...]) -> np.ndarray:
    """1 if a month falls inside any reference crisis interval, else 0."""
    labels = np.zeros(len(months), dtype=int)
    for i, month in enumerate(months):
        for start, end in intervals:
            if str(start) <= month <= str(end):
                labels[i] = 1
                break
    return labels


def monthly_signal(panel: pd.DataFrame) -> pd.DataFrame:
    """Per-month mean stress and count of curves above the high-stress threshold."""
    available = panel[panel["status"] == "available"].copy()
    available["curve"] = available["variable_code"].str[0]
    rows = []
    for month, grp in available.groupby("month"):
        mean_stress = grp["stress_precrisis"].mean()
        curve_means = grp.groupby("curve")["stress_precrisis"].mean()
        n_curves_high = int((curve_means >= HIGH_STRESS).sum())
        rows.append({"month": str(month), "mean_stress": mean_stress,
                     "curve_count": float(n_curves_high)})
    return pd.DataFrame(rows).sort_values("month").reset_index(drop=True)


def evaluate_pilot(panel: pd.DataFrame, pilot: Pilot) -> PilotEval:
    signal = monthly_signal(panel)
    labels = label_crisis_months(signal["month"].tolist(), pilot.crisis_months)
    return PilotEval(
        pilot=pilot.code,
        auroc_mean_stress=roc_auc(labels, signal["mean_stress"].to_numpy()),
        auroc_curve_count=roc_auc(labels, signal["curve_count"].to_numpy()),
        n_crisis=int((labels == 1).sum()),
        n_calm=int((labels == 0).sum()),
        holdout=pilot.holdout,
    )


def _panel_path(settings: Settings, pilot: Pilot) -> Path:
    stem = f"monthly_panel_{pilot.panel_start[:4]}_{pilot.panel_end[:4]}"
    return settings.data_processed_dir / f"{stem}.csv"


def evaluate_all(settings: Settings) -> tuple[list[PilotEval], float, str]:
    """Evaluate every pilot whose processed panel exists, plus a pooled AUROC.

    Returns (per-pilot evals, pooled AUROC of mean stress, markdown report).
    """
    evals: list[PilotEval] = []
    pooled_labels: list[np.ndarray] = []
    pooled_scores: list[np.ndarray] = []
    missing: list[str] = []

    for code, pilot in PILOTS.items():
        path = _panel_path(settings, pilot)
        if not path.exists():
            missing.append(code)
            continue
        panel = pd.read_csv(path)
        evals.append(evaluate_pilot(panel, pilot))
        signal = monthly_signal(panel)
        labels = label_crisis_months(signal["month"].tolist(), pilot.crisis_months)
        pooled_labels.append(labels)
        pooled_scores.append(signal["mean_stress"].to_numpy())

    pooled_auroc = (roc_auc(np.concatenate(pooled_labels), np.concatenate(pooled_scores))
                    if pooled_labels else float("nan"))
    return evals, pooled_auroc, _render(evals, pooled_auroc, missing)


def _fmt(x: float) -> str:
    return "n/a" if x != x else f"{x:.3f}"


def _render(evals: list[PilotEval], pooled_auroc: float, missing: list[str]) -> str:
    lines = [
        "# EcoWave — EWS validation (AUROC vs reference crisis dating)",
        "",
        "AUROC of the monthly stress signal against independent crisis dating "
        "(NBER, CEPR/EABCN, Laeven-Valencia, ECB CISS). 0.5 = no better than chance.",
        "",
        f"**Pooled AUROC (mean stress, all pilots): {_fmt(pooled_auroc)}**",
        "",
        "| Pilot | holdout | AUROC mean-stress | AUROC curve-count | crisis months | calm months |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for e in evals:
        lines.append(
            f"| {e.pilot} | {'yes' if e.holdout else 'no'} | {_fmt(e.auroc_mean_stress)} | "
            f"{_fmt(e.auroc_curve_count)} | {e.n_crisis} | {e.n_calm} |"
        )
    if missing:
        lines += ["", f"_Pilots without a processed panel (run them first): {', '.join(missing)}._"]
    return "\n".join(lines) + "\n"
