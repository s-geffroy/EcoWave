from pathlib import Path
import typer

from ecowave.config import Settings
from ecowave.db import init_db as init_db_impl
from ecowave.validation import check_config as check_config_impl
from ecowave.pipeline import run_pilot as run_pilot_impl
from ecowave.reports.render_report import generate_report as generate_report_impl

app = typer.Typer(help="EcoWave CLI — crisis wave pilot pipeline.")


@app.command("init-db")
def init_db() -> None:
    """Initialize the local SQLite database."""
    settings = Settings.from_env()
    init_db_impl(
        settings.db_path,
        Path("/app/db/schema.sql"),
        Path("/app/db/seed_variables.sql"),
    )
    typer.echo(f"SQLite initialized at {settings.db_path}")


@app.command("check-config")
def check_config(
    mode: str = typer.Option("strict", "--mode", help="strict or exploratory")
) -> None:
    """Validate source/API configuration and local storage."""
    settings = Settings.from_env()
    result = check_config_impl(settings=settings, mode=mode)
    typer.echo(result.to_text())
    if not result.ok:
        raise typer.Exit(code=1)


@app.command("validate")
def validate(
    pilot: str = typer.Option("2008", "--pilot"),
    mode: str = typer.Option("strict", "--mode"),
) -> None:
    """Alias for check-config plus basic pilot validation."""
    settings = Settings.from_env()
    result = check_config_impl(settings=settings, mode=mode)
    typer.echo(result.to_text())
    if not result.ok:
        raise typer.Exit(code=1)
    typer.echo(f"Pilot {pilot} validation passed at configuration level.")


@app.command("run-pilot")
def run_pilot(
    pilot: str = typer.Argument("2008"),
    mode: str = typer.Option("strict", "--mode"),
) -> None:
    """Run the crisis-window CPV pipeline.

    Stack: D (PELT change-point), E (Markov-switching), F (CF Juglar + Hilbert),
    G (Bry-Boschan). Surrogate AR(1) null applied per method. Same four-method
    stack as ``position-cycles`` but on a single crisis window.
    """
    settings = Settings.from_env()
    run_pilot_impl(settings=settings, pilot=pilot, mode=mode)


@app.command("position-cycles")
def position_cycles(
    as_of: str = typer.Option("2026-05", "--as-of",
                              help="Target month (YYYY-MM) for the CPV snapshot."),
    manifest: str = typer.Option("", "--manifest",
                                  help="Manifest path. Defaults depend on --horizon."),
    groups: str = typer.Option("", "--groups",
                                help="Comma-separated group codes. Defaults depend on --horizon."),
    mode: str = typer.Option("strict", "--mode"),
    n_surrogates: int = typer.Option(1000, "--n-surrogates"),
    seed: int = typer.Option(0, "--seed"),
    horizon: str = typer.Option(
        "wb", "--horizon",
        help="Data horizon: 'wb' (World Bank, 1960-present), 'long' "
             "(Maddison + Jordà-Schularick-Taylor, 1870-2020) or "
             "'quarterly' (FRED + Eurostat + OECD QNA, samples_per_year=4 — "
             "unlocks the full 3-5 y Kitchin band; Roadmap #9).",
    ),
    null: str = typer.Option(
        "ar1", "--null",
        help="Gate-1 null: 'ar1' (red-noise bootstrap on CF band-power, "
             "default), 'phase' (Theiler 1992 phase-scrambling), "
             "'wavelet' (AR(1) on Morlet wavelet band-power) or "
             "'dual' (require failure on BOTH ar1 AND phase).",
    ),
) -> None:
    """Position the world (and groups) in Kitchin/Juglar/Kuznets/Kondratieff cycles."""
    from ecowave.cycles.runner import run_position_cycles
    from pathlib import Path

    if horizon not in {"wb", "long", "quarterly", "boe", "bis", "sh"}:
        raise typer.BadParameter(
            "--horizon must be 'wb', 'long', 'quarterly', 'boe', 'bis' or 'sh'."
        )
    if null not in {"ar1", "phase", "wavelet", "dual"}:
        raise typer.BadParameter("--null must be ar1, phase, wavelet, or dual.")

    _DEFAULT_MANIFEST = {
        "wb":        "/app/cycles_manifest.json",
        "long":      "/app/long_history_manifest.json",
        "quarterly": "/app/quarterly_manifest.json",
        "boe":       "/app/boe_millennium_manifest.json",
        "bis":       "/app/bis_manifest.json",
        "sh":        "/app/sectoral_history_manifest.json",
    }
    _DEFAULT_GROUPS = {
        "wb":        "WLD,OECD,HIC,UMC,LMC,LIC,G7,BRICS",
        "long":      "ADV18,G7,USA,EU4,ANGLO,NORDIC",
        "quarterly": "USA,EA,JPN,GBR,G7Q,OECDQ",
        "boe":       "UK_BOE",
        "bis":       "BIS_EM,BIS_AE,BR_BIS,CN_BIS,IN_BIS,MX_BIS,KR_BIS,TR_BIS,ZA_BIS,RU_BIS,ID_BIS",
        "sh":        "US_SH,UK_SH,WORLD_SH",
    }
    if not manifest:
        manifest = _DEFAULT_MANIFEST[horizon]
    if not groups:
        groups = _DEFAULT_GROUPS[horizon]

    settings = Settings.from_env()
    group_list = [g.strip() for g in groups.split(",") if g.strip()]
    out = run_position_cycles(settings=settings, as_of=as_of,
                              manifest_path=Path(manifest),
                              groups=group_list, mode=mode,
                              n_surrogates=n_surrogates, seed=seed,
                              horizon=horizon, null=null)
    typer.echo(f"position-cycles complete: {out}")


