# Synthèse AMH — Friston + MRW + AMH comme méta-cadre

> *Trois candidats pour la synthèse théorique manquante. Aucun n'unifie
> seul les 5 piliers C+B+D+I+S, mais leur combinaison esquisse un
> cadre potentiel à formaliser.*

## Le problème théorique

Le cluster empirique C+B+D+I+S est stable et reproductible. Il
n'existe **aucun cadre théorique unique** qui le prédise à partir de
premiers principes. C'est la question théorique ouverte que CPV
laisse ouverte.

Plus précisément : on cherche un cadre qui prédise *conjointement* :

- **C** — la longue mémoire (`d` > 0 sur 85 % des cellules)
- **B** — la multifractalité (singularity spectrum non-trivial sur
  70 %)
- **D** — la non-linéarité (BDS reject sur 75 %)
- **I** — l'information structurée (entropies réduites sur 80 %)
- **S** — la dérive de régime cognitif (KS sliding-window reject sur
  60 %)

Trois candidats théoriques se présentent. Aucun ne couvre seul les 5
piliers, mais leur **combinaison** esquisse un méta-cadre.

## Candidat 1 — Adaptive Markets Hypothesis (Lo)

**Référence** : Lo, A. (2017). *Adaptive Markets: Financial Evolution
at the Speed of Thought*. Princeton.

### L'idée centrale

Les marchés financiers (et par extension la macroéconomie) sont des
**écosystèmes évolutifs** dans lesquels les agents apprennent,
s'adaptent et survivent selon leurs performances. L'efficience
"néoclassique" (Fama 1970) est un cas limite particulier qui
n'apparaît que sous des conditions très contraintes (population
stable d'agents homogènes rationnels avec information complète).

Dans le cas général, on observe :

- **Hétérogénéité** des stratégies (B émerge par agrégation)
- **Cycles évolutifs** de strategies dominantes / dominées (S émerge
  comme drift de régime)
- **Bornes rationnelles** par contraintes cognitives (I — information
  exploitable)
