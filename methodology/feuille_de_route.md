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
- **Dépendances ajoutées.** `nolds==0.6.2`, `antropy==0.1.7` (rebuild
  Docker requis).

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
