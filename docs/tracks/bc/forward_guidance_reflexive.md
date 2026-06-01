# Forward guidance comme acte réflexif

> *Pourquoi la communication d'une banque centrale change le régime
> cognitif dans lequel les agents anticipent — et comment le modéliser
> formellement via la famille S du cluster CPV.*

## Le problème conceptuel

Dans la théorie standard des anticipations rationnelles, les agents
économiques :

1. Connaissent le modèle "vrai" du système.
2. Calculent la trajectoire d'équilibre intertemporelle.
3. Intègrent les annonces de politique monétaire comme **information
   neutre** : "la BC dit X, j'ajuste mon estimation conditionnellement
   à X selon Bayes".

C'est la base de la calibration des modèles New-Keynesian DSGE depuis
Smets-Wouters 2003 : le forward guidance est censé fonctionner parce
que les agents intègrent l'annonce dans leur calcul d'optimisation
contraint.

Mais cette image suppose que les agents connaissent le **vrai** modèle.
Quand ils ne le connaissent pas — ce qui est plus réaliste — les
annonces ne sont pas seulement de l'information : elles **changent le
modèle même** que les agents utilisent pour interpréter le système.

C'est ce que George Soros appelle la **réflexivité** : *"the
participants' thinking affects the situation to which it relates."*
Le système économique n'est pas extérieur aux croyances sur lui ; il
est **partiellement constitué** par elles.

## La formalisation statistique : régime drift S

Le cluster CPV contient une famille **S** (Reflexive regime drift)
détectée par un test de Kolmogorov-Smirnov appliqué sur des fenêtres
glissantes des statistiques d'ordre supérieur (moments 3 et 4 de la
série).

Concrètement, le test compare la distribution empirique des
fluctuations sur la première moitié d'une fenêtre roulante à celle de
la seconde moitié. Quand le KS rejette l'hypothèse de même
distribution, on a détecté un **régime change** statistique.

Empiriquement, sur les données macro 1960-2024, les ruptures détectées
par ce test correspondent souvent à :

- **Volcker 1979-82** : changement de régime monétaire brutal,
  premier choc des anticipations
- **Black Monday 1987** : choc financier majeur
- **Greenspan put 1998-2003** : émergence de la "BCE put" — les agents
  commencent à anticiper que la BC les sauvera
- **GFC 2008** : effondrement de la confiance + intervention massive
  des BC
- **Whatever it takes Draghi 2012** : régime change BCE
- **COVID 2020 + Powell pivot** : changement de régime monétaire et
  budgétaire combiné
- **Inflation 2021-2022** : test de la crédibilité post-pandémique

Toutes ces ruptures correspondent à des **moments où la communication
de la BC a fondamentalement changé le cadre cognitif** dans lequel les
acteurs interprétaient le système.

## Trois canaux par lesquels le forward guidance change le régime

### Canal 1 — Changement de la fonction de réaction perçue

Quand la BC annonce explicitement un changement de stratégie (par
exemple "average inflation targeting" Fed 2020 ou "whatever it takes"
BCE 2012), elle modifie le modèle que les agents utilisent.

**Modélisation S** : le test KS détecte une rupture après l'annonce.
Avant l'annonce, les chocs avaient une certaine distribution
conditionnelle ; après, la distribution change parce que les agents
réinterprètent les chocs futurs à travers la nouvelle fonction de
réaction.

**Calibration empirique** : la latence typique entre l'annonce et la
détection du break par KS varie selon la séquence du choc. Pour
Volcker 1979, la rupture est détectable dans les 3-6 mois. Pour
Draghi 2012, la rupture est quasi-instantanée (1 mois).

### Canal 2 — Coordination des anticipations

Le forward guidance est un acte **performatif** : il fournit un point
focal autour duquel les anticipations hétérogènes se synchronisent.

Avant l'annonce : les anticipations sont distribuées de façon large
(forte dispersion).

Après l'annonce : les anticipations convergent vers le point focal
proposé (faible dispersion).

**Modélisation S** : le moment 2 (variance) de la distribution des
anticipations chute. Ce changement de moment est exactement ce que le
KS détecte.

### Canal 3 — Changement des contraintes effectives

L'annonce d'un nouveau régime monétaire (par exemple QE post-2009)
modifie les contraintes effectives auxquelles les agents pensent être
soumis. Les firmes financières réévaluent leur stratégie en fonction
de la nouvelle régulation perçue.

**Modélisation S** : les moments d'ordre 3 et 4 (skewness, kurtosis)
de la distribution des fluctuations changent. Le KS détecte la rupture
parce que la **forme** des chocs s'est modifiée, pas seulement
l'amplitude.

## Implications pratiques pour la communication BC

### 1. Reconnaître l'effet performatif

