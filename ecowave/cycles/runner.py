"""End-to-end CPV runner.

Pipeline:
  1. Ingest WB indicators per (group, indicator)
  2. For each (group, cycle band) average the indicator-level bandpassed series
     into one composite signal
  3. Run 4 votant methods: F (CF+Hilbert), G (Bry-Boschan), E (Markov-switching),
     D (PELT) on the composite — each emits a phase label for the as-of date
  4. Apply Gate 1 (AR(1) null), Gate 2 (consensus), Gate 3 (universality)
  5. Persist cycle_positions / cycle_consensus / cycle_universality
  6. Render note + figures
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import typer

from ecowave.config import Settings
from ecowave.cycles.bands import CYCLE_BANDS, GROUPS, INCOME_GROUPS
from ecowave.cycles.consensus import compute_phase_consensus
from ecowave.cycles.decompose import cf_bandpass, morlet_wavelet
from ecowave.cycles.ingest import build_group_panel
from ecowave.cycles.manifest import CycleManifest, load_cycle_manifest
from ecowave.cycles.phase import classify_phase, hilbert_amplitude, hilbert_phase
from ecowave.cycles.report import (
    build_position_table,
    plot_cf_trajectories,
    plot_phase_heatmap,
    plot_wavelet_power,
    render_cycle_position_md,
)
from ecowave.cycles.surrogate import ar1_bootstrap_null
from ecowave.cycles.universality import compute_cross_group_concordance
from ecowave.db import (
    connect,
    finish_ingestion_run,
    get_schema_version,
    init_db,
    migrate_db,
    replace_cycle_consensus,
    replace_cycle_positions,
    replace_cycle_universality,
    start_ingestion_run,
)

DEFAULT_GROUPS_ORDER = ("WLD", "OECD", "HIC", "UMC", "LMC", "LIC", "G7", "BRICS")
SCHEMA_PATH = Path("/app/db/schema.sql")
SEED_PATH = Path("/app/db/seed_variables.sql")
CYCLES_MANIFEST_PATH = Path("/app/cycles_manifest.json")


def _composite_panel(panel: pd.DataFrame) -> pd.Series:
    """Equal-weighted standardized composite across all indicators in the panel.

    Each column is z-scored against its own history, then averaged. NaN-tolerant.
    """
    if panel.empty:
        return pd.Series(dtype=float)
    standardized = (panel - panel.mean(axis=0)) / panel.std(axis=0).replace(0, np.nan)
    return standardized.mean(axis=1, skipna=True)


def _bryboschan_phase_for_endpoint(cycle: pd.Series) -> str:
    """Approximate Bry-Boschan phase at the last observation.

    Locate the most recent peak (local max) and most recent trough (local min)
    with min separation = 2 samples. The phase at the endpoint follows the
    Harding-Pagan convention:
      - last extremum was a peak → contraction
      - last extremum was a trough → expansion
      - slope > 0 in the last 3 samples → expansion
      - slope < 0 in the last 3 samples → contraction
    """
    y = cycle.dropna().to_numpy()
    if y.size < 5:
        return "rejected"
    # Find peaks and troughs via 3-point rule.
    peaks: list[int] = []
    troughs: list[int] = []
    for i in range(2, y.size - 2):
        if y[i] > y[i - 1] and y[i] > y[i - 2] and y[i] > y[i + 1] and y[i] > y[i + 2]:
            peaks.append(i)
        if y[i] < y[i - 1] and y[i] < y[i - 2] and y[i] < y[i + 1] and y[i] < y[i + 2]:
            troughs.append(i)
    last_peak = peaks[-1] if peaks else -1
    last_trough = troughs[-1] if troughs else -1
    if last_peak < 0 and last_trough < 0:
        # Fall back to slope.
        slope = y[-1] - y[-3]
        return "expansion" if slope > 0 else "contraction"
    if last_peak > last_trough:
        # Currently in contraction. Refine with proximity to last peak.
        return "peak" if (y.size - 1 - last_peak) <= 1 else "contraction"
    # Currently in expansion.
    return "trough" if (y.size - 1 - last_trough) <= 1 else "expansion"


def _markov_phase_for_endpoint(series: pd.Series) -> str:
    """Approximate Markov-switching phase at the endpoint via a 2-state fit.

    Returns the cycle label corresponding to the smoothed-state at the last
    observation. State 1 maps to expansion/peak depending on mean sign; state 0
    maps to contraction/trough. Falls back gracefully on convergence failure.
    """
    y = series.dropna()
    if y.size < 16:
        return "rejected"
    try:
        from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
        model = MarkovRegression(y.to_numpy(dtype=float), k_regimes=2, trend="c",
                                 switching_variance=True)
        fit = model.fit(disp=False, search_reps=5)
        smoothed = fit.smoothed_marginal_probabilities
        if hasattr(smoothed, "values"):
            smoothed = smoothed.values
        regime = int(np.argmax(np.asarray(smoothed)[-1]))
        means = fit.params[:2]  # constants per regime (approx)
        high_state = int(np.argmax(np.asarray(means)))
    except Exception:  # noqa: BLE001
        return "rejected"

    if regime == high_state:
        # In the high-mean state: peak or expansion. Use slope.
        slope = y.iloc[-1] - y.iloc[-3] if y.size >= 3 else 0.0
        return "peak" if slope <= 0 else "expansion"
    slope = y.iloc[-1] - y.iloc[-3] if y.size >= 3 else 0.0
    return "trough" if slope >= 0 else "contraction"


def _pelt_phase_for_endpoint(series: pd.Series) -> str:
    """PELT-based regime label for the endpoint.

    Detect breakpoints on the composite; classify the final segment by sign of
    its mean (positive → expansion, negative → contraction). Refine with slope
    if the segment is short enough to be ambiguous.
    """
    y = series.dropna()
    if y.size < 8:
        return "rejected"
    try:
        import ruptures as rpt
        algo = rpt.Pelt(model="l2").fit(y.to_numpy(dtype=float))
        breakpoints = algo.predict(pen=np.log(y.size) * 1.0)
    except Exception:  # noqa: BLE001
        return "rejected"
    if not breakpoints:
        return "rejected"
    start = breakpoints[-2] if len(breakpoints) >= 2 else 0
    segment = y.iloc[start:]
    if segment.empty:
        return "rejected"
    mean_sign = float(segment.mean())
    slope = float(segment.iloc[-1] - segment.iloc[0]) if segment.size >= 2 else 0.0
    if mean_sign > 0:
        return "peak" if slope < 0 else "expansion"
    return "trough" if slope > 0 else "contraction"


def _endpoint_caveat(cycle_band: dict, last_year: int, current_year: int) -> int:
    """Return 1 if the last sample is within hi_years/2 of the data endpoint."""
    return 1 if (current_year - last_year) < cycle_band["hi_years"] / 2 else 0


def run_position_cycles(settings: Settings, as_of: str, manifest_path: Path,
                        groups: list[str], mode: str = "strict",
                        n_surrogates: int = 1000, seed: int = 0) -> Path:
    """Top-level entry. Returns the path to the rendered note."""
    if not settings.db_path.exists():
        init_db(settings.db_path, SCHEMA_PATH, SEED_PATH)
    migrate_db(settings.db_path)

    manifest = load_cycle_manifest(manifest_path)
    typer.echo(f"CPV — manifest {manifest.project} (as-of {manifest.as_of_month}); "
               f"{len(manifest.specs)} variables; {len(groups)} groups.")

    con = connect(settings.db_path)
    run_id = start_ingestion_run(con, mode=mode, notes=f"position-cycles {as_of}")

    panels_by_group: dict[str, pd.DataFrame] = {}
    composite_by_group: dict[str, pd.Series] = {}
    for group in groups:
        if group not in GROUPS:
            typer.echo(f"  Group {group} unknown — skipped.", err=True)
            continue
        try:
            panel = build_group_panel(manifest.specs, group,
                                       settings.world_bank_api_base,
                                       settings.data_raw_dir, con, run_id,
                                       start_year=manifest.start_year)
        except Exception as exc:  # noqa: BLE001
            typer.echo(f"  Group {group}: ingestion failed: {exc}", err=True)
            if mode == "strict":
                finish_ingestion_run(con, run_id, "failed", notes=str(exc))
                con.close()
                raise typer.Exit(code=1)
            continue
        panels_by_group[group] = panel
        composite_by_group[group] = _composite_panel(panel)
        typer.echo(f"  {group}: {panel.shape[0]} years × {panel.shape[1]} vars.")

    positions: list[dict] = []
    consensus_rows: list[dict] = []
    cycles_by_group: dict[str, dict[str, pd.Series]] = {}
    wavelet_power_by_group: dict[str, dict] = {}

    current_year = int(as_of[:4])

    for group, composite in composite_by_group.items():
        cycles_by_group[group] = {}
        if composite.dropna().empty:
            continue
        if group == "WLD":  # only one wavelet figure to keep the report light
            try:
                # Use the broadest band possible for the scaleogram.
                wavelet_power_by_group[group] = morlet_wavelet(
                    composite, lo_years=3, hi_years=60, samples_per_year=1.0)
            except Exception:  # noqa: BLE001
                wavelet_power_by_group[group] = {"power": np.zeros((0, 0)),
                                                  "periods": np.array([])}

        last_year = int(composite.dropna().index.max())

        for cycle_name, band in CYCLE_BANDS.items():
            if cycle_name == "kitchin":
                # Annual data: 3-5y Kitchin is below Nyquist usefulness.
                # We attempt only the upper edge (4-5y) and rely on the null
                # to reject it cleanly if it doesn't survive.
                lo, hi = 4, 5
            else:
                lo, hi = band["lo_years"], band["hi_years"]

            try:
                cycle = cf_bandpass(composite, lo_years=lo, hi_years=hi,
                                    samples_per_year=1.0)
            except Exception:  # noqa: BLE001
                cycle = pd.Series(dtype=float)
            cycles_by_group[group][cycle_name] = cycle

            try:
                null = ar1_bootstrap_null(composite, lo_years=lo, hi_years=hi,
                                          samples_per_year=1.0,
                                          n_surrogates=n_surrogates, seed=seed)
            except Exception:  # noqa: BLE001
                null = None

            # If cycle doesn't survive Gate 1, publish rejected and skip Gate 2.
            if null is None or null.reject_cycle:
                positions.append({
                    "group_code": group, "cycle": cycle_name, "phase": "rejected",
                    "phi_rad": None, "amplitude": None,
                    "ar1_p_value": None if null is None else float(null.p_value),
                    "separable": 0,
                    "endpoint_caveat": _endpoint_caveat(band, last_year, current_year),
                    "notes": "Gate 1: AR(1) null not rejected.",
                })
                continue

            # Method F — CF + Hilbert.
            try:
                phi_series = hilbert_phase(cycle)
                amp_series = hilbert_amplitude(cycle)
                last_phi = float(phi_series.dropna().iloc[-1])
                last_amp = float(amp_series.dropna().iloc[-1])
                phase_f = classify_phase(last_phi)
            except Exception:  # noqa: BLE001
                last_phi, last_amp, phase_f = None, None, "rejected"

            # Method G — Bry-Boschan.
            phase_g = _bryboschan_phase_for_endpoint(cycle)
            # Method E — Markov-switching.
            phase_e = _markov_phase_for_endpoint(cycle)
            # Method D — PELT.
            phase_d = _pelt_phase_for_endpoint(cycle)

            phases_by_model = {"F": phase_f, "G": phase_g, "E": phase_e, "D": phase_d}
            consensus_label, votes = compute_phase_consensus(phases_by_model)

            positions.append({
                "group_code": group, "cycle": cycle_name, "phase": consensus_label,
                "phi_rad": last_phi, "amplitude": last_amp,
                "ar1_p_value": float(null.p_value), "separable": 1,
                "endpoint_caveat": _endpoint_caveat(band, last_year, current_year),
                "notes": f"votes={votes}",
            })
            for model_code, phase in phases_by_model.items():
                consensus_rows.append({
                    "group_code": group, "cycle": cycle_name,
                    "model_code": model_code, "phase": phase,
                    "p_value": float(null.p_value) if model_code == "F" else None,
                    "notes": "",
                })

    # Gate 3 — universality across income groups (WLD + 4 income groups).
    universality_rows: list[dict] = []
    pos_df = pd.DataFrame(positions)
    if not pos_df.empty:
        for cycle_name in CYCLE_BANDS.keys():
            sub = pos_df[pos_df["cycle"] == cycle_name].set_index("group_code")["phase"]
            verdict = compute_cross_group_concordance(sub.to_dict())
            universality_rows.append({"cycle": cycle_name, **verdict, "notes": ""})

    # Persist.
    replace_cycle_positions(con, as_of, positions)
    replace_cycle_consensus(con, as_of, consensus_rows)
    replace_cycle_universality(con, as_of, universality_rows)
    finish_ingestion_run(con, run_id, "success",
                         notes=f"{len(positions)} cells; {len(groups)} groups; CPV")
    con.close()

    # Figures + note.
    settings.figures_dir.mkdir(parents=True, exist_ok=True)
    fig_heatmap = settings.figures_dir / f"cycle_phase_heatmap_{as_of.replace('-', '_')}.png"
    fig_cf = settings.figures_dir / f"cycle_cf_trajectories_{as_of.replace('-', '_')}.png"
    fig_wavelet = settings.figures_dir / f"cycle_wavelet_power_{as_of.replace('-', '_')}.png"

    table = build_position_table(positions)
    try:
        plot_phase_heatmap(table, fig_heatmap)
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  Heatmap figure failed: {exc}", err=True)
    try:
        plot_cf_trajectories(cycles_by_group, fig_cf)
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  CF figure failed: {exc}", err=True)
    try:
        plot_wavelet_power(wavelet_power_by_group, fig_wavelet)
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  Wavelet figure failed: {exc}", err=True)

    figures = {
        "Heatmap des phases": str(Path("../figures") / fig_heatmap.name),
        "CF band-pass par cycle": str(Path("../figures") / fig_cf.name),
        "Spectre wavelet (WLD)": str(Path("../figures") / fig_wavelet.name),
    }
    out_path = settings.reports_dir / f"cycle_position_{as_of.replace('-', '_')}.md"
    schema_version = get_schema_version(settings.db_path) or "unknown"
    render_cycle_position_md(as_of=as_of, table=table,
                             consensus_rows=consensus_rows,
                             universality_rows=universality_rows,
                             figures=figures, schema_version=schema_version,
                             out_path=out_path)
    typer.echo(f"CPV report written: {out_path}")
    return out_path
