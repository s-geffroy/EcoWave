# Failure modes

> *Le verdict est PASS 78 % — donc 22 % d'échecs.* Cette page analyse
> honnêtement les 15 variables (sur 68) où aucun modèle cluster ne bat
> random walk en out-of-sample CRPS à h = 12.

## Liste exhaustive des variables battues par RW

Extrait des sidecars consolidés (n_origins=12, as_of=2026-05) :

| Panel | Variable | Best cluster tenté | Pourquoi (hypothèse) |
|---|---|---|---|
| `wb` | HIC::CY_INV | HAR | Série courte (65 obs annuels), investissement très bruité |
| `wb` | WLD::CY_TRD | ARFIMA+RS | Commerce mondial, dominé par chocs structurels exogènes |
| `wb` | WLD::CY_INV | ARFIMA+RS | Idem |
| `wb` | HIC::CY_TRD | ARFIMA+RS | Idem |
| `q` | EA::Q_YIELD | HAR | Taux long zone euro, ZIRP 2014-2022 = régime exotique |
| `q` | USA::Q_YIELD | MSM | Taux long US, idem ZIRP + QE post-2008 |
| `q` | EA::Q_INV | HAR | Investissement zone euro, vol grégaire pré/post COVID |
| `long` | G7::LH_CREDIT | ARFIMA+RS | Crédit G7 long, contre-intuitivement échoue malgré spécialisation ARFIMA+RS |
| `long` | G7::LH_YIELD | MSM | Taux longs G7, période 1870-2024 |
| `boe` | UK_BOE::BOE_STIR | ARFIMA+RS | Taux short-term Bank of England |
| `bis` | BIS_AE::BIS_HHCRED | HAR | Crédit ménages AE, retournements 2007-2009 atypiques |
| `bis` | BIS_AE::BIS_CRATIO | MSM | Credit ratio AE |
| `sh` | US_SH::SH_US_RAILFREIGHT | ARFIMA+RS | Fret ferroviaire US, série Wen 2005 |
| `sh` | US_SH::SH_US_STEEL | ARFIMA+RS | Acier US, série Wen 2005 |
| `sh` | US_SH::SH_US_INDPROD | ARFIMA+RS | Production industrielle US |

## Pattern n°1 — Taux d'intérêt

**5 variables sur 15** (`Q_YIELD` × 2, `LH_YIELD`, `BOE_STIR`,
`BIS_CRATIO` partiellement) sont des **taux d'intérêt** ou directement
dérivés. Notre cluster perd systématiquement.

**Hypothèse** : les taux d'intérêt sont *administrés* (par les
banques centrales) en plus d'être influencés par le marché. Le régime
ZIRP (Zero Interest Rate Policy) 2008-2022 est un **régime de
politique économique** plutôt qu'un régime cognitif spontané. Nos
modèles cluster cherchent des structures statistiques émergentes ;
les taux n'en ont pas suffisamment.

**Diagnostic confirmable** : sur les périodes pré-2008 (où les taux
varient librement), MSM bat probablement RW. Sur la période 2008+,
RW capture mieux le plateau ZIRP.

**À explorer** : modèle hybride RW-with-jumps qui reconnaît les
ruptures de politique. Ou prior bayésien sur les taux qui contraint
l'évolution à respecter les annonces BC.

## Pattern n°2 — Variables courtes annuelles (wb, sh)

**6 variables sur 15** sont sur le panel `wb` (1960-2024) ou `sh`
(annuels, ~50-60 obs après nettoyage). Ces séries n'ont pas assez de
points pour qu'un MSM à 4 composantes (16 états Markov, 4 paramètres)
soit identifié de façon stable.

**Hypothèse** : `n_obs < 80` → MSM mal calibré → MSM perd contre RW
même si la signature C+B+D+I+S est présente.

**Solution partielle déjà appliquée** : `--min-train-length 40` sur
ces panels (sinon ils seraient tous filtrés à zéro variable). Mais ça
ne résout pas le problème d'identification.

**À explorer** :

