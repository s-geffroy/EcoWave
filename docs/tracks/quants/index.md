# Track quants

> *Pour praticiens de la finance quantitative, prévisionnistes,
> data scientists économiques, équipes risque.* Si vous estimez des
> modèles de volatilité, calibrez du VaR/ES, produisez des forecasts
> probabilistes, ou comparez des modèles sur métrique propre,
> **cette page est faite pour vous**.

## La proposition technique

1. **Le cluster CPV (C+B+D+I+S) a un benchmark out-of-sample
   reproductible.** Six modèles (RW, AR(1), ARMA(1,1), HAR Corsi 2009,
   ARFIMA + regime-switching, MSM Calvet-Fisher 2002) testés contre
   random walk sur 68 variables macro, 6 panels, horizons 1–12 ans
   (ou trimestres). Métrique : CRPS empirique (Gneiting-Raftery 2007),
   tail coverage 5 % gauche/droite, coverage 95 % central, Mincer-
   Zarnowitz. Verdict reproductible : **PASS 78 %** à h = 12.
2. **MSM domine sur les histoires longues** (Bank of England 1700–2016,
   long-history Maddison + JST 1870–2020, BIS quarterly 1970–2024). Le
   cascade multifractale à 4 composantes paye sur les séries longues.
3. **HAR domine sur le quarterly contemporain** (USA + Euro Area
   1995–2024). La cascade par agrégation `(1, 2, 4)` lag-OLS suffit à
   courte cadence — pas besoin de la machinerie multifractale.
4. **ARFIMA + regime-switching a sa niche en crédit et macro lente.**
   La paire (long memory exact via Hosking + 2-regime Markov mean &
   variance via statsmodels MarkovRegression) est compétitive sur
   `LH_CREDIT` (Jordà-Schularick-Taylor) et plusieurs variables BIS.
5. **Aucune baseline stationnaire (RW, AR(1), ARMA(1,1)) ne gagne**
   quand un modèle cluster est compétent. C'est la validation
   *opérationnelle* (et pas seulement statistique) du verdict CPV.

## Contenu (en cours de livraison)

| Page | Statut |
|---|---|
| Catalogue des modèles : MSM / ARFIMA+RS / HAR specs + code | *à venir* |
| Benchmark reproductible : pas-à-pas pour atteindre PASS 78 % | *à venir* |
| API publique `ecowave.forecasting` | *à venir* |
| Extensions roadmap : HABM, MRW, ABM | *à venir* |
| Failure modes : quand et pourquoi le cluster perd | *à venir* |
| **Note quants (~5 000 mots, technique reproductible)** | *en cours* |

## En attendant

- Le **[forecast benchmark consolidé](../../forecast_benchmark.md)** est
  la page de référence du verdict opérationnel : pass rate par panel,
  leaderboard cluster, lecture qualitative.
- Le code est sur GitHub, conteneurisé. Reproduction directe (Docker
  obligatoire — voir `CLAUDE.md`) :

    ```bash
    for panel in wb q long boe bis sh; do
      args="--horizon-data ${panel} --horizons 1,3,6,12"
      args="${args} --n-origins 12 --n-samples 200 --variables-limit 8"
      if [ "${panel}" = "wb" ] || [ "${panel}" = "sh" ]; then
        args="${args} --min-train-length 40"
      fi
      docker compose run --rm ecowave forecast-benchmark ${args}
    done
    docker compose run --rm ecowave forecast-benchmark-consolidate
    ```

    Régénère `docs/forecast_benchmark.md` à partir des sidecars JSON
    par panel. Tests : 225 passing en Docker, 0 régression depuis
    PR #30 (le premier incrément du chantier #20).
- La **[méthode (détail technique)](../../methodology/protocole_cpv.md)**
  documente Gate 1/2/3 et les diagnostics Tier 1+2.
- Les **[diagnostics non-cycliques](../../dx_diagnostics.md)** publient
  les heatmaps des 14 statistiques par cellule (group × variable × test
  diagnostique).
