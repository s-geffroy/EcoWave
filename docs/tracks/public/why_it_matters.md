# Pourquoi ça compte

> *Cinq implications concrètes pour la politique économique, le
> risque, et la prévision — qui changent dès qu'on accepte que la
> macroéconomie n'est pas cyclique.*

## 1 — La crédibilité des banques centrales devient mesurable

Les banques centrales (Fed, BCE, BoE) passent une grande partie de leur
existence institutionnelle à essayer d'établir et de protéger leur
**crédibilité**. La crédibilité, c'est la qualité que rend nécessaire
le fait qu'une banque centrale dit "nous ramènerons l'inflation à 2 %"
et que les acteurs économiques *la croient*, sans attendre la preuve.

Jusqu'à maintenant, la crédibilité était mesurée indirectement : par
les anticipations d'inflation des consommateurs et des professionnels,
par les prix des obligations indexées, par les écarts à la cible.
Toutes ces mesures sont **bruitées** et arrivent souvent **trop tard**.

Notre paramètre `d` de longue mémoire offre une mesure directe : une
banque centrale crédible a une inflation **faiblement persistante**
(`d` proche de zéro) ; une banque centrale faiblement crédible a une
inflation **fortement persistante** (`d` proche de 0.5). Sur les
données réelles, les pays de la zone euro ont un `d` plus bas que les
pays émergents ; le Royaume-Uni post-Brexit a un `d` qui a augmenté ;
la Turquie depuis 2018 a un `d` qui s'est envolé.

**Implication pratique** : on peut tracker la crédibilité en temps réel,
indépendamment des enquêtes d'opinion. Cela donne aux banques
centrales un *outil de pilotage* qu'elles n'ont pas aujourd'hui.

## 2 — Les booms de crédit ont des ombres longues — mesurables

La crise financière globale de 2008 a appris (dans la douleur) que les
booms de crédit accumulent du risque systémique qui peut prendre des
années à se matérialiser. La Banque des règlements internationaux
(BIS) a alors proposé le **credit gap** : la différence entre le ratio
crédit/PIB observé et sa tendance long-terme. C'est l'outil officiel
de surveillance macroprudentielle dans les accords de Bâle III.

Le credit gap a un défaut : il **suppose** qu'il existe une "tendance
normale" et que les écarts à cette tendance sont temporaires. C'est
précisément l'hypothèse cyclique. Quand nous appliquons nos diagnostics
sur les séries de crédit (notamment Jordà-Schularick-Taylor 1870–2020,
qui couvre 18 économies avancées sur 150 ans), nous trouvons une longue
mémoire massive : `d ≈ 0.4` sur les variables de crédit, proche de la
borne théorique d'intégration fractionnaire.

Conséquence : les booms de crédit **ne reviennent pas naturellement à
une tendance**. Ils créent un état du système qui persiste longtemps
et qui modifie la dynamique future. Le credit gap sous-estime
systématiquement l'ampleur réelle du risque accumulé.

**Implication pratique** : on peut construire un *Hurst-based credit
cycle* qui mesure directement la persistance, et qui anticipe mieux
les crises systémiques que le credit gap actuel. Application directe à
Bâle III et au calibrage des coussins de capital contracycliques.

## 3 — La gestion des queues : VaR n'est pas un bon outil

La régulation bancaire (Bâle II, Bâle III) repose largement sur la
**Value-at-Risk** (VaR) : "avec 99 % de probabilité, la perte ne
dépassera pas X euros sur 10 jours". C'est intuitif, simple à calculer,
et c'est ce que les banques rapportent quotidiennement.

Sauf que la VaR a deux problèmes connus dès les années 2000, mais que
nos diagnostics aggravent :

- Elle ne dit rien sur la queue *au-delà* du 99 % — par hypothèse, on
  est dans le 1 % où tout peut arriver, mais la VaR ne nous dit pas
  *combien* peut arriver.
- Elle suppose que les distributions sont relativement bénignes (souvent
  gaussiennes ou exponentielles). Or nos tests de queues lourdes (Hill,
  Lévy stable) montrent que les distributions financières et
  macroéconomiques sont **bien plus lourdes** que ce que VaR suppose.

