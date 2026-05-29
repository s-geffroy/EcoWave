# Feuille de route méthodologique

> **Résumé.** Cette feuille de route trace les choix de conception derrière
> le cadre *Cycle Position Vector* (CPV) actuel. Chaque item documente le
> problème, la méthode adoptée, le code concerné et le critère
> d'acceptation. Seuls les items actifs dans le pipeline courant sont
> listés.

---

## #1 — Null surrogate par phase publiée

- **Problème.** Sans null, un « cycle » trouvé dans n'importe quelle série
  bruitée ne peut pas être distingué d'une coïncidence.
- **Méthode.** Bootstrap AR(1) ([Torrence & Compo, 1998](../bibliographie.md#torrence-compo-1998) ;
  [Grinsted *et al.*, 2004](../bibliographie.md#grinsted-moore-jevrejeva-2004))
  ajustant AR(1) sur l'entrée, simulant $B = 1\,000$ trajectoires
  préservant moyenne / variance / persistance ; rejet du cycle si la
  band-power réelle n'excède pas le percentile $(1 - \alpha)$ des
  surrogates.
- **Code.** `ecowave/cycles/surrogate.py` (Porte 1) ;
  `ecowave/scoring/null_test.py` (null $\eta^2$ pilote-fenêtre) ;
  `ecowave/waves/model_f_cycles.py` (porte au niveau modèle).
- **Acceptance.** Chaque cellule de `cycle_positions` est publiée avec une
  $p$-value ; les cellules à $p \geq 0.05$ portent `phase = rejected`,
  `separable = 0`.

## #2 — Consensus multi-méthode

- **Problème.** Toute décomposition seule peut être spécifique à ses
  propres hypothèses paramétriques. Un cycle qui n'émerge que sous une
  méthode n'est pas un cycle robuste.
- **Méthode.** Quatre méthodes votantes aux hypothèses génératives très
  différentes votent sur chaque phase :
    - **D** — Détection PELT ([Killick *et al.*, 2012](../bibliographie.md#killick-fearnhead-eckley-2012))
    - **E** — Markov-switching ([Hamilton, 1989](../bibliographie.md#hamilton-1989))
    - **F** — CF Juglar + phase de Hilbert ([Christiano & Fitzgerald, 2003](../bibliographie.md#christiano-fitzgerald-2003))
    - **G** — Bry-Boschan ([Harding & Pagan, 2002](../bibliographie.md#harding-pagan-2002))

    Publier la phase modale seulement si $\geq 3$ sur 4 s'accordent ; sinon `disputed`.
- **Code.** `ecowave/cycles/consensus.py` (Porte 2) ;
  `ecowave/scoring/null_test.py:all_models_null_report` (panel par méthode).
- **Acceptance.** Les votes par méthode sont stockés dans
  `cycle_consensus` ; le rapport CPV liste l'étiquette de chaque méthode
  pour chaque cellule publiée.

## #3 — Universalité cross-groupes

- **Problème.** Un cycle qui n'existe que pour les pays à haut revenu
  n'est pas un « cycle global ».
- **Méthode.** Un cycle est qualifié `universal` pour un mois donné
  seulement si $\geq 4$ agrégats de revenu sur 5 (WLD + HIC + UMC + LMC
  + LIC) concordent sur la phase modale. Sinon `regional / idiosyncratic`.
- **Code.** `ecowave/cycles/universality.py` (Porte 3) ; persisté dans
  `cycle_universality`.
- **Acceptance.** Chaque cycle a un drapeau d'universalité dans le rapport CPV.

## #4 — Holdouts hors-échantillon pré-enregistrés

- **Problème.** L'ajustement intra-échantillon est la source canonique
  des faux positifs macroéconomiques (Bailey & López de Prado 2014).
- **Méthode.** Les pilotes `2020` et `2022` sont des holdouts
  pré-enregistrés (champs `registered_at` et `holdout` sur `Pilot`).
  Gelés *avant* la finalisation des fenêtres de référence du manifest.
- **Code.** `ecowave/pilots.py` ; `ecowave/evaluation.py` (AUROC EWS
  poolé + par-pilote, y compris holdouts).

## #5 — Extension historique longue (Maddison + Jordà-Schularick-Taylor) — IMPLÉMENTÉ

- **Problème.** 65 ans de données WB $\approx 1.0$–$1.5$ cycle de
  Kondratieff. La Porte 1 (bootstrap AR(1)) ne peut pas distinguer une
  vraie K-wave d'une excursion lisse de bruit rouge sur si peu de
  cycles.
- **Méthode.** Ajouter un deuxième chemin d'ingestion lisant Maddison
  Project 2023 (PIB par habitant réel 1820-2022) et
  Jordà-Schularick-Taylor R6 (crédit, prix immobiliers, actions, taux
  long, CPI, monnaie pour 18 économies avancées 1870-2020). 154 ans ×
  18 pays donnent $\geq 3$ K-waves, $\geq 8$ Kuznets, $\geq 17$ Juglar.
- **Code.** `ecowave/cycles/long_history.py` ; nouveau
  `long_history_manifest.json` ; option CLI `position-cycles --horizon long`.
- **Acceptance.** Sur le panel long-horizon, le signal Juglar émerge
  proprement à la période attendue (~9 ans) ; K3 et K4 sont retrouvés à
  $\pm 5$ ans de la datation de [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010).

## #6 — Composite par bande — IMPLÉMENTÉ

- **Problème.** Le composite original z-scorait chaque indicateur sur son
  historique complet puis moyennait sur indicateurs. Le contenu cyclique
  à une fréquence donnée était dilué par les indicateurs non-cycliques
  à cette fréquence.
- **Méthode.** Pour chaque bande, d'abord filtrer CF chaque indicateur
  dans la bande, puis z-scorer et moyenner. La composite est désormais
  spécifique à la bande et concentre la puissance cyclique dans la cible.
- **Code.** `ecowave/cycles/runner.py:_composite_panel(panel, band=...)`.
- **Acceptance.** Sur le panel WB avec `--null dual`, le nombre de
  cellules survivant à la Porte 1 est passé de 4 à 7, avec des phases
  concrètes (contraction / expansion) au lieu de simples `disputed`.

## #7 — Null dual (AR(1) + scramble de phase) — IMPLÉMENTÉ

- **Problème.** Le bootstrap AR(1) absorbe une partie du contenu cyclique
  dans le paramètre de persistance $\varphi$ (Vyushin & Kushner 2009).
  Le scramble de phase ([Theiler, 1992](../bibliographie.md#theiler-et-al-1992))
  préserve exactement le spectre ; les deux sont complémentaires.
- **Méthode.** Calculer les deux nulls ; une cellule passe la Porte 1
  seulement quand **les deux** rejettent. La porte duale conservative
  approche un vrai test « cycle réel ».
- **Code.** `ecowave/cycles/surrogate.py:phase_scramble_null` +
  `dual_null`. Option CLI `--null dual`.
- **Acceptance.** La porte duale est par définition $\geq$ chaque porte
  individuelle ; elle attrape les faux positifs propres à chaque null.

## #8 — Puissance wavelet comme statistique alternative — IMPLÉMENTÉ

- **Problème.** La band-power CF est sensible au bord sur les derniers
  $\lfloor \text{hi\_years} / 2 \rfloor$ échantillons — précisément la
  zone la plus pertinente pour la politique économique.
- **Méthode.** Utiliser le scaleogramme Morlet $|W(s, t)|^2$ intégré
  dans la bande comme statistique de test ; bootstrap AR(1) comme
  distribution nulle. Moins sensible au bord que CF.
- **Code.** `ecowave/cycles/surrogate.py:wavelet_bandpower_null`.
  Option CLI `--null wavelet`.

## #9 — Extension trimestrielle pour Kitchin — IMPLÉMENTÉ

- **Problème.** La fréquence annuelle plafonne Kitchin à la bande haute
  4-5 ans (Nyquist).
- **Méthode.** Chemin d'ingestion trimestriel : FRED `GDPC1` /
  `CPIAUCSL` / `UNRATE` pour les États-Unis, Eurostat
  `namq_10_gdp` / `prc_hicp_mmor` / `une_rt_q` pour l'agrégat Euro Area
  (EA20, 1995-présent) et pour DE/FR/IT, séries miroir OECD/IFS
  hébergées sur FRED (`JPNRGDPEXP`, `NGDPRSAXDCGBQ`, `NGDPRSAXDCCAQ`,
  `JPNCPIALLMINMEI`, `GBRCPIALLMINMEI`, `LRUNTTTTJPM156S`,
  `LRUN64TTGBQ156S`) pour JPN/GBR/CAN. La connexion SDMX 2.1 directe à
  `sdmx.oecd.org` reste expérimentale — le registre de structure
  retourne payload vide sur les chemins standards `/datastructure` et
  `/dataflow?references=descendants`, rendant l'introspection du DSD
  impossible sans hardcoding par dataflow. Trois variables au
  v1 : `Q_GDP` (log-différence annualisée), `Q_CPI` (log-différence
  annualisée), `Q_UNRATE` (niveau). Six groupes : USA, EA, JPN, GBR,
  G7Q, OECDQ. Le runner threade `samples_per_year=4` dans CF + Morlet +
  surrogates ; la conditionnelle Kitchin du runner libère la bande
  complète 3-5 ans (le chemin annuel `--horizon wb` continue à narrower
  4-5 ans comme diagnostic). Période EA = 1995-présent (124 trimestres,
  $\geq$ 25 cycles Kitchin) ; flag noté dans le rapport.
- **Code.** `ecowave/cycles/quarterly.py` ;
  `quarterly_manifest.json` ; nouvelle table SQLite
  `cycle_observations_quarterly` (schéma 0.5.1) ; option CLI
  `position-cycles --horizon quarterly`. Tests :
  `tests/test_quarterly_panel.py`,
  `tests/test_samples_per_year_thread.py`,
  `tests/test_kitchin_gate_conditional.py`,
  `tests/test_runner_quarterly_smoke.py`.
- **Acceptance.** Sur le run `2026-05` :
    - Kitchin **séparable** ($p = 0.001$) sur les 6 groupes
      (USA, EA, JPN, GBR, G7Q, OECDQ) là où le rapport `_wb` annuel
      affiche `rejected` partout.
    - USA Kitchin = `contraction` (Gate 2 consensus), GBR Juglar +
      Kuznets = `contraction`, OECDQ Juglar = `contraction`.
    - Non-régression sur `--horizon wb` : aucun changement de phase
      Juglar/Kuznets/Kondratieff par rapport au run pré-Path-5.

## #11 — Pondération des méthodes par bande — IMPLÉMENTÉ

- **Problème.** Le run trimestriel 2026-05 a montré que **D** (PELT) et
  **G** (Bry-Boschan) se calibrent mal sur certaines bandes :
    - **D sur Kitchin (3-5 ans)** : la longueur typique d'un segment
      PELT (5-10 ans sur des séries macro) dépasse la période du
      cycle, ce qui fait que le dernier segment moyenne plusieurs
      cycles et que la phase de fin est dominée par la tendance, non
      par le cycle. Vote constant sur Kitchin : `expansion`.
    - **G sur Kitchin** : la datation Bry-Boschan / Harding-Pagan
      requiert un cycle complet pour déclarer un pic/creux ; sur
      Kitchin à résolution trimestrielle, l'incertitude sur les 1-2
      derniers trimestres rend la classification systématiquement
      "post-pic descendant". Vote constant : `contraction`.
    - **D sur Kondratieff (40-60 ans)** : sur 66 ans de panel, il n'y
      a que 1.1 à 1.65 K-cycles. PELT collapse à un segment unique →
      classification non-informative.
- **Méthode.** Pré-enregistrer une **liste de méthodes admises par
  bande** dans `CYCLE_BANDS[band]["methods"]`, avec un seuil
  d'accord ad-hoc `min_agreement` :
    - Kitchin : `(F, E)`, seuil 2 (unanimité du panel admis).
    - Juglar : `(D, E, F, G)`, seuil 3 (3/4 — règle historique
      conservée).
    - Kuznets : `(D, E, F, G)`, seuil 3 (idem).
    - Kondratieff : `(E, F, G)`, seuil 2 (majorité du panel admis).
  Les votes des méthodes écartées restent **persistés** dans
  `cycle_consensus` pour la transparence ; ils ne pèsent simplement
  pas dans la Porte 2.
- **Code.** `ecowave/cycles/bands.py` (champs `methods` +
  `min_agreement`) ; `ecowave/cycles/consensus.py` (kwarg
  `allowed_methods` + `min_agreement`) ; `ecowave/cycles/runner.py`
  (passage des deux depuis la bande). Test :
  `tests/test_consensus_per_band.py` (7 cas).
- **Acceptance.** Sur le run quarterly 2026-05, gain net de 4
  cellules à consensus :
    - **GBR Kitchin** : disputed → **`peak`** (F+E concordent).
    - **G7Q Juglar** : disputed → **`contraction`** (3/4).
    - **OECDQ Juglar** : disputed → **`contraction`** (3/4).
    - **GBR Kondratieff** : disputed → **`expansion`** (E+G majoritaires).
  Les cellules USA Kitchin = `contraction`, EA Kuznets = `expansion`
  restent stables. Aucune cellule n'a régressé hors variabilité
  stochastique de Markov-switching d'une exécution à l'autre.

## #10 — Variables manquantes (couverture) — TODO

- L'indicateur de protestations `S` (S2, Mass Mobilization / ACLED
  post-2020) et l'indicateur de tonalité narrative `I` (I2, GDELT tone)
  restent à ingérer — tous deux listés `not_automatable_v1` dans
  `sources_manifest.json`.
- La couverture symétrique US + zone euro sur les courbes S et D est
  partielle ; ECB CISS démarre en 1999, ce qui affaiblit C3 (robustesse
  bi-fenêtre) sur D.

## #12 — Évidence par variable (test Gate 1 sans compositing) — IMPLÉMENTÉ

- **Problème.** Le composite z-scoré dilue les cycles sectoriels :
  Kitchin (1923) découvert sur chargements ferroviaires devient
  invisible sur le composite GDP+inflation+chômage+crédit, parce que
  les séries sans contenu Kitchin sont z-scorées à variance unitaire et
  moyennées comme du bruit. Cf. [Wen (2005)](../bibliographie.md#wen-2005)
  qui démontre que le cycle d'inventaire **existe** sur les séries
  sectorielles mais pas sur le PIB.
- **Méthode.** Pour chaque (horizon, agrégat, variable, cycle), z-scorer
  la **série individuelle** (pas le composite) et lancer Gate 1 avec le
  même null dual et le même nombre de surrogates que sur le composite.
  Publie la matrice de p-values brute et le **taux de survie par
  variable** (combien d'agrégats voient le cycle survivre quand on isole
  cette variable).
- **Code.** `ecowave/cycles/evidence.py` (calcul + rendu) ;
  commande `ecowave evidence-per-variable --as-of YYYY-MM`. Sorties :
  `reports/cycle_position_per_variable_*.json` (sidecars par horizon)
  et `docs/evidence_per_variable.md` (page publique de la section 1
  de la nav).
- **Acceptance.** La page démontre la thèse centrale du projet : les
  rejets composites sont cohérents avec la littérature critique
  empirique moderne ([Wen 2005](../bibliographie.md#wen-2005) pour
  Kitchin, [Solomou 1987](../bibliographie.md#solomou-1987) pour
  Kuznets/Kondratieff, etc.).

## #13 — Allongement des séries temporelles — TODO

- **Problème.** L'inférence statistique sur les cycles longs souffre
  d'un manque de répétitions dans l'échantillon. Le panel WB
  (1960-2024) capture ~1.3 cycles Kondratieff — quasiment impossible
  à distinguer d'un AR(1). L'horizon long (Maddison + JST, 1870-2022)
  porte à ~3 K-waves, encore marginal pour la puissance statistique.
  Plus de cycles dans l'échantillon = plus de puissance pour battre
  les nulls et reproduire (ou réfuter) les observations originales
  des découvreurs.
- **Méthode.** Quatre voies complémentaires d'extension envisagées :

    1. **Bank of England — A Millennium of Macroeconomic Data for the
       UK (1086-2024).** ~940 ans de prix, taux d'intérêt, PIB, masse
       monétaire, dette publique sur l'Angleterre/UK. Open access (CC0).
       Permet ~16 K-waves complets sur un seul pays, ce qui rend la
       statistique du cycle long enfin **possible**. Référence :
       BoE Working Paper 845 (Thomas & Dimsdale, 2017, mises à jour
       annuelles).
    2. **Mitchell — International Historical Statistics (1750-2010).**
       Trois volumes Cambridge UP (Europe, Americas, Africa-Asia-Oceania)
       couvrant ~260 ans, 100+ pays, séries sectorielles (charbon,
       fonte, wagons, agriculture). Crucial parce que **ces variables
       sectorielles matchent ce que Kitchin / Juglar / Kuznets ont
       analysé à l'origine** — directement adressable par l'Option A
       (#12) sur les séries originales des découvreurs.
    3. **JST extensions + BIS macroprudential database (1880-2024).**
       Approfondir les séries crédit/HPI Schularick-Taylor et ingérer
       les séries BIS long-term sur ratios crédit/PIB, dette des
       ménages, prix immobiliers. Précis sur cycles financiers
       (Borio-Drehmann) mais peu de variables réelles. Existing JST R6
       à étendre.
    4. **Toutain / INSEE — séries historiques françaises (1789-1990).**
       Reconstruction Toutain (1987-1997) du PIB français + séries
       sectorielles ; INSEE rebases pour les périodes post-1949.
       Spécialisé France mais ~235 ans, complémentaire à Maddison
       (qui est plus généraliste mais moins détaillé).

- **Code.** À écrire dans `ecowave/cycles/` :
    - `boe_millennium.py` (loader BoE)
    - `mitchell_ihs.py` (loader Mitchell volumes)
    - extension de `cycles/long_history.py` pour les sources additionnelles
- **Acceptance.** Le panel "histoire longue" couvre ≥ 200 ans pour
  ≥ 5 agrégats avec ≥ 10 variables ; Gate 1 dual-null sur Kondratieff
  doit avoir suffisamment de puissance pour distinguer le cycle d'un
  AR(1) — c'est-à-dire un p-value ≤ 0.05 sur au moins l'agrégat
  Banque Mondiale ou ADV18-étendu.

## Références

- Bailey, D. H., & López de Prado, M. (2014). The deflated Sharpe ratio.
- [Christiano & Fitzgerald (2003)](../bibliographie.md#christiano-fitzgerald-2003).
- [Grinsted *et al.* (2004)](../bibliographie.md#grinsted-moore-jevrejeva-2004).
- [Hamilton (1989)](../bibliographie.md#hamilton-1989).
- [Harding & Pagan (2002)](../bibliographie.md#harding-pagan-2002).
- [Killick *et al.* (2012)](../bibliographie.md#killick-fearnhead-eckley-2012).
- [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010).
- [Theiler *et al.* (1992)](../bibliographie.md#theiler-et-al-1992).
- [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998).
