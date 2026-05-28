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

## #10 — Variables manquantes (couverture) — TODO

- L'indicateur de protestations `S` (S2, Mass Mobilization / ACLED
  post-2020) et l'indicateur de tonalité narrative `I` (I2, GDELT tone)
  restent à ingérer — tous deux listés `not_automatable_v1` dans
  `sources_manifest.json`.
- La couverture symétrique US + zone euro sur les courbes S et D est
  partielle ; ECB CISS démarre en 1999, ce qui affaiblit C3 (robustesse
  bi-fenêtre) sur D.

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