@app.command("home-synthesis")
def home_synthesis(
    as_of: str = typer.Option("2026-05", "--as-of",
                              help="Target month (YYYY-MM) — must match the "
                                   "three position-cycles runs."),
    snippet_out: str = typer.Option(
        "/app/docs/_includes/home_synthesis_table.md", "--snippet-out",
        help="Path to the MkDocs snippet included from docs/index.md."),
    pvalues_snippet_out: str = typer.Option(
        "/app/docs/_includes/home_pvalues_table.md", "--pvalues-snippet-out",
        help="Path to the p-values matrix snippet (Gate 1 weight of evidence)."),
    note_out: str = typer.Option(
        "/app/reports/cycle_position_synthesis.md", "--note-out",
        help="Path to the cross-horizon synthesis note (signed)."),
) -> None:
    """Recompose the cross-horizon CPV view from the three sidecar JSONs.

    Reads ``reports/cycle_position_{as_of}_{wb,q,long}.json`` (written by
    ``position-cycles``) and emits three artifacts: the per-aggregate
    dashboard snippet, the Gate-1 p-values matrix snippet, and a full
    multi-horizon signed note.
    """
    from ecowave.cycles.report import (
        positions_sidecar_path,
        read_positions_sidecar,
        render_cross_horizon_synthesis_md,
        render_home_aggregates_table,
        render_home_pvalues_table,
    )
    from ecowave.db import get_schema_version

    settings = Settings.from_env()
    by_horizon = {
        h: read_positions_sidecar(
            positions_sidecar_path(settings.reports_dir, as_of, h))
        for h in ("wb", "q", "long", "boe", "bis", "sh")
    }
    missing = [h for h, t in by_horizon.items() if t.empty]
    if missing:
        typer.echo(
            f"Warning: missing sidecars for horizons {missing}. "
            f"Run `position-cycles --horizon <h>` first; rows will appear as "
            f"'en attente'.",
            err=True,
        )

    snippet_path = Path(snippet_out)
    snippet_path.parent.mkdir(parents=True, exist_ok=True)
    snippet_path.write_text(
        render_home_aggregates_table(by_horizon, as_of) + "\n",
        encoding="utf-8",
    )
    pvalues_path = Path(pvalues_snippet_out)
    pvalues_path.parent.mkdir(parents=True, exist_ok=True)
    pvalues_path.write_text(
        render_home_pvalues_table(by_horizon, as_of) + "\n",
        encoding="utf-8",
    )
    schema_version = get_schema_version(settings.db_path) or "unknown"
    render_cross_horizon_synthesis_md(as_of=as_of, by_horizon=by_horizon,
                                       schema_version=schema_version,
                                       out_path=Path(note_out))
    typer.echo(f"Home snippet   : {snippet_path}")
    typer.echo(f"P-values matrix: {pvalues_path}")
    typer.echo(f"Synthesis note : {note_out}")


