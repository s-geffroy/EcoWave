from __future__ import annotations

import pandas as pd

from ecowave.scoring.annotations import Annotation
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

HIGH_STRESS = 75.0
CHAMPION = "B"
MODELS = {"A": MODEL_A, "B": MODEL_B, "C": MODEL_C}


def _months_in_model(model: dict) -> set[str]:
    months: set[str] = set()
    for _, start, end in model["candidate_phases"]:
        rng = pd.period_range(start=start, end=end, freq="M")
        months.update(d.strftime("%Y-%m") for d in rng)
    return months


def _c1_synchronisation(panel: pd.DataFrame, model: dict) -> tuple[int, str]:
    months = _months_in_model(model)
    sub = panel[(panel["month"].isin(months)) & (panel["status"] == "available")].copy()
    sub["curve"] = sub["variable_code"].str[0]
    confirming = set()
    for curve, grp in sub.groupby("curve"):
        if (grp["stress_precrisis"] >= HIGH_STRESS).sum() >= 2:
            confirming.add(curve)
    n = len(confirming)
    score = min(3, n)
    return score, f"{n} courbe(s) confirmante(s) (>=2 mois stress>= {HIGH_STRESS:.0f}): {sorted(confirming)}"


def _c3_robustness(panel: pd.DataFrame, model: dict) -> tuple[int, str]:
    months = _months_in_model(model)
    sub = panel[(panel["month"].isin(months)) & (panel["status"] == "available")]
    both = sub.dropna(subset=["stress_precrisis", "stress_structural"])
    if both.empty:
        return 0, "aucune observation normalisée sur les deux fenêtres"
    agree = ((both["stress_precrisis"] >= HIGH_STRESS) & (both["stress_structural"] >= HIGH_STRESS)).mean()
    if agree >= 0.5:
        score = 3
    elif agree >= 0.3:
        score = 2
    elif agree > 0:
        score = 1
    else:
        score = 0
    return score, f"part d'observations robustes sur les 2 fenêtres = {agree:.2f}"


def compute_model_scores(panel: pd.DataFrame,
                         annotations: dict[tuple[str, str], Annotation] | None = None,
                         models: dict | None = None) -> pd.DataFrame:
    """Compute C1/C3 from data; fill C2/C4/C5/C6 from analyst annotations when present."""
    annotations = annotations or {}
    models = models if models is not None else MODELS
    rows = []
    for model_code, model in models.items():
        c1, c1_note = _c1_synchronisation(panel, model)
        c3, c3_note = _c3_robustness(panel, model)
        computed = {"C1": (c1, c1_note), "C3": (c3, c3_note)}
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
    # Automatic rejection rules (scoring_rules.md).
    if raw_by_crit["C1"] <= 1 or raw_by_crit["C3"] == 0 or raw_by_crit["C5"] == 0:
        return total, "rejected"
    if total >= 2.4:
        return total, "strong"
    if total >= 1.8:
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


def champion_challenger(scores: pd.DataFrame, verdicts: pd.DataFrame, champion: str = CHAMPION) -> str:
    """Adjudicate champion vs challengers only when all models are complete (≥4/6 to dethrone)."""
    if not verdicts["complete"].all():
        return ("Champion/challenger non tranché: les annotations qualitatives sont "
                "incomplètes pour au moins un modèle (verdict provisoire/bloqué).")
    pivot = (scores[scores["status"].isin({"computed", "annotated"})]
             .pivot(index="model_code", columns="criterion_code", values="raw_score"))
    challengers = [m for m in pivot.index if m != champion]
    lines = []
    for challenger in challengers:
        wins = int((pivot.loc[challenger] > pivot.loc[champion]).sum())
        outcome = f"détrône {champion}" if wins >= 4 else f"ne détrône pas {champion}"
        lines.append(f"{challenger} gagne sur {wins}/6 critères → {outcome}.")
    return f"Champion provisoire: {champion}. " + " ".join(lines)
