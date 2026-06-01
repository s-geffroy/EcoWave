"""Forecast benchmark orchestrator — Roadmap #20 PR D.

Mission. Run all six candidate models — three baselines (random walk,
AR(1), ARMA(1, 1)) and three cluster contenders (HAR, ARFIMA+RS, MSM) —
on the same panels and horizons. Score every forecast with the proper-
scoring-rule stack (CRPS, MAE, RMSE, coverage, tail coverage). Decide
whether the acceptance criterion of item #20 holds:

> "At least one cluster model must beat random walk on out-of-sample
> CRPS at the 12-month horizon on ≥ 50 % of variables tested."

Strategy. For each variable in each panel, we set aside the tail of the
series as a holdout. We then place ``n_origins`` evenly-spaced forecast
origins inside that holdout, fit every model on the history up to each
origin, and score the resulting probabilistic forecasts against the
realised values. The origin-wise scores are then averaged per
(model, horizon, variable) — this is the standard rolling-origin
out-of-sample protocol used by Bhardwaj-Swanson 2006 and Calvet-Fisher
2004.

The module exposes pure functions that take in-memory panels (dicts of
1-D numpy arrays). The CLI wiring (:mod:`ecowave.cli`) is responsible
for loading from SQLite, slicing per group, and writing the JSON sidecar
+ markdown report.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Mapping

import numpy as np

from ecowave.forecasting.arfima_rs import arfima_rs_forecast
from ecowave.forecasting.baselines import (
    ar1_forecast,
    arma11_forecast,
    random_walk_forecast,
)
from ecowave.forecasting.har import HARLagConfig, har_forecast
from ecowave.forecasting.msm import MSMConfig, msm_forecast
from ecowave.forecasting.proper_scoring import score_forecast


CLUSTER_MODEL_NAMES = ("har", "arfima_rs", "msm")
BASELINE_MODEL_NAMES = ("rw", "ar1", "arma11")
ALL_MODEL_NAMES = BASELINE_MODEL_NAMES + CLUSTER_MODEL_NAMES
DEFAULT_HORIZONS = (1, 3, 6, 12)
DEFAULT_N_ORIGINS = 8
DEFAULT_N_SAMPLES = 200
DEFAULT_TEST_FRACTION = 0.25
# Default minimum in-sample length for benchmark fits. Calibrated for
# Calvet-Fisher MSM (requires ≥ 50 returns to identify the cascade
# parameters) and HAR (one ``long`` lag of 12 + 4-row OLS buffer ≈ 32).
# The :class:`BenchmarkConfig.min_train_length` field exposes this so
# short annual panels (WB 1960-2024, SH 1960-2024) can be benchmarked
# with a lower bound at the cost of less stable MSM fits.
DEFAULT_MIN_TRAIN_LENGTH = 64


@dataclass(frozen=True)
class BenchmarkConfig:
    """Configuration for a benchmark run."""

    horizons: tuple[int, ...] = DEFAULT_HORIZONS
    models: tuple[str, ...] = ALL_MODEL_NAMES
    n_origins: int = DEFAULT_N_ORIGINS
    n_samples: int = DEFAULT_N_SAMPLES
    test_fraction: float = DEFAULT_TEST_FRACTION
    seed: int = 0
    har_lag_config: HARLagConfig = field(default_factory=HARLagConfig)
    msm_components: int = 4
    min_train_length: int = DEFAULT_MIN_TRAIN_LENGTH

    def __post_init__(self) -> None:
        if not self.horizons or any(horizon <= 0 for horizon in self.horizons):
            raise ValueError(f"horizons must be positive; got {self.horizons}")
        invalid_models = set(self.models) - set(ALL_MODEL_NAMES)
        if invalid_models:
            raise ValueError(
                f"unknown models {sorted(invalid_models)}; "
                f"valid: {ALL_MODEL_NAMES}"
            )
        if not 0.05 <= self.test_fraction <= 0.5:
            raise ValueError(
                f"test_fraction must be in [0.05, 0.5]; got {self.test_fraction}"
            )
        if self.n_origins < 1:
            raise ValueError(f"n_origins must be ≥ 1; got {self.n_origins}")
        if self.min_train_length < 32:
            raise ValueError(
                f"min_train_length must be ≥ 32 (HAR identification floor); "
                f"got {self.min_train_length}"
            )


@dataclass(frozen=True)
class ScoreRow:
    """One scored forecast at one origin × model × horizon."""

    group: str
    variable: str
    model: str
    horizon: int
    origin_index: int
    observation: float
    crps: float
    rmse: float
    mae: float
    coverage_95: float
    tail_left_5pct: float
    tail_right_5pct: float
    bias: float


@dataclass(frozen=True)
class BenchmarkResults:
    """Aggregate output of a benchmark run."""

    config: BenchmarkConfig
    score_rows: tuple[ScoreRow, ...]
    failed_evaluations: tuple[dict, ...]

    def per_cell_crps(self) -> dict[tuple[str, str, str, int], float]:
        """Mean CRPS per (group, variable, model, horizon)."""
        accumulator: dict[tuple[str, str, str, int], list[float]] = {}
        for row in self.score_rows:
            key = (row.group, row.variable, row.model, row.horizon)
            accumulator.setdefault(key, []).append(row.crps)
        return {key: float(np.mean(values)) for key, values in accumulator.items()}


@dataclass(frozen=True)
class AcceptanceVerdict:
    """Pass/fail decision for the roadmap #20 acceptance criterion."""

    decision_horizon: int
    beat_threshold: float
    n_variables_total: int
    n_variables_with_baseline: int
    best_cluster_model_per_variable: dict[str, str]
    cluster_beats_baseline_per_variable: dict[str, bool]
    pass_rate: float
    passes: bool