- **Memoire institutionnelle** longue (C par agrégation
  d'apprentissages)

### Couverture des 5 piliers

- **C** ✓ (par agrégation de mémoires hétérogènes)
- **B** ✓ (par agrégation de stratégies hétérogènes)
- **D** partiel (non explicite)
- **I** ✓ (par contraintes cognitives et apprentissage)
- **S** ✓ (par évolution des stratégies dominantes)

**4/5 piliers couverts**. C'est le meilleur cadre conceptuel
unificateur.

### Limites

1. **Non-quantifiable directement**. AMH est un cadre métathéorique,
   pas un modèle calibrable. Il n'a pas de spécification
   mathématique unifiée.
2. **Identification empirique difficile**. Vérifier que les marchés
   sont "adaptatifs" demande des séries longues et beaucoup de
   bruit dans les conclusions.
3. **Coverage incomplète de D**. La non-linéarité explicite n'est
   pas dérivée des premiers principes AMH.

### Pour aller plus loin

Hommes-Lo 2024 ("Adaptive Markets Hypothesis") dans le *Oxford
Handbook* récapitule l'état de la littérature. Les modèles HABM
(Heterogeneous Agent-Based Models) sont l'implémentation
opérationnelle d'AMH.

## Candidat 2 — Free-Energy Principle (Friston)

**Référence** : Friston, K. (2010). The free-energy principle: a
unified brain theory? *Nature Reviews Neuroscience*.

### L'idée centrale

Tout système qui maintient sa cohérence dans un environnement
incertain **minimise la free-energy variationnelle** entre son modèle
interne du monde et les observations qu'il fait. Cela conduit à une
mise à jour bayésienne *active* (active inference) des croyances.

Appliqué à la macroéconomie : les agents économiques agissent comme
des estimateurs bayésiens contraints par leur capacité computationnelle.
Quand l'environnement change (par exemple Volcker shock), leur
modèle interne du système doit se mettre à jour — d'où les ruptures
S détectées empiriquement.

### Couverture des 5 piliers

- **C** partiel (par persistance des croyances bayésiennes)
- **B** non-explicite
- **D** ✓ (par non-linéarité de la mise à jour bayésienne)
- **I** ✓✓ (centralité de l'information dans le free-energy)
- **S** ✓✓ (formalisation directe via active inference)

**~3/5 piliers couverts** mais avec une formalisation
mathématique forte.

### Limites

1. **Application macro encore émergente**. Le free-energy a été
   développé en neurosciences. Son application à l'économie est
   embryonnaire (quelques papers depuis 2020).
2. **Difficile à calibrer**. Le free-energy variationnel n'a pas
   d'estimation standard sur des séries économiques.
3. **Pas de couverture explicite de B et C**. La multifractalité et
   la longue mémoire ne sont pas dérivées de Friston.

### Pour aller plus loin

Les applications macro de Friston sont encore rares. Les
contributions récentes : Friston-Costa-Stephan 2024 ("Active
inference and economics"), Hosokawa 2023 ("Free energy economics").

## Candidat 3 — Multifractal Random Walk (MRW)

**Référence** : Bacry, E., Muzy, J.-F., Delour, J. (2001).
Multifractal Random Walk. *Physical Review E*.

### L'idée centrale

Un processus log-normal multifractal défini par
`X_t = ∫_0^t W(s) dB(s)` où `B` est un mouvement brownien et `W` est
une variance log-multifractale avec auto-correlation logarithmique.
Reproduit naturellement :

- Multifractalité du processus
- Longue mémoire en magnitudes (mais pas en signe)
- Queues lourdes
- Échelle universelle du type Kolmogorov K41

### Couverture des 5 piliers

- **C** ✓ (longue mémoire dans la magnitude)
- **B** ✓✓ (multifractalité par construction)
- **D** non-explicite (le log-MRW est presque linéaire)
- **I** non-explicite
- **S** non-explicite (MRW est stationnaire par construction)

**~2/5 piliers couverts** mais avec une formalisation
mathématique extrêmement précise pour les 2 piliers couverts.

### Limites

1. **Non-stationnaire dans la réalité**. MRW suppose une stationnarité
   que les séries macro réelles n'ont pas (à cause de S).
2. **Pas de S explicite**. La dérive de régime cognitif n'est pas
   intégrée au cadre.
3. **Calibration coûteuse**. MRW demande des séries très longues pour
   identifier les paramètres `λ²`, `T`, `σ²`.

### Pour aller plus loin

Le MRW reste un cadre canonique pour la multifractalité financière.
Sa généralisation à la macroéconomie est ouverte.

## Synthèse : un cadre potentiel non-encore-formalisé

En combinant les trois cadres, on obtient un méta-cadre potentiel
qui couvre les 5 piliers :

| Pilier | Cadre dominant pour ce pilier | Cadre secondaire |
|---|---|---|
| C — Longue mémoire | MRW (formalisation) | AMH (interprétation) |
| B — Multifractalité | MRW (formalisation) | AMH (mécanisme) |
| D — Non-linéarité | Friston (active inference) | - |
| I — Information structurée | Friston (centralité free-energy) | AMH (apprentissage) |
| S — Régime drift | Friston (active inference) | AMH (évolution stratégies) |

### La synthèse à construire

Un méta-cadre unifié devrait :

1. **Hériter de MRW** pour la couche statistique fractale (C+B).
2. **Hériter de Friston** pour la couche cognitive bayésienne (D+I+S).
3. **Hériter d'AMH** pour le cadre conceptuel évolutif global.

Concrètement, cela pourrait prendre la forme d'un :

**MRW étendu à régimes de free-energy** — un processus log-normal
multifractal dont les paramètres (cascade exponent `λ²`, time
correlation `T`) sont **conditionnellement Markoviens** au régime
cognitif `s_t` qui suit une dynamique d'active inference.

Cela n'a (à notre connaissance) **jamais été formalisé**. C'est un
programme de recherche ouvert.

## Pourquoi cette synthèse vaut la peine

Si elle aboutit, une telle synthèse :

1. **Unifie** 5 propriétés statistiques empiriquement co-occurrentes
   à partir de premiers principes.
2. **Prédit** des relations entre ces propriétés (par exemple : la
   longue mémoire C devrait être plus forte quand le régime cognitif
   est stable et plus faible pendant les transitions).
3. **Fournit** un cadre calibrable opérationnellement (à la
   différence d'AMH seul).
4. **Tend** des ponts entre macroéconomie, finance quantitative et
   neurosciences cognitives — domaines qui partagent désormais des
   méthodologies communes.

### Programme de recherche

Une thèse doctorale ambitieuse pourrait formaliser :

- Une dérivation de MRW à partir de principes d'active inference sur
  des populations d'agents.
- Une caractérisation du régime cognitif `s_t` comme état de
  croyance aggregé.
- Une calibration empirique sur les panels CPV existants.
- Une validation prédictive (comparaison out-of-sample avec MSM,
  ARFIMA+RS).

Effort estimé : 3-5 ans pour une équipe doctorale + supervisor de
qualité.

## Pour aller plus loin

### Théorie principale

- Lo, A. (2017). *Adaptive Markets : Financial Evolution at the
  Speed of Thought*. Princeton.
- Friston, K. (2010). The free-energy principle: a unified brain
  theory? *Nature Reviews Neuroscience* 11(2): 127–138.
- Bacry, E., Muzy, J.-F., Delour, J. (2001). Multifractal Random
  Walk. *Physical Review E* 64: 026103.

### Applications convergentes

- Hommes-Lo 2024. Adaptive Markets Hypothesis. *Oxford Handbook*.
- Bouchaud-Potters 2003. *Theory of Financial Risk and Derivative
  Pricing*. Cambridge.
- Mandelbrot 1997. *Fractals and Scaling in Finance*. Springer.

### Cadres alternatifs non-couverts ici

- **Behavioral economics** (Kahneman-Tversky) — couvre I+S
  partiellement mais pas C+B.
- **Complexity economics** (Arthur, Beinhocker) — méta-cadre
  conceptuel proche d'AMH.
- **Heterogeneous Agent Models** (Lux-Marchesi 1999, Brock-Hommes
  1998) — implémentations de cadres adaptatifs.

### Code

- `ecowave.forecasting.msm` — MSM cascade multifractale (proche MRW
  discret)
- `ecowave.forecasting.arfima_rs` — ARFIMA + Markov regime-switching
- `ecowave.forecasting.extensions_roadmap.md` — HABM, MRW continu,
  active inference comme chantiers futurs (voir
  [extensions roadmap](../quants/extensions_roadmap.md))

### Connexes

- [DSGE en accusation](dsge_in_dock.md) — pourquoi les cadres
  DSGE-naïfs ne couvrent pas le cluster
- [5 prédictions falsifiables](falsifiable_predictions.md) — tests à
  mener pour avancer le programme de recherche
- [Paper V2 académique](paper_v2_academic.md) — synthèse complète
