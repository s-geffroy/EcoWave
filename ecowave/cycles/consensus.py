"""Gate 2 — phase consensus across methods.

For a given (group, cycle, as_of) cell, the CPV publishes the modal phase
only if at least ``MIN_METHOD_AGREEMENT`` methods agree. Otherwise the cell
is published as ``disputed`` — disagreement is information, not a failure
mode to hide.
"""
from __future__ import annotations

from collections import Counter

from ecowave.cycles.bands import MIN_METHOD_AGREEMENT


def compute_phase_consensus(phases_by_model: dict[str, str],
                            min_agreement: int = MIN_METHOD_AGREEMENT) -> tuple[str, dict]:
    """Aggregate per-method phase labels into a single consensus.

    ``phases_by_model`` maps model_code → phase label (one of expansion / peak /
    contraction / trough / rejected). Returns ``(consensus_label, votes)``
    where votes is a dict of label → count. If fewer than ``min_agreement``
    models agree on the modal phase, the consensus is ``"disputed"``.
    """
    valid = {m: p for m, p in phases_by_model.items()
             if p in ("expansion", "peak", "contraction", "trough")}
    votes = dict(Counter(valid.values()))
    if not votes:
        return "rejected", votes
    modal, count = max(votes.items(), key=lambda kv: kv[1])
    if count >= min_agreement:
        return modal, votes
    return "disputed", votes