@app.command("evidence-per-variable")
def evidence_per_variable(
    as_of: str = typer.Option("2026-05", "--as-of",
                              help="Target month (YYYY-MM) for the per-variable run."),
    horizons: str = typer.Option(
        "wb,q,long", "--horizons",
        help="Comma-separated horizons to recompute. Horizons not listed "
             "are loaded from existing sidecars (if any) so the rendered "
             "page still shows the full multi-horizon view."),
    null: str = typer.Option(
        "dual", "--null",
        help="Gate-1 null: 'ar1', 'phase', 'wavelet' or 'dual'. "
             "Default 'dual' for consistency with the composite runs.",
    ),
    n_surrogates: int = typer.Option(1000, "--n-surrogates"),
    seed: int = typer.Option(0, "--seed"),
    out_dir: str = typer.Option(
        "/app/reports", "--out-dir",
        help="Directory where per-variable JSON sidecars are written."),
    page_out: str = typer.Option(
        "/app/docs/evidence_per_variable.md", "--page-out",
        help="Path to the generated docs page."),
) -> None:
    """Run Gate 1 on **each individual variable** for the 3 horizons.

    Demonstrates the central thesis: cycles canoniques survive on
    sector-specific series (Kitchin → inventory/investment, Juglar → credit,
    etc.) but are diluted by the equal-weight composite. Reuses
    ``cycle_observations`` / ``cycle_observations_quarterly`` from SQLite —
    no re-ingestion required.
    """
    from pathlib import Path

    from ecowave.cycles.evidence import (
        HORIZON_VARIABLE_SOURCE,
        _load_annual_panel,
        _load_quarterly_panel,
        _load_variable_codes,
        compute_per_variable_evidence,
        read_evidence_sidecar,
        render_evidence_per_variable_md,
        write_evidence_sidecar,
    )
    from ecowave.db import connect

    if null not in {"ar1", "phase", "wavelet", "dual"}:
        raise typer.BadParameter("--null must be ar1, phase, wavelet, or dual.")

    settings = Settings.from_env()
    con = connect(settings.db_path)

    horizon_groups = {
        "wb":   ["WLD", "OECD", "HIC", "UMC", "LMC", "LIC", "G7", "BRICS"],
        "q":    ["USA", "EA", "JPN", "GBR", "G7Q", "OECDQ"],
        "long": ["ADV18", "G7", "USA", "EU4", "ANGLO", "NORDIC"],
        "boe":  ["UK_BOE"],
        "bis":  ["BIS_EM", "BIS_AE", "BR_BIS", "CN_BIS", "IN_BIS",
                  "MX_BIS", "KR_BIS", "TR_BIS", "ZA_BIS", "RU_BIS", "ID_BIS"],
        "sh":   ["US_SH", "UK_SH", "WORLD_SH"],
    }
    horizons_to_run = {h.strip() for h in horizons.split(",") if h.strip()}
    unknown = horizons_to_run - set(horizon_groups)
    if unknown:
        raise typer.BadParameter(
            f"--horizons unknown: {sorted(unknown)} "
            f"(expected subset of {sorted(horizon_groups)})"
        )
    out_root = Path(out_dir)
    evidence_dfs: dict[str, "pd.DataFrame"] = {}  # type: ignore[name-defined]

    for horizon, groups in horizon_groups.items():
        sidecar = out_root / (
            f"cycle_position_per_variable_{as_of.replace('-','_')}_{horizon}.json"
        )
        if horizon not in horizons_to_run:
            # Skipped on this invocation — load whatever a previous run wrote
            # so the page still aggregates the full multi-horizon evidence.
            df = read_evidence_sidecar(sidecar)
            if not df.empty:
                evidence_dfs[horizon] = df
                typer.echo(
                    f"horizon={horizon}: skipped (reusing sidecar with "
                    f"{len(df)} cells)"
                )
            else:
                typer.echo(
                    f"horizon={horizon}: skipped and no sidecar on disk — "
                    f"page will omit this horizon",
                    err=True,
                )
            continue
        manifest_path, kind = HORIZON_VARIABLE_SOURCE[horizon]
        variable_codes = _load_variable_codes(manifest_path)
        loader = _load_quarterly_panel if kind == "quarterly" else _load_annual_panel
        samples_per_year = 4.0 if kind == "quarterly" else 1.0
        panels_by_group: dict[str, "pd.DataFrame"] = {}  # type: ignore[name-defined]
        for group in groups:
            panel = loader(con, group, variable_codes)
            if not panel.empty:
                panels_by_group[group] = panel
        if not panels_by_group:
            typer.echo(
                f"horizon={horizon}: no observations in DB — skipped. "
                f"Run `ecowave position-cycles --horizon {horizon}` first.",
                err=True,
            )
            continue
        typer.echo(
            f"horizon={horizon}: {len(panels_by_group)} groups × "
            f"{len(variable_codes)} variables — running Gate 1 per variable…"
        )
        records = compute_per_variable_evidence(
            panels_by_group, samples_per_year=samples_per_year,
            n_surrogates=n_surrogates, null=null, seed=seed,
        )
        write_evidence_sidecar(records, sidecar)
        evidence_dfs[horizon] = read_evidence_sidecar(sidecar)
        typer.echo(f"  → {sidecar} ({len(records)} cells)")

    con.close()

    render_evidence_per_variable_md(
        evidence_by_horizon=evidence_dfs,
        groups_by_horizon=horizon_groups,
        as_of=as_of,
        out_path=Path(page_out),
    )
    typer.echo(f"Evidence page written: {page_out}")


