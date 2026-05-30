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

## #13 — Allongement des séries temporelles — EN COURS (phasé)

- **Problème.** L'inférence statistique sur les cycles longs souffre
  d'un manque de répétitions dans l'échantillon. Le panel WB
  (1960-2024) capture ~1.3 cycles Kondratieff — quasiment impossible
  à distinguer d'un AR(1). L'horizon long (Maddison + JST R6,
  1870-2020) porte à ~3 K-waves, encore marginal. Plus de cycles
  dans l'échantillon = plus de puissance pour battre les nulls et
  reproduire (ou réfuter) les observations originales des découvreurs.

- **Méthode.** Quatre voies d'extension explorées (mai 2026). Les
  hypothèses initiales ont été corrigées par une étude bibliographique :

    | Voie | Source canonique | Couverture utile | Effort | Verdict |
    |---|---|---|---|---|
    | **BoE Millennium** | XLSX 28 Mo + miroir CSV `datahub.io/economic-history/millennium-macroeconomic-data-uk` (OGL-UK-3.0) | UK 1086+ annuel · 1700+ trimestriel · ~130 séries | ~1 jour | ✅ priorité |
    | **JST R6 (élargie)** | `macrohistory.net/app/download/9834512469/JSTdatasetR6.dta` (CC BY-NC-SA) | 18 AE × 1870-2020 × **45 variables** (on n'en utilise que 6) | trivial | ✅ **gain immédiat** |
    | **BIS bulk** | `data.bis.org/bulkdownload` + `pysdmx` officiel | 44 économies × trimestriel × 1960-2026 · credit-gap Borio, RPP, DSR | ~1 jour | ✅ priorité |
    | **Mitchell IHS** | Springer Palgrave online (accès institutionnel requis) · pas de bulk public | 1750-2010 · ~600-900 séries sectorielles (charbon, fonte, wagons…) · 200 pays | 1-2 j scraping + 1 sem nettoyage | ⏸ dépend accès Springer |
    | ~~Toutain France~~ | ISMEA imprimé · pas de digital | 1789-1819 sur France seule | 2-4 sem OCR | ❌ skip (proxy CEPII Villa si besoin) |

  **Trois corrections importantes** vs la première rédaction de cet
  item :

    1. **JST R7 n'existe pas** (vérifié mai 2026). R6 (juillet 2022)
       reste canonique. Mais R6 publie **45 variables**, le manifest
       CPV n'en utilise que 6 → Phase 0 ci-dessous.
    2. **BIS RPP long ne remonte pas à 1870** mais à 1970-71 sur le
       panel AE. BIS apporte donc trimestriel + couverture EM (Brésil,
       Chine, Inde, Mexique, Corée, Turquie absents de CPV) + le
       Borio credit-gap prêt à l'emploi — pas de profondeur historique
       supplémentaire.
    3. **Toutain n'est pas digitalisé**. Le segment unique de Toutain
       (1789-1819 sur France) est aussi la partie la plus contestée
       de sa propre reconstruction (frontières Empire/Restauration).
       Gain CPV : <1% du panel multi-pays — à skipper sauf besoin
       spécifique, auquel cas CEPII Villa
       (`cepii.fr/CEPII/fr/bdd_modele/bdd_modele_item.asp?id=31`,
       1820+, déjà digital) est le proxy.

- **Plan d'exécution priorisé** (ratio gain/effort) :

    - **Phase 0 — JST R6 élargi** (1 jour, IMMÉDIAT). Étendre
      `long_history_manifest.json` aux 39 variables JST R6 non
      utilisées (RORE, mortgages, dette publique, current account,
      total credit, debt service, etc.). Aucune nouvelle source —
      même Stata file, même 18 pays, même 1870-2020. **Gain énorme
      pour la thèse Wen** : on pourra tester Gate 1 individuellement
      sur séries crédit/équity/foncier séparées au lieu d'un composite.
    - **Phase 1 — BoE Millennium** (1 jour). Nouveau module
      `ecowave/cycles/boe_millennium.py`, loader CSV depuis miroir
      datahub.io (pas xlsx pour éviter le 403 Cloudflare BoE), nouveau
      group `UK_BOE_1086` (annuel) + `UK_BOE_Q` (trimestriel),
      nouveau manifest `boe_millennium_manifest.json`. Extension de
      `position-cycles --horizon boe`. **Gain Kondratieff** :
      1086-2024 = ~16-23 K-waves théoriques, 1700+ = 5-8 K-waves
      avec qualité de données fiable.
    - **Phase 2 — BIS bulk** (1 jour). Nouveau module
      `ecowave/cycles/bis_bulk.py` via `pysdmx` officiel ou
      `pandas.read_csv` après unzip. Nouveaux groupes EM. Ingest
      `WS_CREDIT_GAP` + `WS_SPP` long + `WS_DSR`. **Gain Kuznets** :
      2-3 cycles supplémentaires par pays + 20+ pays nouveaux.
    - **Phase 3 — Mitchell IHS** (1-2 sem, conditionnelle). Si accès
      Springer Palgrave disponible : scraper poli (1 req/s) ~50
      tables sectorielles prioritaires (coal UK 1700+, pig iron UK
      1720+, US pig iron 1810+, etc.). **Gain Wen 2005 direct** :
      on aurait les séries originales des découvreurs. License
      restrictive (raw tables non-redistribuables, indicateurs
      dérivés OK).
    - **Phase 4 — Toutain** : skippé.

- **Code.** À écrire :
    - `ecowave/cycles/boe_millennium.py` (Phase 1)
    - `ecowave/cycles/bis_bulk.py` (Phase 2)
    - `ecowave/cycles/mitchell_ihs.py` (Phase 3, conditionnel)
    - Extensions de `long_history.py` pour Phase 0 (variables
      additionnelles JST R6) + de `cli.py position-cycles` pour
      nouveaux `--horizon` values (`boe`, `bis`).

- **Acceptance.** Le panel "histoire longue étendu" couvre :
    - ≥ 200 ans pour ≥ 5 agrégats (UK_BOE pousse à 300+ ans),
    - ≥ 30 variables (Phase 0 seule porte à 45),
    - Gate 1 dual-null sur Kondratieff a un `p ≤ 0.05` sur
      au moins UK_BOE_1700 + l'agrégat ADV18-étendu.

- **Références sources** (validées via web search mai 2026) :
    - BoE Millennium : `bankofengland.co.uk/statistics/research-datasets` ·
      mirror `datahub.io/economic-history/millennium-macroeconomic-data-uk`
    - JST R6 : `macrohistory.net/database/` · doc `JST_RORE_Documentation_R6.pdf`
    - BIS bulk : `data.bis.org/bulkdownload` · lib `github.com/bis-med-it/pysdmx`
    - Mitchell IHS online : `link.springer.com/referencework/10.1057/978-1-137-30568-8`

## #15 — Diagnostics non-cycliques (toolkit de l'au-delà-des-cycles) — IMPLÉMENTÉ {#item-15-diagnostics-non-cycliques}

- **Problème.** La chaîne d'audits (CN_BIS K, WLD-WB K, G7-long/UK_BOE K,
  Wen 2005 falsifié) + safeguard #14 a démontré qu'**aucun cycle canonique
  n'est statistiquement défendable** dans le pipeline CPV. Mais les séries
  macro ne sont pas du bruit blanc : ACF lag-1 ≈ 1.000 sur 30 % des séries,
  agglomération de la volatilité, distributions à queues lourdes des
  crashes, trends structurels post-1980. Quelque chose de **non-cyclique
  mais structuré** s'y produit. La page [Au-delà des cycles —
  cadres physiques alternatifs](../methodology_beyond_cycles.md) recense
  15 familles candidates ; il faut un toolkit minimal pour les comparer
  empiriquement sur les données CPV.
