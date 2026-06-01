# API publique `ecowave.forecasting`

> *Référence des fonctions et dataclasses exportées. Chaque entrée
> pointe vers le code source sur GitHub.*

## Vue d'ensemble du package

```
ecowave/forecasting/
├── types.py                   # ProbabilisticForecast (pivot)
├── proper_scoring.py          # CRPS empirique, coverage, MZ
├── baselines.py               # RW, AR(1), ARMA(1,1)
├── har.py                     # HAR Corsi 2009
├── fractional.py              # Hosking + GPH primitives
├── arfima_rs.py               # ARFIMA(0, d, 0) + Markov RS
├── msm.py                     # MSM Calvet-Fisher 2002
├── benchmark.py               # Pipeline rolling-origin
├── reporting.py               # Sidecar JSON + page markdown
└── consolidated_report.py     # Cross-panel aggregation
```

## `types.py` — Le format pivot

### `ProbabilisticForecast` (dataclass frozen)

Toutes les fonctions `*_forecast` retournent un objet de ce type.

| Attribut | Type | Description |
|---|---|---|
| `horizons` | `tuple[int, ...]` | Horizons en cadence steps |
| `samples` | `np.ndarray` shape `(n_samples, H)` | Monte Carlo paths sur le niveau |
| `model_name` | `str` | Identifiant court (`"rw"`, `"har"`, ...) |
| `metadata` | `dict` | Paramètres estimés, flags de fit |

Méthodes :

- `mean` → `np.ndarray (H,)` : point forecast par horizon
- `quantile(q)` → quantile(s) par horizon
- `at(h)` → `np.ndarray (n_samples,)` : slice pour 1 horizon
- `n_samples` → int