@app.command("dx-diagnostics")
def dx_diagnostics(
    as_of: str = typer.Option("2026-05", "--as-of",
                              help="Target month (YYYY-MM)."),
    horizons: str = typer.Option(
        "wb,q,long,boe,bis,sh", "--horizons",
        help="Comma-separated horizons to (re)compute. Unknown horizons "
             "are loaded from existing sidecars (if any) for the rendered "
             "page."),
    n_surrogates: int = typer.Option(
        200, "--n-surrogates",
        help="Number of surrogates per diagnostic (AR(1) or phase-scramble). "
             "Default 200 — heavier than evidence-per-variable because every "
             "surrogate triggers a full recompute of the structural "
             "statistic (Hurst, MF-DFA, β, …)."),
    seed: int = typer.Option(0, "--seed"),
    out_dir: str = typer.Option(
        "/app/reports", "--out-dir",
        help="Directory for the JSON sidecars."),
    page_out: str = typer.Option(
        "/app/docs/dx_diagnostics.md", "--page-out",
        help="Path to the generated docs page."),
) -> None:
    """Run 11 non-cyclical diagnostics (Tier 1 of the beyond-cycles panorama).

    Covers families A (SOC 1/f^β + Hill tails), B (MF-DFA), C (DFA/Hurst),
    E (critical slowing down), G (RMT), I (permutation entropy +
    complexity), J (Lévy stable), P (K41 cascades), R (anomalous diffusion
    MSD), T (Tsallis q-Gaussian) and S (reflexivity drift — transversal
    component). Each diagnostic is scored against an AR(1) or
    phase-scramble null at α = 0.05, reproducing the Gate-1 philosophy
    on band-agnostic structure. Roadmap item #15.
    """
    from pathlib import Path

    from ecowave.cycles.alternative_dynamics import (
        compute_per_variable_diagnostics,
        compute_rmt_per_group,
        load_panels_for_horizon,
        render_dx_diagnostics_md,
        write_diagnostics_sidecar,
        write_rmt_sidecar,
    )

    settings = Settings.from_env()
    horizons_to_run = {h.strip() for h in horizons.split(",") if h.strip()}
    known = {"wb", "q", "long", "boe", "bis", "sh"}
    unknown = horizons_to_run - known
    if unknown:
        raise typer.BadParameter(
            f"--horizons unknown: {sorted(unknown)} "
            f"(expected subset of {sorted(known)})"
        )

    out_root = Path(out_dir)
    results_by_horizon: dict[str, list[dict]] = {}
    rmt_by_horizon: dict[str, list[dict]] = {}

    for horizon in sorted(horizons_to_run):
        panels = load_panels_for_horizon(settings.db_path, horizon)
        if not panels:
            typer.echo(
                f"horizon={horizon}: no observations in DB — skipped. "
                f"Run `ecowave position-cycles --horizon {horizon}` first.",
                err=True,
            )
            continue
        typer.echo(
            f"horizon={horizon}: {len(panels)} groups — "
            f"running 11 diagnostics per variable with "
            f"{n_surrogates} surrogates each…"
        )
        records = compute_per_variable_diagnostics(
            panels, n_surrogates=n_surrogates, seed=seed)
        rmt_records = compute_rmt_per_group(panels)
        diag_sidecar = out_root / (
            f"dx_diagnostics_{as_of.replace('-','_')}_{horizon}.json"
        )
        rmt_sidecar = out_root / (
            f"dx_rmt_{as_of.replace('-','_')}_{horizon}.json"
        )
        write_diagnostics_sidecar(records, diag_sidecar)
        write_rmt_sidecar(rmt_records, rmt_sidecar)
        results_by_horizon[horizon] = records
        rmt_by_horizon[horizon] = rmt_records
        typer.echo(f"  → {diag_sidecar} ({len(records)} cells)")
        typer.echo(f"  → {rmt_sidecar} ({len(rmt_records)} groups)")

    render_dx_diagnostics_md(
        results_by_horizon=results_by_horizon,
        rmt_by_horizon=rmt_by_horizon,
        as_of=as_of,
        out_path=Path(page_out),
    )
    typer.echo(f"Diagnostics page written: {page_out}")


