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
from ecowave.cycles.long_history import (
    LONG_GROUPS,
    LongHistoryDataset,
    build_long_history_panel,
)
from ecowave.cycles.quarterly import (
    QUARTERLY_GROUPS,
    QuarterlyDataset,
    build_quarterly_panel,
    load_quarterly_manifest,
)
from ecowave.cycles.manifest import CycleManifest, load_cycle_manifest
from ecowave.cycles.phase import (
    classify_phase,
    forecast_next_extremum,
    hilbert_amplitude,
    hilbert_phase,
    trend_from_phase,
)
from ecowave.cycles.report import (
    build_position_table,
    plot_amplitude_heatmap,
    plot_cf_trajectories,
    plot_next_extremum_timeline,
    plot_phase_heatmap,
    plot_phase_polar_diagram,
    plot_pvalue_heatmap,
    plot_wavelet_power,
    render_cycle_position_md,
)
from ecowave.cycles.surrogate import (
    ar1_bootstrap_null,
    dual_null,
    phase_scramble_null,
    wavelet_bandpower_null,
)
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


def _composite_panel(panel: pd.DataFrame,
                     band: tuple[float, float] | None = None,
                     samples_per_year: float = 1.0) -> pd.Series:
    """Equal-weighted standardized composite across all indicators in the panel.

    When ``band`` is None, each column is z-scored against its own history then
    averaged (the default cross-band aggregate).

    When ``band = (lo_years, hi_years)`` is provided, each column is FIRST
    band-passed (CF) into the band of interest, then z-scored and averaged.
    This concentrates cyclical power in the target band and substantially
    improves the SNR for Gate 1 — at the cost of the result being band-specific
    (the composite must be recomputed per cycle band).

    ``samples_per_year`` is 1 for the annual horizons (wb / long) and 4 for
    the quarterly horizon; it scales the minimum-length guard and is passed
    through to the CF filter so the cutoffs are computed against the right
    sample frequency.
    """
    if panel.empty:
        return pd.Series(dtype=float)
    if band is None:
        standardized = (panel - panel.mean(axis=0)) / panel.std(axis=0).replace(0, np.nan)
        return standardized.mean(axis=1, skipna=True)

    lo, hi = band
    min_samples = int(2 * hi * samples_per_year)
    filtered_cols: dict[str, pd.Series] = {}
    for col in panel.columns:
        series = panel[col].dropna()
        if series.size < min_samples:
            continue
        try:
            cycle = cf_bandpass(series, lo_years=lo, hi_years=hi,
                                samples_per_year=samples_per_year)
        except Exception:  # noqa: BLE001
            continue
        filtered_cols[col] = cycle.reindex(panel.index)
    if not filtered_cols:
        return pd.Series(dtype=float, index=panel.index)
    df = pd.DataFrame(filtered_cols)
    z = (df - df.mean(axis=0)) / df.std(axis=0).replace(0, np.nan)
    return z.mean(axis=1, skipna=True)


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
                        n_surrogates: int = 1000, seed: int = 0,
                        horizon: str = "wb", null: str = "ar1") -> Path:
    """Top-level entry. Returns the path to the rendered note.

    ``horizon`` selects the data source:
    - ``"wb"``  — World Bank 1960-present panel (default). Manifest from
      ``manifest_path`` (typically ``cycles_manifest.json``).
    - ``"long"`` — Maddison Project + Jordà-Schularick-Taylor 1870-2020
      on the 18 advanced economies. Manifest from
      ``long_history_manifest.json``. See ``ecowave/cycles/long_history.py``.
    """
    if not settings.db_path.exists():
        init_db(settings.db_path, SCHEMA_PATH, SEED_PATH)
    migrate_db(settings.db_path)

    con = connect(settings.db_path)
    run_id = start_ingestion_run(con, mode=mode,
                                  notes=f"position-cycles {as_of} horizon={horizon}")

    panels_by_group: dict[str, pd.DataFrame] = {}
    composite_by_group: dict[str, pd.Series] = {}

    if horizon == "long":
        return _run_long_history(settings, as_of, manifest_path, groups, mode,
                                  n_surrogates, seed, con, run_id, null)

    if horizon == "quarterly":
        return _run_quarterly(settings, as_of, manifest_path, groups, mode,
                              n_surrogates, seed, con, run_id, null)

    manifest = load_cycle_manifest(manifest_path)
    typer.echo(f"CPV — manifest {manifest.project} (as-of {manifest.as_of_month}); "
               f"{len(manifest.specs)} variables; {len(groups)} groups.")

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

    return _analyse_and_render(
        settings=settings, as_of=as_of, con=con, run_id=run_id, mode=mode,
        groups=list(composite_by_group.keys()),
        composite_by_group=composite_by_group,
        panels_by_group=panels_by_group,
        n_surrogates=n_surrogates, seed=seed, null=null,
        horizon_label="World Bank (1960-present)",
        wavelet_group="WLD",
        samples_per_year=1.0,
        report_suffix="wb",
    )


