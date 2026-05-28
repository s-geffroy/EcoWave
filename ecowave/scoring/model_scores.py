"""Auto-computed criteria for the CPV stack (Models D/E/F/G).

Only the falsifiable criteria are scored:

- **C1 — synchronisation_multi_courbes**: number of curves (E/D/S/L/I) whose
  η² phase-separation beats the (1-α) surrogate-null percentile on the
  pre-crisis window. Higher = more curves agree the model's phases separate
  stress.
- **C3 — robustesse_des_fenetres**: share of curves that confirm on both
  reference windows (precrisis + structural). A model that survives the
  window-shift test is more robust.

The qualitative analyst-graded criteria (C2 boundaries, C4 parsimony, C5
added value, C6 transferability) have been retired; only the data-driven
C1 and C3 remain.
"""
from __future__ import annotations

import pandas as pd

from ecowave.scoring.segmentation import confirming_curves

CRITERIA = [
    ("C1", "synchronisation_multi_courbes", 0.5),
    ("C3", "robustesse_des_fenetres", 0.5),
]
WEIGHTS = {code: w for code, _, w in CRITERIA}

# Null-calibration of the auto-computed criteria.
DEFAULT_NULL_DRAWS = 500
DEFAULT_SEED = 0
DEFAULT_ALPHA = 0.05

# Verdict thresholds on the C1/C3 sum (weights sum to 1 → max score = 3).
STRONG_MIN = 2.2
USABLE_MIN = 1.5
STRONG_C1_MIN = 2
STRONG_C3_MIN = 2


def _computed_criteria(panel: pd.DataFrame, model: dict, n_draws: int, seed: int,
                       alpha: float) -> dict[str, tuple[int, str]]:
    """C1 (synchronisation) and C3 (dual-window robustness), null-calibrated."""
    ev = confirming_curves(panel, model, n_draws=n_draws, seed=seed, alpha=alpha)
    confirm, robust, n = ev["confirm_pre"], ev["robust_both"], ev["n_curves"]

    c1 = min(3, len(confirm))
    c1_note = (f"{len(confirm)} courbe(s) battant le nul (alpha={alpha}) sur la "
               f"séparation inter-phases pré-crise: {sorted(confirm)}")

    share = (len(robust) / n) if n else 0.0
    if share >= 0.5:
        c3 = 3
    elif share >= 0.3:
        c3 = 2
    elif share > 0:
        c3 = 1
    else:
        c3 = 0
    c3_note = (f"{len(robust)}/{n} courbe(s) robustes sur les 2 fenêtres "
               f"au-delà du nul {sorted(robust)} (part={share:.2f})")
    return {"C1": (c1, c1_note), "C3": (c3, c3_note)}


def compute_model_scores(panel: pd.DataFrame, annotations=None,
                          models: dict | None = None, *,
                          n_draws: int = DEFAULT_NULL_DRAWS, seed: int = DEFAULT_SEED,
                          alpha: float = DEFAULT_ALPHA) -> pd.DataFrame:
    """Compute C1/C3 for every model in ``models``.

    ``annotations`` is kept as a parameter for backward signature compatibility
    but is unused; the analyst-grading layer has been retired.
    """
    models = models or {}
    rows = []
    for model_code, model in models.items():
        computed = _computed_criteria(panel, model, n_draws, seed, alpha)
        for code, label, weight in CRITERIA:
            raw, note = computed[code]
            rows.append({
                "model_code": model_code, "criterion_code": code,
                "criterion_label": label, "raw_score": raw, "weight": weight,
                "weighted_score": round(raw * weight, 4),
                "status": "computed", "notes": note,
            })
    return pd.DataFrame(rows)


def db_insertable_rows(scores: pd.DataFrame) -> list[dict]:
    filled = scores[scores["status"].isin({"computed", "annotated"})]
    return [
        {
            "model_code": r.model_code, "criterion_code": r.criterion_code,
            "raw_score": int(r.raw_score), "weight": float(r.weight),
            "weighted_score": float(r.weighted_score), "notes": r.notes,
        }
        for r in filled.itertuples()
    ]


def _verdict_for(raw_by_crit: dict[str, int]) -> tuple[float, str]:
    total = round(sum(raw_by_crit[c] * WEIGHTS[c] for c in raw_by_crit), 4)
    if raw_by_crit.get("C1", 0) <= 1 or raw_by_crit.get("C3", 0) == 0:
        return total, "rejected"
    if (total >= STRONG_MIN and raw_by_crit["C1"] >= STRONG_C1_MIN
            and raw_by_crit["C3"] >= STRONG_C3_MIN):
        return total, "strong"
    if total >= USABLE_MIN:
        return total, "usable"
    return total, "fragile"


def model_verdicts(scores: pd.DataFrame) -> pd.DataFrame:
    """Verdict per model based on C1 + C3."""
    rows = []
    for model_code, grp in scores.groupby("model_code"):
        filled = grp[grp["status"].isin({"computed", "annotated"})]
        raw_by_crit = {r.criterion_code: int(r.raw_score) for r in filled.itertuples()}
        complete = set(raw_by_crit) == {c for c, _, _ in CRITERIA}
        if complete:
            total, verdict = _verdict_for(raw_by_crit)
            note = "C1 + C3 computed against the surrogate null"
        else:
            total = round(float(filled["weighted_score"].sum()), 4)
            verdict = "blocked"
            missing = sorted({c for c, _, _ in CRITERIA} - set(raw_by_crit))
            note = f"blocked: criteria missing: {missing}"
        rows.append({
            "model_code": model_code, "weighted_score": total, "complete": complete,
            "verdict": verdict, "notes": note,
        })
    return pd.DataFrame(rows)
