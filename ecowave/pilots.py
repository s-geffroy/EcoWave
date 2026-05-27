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

# --- Pilot 3 (2018-2022): COVID-19 shock and the reflation aftermath ---

MODEL_A_2020 = {
    "name": "Unique cycle 2018-2022",
    "hypothesis": "2018-2022 forms one large Elliott-like cycle.",
    "candidate_phases": [
        ("wave_1", "2018-01", "2018-12"),
        ("wave_2", "2019-01", "2020-01"),
        ("wave_3", "2020-02", "2020-05"),
        ("wave_4", "2020-06", "2021-06"),
        ("wave_5", "2021-07", "2022-12"),
    ],
}

MODEL_B_2020 = {
    "name": "Nested cycles: COVID crash 2020 and reflation 2021-2022",
    "hypothesis": "The COVID crash/rebound and the 2021-2022 reflation/inflation phase are linked but distinct cycles.",
    "candidate_phases": [
        ("cycle_1_covid", "2020-01", "2020-12"),
        ("cycle_2_reflation", "2021-01", "2022-12"),
    ],
}

MODEL_C_2020 = {
    "name": "Elliott limited to the acute 2020 COVID shock",
    "hypothesis": "Elliott is valid only during the acute Feb-May 2020 panic; Dow handles the rest.",
    "candidate_phases": [
        ("acute_shock", "2020-02", "2020-05"),
    ],
}

# --- Pilot 4 (2021-2024): energy/inflation shock and the rate-hike adjustment ---

MODEL_A_2022 = {
    "name": "Unique cycle 2021-2024",
    "hypothesis": "2021-2024 forms one large Elliott-like cycle.",
    "candidate_phases": [
        ("wave_1", "2021-01", "2021-09"),
        ("wave_2", "2021-10", "2022-01"),
        ("wave_3", "2022-02", "2022-10"),
        ("wave_4", "2022-11", "2023-06"),
        ("wave_5", "2023-07", "2024-12"),
    ],
}

MODEL_B_2022 = {
    "name": "Nested cycles: energy/inflation 2022 and rate-hike adjustment 2023-2024",
    "hypothesis": "The 2022 energy/inflation shock and the 2023-2024 monetary adjustment are linked but distinct cycles.",
    "candidate_phases": [
        ("cycle_1_energy_inflation", "2021-09", "2022-12"),
        ("cycle_2_rate_adjustment", "2023-01", "2024-12"),
    ],
}

MODEL_C_2022 = {
    "name": "Elliott limited to the acute 2022 energy shock",
    "hypothesis": "Elliott is valid only during the acute Feb-Oct 2022 energy/inflation panic; Dow handles the rest.",
    "candidate_phases": [
        ("acute_shock", "2022-02", "2022-10"),
    ],
}

# --- Pilot 5 (1998-2003): dot-com bust (data-coverage caveats, see notes) ---

MODEL_A_2000 = {
    "name": "Unique cycle 1998-2003",
    "hypothesis": "1998-2003 forms one large Elliott-like cycle.",
    "candidate_phases": [
        ("wave_1", "1998-01", "1998-09"),
        ("wave_2", "1998-10", "2000-02"),
        ("wave_3", "2000-03", "2001-09"),
        ("wave_4", "2001-10", "2002-07"),
        ("wave_5", "2002-08", "2003-12"),
    ],
}

MODEL_B_2000 = {
    "name": "Nested cycles: dot-com bust 2000-2001 and jobless recovery 2002-2003",
    "hypothesis": "The dot-com bust and the 2002-2003 credit-event recovery are linked but distinct cycles.",
    "candidate_phases": [
        ("cycle_1_dotcom_bust", "2000-03", "2001-12"),
        ("cycle_2_recovery", "2002-01", "2003-12"),
    ],
}

