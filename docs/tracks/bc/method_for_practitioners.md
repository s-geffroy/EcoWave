# La méthode CPV pour les praticiens

> *Comment lire le protocole CPV quand on travaille dans une banque
> centrale. Ce qui est nouveau, ce qui est compatible avec vos outils
> existants, et ce qui mérite votre attention.*

## Ce qui est nouveau

Le protocole CPV introduit **trois portes de falsifiabilité** sur les
mécanismes cycliques classiques. Aucun cadre BC standard ne fait
aujourd'hui cet exercice avec cette rigueur. C'est un *complément*
diagnostique, pas un remplacement de votre boîte à outils.

Concrètement, sur chaque variable macro (inflation, PIB, crédit,
chômage…) et sur chaque agrégat géographique pertinent, le protocole
répond à : *cette série porte-t-elle un cycle réel à 7-11 ans
(Juglar) ? à 15-25 ans (Kuznets) ? à 40-60 ans (Kondratieff) ?*

La réponse est falsifiable. Soit la cellule passe les trois portes,
soit elle échoue à au moins une — et on sait laquelle, avec une
p-value.

## Pourquoi cela importe institutionnellement

Si votre modèle de prévision macro suppose implicitement l'existence
d'un cycle à une fréquence donnée (par exemple un cycle des affaires
de 7-9 ans, ou un cycle financier de 16-20 ans Borio), notre verdict
vous concerne directement :

- **Le cycle des affaires Juglar (7-11 ans)** ne survit pas aux trois
  portes sur les 6 panels testés. Vos hypothèses de retour à la
  moyenne sur ce horizon doivent être réexaminées.
- **Le cycle financier 16-20 ans Borio** que la BIS utilise pour la
  surveillance macroprudentielle est plus proche de Kuznets. Notre
  verdict : Kuznets ne survit pas non plus. Le credit gap reste utile
  *comme indicateur*, mais sa narrative cyclique n'est pas validée.
- **Le cycle technologique Kondratieff** : narrativement utile pour
  les économistes économiques de long terme, mais sans validation
  statistique. À utiliser comme grille herméneutique uniquement.

## Les trois portes en langage BC

### Porte 1 — Dual null hypothesis test

**Ce que ça fait** : prend votre série, génère 1 000 séries simulées
qui ont les *mêmes propriétés statistiques observables* (variance,
autocorrelation, spectre) mais *sans cycle réel*. Compare la
band-power de votre série avec la distribution simulée. Si votre série
n'est pas dans le quantile (1 - α) des simulations, le cycle est
significatif.

**Pourquoi *dual*** : on utilise deux méthodes de simulation
indépendantes (AR(1) bootstrap + phase-scrambling). Une cellule passe
seulement si **les deux** méthodes rejettent. C'est conservateur — on
écarte les faux positifs spécifiques à chaque méthode de simulation.

**Référence** : Theiler 1992, Torrence-Compo 1998, Grinsted-Moore-
Jevrejeva 2004.

**Lien BC** : c'est la version macroéconomique du *placebo control*
en essai clinique. Sans ce contrôle, n'importe quel mouvement visuel
peut être interprété comme "le retour du cycle".

### Porte 2 — Consensus multi-méthode

**Ce que ça fait** : quatre méthodes de décomposition aux hypothèses
paramétriques très différentes votent indépendamment sur la phase
courante du cycle :

- **PELT** (Killick-Fearnhead-Eckley 2012) — segmentation par
  détection de ruptures
- **Markov-switching** (Hamilton 1989) — modèle à régimes latents
- **Christiano-Fitzgerald + Hilbert** (Christiano-Fitzgerald 2003) —
  filtre band-pass + phase instantanée
- **Bry-Boschan** (Harding-Pagan 2002) — détection de turning points

Une cellule passe seulement si **au moins 3 sur 4** s'accordent.

**Lien BC** : c'est l'équivalent statistique de la pratique
*Monetary Policy Committee* — quand un signal n'est pas robuste à
quelle méthode on utilise, on ne lui accorde pas confiance.

### Porte 3 — Universalité cross-agrégats

**Ce que ça fait** : un cycle macroéconomique global doit se
manifester dans **au moins 4 agrégats sur 5** par niveau de revenu
(WLD + HIC + UMC + LMC + LIC). S'il n'apparaît que pour HIC, ce n'est
pas un cycle global — c'est un cycle régional spécifique aux
économies avancées.

**Lien BC** : utile pour la coordination internationale et le suivi
des spillovers. Si vous coordonnez avec la Fed ou la BCE sur un
diagnostic de cycle commun, la Porte 3 vous dit si ce diagnostic tient
au-delà de votre périmètre.

## Le verdict de ces portes

Sur les 6 panels que nous testons (Banque mondiale 1960-2024, panel
trimestriel 1995-2024, histoire longue Maddison + Jordà-Schularick-
Taylor 1870-2024, Bank of England Millennium 1700-2016, BIS
macroprudentiel 1970-2024, sectoral history US/UK/WORLD), **les
quatre cycles canoniques échouent systématiquement**. Les quelques
cellules qui survivent à la Porte 1 échouent à la Porte 2 ou à la
Porte 3.

