"""CPV (Cycle Position Vector) — multi-cycle decomposition.

Combines four falsifiable methods (CF band-pass, Morlet wavelet,
Markov-switching, Bry-Boschan) on World Bank macro indicators to position
the world (and per income group) in the canonical Kitchin / Juglar /
Kuznets / Kondratieff cycles. Layered falsifiability via three gates:

1. Existence — AR(1) bootstrap null per (group, variable, band)
2. Consensus — at least 3 of 4 methods agree on the phase label
3. Universality — at least 4 of 5 income groups concord

See ``methodology/multi_cycle_decomposition.md`` and
``methodology/cycle_methods_survey.md``.
"""
from ecowave.cycles.bands import CYCLE_BANDS, GROUPS, INCOME_GROUPS
from ecowave.cycles.phase import PHASE_LABELS, classify_phase, hilbert_phase

__all__ = [
    "CYCLE_BANDS",
    "GROUPS",
    "INCOME_GROUPS",
    "PHASE_LABELS",
    "classify_phase",
    "hilbert_phase",
]
