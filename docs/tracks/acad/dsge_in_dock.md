# DSGE en accusation

> *Trois modifications structurelles requises pour rendre les
> modèles New-Keynesian DSGE compatibles avec la signature empirique
> C+B+D+I+S. Pourquoi ces modifications ne sont pas optionnelles, et
> pourquoi DSGE n'est cependant pas mort.*

## Les trois hypothèses statistiques en cause

Le DSGE New-Keynesian moderne (Smets-Wouters 2003 → SW07 → SAM ECB
→ FRB/US → COMPASS BoE → similar at most major central banks) repose
sur trois hypothèses statistiques que la signature CPV réfute :

### Hypothèse 1 — Chocs AR(1) ou IID

**Formulation standard** : les chocs exogènes (technologie,
préférences, monétaire, fiscaux) suivent typiquement
`ε_t = ρ ε_{t-1} + η_t`, η_t i.i.d. normal avec persistance ρ ∈ [0.6,
0.9].

**Verdict CPV** : ce modèle suppose une autocorrelation **exponentiellement
décroissante** : `Corr(ε_t, ε_{t+k}) = ρ^k`. Or sur les séries macro
réelles, l'autocorrelation décroît **polynomialement** (long memory) :
`Corr(ε_t, ε_{t+k}) ~ k^{-α}` avec `α ∈ (0, 1)`. Le paramètre `d` GPH
appliqué aux résidus typiques de modèles DSGE atteint 0.15-0.30,
significativement positif.

**Conséquence pratique** : un DSGE qui calibre ρ ≈ 0.7 sous-estime la
persistance des chocs sur horizons longs (8+ trimestres). Cela explique
en partie pourquoi les forecasts DSGE sous-performent random walk
au-delà de 3-4 trimestres (Atkeson-Ohanian 2001 pour l'inflation,
Stock-Watson 2003 pour le PIB).

**Modification requise** : remplacer AR(1) par ARFIMA(0, d, 0) ou
ARFIMA(p, d, q) :

$$
(1 - L)^d \varepsilon_t = \eta_t
$$

avec `d` estimé empiriquement (typiquement 0.15-0.35 selon la
variable). L'extension ne fait pas exploser la dimension du modèle —
elle ajoute un seul paramètre par choc.

Implémentations disponibles : voir `ecowave.forecasting.arfima_rs` et
les références Bhardwaj-Swanson 2006, Hosking 1981.

### Hypothèse 2 — Paramètres "deep" stables

**Formulation standard** : les paramètres structurels (préférences,
technologie, friction) sont **invariants au cours du temps**. Le DSGE
calibre une fois (typiquement sur la période complète disponible) et
projette en utilisant ces paramètres comme constants.

**Verdict CPV** : la famille S (Reflexive regime drift) détecte des
ruptures empiriques significatives à des dates historiquement
identifiables :

- Volcker shock 1979-1982
- Greenspan put 1998-2003
- Whatever it takes Draghi 2012
- COVID 2020 + Powell pivot

À ces dates, les paramètres comportementaux des agents (préférences
d'inflation perçues, anticipations, primes de risque) **changent
structurellement**. C'est la réflexivité de Soros formalisée
statistiquement.

**Conséquence pratique** : un DSGE qui suppose des paramètres deep
stables rate les transitions de régime. Cela explique en partie
pourquoi les modèles DSGE n'ont pas anticipé 2008 (transition de
régime financier) et 2021-2022 (réémergence du régime inflationniste).

**Modification requise** : ajouter un layer Markov sur les paramètres
deep eux-mêmes :

$$
\theta_t = \theta(s_t), \quad s_t \in \{1, \ldots, K\} \text{ Markov chain}
$$

avec `s_t` régime cognitif latent. Implémentations disponibles :
Markov-switching DSGE (Sims-Zha 2006, Liu-Mumtaz 2011, Bianchi-Ilut
2017) mais peu adopté en pratique BC.

Notre `ARFIMARSConfig` + `MarkovRegression` du module
`ecowave.forecasting.arfima_rs` montre une implémentation minimale à
2 régimes.

### Hypothèse 3 — Distributions gaussiennes

**Formulation standard** : les innovations `η_t` des chocs sont
distribuées normalement. Cela simplifie la résolution analytique du
DSGE et permet l'utilisation de filtres de Kalman.