@app.command("sources")
def sources(
    output: str = typer.Option("/app/docs/sources.md", "--output"),
    manifest: str = typer.Option("/app/sources_manifest.json", "--manifest"),
) -> None:
    """Generate the cited data-sources page from the manifest."""
    from ecowave.ingest.manifest import load_manifest
    from ecowave.reports.sources import render_sources_markdown

    md = render_sources_markdown(load_manifest(Path(manifest)))
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    typer.echo(f"Sources page written: {out}")


@app.command("evaluate-ews")
def evaluate_ews(
    output: str = typer.Option("/app/reports/ews_validation.md", "--output"),
) -> None:
    """Out-of-sample AUROC of stress vs reference crisis dating, across all pilots."""
    from ecowave.evaluation import evaluate_all

    settings = Settings.from_env()
    evals, pooled, md = evaluate_all(settings)
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    typer.echo(f"Pooled AUROC (mean stress) = {pooled:.3f} over {len(evals)} pilot(s).")
    typer.echo(f"EWS validation written: {out}")


@app.command("generate-report")
def generate_report(
    pilot: str = typer.Option("2008", "--pilot"),
    mode: str = typer.Option("exploratory", "--mode"),
) -> None:
    """Generate Markdown report from current processed outputs."""
    settings = Settings.from_env()
    path = generate_report_impl(settings=settings, pilot=pilot, mode=mode)
    typer.echo(f"Report generated: {path}")


