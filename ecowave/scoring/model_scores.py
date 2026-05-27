from __future__ import annotations

import pandas as pd

from ecowave.scoring.annotations import Annotation
from ecowave.scoring.segmentation import confirming_curves
from ecowave.waves.model_a_unique_cycle import MODEL_A
from ecowave.waves.model_b_nested_cycles import MODEL_B
from ecowave.waves.model_c_acute_shock import MODEL_C

CRITERIA = [
    ("C1", "synchronisation_multi_courbes", 0.25),
    ("C2", "clarte_des_ruptures", 0.20),
    ("C3", "robustesse_des_fenetres", 0.20),
    ("C4", "parcimonie", 0.10),
    ("C5", "valeur_ajoutee_vs_chronologie", 0.15),
    ("C6", "transferabilite_2011_2016", 0.10),
]
WEIGHTS = {code: w for code, _, w in CRITERIA}

# Criteria that require analyst judgement (filled via annotations, not auto-derived).
QUALITATIVE = {"C2", "C4", "C5", "C6"}

CHAMPION = "B"
MODELS = {"A": MODEL_A, "B": MODEL_B, "C": MODEL_C}

# Null-calibration of the auto-computed criteria C1/C3 (see scoring/segmentation.py).
DEFAULT_NULL_DRAWS = 500
DEFAULT_SEED = 0
DEFAULT_ALPHA = 0.05

# Verdict thresholds, recalibrated for the null-calibrated C1/C3 scale: C1/C3 are now
# hard to score high (they must beat a surrogate null), so 'strong' additionally
# requires the falsifiable evidence to be solid (C1≥2 and C3≥2), not just a strong
# narrative. T is the weighted total on a 0-3 scale.
STRONG_MIN = 2.2
USABLE_MIN = 1.5
STRONG_C1_MIN = 2
STRONG_C3_MIN = 2

# Champion/challenger thresholds.
DETHRONE_WINS = 4          # criteria a challenger must win outright to dethrone
DETHRONE_SOFT_WINS = 3     # relaxed criteria count, valid only if the weighted score diverges
DETHRONE_MARGIN = 0.30     # weighted-score margin (0-3 scale) that relaxes 4/6 to 3/6


def _computed_criteria(panel: pd.DataFrame, model: dict, n_draws: int, seed: int,
                       alpha: float) -> dict[str, tuple[int, str]]:
    """C1 (synchronisation) and C3 (dual-window robustness), calibrated against the null.

    A curve 'confirms' only if its phase-separation (eta-squared) beats the
    (1-alpha) percentile of random segmentations of the same shape — so a random
    segmentation of a crisis window scores ~0 and the champion must earn its score.
    """
    ev = confirming_curves(panel, model, n_draws=n_draws, seed=seed, alpha=alpha)
    confirm, robust, n = ev["confirm_pre"], ev["robust_both"], ev["n_curves"]

    c1 = min(3, len(confirm))
    c1_note = (f"{len(confirm)} courbe(s) battant le nul (alpha={alpha}) sur la séparation "
               f"inter-phases pré-crise: {sorted(confirm)}")

    share = (len(robust) / n) if n else 0.0
    if share >= 0.5:
        c3 = 3
    elif share >= 0.3:
        c3 = 2
    elif share > 0:
        c3 = 1
    else:
        c3 = 0
    c3_note = (f"{len(robust)}/{n} courbe(s) robustes sur les 2 fenêtres au-delà du nul "
               f"{sorted(robust)} (part={share:.2f})")
    return {"C1": (c1, c1_note), "C3": (c3, c3_note)}


def compute_model_scores(panel: pd.DataFrame,
                         annotations: dict[tuple[str, str], Annotation] | None = None,
                         models: dict | None = None, *,
                         n_draws: int = DEFAULT_NULL_DRAWS, seed: int = DEFAULT_SEED,
                         alpha: float = DEFAULT_ALPHA) -> pd.DataFrame:
    """Compute C1/C3 from data; fill C2/C4/C5/C6 from analyst annotations when present."""
    annotations = annotations or {}
    models = models if models is not None else MODELS
    rows = []
    for model_code, model in models.items():
        computed = _computed_criteria(panel, model, n_draws, seed, alpha)
        for code, label, weight in CRITERIA:
            if code in computed:
                raw, note = computed[code]
                status = "computed"
            elif (model_code, code) in annotations:
                ann = annotations[(model_code, code)]
                raw, status = ann.raw_score, "annotated"
                note = f"[{ann.analyst} {ann.date}] {ann.justification}"
            else:
                rows.append({
                    "model_code": model_code, "criterion_code": code, "criterion_label": label,
                    "raw_score": None, "weight": weight, "weighted_score": None,
                    "status": "blocked",
                    "notes": "qualitative criterion: needs analyst annotation (see annotations/)",
                })
                continue
            rows.append({
                "model_code": model_code, "criterion_code": code, "criterion_label": label,
                "raw_score": raw, "weight": weight, "weighted_score": round(raw * weight, 4),
                "status": status, "notes": note,
            })
    return pd.DataFrame(rows)


