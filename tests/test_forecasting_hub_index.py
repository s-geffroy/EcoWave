"""Tests for ``ecowave.forecasting.hub_index``.

Exercise the marker-based replacement on synthetic sidecars + a fake
home page. Confirms (i) the verdict block goes between the markers,
(ii) the rest of the file is preserved, (iii) absent markers raise.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from ecowave.forecasting.consolidated_report import (
    SUPPORTED_SCHEMA_VERSION,
    consolidate_benchmark_sidecars,
)
from ecowave.forecasting.hub_index import (
    AUTO_VERDICT_BEGIN_MARKER,
    AUTO_VERDICT_END_MARKER,
    render_hub_index,
    render_hub_index_from_reports,
    render_verdict_block,
)


def _write_synthetic_sidecar(
    reports_dir: Path,
    as_of: str,
    panel_code: str,
    n_variables: int,
    best_per_variable: dict[str, str],
    beats_per_variable: dict[str, bool],
) -> Path:
    """Write a minimal benchmark sidecar JSON to ``reports_dir``."""
    sidecar_path = (
        reports_dir / f"forecast_benchmark_{as_of.replace('-', '_')}_{panel_code}.json"
    )
    n_passes = sum(1 for label in best_per_variable if beats_per_variable.get(label))
    payload = {
        "schema_version": SUPPORTED_SCHEMA_VERSION,
        "generated_at": "2026-06-01T18:00:00+00:00",
        "as_of": as_of,
        "horizon_data_code": panel_code,
        "config": {
            "horizons": [1, 3, 6, 12],
            "models": ["rw", "har", "msm"],
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


def test_render_verdict_block_contains_pass_label_and_leaderboard(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "long",
        n_variables=4,
        best_per_variable={
            "G::A": "msm",
            "G::B": "msm",
            "G::C": "har",
            "G::D": "arfima_rs",
        },
        beats_per_variable={"G::A": True, "G::B": True, "G::C": True, "G::D": True},
    )
    summary = consolidate_benchmark_sidecars(
        tmp_path, as_of="2026-05", panel_codes=("long",)
    )
    block = render_verdict_block(summary)

    assert "PASS" in block
    assert "pass rate 100 %" in block or "pass rate 100" in block
    assert "MSM" in block
    assert "HAR" in block
    assert "ARFIMA" in block


def test_render_hub_index_replaces_block_in_place(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "long",
        n_variables=2,
        best_per_variable={"G::A": "msm", "G::B": "har"},
        beats_per_variable={"G::A": True, "G::B": True},
    )

    home_page = tmp_path / "index.md"
    original_body = (
        "# Title\n\nSome intro text.\n\n"
        f"{AUTO_VERDICT_BEGIN_MARKER}\n\nstale content\n\n{AUTO_VERDICT_END_MARKER}\n\n"
        "## Other section\n\nTail content.\n"
    )
    home_page.write_text(original_body, encoding="utf-8")

    summary = consolidate_benchmark_sidecars(
        tmp_path, as_of="2026-05", panel_codes=("long",)
    )
    render_hub_index(home_page, summary)

    rewritten = home_page.read_text(encoding="utf-8")
    assert AUTO_VERDICT_BEGIN_MARKER in rewritten
    assert AUTO_VERDICT_END_MARKER in rewritten
    assert "stale content" not in rewritten
    assert "## Other section" in rewritten
    assert "Tail content." in rewritten
    assert "# Title" in rewritten
    assert "PASS" in rewritten


def test_render_hub_index_raises_when_markers_absent(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "long",
        n_variables=2,
        best_per_variable={"G::A": "msm", "G::B": "har"},
        beats_per_variable={"G::A": True, "G::B": True},
    )
    home_page = tmp_path / "index.md"
    home_page.write_text("# No markers here.\n", encoding="utf-8")

    summary = consolidate_benchmark_sidecars(
        tmp_path, as_of="2026-05", panel_codes=("long",)
    )
    with pytest.raises(ValueError, match=AUTO_VERDICT_BEGIN_MARKER):
        render_hub_index(home_page, summary)


def test_render_hub_index_from_reports_end_to_end(tmp_path: Path) -> None:
    _write_synthetic_sidecar(
        tmp_path,
        "2026-05",
        "wb",
        n_variables=3,
        best_per_variable={"W::A": "msm", "W::B": "har", "W::C": ""},
        beats_per_variable={"W::A": True, "W::B": True, "W::C": False},
    )
    home_page = tmp_path / "home.md"
    home_page.write_text(
        f"intro\n\n{AUTO_VERDICT_BEGIN_MARKER}\nold\n{AUTO_VERDICT_END_MARKER}\n",
        encoding="utf-8",
    )
    summary = render_hub_index_from_reports(
        reports_dir=tmp_path,
        index_path=home_page,
        as_of="2026-05",
        panel_codes=("wb",),
    )
    rendered = home_page.read_text(encoding="utf-8")

    assert summary.total_variables == 3
    assert summary.total_passing == 2
    assert "PASS" in rendered or "FAIL" in rendered
    assert "old" not in rendered
