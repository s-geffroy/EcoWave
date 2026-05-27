from __future__ import annotations

from dataclasses import dataclass

from ecowave.waves.model_a_unique_cycle import MODEL_A
from ecowave.waves.model_b_nested_cycles import MODEL_B
from ecowave.waves.model_c_acute_shock import MODEL_C

# --- Pilot 2 (2011-2016): late euro sovereign crisis, recovery, 2015-2016 shocks ---

MODEL_A_2016 = {
    "name": "Unique cycle 2011-2016",
    "hypothesis": "2011-2016 forms one large Elliott-like cycle.",
    "candidate_phases": [
        ("wave_1", "2011-01", "2012-07"),
        ("wave_2", "2012-08", "2013-12"),
        ("wave_3", "2014-01", "2014-12"),
        ("wave_4", "2015-01", "2015-09"),
        ("wave_5", "2015-10", "2016-12"),
    ],
}

MODEL_B_2016 = {
    "name": "Nested cycles 2011-2012 and 2013-2016",
    "hypothesis": "Acute euro sovereign crisis and the recovery/aftershock phase are linked but distinct cycles.",
    "candidate_phases": [
        ("cycle_1_euro_acute", "2011-01", "2012-12"),
        ("cycle_2_recovery_aftershocks", "2013-01", "2016-12"),
    ],
}

MODEL_C_2016 = {
    "name": "Elliott limited to the acute 2011-2012 euro shock",
    "hypothesis": "Elliott is valid only during the acute 2011-2012 sovereign panic; Dow handles the rest.",
    "candidate_phases": [
        ("acute_shock", "2011-07", "2012-09"),
    ],
}


@dataclass(frozen=True)
class Pilot:
    code: str
    title: str
    panel_start: str
    panel_end: str
    dow_context: str
    champion: str
    models: dict


PILOTS: dict[str, Pilot] = {
    "2008": Pilot(
        code="2008",
        title="Global financial crisis + euro sovereign crisis",
        panel_start="2007-01",
        panel_end="2012-12",
        dow_context="2001-2006 (accumulation / primary regime context)",
        champion="B",
        models={"A": MODEL_A, "B": MODEL_B, "C": MODEL_C},
    ),
    "2016": Pilot(
        code="2016",
        title="Late euro sovereign crisis, recovery and 2015-2016 shocks",
        panel_start="2011-01",
        panel_end="2016-12",
        dow_context="2009-2010 (post-crash recovery context)",
        champion="B",
        models={"A": MODEL_A_2016, "B": MODEL_B_2016, "C": MODEL_C_2016},
    ),
}


def get_pilot(code: str) -> Pilot:
    if code not in PILOTS:
        raise ValueError(f"Unknown pilot '{code}'. Available: {sorted(PILOTS)}")
    return PILOTS[code]