def _build_model_callables(config: BenchmarkConfig) -> dict[str, Callable]:
    """Return name → ``(history, horizons, n_samples, seed) -> ProbabilisticForecast``."""

    def call_rw(history, horizons, n_samples, seed):
        return random_walk_forecast(history, horizons, n_samples=n_samples, seed=seed)

    def call_ar1(history, horizons, n_samples, seed):
        return ar1_forecast(history, horizons, n_samples=n_samples, seed=seed)

    def call_arma11(history, horizons, n_samples, seed):
        return arma11_forecast(history, horizons, n_samples=n_samples, seed=seed)

    def call_har(history, horizons, n_samples, seed):
        return har_forecast(
            history,
            horizons,
            n_samples=n_samples,
            seed=seed,
            lag_config=config.har_lag_config,
        )

    def call_arfima_rs(history, horizons, n_samples, seed):
        return arfima_rs_forecast(history, horizons, n_samples=n_samples, seed=seed)

    def call_msm(history, horizons, n_samples, seed):
        return msm_forecast(
            history,
            horizons,
            n_samples=n_samples,
            seed=seed,
            config=MSMConfig(n_components=config.msm_components),
        )

    registry = {
        "rw": call_rw,
        "ar1": call_ar1,
        "arma11": call_arma11,
        "har": call_har,
        "arfima_rs": call_arfima_rs,
        "msm": call_msm,
    }
    return {name: registry[name] for name in config.models}


