"""Per-band Gate 2 method weighting (Roadmap #11).

The methodology surfaced in the 2026-05 Path 5 run: PELT (D) reports
nearly constant `expansion` on Kitchin (cycle period << typical PELT
segment length) and Bry-Boschan (G) reports nearly constant
`contraction` (cycle insufficient at the endpoint). Both are dropped
from the Kitchin consensus panel; D is also dropped from Kondratieff
(only ~1.1-1.65 cycles fit a 66y panel — PELT collapses to a single
segment). Juglar and Kuznets retain all four methods.

These tests pin the behaviour of `compute_phase_consensus` under the
new `allowed_methods` panel + `min_agreement` threshold.
"""
from __future__ import annotations

import pytest

from ecowave.cycles.bands import CYCLE_BANDS
from ecowave.cycles.consensus import compute_phase_consensus


def test_kitchin_panel_uses_only_f_and_e():
    """Kitchin band admits F+E. D='expansion' / G='contraction' are dropped.

    For USA on 2026-05 the raw votes were
    D=expansion / E=contraction / F=contraction / G=contraction;
    under the new panel F+E both vote contraction → consensus contraction.
    The old 4-method panel needed 3/4 agreement; the new 2-method panel
    needs 2/2 (unanimity of admitted methods).
    """
    raw = {"D": "expansion", "E": "contraction", "F": "contraction",
           "G": "contraction"}
    band = CYCLE_BANDS["kitchin"]
    label, votes = compute_phase_consensus(
        raw, allowed_methods=band["methods"],
        min_agreement=band["min_agreement"],
    )
    assert label == "contraction"
    # D and G are excluded from the vote count.
    assert votes == {"contraction": 2}


def test_kitchin_panel_publishes_peak_when_f_and_e_concord():
    """EA / G7Q / OECDQ in 2026-05 had F=peak / E=peak — newly published."""
    raw = {"D": "expansion", "E": "peak", "F": "peak", "G": "contraction"}
    band = CYCLE_BANDS["kitchin"]
    label, votes = compute_phase_consensus(
        raw, allowed_methods=band["methods"],
        min_agreement=band["min_agreement"],
    )
    assert label == "peak"
    assert votes == {"peak": 2}


def test_kitchin_panel_stays_disputed_when_f_and_e_disagree():
    """GBR / JPN in 2026-05 had F and E disagree — must stay disputed."""
    raw = {"D": "expansion", "E": "contraction", "F": "peak",
           "G": "contraction"}
    band = CYCLE_BANDS["kitchin"]
    label, _votes = compute_phase_consensus(
        raw, allowed_methods=band["methods"],
        min_agreement=band["min_agreement"],
    )
    assert label == "disputed"


def test_juglar_panel_keeps_all_four_methods():
    """Juglar band admits all 4 methods; needs 3 of 4 to agree."""
    raw = {"D": "peak", "E": "contraction", "F": "contraction",
           "G": "contraction"}
    band = CYCLE_BANDS["juglar"]
    label, votes = compute_phase_consensus(
        raw, allowed_methods=band["methods"],
        min_agreement=band["min_agreement"],
    )
    assert label == "contraction"
    assert votes == {"peak": 1, "contraction": 3}


def test_juglar_split_remains_disputed():
    """USA Juglar 2026-05: D=contraction, E=trough, F=contraction,
    G=expansion. Modal=contraction with 2 votes; needs 3 → disputed."""
    raw = {"D": "contraction", "E": "trough", "F": "contraction",
           "G": "expansion"}
    band = CYCLE_BANDS["juglar"]
    label, _votes = compute_phase_consensus(
        raw, allowed_methods=band["methods"],
        min_agreement=band["min_agreement"],
    )
    assert label == "disputed"


def test_kondratieff_panel_drops_d():
    """Kondratieff admits E+F+G (drops D). Majority of 3 = 2 agreements.

    GBR 2026-05 had D=trough, E=expansion, F=peak, G=expansion;
    under the new panel E+G both vote expansion → consensus expansion.
    The previous 4-method panel needed 3/4, so this cell was disputed.
    """
    raw = {"D": "trough", "E": "expansion", "F": "peak", "G": "expansion"}
    band = CYCLE_BANDS["kondratieff"]
    label, votes = compute_phase_consensus(
        raw, allowed_methods=band["methods"],
        min_agreement=band["min_agreement"],
    )
    assert label == "expansion"
    assert votes == {"expansion": 2, "peak": 1}


def test_legacy_full_panel_call_still_works():
    """Backwards-compat: calling without ``allowed_methods`` uses all
    submitted methods and the default 3-of-4 threshold."""
    raw = {"D": "expansion", "E": "expansion", "F": "expansion",
           "G": "expansion"}
    label, votes = compute_phase_consensus(raw)
    assert label == "expansion"
    assert votes == {"expansion": 4}
