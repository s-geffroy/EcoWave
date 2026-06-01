# Credibility radar

!!! success "TL;DR"

    **Une banque centrale crédible a une inflation faiblement persistante** : les chocs s'éteignent vite parce que les agents n'anticipent pas une dérive de la cible. Cette persistance est exactement le paramètre `d` GPH. Interprétation : `d < 0.10` crédible, `d > 0.40` crise. Implémentation : une ligne Python, ~milliseconde. Volcker 1979 → `d` chute de 0.40 à 0.10 ; Brexit/COVID 2016-22 → `d` remonte. Mesure directe sans dépendance aux enquêtes.

## Dans cette page

- **[L'intuition](#intuition)** — pourquoi `d` mesure la crédibilité
- **[La formalisation GPH](#formalisation)** — équation et code
- **[Comment l'utiliser opérationnellement](#usage)**
- **[Lecture historique](#historique)** — Volcker, Brexit, COVID
- **[Comparaison cross-pays](#cross-pays)** — tableau indicatif
- **[Comment ça complète vos indicateurs existants](#complement)**
- **[Limites à connaître](#limites)**
- **[Étapes pour intégrer dans votre pipeline BC](#integration)**

---

## L'intuition { #intuition }

Une banque centrale **crédible** est celle dont les acteurs
économiques *croient* la cible d'inflation, sans attendre la preuve
empirique à chaque période. Concrètement : si la BC annonce 2 % et que
les agents intègrent cela rapidement dans leurs anticipations, alors
les chocs d'inflation transitoires **ne se propagent pas** dans le
système — ils s'éteignent vite.

À l'inverse, une banque centrale **non-crédible** : les chocs
d'inflation persistent, parce que les agents intègrent dans leurs
anticipations courantes une trajectoire qui dérive de la cible. Un choc
positif aujourd'hui se traduit par anticipations plus hautes demain,
qui contribuent à l'inflation effective de demain, qui renforcent les
anticipations d'après-demain, etc.

**Cette persistance des chocs d'inflation est exactement le paramètre
de longue mémoire** `d` du modèle ARFIMA — au sens GPH (Geweke-Porter-
Hudak 1983) ou via l'estimateur local-Whittle.

- `d` proche de **0** : pas de longue mémoire, chocs s'éteignent vite,
  BC crédible.
- `d` entre **0.1 et 0.3** : longue mémoire modérée, crédibilité
  intermédiaire.
- `d` supérieur à **0.4** : longue mémoire forte, chocs très
  persistants, crédibilité faible.
- `d` proche de **0.5** : frontière non-stationnarité, BC en perte
  totale de crédibilité.

## La formalisation

L'estimateur GPH régresse le logarithme du périodogramme sur le
logarithme de la fréquence pour les basses fréquences :

$$
\log I(\lambda_j) = c - d \cdot \log\!\left(4 \sin^2(\lambda_j / 2)\right) + \varepsilon_j
$$

pour `j = 1, …, m` où `m = T^{0.5}` (bandwidth Geweke-Porter-Hudak
original) ou `m = T^{0.8}` (plus efficient, parfois biaisé près des
bords).

- `T` : longueur de la série (typiquement 200-600 mois pour
  l'inflation moderne).
- `I(λ_j)` : périodogramme à la fréquence `λ_j = 2π j / T`.
- `d` : paramètre à estimer.

Implémentation : `gph_estimate_d(series, bandwidth_exponent=0.5)` dans
[`fractional.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/fractional.py).
Clipping automatique à `[-0.499, 0.499]` pour rester dans la zone de
stationnarité.

## Comment l'utiliser opérationnellement

### Implémentation minimale

```python
import numpy as np
from ecowave.forecasting.fractional import gph_estimate_d

# Votre série d'inflation, mensuelle, déjà désaisonnalisée
inflation_monthly = np.array([...])  # T observations

d_estimated = gph_estimate_d(inflation_monthly, bandwidth_exponent=0.5)
print(f"d = {d_estimated:.3f}")
```

Sortie typique pour une BC à cible 2 % crédible :

```
d = 0.085
```

Sortie typique pour une économie en perte de crédibilité :

```
d = 0.412
```

### Lecture historique

Le pouvoir interprétatif de `d` vient de sa capacité à montrer des
**ruptures de crédibilité** historiques :

- **États-Unis pré-Volcker (1965-1979)** : `d ≈ 0.4` sur l'inflation
  CPI. Période d'ancrage faible des anticipations.
- **États-Unis post-Volcker (1985-2007)** : `d ≈ 0.1`. Volcker a
  *cassé* la persistance par un régime monétaire restrictif inattendu
  — c'est l'opérationnalisation empirique d'une rupture de régime
  cognitif (famille S du cluster CPV).
- **États-Unis post-2008 (2009-2019)** : `d ≈ 0.05-0.1`. ZIRP + QE
  produisent une inflation très faiblement persistante (inflation
  basse pas par sécurité mais par compression structurelle).
- **États-Unis 2021-2022 (post-COVID)** : `d` remonte à ~0.25 — choc
  persistant, anticipations mises à l'épreuve.
- **Royaume-Uni post-Brexit (2016+)** : `d` augmente
  significativement. Crédibilité érodée par tensions politiques.
- **Turquie depuis 2018** : `d > 0.4`. Crise de crédibilité aiguë.
- **Zone euro stable** : `d ≈ 0.1` sur la période 2003-2020.

### Calibration recommandée

Pour utilisation opérationnelle en BC :

| Paramètre | Recommandation |
|---|---|
| Fréquence | Mensuelle (la plus courante pour CPI ; trimestrielle si seule disponible) |
| Désaisonnalisation | Indispensable (X-13 ARIMA-SEATS ou Tramo-Seats) |
| Longueur série | Minimum 60 observations (5 ans mensuels) ; 120+ idéal |
| Bandwidth | `0.5` Geweke-Porter-Hudak original ; `0.6` un peu plus efficient |
| Fenêtre glissante | 5-10 ans pour suivre l'évolution dans le temps |

### Suivi dans le temps

L'utilisation la plus puissante est en **fenêtre glissante** : calculer
`d` sur les `T_{window}` derniers mois, à chaque période. La série
chronologique `d_t` montre l'évolution de la crédibilité.

```python
def rolling_d_credibility(inflation_series, window_months=120):
    """Calcule d en fenêtre glissante de window_months mois."""
    d_series = []
    for t in range(window_months, len(inflation_series)):
        d_t = gph_estimate_d(
            inflation_series[t - window_months : t],
            bandwidth_exponent=0.5,
        )
        d_series.append(d_t)
    return np.array(d_series)
```

Un *régime drift* dans `d_t` (montée brutale) signale une crise de
crédibilité émergente. C'est complémentaire de l'EWS détaillé dans
[tipping point detection](tipping_point_detection.md).

## Comparaison cross-pays

Tableau indicatif basé sur les données disponibles sur les panels CPV
(notre estimation, à reproduire sur vos données internes BC) :

| Pays / Zone | Période | `d` estimé indicatif | Interprétation |
|---|---|---|---|
| États-Unis | 1965-1979 | ~0.40 | Crédibilité pré-Volcker faible |
| États-Unis | 1985-2007 | ~0.10 | Anchored expectations |
| États-Unis | 2009-2019 | ~0.08 | ZIRP + faible inflation |
| États-Unis | 2021-2024 | ~0.25 | Recovery de crédibilité après choc COVID |
| Royaume-Uni | 1993-2016 | ~0.12 | Inflation targeting stable |
| Royaume-Uni | 2016-2024 | ~0.20 | Brexit + COVID, érosion partielle |
| Zone euro | 2003-2020 | ~0.10 | BCE stable |
| Japon | 1995-2020 | ~0.05 | Déflation persistante (cas limite) |
| Turquie | 2018-2024 | ~0.45 | Crise de crédibilité aiguë |
| Argentine | 2015-2024 | > 0.5 | Hors zone de stationnarité |

**Avertissement** : ces valeurs sont **indicatives**. Pour publication
ou décision politique, recalculer avec vos données internes,
désaisonnalisées avec votre méthode standard, et avec une bandwidth
choisie après sensibility analysis.

## Comment cela complète vos indicateurs existants

Les BC utilisent déjà plusieurs proxies de crédibilité :

| Indicateur classique | Avantage | Limite |
|---|---|---|
| Anticipations d'inflation (enquêtes consommateurs/professionnels) | Direct, capture les croyances | Bruité, lent, biais cognitifs |
| Break-even rates (obligations indexées) | Marché-based, daily | Distorsion liquidité, prime de risque |
| Écart à la cible | Simple | Pas de notion de persistance |
| Dispersion des anticipations | Capture l'incertitude | Sépare mal cible vs persistance |

L'indicateur `d` GPH apporte :

- **Une mesure unique synthétique** de la persistance — qui est
  *exactement* le problème quand on parle d'ancrage des
  anticipations.
- **Indépendance des enquêtes** : mesurable directement sur la série
  CPI sans recours à des données d'enquête potentiellement biaisées.
- **Comparabilité cross-pays** stricte : `d` a la même définition
  partout, pas de problèmes de formulation des questions ou de
  méthodologie d'enquête.
- **Lecture historique falsifiable** : un break dans `d_t` signale
  une rupture de régime, validable par les événements historiques
  (Volcker 1979, Brexit 2016, COVID 2020).

## Limites à connaître

Le `d` GPH n'est pas magique :

- **Sensibilité à la bandwidth** : `m = T^{0.5}` vs `m = T^{0.8}`
  peuvent donner des `d` différents. Reporter les intervalles.
- **Sensibilité aux outliers** : un choc transitoire massif (COVID
  spike) peut biaiser `d`. Robuster avec winsorisation ou estimateur
  local-Whittle robuste.
- **Identification faible sur séries courtes** : `T < 100`, `d` est
  fortement biaisé. Utiliser intervalles plus larges si nécessaire.
- **Pas de structure causale** : `d` mesure une propriété statistique,
  pas un mécanisme. Cela complète, ne remplace pas, les modèles
  structurels DSGE.

## Étapes pour intégrer dans votre pipeline BC

1. **Pilote** (1-2 semaines) : calculer `d` sur votre série d'inflation
   nationale en historique (post-1995 typiquement). Comparer à votre
   diagnostic interne de crédibilité. Sanity check.
2. **Reproduire les patterns historiques** : appliquer la fenêtre
   glissante sur 1965-2024 (ou ce qui est disponible). Détectez-vous
   Volcker 1979, Greenspan 2001-2003, GFC 2008, COVID 2020 ?
3. **Calibrer les seuils** : à partir de quelle valeur de `d`
   considère-t-on une perte de crédibilité préoccupante ? Recommandé :
   `d > 0.30` est un signal d'alerte ; `d > 0.40` est une crise.
4. **Intégrer au dashboard** : ajouter `d_t` mensuel au dashboard
   chief economist / governor. Calculer pour les 4-5 pairs principaux
   pour comparaison.
5. **Documentation interne** : produire une note d'interprétation pour
   le comité de politique monétaire — quoi suivre, quand alerter.

## Ressources techniques

- Code : `gph_estimate_d` dans
  [`ecowave/forecasting/fractional.py`](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/fractional.py)
- Tests : `tests/test_forecasting_fractional.py` (9 tests passants
  validant l'estimateur sur ARFIMA simulé)
- Référence académique : Geweke-Porter-Hudak 1983 *J. Time Series
  Analysis* ; révision moderne dans Beran 1994 *Statistics for Long-
  Memory Processes*.
- Application macroéconomique : "Shades of inflation targeting:
  insights from fractional integration" — *Macroeconomic Dynamics*
  ([Cambridge](https://www.cambridge.org/core/journals/macroeconomic-dynamics/article/shades-of-inflation-targeting-insights-from-fractional-integration/CCE94E57396616BA7C621EDF3D73B66B)).
- Reproduction sur nos données : lancer
  `ecowave forecast-benchmark --horizon-data q --models arfima_rs`
  et inspecter `cells[i].mean_crps` + `d_estimated` dans la
  métadonnée de chaque cellule.

---

*Voir aussi :* [forward guidance réflexif](forward_guidance_reflexive.md),
[tipping point detection](tipping_point_detection.md),
[horizon-aware targeting](horizon_aware_targeting.md).