@app.command("forecast-benchmark")
def forecast_benchmark(
    as_of: str = typer.Option("2026-05", "--as-of",
                              help="Tag (YYYY-MM) for sidecar and page outputs."),
    horizon_data: str = typer.Option(
        "long", "--horizon-data",
        help="Panel to benchmark on: 'wb', 'long', 'q', 'boe', 'bis' or 'sh'."),
    horizons: str = typer.Option(
        "1,3,6,12", "--horizons",
        help="Comma-separated forecast horizons in cadence steps."),
    models: str = typer.Option(
        "rw,ar1,arma11,har,arfima_rs,msm", "--models",
        help="Comma-separated subset of benchmark models."),
    groups: str = typer.Option(
        "", "--groups",
        help="Comma-separated group codes. Defaults to a small subset per "
             "panel for tractability."),
    variables_limit: int = typer.Option(
        8, "--variables-limit",
        help="Maximum number of variables per group (top by length)."),
    n_origins: int = typer.Option(6, "--n-origins"),
    n_samples: int = typer.Option(200, "--n-samples"),
    test_fraction: float = typer.Option(0.25, "--test-fraction"),
    min_train_length: int = typer.Option(
        64, "--min-train-length",
        help="Minimum in-sample length for benchmark fits. Lower "
             "(40–50) for short annual panels (WB, SH) at the cost of "
             "less stable MSM estimation. Floor: 32."),
    decision_horizon: int = typer.Option(
        12, "--decision-horizon",
        help="Horizon at which the acceptance criterion is evaluated."),
    beat_threshold: float = typer.Option(0.5, "--beat-threshold"),
    seed: int = typer.Option(0, "--seed"),
    sidecar_path: str = typer.Option(
        "", "--sidecar-path",
        help="Override the JSON sidecar location."),
    page_path: str = typer.Option(
        "/app/docs/forecast_benchmark.md", "--page-path"),
) -> None:
    """Run the Roadmap #20 forecast benchmark and emit verdict + page."""
    from ecowave.cycles.evidence import (
        HORIZON_VARIABLE_SOURCE,
        _load_annual_panel,
        _load_quarterly_panel,
        _load_variable_codes,
    )
    from ecowave.db import connect
    from ecowave.forecasting.benchmark import (
        ALL_MODEL_NAMES,
        BenchmarkConfig,
        evaluate_acceptance_criterion,
        run_benchmark,
    )
    from ecowave.forecasting.har import HARLagConfig
    from ecowave.forecasting.reporting import (
        render_benchmark_page,
        write_benchmark_sidecar,
    )

    horizon_groups_default: dict[str, list[str]] = {
        "wb":   ["WLD", "HIC"],
        "q":    ["USA", "EA"],
        "long": ["ADV18", "G7"],
        "boe":  ["UK_BOE"],
        "bis":  ["BIS_AE", "BIS_EM"],
        "sh":   ["US_SH", "WORLD_SH"],
    }
    if horizon_data not in HORIZON_VARIABLE_SOURCE:
        raise typer.BadParameter(
            f"--horizon-data must be one of {sorted(HORIZON_VARIABLE_SOURCE)}"
        )
    selected_groups = (
        [g.strip() for g in groups.split(",") if g.strip()]
        if groups.strip()
        else horizon_groups_default[horizon_data]
    )
    horizons_tuple = tuple(int(h) for h in horizons.split(",") if h.strip())
    models_tuple = tuple(m.strip() for m in models.split(",") if m.strip())
    invalid_models = set(models_tuple) - set(ALL_MODEL_NAMES)
    if invalid_models:
        raise typer.BadParameter(
            f"--models unknown: {sorted(invalid_models)} (valid: {ALL_MODEL_NAMES})"
        )

    manifest_path, kind = HORIZON_VARIABLE_SOURCE[horizon_data]
    variable_codes = _load_variable_codes(manifest_path)
    loader = _load_quarterly_panel if kind == "quarterly" else _load_annual_panel

    settings = Settings.from_env()
    con = connect(settings.db_path)
    panels_for_benchmark: dict[str, dict[str, "np.ndarray"]] = {}  # type: ignore[name-defined]
    for group in selected_groups:
        panel = loader(con, group, variable_codes)
        if panel.empty:
            continue
        sorted_columns = sorted(
            panel.columns, key=lambda col: int(panel[col].dropna().size), reverse=True
        )
        kept_columns = sorted_columns[:variables_limit]
        panels_for_benchmark[group] = {
            column: panel[column].dropna().to_numpy(dtype=float)
            for column in kept_columns
        }
    con.close()

    if not panels_for_benchmark:
        raise typer.BadParameter(
            f"No data found for horizon-data={horizon_data} and "
            f"groups={selected_groups}. Run `ecowave position-cycles "
            f"--horizon {horizon_data}` first."
        )

    har_lag_config = HARLagConfig(1, 3, 12) if kind != "quarterly" else HARLagConfig(1, 2, 4)
    config = BenchmarkConfig(
        horizons=horizons_tuple,
        models=models_tuple,
        n_origins=n_origins,
        n_samples=n_samples,
        test_fraction=test_fraction,
        seed=seed,
        har_lag_config=har_lag_config,
        min_train_length=min_train_length,
    )

    typer.echo(
        f"Running benchmark on {sum(len(v) for v in panels_for_benchmark.values())} "
        f"variables across {len(panels_for_benchmark)} groups, "
        f"{len(models_tuple)} models, {len(horizons_tuple)} horizons, "
        f"{n_origins} origins…"
    )
    results = run_benchmark(panels_for_benchmark, config=config)
    verdict = evaluate_acceptance_criterion(
        results,
        decision_horizon=decision_horizon,
        beat_threshold=beat_threshold,
    )

    sidecar = (
        Path(sidecar_path)
        if sidecar_path
        else Path(
            f"/app/reports/forecast_benchmark_{as_of.replace('-','_')}_"
            f"{horizon_data}.json"
        )
    )
    write_benchmark_sidecar(
        results, verdict, sidecar, as_of=as_of, horizon_data_code=horizon_data
    )
    render_benchmark_page(
        results, verdict, Path(page_path), as_of=as_of, horizon_data_code=horizon_data
    )
    typer.echo(
        f"Verdict: pass_rate={verdict.pass_rate:.0%} "
        f"({'PASS' if verdict.passes else 'FAIL'}) at h={decision_horizon}. "
        f"Sidecar → {sidecar}. Page → {page_path}."
    )


