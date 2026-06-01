# Horizon-aware targeting

!!! success "TL;DR"

    Différents modèles dominent à différents horizons. **HAR** pour nowcast (h = 0-3), **HAR ou MSM** pour horizon BC (h = 4-8, choix par BIC), **MSM** pour long terme (h ≥ 12), **ARFIMA+RS** pour variables de crédit. Une BC qui utilise un seul modèle "tout-horizon" sous-optimise systématiquement. Gain estimé : ~30 % de réduction CRPS sur variables où cluster gagne. Implémentation Python en pipeline standard 3-horizons.

## Dans cette page

- **[Le problème](#probleme)** — horizon unique = sous-optimisation
- **[Verdict empirique par horizon](#verdict)** — domination par horizon
- **[Recommandations opérationnelles](#recommandations)**
- **[Implémentation BC pratique](#implementation)** — pipeline 3-horizons
- **[Conséquences théoriques](#theorie)**
- **[Limites et précautions](#limites)**

---

## Le problème { #probleme }

Les banques centrales fonctionnent avec un **horizon de politique
monétaire** typiquement compris entre 6 et 8 trimestres (18 à 24 mois).
C'est l'horizon auquel les décisions actuelles produisent leur effet
maximal sur l'inflation, selon les estimations standard de retard
monétaire (Friedman, Romer, Christiano-Eichenbaum-Evans).

Mais le modèle utilisé pour calibrer la politique est typiquement le
même que celui utilisé pour le nowcast (prévision à 0-2 trimestres) et
pour le scenario à long terme (5-10 ans). C'est un compromis pratique,
mais notre benchmark Roadmap #20 suggère que **c'est sous-optimal** :
différents modèles dominent à différents horizons.

## Le verdict empirique du benchmark

Notre [forecast benchmark consolidé](../../forecast_benchmark.md) sur
68 variables × 6 panels × horizons 1, 3, 6, 12, montre :

| Horizon | Modèle dominant cluster | Pattern |
|---|---|---|
| **h = 1** (1 trimestre / 1 mois selon panel) | HAR | Cascade par agrégation suffit pour le très court terme |
| **h = 3** | HAR | HAR continue à dominer |
| **h = 6** | MSM commence à émerger | Phase transitoire |
| **h = 12** | **MSM** | Cascade multifractale paye sur les long-horizons (47 wins sur 68) |

Pour l'horizon spécifique BC (h ≈ 6-8 trimestres en cadence
trimestrielle), c'est la zone de transition entre HAR et MSM. Selon
la nature de la variable (financière vs réelle, courte mémoire vs
longue mémoire), un modèle ou l'autre est préférable.

## Recommandations opérationnelles

### Pour le nowcasting (h ∈ [0, 3])

**Utiliser HAR** (Heterogeneous Autoregressive de Corsi 2009).

- Spécification simple : OLS sur 3 lags `(short, medium, long)`.
- Calibration trimestrielle recommandée : `HARLagConfig(1, 2, 4)` —
  cascade `(trimestre, semestre, année)`.
- Calibration mensuelle recommandée : `HARLagConfig(1, 3, 12)` —
  cascade `(mois, trimestre, année)`.
- Temps d'estimation : ~0.5 seconde par série.
- Robuste sur séries courtes (≥ 50 observations).

```python
from ecowave.forecasting.har import HARLagConfig, har_forecast

forecast_nowcast = har_forecast(
    history,
    horizons=(1, 2, 3),
    n_samples=500,
    lag_config=HARLagConfig(1, 2, 4),  # trimestriel
)
```

### Pour l'horizon de politique monétaire (h ∈ [4, 8])

**Utiliser une moyenne pondérée HAR + MSM**, ou tester les deux et
choisir le meilleur par BIC.

Notre benchmark suggère que dans cette zone, ni HAR ni MSM n'a
d'avantage systématique. Le choix dépend de :

- **Variable financière** (taux, prix d'actifs, crédit) → MSM est
  généralement meilleur. Cascade multifractale capture la
  multifractalité empirique observée sur ces variables.
- **Variable réelle** (PIB, chômage, investissement) → HAR est
  généralement compétitif voire meilleur. La cascade par agrégation
  suffit.
- **Variable d'inflation** → Tester les deux. Selon la BC, l'un ou
  l'autre peut être préféré.

```python
from ecowave.forecasting.msm import MSMConfig, msm_forecast
from ecowave.forecasting.har import har_forecast

# Tester les deux et garder le meilleur en CRPS in-sample
forecasts_msm = msm_forecast(history, horizons=(6, 8), n_samples=500)
forecasts_har = har_forecast(history, horizons=(6, 8), n_samples=500)
```

### Pour le long terme (h ≥ 12 trimestres / 3 ans)

**Utiliser MSM** (Markov-Switching Multifractal).

- Spécification : cascade multifractale à `K = 4` composantes.
- Calibration : `MSMConfig(n_components=4, use_log_returns=True)`.
- Temps d'estimation : ~5 secondes par série (filtre forward Hamilton
  sur 16 états).
- Requiert série historique longue (≥ 100 observations idéalement).

```python
forecast_long_horizon = msm_forecast(
    history,
    horizons=(12, 16, 20),
    n_samples=500,
    config=MSMConfig(n_components=4),
)
```

### Pour les variables de crédit spécifiquement

**Utiliser ARFIMA(0, d, 0) + Regime-Switching** (Bhardwaj-Swanson 2006).

Notre benchmark montre que ARFIMA+RS a une niche spécifique sur les
variables de crédit (`LH_CREDIT`, `BIS_HHCRED`, `BIS_CRATIO`). La
combinaison `d` longue mémoire + 2 régimes Markov colle bien à la
dynamique de l'accumulation et déchargement de crédit.

```python
from ecowave.forecasting.arfima_rs import ARFIMARSConfig, arfima_rs_forecast

forecast_credit = arfima_rs_forecast(
    credit_history,
    horizons=(4, 8, 12),
    n_samples=500,
    config=ARFIMARSConfig(n_regimes=2, switching_variance=True),
)
```

## Implémentation BC pratique

### Pipeline standard à 3 horizons

```python
def bc_forecasting_pipeline(history, current_quarter):
    """Produit des forecasts à 3 horizons distincts pour usage BC.

    Returns:
        dict avec keys "nowcast", "policy_horizon", "long_horizon".
    """
    # Nowcast : horizon 0-3 trimestres
    nowcast = har_forecast(
        history,
        horizons=(1, 2, 3),
        n_samples=500,
        lag_config=HARLagConfig(1, 2, 4),
    )

    # Policy horizon : 4-8 trimestres (test des 2 modèles)
    policy_msm = msm_forecast(history, horizons=(4, 6, 8))
    policy_har = har_forecast(history, horizons=(4, 6, 8))
    # Sélection par BIC in-sample : voir documentation ci-dessous

    # Long horizon : 12-20 trimestres
    long_horizon = msm_forecast(
        history,
        horizons=(12, 16, 20),
        n_samples=500,
    )

    return {
        "nowcast": nowcast,
        "policy_horizon": ...,  # combinaison
        "long_horizon": long_horizon,
    }
```

### Sélection par BIC pour la zone de transition

Pour la zone h = 4-8, calculer le BIC in-sample des deux modèles
candidats et choisir le plus bas :

```python
def select_by_bic(history, candidate_models):
    """Sélectionne le meilleur modèle par BIC in-sample."""
    bics = {}
    for name, fit_fn in candidate_models.items():
        # Fitter le modèle, extraire log-likelihood
        log_lik = fit_fn(history).metadata.get("log_likelihood", None)
        if log_lik is None:
            continue
        # BIC = -2 log_lik + k log(n)
        n = len(history)
        k = fit_fn(history).metadata.get("n_parameters", None)
        if k is None:
            continue
        bics[name] = -2 * log_lik + k * np.log(n)
    return min(bics, key=bics.get) if bics else None
```

(Note : actuellement nos modèles n'exposent pas tous `log_likelihood`
et `n_parameters` directement — c'est une extension Roadmap.
Voir [extensions roadmap](../quants/extensions_roadmap.md).)

## Conséquences théoriques

Le fait que **différents modèles dominent à différents horizons** a
des implications théoriques importantes pour la BC :

1. **Pas de modèle unique optimal**. La calibration d'un modèle DSGE
   "tout-horizon" est sous-optimale. Cela contraste avec la pratique
   institutionnelle dominante.

2. **Tradeoff entre interprétabilité et précision**. HAR est plus
   interprétable (3 coefficients lag clair) ; MSM est plus précis aux
   long horizons mais difficilement interprétable (4 paramètres
   abstraits de cascade). Le choix dépend de l'usage : MPC
   communication → HAR ; modélisation interne → MSM.

3. **Coût de la calibration multi-horizon**. Maintenir 2-3 modèles en
   production a un coût opérationnel. Tradeoff avec le bénéfice
   prédictif estimé empiriquement à ~30 % de réduction de CRPS sur
   les variables où le cluster gagne.

## Limites et précautions

- **Pas de causalité structurelle**. Les modèles statistiques (HAR,
  MSM, ARFIMA+RS) ne fournissent pas de mécanisme causal. Pour
  l'analyse "what-if" politique, ils doivent être combinés avec un
  modèle structurel.
- **Pas de prise en compte des chocs exogènes**. Aucun de ces modèles
  ne conditionne sur les politiques fiscale, monétaire annoncée,
  ou réglementaire. C'est une extension significative — voir
  [extensions roadmap](../quants/extensions_roadmap.md).
- **Calibration in-sample**. Le choix HAR vs MSM en zone de
  transition par BIC in-sample peut sur-fitter. Validation
  out-of-sample recommandée (cross-validation par rolling-origin).
- **Disponibilité des données long-historique**. MSM bénéficie
  significativement d'historiques longs (≥ 100 observations). Pour
  une BC nouvellement créée ou une nouvelle juridiction, MSM peut
  être instable.

## Pour aller plus loin

### Méthode

- [Catalogue des modèles](../quants/models_catalog.md) — specs précises
- [Benchmark reproductible](../quants/benchmark_reproducible.md) — comment
  reproduire le verdict PASS 78 %
- [Failure modes](../quants/failure_modes.md) — où les modèles échouent

### Contexte BC

- [Méthode pour praticiens](method_for_practitioners.md) — interpréter
  la méthode CPV depuis un point de vue BC
- [Credibility radar](credibility_radar.md) — utiliser `d` pour
  mesurer la crédibilité

### Théorie

- Calvet-Fisher 2008. *Multifractal Volatility : Theory, Forecasting,
  and Pricing*.
- Corsi, F. 2009. A simple approximate long-memory model of realized
  volatility. *Journal of Financial Econometrics*.
- Bhardwaj-Swanson 2006. An empirical investigation of the usefulness
  of ARFIMA models for predicting macroeconomic and financial time
  series. *Journal of Econometrics*.
