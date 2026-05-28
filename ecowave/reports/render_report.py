"""Pilot-report rendering for the CPV stack.

Generates two markdown files per pilot:

  - ``report_<pilot>_pilot.md`` — narrative: source completeness, curve
    coverage, method summary, known limitations.
  - ``model_comparison_<pilot>.md`` — per-method results: D/E/F/G sections,
    the per-model surrogate-null table, the headline-model null test.

The pilot report covers only the CPV stack: no champion adjudication, no
analyst-graded criteria, no pivot-detection sensitivity tables.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from ecowave.config import Settings
from ecowave.pilots import Pilot, get_pilot


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


def _criteria_table(scores: pd.DataFrame) -> str:
    """C1 / C3 auto-computed criteria for the four CPV votant models."""
    if scores.empty:
        return "_No scored models._"
    pivot = scores.pivot_table(index="model_code", columns="criterion_code",
                                values="raw_score", aggfunc="first")
    present = [m for m in ["D", "E", "F", "G", "H"] if m in pivot.index]
    lines = ["| Model | C1 (synchronisation) | C3 (robustness) |",
             "|---|---:|---:|"]
    for m in present:
        def cell(c):
            v = pivot.loc[m, c] if c in pivot.columns else None
            return "—" if v is None or pd.isna(v) else str(int(v))
        lines.append(f"| {m} | {cell('C1')} | {cell('C3')} |")
    return "\n".join(lines)


def _model_d_section(model_d: dict | None) -> str:
    if not model_d:
        return "_Model D (PELT) not run._"
    phases = "\n".join(f"- {label}: {start} → {end}"
                        for label, start, end in model_d["candidate_phases"])
    pen = model_d.get("penalty")
    pen_txt = (f"penalty = {pen:.2f}" if isinstance(pen, (int, float))
               else "single regime (fallback)")
    return (f"**{model_d.get('name', 'PELT change-point')}** — "
            f"{model_d.get('method', 'PELT (L2 cost)')}; {pen_txt}.\n\n{phases}")


def _model_e_section(model_e: dict | None) -> str:
    if not model_e:
        return "_Model E (Markov-switching) not run._"
    if model_e.get("fit_status") != "ok":
        return (f"**Markov-switching fallback** — "
                f"{model_e.get('fit_status', 'unavailable')}.")
    phases = "\n".join(f"- {label}: {start} → {end}"
                        for label, start, end in model_e["candidate_phases"])
    aic_bic = model_e.get("aic_bic_table", {})
    aic_bic_md = "; ".join(f"{k}: AIC={v['aic']}, BIC={v['bic']}"
                            for k, v in aic_bic.items())
    return (f"**{model_e['name']}** — {model_e['method']}; "
            f"BIC-selected k={model_e['selected_k']}. {aic_bic_md}.\n\n{phases}")


def _model_f_section(model_f: dict | None) -> str:
    if not model_f:
        return "_Model F not run._"
    status = model_f.get("fit_status", "unknown")
    p = model_f.get("ar1_pvalue")
    p_txt = f"p = {p:.3f}" if isinstance(p, (int, float)) else "p = —"
    if status != "ok":
        return (f"**CF Juglar + Hilbert fallback** — {status}; AR(1) {p_txt}. "
                "Phase cell published as `rejected_cycle` per Gate 1.")
    phase_lines = "\n".join(f"- {label}: {start} → {end}"
                            for label, start, end in model_f["candidate_phases"])
    return (f"**{model_f['name']}** — {model_f.get('method', 'CF + Hilbert')}; "
            f"AR(1) null {p_txt} (separable when p < 0.05).\n\n{phase_lines}")


def _model_g_section(model_g: dict | None) -> str:
    if not model_g:
        return "_Model G not run._"
    status = model_g.get("fit_status", "unknown")
    if status != "ok":
        return (f"**Bry-Boschan fallback** — {status}. No turning point "
                "survives the Harding-Pagan duration constraints.")
    phase_lines = "\n".join(f"- {label}: {start} → {end}"
                            for label, start, end in model_g["candidate_phases"])
    nP = model_g.get("n_peaks", 0)
    nT = model_g.get("n_troughs", 0)
    return (f"**{model_g['name']}** — {model_g.get('method', 'Bry-Boschan')}; "
            f"{nP} peak(s) / {nT} trough(s).\n\n{phase_lines}")


def _models_null_table(null_reports_by_model: dict | None) -> str:
    if not null_reports_by_model:
        return "_Per-model null test not run._"
    lines = [
        "Per-method η² phase-separation against two surrogate nulls "
        "(`random_seg` = boundary placement; `circ_shift` = cross-curve alignment). "
        "✓ beats chance at α=0.05; ⚠ red-flagged.",
        "",
        "| Model | real η² | random_seg p | circ_shift p | verdict |",
        "|---|---:|---:|---:|---|",
    ]
    for code in ["D", "E", "F", "G", "H"]:
        rep = null_reports_by_model.get(code)
        if rep is None:
            continue
        if "error" in rep:
            lines.append(f"| {code} | — | — | — | error: {rep['error']} |")
            continue
        results = {r.method: r for r in rep["results"]}
        seg = results.get("random_segmentation")
        shift = results.get("circular_shift")
        flagged = rep.get("flag_random") or rep.get("flag_shift")
        verdict = "⚠ ≈ chance" if flagged else "✓ beats chance"
        seg_p = f"{seg.p_value:.3f}" if seg else "—"
        shift_p = f"{shift.p_value:.3f}" if shift else "—"
        lines.append(f"| {code} | {rep['real']:.3f} | {seg_p} | {shift_p} | {verdict} |")
    return "\n".join(lines)


def _null_section(null_report: dict | None) -> str:
    if not null_report:
        return "_Headline null test not run._"
    lines = [
        f"Headline model (F) phase-separation: **mean η² = {null_report['real']:.3f}** "
        "(share of cross-curve stress variance explained by the model's phases).",
        "",
        "| Null | mean η² (null) | percentile | p-value | verdict |",
        "|---|---:|---:|---:|---|",
    ]
    for r in null_report["results"]:
        beats = "beats chance" if r.p_value < null_report["alpha"] \
            else "**RED FLAG: ≈ chance**"
        lines.append(f"| {r.method} | {r.null_mean:.3f} | {r.percentile:.1f}% | "
                     f"{r.p_value:.3f} | {beats} |")
    if null_report["flag_random"] or null_report["flag_shift"]:
        lines += ["", f"> ⚠️ The headline model is **not** distinguishable from a null "
                  f"at α={null_report['alpha']}: its multi-curve evidence may be coincidental."]
    return "\n".join(lines)


def generate_reports(settings: Settings, pilot_def: Pilot, mode: str, panel: pd.DataFrame,
                     curves: pd.DataFrame, scores: pd.DataFrame, verdicts: pd.DataFrame,
                     failures: list[str],
                     null_report: dict | None = None,
                     model_d: dict | None = None, model_e: dict | None = None,
                     model_f: dict | None = None, model_g: dict | None = None,
                     null_reports_by_model: dict | None = None) -> list[Path]:
    pilot = pilot_def.code
    window = f"{pilot_def.panel_start} .. {pilot_def.panel_end}"
    settings.reports_dir.mkdir(parents=True, exist_ok=True)
    n_available_vars = panel[panel["status"] == "available"]["variable_code"].nunique()
    n_missing_vars = panel[panel["status"] == "missing"]["variable_code"].nunique()

    main = settings.reports_dir / f"report_{pilot}_pilot.md"
    main.write_text(f"""# CPV — Pilot {pilot}: {pilot_def.title}

