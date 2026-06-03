# Au-delà des cycles — cadres physiques alternatifs pour les séries macroéconomiques

> **Résumé.** Le pipeline CPV a démontré empiriquement que la lecture
> **universaliste sinusoïdale-sur-tout** des cycles canoniques
> Kitchin / Juglar / Kuznets / Kondratieff est rejetée par
> Benjamini-Hochberg FDR sur la grille jointe (V3) — il n'y a pas
> d'horloge cyclique unique au cœur de toute série macro.
> Simultanément, **trois cycles substantifs vindiqués** émergent sur
> les variables que la théorie d'origine prédit (Juglar sur
> investissement/chômage, Kuznets sur HPI/population/crédit, Kitchin
> sur crédit BIS marchés émergents) et **Kondratieff est recasté**
> comme chronologie Reinhart-Rogoff de dette de guerre (V3
> [résumé](papers/cycles_refuted_v3.md)). Cette page documente le
> programme **complémentaire** : si la lecture universaliste est
> rejetée, quelles signatures *non-cycliques* portent la dynamique
> macro ? Le pipeline CPV a démontré que les séries macroéconomiques
> ne sont **pas du bruit blanc** : ACF lag-1 ≈ 1.000, agglomération
> de la volatilité, ruptures structurelles, lois de puissance dans
> les distributions de crashes — autant de signatures de *quelque chose*.
> Cette page passe en revue **21 familles de cadres physiques
> candidats** (15 initiales + 6 ajoutées dans l'extension : cascades
> K41, universalité/MaxEnt, diffusion anormale, réflexivité,
> Tsallis non-extensive, chimera states) qui pourraient rendre compte
> des signatures observées sans présupposer de périodicité. La famille
> S (réflexivité) est traitée à la fois comme une famille à part
> entière et comme **composante transversale obligatoire** : les
> agents économiques observent et anticipent les phénomènes qu'ils
> habitent, ce qui modifie le contenu et la validité des 20 autres
> familles. Le mot final est ouvert : *"la macroéconomie n'est pas
> un cycle, et voici 21 grilles de lecture alternatives, dont 11
> directement testables, toutes amendables par la réflexivité"*.
> Le papier reste falsifiabiliste — on multiplie les cadres pour ne
> pas tomber dans un nouveau dogme.

## Préambule — si pas un cycle universaliste, quoi alors ?

