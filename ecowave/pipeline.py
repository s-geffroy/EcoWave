"""Crisis-window CPV pipeline.

For a given crisis pilot (e.g. 2008), this pipeline:
  1. Ingests the curated FRED/ECB/WorldBank panel
  2. Computes per-curve stress scores + the global composite intensity
  3. Runs the four CPV votant methods D/E/F/G on the panel
  4. Scores their auto-computable criteria (C1 / C3) against the surrogate null
  5. Renders the pilot report

The pilot framework retains ``crisis_months`` for EWS AUROC validation. The
same four-method stack used by ``position-cycles`` runs here on a shorter
horizon, so a short pilot window will typically see Model F fall back
(Juglar needs > 2 × 11 years of data) while D, E and G still produce phases.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pandas as pd
import typer

from ecowave.config import Settings
from ecowave.pilots import Pilot, get_pilot
from ecowave.figures.plot_curves import plot_curve_stress
from ecowave.figures.plot_global import plot_global_indices
from ecowave.db import (
    add_analyst_note,
    connect,
    finish_ingestion_run,
    init_db,
    log_validation,
    migrate_db,
    replace_curve_scores,
    replace_external_anchor,
    replace_global_indices,
    replace_model_verdicts,
    replace_model_scores,
    start_ingestion_run,
    upsert_monthly_observation,
)
from ecowave.ingest.anchors import fetch_anchor
from ecowave.ingest.ecb import ingest_ecb_variable
from ecowave.ingest.fred import ingest_fred_components, ingest_fred_variable
from ecowave.ingest.manifest import ReferenceWindow, load_manifest
from ecowave.ingest.manual_events import ingest_events, monthly_intervention_intensity
from ecowave.ingest.worldbank import ingest_worldbank_variable
from ecowave.normalize.panel import (
    PANEL_COLUMNS,
    build_composite_variable_rows,
    build_missing_rows,
    build_variable_rows,
)
from ecowave.reports.render_report import generate_reports
from ecowave.scoring.curve_scores import aggregate_curve_scores
from ecowave.scoring.global_indices import compute_global_indices
from ecowave.scoring.model_scores import (
    compute_model_scores,
    db_insertable_rows,
    model_verdicts,
)
from ecowave.scoring.null_test import all_models_null_report, champion_null_report
from ecowave.waves.model_d_regime import fit_model_d
from ecowave.waves.model_e_markov import fit_model_e
from ecowave.waves.model_f_cycles import fit_model_f
from ecowave.waves.model_g_bryboschan import fit_model_g
from ecowave.validation import check_config

SCHEMA_PATH = Path("/app/db/schema.sql")
SEED_PATH = Path("/app/db/seed_variables.sql")
MANIFEST_PATH = Path("/app/sources_manifest.json")

# The CPV stack runs four methods on every pilot. Model F is the headline
# (CF + Hilbert); we use it as the "champion" reference for the surrogate null
# report so the existing scoring/reporting code paths keep a single anchor.
CPV_MODELS = ("D", "E", "F", "G")
HEADLINE_MODEL = "F"


def run_pilot(settings: Settings, pilot: str, mode: str) -> None:
    """Run a crisis-window CPV pilot end-to-end."""
    try:
        pilot_def = get_pilot(pilot)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    if not settings.db_path.exists():
        init_db(settings.db_path, SCHEMA_PATH, SEED_PATH)
    migrate_db(settings.db_path)

    config = check_config(settings=settings, mode=mode)
    typer.echo(config.to_text())
    if not config.ok:
        raise typer.Exit(code=1)

    base = load_manifest(MANIFEST_PATH)
    overrides = {"panel_start": pilot_def.panel_start, "panel_end": pilot_def.panel_end}
    if pilot_def.precrisis is not None:
        overrides["precrisis"] = ReferenceWindow(*pilot_def.precrisis)
    if pilot_def.structural is not None:
        overrides["structural"] = ReferenceWindow(*pilot_def.structural)
    manifest = replace(base, **overrides)
    typer.echo(f"Pilot {pilot}: {pilot_def.title} — window "
               f"{pilot_def.panel_start}..{pilot_def.panel_end}")
    if pilot_def.holdout:
        typer.echo(f"  HOLDOUT pilot (pre-registered {pilot_def.registered_at}): "
                   "out-of-sample test.")
    con = connect(settings.db_path)
    run_id = start_ingestion_run(con, mode=mode, notes=f"pilot {pilot}")
    typer.echo(f"Ingestion run #{run_id} started (mode={mode}).")

    all_rows: list[dict] = []
    source_ids: dict[str, int | None] = {}
    failures: list[str] = []

    events_path = settings.events_dir / "events_master.csv"
    try:
        n_events = ingest_events(events_path, con)
        typer.echo(f"Ingested {n_events} curated events.")
    except Exception as exc:  # noqa: BLE001
        _handle_failure(con, settings, mode, run_id, "events", str(exc), failures)

    for spec in manifest.specs:
        try:
            if spec.is_composite:
                components, source_id = ingest_fred_components(
                    spec, settings.fred_api_key, settings.data_raw_dir, con, run_id
                )
                source_label = f"{spec.provider}:composite({len(components)})"
                rows = build_composite_variable_rows(spec, components, manifest, source_label)
            else:
                if spec.provider in {"FRED", "FRED_SPREAD"}:
                    series, source_id = ingest_fred_variable(
                        spec, settings.fred_api_key, settings.data_raw_dir, con, run_id
                    )
                elif spec.provider == "ECB":
                    series, source_id = ingest_ecb_variable(
                        spec, settings.ecb_api_base, settings.data_raw_dir, con, run_id
                    )
                elif spec.provider == "WORLD_BANK":
                    series, source_id = ingest_worldbank_variable(
                        spec, settings.world_bank_api_base, settings.data_raw_dir,
                        con, run_id,
                    )
                elif spec.provider == "EVENTS_DERIVED":
                    series = monthly_intervention_intensity(events_path)
                    source_id = None
                else:
                    raise ValueError(f"Unknown provider {spec.provider}")
                source_label = f"{spec.provider}:{spec.series_id or spec.series_key or 'events'}"
                rows = build_variable_rows(spec, series, manifest, source_label)

            source_ids[spec.variable_code] = source_id
            all_rows.extend(rows)
            typer.echo(f"  {spec.variable_code} ({spec.provider}) ingested.")
        except Exception as exc:  # noqa: BLE001
            _handle_failure(con, settings, mode, run_id, spec.variable_code, str(exc),
                            failures)
            all_rows.extend(build_missing_rows(spec.variable_code,
                                                f"ingestion failed: {exc}", manifest))

    for code, reason in manifest.not_automatable.items():
        all_rows.extend(build_missing_rows(code, reason, manifest))

    panel = pd.DataFrame(all_rows, columns=PANEL_COLUMNS)
    _write_panel(settings, panel, pilot_def)

    for r in panel.itertuples():
        upsert_monthly_observation(
            con, r.month, r.variable_code, r.raw_value, r.z_precrisis, r.stress_precrisis,
            r.z_structural, r.stress_structural, r.status,
            source_ids.get(r.variable_code), r.notes,
        )
    con.commit()

    # Curve aggregation + composite intensity.
    curves = aggregate_curve_scores(panel)
    replace_curve_scores(con, curves.to_dict("records"))

    anchor_series: pd.Series | None = None
    try:
        anchor_result = fetch_anchor(settings.fred_api_key, settings.data_raw_dir,
                                      con, run_id)
        if anchor_result is not None:
            anchor_series = anchor_result.series
            anchor_series.index = anchor_series.index.astype(str)
            replace_external_anchor(
                con, {m: float(v) for m, v in anchor_series.dropna().items()},
                anchor_result.label, anchor_result.source_id,
            )
            typer.echo(f"  FAVAR anchor ({anchor_result.label}) loaded: "
                       f"{anchor_series.dropna().shape[0]} months.")
        else:
            typer.echo("  FAVAR anchor unavailable -> intensity_favar falls back to "
                       "PCA/equal.")
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  FAVAR anchor fetch failed: {exc}", err=True)

    global_indices = compute_global_indices(curves, anchor=anchor_series)
    replace_global_indices(con, global_indices.to_dict("records"))
    global_indices.to_csv(settings.data_processed_dir / f"global_indices_{pilot}.csv",
                          index=False)
    global_indices.to_parquet(
        settings.data_processed_dir / f"global_indices_{pilot}.parquet", index=False)

    # CPV stack: D (PELT), E (Markov-switching), F (CF + Hilbert), G (Bry-Boschan).
    model_d = fit_model_d(panel)
    typer.echo(f"  Model D (PELT) -> {len(model_d['candidate_phases'])} regime(s).")
    model_e = fit_model_e(panel)
    if model_e.get("fit_status") == "ok":
        typer.echo(f"  Model E (Markov-switching, k={model_e['selected_k']}) -> "
                   f"{len(model_e['candidate_phases'])} regime(s); "
                   f"AIC={model_e.get('aic')}, BIC={model_e.get('bic')}.")
    else:
        typer.echo(f"  Model E (Markov-switching) fallback: {model_e.get('fit_status')}.")
    model_f = fit_model_f(panel)
    typer.echo(f"  Model F (CF Juglar + Hilbert) -> "
               f"{len(model_f['candidate_phases'])} phase(s); "
               f"AR(1) p={model_f.get('ar1_pvalue')}; "
               f"status={model_f.get('fit_status')}.")
    model_g = fit_model_g(panel)
    typer.echo(f"  Model G (Bry-Boschan) -> {len(model_g['candidate_phases'])} phase(s) "
               f"({model_g.get('n_peaks')}P/{model_g.get('n_troughs')}T); "
               f"status={model_g.get('fit_status')}.")

    models = {"D": model_d, "E": model_e, "F": model_f, "G": model_g}

    scores = compute_model_scores(panel, annotations=None, models=models)
    replace_model_scores(con, db_insertable_rows(scores))
    verdicts = model_verdicts(scores)
    replace_model_verdicts(con, _verdict_rows(scores, verdicts))

    # Surrogate-null report on the headline (Model F) plus a per-model panel.
    null_report = champion_null_report(panel, models[HEADLINE_MODEL]) \
        if HEADLINE_MODEL in models else None
    if null_report is not None:
        flagged = null_report["flag_random"] or null_report["flag_shift"]
        sev = "warning" if flagged else "info"
        msg = (f"headline {HEADLINE_MODEL} mean eta^2={null_report['real']:.3f}; "
               + "; ".join(f"{r.method} p={r.p_value:.3f}"
                            for r in null_report["results"]))
        log_validation(settings.db_path, severity=sev, component="null_test",
                       message=msg, mode_effect="evidence_only")
        add_analyst_note(con, "model", f"{pilot}:{HEADLINE_MODEL}", f"null_test: {msg}")
        typer.echo(f"  Null test: {msg}"
                   + ("  [RED FLAG: not distinguishable from chance]" if flagged else ""))

    null_reports_by_model = all_models_null_report(panel, models)
    _write_scores(settings, scores, verdicts, pilot)

    settings.figures_dir.mkdir(parents=True, exist_ok=True)
    try:
        plot_curve_stress(curves, settings.figures_dir / f"curve_stress_{pilot}.png")
        plot_global_indices(global_indices,
                            settings.figures_dir / f"global_indices_{pilot}.png",
                            pilot=pilot, ref="precrisis")
        typer.echo(f"Figures written: curve_stress_{pilot}.png, "
                   f"global_indices_{pilot}.png")
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"Figure generation skipped: {exc}", err=True)

    status = "partial" if failures else "success"
    finish_ingestion_run(con, run_id, status,
                         notes=("failures: " + ", ".join(failures))
                         if failures else "all sources ok")
    con.close()

    reports = generate_reports(settings=settings, pilot_def=pilot_def, mode=mode,
                               panel=panel, curves=curves, scores=scores,
                               verdicts=verdicts, failures=failures,
                               null_report=null_report, model_d=model_d,
                               model_e=model_e, model_f=model_f, model_g=model_g,
                               null_reports_by_model=null_reports_by_model)

    typer.echo(f"Panel + scores written to {settings.data_processed_dir}")
    for path in reports:
        typer.echo(f"Report: {path}")
    if failures:
        typer.echo(f"Run completed PARTIAL — {len(failures)} source(s) failed.")
    else:
        typer.echo(f"Run complete. CPV stack on pilot {pilot}: "
                   f"D={len(model_d['candidate_phases'])}, "
                   f"E={len(model_e['candidate_phases'])}, "
                   f"F={model_f.get('fit_status')}, "
                   f"G={len(model_g['candidate_phases'])}.")


def _handle_failure(con, settings: Settings, mode: str, run_id: int, component: str,
                    message: str, failures: list[str]) -> None:
    failures.append(component)
    log_validation(settings.db_path, severity="error" if mode == "strict" else "warning",
                   component=f"ingest:{component}", message=message,
                   mode_effect="strict_fails_exploratory_warns")
    if mode == "strict":
        finish_ingestion_run(con, run_id, "failed", notes=f"{component}: {message}")
        con.close()
        typer.echo(f"STRICT mode: ingestion of '{component}' failed: {message}", err=True)
        raise typer.Exit(code=1)


def _verdict_rows(scores: pd.DataFrame, verdicts: pd.DataFrame) -> list[dict]:
    """Build model_verdicts rows (one per CPV model)."""
    rows: list[dict] = []
    filled = scores[scores["status"].isin({"computed", "annotated"})]
    for v in verdicts.itertuples():
        if not v.complete:
            continue
        by_crit = {r.criterion_code: int(r.raw_score)
                   for r in filled[filled["model_code"] == v.model_code].itertuples()}
        rows.append({
            "model_code": v.model_code,
            "C1": by_crit.get("C1", 0),
            "C3": by_crit.get("C3", 0),
            "weighted_score": float(v.weighted_score),
            "verdict": v.verdict,
            "notes": v.notes,
        })
    return rows


def _write_panel(settings: Settings, panel: pd.DataFrame, pilot_def: Pilot) -> None:
    settings.data_processed_dir.mkdir(parents=True, exist_ok=True)
    stem = f"monthly_panel_{pilot_def.panel_start[:4]}_{pilot_def.panel_end[:4]}"
    panel.to_csv(settings.data_processed_dir / f"{stem}.csv", index=False)
    panel.to_parquet(settings.data_processed_dir / f"{stem}.parquet", index=False)


def _write_scores(settings: Settings, scores: pd.DataFrame, verdicts: pd.DataFrame,
                  pilot: str) -> None:
    scores.to_csv(settings.data_processed_dir / f"model_scores_{pilot}.csv", index=False)
    scores.to_parquet(settings.data_processed_dir / f"model_scores_{pilot}.parquet",
                       index=False)
    verdicts.to_csv(settings.data_processed_dir / f"model_verdicts_{pilot}.csv",
                     index=False)
