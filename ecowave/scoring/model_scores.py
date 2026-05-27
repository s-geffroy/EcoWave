from __future__ import annotations

import pandas as pd

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

# Criteria that require analyst judgement and cannot be honestly auto-derived in V1.
QUALITATIVE = {"C2", "C4", "C5", "C6"}

HIGH_STRESS = 75.0
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


def compute_model_scores(panel: pd.DataFrame) -> pd.DataFrame:
    """Compute C1/C3 from real panel data; leave qualitative criteria blocked (no fabrication)."""
    rows = []
    for model_code, model in MODELS.items():
        c1, c1_note = _c1_synchronisation(panel, model)
        c3, c3_note = _c3_robustness(panel, model)
        computed = {"C1": (c1, c1_note), "C3": (c3, c3_note)}
        for code, label, weight in CRITERIA:
            if code in computed:
                raw, note = computed[code]
                rows.append({
                    "model_code": model_code,
                    "criterion_code": code,
                    "criterion_label": label,
                    "raw_score": raw,
                    "weight": weight,
                    "weighted_score": round(raw * weight, 4),
                    "status": "computed",
                    "notes": note,
                })
            else:
                rows.append({
                    "model_code": model_code,
                    "criterion_code": code,
                    "criterion_label": label,
                    "raw_score": None,
                    "weight": weight,
                    "weighted_score": None,
                    "status": "blocked",
                    "notes": "qualitative criterion: requires analyst judgement; not auto-scored in V1",
                })
    return pd.DataFrame(rows)


def db_insertable_rows(scores: pd.DataFrame) -> list[dict]:
    """Only honestly-computed integer rows (schema forbids NULL raw_score)."""
    computed = scores[scores["status"] == "computed"]
    return [
        {
            "model_code": r.model_code,
            "criterion_code": r.criterion_code,
            "raw_score": int(r.raw_score),
            "weight": float(r.weight),
            "weighted_score": float(r.weighted_score),
            "notes": r.notes,
        }
        for r in computed.itertuples()
    ]


def model_verdicts(scores: pd.DataFrame) -> pd.DataFrame:
    """Each model stays 'blocked' while any criterion is blocked. Partial weighted total reported."""
    rows = []
    for model_code, grp in scores.groupby("model_code"):
        blocked = (grp["status"] == "blocked").any()
        partial_total = grp.loc[grp["status"] == "computed", "weighted_score"].sum()
        rows.append({
            "model_code": model_code,
            "partial_weighted_score": round(float(partial_total), 4),
            "verdict": "blocked" if blocked else "usable",
            "notes": "verdict bloqué: critères qualitatifs C2/C4/C5/C6 non évalués + courbes S/I absentes",
        })
    return pd.DataFrame(rows)
