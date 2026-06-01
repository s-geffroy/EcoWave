# Forecast benchmark — verdict consolidé

> **Run.** ``as_of = 2026-05``. Decision horizon ``h = 12``. Threshold ``50 %``.

Tested against the random-walk baseline across the full panel set (World Bank, quarterly contemporain, long historique, Bank of England Millennium, BIS, sectoral history). The acceptance criterion of [Roadmap item #20](methodology/feuille_de_route.md#item-20-modeling-benchmark) is met when at least ``50 %`` of variables tested have *some* cluster model beating random walk on out-of-sample CRPS at ``h = 12``.

## Verdict global

✅ **PASS** — aggregate pass rate 78% on 53 / 68 variables across 6 panels.

## Verdicts par panel

| panel | période | pass rate | n vars | verdict | best cluster |
|---|---|---|---|---|---|
| `wb` | World Bank (1960-2024, annuel) | 60% | 10 | ✅ PASS | msm (4) · har (2) |
| `q` | Quarterly contemporain (1995-2024) | 79% | 14 | ✅ PASS | arfima_rs (7) · har (4) |
| `long` | Maddison + JST (1870-2024, annuel) | 88% | 16 | ✅ PASS | msm (8) · har (4) · arfima_rs (2) |
| `boe` | Bank of England Millennium (1700-2016) | 88% | 8 | ✅ PASS | har (4) · msm (3) |
| `bis` | BIS macroprudentiel (1970-2024, trim.) | 83% | 12 | ✅ PASS | msm (6) · arfima_rs (3) · har (1) |
| `sh` | Sectoral history (FRED+OWID+BEIS) | 62% | 8 | ✅ PASS | arfima_rs (2) · msm (2) · har (1) |

## Leaderboard des modèles du cluster

Nombre total de variables où chaque modèle du cluster est *le* meilleur compétiteur (et bat la baseline random-walk) à travers tous les panels.

| modèle | total wins | part |
|---|---|---|
| `msm` | 23 | 43% |
| `har` | 16 | 30% |
| `arfima_rs` | 14 | 26% |

## Lecture qualitative

- **MSM domine sur les panels longs** (Bank of England, long historique, BIS quarterly). La cascade multifractale à 4 composantes a besoin d'historique pour identifier les fréquences lentes — elle paye sur les séries longues mais demande prudence sur les panels courts.
- **HAR domine sur le quarterly contemporain.** La cascade par agrégation (daily/weekly/monthly → 1/2/4 lags) suffit à courte cadence ; pas besoin de la machinerie multifractale ni du switching markovien.
- **ARFIMA+RS a une niche en crédit et en macro lente.** La paire (long memory exact, regime-switching à 2 états) reste compétitive sur LH_CREDIT et plusieurs variables BIS.
- **Aucune baseline (RW, AR(1), ARMA(1,1)) ne gagne** quand un modèle du cluster est compétent — ce qui valide *qualitativement* la thèse cluster C+B+D+I+S.

## Reproduction

Reproduire ce verdict :

```bash
for panel in wb q long boe bis sh; do
  args="--horizon-data ${panel} --horizons 1,3,6,12"
  args="${args} --n-origins 6 --n-samples 200 --variables-limit 8"
  if [ "${panel}" = "wb" ] || [ "${panel}" = "sh" ]; then
    # Annual panels with < 76 obs need a lower train floor
    args="${args} --min-train-length 40"
  fi
  docker compose run --rm ecowave forecast-benchmark ${args}
done
docker compose run --rm ecowave forecast-benchmark-consolidate
```

Per-panel sidecars : ``reports/forecast_benchmark_2026_05_{panel}.json``. Page générée à 2026-06-01T16:56:33+00:00 par `ecowave forecast-benchmark-consolidate`.
