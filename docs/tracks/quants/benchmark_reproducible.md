# Benchmark reproductible

> *Pas-à-pas pour atteindre le verdict PASS 78 % sur votre machine.
> Aucune installation locale : tout passe par Docker.*

## Pré-requis

- **Docker** ≥ 24 et `docker compose` v2.
- ~4 Go de disque pour l'image + données intermédiaires.
- ~30 minutes pour un run complet n_origins=12 (les MSM dominent
  le temps de calcul).

Aucune dépendance Python locale n'est nécessaire — c'est une exigence
explicite du projet (`CLAUDE.md` : *"never install something in
local"*).

## Étape 1 — Cloner et builder

```bash
git clone https://github.com/s-geffroy/EcoWave.git
cd EcoWave
docker compose build ecowave
```

Le build dure ~1 minute (Python 3.12-slim + dépendances numpy/pandas/
statsmodels/scipy/nolds/antropy).

## Étape 2 — Vérifier la suite de tests

```bash
docker compose run --rm --entrypoint pytest ecowave
```

Attendu :

```
================ 225 passed, 2 skipped, 259 warnings in 18.85s =================
```

Si ce n'est pas le cas, ne passez pas à l'étape suivante — votre
environnement Docker a un problème qui faussera les résultats.

## Étape 3 — Initialiser la base SQLite et l'ingestion

Les sidecars de benchmark dépendent des panels macro déjà chargés en
SQLite. Si la DB est vide, il faut d'abord les charger :

```bash
docker compose run --rm ecowave init-db
docker compose run --rm ecowave position-cycles --horizon wb
docker compose run --rm ecowave position-cycles --horizon q
docker compose run --rm ecowave position-cycles --horizon long
docker compose run --rm ecowave position-cycles --horizon boe
docker compose run --rm ecowave position-cycles --horizon bis
docker compose run --rm ecowave position-cycles --horizon sh
```

Chaque `position-cycles` (a) télécharge ou utilise les données mises en
cache dans `data_raw/`, (b) calcule la décomposition CPV pour le panel
correspondant, (c) écrit les observations dans `cycle_observations` /
`cycle_observations_quarterly`.

Si vous avez déjà tourné le projet, ces commandes sont des no-ops
(idempotentes).

## Étape 4 — Exécuter le benchmark panel par panel

Le script ci-dessous exécute les 6 panels en séquence et écrit chaque
sidecar JSON dans `reports/`. Total ~12-15 minutes.

```bash
for panel in wb q long boe bis sh; do
  args="--horizon-data ${panel} --horizons 1,3,6,12"
  args="${args} --n-origins 12 --n-samples 200 --variables-limit 8"
  if [ "${panel}" = "wb" ] || [ "${panel}" = "sh" ]; then
    # Annual panels with < 76 obs need a lower train floor
    args="${args} --min-train-length 40"
  fi
  docker compose run --rm ecowave forecast-benchmark ${args}
done
```

Pour chaque panel, le CLI affiche :

```
Running benchmark on <N> variables across <K> groups, 6 models, 4 horizons, 12 origins…
Verdict: pass_rate=<P>% (PASS|FAIL) at h=12. Sidecar → /app/reports/forecast_benchmark_2026_05_<panel>.json.
```

## Étape 5 — Consolider les 6 verdicts

```bash
docker compose run --rm ecowave forecast-benchmark-consolidate
```

Attendu :

```
Consolidated verdict: aggregate pass rate 78% (PASS) on 53/68 variables across 6 panels (missing: none). Page → /app/docs/forecast_benchmark.md.
```

La page `docs/forecast_benchmark.md` est régénérée — visible aussi
sur le site déployé.

## Lecture des sidecars

Chaque sidecar JSON suit le schéma documenté dans
[`consolidated_report.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/consolidated_report.py)
(`schema_version = 1`). Champs principaux :

- `verdict.decision_horizon` : horizon de l'acceptance criterion (12)
- `verdict.n_variables_with_baseline` : combien de variables ont un
  baseline RW comparable
- `verdict.pass_rate` : fraction des variables où ≥ 1 modèle cluster
  bat RW en CRPS
- `verdict.passes` : booléen `pass_rate >= 0.5`
- `verdict.best_cluster_model_per_variable` : modèle vainqueur par
  variable (`""` si aucun cluster compétent)
- `verdict.cluster_beats_baseline_per_variable` : booléen par variable
- `cells` : 1 record par `(group, variable, model, horizon)` avec
  `mean_crps`, `mean_rmse`, `mean_mae`, `mean_coverage_95`,
  `mean_tail_left_5pct`, `mean_tail_right_5pct`, `mean_bias`,
  `n_origins`
- `failures` : forecasts qui ont raised une exception, avec
  `error`

Exploration rapide avec `jq` :

```bash
jq '.verdict.pass_rate' reports/forecast_benchmark_2026_05_long.json
# 0.88

jq '.cells[] | select(.horizon == 12 and .model == "msm")
   | {var: (.group + "::" + .variable), crps: .mean_crps}' \
   reports/forecast_benchmark_2026_05_long.json
```

## Comportement attendu vs réel

| Panel | Attendu (n_origins=12) | Tolérance |
|---|---|---|
| wb | 60 % | ±5 % |
| q | 79 % | ±10 % |
| long | 88 % | ±5 % |
| boe | 88 % | ±5 % |
| bis | 83 % | ±5 % |
| sh | 62 % | ±10 % |
| **agrégé** | **78 %** | **±3 %** |

Les écarts > tolérance sont des **régressions** :

- Si `wb` chute sous 55 % : problème probable de filtrage de variables
  (vérifier `--min-train-length`).
- Si l'agrégé chute sous 70 % : régression méthodologique. Re-vérifier
  les tests `pytest tests/test_forecasting_*` et auditer les diffs
  récents sur `ecowave/forecasting/`.

## Reproductibilité numérique

Le verdict global (78 %) est **robuste à `n_origins`** : doublé de 6 à
12, il reste 78 % (delta sur les wins individuels mais agrégat
inchangé — voir [forecast benchmark consolidé](../../forecast_benchmark.md)).

Les seeds sont fixés : `seed=0` partout par défaut. Changer la seed
fait varier le verdict de quelques pourcents (échantillonnage MC),
mais le pattern qualitatif (MSM domine boe/long, HAR domine q,
ARFIMA+RS niche crédit) est stable.

## Customisation

Le CLI expose tous les paramètres ([code source CLI](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/cli.py)) :

```
ecowave forecast-benchmark
  --horizon-data wb|q|long|boe|bis|sh
  --groups <comma-separated>      # défaut : 1-2 groupes par panel
  --horizons 1,3,6,12              # défaut
  --models rw,ar1,arma11,har,arfima_rs,msm  # subset OK
  --variables-limit 8              # top N variables par groupe (par longueur)
  --n-origins 6                    # défaut
  --n-samples 200                  # paths MC par forecast
  --test-fraction 0.25             # fraction terminale du holdout
  --decision-horizon 12            # h pour l'acceptance criterion
  --beat-threshold 0.5             # seuil falsifiable
  --seed 0
  --min-train-length 64            # plancher samples pour fit
  --sidecar-path <path>            # override
  --page-path <path>               # override
```

Pour un run "quick smoke" (~2 min) :

```bash
docker compose run --rm ecowave forecast-benchmark \
  --horizon-data long --groups ADV18 \
  --horizons 1,12 --n-origins 3 --n-samples 50 \
  --variables-limit 4
```

## Quand le verdict est PASS — et quand il ne l'est pas

Le critère d'acceptance Roadmap #20 est :

> Au minimum 1 modèle du cluster doit battre random walk en
> out-of-sample CRPS à horizon 12 sur ≥ 50 % des variables.

Notre verdict actuel **78 %** est largement au-dessus. Mais le critère
est conçu pour pouvoir **échouer** :

- Si vous changez de panel (par exemple ajoutez un nouveau panel
  exotique) et que le pass rate tombe sous 50 % : l'image cluster perd
  un argument empirique sur ce panel.
- Si une révision méthodologique fait passer un panel sous 50 % : il
  faut comprendre pourquoi avant de la merger.

Le projet a un historique falsifiable : voir
[failure modes](failure_modes.md) pour l'analyse des 15 variables où
le cluster perd actuellement.
