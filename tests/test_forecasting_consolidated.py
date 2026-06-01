"""Tests for the consolidated benchmark report.

Use synthetic sidecar JSONs written to ``tmp_path`` — no Docker SQLite,
no real benchmark run. Verifies (i) sidecar decoding, (ii) cross-panel
aggregation arithmetic, (iii) leaderboard ordering, (iv) page rendering
contract, (v) missing-panel handling, (vi) schema-version guard.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from ecowave.forecasting.consolidated_report import (
    SUPPORTED_SCHEMA_VERSION,
    consolidate_benchmark_sidecars,
    render_consolidated_page,
)


def _write_synthetic_sidecar(
    reports_dir: Path,
    as_of: str,
    panel_code: str,
    n_variables: int,
    best_per_variable: dict[str, str],
    beats_per_variable: dict[str, bool],
    schema_version: int = SUPPORTED_SCHEMA_VERSION,
) -> Path:
    as_of_token = as_of.replace("-", "_")
    sidecar_path = (
        reports_dir / f"forecast_benchmark_{as_of_token}_{panel_code}.json"
    )
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    n_passes = sum(1 for label in best_per_variable if beats_per_variable.get(label))
    payload = {
        "schema_version": schema_version,
        "generated_at": "2026-06-01T18:00:00+00:00",
        "as_of": as_of,
        "horizon_data_code": panel_code,
        "config": {
            "horizons": [1, 3, 6, 12],
            "models": ["rw", "ar1", "har", "arfima_rs", "msm"],
            "n_origins": 6,
            "n_samples": 200,
            "test_fraction": 0.25,
            "seed": 0,
            "msm_components": 4,
        },
        "verdict": {
            "decision_horizon": 12,
            "beat_threshold": 0.5,
            "n_variables_total": n_variables,
            "n_variables_with_baseline": n_variables,
            "pass_rate": n_passes / n_variables if n_variables else 0.0,
            "passes": (n_passes / n_variables if n_variables else 0.0) >= 0.5,
            "best_cluster_model_per_variable": best_per_variable,
            "cluster_beats_baseline_per_variable": beats_per_variable,
        },
        "cells": [],
        "failures": [],
    }
    sidecar_path.write_text(json.dumps(payload), encoding="utf-8")
    return sidecar_path


def test_consolidate_aggregates_pass_rate_across_panels(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "wb",
        n_variables=4,
        best_per_variable={"WLD::X1": "msm", "WLD::X2": "har", "WLD::X3": "", "WLD::X4": "msm"},
        beats_per_variable={"WLD::X1": True, "WLD::X2": True, "WLD::X3": False, "WLD::X4": False},
    )
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "long",
        n_variables=2,
        best_per_variable={"ADV18::Y1": "arfima_rs", "ADV18::Y2": "msm"},
        beats_per_variable={"ADV18::Y1": True, "ADV18::Y2": True},
    )
    summary = consolidate_benchmark_sidecars(
        tmp_path, as_of="2026-05", panel_codes=("wb", "long")
    )

    assert summary.total_variables == 6
    assert summary.total_passing == 4
    assert summary.aggregate_pass_rate == pytest.approx(4 / 6)
    assert summary.passes is True
    assert summary.decision_horizon == 12


def test_consolidate_marks_missing_panels_without_failing(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "long",
        n_variables=3,
        best_per_variable={"ADV18::Z1": "msm", "ADV18::Z2": "msm", "ADV18::Z3": "har"},
        beats_per_variable={"ADV18::Z1": True, "ADV18::Z2": True, "ADV18::Z3": False},
    )
    summary = consolidate_benchmark_sidecars(
        tmp_path, as_of="2026-05", panel_codes=("wb", "q", "long")
    )

    assert set(summary.missing_panels) == {"wb", "q"}
    assert len(summary.panels) == 1
    assert summary.total_variables == 3
    assert summary.aggregate_pass_rate == pytest.approx(2 / 3)


def test_consolidate_leaderboard_ranks_models_by_wins(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "long",
        n_variables=5,
        best_per_variable={
            "G::V1": "msm",
            "G::V2": "msm",
            "G::V3": "msm",
            "G::V4": "har",
            "G::V5": "arfima_rs",
        },
        beats_per_variable={
            "G::V1": True,
            "G::V2": True,
            "G::V3": True,
            "G::V4": True,
            "G::V5": True,
        },
    )
    summary = consolidate_benchmark_sidecars(
        tmp_path, as_of="2026-05", panel_codes=("long",)
    )
    leaderboard = summary.leaderboard()

    assert leaderboard[0] == ("msm", 3)
    assert {model: count for model, count in leaderboard} == {
        "msm": 3,
        "har": 1,
        "arfima_rs": 1,
    }


def test_consolidate_rejects_unsupported_schema_version(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "long",
        n_variables=2,
        best_per_variable={"G::V1": "msm", "G::V2": "har"},
        beats_per_variable={"G::V1": True, "G::V2": True},
        schema_version=99,
    )
    with pytest.raises(ValueError, match="schema_version"):
        consolidate_benchmark_sidecars(
            tmp_path, as_of="2026-05", panel_codes=("long",)
        )


def test_consolidate_rejects_inconsistent_decision_horizons(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "wb",
        n_variables=2,
        best_per_variable={"X::V1": "msm", "X::V2": "msm"},
        beats_per_variable={"X::V1": True, "X::V2": True},
    )
    # Override decision_horizon to 6 in the second sidecar.
    long_sidecar = (
        tmp_path / "forecast_benchmark_2026_05_long.json"
    )
    long_payload = {
        "schema_version": 1,
        "generated_at": "2026-06-01T18:00:00+00:00",
        "as_of": "2026-05",
        "horizon_data_code": "long",
        "config": {
            "horizons": [1, 6],
            "models": ["rw", "msm"],
            "n_origins": 4,
            "n_samples": 100,
            "test_fraction": 0.25,
            "seed": 0,
            "msm_components": 4,
        },
        "verdict": {
            "decision_horizon": 6,
            "beat_threshold": 0.5,
            "n_variables_total": 2,
            "n_variables_with_baseline": 2,
            "pass_rate": 1.0,
            "passes": True,
            "best_cluster_model_per_variable": {"L::A": "msm", "L::B": "msm"},
            "cluster_beats_baseline_per_variable": {"L::A": True, "L::B": True},
        },
        "cells": [],
        "failures": [],
    }
    long_sidecar.write_text(json.dumps(long_payload), encoding="utf-8")

    with pytest.raises(ValueError, match="inconsistent decision horizons"):
        consolidate_benchmark_sidecars(
            tmp_path, as_of="2026-05", panel_codes=("wb", "long")
        )


def test_render_consolidated_page_writes_expected_sections(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "wb",
        n_variables=3,
        best_per_variable={"W::A": "msm", "W::B": "har", "W::C": "msm"},
        beats_per_variable={"W::A": True, "W::B": True, "W::C": True},
    )
    summary = consolidate_benchmark_sidecars(
        tmp_path, as_of="2026-05", panel_codes=("wb",)
    )
    page_path = tmp_path / "consolidated.md"
    render_consolidated_page(summary, page_path)

    body = page_path.read_text(encoding="utf-8")
    assert "verdict consolidé" in body
    assert "Verdict global" in body
    assert "Leaderboard" in body
    assert "msm" in body
    assert ("PASS" in body) or ("FAIL" in body)