Une annonce BC n'est pas une *prévision* d'évolution future, c'est un
**acte qui contribue à façonner cette évolution**. Cela n'est pas une
limite, c'est un outil — mais il faut le reconnaître pour le calibrer.

Implication : la calibration du forward guidance ne peut pas se faire
en supposant que les agents reçoivent passivement l'information. Il
faut un modèle du *feedback* — où l'annonce, en changeant le modèle
des agents, change l'équilibre que la BC cherche à atteindre.

### 2. Mesurer le coût en crédibilité d'une annonce ratée

Quand l'annonce ne se réalise pas (par exemple "transitory inflation"
2021 qui s'est avérée non-transitoire), le système retourne à un
régime cognitif plus sceptique. Ce coût est quantifiable :

- Le paramètre `d` de longue mémoire ([credibility radar](credibility_radar.md))
  remonte.
- Le test KS détecte une rupture inversée — du régime "ancré" vers le
  régime "non-ancré".

Empiriquement, on observe ces remontées de `d` chez la Fed en 2021-22
et chez la BoE post-Brexit + COVID.

### 3. Échelonner les annonces dans le temps

Si une annonce trop ambitieuse risque de ne pas être tenue (et donc
de coûter en crédibilité), il vaut mieux annoncer **plus modestement**
mais tenir, que **plus ambitieusement** et rater.

Cette logique est connue intuitivement chez les praticiens BC, mais
notre cadre permet de la **quantifier** : le coût `Δd` d'une annonce
ratée vs le bénéfice `Δd` d'une annonce tenue se mesurent
identiquement.

### 4. Coordonner avec d'autres autorités

Si une annonce BC est suivie peu après d'une annonce contradictoire
de l'autorité budgétaire ou réglementaire, le régime cognitif des
agents subit deux chocs successifs. Le KS détecte alors deux ruptures
rapprochées, ce qui désancre profondément.

Implication : la coordination inter-autorités est mesurable
empiriquement par le nombre et le timing des ruptures détectées par S.

## Implémentation pratique

Le test KS sliding-window n'est pas (encore) dans l'API publique
`ecowave.forecasting`. Mais une implémentation minimale est triviale :

```python
import numpy as np
from scipy.stats import ks_2samp

def detect_regime_shifts(series, window_months=60, min_gap_months=12):
    """Détecte les ruptures de régime via KS sliding window.

    Retourne les indices `t` où le test KS rejette H0 avec p < 0.01
    entre la fenêtre `[t-window:t]` et `[t:t+window]`.
    """
    breaks = []
    last_break = -np.inf
    for t in range(window_months, len(series) - window_months):
        if t - last_break < min_gap_months:
            continue
        before = series[t - window_months : t]
        after = series[t : t + window_months]
        statistic, p_value = ks_2samp(before, after)
        if p_value < 0.01:
            breaks.append((t, p_value))
            last_break = t
    return breaks
```

Cette implémentation peut être ajoutée à votre pipeline de monitoring
BC pour détecter en temps quasi-réel les changements de régime.

## Limites conceptuelles

Le cadre réflexif a des limites qu'il faut reconnaître :

- **Pas de prédiction structurelle** : on ne peut pas prédire
  *quel* régime apparaîtra. Le test S détecte les ruptures
  rétrospectivement (avec un décalage), mais ne dit pas vers quoi le
  système bascule.
- **Sensibilité à la fenêtre** : `window_months` est un paramètre
  libre. Trop court (< 24) = bruit ; trop long (> 120) = perte de
  réactivité.
- **Compatibilité limitée avec DSGE** : le cadre réflexif est
  difficile à intégrer dans les modèles DSGE standard sans
  modification structurelle (voir la critique DSGE dans le
  [track académique](../acad/index.md)).
- **Pas de fonctionnement universel** : pour les régimes monétaires
  très stables (Japon 1995-2020), peu de ruptures détectées car peu
  de variations à exploiter.

## Pour aller plus loin

### Théorie

- Soros, G. (2013). *Fallibility, reflexivity, and the human
  uncertainty principle*. Journal of Economic Methodology.
- Lo, A. (2017). *Adaptive Markets : Financial Evolution at the Speed
  of Thought*. Princeton.
- Friston, K. (2010). The free-energy principle: a unified brain
  theory? *Nature Reviews Neuroscience*. (Application macro encore
  émergente, mais cadre proche.)

### Pratique

- [Tipping point detection](tipping_point_detection.md) — extension
  EWS du même test S, calibrée pour usage opérationnel BC
- [Credibility radar](credibility_radar.md) — indicateur `d` de
  longue mémoire qui mesure quantitativement la persistance/sapance
  de crédibilité
- [Horizon-aware targeting](horizon_aware_targeting.md) — comment
  choisir le modèle selon l'horizon de politique monétaire

### Méthode

- [3 portes de falsifiabilité](../../methodology/trois_portes.md)
- [Méthode pour praticiens](method_for_practitioners.md)