Generated: {_ts()}  ·  Mode: `{mode}`  ·  Window: {window}

## Method

The Cycle Position Vector (CPV) stack runs four methods on the panel's
composite intensity:

| Model | Method | Source |
|---|---|---|
| D | PELT change-point detection | Killick et al. 2012 |
| E | Markov-switching AR(1) | Hamilton 1989 |
| F | Christiano-Fitzgerald Juglar band-pass + Hilbert phase | Christiano-Fitzgerald 2003 |
| G | Bry-Boschan / Harding-Pagan turning-point dating | Harding & Pagan 2002 |

The same four-method stack applies to ``position-cycles``; for a crisis
pilot the horizon is short, so Model F may fall back (Juglar needs more
than two cycle lengths of data) while D/E/G still produce phases. Each
model is independently tested against the AR(1) surrogate null
(see ``methodology/cycle_validation_rules.md``).

## Source completeness

- Variables with real data: **{n_available_vars}**
- Variables missing (no source available): **{n_missing_vars}**
- Ingestion failures this run: **{len(failures)}** {failures if failures else ''}

### Curve coverage
{_curve_coverage(panel)}

### Per-variable status (months {window})
{_variable_status_table(panel)}

## Known limitations

- E-curve combines US + Euro Area (composite); E4 GDP is quarterly only.
- D-curve structural window is short (ECB CISS starts 1999) → C3 weak for D.
- D3 derived from curated events only → no pre-crisis baseline (status `partial`).
- I1 is a news-based EPU proxy; I2 (tone) and S2 (protests) remain missing.