@app.command("forecast-benchmark-consolidate")
def forecast_benchmark_consolidate(
    as_of: str = typer.Option("2026-05", "--as-of"),
    reports_dir: str = typer.Option("/app/reports", "--reports-dir"),
    panels: str = typer.Option(
        "wb,q,long,boe,bis,sh", "--panels",
        help="Comma-separated panel codes to consolidate."),
    beat_threshold: float = typer.Option(0.5, "--beat-threshold"),
    page_path: str = typer.Option(
        "/app/docs/forecast_benchmark.md", "--page-path"),
) -> None:
    """Aggregate per-panel benchmark sidecars into a single docs page."""
    from ecowave.forecasting.consolidated_report import (
        consolidate_benchmark_sidecars,
        render_consolidated_page,
    )

    panel_codes = tuple(p.strip() for p in panels.split(",") if p.strip())
    summary = consolidate_benchmark_sidecars(
        reports_dir=Path(reports_dir),
        as_of=as_of,
        panel_codes=panel_codes,
        beat_threshold=beat_threshold,
    )
    render_consolidated_page(summary, Path(page_path))
    typer.echo(
        f"Consolidated verdict: aggregate pass rate "
        f"{summary.aggregate_pass_rate:.0%} "
        f"({'PASS' if summary.passes else 'FAIL'}) on "
        f"{summary.total_passing}/{summary.total_variables} variables "
        f"across {len(summary.panels)} panels "
        f"(missing: {list(summary.missing_panels) or 'none'}). "
        f"Page → {page_path}."
    )


@app.command("render-hub-index")
def render_hub_index_cli(
    as_of: str = typer.Option("2026-05", "--as-of"),
    reports_dir: str = typer.Option("/app/reports", "--reports-dir"),
    index_path: str = typer.Option("/app/docs/index.md", "--index-path"),
    panels: str = typer.Option(
        "wb,q,long,boe,bis,sh", "--panels",
        help="Comma-separated panel codes to consolidate for the verdict block."),
    beat_threshold: float = typer.Option(0.5, "--beat-threshold"),
) -> None:
    """Refresh the AUTO-VERDICT block of the hub home page from sidecars."""
    from ecowave.forecasting.hub_index import render_hub_index_from_reports

    panel_codes = tuple(p.strip() for p in panels.split(",") if p.strip())
    summary = render_hub_index_from_reports(
        reports_dir=Path(reports_dir),
        index_path=Path(index_path),
        as_of=as_of,
        panel_codes=panel_codes,
        beat_threshold=beat_threshold,
    )
    typer.echo(
        f"Hub index refreshed: pass rate {summary.aggregate_pass_rate:.0%} "
        f"({'PASS' if summary.passes else 'FAIL'}) on "
        f"{summary.total_passing}/{summary.total_variables} variables. "
        f"Index → {index_path}."
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