Source : [`types.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/types.py).

## `proper_scoring.py` — Scoring rules

### Fonctions principales

```python
empirical_crps(samples: np.ndarray, observation: float) -> float
```

CRPS empirique via identité Gneiting-Raftery 2007 :
`CRPS = E|X − y| − ½ E|X − X'|`. Implémentation O(n log n) via la
formule rank-based pour la Gini-mean-difference.

```python
coverage_indicator(samples, observation, level=0.95) -> int  # 0 ou 1
tail_coverage_indicator(samples, observation, alpha=0.05, tail="left"|"right") -> int
```

```python
score_forecast(samples, observation) -> ForecastScores
```

Bundle `ForecastScores` : `rmse`, `mae`, `crps`, `coverage_95`,
`tail_coverage_left_5pct`, `tail_coverage_right_5pct`, `bias`.

```python
mincer_zarnowitz(predictions, realisations) -> MincerZarnowitzResult
```

F-test joint `(α, β) = (0, 1)`. Retourne `alpha`, `beta`,
`f_statistic`, `p_value`, `n_observations`.

Source : [`proper_scoring.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/proper_scoring.py).

## `baselines.py` — RW, AR(1), ARMA(1, 1)

```python
random_walk_forecast(history, horizons, n_samples=1000, seed=0) -> ProbabilisticForecast
ar1_forecast(history, horizons, n_samples=1000, seed=0) -> ProbabilisticForecast
arma11_forecast(history, horizons, n_samples=1000, seed=0) -> ProbabilisticForecast
```

Métadonnées exposées :

- RW : `sigma_increment`, `last_level`
- AR(1) : `intercept`, `phi`, `sigma_residual`
- ARMA(1,1) : `converged` (booléen)

Fallbacks : AR(1) explosive (`|φ| ≥ 0.999`) → RW. ARMA(1,1) non
convergent → AR(1).

Source : [`baselines.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/baselines.py).

## `har.py` — HAR Corsi 2009

### `HARLagConfig` (dataclass frozen)

```python
HARLagConfig(short=1, medium=3, long=12)
```

Validation : `0 < short < medium < long`. Defaults monthly. Pour
quarterly utiliser `HARLagConfig(1, 2, 4)`.

### `har_forecast`

```python
har_forecast(
    history, horizons,
    n_samples=1000, seed=0,
    lag_config: HARLagConfig | None = None,
) -> ProbabilisticForecast
```

Métadonnées exposées : `intercept`, `beta_short`, `beta_medium`,
`beta_long`, `sigma_residual`, `lag_config`.

Source : [`har.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/har.py).

## `fractional.py` — Hosking + GPH

Primitives réutilisables si vous voulez construire votre propre
ARFIMA variant.

```python
hosking_coefficients(d: float, length: int) -> np.ndarray
```

Récursion `ψ_0 = 1`, `ψ_k = ψ_{k-1} · (k - 1 - d) / k`. Validation
`-0.499 ≤ d ≤ 0.499`.

```python
fractional_difference(series, d, truncate=None) -> np.ndarray
fractional_integrate(series, d, truncate=None) -> np.ndarray
```

Inverse l'un de l'autre (signe de `d` flippé).

```python
gph_estimate_d(series, bandwidth_exponent=0.5) -> float
```

Geweke-Porter-Hudak log-periodogram regression. Clipping automatique
à `[-0.499, 0.499]`.

Source : [`fractional.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/fractional.py).

## `arfima_rs.py` — ARFIMA + Markov regime-switching

### `ARFIMARSConfig` (dataclass frozen)

```python
ARFIMARSConfig(
    n_regimes=2,
    bandwidth_exponent=0.5,
    hosking_truncate=None,
    switching_variance=True,
)
```

### `arfima_rs_forecast`

```python
arfima_rs_forecast(
    history, horizons,
    n_samples=1000, seed=0,
    config: ARFIMARSConfig | None = None,
) -> ProbabilisticForecast
```

Pipeline interne : GPH → diff → MarkovRegression → simulation Markov +
tirage Gaussien régime-conditionnel → reconstruction des niveaux par
récursion inverse Hosking.

Métadonnées exposées : `d_estimated`, `regime_fit_ok`,
`n_regimes_used`, `regime_means`, `regime_sigmas`,
`transition_matrix`, `bandwidth_exponent`.

Source : [`arfima_rs.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/arfima_rs.py).

## `msm.py` — MSM Calvet-Fisher 2002

### `MSMConfig` + `MSMParameters` (dataclasses frozen)

```python
MSMConfig(
    n_components=4,           # K, supporté ∈ [2, 6]
    use_log_returns=True,     # si série > 0
    fallback_on_failure=True,
)

MSMParameters(m_0, sigma_bar, b, gamma_1)  # is_valid() pour bornes
```

### `msm_forecast`

```python
msm_forecast(
    history, horizons,
    n_samples=1000, seed=0,
    config: MSMConfig | None = None,
) -> ProbabilisticForecast
```

Pipeline interne : extraction returns → ML par filtre forward Hamilton
sur `2^K` états (L-BFGS-B avec box constraints + grille starting points)
→ tirage état initial depuis distribution filtrée terminale →
simulation composantes indépendantes → reconstruction niveau.

Métadonnées exposées : `msm_fit_ok`, `n_components`, `return_mode`
(`"log"` ou `"diff"`), `m_0`, `sigma_bar`, `b`, `gamma_1`.

Source : [`msm.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/msm.py).

## `benchmark.py` — Pipeline

### `BenchmarkConfig` (dataclass frozen)

```python
BenchmarkConfig(
    horizons=(1, 3, 6, 12),
    models=("rw", "ar1", "arma11", "har", "arfima_rs", "msm"),
    n_origins=8,
    n_samples=200,
    test_fraction=0.25,
    seed=0,
    har_lag_config=HARLagConfig(),
    msm_components=4,
    min_train_length=64,
)
```

### Constantes utiles

```python
CLUSTER_MODEL_NAMES = ("har", "arfima_rs", "msm")
BASELINE_MODEL_NAMES = ("rw", "ar1", "arma11")
ALL_MODEL_NAMES = BASELINE_MODEL_NAMES + CLUSTER_MODEL_NAMES
```

### `run_benchmark`

```python
run_benchmark(
    panels: Mapping[str, Mapping[str, np.ndarray]],
    config: BenchmarkConfig | None = None,
) -> BenchmarkResults
```

Signature des `panels` : `{group_code: {variable_code: 1D level series}}`.
Variables trop courtes (< `min_train_length + max_horizon`) sont
silencieusement skippées.

### `evaluate_acceptance_criterion`

```python
evaluate_acceptance_criterion(
    results: BenchmarkResults,
    decision_horizon=12,
    beat_threshold=0.5,
    baseline_model="rw",
) -> AcceptanceVerdict
```

Pour chaque variable, retient le best cluster model et son CRPS. Le
verdict passe si `pass_rate ≥ beat_threshold`.

### Dataclasses output

- `ScoreRow` — 1 par `(group, variable, model, horizon, origin)`
- `BenchmarkResults` — `config`, `score_rows`, `failed_evaluations`,
  méthode `per_cell_crps()`
- `AcceptanceVerdict` — `decision_horizon`, `pass_rate`, `passes`,
  `best_cluster_model_per_variable`,
  `cluster_beats_baseline_per_variable`

Source : [`benchmark.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/benchmark.py).

## `reporting.py` — JSON + Markdown

```python
aggregate_per_cell(results: BenchmarkResults) -> list[dict]
write_benchmark_sidecar(results, verdict, out_path, as_of, horizon_data_code)
render_benchmark_page(results, verdict, out_path, as_of, horizon_data_code)
```

Schéma sidecar : `schema_version=1`, voir documenté dans
[consolidated_report.py](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/consolidated_report.py).

Source : [`reporting.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/reporting.py).

## `consolidated_report.py` — Cross-panel

### `PanelSummary` + `ConsolidatedSummary`

Dataclasses frozen, propriétés calculées :

- `ConsolidatedSummary.total_variables`
- `ConsolidatedSummary.total_passing`
- `ConsolidatedSummary.aggregate_pass_rate`
- `ConsolidatedSummary.passes`
- `ConsolidatedSummary.leaderboard()` → `list[tuple[str, int]]` trié

### Fonctions

```python
consolidate_benchmark_sidecars(
    reports_dir: Path,
    as_of: str,
    panel_codes: Iterable[str] = ("wb", "q", "long", "boe", "bis", "sh"),
    beat_threshold: float = 0.5,
) -> ConsolidatedSummary
```

Schema guard : refuse sidecars `schema_version != 1`.
Consistency guard : refuse decision horizons hétérogènes.
Gracious : signale missing panels sans fail.

```python
render_consolidated_page(summary, out_path) -> None
```

Markdown avec verdict global, table par panel, leaderboard, lecture
qualitative, section reproduction.

Source : [`consolidated_report.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/consolidated_report.py).

## Exemple end-to-end Python

```python
from pathlib import Path
import numpy as np

from ecowave.forecasting.benchmark import (
    BenchmarkConfig,
    evaluate_acceptance_criterion,
    run_benchmark,
)
from ecowave.forecasting.reporting import (
    render_benchmark_page,
    write_benchmark_sidecar,
)

panels = {
    "GROUP_A": {
        "VAR1": np.cumsum(np.random.default_rng(0).normal(size=300)),
        "VAR2": np.cumsum(np.random.default_rng(1).normal(size=300)),
    }
}

config = BenchmarkConfig(
    horizons=(1, 3, 12),
    models=("rw", "har", "msm"),
    n_origins=4,
    n_samples=100,
    seed=42,
)

results = run_benchmark(panels, config=config)
verdict = evaluate_acceptance_criterion(results, decision_horizon=12)

write_benchmark_sidecar(
    results, verdict,
    Path("/tmp/sidecar.json"),
    as_of="2026-05",
    horizon_data_code="custom",
)
render_benchmark_page(
    results, verdict,
    Path("/tmp/report.md"),
    as_of="2026-05",
    horizon_data_code="custom",
)
```

## Tests

La suite couvre 225 tests dont 63 nouveaux sur le module forecasting :

```
tests/test_forecasting_types.py            (6 tests)
tests/test_forecasting_proper_scoring.py   (8 tests)
tests/test_forecasting_baselines.py        (7 tests)
tests/test_forecasting_har.py              (5 tests)
tests/test_forecasting_fractional.py       (9 tests)
tests/test_forecasting_arfima_rs.py        (8 tests)
tests/test_forecasting_msm.py              (11 tests)
tests/test_forecasting_benchmark.py        (11 tests)
tests/test_forecasting_consolidated.py     (6 tests)
```

Lancer en Docker :

```bash
docker compose run --rm --entrypoint pytest ecowave tests/test_forecasting_*.py -v
```