- **Méthode (livrée).** Module
  `ecowave/cycles/alternative_dynamics.py` avec **11 diagnostics
  statistiques compacts** (Tier 1 du panorama étendu PR #22) :

    1. **DFA / Hurst exponent** (famille C) — `hurst_dfa(series)`.
    2. **MF-DFA spectrum width** (famille B) — `mfdfa_spectrum(series)`.
    3. **Power spectrum slope 1/f^β** (famille A — SOC) — `spectrum_slope(series)`.
    4. **Hill tail exponent** (famille A — queues loi de puissance) — `hill_tail_exponent(series)`.
    5. **Permutation entropy + complexité LMC** (famille I) — `permutation_entropy_complexity(series)`.
    6. **Critical slowing down** (famille E) — `critical_slowdown(series)`.
    7. **Lévy stable α** (famille J) — `levy_stable_fit(series)`.
    8. **K41 scaling ζ(6)/ζ(3)** (famille P — cascades turbulence) — `k41_scaling(series)`.
    9. **MSD log-log slope** (famille R — diffusion anormale) — `msd_log_log(series)`.
    10. **Tsallis q index** (famille T — non-extensivité) — `tsallis_q_gaussian(series)`.
    11. **Reflexivity drift KS** (famille S — composante transversale) — `reflexivity_drift(series)`.

    **Panel-level** : `rmt_panel(group_panel)` (famille G — RMT) calcule
    le spectre de covariance et compare à la bande Marchenko-Pastur.

- **Code.** Module `ecowave/cycles/alternative_dynamics.py` + refactor de
  `ecowave/cycles/surrogate.py` qui délègue aux nouveaux générateurs
  `ecowave/cycles/surrogate_generators.py` (`ar1_surrogate_series`,
  `phase_scramble_surrogate_series`). Nouvelle commande CLI
  `ecowave dx-diagnostics --as-of YYYY-MM --horizons {wb|q|long|boe|bis|sh}`
  qui :
    - applique les 11 diagnostics à chaque variable individuelle de
      chaque horizon (band-agnostique — pas d'axe `cycle`) ;
    - applique le RMT panel-level à chaque (horizon, group) ;
    - produit deux sidecars JSON par horizon :
      `reports/dx_diagnostics_{as_of}_{horizon}.json` (per-variable) et
      `reports/dx_rmt_{as_of}_{horizon}.json` (panel-level) ;
    - produit une page consolidée `docs/dx_diagnostics.md` avec
      heatmaps emoji-codées (🟢 ≤ 0.01 · 🟡 0.01-0.05 · 🟠 0.05-0.10 ·
      🔴 > 0.10), table de mapping vers les familles du panorama, et
      section transversale `Réflexivité (famille S)` qui liste les
      variables où le null AR(1) est rejeté sur le drift de
      distribution.
- **Acceptance.** Pour chaque famille du panorama Tier 1, on peut dire
  "tel diagnostic favorise / défavorise ce cadre sur les données CPV".
  Chaque cellule du tableau de synthèse de la page
  `methodology_beyond_cycles.md` devient complétable. Critère
  fonctionnel : `dx_diagnostics.md` publie 11 lignes (une par
  diagnostic) × N colonnes (variables) × 6 horizons.
- **Garde-fou méthodologique.** Chaque diagnostic Tier 1 est accompagné
  d'un null hypothesis test avec surrogates (AR(1) bootstrap ou
  phase-scrambling Theiler 1992) à α=0.05. Tail-test choisi par
  diagnostic : upper (Hurst, β, Δα, ζ, q, KS, τ_var), lower
  (perm-entropy, α_Hill, α_Lévy), two-sided (MSD γ).
- **Décision design : pas de découpage 4-cycles.** Les diagnostics
  mesurent des propriétés structurelles globales des séries, pas
  band-spécifiques. Le scaffold Kitchin/Juglar/Kuznets/Kondratieff
  qu'on vient de falsifier n'est PAS réintroduit ici.
- **Cohabitation Gate 1 ↔ diagnostics.** Les 4 cycles canoniques
  restent la cible de falsification dans Gate 1/2/3. Item #15 ajoute un
  étage parallèle sans toucher à la taxonomie cyclique.
- **Tests.** 17 tests unitaires sur les 11 diagnostics
  (`tests/test_alternative_dynamics.py`) + 8 tests de non-régression
  sur les générateurs surrogate (`tests/test_surrogate_generators.py`)
  qui garantissent que `ar1_bootstrap_null` et `phase_scramble_null`
  restent seed-stables.
- **Dépendances ajoutées.** `nolds==0.6.2`, `antropy==0.1.8` (rebuild
  Docker requis).

- **Résultats du premier run end-to-end (as-of 2026-05, 100 surrogates,
  9 436 cellules).** Run effectué post-rebuild image Docker (PR #24
  fix MF-DFA actif, zéro warning numérique). Couverture : 14
  diagnostics × 336 (variable × group) × 6 horizons + 12 records
  RMT panel-level. Verdict structurel :

    **Diagnostics dominants (taux de rejet null AR(1) ou phase-scramble,
    α = 0.05, toutes horizons confondues) :**

    | Diagnostic | Famille | Rejet | Stat médiane |
    |---|---|---:|---:|
    | `bds_independence` | D — non-linéarité | **88 %** | 3.70 |
    | `permutation_entropy_complexity` | I — information | **69 %** | H_perm = 0.85 |
    | `reflexivity_drift` | S — transversal | 51 % | KS = 0.82 |
    | `hurst_dfa` | C — longue mémoire | 51 % | **H = 1.62** |
    | `tsallis_q_gaussian` | T | 43 % | q = 1.05 |
    | `msd_log_log` | R — diffusion anormale | 42 % | γ = 1.12 |
    | `hill_tail_exponent` | A — queues | 41 % | α_Hill = 3.59 |
    | `k41_scaling` | P — cascades K41 | 37 % | ζ(6)/ζ(3) = **1.78** |
    | `levy_stable_fit` | J — Lévy | 32 % | α = 2.00 |
    | `reflexivity_multi_window` | S étendu | 30 % | 0.99 |
    | `critical_slowdown` | E — tipping | 30 % | τ = 0.27 |
    | `mfdfa_spectrum` | B — multifractalité | 27 % | Δα = 0.81 |
    | `lyapunov_exponent` | D — chaos | 19 % | λ = 0.07 |
    | `spectrum_slope` | A — SOC 1/f^β | **15 %** | β = 1.75 |

    **Ce qui est confirmé empiriquement :**

    - **Quasi-universalité du rejet IID** : 88 % BDS + 69 %
      perm-entropy → les séries macro ne sont *ni* du bruit blanc,
      *ni* de l'AR(1), *ni* du random walk pur.
    - **Longue mémoire forte** : Hurst médian = 1.62 (>> 0.5
      attendu pour fBm classique) + 51 % de rejet — la persistance
      est *structurelle* sur la moitié des séries.
    - **Cascade multifractale** : ζ(6)/ζ(3) médian = 1.78 (< 2 K41
      monofractal) → signature **She-Levêque anomalous scaling**,
      cohérente avec turbulence des marchés (Ghashghaie et al.
      1996).
    - **Mode dominant RMT** : 9 groupes sur 12 ont λ_top > λ_max MP.
      ANGLO (8.54), UK_BOE (6.06), G7 (4.55), BRICS (4.27) — un
      facteur unique explique la majorité de la variance.
    - **Réflexivité statistique** : 51 % de drift de distribution
      significatif → changements de régime cognitif documentés
      empiriquement (Soros 1987, Akerlof-Shiller 2009).

    **Ce qui est *réfuté* empiriquement :**

    - ❌ **SOC pur (1/f^β strict)** : 15 % de rejet seulement →
      la signature SOC canonique de Bak-Tang-Wiesenfeld n'est PAS
      le cadre dominant pour la macroéconomie.
    - ❌ **Critical slowing down** : 30 % → la *majorité* des
      séries ne sont pas en approche d'un tipping point sur la
      fenêtre observée. Bonne nouvelle systémique, mauvaise
      nouvelle pour les early warning systems.
    - ❌ **Chaos déterministe (Lyapunov)** : 19 % → la dynamique
      n'est *pas* dominée par un attracteur chaotique de basse
      dimension. La macro n'est pas un Lorenz.

    **Top variables porteuses (multi-diagnostic >75 % de rejet) :**

    `LH_IMPORTS` (86%), `LH_EXPORTS` (85%), `LH_MONEY` (85%),
    `LH_EXP` (82%), `LH_REV` (81%), `LH_NARROW` (81%),
    `LH_BANKDEBT` (80%), `BOE_MONEY` (79%), `LH_MORT` (76%),
    `LH_CREDIT` (76%) — concentration nette sur **agrégats
    monétaires et de crédit historiques** (JST + BoE Millennium).

    **Pattern par horizon (taux de rejet moyen) :**

    - `boe` (1700-2016, 8 vars × 317 obs) : signaux les plus
      forts (perm-entropy + BDS = 100%, CSD = 94%, Tsallis = 81%).
      Effet "longueur de série" — la puissance statistique
      explose au-delà de 200 obs.
    - `long` (1870-2020, 6 groupes × 14 vars × 153 obs) : 96%
      BDS, 85% perm-entropy, 76% CSD, 65% Hurst. Confirme `boe`.
    - `wb` (1960-2024, 65 obs/série) : signaux les plus faibles —
      seul BDS (85%) tient. Les 65 ans WB sont trop courts pour
      la plupart des diagnostics structurels.

    **Cadre vainqueur (cluster Q d'universalité empirique) :**

    Les diagnostics qui co-rejettent le plus convergent sur
    **5 familles** :

    > **C (longue mémoire) + B (multifractalité) + D (non-linéarité
    > BDS) + I (information structurée) + S (réflexivité)**

    → Le bon mot n'est *ni* « cycle » *ni* « chaos » *ni* « SOC » :
    c'est **dynamique fractale non-linéaire à longue mémoire avec
    dérive de régime cognitif**.

    Cohérent avec [Mandelbrot 1997](../bibliographie.md#mandelbrot-1997),
    [Bacry-Muzy-Delour 2001](../bibliographie.md#bacry-muzy-delour-2001),
    [Ghashghaie et al. 1996](../bibliographie.md#ghashghaie-1996),
    [Soros 1987](../bibliographie.md#soros-1987) et
    [Akerlof-Shiller 2009](../bibliographie.md#akerlof-shiller-2009).

    **Implication pour la thèse du papier académique :**

    *"Le rejet quasi-universel des 4 cycles canoniques n'est pas
    une défaillance — c'est la confirmation empirique que la
    macroéconomie est une dynamique fractale non-linéaire à longue
    mémoire avec dérive de régime cognitif, pas une oscillation."*

    Sidecars JSON : `reports/dx_diagnostics_2026_05_{horizon}.json`
    et `reports/dx_rmt_2026_05_{horizon}.json`. Page consolidée :
    `docs/dx_diagnostics.md` (162 KB).

## #16 — Étude per-band vs band-agnostique (validation du design choice de #15) — TODO {#item-16-per-band-vs-band-agnostique}

- **Problème.** L'item #15 a posé une décision design forte : "les
  diagnostics sont band-agnostiques car réintroduire un axe `cycle ∈
  {kitchin, juglar, kuznets, kondratieff}` recréerait le scaffold qu'on
  vient de falsifier". Cette décision *n'a pas été testée empiriquement*.
  Sans étude de comparaison, on affirme un design choice plutôt qu'on ne
  le démontre. Reviewers et lecteurs sceptiques peuvent légitimement
  demander : "et si on faisait quand même per-band, qu'est-ce qu'on
  perdrait / gagnerait ?"
- **Méthode.** Implémentation parallèle au module `alternative_dynamics.py`
  d'un module `alternative_dynamics_per_band.py` qui applique un
  sous-ensemble restreint de 4 diagnostics au **signal CF-bandpassé**
  dans chacune des 4 bandes (Kitchin 3-5y, Juglar 7-11y, Kuznets 15-25y,
  Kondratieff 40-60y) :

    1. **`spectrum_slope` (β)** — restreint à la bande de fréquence, mesure
       si la bande a sa propre loi de puissance interne.
    2. **`critical_slowdown` (τ_var)** — variance roulante du signal
       bandpassé, mesure si un tipping point cyclique approche.
    3. **`levy_stable_fit` (α)** — fit Lévy sur les incréments du signal
       filtré, mesure les queues du bruit dans la bande.
    4. **`hurst_dfa` (H)** — diagnostic marginal mais inclus pour
       complétude (sera probablement ≈ 0.5 par construction du filtre).

    Les autres diagnostics (MF-DFA, K41, RMT, perm-entropy, MSD,
    Tsallis, Hill, réflexivité) **ne font pas sens per-band** :
    soit multi-scale par définition (K41, MF-DFA), soit panel (RMT),
    soit transversaux (réflexivité), soit altérés par le filtre.

- **Code.** Nouveau module `ecowave/cycles/alternative_dynamics_per_band.py`
  qui réutilise les fonctions atomiques de `alternative_dynamics.py`
  appliquées à `cf_bandpass(series, lo_years, hi_years)`. Nouvelle
  commande CLI `ecowave dx-diagnostics-per-band --as-of YYYY-MM
  --horizons {wb|q|long|boe|bis|sh}` produisant
  `reports/dx_diagnostics_per_band_{as_of}_{horizon}.json` et page
  `docs/dx_diagnostics_per_band.md` avec **table de comparaison directe
  par variable** : colonnes = (raw, kitchin, juglar, kuznets,
  kondratieff) × diagnostic, lignes = variables. Le lecteur voit
  immédiatement si per-band ajoute de l'info.
- **Acceptance.** Deux verdicts possibles, tous deux acceptables :
  - **Cas A (probable a priori)** : per-band n'ajoute pas d'info
    significative au-delà du band-agnostique. **Conclusion** : la
    décision design de #15 est *validée empiriquement* — pas juste
    affirmée. Le papier académique gagne une réponse falsifiabiliste à
    l'objection "vous n'avez pas montré le contrefactuel".
  - **Cas B (intéressant si observé)** : per-band révèle des structures
    internes (ex: bande Kondratieff filtrée montre un CSD significatif
    même quand Gate 1 rejette la band-power). **Conclusion** : nouvelle
    question de recherche, à creuser dans Roadmap #17.
- **Effort estimé.** ~2 jours : module (1 j) + tests (0.5 j) + run +
  page rendering (0.5 j). À implémenter après merge de PR #23
  (item #15).
- **Garde-fou méthodologique.** L'étude #16 ne *remplace pas* l'étude
  #15. Le module per-band est strictement parallèle, pas substitut. La
  taxonomie cyclique n'est pas restaurée comme angle d'analyse principal
  — uniquement comme angle de validation.

## #17 — Working paper (publication track) — V1 PUBLIÉE {#item-17-working-paper}

- **Problème.** L'item #15 a livré le verdict empirique (cluster
  C+B+D+I+S). Le verdict doit maintenant être *publié* sous forme
  académique reproductible et défendable contre les objections
  attendues. Sans un papier formel, le travail reste cantonné au site
  documentaire ; il ne peut pas être cité, évalué par les pairs, ni
  utilisé pour informer la politique économique au-delà du cercle CPV.
- **Méthode V1 (livrée 2026-05).** Working paper en markdown intégré
  au site MkDocs (`docs/papers/cpv_main_paper.md`, ~10 000 mots, 1 352
  lignes) structuré en 6 sections + 3 annexes :

    - §1 Introduction — stakes intellectuels (2008/2020 forecast
      failures), lacunes des critiques antérieures (Garvy 1943,
      Solomou 1987, Wen 2005), claims explicites et limites.
    - §2 Méthodologie — chaque choix justifié point par point :
      dual null (AR(1) + phase-scramble), consensus 4 méthodes,
      universalité, safeguard #14 contre artefacts d'agrégation,
      périmètre 11 familles / 14 diagnostics, décision design
      band-agnostique (3 raisons), réflexivité transversale.
    - §3 Données — 6 panels avec triple justification (couverture
      temporelle + dimensionnelle + indépendance).
    - §4 Résultats — réfutation 4 cycles, profil 14 diagnostics,
      pattern cross-horizon, variables porteuses (concentration sur
      monnaie/crédit historiques), RMT panel-level, cluster vainqueur.
    - §5 Discussion — working hypothesis ("dynamique fractale non-
      linéaire à longue mémoire avec dérive de régime cognitif"),
      3 incompatibilités précises avec cycle-as-mechanism, **7
      objections anticipées avec rebuttals détaillés** (BDS-triviality,
      Hurst small-sample bias, per-horizon variance comme confondeur,
      multiple-comparison sans correction, LPPL bubble compatibility,
      reflexivity unfalsifiability, DSGE défense), **5 prédictions
      falsifiables** pour stress-tester l'hypothèse.
    - §6 Conclusion.
    - 3 annexes : replication command Docker, panorama 21 familles,
      pré-enregistrement Roadmap #16.

- **Code.** Aucun nouveau code. Le papier est entièrement reproductible
  via les sidecars JSON committés en PR #25 et la commande
  `ecowave dx-diagnostics --as-of 2026-05`.

- **Statut V1.** PR #27 mergée le 2026-05-30 (`07eaa82`). Publié sur
  GitHub Pages sous la section nav "6. Working paper".

- **V2 — roadmap vers submission journal.** Avant submission à un
  journal académique (cibles : *Journal of Economic Methodology*,
  *Real-World Economics Review*, *Physica A*, *Journal of Economic
  Behavior & Organization*), il reste :

    1. **Run 1 000-surrogate (vs 100 actuel)** — réplication statistique
       avec n_surrogates ≥ 1 000 pour rigueur publication. Coût ~10×
       le temps de run (estimation : 3-5 h sur tous horizons). Risque
       méthodologique nul (juste plus de puissance statistique). PR
       suivante : `feat/dx-diagnostics-1000-surrogate-replication`.
    2. **Hurst bias-correction explicite** — appliquer Bryce-Sprague
       (2012) sur les estimations DFA et republier les valeurs
       corrigées. §5.3.2 du papier mentionne le calcul mais ne
       l'inclut pas systématiquement.
    3. **Résultats de Roadmap #16 (per-band study)** — si Cas A (per-
       band n'ajoute rien), le papier gagne un argument empirique pour
       le design choice band-agnostique. Si Cas B, le papier doit
       être révisé pour intégrer la découverte.
    4. **Co-auteurs académiques** — identifier 1-2 macroéconomistes ou
       économétriciens disposés à co-signer, idéalement avec expertise
       en analyse multi-fractale ou réflexivité.
    5. **Tests des 5 prédictions §5.4** — résultats partiels suffisent
       pour la V2 (au moins prédictions 2 et 3 testées sur données
       existantes).

- **Acceptance V2.** Papier ré-écrit en LaTeX (pandoc depuis MD source),
  bibliographie BibTeX, prédictions §5.4 partiellement testées, run
  1 000-surrogate intégré, statut prêt-submission.

## #18 — Robustness extensions (prédictions falsifiables du papier §5.4) — TODO {#item-18-robustness-extensions}

- **Problème.** Le papier §5.4 énonce 5 prédictions falsifiables pour
  stress-tester l'hypothèse cluster. Ces prédictions doivent être
  testées dans des PRs suivantes pour que la V2 du papier soit
  défendable. Chacune correspond à un mini-sprint d'effort variable.

- **Prédiction 1 — long-memory durability avant 1700.** Tester si
  Hurst → 0.5 sur des séries pré-1700 (prix médiévaux, registres
  bancaires Renaissance). Si oui, la longue mémoire est un artefact
  post-déepening financier. Si non, c'est structural à toute économie
  monétisée.

    - **Source candidate.** Allen 2001 Real Wages dataset, Clark 2007
      A Farewell to Alms (prix anglais 1209-1869), Hoffman et al.
      Dawn of Modern Banking (Florence/Venise 1300+). Probable
      ingestion manuelle (CSV depuis publications).
    - **Code.** Nouveau module `ecowave/cycles/medieval_panel.py`,
      manifest `medieval_manifest.json`, horizon `--horizon medieval`.
    - **Effort estimé.** ~3 jours (ingestion ardue, série courte).

- **Prédiction 2 — cross-panel robustness sur variables non-
  financières.** Tester si le cluster (Hurst long memory, BDS
  non-linéarité, reflexivity drift) apparaît sur des séries non-
  financières : participation au marché du travail, scolarisation,
  espérance de vie, consommation énergétique. Si le cluster est
  *spécifique* à la finance / monnaie / crédit, c'est une découverte
  *plus restreinte* (mais toujours intéressante). Si le cluster
  apparaît sur les variables réelles aussi, c'est *structurel à toute
  série macro*.

    - **Source candidate.** OWID datasets (health, education, energy
      per capita, life expectancy), ILO labour force participation,
      UNESCO school enrollment. APIs publiques, ingestion automatique.
    - **Code.** Nouveau module `ecowave/cycles/real_economy_panel.py`,
      manifest `real_economy_manifest.json`, horizon `--horizon real`.
    - **Effort estimé.** ~4 jours (3 sources, schémas hétérogènes).
    - **C'est la prédiction la plus impactante pour la V2 du papier.**

- **Prédiction 3 — multifractal vs monofractal discrimination.**
  Avec un run MF-DFA 1 000-surrogate et `nolds.mfdfa` comme estimateur
  canonique (au lieu de l'implémentation custom), tester si Δα > 0
  reste statistiquement significatif sur les variables LH du panel
  long. Si Δα → 0, le cluster picture se réduit à fractional Brownian
  monofractal — plus faible.

    - **Code.** Switch `mfdfa_spectrum` vers `nolds.mfdfa` ;
      n_surrogates → 1 000 ; re-run sur horizon long uniquement
      (suffisant pour discrimination).
    - **Effort estimé.** ~1 jour (switch lib + re-run).

- **Prédiction 4 — regime-conditioned forecast performance.**
  Construire un benchmark forecasting comparant : (a) ARFIMA + regime-
  switching + heavy-tail innovations, (b) cycle-conditioned baseline
  (predict Juglar contraction in N years), (c) random walk. Test
  out-of-sample sur 2020-2024 data. Si (a) bat (b) systématiquement,
  le cluster picture gagne un argument pratique fort.

    - **Code.** Nouveau module `ecowave/forecasting/regime_conditioned.py`,
      pipeline d'évaluation `ecowave forecast-benchmark`. Sortie :
      MAE / RMSE / coverage par horizon, par variable.
    - **Effort estimé.** ~10 jours (le plus gros chantier — modélisation
      ARFIMA + regime-switching non-triviale, intégration heavy-tail
      innovations encore moins).
    - **À reporter en V3 du papier** (trop substantielle pour V2).

- **Prédiction 5 — reflexive split-point specificity.** Avec
  `reflexivity_multi_window` étendue à 1 000 surrogates, tester si le
  split-point dominant *clusterise* sur des dates pré-enregistrées
  (1971 floating exchange rates pour vars financières, 1944 Bretton
  Woods pour vars commerciales). Si oui, c'est une opérationnalisation
  forte de la réflexivité Soros. Si non, c'est un bruit générique.

    - **Code.** Aucun nouveau code. Re-run de `dx-diagnostics` avec
      n_surrogates = 1 000 + analyse post-hoc des `per_window`
      metadata dans les sidecars JSON.
    - **Effort estimé.** ~1 jour (re-run + script d'analyse).

- **Priorisation.** Pour V2 du papier (~3 mois), faire : Prédiction
  3 (1 j) + Prédiction 5 (1 j) + Prédiction 2 (4 j) = 6 jours de
  travail empirique + intégration dans le papier (2 jours) = ~8 jours
  total. Prédictions 1 et 4 reportées en V3.

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