def _origin_indices_for_series(
    series_length: int, config: BenchmarkConfig
) -> list[int]:
    """Return the list of holdout origins for a series of given length.

    The holdout span is the last ``test_fraction`` of the series. We
    place ``n_origins`` origins evenly-spaced inside that span, starting
    no earlier than ``config.min_train_length`` observations into the
    past.
    """
    max_horizon = max(config.horizons)
    test_span_length = int(math.ceil(series_length * config.test_fraction))
    test_start = max(config.min_train_length, series_length - test_span_length)
    last_valid_origin = series_length - max_horizon
    if last_valid_origin <= test_start:
        return []
    if config.n_origins == 1:
        return [last_valid_origin]
    step = max(1, (last_valid_origin - test_start) // (config.n_origins - 1))
    origins = list(range(test_start, last_valid_origin + 1, step))[: config.n_origins]
    return origins


def _score_one_origin(
    series: np.ndarray,
    origin_index: int,
    config: BenchmarkConfig,
    model_callables: dict[str, Callable],
    group: str,
    variable: str,
) -> tuple[list[ScoreRow], list[dict]]:
    """Score every model at one origin on one variable's series."""
    history = series[:origin_index]
    scored_rows: list[ScoreRow] = []
    failures: list[dict] = []
    for model_name, model_call in model_callables.items():
        try:
            forecast = model_call(
                history,
                tuple(config.horizons),
                config.n_samples,
                config.seed + origin_index,
            )
        except Exception as exc:  # noqa: BLE001
            failures.append(
                {
                    "group": group,
                    "variable": variable,
                    "model": model_name,
                    "origin_index": origin_index,
                    "error": str(exc),
                }
            )
            continue
        for horizon_index, horizon in enumerate(config.horizons):
            realisation_index = origin_index + horizon - 1
            if realisation_index >= series.size:
                continue
            observation = float(series[realisation_index])
            if not np.isfinite(observation):
                continue
            samples = forecast.samples[:, horizon_index]
            scores = score_forecast(samples, observation)
            scored_rows.append(
                ScoreRow(
                    group=group,
                    variable=variable,
                    model=model_name,
                    horizon=int(horizon),
                    origin_index=int(origin_index),
                    observation=observation,
                    crps=scores.crps,
                    rmse=scores.rmse,
                    mae=scores.mae,
                    coverage_95=scores.coverage_95,
                    tail_left_5pct=scores.tail_coverage_left_5pct,
                    tail_right_5pct=scores.tail_coverage_right_5pct,
                    bias=scores.bias,
                )
            )
    return scored_rows, failures


def run_benchmark(
    panels: Mapping[str, Mapping[str, np.ndarray]],
    config: BenchmarkConfig | None = None,
) -> BenchmarkResults:
    """Run the full forecast benchmark on the supplied panels.

    Parameters
    ----------
    panels:
        Mapping ``group_code → variable_code → 1-D level series``. The
        series are assumed to be regularly-sampled and pre-cleaned (no
        NaNs in the interior). Variables with fewer than
        ``MIN_TRAIN_LENGTH + max(horizons)`` finite observations are
        silently skipped.
    config:
        :class:`BenchmarkConfig`. Defaults to the full six-model panel
        on horizons ``(1, 3, 6, 12)``.
    """
    config = config or BenchmarkConfig()
    model_callables = _build_model_callables(config)
    score_rows: list[ScoreRow] = []
    failed: list[dict] = []
    max_horizon = max(config.horizons)
    for group_code, variables in panels.items():
        for variable_code, series in variables.items():
            series_arr = np.asarray(series, dtype=float).ravel()
            finite_mask = np.isfinite(series_arr)
            series_arr = series_arr[finite_mask]
            if series_arr.size < config.min_train_length + max_horizon:
                continue
            origins = _origin_indices_for_series(series_arr.size, config)
            for origin_index in origins:
                rows, failures = _score_one_origin(
                    series_arr,
                    origin_index,
                    config,
                    model_callables,
                    group_code,
                    variable_code,
                )
                score_rows.extend(rows)
                failed.extend(failures)
    return BenchmarkResults(
        config=config,
        score_rows=tuple(score_rows),
        failed_evaluations=tuple(failed),
    )


def evaluate_acceptance_criterion(
    results: BenchmarkResults,
    decision_horizon: int = 12,
    beat_threshold: float = 0.5,
    baseline_model: str = "rw",
) -> AcceptanceVerdict:
    """Decide whether the roadmap #20 acceptance criterion holds.

    For each (group, variable), compare the mean CRPS at
    ``decision_horizon`` of each cluster model against the baseline. A
    variable "passes" if at least one cluster model has lower mean
    CRPS than the baseline. The verdict is ``passes`` iff the pass rate
    across variables is ≥ ``beat_threshold``.
    """
    per_cell = results.per_cell_crps()
    variables_observed: set[tuple[str, str]] = set()
    cluster_crps_by_variable: dict[tuple[str, str], dict[str, float]] = {}
    baseline_crps_by_variable: dict[tuple[str, str], float] = {}

    for (group_code, variable_code, model, horizon), crps in per_cell.items():
        if horizon != decision_horizon:
            continue
        key = (group_code, variable_code)
        variables_observed.add(key)
        if model == baseline_model:
            baseline_crps_by_variable[key] = crps
        elif model in CLUSTER_MODEL_NAMES:
            cluster_crps_by_variable.setdefault(key, {})[model] = crps

    best_per_variable: dict[str, str] = {}
    beats_per_variable: dict[str, bool] = {}
    variables_with_baseline = 0
    n_passing = 0
    for key in variables_observed:
        label = f"{key[0]}::{key[1]}"
        baseline_crps = baseline_crps_by_variable.get(key)
        cluster_scores = cluster_crps_by_variable.get(key, {})
        if baseline_crps is None or not cluster_scores:
            beats_per_variable[label] = False
            best_per_variable[label] = ""
            continue
        variables_with_baseline += 1
        best_model = min(cluster_scores, key=cluster_scores.get)
        best_score = cluster_scores[best_model]
        best_per_variable[label] = best_model
        beats = best_score < baseline_crps
        beats_per_variable[label] = beats
        if beats:
            n_passing += 1

    pass_rate = (
        n_passing / variables_with_baseline if variables_with_baseline > 0 else 0.0
    )
    return AcceptanceVerdict(
        decision_horizon=decision_horizon,
        beat_threshold=beat_threshold,
        n_variables_total=len(variables_observed),
        n_variables_with_baseline=variables_with_baseline,
        best_cluster_model_per_variable=best_per_variable,
        cluster_beats_baseline_per_variable=beats_per_variable,
        pass_rate=pass_rate,
        passes=pass_rate >= beat_threshold,
    )
