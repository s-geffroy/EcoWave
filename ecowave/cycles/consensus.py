"""Gate 2 — phase consensus across methods.

For a given (group, cycle, as_of) cell, the CPV publishes the modal phase
only if at least ``min_agreement`` admitted methods agree. Otherwise the
cell is published as ``disputed`` — disagreement is information, not a
failure mode to hide.

The admitted method panel is per-band (configured in
``ecowave.cycles.bands.CYCLE_BANDS[band]["methods"]``): D and G are excluded
from the Kitchin band, and D is excluded from Kondratieff — both methods
collapse to nearly constant phases on those bands due to either too-few
change-points (D on Kondratieff) or too-many (D on Kitchin), or the
inability to date a complete cycle at the endpoint (G on Kitchin).
"""
from __future__ import annotations

from collections import Counter
from typing import Iterable

from ecowave.cycles.bands import MIN_METHOD_AGREEMENT


def compute_phase_consensus(phases_by_model: dict[str, str],
                            min_agreement: int = MIN_METHOD_AGREEMENT,
                            allowed_methods: Iterable[str] | None = None,
                            ) -> tuple[str, dict]:
    """Aggregate per-method phase labels into a single consensus.

    ``phases_by_model`` maps model_code → phase label (one of expansion /
    peak / contraction / trough / rejected). When ``allowed_methods`` is
    provided, only those method codes contribute to the consensus (the
    others are dropped — their votes are still persisted in
    ``cycle_consensus`` for transparency but do not influence Gate 2).

    Returns ``(consensus_label, votes)`` where votes is a dict of label →
    count restricted to the admitted panel. If fewer than ``min_agreement``
    admitted models agree on the modal phase, the consensus is
    ``"disputed"``.
    """
    allowlist = set(allowed_methods) if allowed_methods is not None else None
    valid = {
        m: p for m, p in phases_by_model.items()
        if p in ("expansion", "peak", "contraction", "trough")
        and (allowlist is None or m in allowlist)
    }
    votes = dict(Counter(valid.values()))
    if not votes:
        return "rejected", votes
    modal, count = max(votes.items(), key=lambda kv: kv[1])
    if count >= min_agreement:
        return modal, votes
    return "disputed", votes
