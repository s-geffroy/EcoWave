# Au-delà des cycles — cadres physiques alternatifs pour les séries macroéconomiques

> **Résumé.** Le pipeline CPV a démontré empiriquement que les cycles
> canoniques Kitchin / Juglar / Kuznets / Kondratieff sont indétectables
> au niveau strictement statistique — ni sur composites, ni sur variables
> individuelles, ni même sur les séries originales que les découvreurs
> ont étudiées. Cette défaite empirique est la base du papier académique
> et ne doit pas être quittée. Mais les séries macroéconomiques ne sont
> **pas du bruit blanc** : ACF lag-1 ≈ 1.000, agglomération de la
> volatilité, ruptures structurelles, lois de puissance dans les
> distributions de crashes — autant de signatures de *quelque chose*.
> Cette page passe en revue **15 familles de cadres physiques candidats**
> qui pourraient rendre compte des signatures observées sans présupposer
> de périodicité. Le mot final est ouvert : *"la macroéconomie n'est pas
> un cycle, et voici 15 grilles de lecture alternatives, dont 5
> directement testables"*. Le papier reste falsifiabiliste — on
> multiplie les cadres pour ne pas tomber dans un nouveau dogme.

## Préambule — si pas un cycle, quoi alors ?

La chaîne d'audits CPV (cf. études de cas
[CN_BIS](case_study_cn_bis_kondratieff.md),
[WLD-WB](case_study_wld_wb_kondratieff.md),
[G7-long & UK_BOE](case_study_g7_long_uk_boe_kondratieff.md),
[Wen 2005 falsifié](case_study_wen_2005_test.md) +
[safeguard Roadmap #14](methodology_safeguard_roadmap_14.md)) établit :

- **Composites macro** : 35 cellules vetoed sur 128, 4 survies authentiques.
- **Per-variable Gate 1** : ~5000 cellules testées toutes bandes confondues, 1.5 % de survie globale (et après safeguard quasi-zéro).
- **Séries originales de Kitchin (1923)** : 0/44 cellules survivent sur le panel sectoriel `SH_*` (charbon, fonte, fret, blé, coton).

Aucune périodicité statistiquement défendable n'émerge.

Pourtant les signatures qu'on observe ne sont pas celles du bruit blanc :

| Signature observée sur CPV | Incompatible avec | Compatible avec |
|---|---|---|
| ACF lag-1 ≈ 0.97-1.000 sur ~30 % des séries | Bruit blanc | Longue mémoire, marche aléatoire, processus fractionnaires |
| Pas de pics nets dans spectres wavelet | Cycle déterministe | 1/f noise, spectre continu de scaling |
| Distributions à queues lourdes (crashes 1929, 2008) | Gaussienne | Lévy stables, SOC, lois de puissance |
| Agglomération de la volatilité | I.I.D. | GARCH, multifractalité, processus stochastique de la volatilité |
| Trends structurels post-1980 (financiarisation, productivité, dette/PIB) | Stationnarité | Ruptures, drifts non-stationnaires, bifurcations |
| Per-variable Gate 1 reject, composite survive (artefacts d'agrégation) | Synchronisation parfaite | Synchronisation partielle (Kuramoto), critical slowing, RMT modes |

L'enjeu est de **caractériser** ces signatures avec un cadre cohérent —
sans imposer la grille du cycle. La physique offre une douzaine de
candidats explorés ci-dessous.

## Famille A — Criticité auto-organisée et lois de puissance

> *"Les systèmes complexes évoluent spontanément vers un état critique
> où les avalanches se produisent à toutes les échelles."*

- **A1. Self-Organized Criticality (SOC)** —
  [Bak, Tang & Wiesenfeld (1987)](bibliographie.md#bak-tang-wiesenfeld-1987),
  [Bak (1996)](bibliographie.md#bak-1996). Modèle canonique du tas de
  sable : grains qui s'accumulent jusqu'à déclencher des avalanches de
  toutes tailles. Reproduit le bruit 1/f.
- **A2. Loi de Gutenberg-Richter** appliquée aux crashes — [Sornette
  (2003)](bibliographie.md#sornette-2003). Distribution log-normale ou
  loi de puissance des magnitudes de crises financières.
- **A3. Log-Periodic Power Law Singularity (LPPL)** —
  [Sornette & Johansen (1999)](bibliographie.md#sornette-johansen-1999).
  Bulles financières caractérisées par une accélération en loi de
  puissance avec oscillations log-périodiques précurseurs.
- **A4. Dragon kings** — Sornette (2009). Événements outliers
  au-dessus de la loi de puissance générale, potentiellement
  prédictibles localement.

**Signature statistique** : distribution des incréments en loi de
puissance avec exposant α ∈ [2, 3] ; spectre de puissance 1/f^β avec
β ∈ [0.5, 1.5]. Tests directs : fit de Hill, test K-S vs loi de
puissance, slope spectrale log-log.

**Applicabilité CPV** : ★★★★★. Directement testable sur CPI long
(BoE 1661+), équity returns, GDP growth. Les crashes observés
(1929, 1971, 2008, 2020) sont compatibles avec une distribution
en loi de puissance — non-périodiques mais structurés.

## Famille B — Géométrie fractale et multifractalité

> *"Les séries n'ont pas un mais une infinité de scaling exponents."*

- **B1. Multifractal Random Walk (MRW)** —
  [Bacry, Muzy & Delour (2001)](bibliographie.md#bacry-muzy-delour-2001).
  Modèle stochastique à mémoire log-normale qui reproduit les faits
  stylisés des séries financières (queues lourdes, clustering).
- **B2. Detrended Fluctuation Analysis (DFA)** —
  [Peng et al. (1994)](bibliographie.md#peng-1994). Quantifie le Hurst
  exponent H sur séries non-stationnaires.
- **B3. Multifractal DFA (MF-DFA)** —
  [Kantelhardt et al. (2002)](bibliographie.md#kantelhardt-2002). Étend
  DFA aux différents moments q, génère le spectre multifractal f(α).
- **B4. Mandelbrot Finance Fractale** —
  [Mandelbrot (1997)](bibliographie.md#mandelbrot-1997). Manuel
  synthétique.

**Signature statistique** : spectre multifractal f(α) de largeur
Δα = α_max − α_min > 0.1 ; scaling exponent τ(q) non-linéaire en q.

**Applicabilité CPV** : ★★★★. Diagnostic MF-DFA réalisable sur les
séries longues (BoE 316 ans, JST 152 ans). Si Δα > 0.2, on a une
preuve directe de multifractalité — incompatible avec le cadre
monofractal du bruit blanc et du cycle.

## Famille C — Longue mémoire et processus fractionnaires

> *"L'ACF décroît en loi de puissance, pas exponentiellement."*

- **C1. Hurst exponent** —
  [Hurst (1951)](bibliographie.md#hurst-1951). H > 0.5 = persistance ;
  H < 0.5 = anti-persistance ; H = 0.5 = marche aléatoire.
- **C2. Fractional Brownian motion** — Mandelbrot & Van Ness (1968).
  Processus auto-similaire d'index H.
- **C3. ARFIMA** (Granger & Joyeux 1980 ; Hosking 1981). Modèle
  économétrique de longue mémoire avec différenciation fractionnaire.
- **C4. Cohérence CPV** : ACF lag-1 = 0.97-1.000 observée sur CY_FIN,
  CY_PRD, CY_POP, CY_TRD, LH_DEBTGDP, BIS_CRATIO, etc.
  Hypothèse forte : H >> 0.5.

**Signature statistique** : ρ(k) ~ k^{−α} pour des grands lags k,
spectre de puissance avec pic à basse fréquence en loi de puissance.

**Applicabilité CPV** : ★★★★★. Le diagnostic le plus naturel pour
les signatures déjà observées. Si on n'a pas de cycle mais H = 0.85
sur LH_DEBTGDP, alors le "cycle long de la dette" est en fait un
processus de longue mémoire — pas un cycle, mais pas du bruit non
plus.

## Famille D — Chaos déterministe et attracteurs étranges

> *"La dynamique semble aléatoire mais est en fait déterministe
> sensitive aux conditions initiales."*

- **D1. Lyapunov exponent positif** — Wolf et al. (1985). Mesure de
  sensibilité aux conditions initiales.
- **D2. Embedding de Takens** —
  [Takens (1981)](bibliographie.md#takens-1981). Reconstruction
  d'espace de phase depuis time series 1D.
- **D3. Dimension de corrélation** —
  [Grassberger & Procaccia (1983)](bibliographie.md#grassberger-procaccia-1983).
- **D4. Tests BDS** —
  [Brock, Dechert & Scheinkman (1996)](bibliographie.md#brock-dechert-scheinkman-1996)
  pour non-linéarité et non-indépendance.
- **D5. Reservoir computing / Echo State Networks** — Jaeger (2001).
- **D6. Edge of chaos** — Langton (1990), Kauffman (1993).

**Signature statistique** : λ_max > 0 (chaos) ; dimension de
corrélation finie non-entière ; BDS rejette IID.

**Applicabilité CPV** : ★★. Coût élevé (estimations Lyapunov fragiles
sur séries courtes < 500 obs). Plus utile sur Path 5 quarterly
(225+ obs) que sur WB annuel (65 obs). Le verdict serait : "ce n'est
pas du chaos déterministe pur, c'est du bruit + structure."

## Famille E — Critical slowing down et tipping points

> *"Avant un basculement, la variance et l'autocorrélation augmentent
> systématiquement."*

- **E1. Scheffer et al.** —
  [Scheffer (2009)](bibliographie.md#scheffer-2009). Article de
  référence sur les early-warning signals.
- **E2. Dakos et al.** —
  [Dakos et al. (2008)](bibliographie.md#dakos-2008). Variance, AC1,
  skewness, return-rate — tous augmentent près d'un tipping point.
- **E3. Carpenter-Brock 2006**. Application écologique.
- **E4. Tipping cascades** —
  [Lenton & Williams (2013)](bibliographie.md#lenton-williams-2013).
  Cascades transversales entre systèmes.

**Signature statistique** : variance et AC1 croissants en fenêtre
roulante avant rupture, test Kendall-tau pour tendance ascendante.

**Applicabilité CPV** : ★★★★. Test direct : appliquer
le diagnostic Dakos sur les fenêtres pré-1929, pré-2008, pré-2020,
pré-1971 (Bretton Woods) sur le CPI BoE 1661+ ou le crédit-PIB
historique. Si les early-warning signals s'allument systématiquement,
on a une lecture cohérente "régimes successifs + transitions
critiques" qui supplante celle "cycle".

## Famille F — Synchronisation et oscillateurs couplés

> *"La régularité apparente émerge de la synchronisation de multiples
> oscillateurs incommensurables."*

- **F1. Modèle de Kuramoto** —
  [Kuramoto (1984)](bibliographie.md#kuramoto-1984). N oscillateurs
  avec fréquences naturelles, transition de phase ordre-désordre.
- **F2. Strogatz** —
  [Strogatz (2003)](bibliographie.md#strogatz-2003). Vulgarisation
  synthétique.
- **F3. KAM theorem / pendules multiples** (Kolmogorov 1954, Arnold
  1963, Moser 1962). Orbites quasi-périodiques préservées sous
  perturbations en systèmes Hamiltoniens. *Cadre suggéré par sge.*
  Le cas du double pendule est chaotique ; le pendule triple
  fortement couplé reste chaotique. Plusieurs pendules faiblement
  couplés peuvent rester quasi-périodiques (KAM).
- **F4. Arnold tongues / mode locking**. Plages de fréquences
  synchronisées dans systèmes paramétriques.
- **F5. Coupled oscillators with delay**. Plus réaliste pour
  économie (transmission de chocs avec lag).

**Signature statistique** : pics multiples dans spectre, non
commensurables ; cohérence cross-séries qui dépend de l'amplitude ;
épisodes de synchronisation partielle alternant avec décohérence.

**Applicabilité CPV** : ★★★. Intéressant mais coût élevé
(modèles paramétriques à fitter). Le rejet composite vs survie
individuelle de certaines variables (G7-long K, par exemple) pourrait
s'interpréter comme synchronisation partielle plutôt qu'artefact —
à creuser via cohérence wavelet.

## Famille G — Théorie des matrices aléatoires (RMT)

> *"La majorité du spectre eigenvalues des matrices de corrélation
> est du bruit pur ; seules quelques eigenvalues portent du signal."*

- **G1. Marchenko-Pastur** —
  [Marchenko & Pastur (1967)](bibliographie.md#marchenko-pastur-1967).
  Distribution théorique des eigenvalues d'une matrice de covariance
  bruitée.
- **G2. Bouchaud-Potters** —
  [Bouchaud & Potters (2003)](bibliographie.md#bouchaud-potters-2003).
  RMT pour panels financiers.
- **G3. Laloux et al.** —
  [Laloux et al. (1999)](bibliographie.md#laloux-1999). "Noise
  dressing" des corrélations financières.

**Signature statistique** : spectre eigenvalues conforme à
Marchenko-Pastur sauf pour quelques eigenvalues "bulk-deviating".

**Applicabilité CPV** : ★★★★. Tests immédiats sur les corrélations
inter-pays JST (18 économies × 35 variables) ou inter-variable.
La conclusion attendue : la matrice de corrélation a 2-3 modes
significatifs (mode commun, mode régional, mode financier vs réel)
+ un bulk de bruit. Aucun mode n'est un "cycle".

## Famille H — Verres de spin et systèmes désordonnés

> *"Multiples états métastables, relaxation lente, hétérogénéité des
> agents."*

- **H1. Mézard-Parisi-Virasoro** —
  [Mézard, Parisi & Virasoro (1987)](bibliographie.md#mezard-parisi-virasoro-1987).
  Frustration, replica symmetry breaking.
- **H2. Aging dynamics** — Bouchaud (1992), Cugliandolo-Kurchan (1993).
  Le temps de relaxation dépend du temps d'observation.
- **H3. Mode coupling theory** — Götze (1991). Transition vitreuse.
- **H4. Minority Games** — Marsili-Challet-Zhang (1998). Marché
  comme système désordonné.

**Signature statistique** : autocorrélation non-stationnaire (aging),
pseudo-équilibres multiples, hétérogénéité des temps de relaxation.

**Applicabilité CPV** : ★★. Cadre conceptuellement riche pour penser
l'hétérogénéité des agents et des chocs ; statistiquement difficile à
tester sur séries univariées (les diagnostics canoniques exigent
simulations ou ABM).

## Famille I — Théorie de l'information et complexité

> *"Mesurer la quantité d'information, sa structure, sa transmission."*

- **I1. Permutation entropy** —
  [Bandt & Pompe (2002)](bibliographie.md#bandt-pompe-2002). Motifs
  ordinaux, robuste au bruit.
- **I2. Transfer entropy** —
  [Schreiber (2000)](bibliographie.md#schreiber-2000). Mesure
  asymétrique de l'information transférée entre séries.
- **I3. Statistical complexity** —
  [Crutchfield & Young (1989)](bibliographie.md#crutchfield-young-1989).
  Distingue ordre, désordre, complexité structurée.
- **I4. Compression-based metrics** — Cilibrasi & Vitanyi (2005).

**Signature statistique** : permutation entropy intermédiaire
(ni 1 = bruit blanc, ni 0 = constante) ; statistical complexity
élevée (Crutchfield).

**Applicabilité CPV** : ★★★★★. Permutation entropy est trivialement
applicable, robuste au bruit, donne un diagnostic immédiat : si
l'entropie permutationnelle des séries CPV est intermédiaire (entre
0.7 et 0.95), on a une preuve de structure non-périodique mais
non-aléatoire.

## Famille J — Lévy flights et processus à sauts

> *"Les rendements suivent une distribution à queue lourde
> (Lévy stable), pas Gaussienne."*

- **J1. Mantegna-Stanley** —
  [Mantegna & Stanley (1999)](bibliographie.md#mantegna-stanley-1999).
  Manuel fondateur de l'econophysique. Distributions Lévy stables sur
  S&P 500, or, etc.
- **J2. Continuous-Time Random Walk (CTRW)** — Montroll & Weiss (1965).
- **J3. Subordinators / time-changed Brownian motion**. Activity time
  vs clock time.
- **J4. Stochastic resonance** — Benzi-Sutera-Vulpiani (1981).
  Optimum de bruit pour détection de signal.

**Signature statistique** : queues lourdes (kurtosis > 3),
distributions Lévy stables avec α ∈ [1, 2].

**Applicabilité CPV** : ★★★★. Fit direct de la distribution des
incréments annuels du CPI BoE 1661+, des returns equity, du
crédit-PIB. Si on observe α = 1.5-1.7 (Lévy stable, pas
Gaussienne), c'est compatible avec un cadre Lévy flight et
incompatible avec un cycle déterministe + bruit gaussien.

## Famille K — Soft matter, cristaux liquides, topologie

> *"Phases avec ordre partiel et défauts topologiques persistants."*

- **K1. Cristaux liquides** —
  [De Gennes (1974)](bibliographie.md#de-gennes-1974). Phase nématique,
  smectique, cholestérique. Champs directeurs, défauts topologiques.
  Métaphore proposée par sge : les phases macroéconomiques ont un
  ordre partiel, structurées mais non-cristallines.
- **K2. Solitons et structures topologiques**. Persistance sans
  périodicité (vagues isolées qui voyagent sans déformation).
- **K3. Quasi-cristaux** — Shechtman (1984). Ordre apériodique mais
  structuré (Penrose tilings).
- **K4. Topological data analysis** — Carlsson (2009). Persistent
  homology pour caractériser géométrie d'embedding.

**Signature statistique** : ordre quasi-périodique, invariants
topologiques, défauts persistants dans embedding de Takens.

**Applicabilité CPV** : ★★. Conceptuellement riche, statistiquement
exotique. La métaphore cristal liquide est belle mais difficile à
opérationnaliser sur des séries macro 1D. TDA est plus directement
applicable mais reste exploratoire pour l'économétrie.

## Famille L — Biologie évolutionniste et écologie

> *"Stases longues + ruptures rapides, lois d'échelle universelles."*

- **L1. Punctuated equilibrium** —
  [Gould & Eldredge (1972)](bibliographie.md#gould-eldredge-1972).
  Analogue paléontologique de la creative destruction schumpetérienne.
- **L2. Bak-Sneppen (1993)**. Coévolution avalanches.
- **L3. Allometric scaling** —
  [West, Brown & Enquist (1997)](bibliographie.md#west-brown-enquist-1997).
  Lois d'échelle universelles.
- **L4. Tipping cascades en écosystèmes** — Scheffer (2009).

**Signature statistique** : distributions de temps inter-ruptures en
loi de puissance ; allométrie de la taille des firmes / métropoles.

**Applicabilité CPV** : ★★★. Test direct : distribution des durées
inter-crises (Reinhart-Rogoff, Laeven-Valencia 2018) est-elle en
loi de puissance ? Si oui, c'est un argument pour un cadre
punctuated-equilibrium / SOC.

## Famille M — Quantum analogies

> *"Réutiliser le formalisme quantique (intégrales de chemin,
> superposition) comme outil mathématique."*

- **M1. Baaquie** —
  [Baaquie (2004)](bibliographie.md#baaquie-2004). Path integral pour
  options pricing.
- **M2. Schaden (2002)**. Quantum finance.
- **M3. Open quantum systems / decoherence**. Métaphore pour la
  transition micro-macro ou la dispersion d'information.

**Signature statistique** : difficile à isoler ; intérêt surtout
méthodologique (calcul d'expectations).

**Applicabilité CPV** : ★. Cadre intéressant pour pricing dérivés,
peu opérationnel pour le diagnostic des séries macro. Risque de
métaphore vide ("c'est quantique parce que c'est mystérieux").
À garder en réserve.

## Famille N — Cybernétique, bifurcations, catastrophes

> *"Le système change qualitativement quand un paramètre franchit un
> seuil critique."*

- **N1. Théorie des bifurcations** : Hopf, saddle-node, pitchfork,
  transcritique. Régimes qualitativement distincts séparés par
  valeurs critiques.
- **N2. Limit cycles vs équilibres structurellement stables**.
  Question : les "cycles" sont-ils des limit cycles dégradés ou des
  oscillations transitoires autour d'équilibres stables ?
- **N3. Catastrophe theory** — Thom (1972), Zeeman (1977). Sept
  catastrophes élémentaires.

**Signature statistique** : régimes discrets identifiables par
clustering, hystérésis (la trajectoire dépend de l'historique).

**Applicabilité CPV** : ★★★. La théorie des bifurcations est le
langage naturel des "régimes" macro (Great Moderation, Bretton Woods,
post-WWII reconstruction). Tests possibles via régimes markoviens
non-stationnaires.

## Famille O — Cellular automata et calcul universel

> *"Comportement complexe émergent de règles simples locales."*

- **O1. Wolfram Class IV** —
  [Wolfram (2002)](bibliographie.md#wolfram-2002). Comportements
  complexes au edge of chaos.
- **O2. Computational mechanics** — Crutchfield. ε-machines minimales.
- **O3. Reservoir computing** comme test de capacité prédictive
  structurée.

**Signature statistique** : prédictibilité partielle non-périodique ;
ε-machine de taille minimale > 1 état (non-trivial) mais < N (pas
chaotique).

**Applicabilité CPV** : ★★. Théoriquement fertile mais opérationnel-
lement difficile sur séries continues. À garder pour la simulation
ABM future.

## Synthèse — quelle famille pour CPV ?

Tableau d'évaluation pour les 15 familles candidates (1-5 étoiles) :

| Famille | Force conceptuelle | Disponibilité données CPV | Coût implementation | Pouvoir explicatif observé | Verdict |
|---|:---:|:---:|:---:|:---:|---|
| A — SOC + lois de puissance | ★★★★★ | ★★★★★ | ★★ | ★★★★★ | **Tier 1 — prioritaire** |
| B — Multifractalité | ★★★★ | ★★★★★ | ★★ | ★★★★ | **Tier 1** |
| C — Longue mémoire | ★★★★ | ★★★★★ | ★ | ★★★★★ | **Tier 1** |
| D — Chaos déterministe | ★★★ | ★★ | ★★★★ | ★★ | Tier 3 |
| E — Critical slowing down | ★★★★ | ★★★★ | ★★ | ★★★★ | **Tier 1** |
| F — Oscillateurs couplés (Kuramoto, KAM) | ★★★★ | ★★★ | ★★★★ | ★★★ | Tier 2 |
| G — RMT | ★★★★ | ★★★★★ | ★★ | ★★★★ | **Tier 1** |
| H — Verres de spin | ★★★★ | ★ | ★★★★★ | ★★★ | Tier 3 |
| I — Théorie de l'information | ★★★★★ | ★★★★★ | ★ | ★★★★ | **Tier 1** |
| J — Lévy flights | ★★★★ | ★★★★ | ★★ | ★★★★ | **Tier 1** |
| K — Cristaux liquides / topologie | ★★★ | ★ | ★★★★★ | ★★ | Tier 3 |
| L — Biologie évolutionniste | ★★★ | ★★★ | ★★★ | ★★★ | Tier 2 |
| M — Quantum analogies | ★★ | ★ | ★★★★★ | ★ | Tier 3 |
| N — Bifurcations / catastrophes | ★★★★ | ★★ | ★★★ | ★★★ | Tier 2 |
| O — Cellular automata | ★★★ | ★ | ★★★★ | ★★ | Tier 3 |

### Tier 1 (à implémenter en priorité — Roadmap item #15)

Six familles directement testables sur les données CPV existantes
avec des diagnostics statistiques compacts :

1. **Famille A — SOC** : slope spectrale log-log (test 1/f^β), distribution des incréments (test loi de puissance via Hill).
2. **Famille B — Multifractalité** : MF-DFA, spectre f(α).
3. **Famille C — Longue mémoire** : DFA, Hurst exponent.
4. **Famille E — Critical slowing down** : rolling variance + AC1, Kendall-tau.
5. **Famille G — RMT** : Marchenko-Pastur fit sur matrices de corrélation panel.
6. **Famille I — Théorie de l'information** : permutation entropy + statistical complexity.
7. **Famille J — Lévy flights** : fit Lévy stable, test queue lourde.

Ces 7 cadres se testent avec un module compact `ecowave/cycles/alternative_dynamics.py`
(spec dans le roadmap item #15 — voir [feuille de route](methodology/feuille_de_route.md)).

### Tier 2 (à explorer après Tier 1)

- **Famille F — Kuramoto / KAM / pendules multiples**. Coût élevé
  (modèles paramétriques à fitter), mais hautement pertinent si les
  diagnostics Tier 1 pointent vers de la synchronisation partielle.
- **Famille L — Biologie évolutionniste**. Distribution durées
  inter-crises.
- **Famille N — Bifurcations**. Régimes markoviens non-stationnaires.

### Tier 3 (gardés en réserve)

- **Familles D, H, K, M, O**. Conceptuellement intéressantes mais
  soit coût implémentation prohibitif, soit applicabilité statistique
  exotique sur 1D macro time series.

## Limites épistémologiques

Le mot final n'est pas *"la macroéconomie est SOC"* ni *"la
macroéconomie est multifractale"* — c'est *"la macroéconomie n'est
pas un cycle, et voici 15 grilles de lecture alternatives, dont 7
directement testables. À chacun de ces 7 diagnostics, on appliquera
le même protocole strict que pour les cycles : test statistique avec
null hypothesis, surrogates, seuil α=0.05."*

Le programme reste falsifiabiliste — on multiplie les cadres
candidats pour ne pas tomber dans un nouveau dogme. Le succès
empirique d'un cadre alternatif (par ex. "Hurst exponent universellement
> 0.7 sur 80 % des séries CPV") ne valide pas ce cadre seul, mais
ouvre une question : *"qu'est-ce qui produit physiquement de la
longue mémoire dans les séries macro ?"*. Plusieurs des 15 familles
peuvent **coexister** — SOC + Lévy + longue mémoire ne s'excluent
pas mutuellement, elles décrivent des aspects complémentaires.

C'est cette ouverture épistémologique qui distingue CPV d'un projet
unimodal : on multiplie les portes d'entrée plutôt que d'imposer une
seule grille de lecture.

## Référence

Page bibliographique complète : voir
[section "Au-delà des cycles" de bibliographie.md](bibliographie.md#au-dela-des-cycles).

Implémentation diagnostique : voir
[item #15 de la feuille de route](methodology/feuille_de_route.md#item-15-diagnostics-non-cycliques).
