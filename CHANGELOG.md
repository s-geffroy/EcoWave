# Changelog

All notable changes to the project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased] — Cycle Position Vector (CPV) framework

### Implications du verdict — page conceptuelle + 3 items roadmap (#19-#21)

Suite à la livraison du verdict empirique (cluster C+B+D+I+S, sprint
#15+#27) le projet manquait d'une cartographie des *implications* du
verdict — modélisation, prévision, politique, théorie. Cette
livraison comble ce trou avec :

**Page conceptuelle `docs/implications_of_cluster.md`** (~3 900 mots,
5 sections + sign-off) intégrée à mkdocs sous "6. Working paper" :

1. *Le verdict en clair* — rappel du cluster C+B+D+I+S, ce qui est
   réfuté (SOC pur, CSD, chaos déterministe).
2. *Implications pour la modélisation* — 5 familles candidates
   informées par recherche bibliographique substantielle : MSM
   (Calvet-Fisher), ARFIMA+RS (Bhardwaj-Swanson), HAR (Corsi),
   MRW (Bacry-Muzy-Delour), HABM (Lux-Marchesi), AMH (Lo). *Aucun
   modèle ne couvre les 5 piliers simultanément.*
3. *Implications pour la prévision* — l'horizon compte (long-memory
   dominate à 6+ mois), comparateurs canoniques (FOMC SEP, ECB BMPE,
   SPF), métriques propres (CRPS Gneiting-Raftery, coverage 95 %,
   tail coverage), régime-conditioning (pré/post-2008,
   pré/COVID/post-COVID).
4. *Implications pour la politique économique* — inflation targeting
   et crédibilité monétaire, macroprudentiel/Bâle, VaR vs Expected
   Shortfall, horizons de forecasting des autorités, réflexivité
   communicationnelle.
5. *Implications pour la théorie* — cycle → cascade, DSGE en
   accusation, cycles narratifs vs mécanistes, synthèse théorique
   manquante (Active inference + MRW + AMH ?).

**Trois nouveaux items roadmap** dans `methodology/feuille_de_route.md` :

- **#19** — Page conceptuelle (LIVRÉE par ce sprint).
- **#20** — Benchmark de modélisation : MSM + HAR + ARFIMA+RS vs
  baselines. Nouveau module `ecowave/forecasting/`, CLI
  `ecowave forecast-benchmark`. ~15 jours d'effort. Acceptance :
  au minimum 1 modèle du cluster doit battre random walk en
  out-of-sample CRPS à 12 mois sur ≥ 50 % des variables testées.
- **#21** — Bibliographie enrichie modélisation post-cluster. ~0.5
  jour. LIVRÉE par ce sprint.

**Bibliographie enrichie** (`docs/bibliographie.md`) avec **15
nouvelles références** couvrant les 5 familles de modélisation du
cluster :

- Beran (1994), Bhardwaj-Swanson (2006), Borio (2014),
  Brock-Hommes (1998), Calvet-Fisher (2002, 2004, 2008),
  Corsi (2009), Drehmann-Borio-Tsatsaronis (2012),
  Gneiting-Raftery (2007), Hommes (2006), Hosking (1981),
  Lo (2017), Lux-Marchesi (1999), Sornette-Johansen-Bouchaud (1996).

**Lien V2 papier** : la page `implications_of_cluster.md` fournit la
matière pour la nouvelle section §6 du working paper V2
*"Constructive replacement — implications et benchmark"*.

### Diagnostics non-cycliques — toolkit Tier 1 (roadmap #15)

Livraison du toolkit `ecowave dx-diagnostics` qui complète le panorama
"au-delà des cycles" avec **11 diagnostics statistiques compacts** couvrant
les familles Tier 1 :

1. **DFA / Hurst** (famille C — longue mémoire) — `nolds`-free réimplémentation Peng et al. 1994.
2. **MF-DFA Δα** (famille B — multifractalité) — Kantelhardt et al. 2002, q ∈ {-5,-3,-1,1,3,5}.
3. **Slope spectrale 1/f^β** (famille A — SOC) — Welch + polyfit log-log.
4. **Hill α_tail** (famille A — queues de loi de puissance) — Hill 1975.
5. **Permutation entropy + complexité LMC** (famille I — information) — Bandt-Pompe + López-Ruiz-Mancini-Calbet.
6. **Critical slowdown** (famille E — tipping point) — Kendall τ sur variance roulante, Dakos et al. 2008.
7. **Lévy stable α** (famille J — vols de Lévy) — McCulloch 1986 quantile estimator.
8. **K41 scaling ζ(6)/ζ(3)** (famille P — cascades turbulence) — Frisch 1995.
9. **MSD γ** (famille R — diffusion anormale) — Metzler-Klafter 2000.
10. **Tsallis q** (famille T — non-extensivité) — proxy kurtosis.
11. **Reflexivity drift KS** (famille S — composante transversale Soros + Friston) — KS deux-échantillons entre les deux moitiés de la fenêtre.

**Panel-level** : `rmt_panel` (famille G — RMT) calcule le spectre de
covariance et compare à la bande Marchenko-Pastur.

**Architecture** : module `ecowave/cycles/alternative_dynamics.py` (~1100
lignes) + refactor de `ecowave/cycles/surrogate.py` qui délègue
maintenant à `ecowave/cycles/surrogate_generators.py` (`ar1_surrogate_series`,
`phase_scramble_surrogate_series`) en briques réutilisables. Le contrat
de non-régression Gate 1 est vérifié par `tests/test_surrogate_generators.py`
(seed-stable, p-values identiques avant/après refactor).

**Null wrapper unifié** : chaque diagnostic atomique est scoré contre
AR(1) ou phase-scramble selon ce qui fait sens physiquement (cf. tableau
dans le module). Tail-test choisi par diagnostic : upper (Hurst, β, Δα,
ζ, q, KS), lower (perm-entropy, α_Hill, α_Lévy), two-sided (MSD γ).

**Décision design : pas de découpage 4-cycles.** Les diagnostics
mesurent des propriétés **structurelles globales** des séries, pas
band-spécifiques. Réintroduire un axe `cycle ∈ {kitchin, juglar, kuznets,
kondratieff}` recréerait le scaffold cyclique précisément falsifié. La
page `docs/dx_diagnostics.md` est structurée comme **diagnostic ×
variable × horizon** (3 axes).

**Lecture transversale réflexivité (famille S).** Conformément à PR #22,
la famille S est traitée comme composante transversale obligatoire. Le
diagnostic `reflexivity_drift` sert d'indicateur de validité des 10
autres : quand il rejette le null, les statistiques structurelles
(Hurst, β, Δα, …) sont valables uniquement sur la fenêtre analysée, pas
comme lois universelles transhistoriques.

**Dépendances ajoutées** : `nolds==0.6.2`, `antropy==0.1.7` dans
`requirements.txt` (rebuild Docker requis). Diagnostics 3-7 et 8-11
utilisent uniquement scipy/numpy déjà présents ; les libs externes sont
là pour permettre un futur swap des implémentations custom (DFA,
permutation entropy) vers les implémentations peer-reviewed si besoin.

**Tests** : 17 tests unitaires sur les 11 diagnostics + 8 tests de
non-régression sur les générateurs surrogate. Coverage des cas : bruit
blanc (référence neutre), marche aléatoire (mémoire infinie / β=2 / H=1),
distribution Pareto (heavy-tailed), série avec rupture de régime
(réflexivité).

**Sortie** : `reports/dx_diagnostics_{as_of}_{horizon}.json` (per-variable)
+ `reports/dx_rmt_{as_of}_{horizon}.json` (panel-level) + page
`docs/dx_diagnostics.md` consolidée avec heatmaps emoji-codées et
synthèse cross-horizon.