**Verdict CPV** : la famille D (BDS) et les tests de queues (Hill,
Lévy stable) montrent que les distributions empiriques des
fluctuations macro sont **systématiquement non-gaussiennes** :

- Kurtosis empirique : 5-15 (gaussienne : 3)
- Skewness systématiquement non-nulle
- Hill index estime des paramètres de queue α ∈ (1, 3) (gaussienne :
  α = ∞)

**Conséquence pratique** : le DSGE Gaussian sous-estime
systématiquement les événements extrêmes. Cela impacte les VaR et
ES calculés à partir des modèles DSGE, qui sous-estiment le tail risk
de 20-40 %.

**Modification requise** : remplacer Gaussian par Tsallis ou Lévy
stable :

$$
\eta_t \sim \text{Tsallis}(q, \beta) \quad \text{ou} \quad \eta_t \sim \text{Lévy}(\alpha, \beta, \gamma, \delta)
$$

avec `q` (Tsallis non-extensivity) ou `α` (Lévy index) estimés
empiriquement. Les implémentations existent mais ne sont pas
encore standard.

## Pourquoi DSGE n'est cependant pas mort

Les trois modifications ci-dessus sont **structurelles** mais elles
ne tuent pas le DSGE. Elles le **généralisent**. Les versions
modifiées :

1. Conservent la structure d'équilibre intertemporel (Euler,
   Phillips, IS).
2. Conservent l'identification des chocs structurels (technologie,
   préférences, etc.).
3. Conservent l'usage en politique monétaire (analyses what-if,
   scenarios policy).

Ce qui change :

- Le calcul des forecasts utilise un modèle stochastique plus riche.
- L'estimation est plus coûteuse (ARFIMA + MS demande plus de
  données).
- Les analyses de variance unconditionnelle changent (variance
  asymptotique plus grande sous long memory).
- Les intervalles de confiance prédictifs sont plus larges (queues
  lourdes).

Le DSGE *amélioré* reste un cadre légitime pour la modélisation
structurelle. Ce qui est mort, c'est le DSGE *naïf* qui suppose AR(1)
+ paramètres stables + Gauss.

## Le programme de recherche conjoint

Pour réaliser ces modifications, un programme de recherche
banques centrales + universités est nécessaire :

### Axe 1 — Long-memory shocks dans DSGE

**Tâche** : reformuler les modèles SW07 / FRB/US / SAM / COMPASS avec
des chocs ARFIMA au lieu d'AR(1).

**Difficulté technique** : résolution analytique du DSGE devient plus
complexe (pas de solution exponentielle simple). Approches possibles :

- Approximation Padé du processus ARFIMA en somme finie d'AR(1)
  (Sowell 1992).
- Discrétisation du domaine fréquentiel.
- Résolution numérique par Monte Carlo.

**Estimation effort** : 6-12 mois pour une équipe BC standard.

### Axe 2 — Markov-switching layer

**Tâche** : ajouter un layer de régime cognitif au-dessus des
paramètres deep. Suit les approches Sims-Zha 2006, Bianchi-Ilut 2017.

**Difficulté technique** : identification empirique des régimes
(combien ? quand ?), estimation simultanée des paramètres conditionnels
et de la matrice de transition.

**Estimation effort** : 6-9 mois pour adaptation à un modèle BC
existant.

### Axe 3 — Distributions non-gaussiennes

**Tâche** : remplacer Gaussian par Tsallis (économique-théorique
plausible) ou Lévy stable (statistiquement riche).

**Difficulté technique** : filtre de Kalman standard ne s'applique
plus. Solutions :

- Particle filter (Doucet-de Freitas-Gordon 2001).
- Approximation par moments d'ordre supérieur.

**Estimation effort** : 3-6 mois.

### Axe 4 — Validation conjointe

**Tâche** : démontrer empiriquement que le DSGE modifié bat le DSGE
naïf out-of-sample.