MODEL_C_2000 = {
    "name": "Elliott limited to the acute 2000-2001 bust",
    "hypothesis": "Elliott is valid only during the acute Sep-2000..Nov-2001 bust; Dow handles the rest.",
    "candidate_phases": [
        ("acute_shock", "2000-09", "2001-11"),
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
    # Optional per-pilot reference-window overrides (else the manifest windows apply).
    precrisis: tuple[str, str] | None = None
    structural: tuple[str, str] | None = None
    # Crisis dating intervals (month-start, month-end) for out-of-sample EWS labels.
    crisis_months: tuple[tuple[str, str], ...] = ()
    # Pre-registration / out-of-sample discipline (see methodology/improvement_roadmap.md).
    registered_at: str | None = None
    holdout: bool = False
    notes: str = ""


PILOTS: dict[str, Pilot] = {
    "2008": Pilot(
        code="2008",
        title="Global financial crisis + euro sovereign crisis",
        panel_start="2007-01",
        panel_end="2012-12",
        dow_context="2001-2006 (accumulation / primary regime context)",
        champion="B",
        models={"A": MODEL_A, "B": MODEL_B, "C": MODEL_C},
        crisis_months=(("2007-08", "2009-06"), ("2010-05", "2012-09")),
        notes="In-sample design pilot (NBER 2007-12..2009-06; euro sovereign 2010-2012).",
    ),
    "2016": Pilot(
        code="2016",
        title="Late euro sovereign crisis, recovery and 2015-2016 shocks",
        panel_start="2011-01",
        panel_end="2016-12",
        dow_context="2009-2010 (post-crash recovery context)",
        champion="B",
        models={"A": MODEL_A_2016, "B": MODEL_B_2016, "C": MODEL_C_2016},
        crisis_months=(("2011-07", "2012-09"),),
        notes="Transferability pilot (C6).",
    ),
    "2020": Pilot(
        code="2020",
        title="COVID-19 shock and the reflation aftermath",
        panel_start="2018-01",
        panel_end="2022-12",
        dow_context="2013-2017 (post-euro-crisis expansion context)",
        champion="B",
        models={"A": MODEL_A_2020, "B": MODEL_B_2020, "C": MODEL_C_2020},
        # Pre-crisis 1990-2006 and structural 1990-2019 are both clean baselines for 2020+.
        crisis_months=(("2020-02", "2020-12"),),
        registered_at="2026-05-27",
        holdout=True,
        notes="OUT-OF-SAMPLE HOLDOUT: phases/annotations pre-registered before normalisation. "
              "NBER recession 2020-02..2020-04.",
    ),
    "2022": Pilot(
        code="2022",
        title="Energy/inflation shock and the rate-hike adjustment",
        panel_start="2021-01",
        panel_end="2024-12",
        dow_context="2016-2019 (late-cycle expansion context)",
        champion="B",
        models={"A": MODEL_A_2022, "B": MODEL_B_2022, "C": MODEL_C_2022},
        crisis_months=(("2022-02", "2022-12"),),
        registered_at="2026-05-27",
        holdout=True,
        notes="OUT-OF-SAMPLE HOLDOUT. Russia-Ukraine energy shock + inflation peak 2022.",
    ),
    "2000": Pilot(
        code="2000",
        title="Dot-com bust (data-coverage caveats)",
        panel_start="1998-01",
        panel_end="2003-12",
        dow_context="1994-1997 (pre-bubble expansion context)",
        champion="B",
        models={"A": MODEL_A_2000, "B": MODEL_B_2000, "C": MODEL_C_2000},
        # Pre-crisis 1990-2006 contains the bust; override to a clean pre-2000 baseline.
        precrisis=("1990-01", "1998-12"),
        structural=("1990-01", "2019-12"),
        crisis_months=(("2000-09", "2002-10"),),
        notes="PARTIAL COVERAGE: variables are US/EA-centric; ECB CISS starts 1999, so the "
              "D-curve is unnormalised before 1999. NBER recession 2001-03..2001-11.",
    ),
}


def get_pilot(code: str) -> Pilot:
    if code not in PILOTS:
        raise ValueError(f"Unknown pilot '{code}'. Available: {sorted(PILOTS)}")
    return PILOTS[code]
