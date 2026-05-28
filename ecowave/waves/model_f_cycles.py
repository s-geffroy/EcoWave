"""Model F — Christiano-Fitzgerald Juglar band-pass + Hilbert phase.

Model F applies the CPV cycle-band decomposition to a crisis pilot's
composite intensity. For a pilot's panel (5 curves E/D/S/L/I), Model F builds
an equal-weight MA3 intensity (reusing ``model_e._equal_intensity_ma3``),
band-passes it to the Juglar band (7-11 years) — the only band whose period
is short enough to be resolvable inside a 5-7 year pilot window — and converts
the instantaneous Hilbert phase trajectory into ``candidate_phases``.

Falsifiability: a degenerate or non-separable filter output (insufficient
samples or AR(1)-null not rejected) returns a single ``rejected_cycle`` phase.

Reference: Christiano & Fitzgerald (2003); Torrence & Compo (1998); Aguiar-
Conraria & Soares (2014). The Hilbert quadrant rule and AR(1) surrogate
parameters are pre-registered in ``ecowave/cycles/phase.py`` and
``ecowave/cycles/surrogate.py``.
"""
from __future__ import annotations

import pandas as pd

from ecowave.cycles.bands import CYCLE_BANDS
from ecowave.cycles.decompose import cf_bandpass
from ecowave.cycles.phase import classify_phase, hilbert_phase
from ecowave.cycles.surrogate import ar1_bootstrap_null
from ecowave.waves.model_e_markov import _equal_intensity_ma3

JUGLAR_LO = CYCLE_BANDS["juglar"]["lo_years"]
JUGLAR_HI = CYCLE_BANDS["juglar"]["hi_years"]
SAMPLES_PER_YEAR_MONTHLY = 12.0
MIN_PHASE_MONTHS = 3


def _phases_from_labels(months: list[str], labels: list[str],
                        min_run: int = MIN_PHASE_MONTHS) -> list[tuple[str, str, str]]:
    """Group contiguous identical labels into (label, start, end) phases. Short
    runs are merged into the preceding phase, mirroring Model E's behaviour."""
    if not months:
        return []
    phases: list[list] = [[labels[0], months[0], months[0]]]
    for i in range(1, len(months)):
        if labels[i] == phases[-1][0]:
            phases[-1][2] = months[i]
        else:
            phases.append([labels[i], months[i], months[i]])
    # Merge short runs.
    merged: list[list] = []
    for ph in phases:
        if merged and (months.index(ph[2]) - months.index(ph[1]) + 1) < min_run:
            merged[-1][2] = ph[2]
        else:
            merged.append(list(ph))
    return [(p[0], p[1], p[2]) for p in merged]


def fit_model_f(panel: pd.DataFrame, lo_years: float = JUGLAR_LO,
                hi_years: float = JUGLAR_HI,
                n_surrogates: int = 500, alpha: float = 0.05,
                seed: int = 0) -> dict:
    """Fit Model F (CF Juglar band-pass + Hilbert phase) on the panel.

    Returns a dict matching the Model D/E contract:
      {name, hypothesis, candidate_phases, method, ar1_pvalue, ar1_reject,
       fit_status}
    """
    intensity = _equal_intensity_ma3(panel).dropna()
    months = list(intensity.index.astype(str))
    fallback = {
        "name": "Cycle phases (CF Juglar + Hilbert, fallback)",
        "hypothesis": "Crisis is the visible signature of the Juglar (7-11y) "
                      "cycle on the composite intensity — degenerate case.",
        "candidate_phases": [("rejected_cycle", months[0], months[-1])] if months else [],
        "method": "CF[7-11y] + Hilbert",
        "ar1_pvalue": None, "ar1_reject": True,
        "fit_status": "fallback",
    }
    if len(intensity) < int(2 * hi_years * SAMPLES_PER_YEAR_MONTHLY):
        return fallback

    try:
        null = ar1_bootstrap_null(intensity, lo_years=lo_years, hi_years=hi_years,
                                  samples_per_year=SAMPLES_PER_YEAR_MONTHLY,
                                  n_surrogates=n_surrogates, alpha=alpha, seed=seed)
    except Exception as exc:  # noqa: BLE001
        fallback["fit_status"] = f"AR(1) null failed: {exc}"
        return fallback

    if null.reject_cycle:
        fallback["fit_status"] = (f"Juglar band not separable from AR(1) "
                                  f"(p={null.p_value:.3f}).")
        fallback["ar1_pvalue"] = float(null.p_value)
        fallback["ar1_reject"] = True
        return fallback

    try:
        cycle = cf_bandpass(intensity, lo_years=lo_years, hi_years=hi_years,
                            samples_per_year=SAMPLES_PER_YEAR_MONTHLY)
        phi = hilbert_phase(cycle)
    except Exception as exc:  # noqa: BLE001
        fallback["fit_status"] = f"CF/Hilbert decomposition failed: {exc}"
        return fallback

    labels = [classify_phase(p) for p in phi.values]
    phases = _phases_from_labels(months, labels)
    if not phases:
        return fallback

    return {
        "name": f"Cycle phases — CF [{lo_years}–{hi_years}y] + Hilbert"
                f" ({len(phases)} phase(s))",
        "hypothesis": "Crisis is the visible signature of the Juglar cycle on the "
                      "composite intensity; phases are the four Hilbert quadrants "
                      "of the band-passed signal.",
        "candidate_phases": phases,
        "method": f"CF[{lo_years}-{hi_years}y] + Hilbert + AR(1) null",
        "ar1_pvalue": float(null.p_value),
        "ar1_reject": False,
        "fit_status": "ok",
    }