See ``methodology/multi_cycle_decomposition.md`` for the full CPV protocol.
""", encoding="utf-8")

    computed_notes = "\n".join(
        f"- {r.model_code}/{r.criterion_code}: {r.notes}"
        for r in scores[scores["status"] == "computed"].itertuples()
    ) or "_No computed-criterion notes._"

    comparison = settings.reports_dir / f"model_comparison_{pilot}.md"
    comparison.write_text(f"""# CPV — Model comparison (Pilot {pilot}: {pilot_def.title})

Generated: {_ts()}  ·  Mode: `{mode}`  ·  Window: {window}

## Auto-computed criteria (C1 + C3)

C1 (multi-curve synchronisation) and C3 (reference-window robustness) are
the two falsifiable criteria scored by the pipeline. They are evaluated
against the η² phase-separation null (see ``methodology/cycle_validation_rules.md``).

{_criteria_table(scores)}

## CPV stack

### Model D — PELT change-point detection

{_model_d_section(model_d)}

### Model E — Markov-switching regimes

{_model_e_section(model_e)}

### Model F — CF Juglar band-pass + Hilbert phase (headline)

{_model_f_section(model_f)}

### Model G — Bry-Boschan / Harding-Pagan dating

{_model_g_section(model_g)}

## Surrogate null test (falsifiability)

### Headline (Model F)

{_null_section(null_report)}

### Per-method panel

{_models_null_table(null_reports_by_model)}

## Computation notes

{computed_notes}
""", encoding="utf-8")

    return [main, comparison]


def generate_report(settings: Settings, pilot: str, mode: str) -> Path:
    """Standalone report generation from already-processed outputs (CLI generate-report)."""
    pilot_def = get_pilot(pilot)
    stem = f"monthly_panel_{pilot_def.panel_start[:4]}_{pilot_def.panel_end[:4]}"
    panel_path = settings.data_processed_dir / f"{stem}.csv"
    scores_path = settings.data_processed_dir / f"model_scores_{pilot}.csv"
    verdicts_path = settings.data_processed_dir / f"model_verdicts_{pilot}.csv"
    if not panel_path.exists():
        settings.reports_dir.mkdir(parents=True, exist_ok=True)
        path = settings.reports_dir / f"report_{pilot}_pilot.md"
        path.write_text(
            f"# CPV — Pilot {pilot}\n\nMode: `{mode}`\n\n"
            f"No processed panel found. Run `ecowave run-pilot {pilot}` first.\n",
            encoding="utf-8",
        )
        return path

    panel = pd.read_csv(panel_path)
    scores = pd.read_csv(scores_path) if scores_path.exists() else pd.DataFrame()
    verdicts = pd.read_csv(verdicts_path) if verdicts_path.exists() else pd.DataFrame()
    if "complete" in verdicts.columns:
        verdicts["complete"] = (verdicts["complete"].astype(str).str.lower()
                                 .isin({"true", "1"}))
    reports = generate_reports(settings, pilot_def, mode, panel, pd.DataFrame(),
                                scores, verdicts, [])
    return reports[0] if reports else settings.reports_dir / f"report_{pilot}_pilot.md"