def _run_gate1(series: pd.Series, lo: float, hi: float, null: str,
                n_surrogates: int, seed: int,
                samples_per_year: float = 1.0):
    """Dispatch to the Gate 1 null requested by ``null``.

    Returns either a NullResult (for ar1 / phase / wavelet) or a dict (for
    dual). The caller treats both uniformly via the ``reject_cycle`` and
    ``p_value`` attributes/keys. ``samples_per_year`` is threaded through to
    the surrogate generators so the band cutoffs are correct on quarterly
    grids.
    """
    if null == "phase":
        return phase_scramble_null(series, lo_years=lo, hi_years=hi,
                                    samples_per_year=samples_per_year,
                                    n_surrogates=n_surrogates, seed=seed)
    if null == "wavelet":
        return wavelet_bandpower_null(series, lo_years=lo, hi_years=hi,
                                       samples_per_year=samples_per_year,
                                       n_surrogates=min(n_surrogates, 500),
                                       seed=seed)
    if null == "dual":
        return dual_null(series, lo_years=lo, hi_years=hi,
                          samples_per_year=samples_per_year,
                          n_surrogates=n_surrogates, seed=seed)
    return ar1_bootstrap_null(series, lo_years=lo, hi_years=hi,
                               samples_per_year=samples_per_year,
                               n_surrogates=n_surrogates, seed=seed)


