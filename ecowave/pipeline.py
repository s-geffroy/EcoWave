from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pandas as pd
import typer

from ecowave.config import Settings
from ecowave.pilots import Pilot, get_pilot
from ecowave.figures.plot_curves import plot_curve_stress
from ecowave.figures.plot_global import plot_global_indices
from ecowave.figures.plot_models import plot_model_windows
from ecowave.db import (
    add_analyst_note,
    connect,
    finish_ingestion_run,
    init_db,
    log_validation,
    replace_curve_scores,
    replace_elliott_waves,
    replace_external_anchor,
    replace_global_indices,
    replace_model_comparisons,
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
from ecowave.scoring.annotations import load_annotations
from ecowave.scoring.curve_scores import aggregate_curve_scores
from ecowave.scoring.elliott_on_composite import detect_elliott_waves, waves_to_frame
from ecowave.scoring.global_indices import compute_global_indices
from ecowave.scoring.model_scores import (
    CRITERIA,
    champion_challenger,
    compute_model_scores,
    db_insertable_rows,
    model_verdicts,
)
from ecowave.scoring.null_test import champion_null_report
from ecowave.waves.model_d_regime import fit_model_d
from ecowave.validation import check_config

SCHEMA_PATH = Path("/app/db/schema.sql")
SEED_PATH = Path("/app/db/seed_variables.sql")
MANIFEST_PATH = Path("/app/sources_manifest.json")


def run_pilot(settings: Settings, pilot: str, mode: str) -> None:
    try:
        pilot_def = get_pilot(pilot)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    if not settings.db_path.exists():
        init_db(settings.db_path, SCHEMA_PATH, SEED_PATH)

    config = check_config(settings=settings, mode=mode)
    typer.echo(config.to_text())
    if not config.ok:
        raise typer.Exit(code=1)

    # The manifest defines the data sources; the pilot defines the analysis window
    # and may override the reference windows (e.g. a clean pre-crisis baseline).
    base = load_manifest(MANIFEST_PATH)
    overrides = {"panel_start": pilot_def.panel_start, "panel_end": pilot_def.panel_end}
    if pilot_def.precrisis is not None:
        overrides["precrisis"] = ReferenceWindow(*pilot_def.precrisis)
    if pilot_def.structural is not None:
        overrides["structural"] = ReferenceWindow(*pilot_def.structural)
    manifest = replace(base, **overrides)
    typer.echo(f"Pilot {pilot}: {pilot_def.title} — window {pilot_def.panel_start}..{pilot_def.panel_end}")
    if pilot_def.holdout:
        typer.echo(f"  HOLDOUT pilot (pre-registered {pilot_def.registered_at}): out-of-sample test.")
    con = connect(settings.db_path)
    run_id = start_ingestion_run(con, mode=mode, notes=f"pilot {pilot}")
    typer.echo(f"Ingestion run #{run_id} started (mode={mode}).")

    all_rows: list[dict] = []
    source_ids: dict[str, int | None] = {}
    failures: list[str] = []

    # Curated institutional events -> SQLite + D3 derivation.
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
                        spec, settings.world_bank_api_base, settings.data_raw_dir, con, run_id
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
            _handle_failure(con, settings, mode, run_id, spec.variable_code, str(exc), failures)
            all_rows.extend(build_missing_rows(spec.variable_code, f"ingestion failed: {exc}", manifest))

    # Variables with no automatable source in V1.
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

    # Curve aggregation + model scoring.
    curves = aggregate_curve_scores(panel)
    replace_curve_scores(con, curves.to_dict("records"))

    # Synthetic global indicators (intensity + diffusion) across 3 weightings.
    anchor_series: pd.Series | None = None
    try:
        anchor_result = fetch_anchor(settings.fred_api_key, settings.data_raw_dir, con, run_id)
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
            typer.echo("  FAVAR anchor unavailable -> intensity_favar falls back to PCA/equal.")
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"  FAVAR anchor fetch failed: {exc}", err=True)

    global_indices = compute_global_indices(curves, anchor=anchor_series)
    replace_global_indices(con, global_indices.to_dict("records"))
    global_indices.to_csv(settings.data_processed_dir / f"global_indices_{pilot}.csv", index=False)
    global_indices.to_parquet(settings.data_processed_dir / f"global_indices_{pilot}.parquet", index=False)

    wave_rows: list[dict] = []
    for weighting in ("equal", "pca", "favar"):
        gsub = global_indices[(global_indices["ref"] == "precrisis")
                              & (global_indices["weighting"] == weighting)]
        if gsub.empty:
            continue
        intensity_ma3 = gsub.set_index("month")["intensity_ma3"]
        intensity_hp = gsub.set_index("month")["intensity_hp_cycle"]
        diffusion = gsub.set_index("month")["diffusion"]
        for smoothing, series in (("ma3", intensity_ma3), ("hp_cycle", intensity_hp)):
            for w in detect_elliott_waves(series, diffusion):
                wave_rows.append({**w.to_dict(), "weighting": weighting, "smoothing": smoothing})
    replace_elliott_waves(con, pilot, wave_rows)
    if wave_rows:
        waves_df = pd.DataFrame(wave_rows)
        waves_df.to_csv(settings.data_processed_dir / f"elliott_waves_composite_{pilot}.csv", index=False)
        typer.echo(f"  Elliott on composite: detected {len(wave_rows)} wave leg(s) "
                   f"({waves_df['confirmed'].sum()} confirmed by diffusion).")
    else:
        waves_df = None
        typer.echo("  Elliott on composite: no impulse passes canonical constraints.")


    annotations = load_annotations(settings.annotations_dir / f"model_scores_qualitative_{pilot}.csv")
    if annotations:
        typer.echo(f"Loaded {len(annotations)} analyst annotation(s) for C2/C4/C5/C6.")

    # Model D: data-driven, non-Elliott benchmark (phases derived from the panel).
    model_d = fit_model_d(panel)
    typer.echo(f"  Model D (PELT) detected {len(model_d['candidate_phases'])} regime(s).")
    models = {**pilot_def.models, "D": model_d}

    scores = compute_model_scores(panel, annotations, models=models)
    replace_model_scores(con, db_insertable_rows(scores))

    # A/B/C carry the full weighted verdict; D is a benchmark on the computed criteria only.
    elliott_scores = scores[scores["model_code"] != "D"]
    verdicts = model_verdicts(elliott_scores)
    for v in verdicts.itertuples():
        add_analyst_note(con, "model", f"{pilot}:{v.model_code}",
                         f"verdict={v.verdict}; weighted={v.weighted_score}; complete={v.complete}; {v.notes}")

    # Persist final verdicts only for models scored on all six criteria.
    comparison_rows = _comparison_rows(elliott_scores, verdicts)
    replace_model_comparisons(con, comparison_rows)
    champion_text = champion_challenger(elliott_scores, verdicts, pilot_def.champion,
                                        margin=settings.dethrone_margin)

    # Null / surrogate test on the champion's phase-separation evidence.
    null_report = _run_null_test(panel, models, pilot_def.champion)
    if null_report is not None:
        flagged = null_report["flag_random"] or null_report["flag_shift"]
        sev = "warning" if flagged else "info"
        msg = (f"champion {pilot_def.champion} mean eta^2={null_report['real']:.3f}; "
               + "; ".join(f"{r.method} p={r.p_value:.3f}" for r in null_report["results"]))
        log_validation(settings.db_path, severity=sev, component="null_test",
                       message=msg, mode_effect="evidence_only")
        add_analyst_note(con, "model", f"{pilot}:{pilot_def.champion}", f"null_test: {msg}")
        typer.echo(f"  Null test: {msg}"
                   + ("  [RED FLAG: not distinguishable from chance]" if flagged else ""))

    _write_scores(settings, scores, verdicts, pilot)

    # Figures
    settings.figures_dir.mkdir(parents=True, exist_ok=True)
    try:
        plot_curve_stress(curves, settings.figures_dir / f"curve_stress_{pilot}.png")
        plot_model_windows(curves, settings.figures_dir / f"model_windows_{pilot}.png", pilot_def.models)
        plot_global_indices(global_indices, settings.figures_dir / f"global_indices_{pilot}.png",
                            pilot=pilot, ref="precrisis", waves=waves_df)
        typer.echo(f"Figures written: curve_stress_{pilot}.png, model_windows_{pilot}.png, "
                   f"global_indices_{pilot}.png")
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"Figure generation skipped: {exc}", err=True)

    status = "partial" if failures else "success"
    finish_ingestion_run(con, run_id, status,
                         notes=("failures: " + ", ".join(failures)) if failures else "all sources ok")
    con.close()

    reports = generate_reports(settings=settings, pilot_def=pilot_def, mode=mode, panel=panel,
                               curves=curves, scores=scores, verdicts=verdicts,
                               failures=failures, champion_text=champion_text,
                               null_report=null_report, model_d=model_d)

    typer.echo(f"Panel + scores written to {settings.data_processed_dir}")
    for path in reports:
        typer.echo(f"Report: {path}")
    if failures:
        typer.echo(f"Run completed PARTIAL — {len(failures)} source(s) failed; verdict provisional/blocked.")
    elif bool(verdicts["complete"].all()):
        summary = ", ".join(f"{v.model_code}={v.verdict}" for v in verdicts.itertuples())
        typer.echo(f"Run complete. All six criteria scored — verdicts: {summary}. {champion_text}")
    else:
        typer.echo("Run complete. Verdict remains provisional/blocked "
                   "(C2/C4/C5/C6 await analyst annotation in annotations/).")


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


