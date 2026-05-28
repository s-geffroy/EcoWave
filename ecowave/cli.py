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
    manifest: str = typer.Option("/app/cycles_manifest.json", "--manifest"),
    groups: str = typer.Option("WLD,OECD,HIC,UMC,LMC,LIC,G7,BRICS", "--groups",
                                help="Comma-separated group codes."),
    mode: str = typer.Option("strict", "--mode"),
    n_surrogates: int = typer.Option(1000, "--n-surrogates"),
    seed: int = typer.Option(0, "--seed"),
) -> None:
    """Position the world (and groups) in Kitchin/Juglar/Kuznets/Kondratieff cycles."""
    from ecowave.cycles.runner import run_position_cycles
    from pathlib import Path

    settings = Settings.from_env()
    group_list = [g.strip() for g in groups.split(",") if g.strip()]
    out = run_position_cycles(settings=settings, as_of=as_of,
                              manifest_path=Path(manifest),
                              groups=group_list, mode=mode,
                              n_surrogates=n_surrogates, seed=seed)
    typer.echo(f"position-cycles complete: {out}")


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


def main() -> None:
    app()


if __name__ == "__main__":
    main()