**Implication pour la modélisation macroéconomique BC** : les chocs
cycliques que vous calibrez dans vos modèles DSGE (et qui sont
typiquement AR(1) avec une persistance moyenne de 0.6-0.8) ne
correspondent pas à des cycles canoniques mais à *une moyenne lisse
sur une dynamique fractale non-linéaire à mémoire longue*. Ce n'est
pas la même chose, et ça a des conséquences que les outils CPV peuvent
quantifier.

## Ce qui reste utilisable de votre boîte à outils

**Vos modèles DSGE ne sont pas à jeter**. Mais leurs hypothèses
statistiques sous-jacentes doivent être révisées :

- **Chocs AR(1) ou IID → chocs ARFIMA**. La longue mémoire `d` GPH
  estimée sur vos résidus de modèle est généralement positive et
  significative. Calibrer un AR(1) qui ignore cela sous-estime la
  persistance des chocs et donc sous-réagit aux chocs persistants.
- **Paramètres "deep" stables → layer Markov sur ces paramètres**.
  Smets-Wouters 2003 calibre des paramètres (préférences, technologie)
  comme s'ils étaient invariants dans le temps. Notre famille S
  documente empiriquement des changements de régime cognitif. Volcker
  1979 est un cas connu, mais le phénomène est plus général.
- **Innovations gaussiennes → innovations à queues lourdes**. Notre
  test Hill et Lévy stable rejette systématiquement la gaussianité.
  Pour les coussins de capital prudentiels, c'est central.

Concrètement, beaucoup de praticiens BC font déjà certains de ces
ajustements localement (ad-hoc, par expérience). Notre cadre les
rend systématiques et falsifiables.

## Ce qui est nouveau et compatible

**Les outils du track BC** (présentés dans les pages voisines) sont
designés pour être *insérables* dans une pipeline BC existante :

- **[Credibility radar](credibility_radar.md)** — calcule `d` GPH sur
  l'inflation. Indicateur unique, mensuel. Peut être ajouté à un
  dashboard chief economist sans changer rien d'autre.
- **[Forward guidance réflexif](forward_guidance_reflexive.md)** —
  cadre conceptuel pour interpréter la communication BC. Pas un
  modèle calibrable, mais une grille pour interpréter Volcker 1979,
  Greenspan 2003, Draghi 2012, Powell 2021-22.
- **[Tipping point detection](tipping_point_detection.md)** — EWS
  sur régime drift. Implémentation Python ouverte, peut être adaptée
  à votre série interne.
- **[Horizon-aware targeting](horizon_aware_targeting.md)** —
  recommandations sur quel modèle utiliser à quel horizon (HAR court,
  ARFIMA+RS long).

## Les contraintes institutionnelles que nous reconnaissons

Travailler dans une BC impose des contraintes que la recherche
universitaire peut ignorer :

- **Communication** : un modèle nouveau ne peut pas remplacer du jour
  au lendemain le modèle officiel. Notre cadre se positionne comme
  *complément diagnostique*, pas comme refonte.
- **Continuité historique** : les comparaisons internationales et
  intertemporelles imposent de maintenir certains protocoles
  longtemps. Les outils CPV peuvent tourner en parallèle de votre
  méthodologie standard.
- **Robustesse** : un signal qui s'effondre dès qu'on change de
  période ou de pays ne peut pas guider une décision de politique
  monétaire. Nos diagnostics sont volontairement conservateurs (dual
  null, consensus 3/4, universalité 4/5).
- **Transparence** : la BCE et la Fed publient leurs codes de plus
  en plus. Notre projet est entièrement open-source sous MIT, code
  Python conteneurisé Docker, reproductible en une commande.

## Pour commencer

1. **Lire la [note phare BC](note_bc.md)** (~5 000 mots). Synthèse
   prête à être circulée à votre équipe.
2. **Tester le [credibility radar](credibility_radar.md)** sur votre
   propre série d'inflation pour votre juridiction. ~30 minutes,
   Docker, résultat lisible.
3. **Évaluer [horizon-aware targeting](horizon_aware_targeting.md)** :
   est-ce que votre modèle officiel utilise un modèle adapté à votre
   horizon de politique monétaire (généralement 6-8 trimestres) ?
4. **Consulter [forward guidance réflexif](forward_guidance_reflexive.md)**
   pour la prochaine séance de communication MPC : votre annonce
   modifie-t-elle le régime cognitif anticipé ?

## Ressources complémentaires

- [Méthodologie technique détaillée](../../methodology/protocole_cpv.md) —
  les 3 portes en formalisme statistique complet
- [Verdict consolidé](../../forecast_benchmark.md) — PASS 78 % sur
  68 variables
- [Implications multi-axe](../../reference/implications_of_cluster.md) —
  les 4 axes (modélisation, prévision, politique, théorie) en détail
- [Working paper V1](../../papers/cpv_main_paper.md) — ~10 000 mots,
  réfutation-first, décembre 2025
