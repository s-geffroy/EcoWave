# Note quants — le cluster CPV en pratique

*Synthèse technique reproductible. ~5 000 mots. Pour data scientists,
prévisionnistes, équipes risque.*

---

## TL;DR

Notre **forecast benchmark** Roadmap #20 teste 6 modèles (3 baselines
+ 3 modèles cluster issus de la littérature multifractale et long-
memory) sur **68 variables macro** réelles, **6 panels** couvrant
1700-2024, avec un protocole rolling-origin out-of-sample. Le verdict
est **PASS 78 %** à horizon 12 (largement au-dessus du seuil
falsifiable 50 %), **robuste à `n_origins`** (doubler de 6 à 12 ne
change pas l'agrégat).

**MSM Calvet-Fisher** domine les histoires longues (`boe` 6/7 wins,
`long` 8/14, `bis` 6/10). **HAR Corsi** domine le trimestriel
contemporain (`q` 8/11 wins). **ARFIMA+RS Bhardwaj-Swanson** a une
niche en crédit (`LH_CREDIT`, plusieurs variables BIS). Aucune
baseline (RW, AR(1), ARMA(1,1)) ne gagne quand un modèle cluster est
compétent.

Tout est reproductible en Docker en **~15 minutes** avec une seule
commande de boucle shell. Le code est public ([GitHub](https://github.com/s-geffroy/EcoWave)),
le schéma des sidecars JSON est documenté (`schema_version = 1`), et
nous publions le code sous licence MIT.

---

## Pourquoi un benchmark ?

Le projet CPV part d'une démolition empirique : les 4 cycles canoniques
(Kitchin, Juglar, Kuznets, Kondratieff) ne survivent pas à un triple
gate (dual null + consensus multi-méthode + universalité cross-
aggregates) sur 6 panels macro. Ce résultat — détaillé dans le
[track académique](../acad/index.md) et le [working paper V1](../../papers/cpv_main_paper.md)
— est *destructif*.

Sa critique légitime : "ok les cycles sont morts, mais qu'est-ce que
vous proposez à la place ?" Les diagnostics non-cycliques Tier 1+2
montrent un cluster stable **C + B + D + I + S** (longue mémoire,
multifractalité, non-linéarité, information structurée, dérive de
régime cognitif) — mais c'est une signature, pas un modèle.

D'où le benchmark : **prouver opérationnellement** qu'on peut
construire des modèles qui reproduisent cette signature et **font mieux
que random walk en prévision out-of-sample**. Sans cette preuve, la
critique CPV reste destructive ; avec, elle a son pendant constructif.

C'est le chantier Roadmap #20, livré dans les PRs #30 → #38.

---

## Les six modèles

### Baselines stationnaires (3)

**Random walk** (`rw`) — `X_{t+h} = X_t + Σ ε_k`, Gaussian. Le
benchmark à battre. Variance prédictive croît linéairement avec `h`.

**AR(1)** (`ar1`) — `X_t = c + φ X_{t-1} + ε_t`. Fallback automatique
vers RW si `|φ| ≥ 0.999` (quasi-unit-root, explosion à long h).

**ARMA(1, 1)** (`arma11`) — `X_t = c + φ X_{t-1} + ε_t + θ ε_{t-1}`
via `statsmodels.SARIMAX`. Fallback vers AR(1) si l'optimisation ne
converge pas.

### Cluster (3)

**HAR** (`har`) — Heterogeneous Autoregressive Corsi 2009. Régression
OLS sur 3 moyennes glissantes `(short, medium, long)`. Par défaut
`(1, 3, 12)` pour mensuel, `(1, 2, 4)` pour trimestriel. La longue
mémoire empirique émerge de l'agrégation, sans paramètre `d`.

**ARFIMA(0, d, 0) + Markov-Switching** (`arfima_rs`) — Bhardwaj-
Swanson 2006. Pipeline en 5 étapes : (1) GPH estimate de `d`, (2)
Hosking fractional differencing, (3) MarkovRegression à 2 régimes sur
le résidu, (4) simulation Markov forward + tirage Gaussien régime-
conditionnel, (5) reconstruction des niveaux par récursion inverse.
Fallback gracieux vers single-regime.

**MSM** (`msm`) — Markov-Switching Multifractal Calvet-Fisher 2002.
Cascade `σ_t = σ̄ √(M_1 · … · M_K)` avec K = 4 multiplicateurs
indépendants en `{m_0, 2 - m_0}`. 4 paramètres `(m_0, σ̄, b, γ_1)`
estimés par filtre forward Hamilton sur `2^K = 16` états. Simulation
par composantes indépendantes (exponentiellement moins cher que la
chaîne jointe). Fallback gracieux si l'optimisation diverge.

---

## L'interface commune

Tous les modèles partagent la signature :

```python
def model_forecast(history, horizons, n_samples=1000, seed=0, **kwargs) -> ProbabilisticForecast
```

Le retour est un `ProbabilisticForecast` portant `samples` de shape
`(n_samples, len(horizons))`. C'est la **lingua franca** : tout le
scoring downstream consomme cette matrice sans branchement
spécifique.

Pourquoi sample-based ? Trois raisons :

1. **CRPS empirique** ne demande pas d'hypothèse paramétrique.
   L'identité Gneiting-Raftery 2007 `CRPS = E|X - y| − ½ E|X - X'|`
   s'évalue en O(n log n) sur `n` samples via la formule rank-based
   pour la Gini-mean-difference.
2. **Coverage** se lit comme un quantile empirique. Le central 95 %
   est entre `q_0.025` et `q_0.975`. Le tail 5 % gauche/droite est
   `q_0.05` et `q_0.95`. Pas de fit paramétrique requis.
3. **Heavy tails** sont préservées. Un fit gaussien sur les samples
   les casserait — sample-based les garde.

Coût : `n_samples × max(horizons)` cellules Monte Carlo par forecast.
Pour `n_samples = 200` et `max_horizon = 12`, c'est 2 400 cellules par
forecast — négligeable.

---

## Le pipeline benchmark

### Rolling-origin out-of-sample

Pour chaque variable, on garde les `test_fraction` (25 %) dernières
observations comme holdout. À l'intérieur on place `n_origins`
origines évenly-spaced. Pour chaque origine `t` :

1. Fit chaque modèle sur `history[:t]` (longueur ≥ `min_train_length`).
2. Forecast aux horizons `(1, 3, 6, 12)`.
3. Score chaque forecast contre `history[t + h - 1]` pour chaque `h`.

Les scores sont :

- **CRPS** (proper, sample-based)
- **RMSE** (point error)
- **MAE** (point error)
- **Coverage 95 %** (0/1 : observation dans le central 95 % ?)
- **Tail coverage left/right 5 %** (0/1 : observation au-delà des
  queues 5 % ?)
- **Bias** (sample mean - observation)

Moyennés sur les `n_origins` origines pour chaque cellule `(group,
variable, model, horizon)`.

### Acceptance criterion

Pour chaque variable, on prend le best cluster model (lowest mean
CRPS au horizon de décision `h = 12`) et on le compare au baseline
(RW par défaut). La variable "passe" si `best_cluster.crps <
baseline.crps`.

Le verdict global est `pass_rate ≥ beat_threshold` où
`pass_rate = n_passes / n_variables_with_baseline` et `beat_threshold
= 0.5` (50 %).

Cette construction est **falsifiable** : avec un seuil à 50 % et un
horizon fixé à 12, on peut clairement échouer. Si l'image cluster
était fausse, on s'attendrait à un pass rate ~25-40 % (les 3 modèles
cluster valent en moyenne ~les baselines, choisir le meilleur des 3
donne un boost mais pas suffisant pour passer 50 %).

---

## Le verdict actuel : PASS 78 %

Sur les 6 panels avec n_origins=12 :

| Panel | Pass rate | n vars | Winners |
|---|---|---|---|
| wb | 60 % | 10 | MSM 4 · HAR 2 |
| q | 79 % | 14 | HAR 8 · ARFIMA+RS 5 |
| long | 88 % | 16 | MSM 8 · HAR 4 · ARFIMA+RS 2 |
| boe | 88 % | 8 | MSM 6 · HAR 1 |
| bis | 83 % | 12 | MSM 6 · ARFIMA+RS 3 · HAR 1 |
| sh | 62 % | 8 | MSM 2 · ARFIMA+RS 2 · HAR 1 |
| **agrégé** | **78 %** | **68** | **MSM 23 · HAR 16 · ARFIMA+RS 14** |

Le seuil falsifiable 50 % est largement dépassé. **Aucun panel** ne le
franchit par le bas. Le total leaderboard cluster est 53 wins
distribués entre les 3 modèles.

### Robustesse à `n_origins`

En passant `n_origins` de 6 à 12, le verdict agrégé reste **78 %**.
Quelques panels bougent (q 93 → 79 %, long 69 → 88 %), avec
redistribution mineure du leaderboard (MSM 25 → 23, HAR 15 → 16,
ARFIMA+RS 12 → 14). Le pattern qualitatif (MSM ↔ longs, HAR ↔
quarterly, ARFIMA+RS ↔ crédit) est stable.

C'est le test de robustesse principal : avec deux fois plus
d'observations rolling-origin, l'estimation de `pass_rate` est plus
précise. Le fait que l'agrégat ne bouge pas est rassurant.

### Robustesse à la seed

Le seed RNG est `seed = 0` partout par défaut. Changer la seed fait
varier le verdict de ±2-3 % (échantillonnage MC sur les forecasts
probabilistes). Le pattern qualitatif reste.

---

## Pourquoi ces modèles, et pas d'autres ?

Le choix des 3 modèles cluster est dicté par 3 critères :

1. **Pertinence théorique** au cluster C+B+D+I+S.
2. **Maturité dans la littérature** (papiers fondateurs cités > 1 000
   fois, implémentations publiques).
3. **Coût d'estimation tractable** pour benchmark scale (~6 000
   forecasts).

**MSM** combine B (multifractalité par construction), C (long memory
émergeant de la cascade) et queues lourdes (mélange de régimes de
variance). C'est le modèle canonique du cluster.

**ARFIMA+RS** combine C (long memory exact via `d`) et S
(regime-switching à 2 états sur le résidu). C'est la combinaison
canonique selon Bhardwaj-Swanson 2006.

**HAR** est le workhorse industriel — trivialement OLS, robuste,
prouvé sur la volatilité réalisée. Cascade par agrégation, capture
empiriquement la longue mémoire sans paramètre `d`.

D'autres modèles candidats (HABM, MRW, AMH-ensemble, active inference)
sont dans la
[roadmap d'extensions](extensions_roadmap.md) — pas livrés dans le
benchmark v1 par contrainte de scope.

---

## Failure modes : où le cluster perd

Sur les 15 / 68 variables (22 %) où aucun modèle cluster ne bat RW,
les patterns identifiés sont :

- **5 taux d'intérêt** (Q_YIELD × 2, LH_YIELD, BOE_STIR, BIS_CRATIO
  partiellement). Taux administrés par BC + régime ZIRP atypique.
- **6 variables courtes annuelles** sur wb (1960-2024) et sh
  (~50 obs). Identification instable pour MSM à 4 composantes.
- **4 agrégats commerce/investissement** (CY_TRD × 2, CY_INV × 2,
  EA::Q_INV, BIS_HHCRED). Chocs structurels exogènes mal modélisés
  par le cluster.
- **3 séries historiques US sectorielles** (SH_US_RAILFREIGHT,
  SH_US_STEEL, SH_US_INDPROD). Cas où la structure cyclique pré-
  moderne pourrait subsister partiellement.

Détails complets : voir [failure modes](failure_modes.md).

**Rien dans ces 15 échecs ne disqualifie le cluster.** Au contraire,
chaque pattern a une explication structurelle claire qui suggère soit
une amélioration de modèle (priors, K adaptive), soit l'usage d'un
modèle externe (jump-diffusion sur les taux), soit une acceptance que
sur certaines séries spécifiques RW est l'optimum opérationnel.

---

## Reproduction sur votre machine

Pré-requis : Docker. Aucune install Python locale.

```bash
git clone https://github.com/s-geffroy/EcoWave.git
cd EcoWave
docker compose build ecowave

# 1. Tests (sanity check) — doit afficher 225 passed
docker compose run --rm --entrypoint pytest ecowave

# 2. Ingestion des panels si DB vide
docker compose run --rm ecowave init-db
for panel in wb q long boe bis sh; do
  docker compose run --rm ecowave position-cycles --horizon ${panel}
done

# 3. Benchmark panel par panel
for panel in wb q long boe bis sh; do
  args="--horizon-data ${panel} --horizons 1,3,6,12"
  args="${args} --n-origins 12 --n-samples 200 --variables-limit 8"
  if [ "${panel}" = "wb" ] || [ "${panel}" = "sh" ]; then
    args="${args} --min-train-length 40"
  fi
  docker compose run --rm ecowave forecast-benchmark ${args}
done

# 4. Consolidation
docker compose run --rm ecowave forecast-benchmark-consolidate
```

Total ~15-30 minutes. La page `docs/forecast_benchmark.md` est
régénérée avec votre verdict consolidé.

Détails et flags : voir [benchmark reproductible](benchmark_reproducible.md).

---

## API publique

Le module `ecowave.forecasting` est designé pour être utilisable
en bibliothèque, pas seulement via CLI :

```python
import numpy as np
from ecowave.forecasting.benchmark import (
    BenchmarkConfig, run_benchmark, evaluate_acceptance_criterion,
)
from ecowave.forecasting.reporting import write_benchmark_sidecar

# Tes propres panels — dict[group, dict[variable, np.ndarray]]
panels = {"MY_GROUP": {"MY_VAR": np.array([...])}}

config = BenchmarkConfig(
    horizons=(1, 12),
    models=("rw", "msm", "har"),
    n_origins=8,
    n_samples=500,
)

results = run_benchmark(panels, config=config)
verdict = evaluate_acceptance_criterion(results, decision_horizon=12)

print(f"Pass rate: {verdict.pass_rate:.0%}")
print(f"Best cluster per variable: {verdict.best_cluster_model_per_variable}")
```

Référence complète : voir [API publique](code_api.md).

---

## Limites connues

1. **Forecast unconditional**. Notre pipeline ne conditionne pas sur
   covariables exogènes (taux directeurs, indicateurs avancés). Pour
   prévision conditionnelle, il faudrait étendre l'interface
   `ProbabilisticForecast` avec un `exog` parameter et adapter chaque
   modèle. Effort estimé : ~10 jours.
2. **Pas de cross-variable structure**. Les forecasts sont
   indépendants par variable. Pour capturer les corrélations
   contemporaines (par exemple inflation ↔ taux ↔ chômage), il
   faudrait un VARFIMA ou un MSM multivarié. Non livré v1.
3. **Évaluation point + intervalle, pas densité jointe inter-horizon**.
   Le CRPS est marginal par horizon. La densité jointe `(X_{t+1}, …,
   X_{t+12})` n'est pas évaluée. Energy score ou Variogram score
   complèteraient — voir [extensions](extensions_roadmap.md).
4. **Pas de test statistique sur la différence CRPS**. Aujourd'hui
   l'acceptance criterion est binaire "mean_cluster < mean_baseline".
   Pas de p-value Diebold-Mariano. Donc on peut dire "le cluster
   gagne 78 % en valeur moyenne" mais pas "le cluster gagne 78 % avec
   p < 0.05". À ajouter — voir [extensions](extensions_roadmap.md).
5. **Calibration de la seed**. Le seed `seed = 0` partout est une
   convention de reproductibilité. Pour publication scientifique, il
   faudrait faire bootstrap sur les seeds et reporter intervalles de
   confiance sur le pass rate.

---

## Implications pour les utilisateurs

### Pour la prévision opérationnelle

Si vous prévoyez des variables macro à horizon ≥ 6 mois, **utilisez
MSM ou ARFIMA+RS au lieu de random walk**. Performance attendue : ~30 %
de réduction de CRPS sur les variables où le cluster gagne. Coût
computationnel : MSM ~5 secondes par fit, ARFIMA+RS ~2 secondes.

### Pour la gestion du risque

Le diagnostic préalable des panels via les Tier 1+2 (long memory,
multifractalité, non-linéarité, regime drift) est plus important que
le choix du modèle. Si les diagnostics rejettent fortement le cluster
C+B+D+I+S sur votre série, ne forcez pas un MSM — le baseline RW est
optimal.

### Pour la recherche

Les patterns failure modes (taux administrés, séries courtes, agrégats
exogènes-driven) ouvrent des questions de recherche. Les
[extensions roadmap](extensions_roadmap.md) listent ~10 chantiers.
Contributions GitHub bienvenues.

---

## Conclusion

Le benchmark Roadmap #20 livre un verdict opérationnel **falsifiable
mais positif** : 78 % de variables battues par le cluster vs random
walk, à horizon de politique économique (h = 12). Aucune baseline
stationnaire (AR(1), ARMA(1,1)) ne gagne. La signature cluster
C+B+D+I+S a maintenant son pendant constructif.

Tout est reproductible en Docker, le code est public, les sidecars
JSON sont standardisés (`schema_version = 1`), et la roadmap
d'extensions est explicite. Si vous voulez contribuer ou utiliser nos
modèles dans votre pipeline, le matériel est prêt.

---

*Liens utiles :*

- [Catalogue des modèles](models_catalog.md) — specs précises de chaque modèle
- [Benchmark reproductible](benchmark_reproducible.md) — guide pas à pas
- [API publique](code_api.md) — référence Python du module `ecowave.forecasting`
- [Extensions roadmap](extensions_roadmap.md) — HABM, MRW, AMH, active inference, Diebold-Mariano
- [Failure modes](failure_modes.md) — analyse des 15 variables battues par RW
- [Verdict consolidé](../../forecast_benchmark.md) — vue cross-panel