La chaîne d'audits CPV (cf. études de cas
[CN_BIS](case_study_cn_bis_kondratieff.md),
[WLD-WB](case_study_wld_wb_kondratieff.md),
[G7-long & UK_BOE](case_study_g7_long_uk_boe_kondratieff.md),
[Wen 2005 falsifié](case_study_wen_2005_test.md) +
[safeguard Roadmap #14](methodology_safeguard_roadmap_14.md))
et le verdict V3 ([Cycles Refuted V3 portail](papers/cycles_refuted_v3.md))
établissent :

- **Composites macro** : 35 cellules vetoed sur 128 (Roadmap #14), 4 survies authentiques composite — toutes recastées en V3 comme survies *per-variable* sur les canaux substantifs (Juglar/Kuznets/Kitchin), pas comme survies universalistes.
- **Per-variable Gate 1 (V3)** : sur 1 456 cellules testables, 166 positifs Gate 1 unadjusted (excès 2.3×) concentrés sur les variables que la théorie substantive prédit. Mais **0 cellule** ne survit à l'ajustement Benjamini-Hochberg FDR α = 0.05 sur la grille jointe (floor 1/(B+1) > p* = 3.4·10⁻⁵).
- **Séries originales de Kitchin (1923)** : sur le panel sectoriel `SH_*`, 3 / 26 cellules passent Gate 1 unadjusted (US wheat *p*<sub>1</sub> = 0.040, US WPI *p*<sub>1</sub> = 0.015, world coal *p*<sub>1</sub> = 0.020), zéro après BH-FDR — cohérent avec la lecture Wen (2005) que les cycles vivent sur des séries d'inventaire dédiées plutôt que sur composites macro, mais distinguabilité borderline sur ces agrégats historiques spécifiques.

Conclusion : la lecture **universaliste sinusoïdale-sur-tout** est rejetée ; la lecture **variable-spécifique** est tenue pour trois cycles ; Kondratieff est recasté Reinhart-Rogoff. Le programme « au-delà des cycles » ci-dessous documente une signature non-cyclique **complémentaire**, qui pourrait porter la dynamique macro à côté des trois cycles substantifs vindiqués.

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

## Famille P — Cascades multi-échelle et turbulence (Kolmogorov)

> *"L'énergie cascade des grandes vers les petites échelles, avec
> intermittence. Mécanisme générateur de la multifractalité."*

- **P1. Kolmogorov K41** —
  [Kolmogorov (1941)](bibliographie.md#kolmogorov-1941). Théorie
  statistique de la turbulence : spectre d'énergie E(k) ∝ k^{-5/3}
  dans la zone inertielle. Cascade d'énergie multi-échelle depuis les
  grandes vers les petites échelles, dissipation viscosulle à
  l'échelle de Kolmogorov.
- **P2. Frisch synthèse moderne** —
  [Frisch (1995)](bibliographie.md#frisch-1995). Corrections multifractales
  (β-model, p-model), intermittence anomale.
- **P3. Cascades en finance** —
  [Ghashghaie et al. (1996)](bibliographie.md#ghashghaie-1996). Démonstration
  empirique : volatilité des taux de change obéit aux mêmes lois
  multi-échelle que la turbulence.

**Différence avec la famille B (multifractalité)** : B *décrit*, P
*explique le mécanisme*. La famille B observe la signature multifractale ;
P propose pourquoi (cascade d'énergie/information à travers les
échelles).

**Signature statistique** : pente spectrale −5/3 (ou exposants
voisins) dans la zone inertielle, queues distribution incréments
qui s'élargissent à mesure que l'échelle de temps diminue,
exposants de scaling ζ(p) non-linéaires en p (intermittence).

**Applicabilité CPV** : ★★★★. Testable directement sur la
volatilité réalisée (squared returns) des séries longues
(BoE 316 ans, JST 152 ans). Si la pente spectrale et les exposants
ζ(p) correspondent au K41 corrigé, on a un cadre **mécaniste**
pour la multifractalité observée.

## Famille Q — Universalité statistique et choix de modèle (renormalisation, MaxEnt)

> *"Pourquoi des systèmes différents montrent les mêmes signatures
> statistiques ? Comment choisir parmi les 21 familles candidates ?"*

- **Q1. Groupe de renormalisation** —
  [Wilson (1971)](bibliographie.md#wilson-1971). Prix Nobel 1982.
  Explique l'**universalité** : des systèmes microscopiquement très
  différents (ferromagnétiques, liquides, supraconducteurs) montrent
  les mêmes exposants critiques près des transitions de phase
  parce qu'ils appartiennent à la même **classe d'universalité**.
- **Q2. Maximum Entropy Principle** —
  [Jaynes (1957)](bibliographie.md#jaynes-1957). La distribution la
  moins informative compatible avec les contraintes observées maximise
  l'entropie de Shannon. **Méta-cadre pour le choix de modèle** :
  parmi 21 familles candidates, laquelle est la plus parcimonieuse
  étant donné les signatures observées sur CPV ?

**Caractère méta** : cette famille n'est pas un cadre concurrent
des 20 autres mais un **outil pour les arbitrer entre elles**.

**Signature statistique** : ratios d'exposants prédictibles entre
séries de natures différentes (équivalence de classe d'universalité) ;
choix de modèle via critère information (AIC, BIC, MDL).

**Applicabilité CPV** : ★★★★. Test direct : les exposants Hurst,
multifractal Δα, slope spectrale 1/f^β, kurtosis, etc., présentent-ils
des **regroupements** par classe (financier vs réel, AE vs EM,
court vs long terme) ? Si oui, on a une confirmation d'universalité.

## Famille R — Diffusion anormale

> *"Comment l'écart-type d'une série grandit-il avec le temps ?"*

- **R1. Mean Square Displacement scaling** —
  [Metzler & Klafter (2000)](bibliographie.md#metzler-klafter-2000).
  MSD(t) ~ t^α avec α ≠ 1. **Sub-diffusion** (α<1) : piégeage,
  mémoire, viscoélasticité. **Super-diffusion** (α>1) : sauts longs,
  vols actifs.
- **R2. Continuous Time Random Walk (CTRW)** — Montroll & Weiss (1965).
  Cadre théorique unifié des marches avec distribution de waiting times
  et sauts.
- **R3. Équations de diffusion fractionnaires** — Metzler-Klafter.
  ∂^α u / ∂t^α = D ∂² u / ∂x².

**Différence avec familles C (longue mémoire) et J (Lévy flights)** :
- C caractérise l'**autocorrélation** (mémoire temporelle).
- J caractérise la **distribution des incréments** (taille des sauts).
- R caractérise la **croissance de l'écart-type** (transport temporel).

Les trois peuvent coexister et se renforcer mutuellement.

**Signature statistique** : MSD(t) ~ t^α avec α ≠ 1. Test : régression
log-log de MSD sur t.

**Applicabilité CPV** : ★★★★. Test direct sur le rapport
écart-type / racine du temps pour différentes échelles temporelles
(annuelle, trimestrielle, mensuelle quand disponible). Si on trouve
α = 0.5-0.7 (sub-diffusion) sur CY_FIN ou LH_DEBTGDP, on identifie
un type spécifique de longue mémoire (avec mécanisme de piégeage).

## Famille S — Réflexivité et anticipation des agents

> *"Les agents économiques observent et anticipent le système qu'ils
> habitent. La grille du physicien doit intégrer l'observateur."*

- **S1. Réflexivité** —
  [Soros (1987, 2008)](bibliographie.md#soros-1987). Les croyances
  des participants influencent la réalité économique qu'ils prétendent
  observer. Boucle de rétroaction **fondamentalement non-stationnaire** :
  une perception biaisée crée la réalité qu'elle anticipait, qui
  modifie alors les perceptions, etc.
- **S2. Free Energy Principle / Active Inference** —
  [Friston (2010)](bibliographie.md#friston-2010). Les systèmes
  biologiques minimisent leur énergie libre variationnelle = borne
  supérieure de la surprise bayésienne. Unifie perception, action,
  inférence. Transférable à la modélisation d'agents qui inférent
  et anticipent.
- **S3. Animal spirits** —
  [Akerlof & Shiller (2009)](bibliographie.md#akerlof-shiller-2009).
  Reprise contemporaine de Keynes. Comportements collectifs (confiance,
  équité, histoires partagées) comme moteurs primaires des fluctuations
  macro.
- **S4. Bounded rationality** — Simon (1955). Agents à capacité
  cognitive limitée, satisficing plutôt qu'optimisation.

**Position épistémologique unique** : cette famille **n'est pas un
phénomène physique à fitter sur les données** — c'est une
**pré-condition** sur ce que peuvent être les autres familles. Voir
section "Composante transversale" ci-dessous.

**Signature statistique** : non-stationnarité endogène, ruptures
structurelles synchronisées avec changements de paradigme collectif,
distributions de croyances avec modalités multiples (cf. surveys
d'anticipations).

**Applicabilité CPV** : ★★★. Test indirect via les régimes
identifiés (Great Moderation, Bretton Woods, post-2008 — chacun
peut être lu comme une période de cohérence des anticipations
collectives). Beaucoup plus difficile à formaliser que les familles
A-O ; intérêt principalement conceptuel.

## Famille T — Thermodynamique non-extensive (Tsallis)

> *"Généraliser l'entropie de Boltzmann-Gibbs pour systèmes avec
> longue mémoire, fractalité et interactions à longue portée."*

- **T1. Entropie de Tsallis** —
  [Tsallis (1988)](bibliographie.md#tsallis-1988). `S_q = (1 - Σ p_i^q) / (q-1)`.
  Pour q→1 : Boltzmann-Gibbs. Pour q≠1 : distributions stationnaires
  en loi de puissance (q-Gaussiennes, q-exponentielles).
- **T2. Distributions q-Gaussiennes** universelles : pour
  q ∈ ]1, 3[, queues lourdes en loi de puissance. Observées
  empiriquement sur returns financiers, taux de change, températures.

**Cadre unifié** : englobe les familles A (SOC), B (multifractal),
C (longue mémoire) et J (Lévy) sous une même **statistique
généralisée**. Le paramètre q mesure l'écart à l'équilibre
Boltzmann-Gibbs et indique le **type de non-extensivité**.

**Signature statistique** : ajustement de q-Gaussiennes à la
distribution des incréments — q ≈ 1.4-1.6 typique pour returns
financiers, q = 1 pour bruit blanc, q > 2 pour distributions très
lourdes.

**Applicabilité CPV** : ★★★★. Fit immédiat de la distribution des
incréments annuels (BoE 316 ans, JST 152 ans) à la famille
q-Gaussienne. Si q s'écarte significativement de 1, on a une
preuve directe de non-extensivité et un paramètre unique qui
**résume** plusieurs signatures (queues, mémoire, fractalité).

## Famille U — Synchronisation partielle (chimera states)

> *"Sur un même substrat d'oscillateurs identiques, des zones
> synchronisées et désordonnées peuvent coexister stablement."*

- **U1. Chimera states** —
  [Kuramoto & Battogtokh (2002)](bibliographie.md#kuramoto-battogtokh-2002),
  [Abrams & Strogatz (2004)](bibliographie.md#abrams-strogatz-2004).
  Sur un anneau d'oscillateurs identiques avec couplage non-local,
  une partie se synchronise tandis que le reste reste désordonné —
  les deux phases coexistent stablement.
- **U2. Multi-cluster synchronization**. Plusieurs sous-groupes
  synchronisés sur des phases différentes.
- **U3. Phase-coherent transitions** — les chimera peuvent migrer,
  se fragmenter, se reformer.

**Pertinence pour CPV** : explique pourquoi certains agrégats du
panel CPV semblent porter un cycle (G7-long K, ADV18 dans certaines
runs) tandis que d'autres voisins le rejettent (USA-long, ANGLO).
**Pas d'agrégation artefactuelle ni de signal vraiment universel**,
mais des **zones de synchronisation partielle** sur un substrat
hétérogène.

**Signature statistique** : matrice de cohérence cross-séries avec
**structure de cluster** (groupes synchronisés vs groupes désordonnés),
distribution bimodale des phases de Hilbert dans une fenêtre roulante.

**Applicabilité CPV** : ★★★. Tests via cohérence wavelet pairwise
sur le panel JST 18 économies. Si on observe des sous-groupes de
3-5 économies synchronisées coexistant avec d'autres désordonnées,
c'est un **chimera** plutôt qu'un cycle global.

## Composante transversale — la réflexivité reshape les 20 familles

> *"Les familles A-R et T-U décrivent des systèmes physiques. Or les
> agents économiques **observent et anticipent** ce qu'ils habitent.
> La famille S n'est pas seulement une famille — c'est une condition
> de validité pour les autres."*

Toutes les familles physiques A-R, T-U héritent de propriétés que
les systèmes naturels ont : Markov property, ergodicité asymptotique,
exogéneité du paramètre observé. Les systèmes macroéconomiques
**n'ont aucune de ces propriétés** parce que les agents
**réfléchissent** sur eux-mêmes. Chaque famille doit donc être
amendée :

| Famille | Composante réflexivité (Soros/Friston/Akerlof-Shiller) |
|---|---|
| **A — SOC** | L'observation collective d'une approche du point critique modifie le moment de l'avalanche. Endogeneité de la criticité. |
| **B — Multifractalité** | Les anticipations créent de nouvelles échelles d'organisation (intraday algorithmique vs hebdomadaire vs cycle politique). Le spectre f(α) est **time-varying**. |
| **C — Longue mémoire** | La mémoire est partiellement **cognitive collective** (souvenir partagé des crises 1929, 1973, 2008), pas seulement statistique. Hurst exponent varie avec les générations. |
| **D — Chaos déterministe** | L'observation modifie la trajectoire (feedback réflexif). Pas de séparation propre observateur-système. |
| **E — Critical slowing down** | Les early-warning signals **identifiés sont exploités** par les agents sophistiqués, modifiant ainsi la dynamique de slowdown elle-même. Self-fulfilling. |
| **F — Kuramoto / KAM** | Les coupling strengths entre agents dépendent des **anticipations sur les anticipations** (mimétisme keynésien). Coupling time-varying. |
| **G — RMT** | Une fois identifiées et publiées, les eigenvalues "bulk-deviating" sont arbitrées, modifiant la matrice de corrélation elle-même. Goodhart's law spectral. |
| **H — Verres de spin** | Le free energy landscape est **endogène** : les choix passés modifient la topographie pour les choix futurs. |
| **I — Théorie de l'information** | L'observateur est partie du système (canal de Shannon auto-référentiel). |
| **J — Lévy flights** | Les queues lourdes reflètent **les anticipations d'extrêmes par les agents**, non un processus stochastique exogène. |
| **K — Cristaux liquides** | L'order parameter est partiellement **cognitif** (croyance collective sur la phase). Hystérésis lors des transitions de phase macroéconomiques. |
| **L — Punctuated equilibrium** | Les rates of change dépendent de la **conscience collective** de la stase ou de la rupture (récits, médias). |
| **M — Quantum** | Le problème de la mesure est explicite — directement transférable. |
| **N — Bifurcations** | Les bifurcation parameters incluent les **anticipations collectives** sur la valeur critique du paramètre. |
| **O — Cellular automata** | Les règles peuvent être **modifiées par apprentissage des agents** (meta-learning). |
| **P — Cascades K41** | Les cascades inter-échelle sont biaisées par les **stratégies trading inter-fréquence** (HFT vs swing trade vs investisseur LT). |
| **Q — Universalité** | Les classes d'universalité incluent une **classe humaine** : on retrouve les mêmes signatures parce que les structures cognitives convergent. |
| **R — Diffusion anormale** | Les "pièges" sub-diffusifs sont souvent des **points focaux d'attention collective** (niveaux psychologiques, événements politiques attendus). |
| **T — Tsallis** | Le paramètre q non-extensif reflète la **densité de l'interaction sociale** dans le système — corrigible empiriquement. |
| **U — Chimera states** | Les zones synchronisées sont des **communautés d'anticipation partagée**, séparées des zones désordonnées par hétérogénéité des croyances. |

**Conséquence méthodologique** : tout cadre physique appliqué à
des séries macro doit **soit** modéliser explicitement la réflexivité
(ajout d'une couche d'anticipations bayésiennes Friston-like),
**soit** assumer explicitement une limite de validité (par exemple
"valide sur fenêtres courtes où les anticipations sont stables").

C'est pourquoi la famille S est **dédoublée** : sa propre famille
ET composante transversale des 20 autres. Le panorama n'est pas une
liste plate de 21 candidats indépendants, mais une **matrice 20 × 1**
où chaque famille est conditionnellement modifiée par la réflexivité.

## Synthèse — quelle famille pour CPV ?

Tableau d'évaluation pour les 21 familles candidates (1-5 étoiles) :

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
| **P — Cascades K41 / turbulence** | ★★★★★ | ★★★★ | ★★★ | ★★★★ | **Tier 1** |
| **Q — Universalité / RG / MaxEnt** (méta) | ★★★★★ | ★★★★ | ★★ | ★★★★ | **Tier 1 méta** |
| **R — Diffusion anormale** | ★★★★ | ★★★★ | ★★ | ★★★★ | **Tier 1** |
| **S — Réflexivité (transversale)** | ★★★★★ | ★★★ | ★★★★★ | ★★★ | **Composante transversale** |
| **T — Tsallis non-extensive** | ★★★★ | ★★★★★ | ★★ | ★★★★ | **Tier 1** |
| **U — Chimera states** | ★★★★ | ★★★★ | ★★★ | ★★★★ | Tier 2 |

### Tier 1 (à implémenter en priorité — Roadmap item #15)

Onze familles directement testables sur les données CPV existantes
avec des diagnostics statistiques compacts (les 7 originales + P, R, T
ajoutées dans cette extension ; Q comme méta-cadre ; S comme
composante transversale obligatoire) :

1. **Famille A — SOC** : slope spectrale log-log (test 1/f^β), distribution des incréments (test loi de puissance via Hill).
2. **Famille B — Multifractalité** : MF-DFA, spectre f(α).
3. **Famille C — Longue mémoire** : DFA, Hurst exponent.
4. **Famille E — Critical slowing down** : rolling variance + AC1, Kendall-tau.
5. **Famille G — RMT** : Marchenko-Pastur fit sur matrices de corrélation panel.
6. **Famille I — Théorie de l'information** : permutation entropy + statistical complexity.
7. **Famille J — Lévy flights** : fit Lévy stable, test queue lourde.
8. **Famille P — Cascades K41** : exposants de scaling ζ(p), pente spectrale dans la zone inertielle.
9. **Famille R — Diffusion anormale** : régression log-log MSD(t).
10. **Famille T — Tsallis non-extensive** : ajustement q-Gaussien à la distribution des incréments.
11. **Famille Q (méta) — Universalité / MaxEnt** : regroupement des exposants par classe d'universalité, sélection MDL/AIC du meilleur modèle.

**Composante transversale obligatoire** : **Famille S (réflexivité)**
doit être intégrée dans chaque test Tier 1 sous une des deux formes :
soit modélisation explicite (couche bayésienne d'anticipations type
Friston), soit limite de validité affichée ("résultat valable sur la
fenêtre 1980-2020 où le régime cognitif collectif est stable").

Ces cadres se testent avec un module compact `ecowave/cycles/alternative_dynamics.py`
(spec dans le roadmap item #15 — voir [feuille de route](methodology/feuille_de_route.md)).

### Tier 2 (à explorer après Tier 1)

- **Famille F — Kuramoto / KAM / pendules multiples**. Coût élevé
  (modèles paramétriques à fitter), mais hautement pertinent si les
  diagnostics Tier 1 pointent vers de la synchronisation partielle.
- **Famille L — Biologie évolutionniste**. Distribution durées
  inter-crises.
- **Famille N — Bifurcations**. Régimes markoviens non-stationnaires.
- **Famille U — Chimera states**. À tester via cohérence wavelet
  pairwise sur le panel JST 18 économies pour identifier les clusters
  de synchronisation partielle.

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