def _run_null_test(panel: pd.DataFrame, models: dict, champion: str) -> dict | None:
    """Test whether the champion's phase-separation beats random/time-scrambled nulls."""
    if champion not in models:
        return None
    return champion_null_report(panel, models[champion])


def _comparison_rows(scores: pd.DataFrame, verdicts: pd.DataFrame) -> list[dict]:
    """Build model_comparisons rows for models scored on all six criteria."""
    rows: list[dict] = []
    filled = scores[scores["status"].isin({"computed", "annotated"})]
    for v in verdicts.itertuples():
        if not v.complete:
            continue
        by_crit = {r.criterion_code: int(r.raw_score)
                   for r in filled[filled["model_code"] == v.model_code].itertuples()}
        rows.append({
            "model_code": v.model_code,
            **{code: by_crit[code] for code, _, _ in CRITERIA},
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


def _write_scores(settings: Settings, scores: pd.DataFrame, verdicts: pd.DataFrame, pilot: str) -> None:
    scores.to_csv(settings.data_processed_dir / f"model_scores_abc_{pilot}.csv", index=False)
    scores.to_parquet(settings.data_processed_dir / f"model_scores_abc_{pilot}.parquet", index=False)
    verdicts.to_csv(settings.data_processed_dir / f"model_verdicts_{pilot}.csv", index=False)