**Cohabitation Gate 1 ↔ diagnostics non-cycliques.** Les 4 cycles
canoniques (Kitchin/Juglar/Kuznets/Kondratieff) restent la cible de
falsification dans Gate 1/2/3. Item #15 ajoute un étage parallèle qui
ne touche pas à la taxonomie cyclique. Une décision data-driven d'ajout
/ retrait de cycle (ex: Toynbee 60-120y ou retrait au profit de fBm)
sera prise après les premiers runs, dans une PR séparée avec
pré-enregistrement explicite.

**Roadmap #16 pré-enregistré : étude per-band vs band-agnostique.** La
décision design "pas de découpage 4-cycles" de l'item #15 sera *testée
empiriquement* dans une PR ultérieure (item #16 dans la feuille de
route) : appliquer 4 diagnostics (β, τ_var, α_Lévy, Hurst) au signal
CF-bandpassé dans chacune des 4 bandes canoniques, puis comparer
directement avec la version band-agnostique. Si per-band n'ajoute pas
d'info, la décision design de #15 est validée empiriquement (pas juste
affirmée). Si per-band révèle des structures internes, nouvelle question
de recherche pour #17.

### Au-delà des cycles — extension à 21 familles + composante transversale de réflexivité

Extension du panorama initial (15 → 21 familles) pour combler trois
angles morts identifiés :

