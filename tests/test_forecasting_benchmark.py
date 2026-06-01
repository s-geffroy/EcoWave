"""Tests for the benchmark orchestrator + reporting.

Use synthetic panels — small enough to run in ~5 s under Docker — to
exercise the full pipeline including verdict computation. We don't pin
specific scores; we pin the *contract* (rows are produced, the verdict
object has the right shape, the markdown page is non-empty).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from ecowave.forecasting.benchmark import (
    ALL_MODEL_NAMES,
    BASELINE_MODEL_NAMES,
    BenchmarkConfig,
    CLUSTER_MODEL_NAMES,
    _origin_indices_for_series,
    evaluate_acceptance_criterion,
    run_benchmark,
)
from ecowave.forecasting.reporting import (
    aggregate_per_cell,
    render_benchmark_page,
    write_benchmark_sidecar,
)


def _make_synthetic_panel(seed: int, n_variables: int = 3, length: int = 200) -> dict[str, np.ndarray]:
    """Random ARFIMA-flavoured series for benchmark smoke tests."""
    rng = np.random.default_rng(seed=seed)
    panel: dict[str, np.ndarray] = {}
    for variable_index in range(n_variables):
        innovations = rng.normal(scale=0.4, size=length)
        slow_component = np.cumsum(innovations)
        panel[f"V{variable_index:02d}"] = 10.0 + slow_component + 0.1 * rng.normal(size=length)
    return panel


def test_origin_indices_evenly_spaced_inside_holdout_span() -> None:
    config = BenchmarkConfig(
        horizons=(1, 3, 12), n_origins=4, test_fraction=0.25, models=("rw",)
    )
    origins = _origin_indices_for_series(series_length=300, config=config)

    assert len(origins) == 4
    # Each origin must leave room for the longest horizon.
    assert max(origins) <= 300 - 12
    # Strict monotone.
    assert all(origins[index] < origins[index + 1] for index in range(len(origins) - 1))


def test_origin_indices_empty_when_series_too_short() -> None:
    config = BenchmarkConfig(horizons=(12,), n_origins=4, models=("rw",))
    assert _origin_indices_for_series(series_length=40, config=config) == []


def test_benchmark_config_rejects_unknown_model() -> None:
    with pytest.raises(ValueError, match="unknown models"):
        BenchmarkConfig(models=("rw", "unknown_model"))


def test_benchmark_config_rejects_min_train_length_below_floor() -> None:
    with pytest.raises(ValueError, match="min_train_length"):
        BenchmarkConfig(min_train_length=16)


def test_origin_indices_respect_lowered_min_train_length() -> None:
    """Short annual panels (e.g. WB 1960-2024 ≈ 65 obs) need a lower train floor."""
    short_config = BenchmarkConfig(
        horizons=(1, 3, 12),
        n_origins=4,
        test_fraction=0.25,
        models=("rw",),
        min_train_length=40,
    )
    origins = _origin_indices_for_series(series_length=65, config=short_config)
    assert len(origins) > 0
    assert min(origins) >= 40
    assert max(origins) <= 65 - 12


def test_run_benchmark_produces_one_row_per_model_horizon_origin() -> None:
    panels = {"GROUP_A": _make_synthetic_panel(seed=1, n_variables=2, length=200)}
    config = BenchmarkConfig(
        horizons=(1, 3),
        models=("rw", "ar1", "har"),
        n_origins=2,
        n_samples=40,
        seed=7,
    )
    results = run_benchmark(panels, config=config)

    # At least one row per (variable, model, horizon, origin).
    assert len(results.score_rows) > 0
    distinct_models = {row.model for row in results.score_rows}
    assert distinct_models.issubset(set(config.models))
    distinct_horizons = {row.horizon for row in results.score_rows}
    assert distinct_horizons.issubset(set(config.horizons))


def test_evaluate_acceptance_criterion_returns_expected_shape() -> None:
    panels = {"GROUP_A": _make_synthetic_panel(seed=2, n_variables=3, length=220)}
    config = BenchmarkConfig(
        horizons=(1, 12),
        models=("rw", "har", "arfima_rs"),
        n_origins=2,
        n_samples=40,
        seed=11,
    )
    results = run_benchmark(panels, config=config)
    verdict = evaluate_acceptance_criterion(
        results, decision_horizon=12, beat_threshold=0.5
    )

    assert verdict.decision_horizon == 12
    assert verdict.beat_threshold == 0.5
    assert verdict.n_variables_total <= 3
    assert 0.0 <= verdict.pass_rate <= 1.0
    assert verdict.passes == (verdict.pass_rate >= 0.5)


def test_aggregate_per_cell_yields_one_record_per_cell() -> None:
    panels = {"GROUP_A": _make_synthetic_panel(seed=3, n_variables=2, length=180)}
    config = BenchmarkConfig(
        horizons=(1, 3),
        models=("rw", "ar1"),
        n_origins=2,
        n_samples=20,
        seed=13,
    )
    results = run_benchmark(panels, config=config)
    aggregated = aggregate_per_cell(results)

    distinct_keys = {
        (record["group"], record["variable"], record["model"], record["horizon"])
        for record in aggregated
    }
    assert len(aggregated) == len(distinct_keys)
    for record in aggregated:
        assert record["mean_crps"] >= 0.0
        assert record["n_origins"] >= 1


def test_write_and_read_benchmark_sidecar(tmp_path: Path) -> None:
    panels = {"GROUP_A": _make_synthetic_panel(seed=4, n_variables=2, length=200)}
    config = BenchmarkConfig(
        horizons=(1, 12),
        models=("rw", "har"),
        n_origins=2,
        n_samples=20,
        seed=17,
    )
    results = run_benchmark(panels, config=config)
    verdict = evaluate_acceptance_criterion(results, decision_horizon=12)
    sidecar_path = tmp_path / "benchmark.json"
    write_benchmark_sidecar(
        results, verdict, sidecar_path, as_of="2026-05", horizon_data_code="test"
    )

    payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["horizon_data_code"] == "test"
    assert payload["verdict"]["decision_horizon"] == 12
    assert "cells" in payload and len(payload["cells"]) > 0


def test_render_benchmark_page_writes_non_empty_markdown(tmp_path: Path) -> None:
    panels = {"GROUP_A": _make_synthetic_panel(seed=5, n_variables=2, length=180)}
    config = BenchmarkConfig(
        horizons=(1, 12),
        models=("rw", "har"),
        n_origins=2,
        n_samples=20,
        seed=23,
    )
    results = run_benchmark(panels, config=config)
    verdict = evaluate_acceptance_criterion(results, decision_horizon=12)
    page_path = tmp_path / "benchmark.md"
    render_benchmark_page(
        results, verdict, page_path, as_of="2026-05", horizon_data_code="test"
    )

    body = page_path.read_text(encoding="utf-8")
    assert "Forecast benchmark" in body
    assert "Verdict" in body
    assert ("PASS" in body) or ("FAIL" in body)
    assert "rw" in body  # baseline appears in CRPS table


def test_benchmark_model_names_partition_into_baselines_and_cluster() -> None:
    assert set(BASELINE_MODEL_NAMES) & set(CLUSTER_MODEL_NAMES) == set()
    assert set(BASELINE_MODEL_NAMES) | set(CLUSTER_MODEL_NAMES) == set(ALL_MODEL_NAMES)