def _analyse_and_render(*, settings: Settings, as_of: str,
                        con: "sqlite3.Connection", run_id: int, mode: str,
                        groups: list[str],
                        composite_by_group: dict[str, pd.Series],
                        panels_by_group: dict[str, pd.DataFrame],
                        n_surrogates: int, seed: int, null: str,
                        horizon_label: str, wavelet_group: str,
                        samples_per_year: float = 1.0,
                        report_suffix: str = "wb") -> Path:
    """Common back-end: surrogate test, phase classification, Gate 2/3,
    persistence, figures, and Markdown rendering. Shared by both horizons."""
    positions: list[dict] = []
    consensus_rows: list[dict] = []
    cycles_by_group: dict[str, dict[str, pd.Series]] = {}
    wavelet_power_by_group: dict[str, dict] = {}

    current_year = int(as_of[:4])

    for group, composite in composite_by_group.items():
        cycles_by_group[group] = {}
        if composite.dropna().empty:
            continue
        if group == wavelet_group:  # one wavelet figure per run for readability
            try:
                # Use the broadest band possible for the scaleogram.
                wavelet_power_by_group[group] = morlet_wavelet(
                    composite, lo_years=3, hi_years=60,
                    samples_per_year=samples_per_year)
            except Exception:  # noqa: BLE001
                wavelet_power_by_group[group] = {"power": np.zeros((0, 0)),
                                                  "periods": np.array([])}

        last_index = composite.dropna().index.max()
        last_year = (last_index.year if hasattr(last_index, "year")
                     else int(last_index))

        panel = panels_by_group.get(group)

        for cycle_name, band in CYCLE_BANDS.items():
            if cycle_name == "kitchin" and samples_per_year <= 1.0:
                # Annual data: 3-5y Kitchin is below Nyquist usefulness.
                # We attempt only the upper edge (4-5y) and rely on the null
                # to reject it cleanly if it doesn't survive. The quarterly
                # horizon (samples_per_year=4) gets the full 3-5y band —
                # Roadmap #9.
                lo, hi = 4, 5
            else:
                lo, hi = band["lo_years"], band["hi_years"]

            # Per-band composite: band-pass each indicator first, then average.
            # Falls back to the cross-band composite if the panel is missing
            # (e.g. when called from a test path that only provides composites).
            if panel is not None and not panel.empty:
                band_composite = _composite_panel(
                    panel, band=(lo, hi), samples_per_year=samples_per_year)
                if band_composite.dropna().empty:
                    band_composite = composite
            else:
                band_composite = composite

            try:
                cycle = cf_bandpass(band_composite, lo_years=lo, hi_years=hi,
                                    samples_per_year=samples_per_year)
            except Exception:  # noqa: BLE001
                cycle = pd.Series(dtype=float)
            cycles_by_group[group][cycle_name] = cycle

            try:
                null_res = _run_gate1(band_composite, lo, hi, null,
                                       n_surrogates=n_surrogates, seed=seed,
                                       samples_per_year=samples_per_year)
            except Exception:  # noqa: BLE001
                null_res = None

            def _null_props(r):
                if r is None:
                    return True, None
                if isinstance(r, dict):  # dual_null returns a dict
                    return bool(r["reject_cycle"]), float(r["p_value"])
                return bool(r.reject_cycle), float(r.p_value)

            reject, p_value = _null_props(null_res)

            # If cycle doesn't survive Gate 1, publish rejected and skip Gate 2.
            if reject:
                positions.append({
                    "group_code": group, "cycle": cycle_name, "phase": "rejected",
                    "phi_rad": None, "amplitude": None,
                    "ar1_p_value": p_value,
                    "separable": 0,
                    "endpoint_caveat": _endpoint_caveat(band, last_year, current_year),
                    "trend": "—", "next_kind": "—", "next_eta_years": None,
                    "notes": f"Gate 1 ({null}) rejected.",
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
            consensus_label, votes = compute_phase_consensus(
                phases_by_model,
                allowed_methods=band.get("methods"),
                min_agreement=band.get("min_agreement", 3),
            )

            # Trend + next-extremum forecast from the Hilbert phase (Model F).
            period_years = (lo + hi) / 2.0
            forecast = forecast_next_extremum(last_phi, period_years)
            trend = trend_from_phase(last_phi)

            positions.append({
                "group_code": group, "cycle": cycle_name, "phase": consensus_label,
                "phi_rad": last_phi, "amplitude": last_amp,
                "ar1_p_value": p_value, "separable": 1,
                "endpoint_caveat": _endpoint_caveat(band, last_year, current_year),
                "trend": trend, "next_kind": forecast["next_kind"],
                "next_eta_years": forecast["next_eta_years"],
                "notes": f"votes={votes}; null={null}",
            })
            for model_code, phase in phases_by_model.items():
                consensus_rows.append({
                    "group_code": group, "cycle": cycle_name,
                    "model_code": model_code, "phase": phase,
                    "p_value": p_value if model_code == "F" else None,
                    "notes": "",
                })

    # Gate 3 — universality across the available groups.
    universality_rows: list[dict] = []
    pos_df = pd.DataFrame(positions)
    if not pos_df.empty:
        for cycle_name in CYCLE_BANDS.keys():
            sub = pos_df[pos_df["cycle"] == cycle_name].set_index("group_code")["phase"]
            # For the long horizon there are no income classes; use all groups.
            income_only = any(k in sub.index for k in INCOME_GROUPS)
            verdict = compute_cross_group_concordance(sub.to_dict(),
                                                      income_only=income_only)
            universality_rows.append({"cycle": cycle_name, **verdict, "notes": ""})

    # Persist.
    replace_cycle_positions(con, as_of, positions)
    replace_cycle_consensus(con, as_of, consensus_rows)
    replace_cycle_universality(con, as_of, universality_rows)
    finish_ingestion_run(con, run_id, "success",
                         notes=f"{len(positions)} cells; {len(groups)} groups; "
                                f"{horizon_label}")
    con.close()

    # Figures + note.
    settings.figures_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{as_of.replace('-', '_')}_{report_suffix}"
    fig_heatmap = settings.figures_dir / f"cycle_phase_heatmap_{stem}.png"
    fig_cf = settings.figures_dir / f"cycle_cf_trajectories_{stem}.png"
    fig_wavelet = settings.figures_dir / f"cycle_wavelet_power_{stem}.png"
    fig_amplitude = settings.figures_dir / f"cycle_amplitude_heatmap_{stem}.png"
    fig_pvalue = settings.figures_dir / f"cycle_pvalue_heatmap_{stem}.png"
    fig_timeline = settings.figures_dir / f"cycle_next_extremum_timeline_{stem}.png"

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
    try:
        plot_amplitude_heatmap(table, fig_amplitude)
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  Amplitude heatmap failed: {exc}", err=True)
    try:
        plot_pvalue_heatmap(table, fig_pvalue)
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  p-value heatmap failed: {exc}", err=True)
    try:
        plot_next_extremum_timeline(table, as_of, fig_timeline)
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  Timeline figure failed: {exc}", err=True)

    fig_polar_per_cycle: dict[str, Path] = {}
    for cycle_name in CYCLE_BANDS.keys():
        fig_polar = settings.figures_dir / (
            f"cycle_phase_polar_{cycle_name}_{stem}.png")
        try:
            plot_phase_polar_diagram(table, cycle_name, fig_polar)
            fig_polar_per_cycle[cycle_name] = fig_polar
        except Exception as exc:  # noqa: BLE001
            typer.echo(f"  Polar figure ({cycle_name}) failed: {exc}", err=True)

    figures = {
        "Heatmap des phases (consensus)":
            str(Path("../figures") / fig_heatmap.name),
        "Heatmap des amplitudes":
            str(Path("../figures") / fig_amplitude.name),
        "Heatmap des p-values (Gate 1)":
            str(Path("../figures") / fig_pvalue.name),
        "Frise des prochains extrema":
            str(Path("../figures") / fig_timeline.name),
        "CF band-pass par cycle":
            str(Path("../figures") / fig_cf.name),
        f"Spectre wavelet ({wavelet_group})":
            str(Path("../figures") / fig_wavelet.name),
    }
    for cycle_name, fig_polar in fig_polar_per_cycle.items():
        figures[f"Diagramme polaire — {cycle_name.capitalize()}"] = str(
            Path("../figures") / fig_polar.name)
    out_path = settings.reports_dir / f"cycle_position_{stem}.md"
    schema_version = get_schema_version(settings.db_path) or "unknown"
    render_cycle_position_md(as_of=as_of, table=table,
                             consensus_rows=consensus_rows,
                             universality_rows=universality_rows,
                             figures=figures, schema_version=schema_version,
                             out_path=out_path)
    typer.echo(f"CPV report written ({horizon_label}): {out_path}")
    return out_path


def _run_long_history(settings: Settings, as_of: str, manifest_path: Path,
                      groups: list[str], mode: str,
                      n_surrogates: int, seed: int,
                      con: "sqlite3.Connection", run_id: int,
                      null: str = "ar1") -> Path:
    """Long-horizon (Maddison + JST) variant of ``run_position_cycles``."""
    import json as _json

    dataset = LongHistoryDataset.default(settings.data_raw_dir)
    try:
        dataset.assert_exists()
    except FileNotFoundError as exc:
        typer.echo(str(exc), err=True)
        finish_ingestion_run(con, run_id, "failed", notes="missing long-history files")
        con.close()
        raise typer.Exit(code=1)

    spec = _json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    variable_codes = [v["variable_code"] for v in spec.get("variable_codes", [])]
    start_year = int(spec.get("start_year", 1870))
    typer.echo(f"CPV (long horizon) — {spec.get('project','cpv_long_history')}; "
               f"{len(variable_codes)} variables; {len(groups)} groups; "
               f"start_year={start_year}.")

    composite_by_group: dict[str, pd.Series] = {}
    panels_by_group: dict[str, pd.DataFrame] = {}
    for group in groups:
        if group not in LONG_GROUPS:
            typer.echo(f"  Long-history group {group} unknown — skipped.", err=True)
            continue
        try:
            panel = build_long_history_panel(group, variable_codes, dataset,
                                              start_year=start_year,
                                              persist={"con": con})
        except Exception as exc:  # noqa: BLE001
            typer.echo(f"  Group {group}: long ingestion failed: {exc}", err=True)
            if mode == "strict":
                finish_ingestion_run(con, run_id, "failed", notes=str(exc))
                con.close()
                raise typer.Exit(code=1)
            continue
        if panel.empty:
            typer.echo(f"  Group {group}: empty panel — skipped.")
            continue
        panels_by_group[group] = panel
        composite_by_group[group] = _composite_panel(panel)
        typer.echo(f"  {group}: {panel.shape[0]} years × {panel.shape[1]} vars.")

    if not composite_by_group:
        typer.echo("No long-history group produced data; aborting.", err=True)
        finish_ingestion_run(con, run_id, "failed", notes="empty panels")
        con.close()
        raise typer.Exit(code=1)

    return _analyse_and_render(
        settings=settings, as_of=as_of, con=con, run_id=run_id, mode=mode,
        groups=list(composite_by_group.keys()),
        composite_by_group=composite_by_group,
        panels_by_group=panels_by_group,
        n_surrogates=n_surrogates, seed=seed, null=null,
        horizon_label="Maddison + Jordà-Schularick-Taylor (1870-2020)",
        wavelet_group="ADV18",
        samples_per_year=1.0,
        report_suffix="long",
    )


def _run_quarterly(settings: Settings, as_of: str, manifest_path: Path,
                   groups: list[str], mode: str,
                   n_surrogates: int, seed: int,
                   con: "sqlite3.Connection", run_id: int,
                   null: str = "ar1") -> Path:
    """Quarterly (FRED + Eurostat + OECD QNA) variant of ``run_position_cycles``.

    This is the Kitchin-targeted extension (Roadmap #9): all four bands are
    re-evaluated at ``samples_per_year=4`` so the full 3-5 y Kitchin band is
    above the Nyquist threshold.
    """
    spec = load_quarterly_manifest(Path(manifest_path))
    samples_per_year = float(spec.get("samples_per_year", 4))
    variable_specs = spec.get("variable_codes", [])
    start_year = int(spec.get("start_year", 1960))
    typer.echo(
        f"CPV (quarterly horizon) — {spec.get('project','cpv_quarterly')}; "
        f"{len(variable_specs)} variables; {len(groups)} groups; "
        f"start_year={start_year}; samples_per_year={int(samples_per_year)}."
    )

    dataset = QuarterlyDataset.default(settings.data_raw_dir)

    composite_by_group: dict[str, pd.Series] = {}
    panels_by_group: dict[str, pd.DataFrame] = {}
    for group in groups:
        if group not in QUARTERLY_GROUPS:
            typer.echo(f"  Quarterly group {group} unknown — skipped.", err=True)
            continue
        try:
            panel = build_quarterly_panel(
                group, variable_specs, dataset,
                fred_api_key=settings.fred_api_key,
                start_year=start_year, run_id=run_id,
                persist={"con": con},
            )
        except Exception as exc:  # noqa: BLE001
            typer.echo(f"  Group {group}: quarterly ingestion failed: {exc}",
                       err=True)
            if mode == "strict":
                finish_ingestion_run(con, run_id, "failed", notes=str(exc))
                con.close()
                raise typer.Exit(code=1)
            continue
        if panel.empty:
            typer.echo(f"  Group {group}: empty panel — skipped.")
            continue
        panels_by_group[group] = panel
        composite_by_group[group] = _composite_panel(panel)
        typer.echo(f"  {group}: {panel.shape[0]} quarters × {panel.shape[1]} vars.")

    if not composite_by_group:
        typer.echo("No quarterly group produced data; aborting.", err=True)
        finish_ingestion_run(con, run_id, "failed", notes="empty panels")
        con.close()
        raise typer.Exit(code=1)

    return _analyse_and_render(
        settings=settings, as_of=as_of, con=con, run_id=run_id, mode=mode,
        groups=list(composite_by_group.keys()),
        composite_by_group=composite_by_group,
        panels_by_group=panels_by_group,
        n_surrogates=n_surrogates, seed=seed, null=null,
        horizon_label="Quarterly FRED+Eurostat+OECD (1960-present, EA from 1995)",
        wavelet_group="USA",
        samples_per_year=samples_per_year,
        report_suffix="q",
    )
