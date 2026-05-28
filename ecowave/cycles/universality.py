"""Gate 3 — cross-group concordance test.

A cycle is qualified ``universal`` for a given month only if ≥ ``MIN_GROUP_CONCORDANCE``
of the income groups (WLD + HIC + UMC + LMC + LIC) share the same phase. This
applies the transferability criterion (C6 in the EcoWave score grammar) to the
income-group dimension instead of the temporal dimension.
"""
from __future__ import annotations

from collections import Counter

from ecowave.cycles.bands import INCOME_GROUPS, MIN_GROUP_CONCORDANCE


def compute_cross_group_concordance(phases_by_group: dict[str, str],
                                    min_groups: int = MIN_GROUP_CONCORDANCE,
                                    income_only: bool = True) -> dict:
    """Return universality verdict for a given cycle across income groups.

    ``phases_by_group`` maps group_code → phase label. If ``income_only`` is
    True (default), we restrict to ('WLD',) + INCOME_GROUPS. Otherwise the
    test runs on whatever keys are present.
    """
    if income_only:
        keys = ("WLD",) + INCOME_GROUPS
        subset = {k: phases_by_group[k] for k in keys if k in phases_by_group}
    else:
        subset = dict(phases_by_group)

    valid = {k: v for k, v in subset.items()
             if v in ("expansion", "peak", "contraction", "trough")}
    counts = Counter(valid.values())
    if not counts:
        return {"universal": 0, "modal_phase": "rejected", "n_groups_concording": 0,
                "n_groups_total": len(subset)}
    modal, n_concord = max(counts.items(), key=lambda kv: kv[1])
    universal = 1 if n_concord >= min_groups else 0
    return {
        "universal": universal,
        "modal_phase": modal,
        "n_groups_concording": int(n_concord),
        "n_groups_total": len(subset),
    }
