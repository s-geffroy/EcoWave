# Implications du verdict CPV — modélisation, prévision, politique, théorie

> *"Macroeconomic dynamics are a fractional, multifractal, non-linear
> long-memory process with cognitive regime drift."*
> — Working paper CPV §5.1

Le sprint Roadmap #15 a livré une signature empirique sur 9 436 cellules
diagnostiques : le **cluster C+B+D+I+S**. Cette page cartographie ce que
cette signature implique pour la *modélisation*, la *prévision*, la
*politique économique*, et la *théorie* — informée par une recherche
substantielle dans la littérature de modélisation post-cyclique.

Le verdict est *empirique*. Il identifie un cahier des charges
structurel qu'un modèle de la macroéconomie doit satisfaire pour être
crédible. Aucun modèle existant ne satisfait *les cinq piliers
simultanément*. Cette page identifie les candidats les plus proches,
les implications pratiques, et les questions théoriques ouvertes.

---

## 1 · Le verdict en clair

### 1.1 Le cluster C+B+D+I+S

Le toolkit `dx-diagnostics` applique 14 diagnostics structurels non-
cycliques à chaque variable de chaque horizon, plus une analyse panel-
level RMT. Cinq familles co-rejettent leur null AR(1) ou phase-scramble
à α = 0.05 sur une part substantielle des cellules :

| Pilier | Famille | Diagnostic | Rejet null | Statistique médiane |
|---|---|---|---:|---:|
| **C** | Longue mémoire | `hurst_dfa` | 51 % | **H ≈ 1.62** |
| **B** | Multifractalité | `mfdfa_spectrum` | 27 % | Δα ≈ 0.81 |
| **D** | Non-linéarité / non-IID | `bds_independence` | **88 %** | BDS ≈ 3.70 |
| **I** | Information structurée | `permutation_entropy_complexity` | **69 %** | H_perm ≈ 0.85 |
| **S** | Dérive de régime cognitif | `reflexivity_drift` | 51 % | KS ≈ 0.82 |

Plus, au niveau panel : 9 groupes sur 12 ont **un mode dominant**
au-dessus de la bande Marchenko-Pastur — signature G (RMT).

### 1.2 Ce qui est *réfuté*

Trois familles fréquemment invoquées dans la littérature
macroéconomique et physique-of-finance sont *empiriquement faibles* sur
nos données :

- **SOC pur (1/f^β strict)** : 15 % de rejet → la macroéconomie n'est
  pas un Bak sandpile.
- **Critical slowing down (CSD)** : 30 % de rejet → la majorité des
  séries ne sont pas en approche d'un tipping point.
- **Chaos déterministe (Lyapunov)** : 19 % de rejet → la dynamique
  n'est pas dominée par un attracteur chaotique de basse dimension.

### 1.3 Implication immédiate

Le bon mot n'est ni « cycle » ni « chaos » ni « SOC » : c'est
**dynamique fractale non-linéaire à longue mémoire avec dérive de
régime cognitif**. Cette image bouge de Frisch-Slutsky 1933 +
Hodrick-Prescott 1980 (cycle = fluctuation stationnaire autour d'une
tendance) vers Mandelbrot 1997 + Bacry-Muzy-Delour 2001 +
Bouchaud-Potters 2003.

Le reste de cette page développe ce que cela signifie en pratique.

---

## 2 · Implications pour la modélisation

> **Question centrale : quel modèle reproduit le cluster C+B+D+I+S ?**

La recherche bibliographique 2026-05 identifie cinq familles de
modèles techniquement disponibles aujourd'hui. *Aucune ne reproduit les
cinq piliers simultanément* — c'est précisément la question ouverte.

### 2.1 Markov-Switching Multifractal (MSM)

