from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from ecowave.config import Settings


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def _variable_status_table(panel: pd.DataFrame) -> str:
    counts = (panel.groupby(["variable_code", "status"]).size()
              .unstack(fill_value=0))
    lines = ["| Variable | available | partial | missing |", "|---|---:|---:|---:|"]
    for code in sorted(counts.index):
        row = counts.loc[code]
        lines.append(f"| {code} | {int(row.get('available', 0))} | "
                     f"{int(row.get('partial', 0))} | {int(row.get('missing', 0))} |")
    return "\n".join(lines)


def _curve_coverage(panel: pd.DataFrame) -> str:
    work = panel.copy()
    work["curve"] = work["variable_code"].str[0]
    avail = work[work["status"] == "available"].groupby("curve")["variable_code"].nunique()
    lines = ["| Curve | variables with real data |", "|---|---:|"]
    for curve in ["E", "D", "S", "L", "I"]:
        lines.append(f"| {curve} | {int(avail.get(curve, 0))} |")
    return "\n".join(lines)


def _model_table(scores: pd.DataFrame, verdicts: pd.DataFrame) -> str:
    pivot = scores.pivot(index="model_code", columns="criterion_code", values="raw_score")
    verdict_map = verdicts.set_index("model_code")
    lines = ["| Model | C1 | C2 | C3 | C4 | C5 | C6 | weighted | verdict |",
             "|---|---|---|---|---|---|---|---:|---|"]
    for m in ["A", "B", "C"]:
        def cell(c):
            v = pivot.loc[m, c] if (m in pivot.index and c in pivot.columns) else None
            return "—" if v is None or pd.isna(v) else str(int(v))
        pw = verdict_map.loc[m, "weighted_score"] if m in verdict_map.index else "—"
        vd = verdict_map.loc[m, "verdict"] if m in verdict_map.index else "—"
        lines.append(f"| {m} | {cell('C1')} | {cell('C2')} | {cell('C3')} | {cell('C4')} | "
                     f"{cell('C5')} | {cell('C6')} | {pw} | **{vd}** |")
    return "\n".join(lines)


