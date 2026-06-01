"""JSON sidecar + markdown rendering for the forecast benchmark.

The shape of the sidecar is intentionally narrow — one record per
``(group, variable, model, horizon)`` carrying mean and median CRPS,
RMSE, MAE, coverage and tail rates aggregated across origins. The
markdown page produced by :func:`render_benchmark_page` mirrors the
``dx_diagnostics`` styling : heatmap-coloured tables for at-a-glance
ranking, a verdict section that quotes the acceptance criterion of
:doc:`item #20 <feuille_de_route>`, and a per-variable breakdown.
"""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ecowave.forecasting.benchmark import (
    AcceptanceVerdict,
    BenchmarkResults,
    CLUSTER_MODEL_NAMES,
)


def aggregate_per_cell(results: BenchmarkResults) -> list[dict]:
    """One record per ``(group, variable, model, horizon)`` with summary scores."""
    buckets: dict[
        tuple[str, str, str, int], dict[str, list[float]]
    ] = defaultdict(
        lambda: {
            "crps": [],
            "rmse": [],
            "mae": [],
            "coverage_95": [],
            "tail_left_5pct": [],
            "tail_right_5pct": [],
            "bias": [],
        }
    )
    for row in results.score_rows:
        key = (row.group, row.variable, row.model, row.horizon)
        bucket = buckets[key]
        bucket["crps"].append(row.crps)
        bucket["rmse"].append(row.rmse)
        bucket["mae"].append(row.mae)
        bucket["coverage_95"].append(row.coverage_95)
        bucket["tail_left_5pct"].append(row.tail_left_5pct)
        bucket["tail_right_5pct"].append(row.tail_right_5pct)
        bucket["bias"].append(row.bias)
    records: list[dict] = []
    for (group, variable, model, horizon), values in buckets.items():
        record = {
            "group": group,
            "variable": variable,
            "model": model,
            "horizon": int(horizon),
            "n_origins": len(values["crps"]),
            "mean_crps": float(np.mean(values["crps"])),
            "median_crps": float(np.median(values["crps"])),
            "mean_rmse": float(np.mean(values["rmse"])),
            "mean_mae": float(np.mean(values["mae"])),
            "mean_coverage_95": float(np.mean(values["coverage_95"])),
            "mean_tail_left_5pct": float(np.mean(values["tail_left_5pct"])),
            "mean_tail_right_5pct": float(np.mean(values["tail_right_5pct"])),
            "mean_bias": float(np.mean(values["bias"])),
        }
        records.append(record)
    return records


