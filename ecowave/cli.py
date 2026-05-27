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
    """Run the full pilot pipeline."""
    settings = Settings.from_env()
    run_pilot_impl(settings=settings, pilot=pilot, mode=mode)


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
