# Catalogue des modèles

> *Six modèles, trois familles, une interface unique.* Chaque modèle
> produit un objet `ProbabilisticForecast` standardisé que la pipeline
> de scoring consomme sans branchement spécifique.

## Interface commune

Tous les modèles partagent la même signature de fonction :

```python
def model_forecast(
    history: np.ndarray,            # 1-D level series, no NaNs
    horizons: tuple[int, ...],      # forecast horizons in cadence steps
    n_samples: int = 1000,          # MC paths
    seed: int = 0,                  # RNG seed (deterministic)
    **config_specific_kwargs,
) -> ProbabilisticForecast
```

Retour : un `ProbabilisticForecast` portant `samples` de shape
`(n_samples, len(horizons))`. Le sample-based representation est la
*lingua franca* : empirical CRPS, coverage, tail coverage sont
calculés sur la matrice sans hypothèse paramétrique.

Code : [`ecowave/forecasting/types.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/types.py).

## Famille 1 — Baselines stationnaires

### Random walk (RW)

**Spécification** : `X_{t+h} = X_t + Σ_{k=1}^{h} ε_k` avec
`ε_k ~ N(0, σ²)` estimé par la sample variance des first differences.

**Hypothèses** : pas de tendance, innovations gaussiennes
indépendantes. La variance prédictive croît linéairement avec h.

**Quand utiliser** : comme *benchmark de référence* — c'est le modèle
qu'on doit battre. Surtout pas comme modèle final.

**Code** : `random_walk_forecast` dans
[`baselines.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/baselines.py).

```python
forecast = random_walk_forecast(history, horizons=(1, 3, 12), n_samples=500, seed=0)
```

### AR(1)

**Spécification** : `X_t = c + φ X_{t-1} + ε_t` estimé par OLS. Pour
`|φ| ≥ 0.999` (quasi-unit-root), fallback automatique vers RW pour
éviter les explosions à long horizon.

**Quand utiliser** : comparateur stationnaire minimal. Si AR(1) bat
RW de façon significative, la série est mean-reverting — c'est un
diagnostic utile.

**Code** : `ar1_forecast` dans
[`baselines.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/baselines.py).

### ARMA(1, 1)

**Spécification** : `X_t = c + φ X_{t-1} + ε_t + θ ε_{t-1}` estimé par
ML via `statsmodels.tsa.SARIMAX(order=(1, 0, 1))`. Fallback vers AR(1)
en cas d'échec de convergence (séries courtes, near-integrated).

**Quand utiliser** : test du gain d'un terme MA. Modeste habituellement.

**Code** : `arma11_forecast` dans
[`baselines.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/baselines.py).

## Famille 2 — Cluster cascade

### HAR — Heterogeneous Autoregressive (Corsi 2009)

**Spécification** : `y_t = c + b_s · S_{t-1} + b_m · M_{t-1} + b_l ·
L_{t-1} + ε_t` où `S`, `M`, `L` sont des moyennes glissantes à trois
échelles. Default mensuel : `(1, 3, 12)`. Default trimestriel : `(1, 2, 4)`.

**Hypothèses** : la longue mémoire empirique émerge de l'agrégation de
trois cascades à fréquences hétérogènes. Innovations gaussiennes
homoscédastiques.

**Quand utiliser** : quarterly contemporain ou monthly. Notre benchmark
montre 16 wins sur les 6 panels, dominants sur `q` (8/13 wins) et
`boe` (4/7 wins).

**Code** : `har_forecast` dans
[`har.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/har.py).
Configuration : `HARLagConfig(short, medium, long)`.

```python
from ecowave.forecasting.har import HARLagConfig, har_forecast

forecast = har_forecast(
    history,
    horizons=(1, 3, 6, 12),
    n_samples=200,
    lag_config=HARLagConfig(1, 2, 4),  # quarterly
)
```

### ARFIMA(0, d, 0) + Regime-Switching (Bhardwaj-Swanson 2006)

**Spécification** :

1. Estime `d` par log-périodogramme GPH (bandwidth `m = T^0.5`),
   clipping à `[-0.499, 0.499]`.
2. Calcule la série différenciée fractionnaire `Y_t = (1 - L)^d X_t`
   par convolution Hosking 1981 tronquée.
3. Fit `MarkovRegression` à 2 régimes sur `Y` (switching mean +
   variance via statsmodels).
4. Simule chaîne de Markov forward + tirage Gaussien régime-conditionnel.
5. Reconstruit le niveau par récursion inverse
   `X_t = Y_t - Σ ψ_k · X_{t-k}` où `ψ_k` sont les coefficients
   Hosking.

**Hypothèses** : longue mémoire exacte (`d ∈ (-0.5, 0.5)`) + dérive de
régime cognitif à 2 états Markov. Fallback gracieux vers single-regime
ARFIMA(0, d, 0) si `MarkovRegression` ne converge pas.

**Quand utiliser** : variables avec longue mémoire claire et signature
de switching (notamment crédit). 14 wins sur les 6 panels, niche
spécifique sur `LH_CREDIT`.

**Code** : `arfima_rs_forecast` dans
[`arfima_rs.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/arfima_rs.py).
Configuration : `ARFIMARSConfig(n_regimes, bandwidth_exponent,
hosking_truncate, switching_variance)`.