def write_benchmark_sidecar(
    results: BenchmarkResults,
    verdict: AcceptanceVerdict,
    out_path: Path,
    as_of: str,
    horizon_data_code: str,
) -> None:
    """Write the JSON sidecar holding aggregated cell records + verdict."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "as_of": as_of,
        "horizon_data_code": horizon_data_code,
        "config": {
            "horizons": list(results.config.horizons),
            "models": list(results.config.models),
            "n_origins": int(results.config.n_origins),
            "n_samples": int(results.config.n_samples),
            "test_fraction": float(results.config.test_fraction),
            "seed": int(results.config.seed),
            "msm_components": int(results.config.msm_components),
        },
        "verdict": {
            "decision_horizon": int(verdict.decision_horizon),
            "beat_threshold": float(verdict.beat_threshold),
            "n_variables_total": int(verdict.n_variables_total),
            "n_variables_with_baseline": int(verdict.n_variables_with_baseline),
            "pass_rate": float(verdict.pass_rate),
            "passes": bool(verdict.passes),
            "best_cluster_model_per_variable": dict(
                verdict.best_cluster_model_per_variable
            ),
            "cluster_beats_baseline_per_variable": {
                key: bool(value)
                for key, value in verdict.cluster_beats_baseline_per_variable.items()
            },
        },
        "cells": aggregate_per_cell(results),
        "failures": [dict(failure) for failure in results.failed_evaluations],
    }
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _format_crps_table(records: list[dict], horizon: int) -> str:
    """Markdown table of mean CRPS per (group::variable, model) at ``horizon``."""
    pivot: dict[str, dict[str, float]] = defaultdict(dict)
    models_seen: set[str] = set()
    for record in records:
        if record["horizon"] != horizon:
            continue
        label = f"{record['group']}::{record['variable']}"
        pivot[label][record["model"]] = record["mean_crps"]
        models_seen.add(record["model"])
    if not pivot:
        return "_No cells at this horizon._\n"
    model_order = ["rw", "ar1", "arma11", "har", "arfima_rs", "msm"]
    sorted_models = [model for model in model_order if model in models_seen]
    header = "| variable | " + " | ".join(sorted_models) + " | best |"
    separator = "|---|" + "|".join(["---"] * (len(sorted_models) + 1)) + "|"
    lines = [header, separator]
    for variable_label in sorted(pivot):
        cells = pivot[variable_label]
        baseline_crps = cells.get("rw")
        formatted: list[str] = []
        best_model = ""
        best_crps = float("inf")
        for model in sorted_models:
            value = cells.get(model)
            if value is None:
                formatted.append("—")
                continue
            cell_string = f"{value:.4f}"
            if (
                model in CLUSTER_MODEL_NAMES
                and baseline_crps is not None
                and value < baseline_crps
            ):
                cell_string = f"**{cell_string}**"
            formatted.append(cell_string)
            if model in CLUSTER_MODEL_NAMES and value < best_crps:
                best_crps = value
                best_model = model
        beats_baseline = (
            best_model
            and baseline_crps is not None
            and best_crps < baseline_crps
        )
        best_cell = f"{best_model} ✓" if beats_baseline else (best_model or "—")
        lines.append(
            f"| {variable_label} | " + " | ".join(formatted) + f" | {best_cell} |"
        )
    return "\n".join(lines) + "\n"


def render_benchmark_page(
    results: BenchmarkResults,
    verdict: AcceptanceVerdict,
    out_path: Path,
    as_of: str,
    horizon_data_code: str,
) -> None:
    """Render the consolidated markdown page for the docs site."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    aggregated = aggregate_per_cell(results)
    verdict_emoji = "✅" if verdict.passes else "❌"
    verdict_blurb = (
        "The empirical-cluster picture gains a constructive operational "
        "counterpart — at least one cluster model outperforms the random "
        "walk on out-of-sample CRPS at the decision horizon on the "
        f"required {int(verdict.beat_threshold * 100)} % of variables."
        if verdict.passes
        else "The empirical-cluster picture does **not** yet deliver an "
        "operational forecast improvement against the random-walk "
        "benchmark — pass rate is below the falsifiable threshold. The "
        "working paper V2 must report this honestly."
    )

    lines: list[str] = [
        "# Forecast benchmark — Roadmap #20",
        "",
        "> **Run.** `as_of = " + as_of + "`, horizon data `" + horizon_data_code + "`.",
        "",
        "## Verdict",
        "",
        f"{verdict_emoji} **{'PASS' if verdict.passes else 'FAIL'}** — pass rate "
        f"{verdict.pass_rate:.0%} (threshold {verdict.beat_threshold:.0%}) on "
        f"{verdict.n_variables_with_baseline} variables with baseline "
        f"comparator at horizon {verdict.decision_horizon}.",
        "",
        verdict_blurb,
        "",
        "## Mean CRPS — decision horizon",
        "",
        f"At the decision horizon ``h = {verdict.decision_horizon}``. Cluster "
        "models that beat the random-walk baseline appear in **bold**.",
        "",
        _format_crps_table(aggregated, verdict.decision_horizon),
    ]

    horizons_other = sorted(set(record["horizon"] for record in aggregated))
    for horizon in horizons_other:
        if horizon == verdict.decision_horizon:
            continue
        lines.append(f"## Mean CRPS — h = {horizon}")
        lines.append("")
        lines.append(_format_crps_table(aggregated, horizon))
        lines.append("")

    if verdict.cluster_beats_baseline_per_variable:
        lines.append("## Per-variable pass/fail")
        lines.append("")
        lines.append("| variable | best cluster model | beats RW @ h = "
                      f"{verdict.decision_horizon} |")
        lines.append("|---|---|---|")
        for variable_label in sorted(verdict.cluster_beats_baseline_per_variable):
            beats = verdict.cluster_beats_baseline_per_variable[variable_label]
            best_model = verdict.best_cluster_model_per_variable.get(
                variable_label, "—"
            )
            lines.append(
                f"| {variable_label} | {best_model or '—'} | "
                f"{'✓' if beats else '✗'} |"
            )
        lines.append("")

    if results.failed_evaluations:
        lines.append("## Failed evaluations")
        lines.append("")
        lines.append(
            f"{len(results.failed_evaluations)} forecasts raised exceptions and "
            "were excluded from the scores. First 10 reproduced below for "
            "diagnostic purposes."
        )
        lines.append("")
        lines.append("| group | variable | model | origin | error |")
        lines.append("|---|---|---|---|---|")
        for failure in results.failed_evaluations[:10]:
            lines.append(
                f"| {failure['group']} | {failure['variable']} | "
                f"{failure['model']} | {failure['origin_index']} | "
                f"`{failure['error'][:80]}` |"
            )
        lines.append("")

    lines.append("## Method")
    lines.append("")
    lines.append(
        "Each variable's tail is held out as the test region. Inside the "
        f"test region we place ``n_origins = {results.config.n_origins}`` "
        "evenly-spaced forecast origins, fit each model on the history "
        "up to the origin, and score the resulting probabilistic "
        "forecast against the realised value at each horizon. Scores are "
        "averaged across origins to yield the per-cell summary tables "
        "above. Probabilistic samples per forecast: "
        f"``{results.config.n_samples}``. RNG seed: "
        f"``{results.config.seed}``. CRPS is the proper scoring rule of "
        "Gneiting-Raftery 2007 ; lower is better."
    )
    lines.append("")
    lines.append(
        "Generated at "
        f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} by "
        "`ecowave forecast-benchmark`."
    )
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
