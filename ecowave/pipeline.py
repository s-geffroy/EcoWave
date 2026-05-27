from __future__ import annotations

from pathlib import Path

import pandas as pd
import typer

from ecowave.config import Settings
from ecowave.figures.plot_curves import plot_curve_stress
from ecowave.figures.plot_models import plot_model_windows
from ecowave.db import (
    add_analyst_note,
    connect,
    finish_ingestion_run,
    init_db,
    log_validation,
    replace_curve_scores,
    replace_model_comparisons,
    replace_model_scores,
    start_ingestion_run,
    upsert_monthly_observation,
)
from ecowave.ingest.ecb import ingest_ecb_variable
from ecowave.ingest.fred import ingest_fred_components, ingest_fred_variable
from ecowave.ingest.manifest import load_manifest
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
from ecowave.scoring.model_scores import (
    CRITERIA,
    champion_challenger,
    compute_model_scores,
    db_insertable_rows,
    model_verdicts,
)
from ecowave.validation import check_config

SCHEMA_PATH = Path("/app/db/schema.sql")
SEED_PATH = Path("/app/db/seed_variables.sql")
MANIFEST_PATH = Path("/app/sources_manifest.json")


def run_pilot(settings: Settings, pilot: str, mode: str) -> None:
    if pilot != "2008":
        raise typer.BadParameter("Only pilot 2008 is implemented.")

    if not settings.db_path.exists():
        init_db(settings.db_path, SCHEMA_PATH, SEED_PATH)

    config = check_config(settings=settings, mode=mode)
    typer.echo(config.to_text())
    if not config.ok:
        raise typer.Exit(code=1)

    manifest = load_manifest(MANIFEST_PATH)
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
    _write_panel(settings, panel)

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

    annotations = load_annotations(settings.annotations_dir / "model_scores_qualitative.csv")
    if annotations:
        typer.echo(f"Loaded {len(annotations)} analyst annotation(s) for C2/C4/C5/C6.")
    scores = compute_model_scores(panel, annotations)
    replace_model_scores(con, db_insertable_rows(scores))
    verdicts = model_verdicts(scores)
    for v in verdicts.itertuples():
        add_analyst_note(con, "model", v.model_code,
                         f"verdict={v.verdict}; weighted={v.weighted_score}; complete={v.complete}; {v.notes}")

    # Persist final verdicts only for models scored on all six criteria.
    comparison_rows = _comparison_rows(scores, verdicts)
    replace_model_comparisons(con, comparison_rows)
    champion_text = champion_challenger(scores, verdicts)

    _write_scores(settings, scores, verdicts)

    # Figures
    settings.figures_dir.mkdir(parents=True, exist_ok=True)
    try:
        plot_curve_stress(curves, settings.figures_dir / "curve_stress.png")
        plot_model_windows(curves, settings.figures_dir / "model_windows.png")
        typer.echo("Figures written: curve_stress.png, model_windows.png")
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"Figure generation skipped: {exc}", err=True)

    status = "partial" if failures else "success"
    finish_ingestion_run(con, run_id, status,
                         notes=("failures: " + ", ".join(failures)) if failures else "all sources ok")
    con.close()

    reports = generate_reports(settings=settings, pilot=pilot, mode=mode, panel=panel,
                               curves=curves, scores=scores, verdicts=verdicts,
                               failures=failures, champion_text=champion_text)

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


def _write_panel(settings: Settings, panel: pd.DataFrame) -> None:
    settings.data_processed_dir.mkdir(parents=True, exist_ok=True)
    panel.to_csv(settings.data_processed_dir / "monthly_panel_2007_2012.csv", index=False)
    panel.to_parquet(settings.data_processed_dir / "monthly_panel_2007_2012.parquet", index=False)


def _write_scores(settings: Settings, scores: pd.DataFrame, verdicts: pd.DataFrame) -> None:
    scores.to_csv(settings.data_processed_dir / "model_scores_abc.csv", index=False)
    scores.to_parquet(settings.data_processed_dir / "model_scores_abc.parquet", index=False)
    verdicts.to_csv(settings.data_processed_dir / "model_verdicts.csv", index=False)