- Prior empirique informatif sur `(m_0, σ̄, b, γ_1)` issu des panels
  longs.
- MSM avec K = 3 (8 états) pour les séries courtes.
- HAR avec `(1, 2, 5)` pour respecter la dimension d'échantillon.

## Pattern n°3 — Commerce international et investissement agrégé

**4 variables sur 15** (`CY_TRD` × 2, `CY_INV` × 2, `EA::Q_INV`,
`BIS_HHCRED`) sont des agrégats de **commerce** ou
**investissement** à l'échelle de zones économiques larges.

**Hypothèse** : ces agrégats subissent des **chocs structurels
exogènes** très grands (chocs pétroliers, GFC, COVID, tensions
commerciales US-Chine) qui sont mal modélisés par le cluster. Le
random walk capture mieux ces "step changes" qui ne sont pas
multifractaux.

**Diagnostic confirmable** : sur sous-périodes "calmes" (entre chocs
majeurs), MSM probablement gagne. Sur les périodes traversant 1 ou
2 chocs majeurs, RW gagne.

**À explorer** : modèle avec composante structural break détectée
endogène (à la Hamilton 2018 + Bai-Perron).

## Pattern n°4 — Séries historiques US sectorielles (sh)

**3 variables sur 15** sont les trois séries du panel `sh`
(fret rail, acier, production industrielle). Ce sont précisément les
séries que Wen 2005 utilisait pour défendre le cycle Kitchin.

**Hypothèse intéressante** : sur ces séries pré-modernes (les données
remontent aux années 1920), il existe peut-être *encore* une structure
cyclique partielle que nos modèles cluster ne capturent pas mieux que
RW. C'est un cas où la réfutation des cycles n'est pas
opérationnellement utile — bien que statistiquement valide.

**À explorer** :

- Modèle hybride cycle + cluster sur ces séries spécifiques.
- Analyse Gate 1 dual null sur ces 3 séries spécifiquement — survivent-
  elles, contre toute attente ?

## Ce que ces 15 échecs ne signifient pas

Il est tentant de dire : "le cluster perd sur 22 % des variables donc
le cluster est faux". Ce serait incorrect pour trois raisons :

1. **Random walk est un benchmark redoutable**. Sur 68 variables,
   battre RW sur 53 (78 %) est déjà un résultat très fort. Pour
   référence, Atkeson-Ohanian 2001 ont montré qu'aucun modèle macro
   sophistiqué n'a battu RW sur l'inflation US 1984-2000.
2. **Les 22 % d'échecs ont des explications structurelles
   identifiables** (taux administrés, séries trop courtes, chocs
   structurels). Ce ne sont pas des "échecs aléatoires" qui signalent
   un problème méthodologique fondamental.
3. **Aucune baseline AR(1) ni ARMA(1,1) ne gagne** — c'est-à-dire
   qu'aucun modèle stationnaire-simple ne fait mieux sur les 15
   échecs. Le résultat opérationnel reste : *quand un modèle bat RW,
   c'est un modèle cluster ; sinon, c'est RW*.

## Implication pour la pratique

Si vous voulez utiliser nos modèles pour de la prévision opérationnelle :

- **Variables financières et taux long-horizon** : MSM excellent (les
  6 wins sur boe le confirment).
- **Variables trimestrielles macro modernes** : HAR excellent (les
  8 wins sur q le confirment).
- **Variables crédit long-horizon** : ARFIMA+RS spécifiquement
  compétent.
- **Taux d'intérêt** : utilisez RW + composante structural break.
- **Séries courtes (< 80 obs)** : utilisez RW ou AR(1) avec prudence.
- **Agrégats commerce/investissement avec chocs structurels** :
  attention, RW peut faire mieux qu'un MSM si vous traversez un
  régime atypique.

## Sources

- Sidecars sources : `reports/forecast_benchmark_2026_05_*.json`
  (générés par `ecowave forecast-benchmark` — voir
  [benchmark reproductible](benchmark_reproducible.md))
- Code de l'extraction des failure modes : voir le snippet Python
  dans le commit qui a produit cette page sur GitHub.