Calvet & Fisher
([NBER WP 9839, 2002](https://www.nber.org/papers/w9839),
*Multifractal Volatility* book 2008). **Le modèle canonique combinant
régime-switching + multifractalité.** Outperforme GARCH(1,1) et FIGARCH
en in-sample et out-of-sample sur les séries financières (rendements
actions, taux de change). Implémentations disponibles :

- Package R [`MSM`](https://cran.r-project.org/package=MSM) sur CRAN.
- [Sage `sage.finance.markov_multifractal`](http://sporadic.stanford.edu/reference/finance/sage/finance/markov_multifractal.html).
- Pas de package Python mature → port custom ou interop R via
  `rpy2`.

**Cluster coverage** : B (multifractalité) + S (régime-switching) +
queues lourdes simultanément. Manque C de manière directe (le modèle
*approxime* la longue mémoire via la cascade multi-fréquence, pas la
modélise comme longue mémoire fractionnaire).

C'est le candidat *#1* pour le benchmark de l'item Roadmap #20.

### 2.2 ARFIMA + Regime-Switching

Granger-Joyeux 1980, Hosking 1981 pour ARFIMA ; Hamilton 1989 pour
regime-switching ; Bhardwaj-Swanson 2006 *J Econometrics* pour
l'application aux 21 datasets macro. **ARFIMA capture C (longue
mémoire) ; l'extension regime-switching capture S.** Couvre la majeure
partie du cluster.

Implémentation Python :

- `statsmodels.tsa.arima.model.ARIMA` ne supporte pas le paramètre
  fractionnaire `d ∈ ℝ`. Il faut soit (a) `arch` package, soit (b)
  réimplémentation directe (la formule récursive de Hosking est
  ~20 lignes Python).
- Regime-switching layer : `statsmodels.tsa.regime_switching.MarkovRegression`.

**Cluster coverage** : C (longue mémoire) + S (regime-switching).
Manque B (multifractalité unifrequence) et J (queues lourdes — il
faudrait extension à queues Student-t ou Tsallis).

C'est le candidat *#2* pour Roadmap #20.

### 2.3 Heterogeneous Autoregressive (HAR)

Corsi 2009 *J Financial Econometrics*. **Workhorse de la prévision de
volatilité réalisée.** Cascade daily/weekly/monthly approxime la
longue mémoire par agrégation. Pas formellement long-memory mais
produit la signature C par construction.

```python
# HAR équation (Corsi 2009)
σ²_t+1 = β₀ + β_d · σ²_t,daily + β_w · σ²_t,weekly + β_m · σ²_t,monthly + ε_t
```

Estimation : régression OLS. Très simple, très compétitif sur la
prévision long-horizon. Cinq lignes Python avec `statsmodels` ou
`scikit-learn`.

**Cluster coverage** : C approximé. Manque B, D, I, S.

C'est le candidat *baseline pratique* pour Roadmap #20 : si MSM ne
bat pas HAR sur out-of-sample, MSM n'apporte rien d'opérationnel.

### 2.4 Multifractal Random Walk (MRW)

Bacry-Muzy-Delour 2001 *Physical Review E*. **Le modèle fondateur
qui capture B + C + queues lourdes simultanément.** Lien direct avec
les cascades K41 de turbulence
([Ghashghaie et al. 1996](https://www.nature.com/articles/381767a0)).

```
log σ²(t) = ω(t) + drift
ω(t) = stationnaire gaussien à covariance log-normale
```

Implémentation : pas de package Python mature. Le générateur MRW est
~50 lignes (cf. nos tests `test_alternative_dynamics_validation.py:_multifractal_random_walk`).
La calibration est plus complexe ; un proxy par méthode des moments
est suffisant en première passe.

**Cluster coverage** : B + C + J. Manque D (non-linéarité explicite —
le MRW est non-linéaire par construction mais non-paramétré
explicitement) et S (regime-switching à ajouter en sur-couche).

C'est le candidat *#3* pour Roadmap #20 : intéressant comme *target
model* pour générer des trajectoires synthétiques sur lesquelles
calibrer les autres modèles.

### 2.5 Heterogeneous Agent-Based Models (HABM)

Lux-Marchesi 1999 *Nature*, Brock-Hommes 1998 *J Economic Dynamics &
Control*, review Hommes 2006 *Handbook of Computational Economics*.
**Produit la signature C + queues lourdes + clustered volatility par
agrégation endogène d'agents à mémoires hétérogènes.**

Mécanisme : agents à croyances/mémoires distribuées hétérogénéement
→ aggregation crée endogénéiquement la longue mémoire + les queues.
Bridge naturel avec réflexivité (S) : les agents peuvent *réviser*
leurs croyances en réaction aux résultats observés.

**Cluster coverage** : C + queues lourdes + S si bouclage de
révision. Mais coût computationnel élevé (Monte Carlo sur des
populations d'agents) et calibration difficile.

**Out-of-scope pour Roadmap #20** mais potentiellement intéressant
pour une étude plus longue (Roadmap #22+).

### 2.6 Adaptive Markets Hypothesis (AMH)

Lo 2004, Lo 2017 *Adaptive Markets : Financial Evolution at the
Speed of Thought*, Princeton. **Cadre conceptuel englobant : marchés
= écosystèmes évolutifs d'agents bornés rationnels.** Connecte
régime change (S), hétérogénéité (multifractalité B), apprentissage
(information I).

**N'est pas un modèle calibrable directement.** Mais une grille de
lecture qui *unifie* le cluster : tous les piliers reflètent une
adaptation évolutive sous pression sélective changeante. Plus utile
comme cadre théorique en discussion (§5) que comme cible de
benchmark.

### 2.7 Active inference / free-energy (Friston)

Friston 2010 *Nature Reviews Neuroscience*. **Formalise la mise à
jour bayésienne de croyances sous incertitude.** Application à la
macroéconomie est *naissante* — pas de benchmark macro mature à ce
jour. Lien naturel avec S (regime drift comme révision de prior) et
I (information structurée comme convergence de croyances).

Implémentation : pas de package Python pour active inference macro.
Travail de recherche, pas de benchmark.

**Out-of-scope** pour Roadmap #20. À garder en réserve pour Roadmap
#22+ comme question théorique.

### 2.8 Synthèse modélisation

| Modèle | C | B | D | I | S | J | Disponible Python | Effort |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| MSM | ★ | ✅ | ★ | – | ✅ | ✅ | port custom | 5 j |
| ARFIMA+RS | ✅ | – | – | – | ✅ | ★ | partiel | 4 j |
| HAR | ★ | – | – | – | – | – | trivial | 1 j |
| MRW | ✅ | ✅ | ★ | – | – | ✅ | port custom | 3 j |
| HABM | ✅ | – | – | – | ✅ | ✅ | Mesa | 15+ j |

★ = couverture partielle / approximative · ✅ = couverture explicite · – = non couvert

**Aucun modèle ne couvre les 5 piliers simultanément.** Le chantier
de modélisation (Roadmap #20) priorise les 3 plus accessibles : HAR
(baseline) + ARFIMA+RS (couverture maximale ARFIMA) + MSM (référence
multifractale).

Pour l'item #20, on construit le pipeline `ecowave forecast-benchmark`
qui compare ces 3 modèles + AR(1) + random walk sur les variables
porteuses du cluster (top 10 de la table §4.4 du papier).

---

## 3 · Implications pour la prévision

### 3.1 L'horizon compte

La littérature
([Bhardwaj-Swanson 2006](https://econweb.rutgers.edu/nswanson/papers/arfima3.pdf) ;
[arxiv 1712.08057](https://arxiv.org/pdf/1712.08057))
montre que les modèles long-memory (ARFIMA, MSM) *outperforment* les
modèles short-memory (AR, ARMA) **uniquement aux horizons médians
et longs** (6 mois et plus). Aux horizons courts (1-3 mois), la
différence est marginale ou négative.

**Conclusion opérationnelle** : la valeur ajoutée du cluster est sur
la prévision *long-terme* — politique économique pluri-annuelle,
planification stratégique, allocation d'actifs long-horizon, design
de garanties d'assurance long-tail. Pas sur le *nowcasting*. Le
benchmark Roadmap #20 doit donc se concentrer sur les horizons 6,
12, 24 mois (cf. spec).

### 3.2 Les comparateurs canoniques

Le benchmark doit être *honest*. Les comparateurs minimaux :

- **Random walk** (statistical floor)
- **AR(1)** (Markov state-space floor)
- **ARMA(1,1)** (short-memory benchmark)
- **HAR Corsi 2009** (long-memory approximation par cascade)
- **Professional forecasters** : FOMC SEP, ECB BMPE, BOE MPC, Survey
  of Professional Forecasters (où les variables se recoupent).

**Important** : si MSM ne bat pas SPF sur les variables que SPF
couvre (croissance PIB US, inflation US à 4 trimestres), c'est une
information importante — elle signifie que les humains forecasters
intègrent déjà la longue mémoire implicitement. La force du cluster
picture serait alors *narrative* (expliquer pourquoi SPF marche),
pas *opérationnelle* (remplacer SPF).

### 3.3 La métrique compte

Sous queues lourdes (notre J + T + Hill), MSE/MAE sous-pénalisent
les pertes catastrophiques. Le benchmark doit reporter au minimum :

- **RMSE / MAE** (canoniques)
- **CRPS** (Continuous Ranked Probability Score — *proper scoring
  rule*, sensible aux queues, cf. Gneiting-Raftery 2007 *JASA*)
- **Coverage 95 %** (le forecast interval à 95 % contient-il la
  réalisation à la bonne fréquence ?)
- **Tail coverage** (couverture conditionnelle aux 5 % de
  réalisations les plus extrêmes — capture spécifique des queues)

### 3.4 Le régime-conditioning

Sous reflexive regime drift (S), les performances de prévision
*varient par régime*. Un modèle qui bat le random walk en moyenne
peut perdre catastrophiquement près d'un tipping point. Le benchmark
doit *décomposer la performance par régime identifié* :

- **Pré-2008** vs **post-2008**
- **Pré-COVID** vs **COVID** vs **post-COVID**
- **Optionnel** : reflexivity_multi_window split points (1971, 1979,
  etc.) sur l'horizon long.

Si un modèle bat random walk en moyenne mais sous-performe
catastrophiquement en COVID, c'est *l'opposé* d'un modèle utile.
Cette décomposition par régime est *la* contribution méthodologique
spécifique au cluster picture : le benchmark doit explicitement la
mesurer.

### 3.5 Les variables porteuses

La page §4.4 du working paper identifie le top 10 des variables
multi-diagnostic-rejet : `LH_IMPORTS`, `LH_EXPORTS`, `LH_MONEY`,
`LH_EXP`, `LH_REV`, `LH_NARROW`, `LH_BANKDEBT`, `BOE_MONEY`,
`LH_MORT`, `LH_CREDIT`. Ce sont les **agrégats monétaires et de
crédit historiques** (JST R6 + BoE Millennium).

**Implication pour le benchmark** : commencer par ces 10 variables
maximise les chances d'observer une supériorité du cluster picture
sur les comparateurs canoniques. C'est là que le signal structural
est le plus fort, donc là que les modèles long-memory / multifractal
ont le plus de marge.

Variables contemporaines à ajouter pour pertinence politique :
`Q_GDP` (US, Eurozone, JPN, GBR), `Q_CPI`, `Q_UNRATE`. Même si le
signal y est plus faible (horizon `q` 1995-2024, n=120 trimestres),
ce sont les variables sur lesquelles les central banks forecast.

---

## 4 · Implications pour la politique économique

### 4.1 Inflation targeting et crédibilité monétaire

La longue mémoire dans l'inflation (notre H médian = 1.62) est un
*indicateur de crédibilité du régime monétaire*
([cambridge.org Shades of inflation targeting](https://www.cambridge.org/core/journals/macroeconomic-dynamics/article/shades-of-inflation-targeting-insights-from-fractional-integration/CCE94E57396616BA7C621EDF3D73B66B)).
Les pays avec `d > 0.5` sur l'inflation ont une crédibilité plus
faible : les chocs persistent et les ancrages d'anticipations sont
fragiles.

**Volcker a *cassé* la persistance** post-1979 en imposant un régime
haussier brutal — c'est l'opérationnalisation empirique de S (regime
shift exogène par acte de politique). Notre diagnostic
`reflexivity_multi_window` détecte ce split-point sur les séries
financières du panel long.

Implication opérationnelle pour les central banks : une mesure
*continue* du Hurst d'inflation est un *indicateur de crédibilité*
qui complète les enquêtes d'attentes (Michigan, Conference Board,
NY Fed SCE). Un Hurst d'inflation qui *monte* sur fenêtre roulante
signale un *décrochage* de la crédibilité avant que les enquêtes
le détectent. Roadmap #18 Prédiction 5 (reflexive split-point
specificity) testera cette hypothèse.

### 4.2 Macroprudentiel et Bâle

La longue mémoire + multifractalité sur les agrégats crédit
(`LH_CREDIT`, `LH_MORT`, `LH_BANKDEBT`, top 5 de notre cluster)
implique que **les booms de crédit ont des ombres très longues**.
Bâle II/III sous-estime la persistance des risques systémiques en
supposant des distributions exponentielles ou des chocs IID.

Le **credit-to-GDP gap** de Borio (2014) est un proxy utile mais
incomplet — il mesure la déviation par rapport à une tendance HP,
qui suppose des décompositions stationnaires. Un **Hurst-based
credit cycle** mesurant directement la persistance fractionnaire de
la dette accumulée serait une mesure plus fidèle au cluster picture.

**Implication concrète** : Bâle IV (en préparation) pourrait
incorporer une *long-memory adjustment factor* aux pondérations de
risque sur le crédit. La dette accumulée sur les périodes de boom
long-mémoire a une probabilité de défaut conditionnelle *plus
élevée* que celle prédite par les modèles short-memory.

### 4.3 VaR vs Expected Shortfall

Sous queues lourdes (notre J + T + Hill), **VaR est non-cohérent**
(non-additif) et sous-estime systématiquement le tail risk. ES
(Expected Shortfall) est la mesure cohérente recommandée par
Artzner-Delbaen-Eber-Heath 1999 et adoptée par le Comité de Bâle
dans Basel 2.5 (2009-2012) et Basel III (2016).

Le passage VaR → ES est *consistent* avec notre cluster. **Mais les
calibrations actuelles de ES sur des distributions normales
sous-estiment encore le tail risk** : le median Hill α = 3.59 sur
nos cellules implique des queues *strictement plus lourdes* qu'une
gaussienne. Un cluster-picture-aware ES calculé sur q-Gaussien
(Tsallis) ou Lévy stable donnerait des estimations *plus
prudentes*.

Réplique pour les régulateurs : passer de "ES sur distribution
normale" à "ES sur distribution q-Gaussienne calibrée" augmenterait
les exigences de capital de ~20-30 % sur les portefeuilles à
exposition aux queues lourdes (compute exact à faire dans Roadmap
#20+). C'est *coûteux* pour les banques mais *prudent* pour la
stabilité financière.

### 4.4 Horizons de forecasting des autorités

- Central banks : forecast à 1-2 ans (FOMC SEP, ECB BMPE)
- Trésors : planification à 5-10 ans (CBO long-term budget outlook,
  EU MFF)
- Fonds souverains : 30-50 ans (Norway, GIC Singapore)

La longue mémoire implique que des **modèles différents** sont
optimaux pour chaque horizon. Une politique monétaire qui ignore la
longue mémoire dans l'inflation va *sous-réagir* aux chocs
persistants — c'est exactement ce qui s'est passé en 2021-2022
(Powell et Lagarde annonçaient "inflation transitoire" alors que
les diagnostics long-memory auraient signalé une persistance bien
réelle).

**Implication concrète** : un dashboard *long-memory persistence*
calibré sur le cluster picture serait un complément utile aux SEPs
existants. Le Hurst d'inflation, le Hurst de prix énergétiques, le
Hurst de salaires nominaux — tous mesurés sur fenêtres roulantes,
seraient des signaux de persistance des chocs *avant* qu'ils
deviennent visibles dans les SEPs.

### 4.5 Réflexivité et communication des banques centrales

Les annonces de politique *changent* le régime cognitif collectif.
Le QE post-2008, le forward guidance, le QT post-2022 sont des
*actes performatifs* au sens Soros : ils ne se contentent pas de
*répondre* à l'économie, ils la *constituent* en redéfinissant
les anticipations. C'est *exactement* la signature de S
(reflexive regime drift) opérationnalisée empiriquement par notre
51 % de rejet `reflexivity_drift`.

**Conséquence théorique** : la banque centrale ne peut pas se
contenter d'*observer* l'économie comme un système physique stable.
Elle est *partie* du système. Les modèles DSGE qui traitent la
politique monétaire comme exogène à l'équilibre manquent S par
construction — c'est pourquoi ils ratent les inflexions de régime.

**Conséquence pratique** : la *communication* est un instrument
de politique au même titre que les taux. Forward guidance et
press conferences ne sont pas des "explications" du dernier
décision — ce sont des *outils* qui modifient le régime cognitif.
Cela est largement reconnu en pratique mais rarement modélisé
formellement.

---

## 5 · Implications pour la théorie

### 5.1 Le cycle est mort, vive la cascade

La macroéconomie *n'est pas* une oscillation autour d'un équilibre.
C'est une **cascade multifractale non-linéaire à longue mémoire sur
un fond de régimes cognitifs glissants**.

Cette image *bouge* le cadre standard de :

- Frisch-Slutsky 1933 + Hodrick-Prescott 1980 (cycle =
  fluctuation stationnaire autour d'une tendance) ;
- RBC / King-Plosser-Rebelo 1988 (cycle = réponse impulse à
  chocs IID Gaussiens) ;
- NK-DSGE Smets-Wouters 2003 (cycle = propagation AR(1) de chocs
  sur paramètres calibrés) ;

vers :

- Mandelbrot 1997 *Fractals and Scaling in Finance* (longue
  mémoire fractale) ;
- Bacry-Muzy-Delour 2001 *Phys Rev E* (multifractalité comme
  signature structurelle) ;
- Bouchaud-Potters 2003 *Theory of Financial Risk* (structured
  noise + dominant correlation factor) ;
- Soros 1987 *Alchemy of Finance* (réflexivité comme couche
  cognitive performative) ;
- Lo 2017 *Adaptive Markets* (évolution adaptative comme
  méta-cadre).

### 5.2 DSGE en accusation

NK-DSGE assume trois choses :

1. **Chocs AR(1) ou IID exogènes** sur les paramètres profonds
   (productivité, préférences, technologie).
2. **Régime cognitif stable** : les anticipations rationnelles
   forward-looking sont une équation d'équilibre permanente.
3. **Distributions gaussiennes** pour les innovations stochastiques.

**Les trois sont falsifiés par notre cluster.** Notre BDS à 88 %
rejette IID. Notre Hurst > 1 rejette AR(1). Notre Tsallis q > 1.05
rejette gaussien. Notre reflexivity_drift à 51 % rejette stabilité
cognitive.

Ce n'est pas que DSGE est *inutilisable* — c'est qu'il a besoin de
**modifications structurelles** :

- Chocs *fractionnaires* (processus Lévy à long memory) au lieu
  d'AR(1).
- *Layer Markovien* sur les paramètres profonds pour capturer le
  regime drift.
- Innovations *q-Gaussiennes* ou *Lévy stables* pour les queues.
- Mécanismes de *belief-updating* pour la réflexivité (Friston
  active inference style).

Sans ces modifications, DSGE ne peut pas prédire 2008, 2020, 2022 —
*exactement* ses échecs documentés. Avec ces modifications, DSGE
devient computationnellement *beaucoup* plus lourd (la propriété
state-space Markov disparaît avec la longue mémoire). Mais le
sacrifice computationnel est *empiriquement justifié*.

### 5.3 Cycles, narrativement OK ; statistiquement non

La *narration* des 4 cycles reste utile pédagogiquement (Kitchin =
inventory, Juglar = credit/investment, Kuznets = building,
Kondratieff = technology). Comme **grilles herméneutiques**, elles
structurent le récit historique : on peut *raconter* Bretton Woods
1944, le choc Volcker 1979, la dérégulation Reagan-Thatcher 1980+,
Lehman 2008, comme des inflexions de cycles de Juglar ou
Kondratieff.

Le problème est leur **statut statistique-mécaniste** : on les
invoque comme s'ils *existaient* comme oscillateurs détectables sur
les séries. C'est cette **double identité — narrative et
mécaniste** — qu'il faut désentangler.

Le cluster picture rebrand ces narrations : *Kondratieff* n'est pas
un cycle de 40-60 ans, c'est une *séquence de régimes cognitifs*
(Pax Britannica, Pax Americana, Pax Sino-Americana émergente) avec
*persistance fractionnaire* dans chaque régime. *Kitchin* n'est pas
un cycle d'inventaire de 3-5 ans, c'est la *durée de relaxation*
du cycle de stock dans le régime cognitif courant. Etc.

Cette traduction *préserve* l'utilité narrative tout en *abandonnant*
la prétention statistique-mécaniste qui s'avère fausse.

### 5.4 Synthèse théorique manquante

**Aucune théorie unifiée ne *prédit* le cluster à partir de premiers
principes.** Les candidats existants couvrent chacun une partie :

| Cadre | Pilier C | Pilier B | Pilier D | Pilier I | Pilier S |
|---|:-:|:-:|:-:|:-:|:-:|
| Friston free-energy | – | – | – | ✅ | ✅ |
| Bouchaud structured-noise | ✅ | ✅ | – | – | – |
| Mandelbrot finance fractals | ✅ | ✅ | – | – | – |
| Bacry-Muzy-Delour MRW | ✅ | ✅ | ✅ | – | – |
| Lo adaptive markets | – | – | – | – | ✅ (umbrella) |
| Active inference + MRW (hypothétique) | ✅ | ✅ | ✅ | ✅ | ✅ |

**Aucun cadre n'unifie les 5 piliers.** L'hypothèse intuitive : la
combinaison *Active inference + MRW* pourrait couvrir le cluster
complet :

- Active inference fournit S (regime drift comme révision de prior)
  + I (information structurée comme convergence Bayesienne) ;
- MRW fournit C (longue mémoire) + B (multifractalité) + queues
  lourdes ;
- Non-linéarité D émerge de l'interaction Bayesienne-multifractale
  (à démontrer).

C'est *la* question théorique ouverte que pose le cluster picture.
Notre travail empirique donne le **cahier des charges** qu'une
théorie unifiée devra satisfaire. La construction d'une telle
théorie est *hors scope* du projet CPV ; elle relève d'une
collaboration entre économistes computationnels, physiciens
statistiques, et neuroscientifiques (Friston-école).

### 5.5 Adaptive Markets Hypothesis comme méta-cadre

[Lo 2017](https://press.princeton.edu/books/paperback/9780691191362/adaptive-markets)
propose **AMH** comme cadre conceptuel unifiant : marchés =
écosystèmes évolutifs d'agents bornés rationnels avec adaptation
sélective. Sous AMH :

- Les **régimes cognitifs** (S) sont des *équilibres temporaires*
  dans la fitness landscape évolutive.
- La **multifractalité** (B) reflète l'*hétérogénéité* des agents
  et des stratégies.
- La **longue mémoire** (C) reflète la *persistance* des stratégies
  adaptées au régime courant.
- L'**information structurée** (I) reflète l'*apprentissage*
  collectif sur le régime.
- La **non-linéarité** (D) reflète la *sélection* sur les
  stratégies perdantes.

AMH n'est pas un modèle calibrable — c'est une *grille de lecture*.
Mais elle a l'avantage d'unifier *narrativement* les 5 piliers du
cluster sans présupposer de mécanisme oscillatoire.

Une suggestion conceptuelle pour le papier V2 : faire de **AMH le
cadre méta-théorique** explicite du cluster picture, avec MRW
comme modèle statistique calibrable et active inference comme
mécanisme microfondé.

---

## 6 · Conclusion et chantiers

Le verdict CPV n'est pas une *fin* — c'est un *point de bascule*.
Avant : on cherchait des cycles, on n'en trouvait pas
statistiquement. Maintenant : on a identifié un cluster structurel
(C+B+D+I+S+G), on connaît la littérature de modélisation qui en
couvre les fragments, et on sait ce qui manque.

Les chantiers concrets identifiés dans cette page sont consignés
dans la feuille de route :

- **Roadmap #19** (cette page elle-même) — livrée.
- **Roadmap #20** — benchmark de modélisation (HAR + ARFIMA+RS +
  MSM vs random walk vs AR(1)). ~15 jours.
- **Roadmap #21** — enrichissement bibliographie modélisation
  post-cluster. ~0.5 jour.

Les chantiers conceptuels ouverts :

- Synthèse théorique unifiée (Active inference + MRW + AMH ?) —
  *hors scope* CPV, à confier à des collaborations académiques.
- Long-memory adjustment factor pour Bâle IV — *out of scope* CPV,
  mais consignable comme implication policy à publier en working
  paper séparé.
- Operationalisation du *Hurst-based credit cycle* — extension
  naturelle de Roadmap #18 Prédiction 5.

Le cluster picture est **falsifiable**, **constructible**, et
**actionnable**. C'est ce que veut un cadre scientifique robuste,
et c'est ce que les cycles canoniques *ne sont pas*.

---

## Sign-off

- **Date de la note** : 2026-05-30
- **Auteur** : Sylvain Geffroy
- **Liens** :
    - Working paper V1 : [`papers/cpv_main_paper.md`](papers/cpv_main_paper.md)
    - Diagnostics empiriques : [`dx_diagnostics.md`](dx_diagnostics.md)
    - Panorama des familles : [`methodology_beyond_cycles.md`](methodology_beyond_cycles.md)
    - Feuille de route : [`methodology/feuille_de_route.md`](methodology/feuille_de_route.md)
- **Sidecars JSON** : `reports/dx_diagnostics_2026_05_*.json` (12
  fichiers, 4.5 MB) et `reports/dx_rmt_2026_05_*.json`.
- **Reproductibilité** : `docker compose run --rm --entrypoint ecowave ecowave dx-diagnostics --as-of 2026-05 --horizons wb,q,long,boe,bis,sh --n-surrogates 100 --seed 0`.