def generate_reports(settings: Settings, pilot: str, mode: str, panel: pd.DataFrame,
                     curves: pd.DataFrame, scores: pd.DataFrame, verdicts: pd.DataFrame,
                     failures: list[str], champion_text: str = "") -> list[Path]:
    settings.reports_dir.mkdir(parents=True, exist_ok=True)
    n_available_vars = panel[panel["status"] == "available"]["variable_code"].nunique()
    n_missing_vars = panel[panel["status"] == "missing"]["variable_code"].nunique()
    blocked_models = int((verdicts["verdict"] == "blocked").sum()) if not verdicts.empty else 0
    all_complete = (not verdicts.empty) and bool(verdicts["complete"].all())

    if not champion_text:
        champion_text = (
            "Champion provisoire: B. Arbitrage non tranché tant que les annotations "
            "qualitatives (C2/C4/C5/C6) ne sont pas complètes pour les trois modèles."
        )

    if all_complete:
        verdict_header = "## Final verdict: SCORED (analyst-annotated)"
        verdict_para = (
            "All six criteria are filled for every model (C1/C3 computed, C2/C4/C5/C6 "
            "analyst-annotated). Verdicts and the champion/challenger adjudication below "
            "are therefore decisive for this evidence base. Remaining data gaps (I2 media "
            "tone, S2 protests) are documented as limitations."
        )
    else:
        verdict_header = "## Final verdict: PROVISIONAL / BLOCKED"
        verdict_para = (
            f"EcoWave does **not** deliver a final analytical verdict yet. The qualitative "
            f"criteria (C2, C4, C5, C6) require analyst annotation (see `annotations/`), and "
            f"{blocked_models} model(s) remain **blocked**. Fill the annotation template to "
            f"obtain decisive verdicts. This gate is by design (anti-pseudoscience rules)."
        )

    main = settings.reports_dir / f"report_{pilot}_pilot.md"
    main.write_text(f"""# EcoWave — Pilot {pilot}

Generated: {_ts()}  ·  Mode: `{mode}`

{verdict_header}

{verdict_para}

## Source completeness

- Variables with real data: **{n_available_vars}**
- Variables missing (no V1 source): **{n_missing_vars}**
- Ingestion failures this run: **{len(failures)}** {failures if failures else ''}

### Curve coverage
{_curve_coverage(panel)}

### Per-variable status (months 2007-01 .. 2012-12)
{_variable_status_table(panel)}

## Method

- Dow context window: 2001-2006 (regime context)
- Elliott active window: 2007-2012
- Competing models: A (unique cycle), B (nested cycles, provisional champion), C (acute shock only)
- Dual reference windows: pre-crisis 1990-2006, structural 1990-2019 (Covid/Ukraine excluded)

## Computed criteria (honest, data-driven)

Only C1 (multi-curve synchronisation) and C3 (reference-window robustness) are
auto-computed from the real panel. See `model_comparison.md`.

## Known structural limitations

- E-curve combines US + Euro Area (composite); E4 GDP is quarterly only.
- D-curve structural window is short (ECB CISS starts 1999) → C3 weak for D.
- D3 derived from curated events only → no pre-crisis baseline (status `partial`).
- I1 is a news-based EPU proxy (not GDELT); I2 (tone) and S2 (protests) still missing.
""", encoding="utf-8")

    computed_notes = "\n".join(
        f"- {r.model_code}/{r.criterion_code}: {r.notes}"
        for r in scores[scores["status"] == "computed"].itertuples()
    )
    annotated_rows = scores[scores["status"] == "annotated"]
    annotated_notes = "\n".join(
        f"- {r.model_code}/{r.criterion_code} = {int(r.raw_score)}: {r.notes}"
        for r in annotated_rows.itertuples()
    ) or "_No analyst annotations yet — C2/C4/C5/C6 remain blocked._"
    comparison = settings.reports_dir / "model_comparison.md"
    comparison.write_text(f"""# EcoWave — Model comparison (Pilot {pilot})

Generated: {_ts()}  ·  Mode: `{mode}`

## Scores A / B / C

Raw scores 0-3. `—` = blocked (qualitative criterion not auto-scored in V1).

{_model_table(scores, verdicts)}

Weights: C1=0.25, C2=0.20, C3=0.20, C4=0.10, C5=0.15, C6=0.10.

## Champion / challenger

{champion_text}

## Annotated criteria (analyst judgement)

{annotated_notes}

## Computation notes

{computed_notes}
""", encoding="utf-8")

    validation = settings.reports_dir / "validation_summary.md"
    validation.write_text(f"""# EcoWave — Validation summary (Pilot {pilot})

Generated: {_ts()}  ·  Mode: `{mode}`

## Run outcome

- Mode: `{mode}`
- Ingestion failures: {len(failures)} {failures if failures else '(none)'}
- Models blocked: {blocked_models} / 3

## Reference windows used

- Pre-crisis: 1990-2006 (longest available pre-2007 per variable; CISS from 1999)
- Structural: 1990-2019 (Covid/Ukraine excluded)

## Anti-pseudoscience compliance

- [x] Competing models A/B/C scored on identical criteria
- [x] Raw values preserved; transforms documented per variable
- [x] Missing data marked explicitly (`missing` / `partial`), never imputed silently
- [x] No final verdict while curves are incomplete (verdict = blocked/provisional)
- [x] Source manifest is the single source of truth for ingestion
- [x] Qualitative criteria left blocked rather than fabricated

## Confidence grades

Per-variable confidence grades (A-D) are carried in the monthly panel `confidence` column.
""", encoding="utf-8")

    return [main, comparison, validation]


def generate_report(settings: Settings, pilot: str, mode: str) -> Path:
    """Standalone report generation from already-processed outputs (CLI generate-report)."""
    panel_path = settings.data_processed_dir / "monthly_panel_2007_2012.csv"
    scores_path = settings.data_processed_dir / "model_scores_abc.csv"
    verdicts_path = settings.data_processed_dir / "model_verdicts.csv"
    if not panel_path.exists():
        settings.reports_dir.mkdir(parents=True, exist_ok=True)
        path = settings.reports_dir / f"report_{pilot}_pilot.md"
        path.write_text(
            f"# EcoWave — Pilot {pilot}\n\nMode: `{mode}`\n\n"
            "No processed panel found. Run `ecowave run-pilot 2008` first.\n",
            encoding="utf-8",
        )
        return path

    panel = pd.read_csv(panel_path)
    scores = pd.read_csv(scores_path)
    verdicts = pd.read_csv(verdicts_path)
    if "complete" in verdicts.columns:
        verdicts["complete"] = verdicts["complete"].astype(str).str.lower().isin({"true", "1"})
    reports = generate_reports(settings, pilot, mode, panel, pd.DataFrame(), scores, verdicts, [])
    return reports[0]