1. **Mécanisme générateur** vs description : la famille **B
   (multifractalité)** observe la signature ; la nouvelle **famille
   P — cascades multi-échelle (Kolmogorov K41)** propose le
   mécanisme physique qui la génère ([Frisch 1995](docs/bibliographie.md#frisch-1995),
   [Ghashghaie et al. 1996](docs/bibliographie.md#ghashghaie-1996)
   sur la turbulence des taux de change).
2. **Méta-cadre du choix de modèle** : ajout de la nouvelle
   **famille Q — universalité statistique et MaxEnt** (groupe de
   renormalisation de [Wilson (1971)](docs/bibliographie.md#wilson-1971),
   maximum d'entropie de [Jaynes (1957)](docs/bibliographie.md#jaynes-1957))
   comme cadre pour arbitrer entre les 20 autres familles.
3. **Caractérisation temporelle de la diffusion** : nouvelle
   **famille R — diffusion anormale** ([Metzler & Klafter (2000)](docs/bibliographie.md#metzler-klafter-2000)),
   complétant les familles C (autocorrélation) et J (queues) avec
   un troisième angle (MSD scaling).
4. **Statistique unifiée** : nouvelle **famille T — Tsallis
   non-extensive** ([Tsallis (1988)](docs/bibliographie.md#tsallis-1988))
   comme cadre généralisé englobant SOC, multifractalité, longue
   mémoire et Lévy sous une même formulation.
5. **Hétérogénéité spatiale** : nouvelle **famille U — chimera
   states** ([Kuramoto & Battogtokh (2002)](docs/bibliographie.md#kuramoto-battogtokh-2002),
   [Abrams & Strogatz (2004)](docs/bibliographie.md#abrams-strogatz-2004))
   pour expliquer la coexistence stable de zones synchronisées et
   désordonnées sur le même substrat — analogie directe pour les
   patterns d'agrégats CPV.

**Famille S — réflexivité et anticipation des agents** est
introduite avec un **double statut** :
- **Famille à part entière** : Soros ([1987 / 2008](docs/bibliographie.md#soros-1987)),
  Friston ([2010](docs/bibliographie.md#friston-2010)) free energy
  principle, Akerlof & Shiller ([2009](docs/bibliographie.md#akerlof-shiller-2009))
  animal spirits.
- **Composante transversale obligatoire** des 20 autres familles.
  Une nouvelle section *"La réflexivité reshape les 20 familles"*
  publie un tableau de **21 lignes × 1 colonne** précisant pour
  chaque famille comment l'anticipation des agents modifie le
  contenu (endogeneité de la criticité pour A, mémoire cognitive
  pour C, Goodhart spectral pour G, etc.). Tout cadre physique
  appliqué à des séries macro doit soit modéliser explicitement la
  réflexivité (couche bayésienne Friston-like), soit afficher sa
  limite de validité.

**Roadmap item #15 mis à jour** : le toolkit de diagnostics passe de
7 à **11 diagnostics Tier 1** (ajout : exposants ζ(p) K41 pour
cascades, MSD scaling pour diffusion anormale, fit q-Gaussien
Tsallis, regroupement universalité par classe Q). La composante
réflexivité est obligatoire en clause de validité.

**Bibliographie** enrichie de 13 nouvelles références (Abrams-Strogatz,
Akerlof-Shiller, Frisch, Friston, Ghashghaie, Jaynes, Kolmogorov,
Kuramoto-Battogtokh, Metzler-Klafter, Soros, Tsallis, Wilson) + une
nouvelle section ## F (Frisch, Friston) précédemment manquante.
Section thématique *"Au-delà des cycles — références par famille"*
étendue aux familles P à U.

### Au-delà des cycles — panorama de 15 cadres physiques alternatifs

Suite à la chaîne d'audits (PRs #15-20) qui a démontré l'absence de
cycles authentiques à tous les niveaux du protocole CPV (composites
macro, variables individuelles, séries originales des découvreurs),
ouverture du chantier *positif* du papier : si les cycles n'existent
pas, par quoi sont remplacés les phénomènes observés (ACF ≈ 1.000,
agglomération de la volatilité, queues lourdes, ruptures
structurelles) ?

**Nouvelle page** `docs/methodology_beyond_cycles.md` (~700 lignes)
publie un panorama de **15 familles de cadres physiques candidats**,
organisées en 3 tiers d'applicabilité :

- **Tier 1** (7 cadres directement testables) : SOC + lois de
  puissance (Bak 1996, Sornette 2003), multifractalité
  (Bacry-Muzy-Delour 2001, Kantelhardt 2002), longue mémoire
  (Hurst 1951, Mandelbrot 1997), critical slowing down
  (Scheffer 2009, Dakos 2008), RMT (Bouchaud-Potters 2003,
  Marchenko-Pastur 1967), théorie de l'information
  (Bandt-Pompe 2002, Schreiber 2000, Crutchfield-Young 1989),
  Lévy flights (Mantegna-Stanley 1999).
- **Tier 2** : oscillateurs couplés / Kuramoto / KAM / pendules
  multiples (Kuramoto 1984, Strogatz 2003) ; biologie évolutionniste
  (Gould-Eldredge 1972, West-Brown-Enquist 1997) ; bifurcations
  / catastrophes (Thom 1972).
- **Tier 3** : chaos déterministe (Takens 1981, Grassberger-Procaccia
  1983), verres de spin (Mézard-Parisi-Virasoro 1987), soft matter /
  cristaux liquides (De Gennes 1974), quantum analogies
  (Baaquie 2004), cellular automata (Wolfram 2002).

Pour chaque famille : description conceptuelle, références-clé,
**signature statistique attendue**, et applicabilité au matériau CPV
(★1-5).

**Enrichissement `docs/bibliographie.md`** : 28 nouvelles références
physique réparties dans les sections A-W de la biblio + nouvelle
section *"Au-delà des cycles — références par famille"* qui regroupe
par famille.

**Roadmap item #15** (TODO) ajouté à `methodology/feuille_de_route.md` :
plan d'implémentation pour la session suivante d'un module
`ecowave/cycles/alternative_dynamics.py` avec 7 diagnostics
statistiques compacts (DFA/Hurst, MF-DFA, slope spectrale 1/f,
permutation entropy + complexity, critical slowing down,
Lévy stable fit, RMT analysis) appliqués à toutes les séries CPV.
Chaque diagnostic accompagné d'un null hypothesis test (philosophie
Gate 1 reproduite hors paradigme cyclique).

**Position épistémologique explicite** : *"la macroéconomie n'est
pas un cycle, et voici 15 grilles de lecture alternatives, dont 7
directement testables"*. Le programme reste falsifiabiliste — on
multiplie les cadres candidats pour ne pas tomber dans un nouveau
dogme post-cycle.

### Roadmap #13 Phase 3 — Substitut Mitchell IHS via FRED + OWID + DECC/BEIS : Wen 2005 falsifié

Substitut ouvert au Mitchell IHS (paywall Springer Palgrave) via :
- **FRED** (NBER Macrohistory + BLS PPI, CC0) — 8 séries sectorielles US
- **OWID grapher** (CC BY 4.0) — World coal + oil 1900-2024
- **OWID legacy + DECC/BEIS** (OGL-UK-3.0) — UK coal 1853-2019

**11 séries × 3 groupes** :
- `US_SH` (8 vars 1856-2026) : SH_US_WPI, INDPROD, COAL, STEEL, PIGIRON, RAILFREIGHT, WHEAT, COTTON
- `UK_SH` (1 var 1853-2019) : SH_UK_COAL
- `WORLD_SH` (2 vars 1900-2024) : SH_WORLD_COAL, SH_WORLD_OIL

**Test décisif Wen (2005)** : Kitchin (3-5 ans) doit survivre sur les
séries sectorielles d'inventaire/production là où il échoue sur les
composites macro.

**Verdict : Wen (2005) falsifié empiriquement.**

| Niveau | Cellules testées | Kitchin survivants |
|---|---|---|
| Composite Gate 1 | 12 (3 groupes × 4 cycles) | 0 (1 vetoed par safeguard #14) |
| **Per-variable Gate 1** | **44 (11 vars × 4 cycles)** | **0** |

Aucune des 11 séries sectorielles — y compris les variables originales
de Kitchin (1923) (production charbon, fonte, fret, blé, coton) — ne
porte de cycle Kitchin détectable au niveau individuel à α=0.05.
Min p-value : `SH_US_PIGIRON Kitchin p=0.188` — loin de tout seuil
honnête.

Le rejet des cycles canoniques est désormais empiriquement étendu à :
1. Tous les composites macroéconomiques (Phases 0-2)
2. **Toutes les séries sectorielles individuelles** (Phase 3)
3. Toutes les bandes cycliques (Kitchin/Juglar/Kuznets/Kondratieff)

**Confirmation maximale de la thèse centrale CPV** —
[Garvy 1943](docs/bibliographie.md#garvy-1943) →
[Solomou 1987](docs/bibliographie.md#solomou-1987) →
[Maddison 1991](docs/bibliographie.md#maddison-1991) →
[Wen 2005 lui-même](docs/bibliographie.md#wen-2005) tous validés
empiriquement par le protocole strict.

- Nouveau module `ecowave/cycles/sectoral_history.py`
- Nouveau manifest `sectoral_history_manifest.json`
- Nouveau downloader `scripts/download_sectoral_history.sh`
- Nouvel horizon `position-cycles --horizon sh`
- Nouvelle page `docs/case_study_wen_2005_test.md` (section 1 nav)
- Nouvelle ligne dashboard home : US_SH / UK_SH / WORLD_SH
- Fix collatéral : `_analyse_and_render` skip figures non écrites (analogue PR #12 sur polar Kuznets)

### Roadmap #14 — garde-fou per-variable systématique

Nouveau garde-fou universel dans `_analyse_and_render` : pour publier
une cellule `(agrégat, cycle)` comme survivante, exiger qu'**au moins
une variable individuelle** de `band_panel` survive Gate 1
dual-null sur la même bande (avec différenciation pour K).

Mécanique :
- Pour chaque cellule, calculer le composite Gate 1 (inchangé).
- Si composite REJETTE → publier `rejected` (inchangé).
- Si composite SURVIT → lancer `_per_variable_gate1_check` sur le
  sous-ensemble `band_panel` filtré par `cycle_targets`.
- Si 0 variable testable ne survit individuellement → basculer
  en `rejected` avec note `Roadmap #14 veto: composite p=X but
  0/N individual variables survive Gate 1`.
- Sinon → publier le composite normalement.

**Résultats sur le pipeline complet** (5 horizons, 128 cellules) :

| Horizon | Survivors | Vetoed | Total |
|---|---:|---:|---:|
| WB | **0** | 10 | 32 |
| Q | **0** | 5 | 24 |
| Long | 3 | 8 | 24 |
| BoE | **0** | 2 | 4 |
| BIS | 1 | 10 | 44 |
| **Total** | **4** | **35** | **128** |

**4 cellules survivent post-safeguard, étayées par variables** :
- `G7-long K` (LH_GDP + LH_RGDP_BARRO survivent en différencié)
- `EU4-long K` (LH_DEBTGDP + LH_RGDP_BARRO en diff)
- `NORDIC-long K` (LH_DEBTGDP en diff)
- `MX_BIS Kitchin` (1 variable carrying)

**35 cellules composite-survies ont été vetoed** — toutes manquaient
de support variable individuelle. Inclut TOUTES les Kitchin du
panel WB (8 agrégats), les artefacts précédemment diagnostiqués
(WLD-K3, UMC-Juglar, LIC-K), et les composites Q sans porteur.

**Bilan empirique** : aucune cellule survivante n'est désormais un
artefact d'agrégation au sens des audits CN_BIS/WLD-WB/UK_BOE. Les
4 survivants restants ont au moins une variable porteuse — la
publication CPV est désormais doublement falsifiable (composite +
≥1 variable).

Nouvelle page `docs/methodology_safeguard_roadmap_14.md` sous
section 3 de la nav.

### Verdict final K — la différenciation a redistribué l'artefact, pas révélé un K européen

Diagnostic per-variable post-différenciation sur les 4 nouvelles
cellules K composite-survivantes (G7-long, NORDIC-long, EU4-long,
UK_BOE) confirme :

| Composite K post-diff | p | Variables individuelles survivantes |
|---|---:|---:|
| G7-long | 0.001 🟢 | **0/35** |
| NORDIC-long | 0.001 🟢 | **0/35** |
| EU4-long | 0.004 🟢 | **0/35** |
| UK_BOE | 0.001 🟢 | **0/16** |

**Sur ~250 cellules (variable × groupe × K=4) testées par variable
individuelle, 1 seule survit Gate 1** : `LH_DEBTGDP` sur `ADV18` à
p=0.028 (marginal). Tous les autres K post-fix sont des **artefacts
d'agrégation post-différenciation** — la différenciation introduit
une cohérence de phase artificielle sur les longs samples
hétérogènes, créant un nouveau type d'artefact qui remplace
l'ancien (fuite de tendance par effet de bord CF) supprimé.

**Conclusion empirique forte** : aucun Kondratieff endogène n'est
détectable au niveau variable dans le pipeline CPV — sur 6
horizons × ~25 groupes × ~80 variables × 316 ans de données UK,
**zéro K-wave authentique** ne survit Gate 1 dual-null à α=0.05.

C'est la confirmation la plus précise possible de la
[thèse centrale](docs/bibliographie.md#critiques-et-scepticisme-empirique-par-cycle)
: les "K-waves" empiriques rapportées dans la littérature
([Schumpeter 1939](docs/bibliographie.md#schumpeter-1939),
[Perez 2002](docs/bibliographie.md#perez-2002),
[Korotayev-Tsirel 2010](docs/bibliographie.md#korotayev-tsirel-2010))
sont des artefacts de méthode (composites de variables trend-dominées,
ou cohérences cross-variable post-transformation), pas des cycles
empiriques distinguables du bruit.

Nouvelle page `docs/case_study_g7_long_uk_boe_kondratieff.md`
sous section 1 de la nav. Documente le diagnostic per-variable,
le mécanisme de l'artefact redistribué, et formule la thèse
centrale en sa forme la plus complète. Roadmap item #14 à
créer : "Garde-fou systématique pour composite-survies — exiger
≥1 variable individuelle survivante avant publication".

### Différenciation pour Kondratieff (anti-trend-leakage) — résultat plus nuancé qu'attendu

Suite aux audits CN_BIS K et WLD-WB K qui ont exposé un artefact
systématique d'agrégation par fuite de tendance via les effets de
bord du filtre Christiano-Fitzgerald, le pipeline applique
désormais une **première-différence avant compositing pour la
bande Kondratieff uniquement**. `_composite_panel` accepte un
nouveau paramètre `differencing=True` qui transforme `panel.diff()`
puis applique band-pass + z-score + moyenne. Pour les samples trop
courts (`hi_years × 2 > n_samples`), le fallback z-scoré
cross-band hérite aussi de la différenciation.

**Le pipeline a été re-tourné sur les 5 horizons** (`wb`, `q`,
`long`, `boe`, `bis`) avec dual null + 1000 surrogates par cellule.

#### Artefacts éliminés (résultat attendu)

| Cellule | p avant (niveaux) | p après (différencié) |
|---|---|---|
| WLD-WB K | 0.001 🟢 contraction | **0.488 🔴 rejected** |
| HIC-WB K | 0.001 🟢 disputed | **0.473 🔴 rejected** |
| OECD-WB K | 0.001 🟢 disputed | **0.560 🔴 rejected** |
| G7-WB K | 0.055 🟠 marginal | 0.161 🔴 rejected |

Sur le panel WB (1960-2024, 65 ans), **toutes** les anciennes K-
survivances étaient des artefacts de fuite de tendance des variables
trend-dominées `CY_FIN` (financiarisation) et `CY_PRD` (productivité).
La thèse centrale est confirmée sur ce périmètre.

#### Survies inattendues — possiblement réelles

Plus surprenant, la différenciation **fait émerger** plusieurs K
sur les horizons longs européens, jusqu'ici cachées sous le bruit
de trend :

| Cellule | p avant (niveaux) | p après (différencié) |
|---|---|---|
| **G7-long K** | 0.001 🟢 | **0.001 🟢** (persistant) |
| **NORDIC-long K** | 0.608 🔴 | **0.001 🟢** (émerge) |
| **EU4-long K** | 0.142 🔴 | **0.004 🟢** (renforcé) |
| **UK_BOE K** | 0.892 🔴 | **0.001 🟢** (émerge sur 316 ans) |

Pattern frappant : K émerge sur les **panels européens longs** (G7,
NORDIC, EU4 sur 152 ans ; UK sur 316 ans) mais **pas sur USA-long
ni ANGLO-long**. Cohérent avec Schumpeter (1939) qui regardait des
taux de croissance, pas des niveaux. Pourrait être un phénomène
empirique authentique — un K-wave européen mesurable sur les
taux de croissance économique de long terme — ou un nouvel artefact.

#### Diagnostic en cours

Run `evidence-per-variable --horizons boe,long` lancé en
parallèle pour distinguer redistribution d'artefact vs. découverte
authentique. Si les K nouvellement-survivants sont portés par
**plusieurs variables individuelles** indépendamment, le signal
est probablement réel. Si seul le composite survit, c'est un
artefact d'agrégation post-différenciation.

Nouvelle page `docs/methodology_differencing_for_kondratieff.md`
sous la section 3 (Protocole) de la nav. Documente le mécanisme,
les résultats post-fix, la nuance entre artefacts éliminés et
signaux émergents, et les garde-fous pour distinguer les deux.

### Audit WLD-WB Kondratieff — second artefact d'agrégation démasqué

Application du même protocole 5-étapes que pour
[CN_BIS K](docs/case_study_cn_bis_kondratieff.md) à
`WLD-WB Kondratieff p=0.001` (le seul autre survivant K du pipeline).

**Résultat identique** : artefact d'agrégation, pas un vrai cycle.

Le composite K WLD ne consomme que 2 variables (`CY_FIN`,
`CY_PRD` — celles pré-enregistrées avec `cycle_targets=['kondratieff']`
dans le manifest WB). Ces deux variables sont **toutes deux des
tendances structurelles pures** :

| Variable | R² log-lin | ACF lag-1 | p Gate 1 individuel |
|---|---:|---:|---:|
| CY_FIN (financiarisation) | 0.64 | 0.97 | 0.728 (rejected) |
| CY_PRD (productivité) | **0.99** | **1.000** | 0.993 (rejected) |

Individuellement, AUCUN signal K. Mais leur composite z-score à
`p=0.001` parce que la moyenne de 2 trends z-scorées est encore
une trend (avec un peu de bruit), et le filtre band-pass CF [40-60y]
capture la moitié de la rampe sur 65 ans comme un demi-cycle K.

**Le seul Kondratieff publié du pipeline CPV est donc également un
artefact**. La thèse centrale (rejets = empirisme honnête) est
confirmée de façon écrasante : aucune K-wave authentique ne survit
quand on regarde par variable individuelle.

Page `docs/case_study_wld_wb_kondratieff.md` ajoutée à la section 1
de la nav. Documente le même protocole 5-étapes (coverage / forme /
votes / per-variable / mécanisme) et soulève la question
méthodologique de fond : doit-on **transformer les séries pour
qu'elles ressemblent à des cycles** (pre-detrending, différenciation)
avant de tester, ou tester telles quelles et accepter que les
tendances structurelles fassent rejeter les K-waves par défaut ?

### Étude de cas CN_BIS Kondratieff — démasque un artefact d'agrégation

Dive deep sur le seul Kondratieff survivant hors `WLD-WB` :
`CN_BIS K p=0.025 (peak)`. L'évidence par variable montre que
**aucune des 4 séries BIS chinoises individuelles** ne porte de
signal Kondratieff (BIS_CRATIO et BIS_TCRED à `p=1.000`, BIS_RPP
à `p=0.108`, BIS_CGAP à `p=0.335`). La survie composite était
**créée par l'agrégation**.

Diagnostic en deux temps :
1. **Bug de filtre BIS** — `BIS_TCRED` et `BIS_CRATIO` chargeaient
   la même série ("Credit to Private non-financial sector from
   All sectors at Market value - % of GDP"). Le composite z-scoré
   pondérait cette série 50 % du temps, doublant son influence.
2. **Transition structurelle 1985-2025 chinoise** — crédit-PIB
   chinois passe de 62 % à 200 % avec CAGR 3.2 %/an, R² log-linéaire
   = 0.956, ACF=0.998. Sur 40 ans, le filtre band-pass [40-60y]
   capture la rampe comme un demi-cycle K.

Fix : `load_total_credit` remplace le filtre `TC_BORROWERS='P'`
(privé tous) par une décomposition Mian-Sufi sectorielle —
`BIS_HHCRED` (households), `BIS_BUSCRED` (corporates),
`BIS_GVCRED` (general government). Manifest mis à jour.

Vérification post-fix :

| Cycle | p avant (dupliqué) | p après (décomposé) | Verdict |
|---|---|---|---|
| Kitchin | 0.044 🟡 | 0.091 🟠 | survie → marginal |
| Kondratieff | **0.025 🟡** | **0.051 🟠** | **survie → rejected** |

**Le seul K hors WLD-WB disparaît avec la duplication corrigée**.
Cohérent avec [Maddison (1991)](docs/bibliographie.md#maddison-1991) :
les transitions structurelles visibles ne sont pas des K-waves
endogènes. La résiduelle `p=0.051` (juste sous le seuil) reste
explicable par la signature de bord du structural break.

Nouvelle page `docs/case_study_cn_bis_kondratieff.md` ajoutée à
la section 1 de la nav. Documente le diagnostic en 5 étapes
(coverage / forme / votes inter-méthode / per-variable / mécanisme
d'artefact) et tire les implications pour le protocole CPV
(évidence par variable = garde-fou critique ; sample minimum
N≥2 cycles pour Kondratieff = 120 ans ; hygiène de
non-duplication dans le compositing).

### Roadmap #13 Phase 2 : BIS macroprudential — 9 EM + 8 AE quarterly

Nouveau module `ecowave/cycles/bis_bulk.py`, nouveau manifest
`bis_manifest.json`, nouvel horizon `bis` dans `position-cycles`.
Apporte sur le panel CPV les **9 marchés émergents** (Brésil, Chine,
Inde, Mexique, Corée, Turquie, Afrique du Sud, Russie, Indonésie) +
8 économies avancées, **entièrement absents des horizons précédents**
(WB groupes par tier de revenu, Path 5 = AE seulement, JST = 18 AE).
Quarterly, 1970-2025, ~225 trimestres par groupe.

**4 variables BIS ingérées** :
- `BIS_CGAP` — credit-to-GDP gap (Borio-Drehmann CCyB signal, Basel III)
- `BIS_CRATIO` — credit-to-GDP actual ratio
- `BIS_RPP` — residential property prices
- `BIS_TCRED` — total credit % of GDP

**Résultats scientifiques fort** :

| Cellule | p-value | Statut | Insight |
|---|---|---|---|
| BIS_EM Kitchin | 0.001 🟢 | survives | composite EM converge sur K3 |
| BIS_EM Kuznets | 0.001 🟢 | survives | swing financier EM 1.5-7 ans |
| BIS_EM Kondratieff | 0.965 🔴 | rejected | pas de K-wave EM |
| **CN_BIS Kondratieff** | **0.025 🟡** | **survives — peak** | **credit cycle chinois K-wave détectable, min dans 13 ans** |
| BIS_AE all 4 cycles | > 0.18 🔴 | all rejected | composite AE post-1970 plat (Great Moderation confirme Romer 1999, Stock-Watson 2003) |
| ID_BIS Juglar | 0.021 🟡 | expansion | seul Juglar individuel net dans EM |
| 6 EM Kitchin survive | p ≤ 0.044 | Kitchin EM-spécifique | cycle inventory EM-driven |

Intégration site :
- 11 lignes BIS ajoutées au dashboard home (BIS_EM, BIS_AE, BR/CN/IN/MX/KR/TR/ZA/RU/ID).
- Note signée `cycle_position_2026_05_bis.md` sous section 1 de la nav.
- `position-cycles --horizon bis` dans la CLI.
- `home-synthesis` lit le sidecar `bis`.

Téléchargement bootstrap des données :
```bash
mkdir -p data_raw/bis && cd data_raw/bis && \
  curl -sL -o credit_gap.zip "https://data.bis.org/static/bulk/WS_CREDIT_GAP_csv_col.zip" && \
  curl -sLO "https://data.bis.org/static/bulk/WS_SPP_csv_col.zip" && \
  curl -sLO "https://data.bis.org/static/bulk/WS_TC_csv_col.zip"
```

### Roadmap #13 Phases 0 + 1 : JST R6 élargi + Bank of England Millennium

**Phase 0 — JST R6 élargi** (gain immédiat, zéro coût d'ingestion) :
le manifest `long_history_manifest.json` passe de **7 à 35 variables**
en exposant les colonnes JST R6 jusqu'ici non utilisées (RORE returns,
mortgages, dette publique, current account, total credit, debt service,
investment-to-GDP, unemployment, wages, etc.). Même fichier Stata, mêmes
18 pays, même 1870-2020. Conformément à la thèse centrale (cf.
[[cpv-central-thesis]]), cela enrichit massivement le périmètre du test
Gate 1 par variable (`evidence-per-variable`) — on peut désormais tester
le crédit business séparément du crédit ménages séparément des
mortgages, l'investissement séparément de la consommation, etc.

**Phase 1 — Bank of England Millennium dataset** : nouveau module
`ecowave/cycles/boe_millennium.py`, nouveau manifest
`boe_millennium_manifest.json`, nouvel horizon `boe` dans
`position-cycles`. Source : BoE WP 845 v3.1 (Thomas & Dimsdale 2017,
data jusqu'à 2016), miroir CSV propre sur `datahub.io` (le xlsx BoE
direct retourne 403 Cloudflare). License OGL-UK-3.0 (open).

- **316 ans** de données annuelles UK (1700-2016), **16 variables**
  couvrant GDP, CPI, WPI, Bank Rate (1694+), Consols yield (1703+),
  broad money, credit, HPI, equity, investment, unemployment,
  productivity, debt-to-GDP, population, real consumption.
- **Résultat scientifique fort** : sur 316 ans = ~5-8 K-waves
  théoriques, **UK_BOE Kondratieff reste rejeté à p=0.892** sur le
  composite — confirmation empirique massive de
  [Maddison (1991)](docs/bibliographie.md#maddison-1991) et
  [Solomou (1987)](docs/bibliographie.md#solomou-1987). Le seul cycle
  survivant est Kuznets : `p=0.024 (🟡)`, phase contraction,
  trajectoire vers un pic dans ~7.8 ans.

Intégration site :
- `UK_BOE` ajouté au dashboard home (21e ligne) et à la matrice
  p-values.
- Note signée `cycle_position_2026_05_boe.md` publiée sous section 1
  de la nav.
- `position-cycles --horizon boe` dans la CLI.
- `home-synthesis` lit désormais aussi le sidecar `boe`.

Téléchargement : `mkdir -p data_raw/boe && curl -sL
"https://datahub.io/economic-history/millennium-macroeconomic-data-uk/_r/-/data/annual.csv"
-o data_raw/boe/annual.csv`.

### Évidence par variable + bibliographie critique : thèse centrale du papier

**Résultat empirique central** : sur **548 cellules** (variable × agrégat
× cycle, 3 horizons) testées via Gate 1 dual-null à α=0.05 avec 1000
surrogates, seules **8 cellules survivent (1.5%)**. Sur les agrégats
composites, le même test laisse passer ~25-30% des cellules.

L'écart de ~20 points s'explique mécaniquement : sommer plusieurs séries
z-scorées crée des artefacts de variance autocorrélée qui battent un
null AR(1), même quand aucune des séries n'a individuellement de
signal cyclique. **C'est exactement le diagnostic posé par Wen (2005)
sur Kitchin et Solomou (1987) sur Kuznets/Kondratieff il y a 20-40
ans.** Le résultat positionne CPV comme **stress test** du cycle
composite, pas comme méthode d'attribution.

- Nouveau module `ecowave/cycles/evidence.py` (panel reconstruction depuis
  SQLite, calcul Gate 1 par variable, rendu page).
- Nouvelle commande `ecowave evidence-per-variable --as-of YYYY-MM
  --horizons wb,q,long --null dual --n-surrogates 1000` avec fallback
  read-from-sidecar pour réexécutions partielles.
- Nouvelle page `docs/evidence_per_variable.md` ajoutée à la section
  "1. Où en sommes-nous ?" de la nav. Structure : headline 1.5% +
  tables de survie par variable par cycle par horizon + spotlight par
  agrégat phare. Chaque cycle linké à sa référence critique canonique.
- **Bibliographie enrichie** (`docs/bibliographie.md`) : 11 nouvelles
  références (Burns-Mitchell 1946, Garvy 1943, Hodrick-Prescott 1997,
  Klotz-Neal 1973, Mansfield 1983, Maddison 1991, Quah 1992, Romer 1999,
  Solomou 1987, Stock-Watson 2003, Wen 2005) + section "Critiques et
  scepticisme empirique par cycle" qui articule la thèse centrale avec
  les résultats CPV cellule par cellule.
- **Roadmap** : item #12 "Évidence par variable" (IMPLÉMENTÉ) ;
  item #13 "Allongement des séries temporelles" (TODO) documentant 4
  voies — BoE Millennium 1086-2024, Mitchell IHS 1750-2010, JST/BIS
  extensions, Toutain France 1789-1990.
- Tests : 5 nouveaux dans `tests/test_evidence_per_variable.py`
  (reconstruction panel annual + quarterly, sidecar NaN-safe roundtrip,
  helper survival count, rendu page avec liens biblio).

### GitHub Pages : matrice "poids de preuve" (p-values Gate 1) sous le dashboard

Complète le dashboard binaire (cycle survit/rejected à α=0.05) par
une matrice colorée 20 × 4 (un agrégat par ligne, un cycle par
colonne) qui publie la **p-value brute** du test dual-null. Le
lecteur peut appliquer son propre seuil sans recalcul :

- 🟢 `p ≤ 0.01` — signal fort, survit à α=0.01
- 🟡 `0.01 < p ≤ 0.05` — seuil CPV standard
- 🟠 `0.05 < p ≤ 0.10` — marginal, survit à la convention macro α=0.10
- 🔴 `p > 0.10` — clairement null

Met en lumière les cas borderline qui auraient été perdus dans le
binaire : `WLD Kuznets p=0.054`, `G7 Kondratieff p=0.055`,
`LMC Kondratieff p=0.063` — autant de pistes d'analyse pour la
suite. Pied de page rappelle que les p-values ne sont **pas
corrigées** pour comparaisons multiples (Bonferroni-stricte sur 36
cellules WB → α ≈ 0.0014).

- Nouvelles fonctions `render_home_pvalues_table()` et
  `_format_pvalue_cell()` + constante `PVALUE_THRESHOLDS` dans
  `ecowave/cycles/report.py`.
- La commande `ecowave home-synthesis` écrit désormais un troisième
  artefact : `docs/_includes/home_pvalues_table.md`, inclus dans
  `docs/index.md` sous le dashboard (snippet séparé pour
  modularité).
- Tests : 3 cas supplémentaires
  (`test_pvalue_thresholds_are_ordered_ascending`,
  `test_format_pvalue_cell_maps_each_threshold_band`,
  `test_home_pvalues_table_renders_20_rows_with_4_cycle_columns`).

### GitHub Pages : dashboard agrégats en home (20 × 14)

Le snippet inclus dans `docs/index.md` n'est plus le tableau 4 lignes
"un cycle = un agrégat canonique" mais un **dashboard 20 lignes ×
14 colonnes** (Agrégat, Source + 4 cycles × {Phase, Tendance, Next}).
Vingt agrégats : 8 WB (WLD > G7 > OECD > BRICS > HIC > UMC > LMC >
LIC), 6 Path 5 trimestriel (G7Q, OECDQ, USA, EA, JPN, GBR), 6 histoire
longue (ADV18, G7, EU4, ANGLO, NORDIC, USA), dans cet ordre canonique
figé. Cellules `—` lorsque la Porte 1 dual-null a rejeté le cycle
sur l'agrégat — fidèle au principe "publier les échecs" mais sans
saturer visuellement (em-dash plutôt que texte `rejected`).

- Nouvelle fonction `render_home_aggregates_table()` +
  constantes `AGGREGATE_ROW_ORDER` et `HORIZON_LABEL_SHORT` dans
  `ecowave/cycles/report.py`.
- La commande `ecowave home-synthesis` écrit désormais le dashboard
  dans `docs/_includes/home_synthesis_table.md` (la note signée
  multi-horizons conserve, elle, le tableau 4 lignes en headline).
- `docs/index.md` met à jour le paragraphe d'introduction.
- Tests : 3 cas supplémentaires (`test_aggregate_row_order_covers_3_horizons`,
  `test_home_aggregates_table_renders_surviving_cells_and_emdashes`,
  `test_home_aggregates_table_link_prefix_override`).

### GitHub Pages : refonte du site et tableau de synthèse en home

Refonte complète du site MkDocs (`https://s-geffroy.github.io/EcoWave/`)
pour passer d'une nav "par jeu de données" à une nav "par question
scientifique" (1. Où en sommes-nous ? / 2. Pourquoi ? / 3. Comment ? /
4. Preuves détaillées / 5. Données & références).

- **Tableau de synthèse home** — `docs/index.md` affiche désormais en
  headline un tableau 4 lignes (une par cycle canonique) avec phase,
  tendance et prochain extremum. Sources canoniques par bande,
  sélectionnées sur le critère "Gate 1 dual-null survives at α=0.05" :
  Kitchin → WB / WLD (p=0.002), Juglar → long / G7 (p=0.005),
  Kuznets → long / G7 (p=0.008), Kondratieff → WB / WLD (p=0.001).
  Le couple (WB-WLD, long-G7) couvre les 4 bandes parce que (a) la
  longue histoire fournit ~17 cycles Juglar et ~7 Kuznets sur G7
  (impossible avec 65 ans annuels WB), et (b) le WB-WLD a assez de
  cycles Kitchin (~16) et Kondratieff (~1.3) pour battre le bruit
  rouge. Le trimestriel G7Q dilue le Kitchin (agrégation 7 pays
  out-of-phase). Aucune agrégation inter-dataset artificielle ;
  chaque cellule est traçable à une ligne SQLite `cycle_positions`.
- **Nouvelle commande CLI** `ecowave home-synthesis --as-of YYYY-MM`
  qui recompose la synthèse cross-horizon depuis trois sidecars JSON
  (`reports/cycle_position_{as_of}_{wb,q,long}.json`) écrits par
  `position-cycles`. Sortie : `docs/_includes/home_synthesis_table.md`
  (inclus via `pymdownx.snippets`) + `reports/cycle_position_synthesis.md`
  (note signée multi-horizons publiée dans la section 1 de la nav).
- **Notes `cycle_position_*.md` publiées** — `scripts/sync_docs.sh`
  copie maintenant les trois rapports horizon-par-horizon vers
  `docs/reports/`, accessibles depuis la section "Où en sommes-nous ?".
- **Activation de `pymdownx.snippets` + `pymdownx.details`** dans
  `mkdocs.yml` (le second pour replier les métadonnées denses des
  figures sans perdre la rigueur).
- **Fonctions ajoutées dans `ecowave/cycles/report.py`** :
  `positions_sidecar_path`, `write_positions_sidecar`,
  `read_positions_sidecar`, `render_home_synthesis_table`,
  `render_cross_horizon_commentary`,
  `render_cross_horizon_synthesis_md`, et le mapping
  `CANONICAL_HOME_ROWS` qui verrouille la sélection cycle ↔ horizon ↔
  agrégat.

Tests : `test_report_home_synthesis.py` (6 cas) couvre la sélection
des 4 lignes canoniques, le placeholder "en attente" quand un sidecar
manque, le roundtrip JSON, et le rendu de la note multi-horizons signée.

### Extended quarterly coverage + per-band variable filter + long-horizon comparison

Two new quarterly variables on top of GDP / CPI / UNRATE / YIELD /
CREDIT:

- **Q_INV** (`NAEXKP04<ISO>Q652S` on FRED for USA/EA/GBR;
  `namq_10_gdp na_item=P51G` on Eurostat for DEU/FRA/ITA) — real
  gross fixed capital formation, volume index, SA. Schumpeter's
  canonical Juglar driver. Annualised quarterly log-growth.
- **Q_HPI** (BIS `Q<ISO>R628BIS` on FRED for the 8 country
  providers) — real residential property prices. Lewis-Kuznets
  construction swing. Annualised quarterly log-growth.

JPN/CAN Q_INV not yet wired (NAEXKP04 mirror absent on FRED for
these ISOs; OECD SDMX direct path remains experimental — would need
a dedicated dim mapping).

#### Per-band variable filter

The runner now restricts each band composite to manifest variables
that pre-register the band in their `cycle_targets` — feeding the
K-band composite with strictly-Juglar columns would z-score their
near-zero K-band content to unit variance and dilute the K-wave SNR
of genuine K-targeting columns. `_analyse_and_render` takes a new
`targets_by_var` kwarg; all three `_run_*` dispatchers (wb, long,
quarterly) build it from their manifest and pass it through.
Backwards-compatible: when omitted, every band sees the full panel
(legacy behaviour, used by the smoke tests).

Tests: `test_targets_by_var_filter.py` (3 cases) pin the filter +
the no-targets fallback + the legacy no-filter path.

#### Long-horizon comparison

Side-by-side 2026-05 matrices show Kondratieff Gate 1 separable on
EVERY long-horizon group (p=0.001 across ADV18, ANGLO, EU4, G7,
NORDIC, USA) where the quarterly horizon rejects on 5 of 6 groups
(p ∈ [0.11, 0.67]). On 150y panels the AR(1) bootstrap sees
2.5-3.75 K-cycles vs 1.1-1.65 on the quarterly's 66y window —
direct confirmation that the quarterly K-wave rejection is a
statistical-power constraint, not absence of cycle.

Long-horizon phases published 2026-05: USA Kondratieff `expansion`,
ANGLO Kondratieff `expansion`, G7 Kondratieff `contraction`, ADV18
Kondratieff `contraction`, NORDIC Kondratieff `expansion`. ADV18
reaches separable Gate 1 on all four bands simultaneously
(Kitchin/Juglar/Kuznets/Kondratieff = `contraction`, `contraction`,
`disputed`, `contraction`).

### Per-band method weighting (Roadmap #11)

The Path 5 v1 run surfaced that two of the four Gate-2 methods —
**D (PELT)** and **G (Bry-Boschan)** — vote nearly constant phases on
some bands due to a mismatch between the method's design horizon and
the cycle period:

- D on Kitchin (3-5 y) → constant `expansion` (PELT segments span
  multiple Kitchin cycles, endpoint phase = trend, not cycle).
- G on Kitchin → constant `contraction` (B-B endpoint dating is
  borderline at 3-5 y on quarterly grids).
- D on Kondratieff (40-60 y) → uninformative (only 1.1-1.65 cycles
  fit a 66 y panel; PELT collapses to a single segment).

`bands.py` now pre-registers per-band `methods` allowlists and
`min_agreement` thresholds; `consensus.py` accepts an
`allowed_methods` kwarg; `runner.py` reads both from `CYCLE_BANDS`:

- Kitchin: `(F, E)`, min 2 (unanimity of the admitted panel).
- Juglar: `(D, E, F, G)`, min 3 (3/4 — unchanged).
- Kuznets: `(D, E, F, G)`, min 3 (unchanged).
- Kondratieff: `(E, F, G)`, min 2 (majority of admitted panel).

Excluded methods' votes are still persisted in `cycle_consensus` for
transparency — they simply do not influence Gate 2. Tests
(`test_consensus_per_band.py`, 7 cases) pin both the new
allowlist-filtered consensus and the legacy 4-method path.

Gate 2 gains on the 2026-05 quarterly run:
- **GBR Kitchin**: disputed → **`peak`** (F + E concord).
- **G7Q Juglar**: disputed → **`contraction`** (3/4 under full panel).
- **OECDQ Juglar**: disputed → **`contraction`** (3/4).
- **GBR Kondratieff**: disputed → **`expansion`** (E + G majority,
  D excluded).
- USA Kitchin = `contraction` and EA Kuznets = `expansion` remain
  stable.

### Path 5 v2 — Q_YIELD + Q_CREDIT for the long bands

Extends the quarterly manifest with two BIS/OECD-MEI variables hosted
on FRED to unblock the long-band cells that Path 5 v1 (GDP + CPI +
UNRATE) couldn't separate:

- **Q_YIELD** — 10-year government bond yield, OECD MEI mirror on
  FRED (`IRLTLT01<ISO>Q156N` for US, EA, JPN, GBR, CAN, DEU, FRA,
  ITA). Level transform, Kondratieff target. Parallels `LH_YIELD` in
  the long-history manifest.
- **Q_CREDIT** — total credit to private non-financial sector, BIS
  data hosted on FRED (`Q<ISO>PAM770A`). Annualised quarterly
  log-growth. Targets Juglar + Kuznets + Kondratieff. Carries the
  Borio-Drehmann financial cycle and the Reinhart-Rogoff credit
  super-cycle.

Gate 1 improvements on the 2026-05 run:
- **EA Kuznets**: p = 0.922 → 0.001 (rejected → separable + Gate 2
  consensus `expansion`).
- **JPN Kondratieff**: p = 0.706 → 0.144 (≈5× reduction).
- **EA Kondratieff**: p = 0.976 → 0.237.
- **USA Kondratieff**: p = 0.121 → 0.081 (approaches the 0.05
  threshold).
- All Kitchin/Juglar/Kuznets Gate 1 values stay at p = 0.001 (no
  regression).

Gate 2 (consensus) stays mostly `disputed` for Kitchin/Kuznets — the
methodological bias of D (PELT) and G (Bry-Boschan) on short cycles
documented in the Path 5 v1 commit is unaffected by adding variables.

### Path 5 — Quarterly Kitchin extension (Roadmap #9 — IMPLÉMENTÉ)

Adds a third data horizon `position-cycles --horizon quarterly` that
lifts Kitchin (3-5 y) above the practical Nyquist threshold, the
limitation that was forcing every Kitchin cell in the 2026-05 World
Bank run to publish as `rejected`. The annual `--horizon wb` path keeps
its narrow 4-5 y diagnostic attempt unchanged (non-regression).

- **New module** `ecowave/cycles/quarterly.py` — fetchers for FRED
  (JSON observations), Eurostat (JSON-stat 2.0 via
  `statistics/1.0/data`), and OECD (SDMX 2.1 REST at `sdmx.oecd.org`
  with DSD introspection that probes three structure-endpoint
  variants). GDP-weighted multi-country aggregation;
  `PeriodIndex(freq="Q")`-aware panel construction. Tagged silent
  fetch failures bubble up as a stderr summary per group.
- **OECD path is experimental** — `sdmx.oecd.org`'s compound DSD refs
  (`DSD_X@DF_Y`) return empty payloads under the standard
  `/datastructure/{agency}/{id}/{version}` and `/dataflow/.../?references=descendants`
  endpoints, blocking automatic dimension-order discovery. The v1
  manifest uses FRED-hosted OECD/IFS mirror series for JPN/GBR/CAN
  (`JPNRGDPEXP`, `NGDPRSAXDCGBQ`, `NGDPRSAXDCCAQ`,
  `JPNCPIALLMINMEI`, `GBRCPIALLMINMEI`,
  `LRUNTTTTJPM156S`, `LRUN64TTGBQ156S`) — same underlying source data,
  one API surface to maintain. The native OECD fetcher remains
  callable for users with known dim mappings.
- **CF bandpass NaN robustness** — `ecowave/cycles/decompose.cf_bandpass`
  now drops NaN before calling `cffilter`, then reindexes to the
  original index. `statsmodels.cffilter` propagates any single NaN
  to all outputs; the previous behaviour broke Gate 2 on multi-country
  composites that picked up a 1-quarter alignment hole. Surfaced by
  Path 5 testing on G7Q.
- **New manifest** `quarterly_manifest.json` — three variables
  (`Q_GDP`, `Q_CPI`, `Q_UNRATE`), six groups (USA, EA, JPN, GBR, G7Q,
  OECDQ). EA aggregate starts 1995 (Eurostat `EA20` native).
- **Runner threading** — `samples_per_year` plumbed through
  `_composite_panel`, `_run_gate1`, `_analyse_and_render`. Kitchin
  band gate is now conditional: `samples_per_year <= 1.0` → narrow
  (4, 5); `samples_per_year > 1.0` → full (3, 5). New
  `report_suffix` kwarg replaces the substring-based horizon sniff so
  the quarterly report lands at
  `reports/cycle_position_<as_of>_q.md`.
- **DB schema 0.5.0 → 0.5.1** — new table
  `cycle_observations_quarterly(group_code, variable_code, year,
  quarter, value, source_id)` with `UNIQUE(group, var, year, quarter)`
  and `CHECK(quarter BETWEEN 1 AND 4)`. The annual
  `cycle_observations` table is unchanged. `migrate_db` is now
  idempotent and handles in-place 0.5.0 → 0.5.1 upgrades. New helper
  `upsert_cycle_observation_quarterly`.
- **CLI** — `--horizon` accepts `wb | long | quarterly`; per-horizon
  defaults for `--manifest` and `--groups`.
- **Tests** — `tests/test_quarterly_panel.py`,
  `tests/test_samples_per_year_thread.py`,
  `tests/test_kitchin_gate_conditional.py`,
  `tests/test_runner_quarterly_smoke.py`.
- **Docs** — `methodology/feuille_de_route.md` Item #9 flipped to
  IMPLÉMENTÉ; `docs/cycles/kitchin.md` adds a "Chemin trimestriel
  natif" subsection.

### Schema version: 0.5.1 (was 0.5.0)



The project's active framework. Decomposes macroeconomic time-series into the
four canonical economic cycles (Kitchin / Juglar / Kuznets / Kondratieff) and
publishes per-group phase labels under three falsifiability gates
(existence / consensus / universality).

### Site rewrite — French academic edition (2026-05)

The published documentation site is rewritten in French with an academic
template (Résumé / Notation / Méthode / Résultats / Caveats / Références)
and a figures-forward layout. The code, commit messages, and this
CHANGELOG remain in English by design.

- **mkdocs.yml**: `language: fr`, indigo palette, MathJax via
  `pymdownx.arithmatex`, footnotes, navigation tabs + indexes. Nav restructured
  to Accueil / Protocole CPV / Cycles canoniques / Groupes / Résultats /
  Analyses approfondies / Validation EWS / Sources / Bibliographie.
- **New consolidated bibliography** (`docs/bibliographie.md`) with stable
  author-year anchors. All site pages cite into this single file.
- **Four new figure functions** in `ecowave/cycles/report.py`:
  `plot_amplitude_heatmap`, `plot_pvalue_heatmap`, `plot_phase_polar_diagram`,
  `plot_next_extremum_timeline`. Wired into `runner.py:_analyse_and_render`
  so they ship with every `position-cycles` run on both horizons.
- **Methodology renamed + translated**: 8 pages (`protocole_cpv`,
  `trois_portes`, `methodes_decomposition`, `indicateur_composite`,
  `normalisation`, `garde_fous`, `fenetres_reference`, `feuille_de_route`).
- **Result reports rewritten** in academic French with figures-forward
  layout: `panel_banque_mondiale_2026.md`, `histoire_longue_2026.md`,
  `validation_ews.md`.
- **Deep-dive analyses academised**: Résumé / Notation / Références
  sections added to `juglar_us_anglo_nordic_2026.md` and
  `kondratieff_adv18_eu4_2026.md`.
- **Cycles pages** (Kitchin / Juglar / Kuznets / Kondratieff) translated
  and each lead with the polar phase diagram for its band.
- **Sync + CI**: `scripts/sync_docs.sh` updated for the new figure
  patterns and French slugs; `.github/workflows/pages.yml` description
  updated.

`mkdocs build --strict` passes cleanly. Site name stays *CPV — Cycle
Position Vector* with the French subtitle « Décomposition multi-cycles
falsifiable des indicateurs macroéconomiques ».

### Schema version: 0.5.0 (initial CPV schema)

DB schema is rebuilt from scratch. Tables:

- `sources`, `variables`, `ingestion_runs`, `raw_files`, `events`,
  `event_sources`, `analyst_notes`, `monthly_observation_index`,
  `curve_scores` — pilot-window panel.
- `global_indices` — composite intensity + diffusion across three weightings.
- `model_scores`, `model_verdicts` — CPV stack outputs (one row per
  D/E/F/G/H method).
- `cycle_observations`, `cycle_positions`, `cycle_consensus`,
  `cycle_universality` — CPV long-horizon outputs.
- `external_anchors`, `validation_errors`, `schema_meta`.

### CPV stack (Models D / E / F / G)

- **Model D** — PELT change-point detection (`waves/model_d_regime.py`).
- **Model E** — Markov-switching AR(1) (`waves/model_e_markov.py`).
- **Model F** — Christiano-Fitzgerald Juglar band-pass + Hilbert phase
  (`waves/model_f_cycles.py`).
- **Model G** — Bry-Boschan / Harding-Pagan turning-point dating
  (`waves/model_g_bryboschan.py`).

### CPV module (`ecowave/cycles/`)

- `bands.py` — frozen 4 cycle bands + 9 group codes (WLD, OECD, HIC, UMC,
  LMC, LIC, G7, G20, BRICS).
- `manifest.py` — `CycleSpec` + `CycleManifest` loader.
- `ingest.py` — multi-country WB ingestion with GDP-weighted aggregation.
- `decompose.py` — CF band-pass + continuous Morlet wavelet + COI.
- `phase.py` — Hilbert instantaneous phase + 4-quadrant classification.
- `surrogate.py` — AR(1) bootstrap null (Gate 1).
- `consensus.py` — method consensus (Gate 2).
- `universality.py` — cross-group concordance (Gate 3).
- `report.py` — signed-note rendering + figures.
- `runner.py` — end-to-end pipeline.

### CLI

- `ecowave init-db` — initialize the SQLite database.
- `ecowave check-config` — validate sources and storage.
- `ecowave position-cycles` — multi-cycle world positioning.
- `ecowave run-pilot <code>` — CPV stack on a crisis window.
- `ecowave evaluate-ews` — out-of-sample AUROC validation.
- `ecowave sources` — render the data-sources page.
- `ecowave generate-report` — render the pilot report.

### Manifests

- `sources_manifest.json` — pilot-window FRED/ECB/WorldBank panel.
- `cycles_manifest.json` — long-horizon 8-indicator World Bank panel.

### Methodology

- `methodology/multi_cycle_decomposition.md` — CPV protocol spec.
- `methodology/cycle_validation_rules.md` — three falsifiability gates.
- `methodology/cycle_methods_survey.md` — decision matrix.
- `methodology/composite_indicator.md` — intensity + diffusion.
- `methodology/anti_pseudoscience_rules.md` — CPV guardrails.
- `methodology/improvement_roadmap.md` — design history.
- `methodology/normalization_rules.md`.
- `methodology/reference_windows.md`.

### Reports & analyses (2026-05)

- `reports/cycle_position_2026_05_wb.md` — World Bank panel run
  (9 groups, 1000 surrogates, dual null).
- `reports/cycle_position_2026_05_long.md` — long-history run
  (Maddison Project 2023 + Jordà-Schularick-Taylor R6, 1870-2022,
  ADV18 / G7 / USA / EU4 / ANGLO / NORDIC).
- `reports/juglar_us_anglo_nordic_2026.md` — signed deep-dive on the
  Juglar divergence between USA/ANGLO (expansion, peak ~2024) and
  NORDIC (contraction, trough late-2023, peak ~mid-2026).
- `reports/kondratieff_adv18_eu4_2026.md` — signed deep-dive on the
  K5 peak in 2018-2022, K3/K4 historical retrieval at ±5 years,
  amplitude (~0.85) at half of K3/K4 (~1.55/1.28).

### Dependencies

`typer`, `click`, `pydantic`, `pandas`, `numpy`, `scipy`, `ruptures`,
`statsmodels`, `requests`, `matplotlib`, `jinja2`, `pyarrow`, `pywavelets`,
`tabulate`, `pytest`, `ruff`, `mkdocs-material`.