**Tests requis** : forecasts à 4, 8, 12 quarters, comparés en CRPS
(comme dans notre benchmark Roadmap #20), sur la même cellule de
variables.

**Estimation effort** : 6-12 mois.

**Total** : 2-3 ans pour un programme bien orchestré, avec coordination
BC + équipes universitaires.

## Pourquoi cela vaut le coût

Le coût opérationnel de moderniser un modèle DSGE est substantiel.
Pourquoi le payer ?

1. **Calibration en politique monétaire** : un modèle qui rate les
   transitions de régime (2008, 2020, 2022) coûte cher en erreurs de
   politique. Le gain attendu : meilleure anticipation des
   retournements et calibration plus adaptative.
2. **Comparabilité internationale** : si les FRB, BCE, BoE adoptent
   tous les modifications, les analyses cross-pays deviennent plus
   robustes. Coordination internationale renforcée.
3. **Crédibilité scientifique** : les critiques académiques (Caballero
   2010, Romer 2016, Stiglitz 2018) qui pointent les limites du DSGE
   moderne deviennent obsolètes. Le programme méta-théorique
   s'avance.
4. **Macroprudentiel** : meilleurs forecasts → meilleurs stress tests
   → meilleurs coussins de capital → moins de défaillances bancaires.
   Le coût social est facile à justifier.

## Argument contre une refonte totale

L'argument alternatif serait d'**abandonner DSGE** au profit d'un cadre
entièrement nouveau (HABM, ABM, active inference). Mais :

- **DSGE a 30 ans d'investissement institutionnel**. Les équipes BC
  sont formées à DSGE. La transition vers un nouveau cadre demanderait
  10+ ans.
- **L'identification structurelle de DSGE est robuste**. Pour
  l'analyse what-if (effet d'une hausse de taux), aucun cadre alternatif
  ne fait mieux pour le moment.
- **Les modifications proposées sont incrémentales**. Pas besoin de
  jeter pour adopter — on peut ajouter par layers.

C'est l'argument du "généraliser plutôt que remplacer". Notre
position : généraliser DSGE est la voie raisonnable. Remplacer
totalement est un objectif de long terme, pas une urgence.

## Implications pour les programmes de PhD

Les modifications proposées suggèrent un programme de formation
doctorale :

- **Cours obligatoires** : intégration fractionnaire (Beran 1994),
  Markov-switching (Hamilton 1989, Sims-Zha 2006), distributions à
  queues lourdes (Embrechts-Klüppelberg-Mikosch 1997).
- **Coursework de séminaire** : finance fractale (Mandelbrot 1997),
  adaptive markets (Lo 2017), reflexivity (Soros 2013).
- **Thèses possibles** : "ARFIMA-DSGE for the eurozone", "Markov-
  switching for monetary policy regime detection", "Heavy-tail
  calibration for macroprudential stress tests", etc.

Plusieurs programmes doctoraux ont déjà commencé à intégrer ces
éléments (LSE, Bocconi, Sciences Po), mais c'est encore minoritaire.

## Pour aller plus loin

### Méthode et verdict

- [Méthode compacte](method_compact.md)
- [Verdict constructif](verdict_constructive.md)
- [Synthèse AMH](synthesis_amh.md) — au-delà de DSGE
- [5 prédictions falsifiables](falsifiable_predictions.md)

### Références

- Smets-Wouters 2003. *Journal of the European Economic Association*.
- Sims-Zha 2006. *Econometrica*.
- Bianchi-Ilut 2017. *Review of Economic Studies*.
- Caballero 2010. *Journal of Economic Perspectives*. "Macroeconomics
  after the Crisis".
- Romer 2016. *American Economic Review*. "The Trouble with
  Macroeconomics".
- Stiglitz 2018. *Oxford Review of Economic Policy*. "Where Modern
  Macroeconomics Went Wrong".
- Bhardwaj-Swanson 2006. *Journal of Econometrics*.
- Beran 1994. *Statistics for Long-Memory Processes*.
- Embrechts-Klüppelberg-Mikosch 1997. *Modelling Extremal Events*.

### Pratique BC

- [Implications opérationnelles (BC track)](../bc/index.md)
- [Horizon-aware targeting](../bc/horizon_aware_targeting.md)

### Code

- `ecowave.forecasting.arfima_rs` — implémentation ARFIMA + Markov
  regime-switching
- `ecowave.forecasting.msm` — implémentation MSM (cascade
  multifractale)
- `ecowave.forecasting.fractional` — primitives Hosking + GPH