Primitives réutilisables : `fractional_difference`,
`fractional_integrate`, `gph_estimate_d`, `hosking_coefficients` dans
[`fractional.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/fractional.py).

### MSM — Markov-Switching Multifractal (Calvet-Fisher 2002)

**Spécification** :

```
r_t = σ_t · z_t,    z_t ~ N(0, 1)
σ_t = σ̄ · √(M_{1,t} · M_{2,t} · … · M_{K,t})
M_{k,t} ∈ {m_0, 2 − m_0},   chaîne de Markov à 2 états
γ_k = 1 − (1 − γ_1)^{b^{k−1}}
```

**4 paramètres** : `(m_0, σ̄, b, γ_1)`.

- `m_0` : taille du multiplicateur (proche de 1 = volatilité stable,
  proche de 2 = bursts intenses)
- `σ̄` : niveau de volatilité unconditionnelle
- `b` : décroissance géométrique des taux de switching à travers les
  composantes (`b > 1`)
- `γ_1` : probabilité de switch de la composante la plus rapide

**Estimation** : ML par filtre forward Hamilton sur l'espace combiné
`2^K` états. `K = 4` (16 états) est le sweet spot Calvet-Fisher.
Grille de starting points + L-BFGS-B avec box constraints. Fallback
gracieux (single random-walk) si toutes les optimisations divergent.

**Simulation** : tirage de l'état initial depuis la distribution
filtrée terminale, puis chaînes indépendantes par composante
(exponentiellement moins cher que la chaîne jointe sur `2^K` états).
Reconstruction des niveaux : log-returns cumulés (si série > 0) ou
first differences cumulés.

**Quand utiliser** : panels longs (histoires de plusieurs siècles ou
décennies). Notre benchmark montre 23 wins sur les 6 panels,
dominants sur `boe` (6/7), `long` (7/14) et `bis` (6/10).

**Code** : `msm_forecast` dans
[`msm.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/msm.py).
Configuration : `MSMConfig(n_components, use_log_returns,
fallback_on_failure)`.

```python
from ecowave.forecasting.msm import MSMConfig, msm_forecast

forecast = msm_forecast(
    history,
    horizons=(1, 3, 6, 12),
    n_samples=200,
    config=MSMConfig(n_components=4, use_log_returns=True),
)
```

## Table comparative

| Modèle | Famille | Paramètres | Long memory | Régime switching | Multifractalité | Code |
|---|---|---|---|---|---|---|
| RW | Baseline | 1 (σ) | non | non | non | [link](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/baselines.py) |
| AR(1) | Baseline | 3 (c, φ, σ) | non (mais persistance) | non | non | [link](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/baselines.py) |
| ARMA(1,1) | Baseline | 4 (c, φ, θ, σ) | non | non | non | [link](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/baselines.py) |
| HAR | Cluster | 5 (c, b_s, b_m, b_l, σ) | par agrégation | non | non | [link](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/har.py) |
| ARFIMA+RS | Cluster | 4 + 2·k_regimes (d, c, σ, μ_k, σ_k, p_k) | **exact (d)** | **oui (Markov)** | non | [link](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/arfima_rs.py) |
| MSM | Cluster | 4 (m_0, σ̄, b, γ_1) | **par cascade** | **oui (multi-composant)** | **oui** | [link](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/msm.py) |

## Quel modèle sur quel panel ?

Verdict empirique de notre [forecast benchmark consolidé](../../forecast_benchmark.md) (n_origins=12, h=12) :

| Panel | Vainqueur dominant | Note |
|---|---|---|
| `wb` (1960-2024 annuel) | **MSM 4/6 wins** | Limité par série courte ; voir failure modes |
| `q` (1995-2024 trimestriel) | **HAR 8/11 wins** | Cascade par agrégation suffit à courte cadence |
| `long` (1870-2024 annuel) | **MSM 8/14 wins** | Bénéficie de l'historique long |
| `boe` (1700-2016 annuel) | **MSM 6/7 wins** | Idem, encore plus marqué |
| `bis` (1970-2024 trim.) | **MSM 6/10 wins** | Variables financières favorables MSM |
| `sh` (annuel court) | **MSM 2/5 + ARFIMA+RS 2/5** | Spécialisation ARFIMA+RS sur LH_CREDIT |

## Pour aller plus loin

- [Benchmark reproductible](benchmark_reproducible.md) — pas-à-pas pour
  obtenir le verdict PASS 78 % sur votre machine.
- [API publique](code_api.md) — signature de chaque fonction
  exportée.
- [Failure modes](failure_modes.md) — analyse des 15 variables où
  aucun modèle cluster n'a battu RW.
- [Extensions roadmap](extensions_roadmap.md) — HABM, MRW, ABM,
  active inference, ensemble methods.