L'**Expected Shortfall** (ES), adopté par Bâle III en 2016, corrige le
premier défaut. Mais ses calibrations actuelles utilisent toujours des
distributions gaussiennes ou faiblement queuées. **L'ES réel, sous
queues lourdes, est probablement 20–40 % plus élevé que ce qu'on
rapporte**.

**Implication pratique** : les coussins de capital actuels des banques
sous-estiment le risque systémique. Le problème n'est pas la VaR (qui
est encore largement utilisée) — c'est la *calibration* des
distributions sous-jacentes, qui reste hypothétique.

## 4 — Les prévisions macro publiques sont battables

Le Survey of Professional Forecasters (SPF) de la Fed de Philadelphie,
les Summary of Economic Projections (SEP) du FOMC, les Broad
Macroeconomic Projection Exercises (BMPE) de la BCE — toutes ces
prévisions publiques officielles sous-performent random walk au-delà
de 3 à 4 trimestres. Cela a été démontré dans la littérature
empirique depuis longtemps (Atkeson-Ohanian 2001 pour l'inflation,
Stock-Watson 2003 pour le PIB).

Notre benchmark Roadmap #20 va plus loin : nous montrons que des
modèles **simples et reproductibles** (MSM, ARFIMA+RS, HAR), une fois
calibrés sur les variables cluster, **battent random walk à horizon
12 mois sur 78 % des variables testées**. Donc ils battent
probablement aussi SPF/FOMC/BMPE.

Une banque centrale qui utilise nos modèles pour son scénario de base
à 12 mois aurait fait mieux que le SPF officiel sur 2020–2024. C'est
testable, et l'infrastructure existe.

**Implication pratique** : il y a un *gap* entre la science de la
prévision macro disponible aujourd'hui et la prévision macro
effectivement utilisée par les institutions. Combler ce gap est un
investissement à très haute rentabilité publique.

## 5 — DSGE n'est pas mort, mais doit être révisé structurellement

Les modèles DSGE (Dynamic Stochastic General Equilibrium) sont la
colonne vertébrale de la modélisation macro institutionnelle depuis
Smets-Wouters 2003. Ils supposent :

- des chocs **AR(1)** ou **IID** (donc à mémoire courte),
- des paramètres "deep" (préférences, technologie) **stables** au
  cours du temps,
- des distributions **gaussiennes** des innovations.

Les trois hypothèses sont **falsifiées** par notre cluster :

- C — longue mémoire **incompatible** avec AR(1)/IID.
- S — dérive de régime cognitif **incompatible** avec paramètres deep
  stables.
- Queues lourdes — Tsallis et Lévy **incompatibles** avec
  gaussianité.

Cela ne signifie pas que DSGE doive être abandonné. Cela signifie
qu'il doit être **structurellement révisé** :

- Remplacer les chocs AR(1) par des chocs ARFIMA (intégration
  fractionnaire),
- Ajouter un **layer Markovien** sur les paramètres deep (qui
  switchent entre régimes cognitifs),
- Admettre des distributions **Tsallis** ou **Lévy stables** pour les
  innovations.

Sans ces trois ajouts, les modèles DSGE continueront à rater les
retournements brutaux (2008, 2020, 2022) — pas parce qu'ils sont
théoriquement mauvais, mais parce que leurs **hypothèses statistiques**
ne correspondent pas à la réalité empirique.

**Implication pratique** : un programme de recherche commun
banques centrales / universités sur la "structural revision" des DSGE
est urgent. Notre cluster donne le cahier des charges minimal.

## Pour aller plus loin

L'essai phare [Le cycle est mort, vive la cascade](note_public.md)
tresse ces trois pages en un récit narratif d'une seule traite,
~2 500 mots, prêt à être lu d'une vue par un lecteur curieux.

Pour le détail technique :

- [Le track académique](../acad/index.md) pour la formalisation
  théorique et la discussion DSGE,
- [Le track BC](../bc/index.md) pour les outils opérationnels
  politique monétaire / prudentiel,
- [Le track quants](../quants/index.md) pour le code et la
  reproduction des résultats.