def db_insertable_rows(scores: pd.DataFrame) -> list[dict]:
    """Honestly-scored integer rows (computed or annotated); schema forbids NULL raw_score."""
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
    # Automatic rejection (scoring_rules.md): falsifiable evidence in ≤1 curve (C1≤1),
    # no dual-window robustness (C3=0), or no added value over chronology (C5=0).
    if raw_by_crit["C1"] <= 1 or raw_by_crit["C3"] == 0 or raw_by_crit["C5"] == 0:
        return total, "rejected"
    # 'strong' demands solid null-calibrated computed evidence, not just narrative:
    # ≥2 curves confirm beyond chance AND dual-window robustness.
    if (total >= STRONG_MIN and raw_by_crit["C1"] >= STRONG_C1_MIN
            and raw_by_crit["C3"] >= STRONG_C3_MIN):
        return total, "strong"
    if total >= USABLE_MIN:
        return total, "usable"
    return total, "fragile"


def model_verdicts(scores: pd.DataFrame) -> pd.DataFrame:
    """Full verdict when all six criteria are filled; otherwise blocked with a partial total."""
    rows = []
    for model_code, grp in scores.groupby("model_code"):
        filled = grp[grp["status"].isin({"computed", "annotated"})]
        raw_by_crit = {r.criterion_code: int(r.raw_score) for r in filled.itertuples()}
        complete = set(raw_by_crit) == {c for c, _, _ in CRITERIA}
        if complete:
            total, verdict = _verdict_for(raw_by_crit)
            note = "all six criteria filled (C1/C3 computed; C2/C4/C5/C6 annotated)"
        else:
            total = round(float(filled["weighted_score"].sum()), 4)
            verdict = "blocked"
            missing = sorted({c for c, _, _ in CRITERIA} - set(raw_by_crit))
            note = f"blocked: criteria not yet annotated: {missing}"
        rows.append({
            "model_code": model_code, "weighted_score": total, "complete": complete,
            "verdict": verdict, "notes": note,
        })
    return pd.DataFrame(rows)


def champion_challenger(scores: pd.DataFrame, verdicts: pd.DataFrame, champion: str = CHAMPION,
                        margin: float = DETHRONE_MARGIN) -> str:
    """Adjudicate champion vs challengers when all models are complete.

    A challenger dethrones the champion if it wins ≥4/6 criteria, OR if it wins ≥3/6
    AND its weighted score exceeds the champion's by at least `margin` (the relaxed rule
    for a clearly diverging weighted score).
    """
    if not verdicts["complete"].all():
        return ("Champion/challenger non tranché: les annotations qualitatives sont "
                "incomplètes pour au moins un modèle (verdict provisoire/bloqué).")
    pivot = (scores[scores["status"].isin({"computed", "annotated"})]
             .pivot(index="model_code", columns="criterion_code", values="raw_score"))
    weighted = verdicts.set_index("model_code")["weighted_score"]
    champ_w = float(weighted[champion])

    lines = []
    dethroners = []
    for challenger in [m for m in pivot.index if m != champion]:
        wins = int((pivot.loc[challenger] > pivot.loc[champion]).sum())
        diff = float(weighted[challenger]) - champ_w
        if wins >= DETHRONE_WINS:
            reason, dethrone = f"≥{DETHRONE_WINS}/6 critères", True
        elif wins >= DETHRONE_SOFT_WINS and diff >= margin:
            reason, dethrone = f"{wins}/6 critères mais score pondéré +{diff:.2f} ≥ {margin}", True
        else:
            reason, dethrone = "", False
        if dethrone:
            dethroners.append(challenger)
            outcome = f"détrône {champion} ({reason})"
        else:
            outcome = f"ne détrône pas {champion}"
        lines.append(f"{challenger}: {wins}/6 critères, score {float(weighted[challenger]):.2f} "
                     f"vs {champ_w:.2f} → {outcome}.")

    if dethroners:
        winner = max(dethroners, key=lambda m: float(weighted[m]))
        header = f"Champion provisoire: {winner} (détrône {champion})."
    else:
        header = f"Champion provisoire: {champion} (conservé)."
    return header + " " + " ".join(lines)
