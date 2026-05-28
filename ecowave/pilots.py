"""Crisis-window pilot definitions for the CPV pipeline.

Each pilot is a labelled time window with optional pre-crisis / structural
reference-window overrides and a tuple of ``crisis_months`` used by the EWS
AUROC validation. The four CPV votant methods (D, E, F, G) run on every pilot
unchanged; there are no per-pilot model hypotheses.

Holdout pilots carry a ``registered_at`` timestamp and a ``holdout`` flag for
out-of-sample discipline (see ``methodology/cycle_validation_rules.md``).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Pilot:
    code: str
    title: str
    panel_start: str
    panel_end: str
    # Optional per-pilot reference-window overrides (else manifest windows apply).
    precrisis: tuple[str, str] | None = None
    structural: tuple[str, str] | None = None
    # Crisis dating intervals (month-start, month-end) for out-of-sample EWS labels.
    crisis_months: tuple[tuple[str, str], ...] = ()
    # Pre-registration / out-of-sample discipline.
    registered_at: str | None = None
    holdout: bool = False
    notes: str = ""


PILOTS: dict[str, Pilot] = {
    "2008": Pilot(
        code="2008",
        title="Global financial crisis + euro sovereign crisis",
        panel_start="2007-01",
        panel_end="2012-12",
        crisis_months=(("2007-08", "2009-06"), ("2010-05", "2012-09")),
        notes="In-sample design pilot (NBER 2007-12..2009-06; euro sovereign 2010-2012).",
    ),
    "2016": Pilot(
        code="2016",
        title="Late euro sovereign crisis, recovery and 2015-2016 shocks",
        panel_start="2011-01",
        panel_end="2016-12",
        crisis_months=(("2011-07", "2012-09"),),
        notes="Transferability test.",
    ),
    "2020": Pilot(
        code="2020",
        title="COVID-19 shock and the reflation aftermath",
        panel_start="2018-01",
        panel_end="2022-12",
        crisis_months=(("2020-02", "2020-12"),),
        registered_at="2026-05-27",
        holdout=True,
        notes="OUT-OF-SAMPLE HOLDOUT: window pre-registered before normalisation. "
              "NBER recession 2020-02..2020-04.",
    ),
    "2022": Pilot(
        code="2022",
        title="Energy/inflation shock and the rate-hike adjustment",
        panel_start="2021-01",
        panel_end="2024-12",
        crisis_months=(("2022-02", "2023-03"),),
        registered_at="2026-05-27",
        holdout=True,
        notes="OUT-OF-SAMPLE HOLDOUT: post-Ukraine, post-Fed-hike cycle.",
    ),
    "2000": Pilot(
        code="2000",
        title="Dot-com bust",
        panel_start="1998-01",
        panel_end="2003-12",
        crisis_months=(("2001-03", "2001-11"),),
        notes="Earlier reference pilot; coverage limited before 2000 for some indicators.",
    ),
}


def get_pilot(code: str) -> Pilot:
    if code not in PILOTS:
        raise ValueError(f"Unknown pilot '{code}'. Available: {sorted(PILOTS.keys())}")
    return PILOTS[code]
