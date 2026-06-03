# Trois portes de falsifiabilité

> **Résumé.** Une phase n'est publiée pour une cellule (agrégat, cycle,
> mois) que si **les trois portes** réussissent : existence du cycle dans
> les données (Porte 1, **dual null AR(1) + ARFIMA** en V3), consensus
> inter-méthode (Porte 2), concordance cross-agrégats (Porte 3). Les
> échecs sont publiés explicitement (`rejected` / `disputed` /
> `regional`) plutôt que dissimulés — c'est ce qui distingue le
> protocole CPV de la littérature classique sur les vagues longues.
> S'y ajoutent **deux robustesses** V3 : R4 band-edge sensitivity et
> R5 rolling-window Gate 1 50–80y. L'engagement de seuils est libellé
> « **threshold transparency** » (Git tags publics avant ingestion des
> panels), distinct d'une pre-registration formelle OSF.

## Notation

| Symbole | Sens |
|---|---|
| $H_0$ | Hypothèse nulle : la bande ne porte pas de puissance distincte d'un bruit AR(1) + phase scramble |
| $H_1$ | Hypothèse alternative : un cycle de la bande est présent |
| $\alpha$ | Seuil de rejet du null ($\alpha = 0.05$) |
| $p_{\text{dual}}$ | $p$-value combinée du null dual (max des deux $p$-values individuelles) |
| $m$ | Nombre de méthodes votantes ($m = 4$) |
| $k$ | Nombre minimum d'accord pour la Porte 2 ($k = 3$) |
| $n$ | Nombre de groupes de revenu pour la Porte 3 ($n = 5$) |
| $q$ | Nombre minimum d'accord cross-groupes ($q = 4$) |

## Porte 1 — existence du cycle (dual null V3)

**Énoncé du test V3.** $H_0$ : la puissance dans la bande $[\text{lo}, \text{hi}]$
est compatible avec un null conservatif combinant :

- (a) un **AR(1)** ajusté sur la série (moyenne, variance, persistance) —
  primaire ;
- (b) un **ARFIMA(0, $\hat d_{\mathrm{GPH}}$, 0)** où $\hat d$ est estimé
  par GPH sur la série — robustesse long-memory (R1 referee TSE).

**Pourquoi remplacer le phase-scrambling par ARFIMA.** Le phase-scrambling de
[Theiler *et al.* (1992)](../bibliographie.md#theiler-et-al-1992) est
**dégénéré par Parseval** contre la puissance de bande (préservant
exactement le spectre, il préserve aussi la puissance de bande de la
série originale et ne peut donc pas la rejeter). La V3 le rapporte en
diagnostic mais ne le laisse plus gater Gate 1.

**Pourquoi ARFIMA est critique en V3.** Les diagnostics par cellule
([long_memory_diagnostics.md](long_memory_diagnostics.md)) montrent que
**97-100 %** des cellules JST R6 / BoE Millennium ont $|\hat d| > 0.1$,
ce qui rend l'AR(1) seul **mis-spécifié** sur les niveaux bruts à
mémoire longue. La lecture **load-bearing** sur ces cellules est la
lecture **ARFIMA-conditional**.

**Critère de décision V3.** $p_{1,\mathrm{AR(1)}} < \alpha = 0.05$ → la cellule
passe la Porte 1 et procède à la Porte 2. Quand $|\hat d| > 0.1$, le
verdict ARFIMA est également exigé : si $p_{1,\mathrm{AR(1)}} < \alpha$
mais $p_{1,\mathrm{ARFIMA}} \geq \alpha$, la cellule est **déclassée
comme faux positif long-memory**. Sur BoE, 16 cellules sont concernées
par ce déclassement.

**Implémentation.** `ecowave/cycles/surrogate.py:dual_null` (AR(1)) et
`arfima_bootstrap_null` (ARFIMA), `scripts/arfima_null_per_cell.py` pour
le run dédié. Cibles Makefile : `referee-r1`. Sortie :
`reports/arfima_null_per_cell.json`. Voir
[arfima_dual_null.md](arfima_dual_null.md).

**Source.** [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998) ;
[Grinsted *et al.* (2004)](../bibliographie.md#grinsted-moore-jevrejeva-2004) ;
[Granger & Joyeux (1980)](../bibliographie.md#granger-joyeux1980) ;
Hosking (1981) ; [Baillie (1996)](../bibliographie.md#baillie1996).

## Porte 2 — consensus inter-méthode

**Énoncé du test.** Au moins $k = 3$ méthodes parmi $\{D, E, F, G\}$ doivent
voter la **même** étiquette de phase :

- **F** — CF band-pass + phase de Hilbert ([Christiano & Fitzgerald, 2003](../bibliographie.md#christiano-fitzgerald-2003))
- **G** — Datation Bry-Boschan ([Harding & Pagan, 2002](../bibliographie.md#harding-pagan-2002))
- **E** — Markov-switching AR(1) ([Hamilton, 1989](../bibliographie.md#hamilton-1989))
- **D** — Ruptures PELT ([Killick *et al.*, 2012](../bibliographie.md#killick-fearnhead-eckley-2012))

**Critère de décision.** Si l'étiquette modale rassemble $\geq 3$ votes :
phase publiée. Si la modale ne rassemble que 2 votes : `phase = disputed`.
Le **désaccord est publié explicitement** dans `cycle_consensus`, jamais
résolu en choisissant une méthode « amicale ».

**Implémentation.** `ecowave/cycles/consensus.py:compute_phase_consensus`.

**Justification.** Les quatre méthodes incarnent des hypothèses génératives
très hétérogènes (filtre fréquentiel vs deux régimes Markov vs ruptures de
moyenne vs détection de retournements). Un accord à 3/4 implique qu'aucun
artéfact méthodologique unique ne pilote le résultat.

## Porte 3 — universalité cross-groupes

**Énoncé du test.** Pour chaque cycle et chaque mois `as_of`, le cycle est
qualifié `universal` seulement si $\geq q = 4$ agrégats de revenu sur
$n = 5$ (WLD + HIC + UMC + LMC + LIC) partagent la même phase modale.

**Critère de décision.** Si $\geq 4 / 5$ accordent : flag `universal = 1`.
Sinon : `universal = 0` ; le cycle est qualifié `regional / idiosyncratic`
et la liste des groupes concordants est publiée dans `cycle_universality.notes`.

**Implémentation.** `ecowave/cycles/universality.py:compute_cross_group_concordance`.

**Justification.** Transpose le critère C6 de transférabilité (EcoWave
historique) de la dimension temporelle à la dimension de stratification de
revenu. Un cycle global doit s'imposer indépendamment du niveau de
développement ; un cycle qui n'existe que pour HIC est `regional`.

## Robustesses V3 (R4 + R5)

Deux tests de robustesse ont été ajoutés en V3 en réponse aux
recommandations R4 et R5 du referee TSE. Ils ne remplacent pas les
trois portes mais les **conditionnent** : un cycle qui passe Gate 1
mais échoue R4 ou pivote sous R5 est lu comme artefact ou comme
intermittent.

- **R4 — Band-edge sensitivity** ([détail](band_sensitivity.md)).
  Perturbation des bornes canoniques de ±1 an (Kitchin/Juglar) ou
  ±2 ans (Kuznets/Kondratieff), Gate 1 relancé. Un cycle substantif
  survit ; un artefact s'effondre asymétriquement. **Exemple V3** :
  BoE Kitchin pass-rate 7.7 % sur `[3,5]` → 0.0 % sous `[4,5]`,
  16.9 % sous `[3,6]` → cellule **déclassée**. Sortie :
  `reports/band_sensitivity.json`.
- **R5 — Rolling-window Gate 1 50-80y**
  ([détail](rolling_window_gates.md)). Gate 1 appliqué sur fenêtres
  glissantes 50y (200y pour Kondratieff) avec step 25-40y, pour
  cartographier la présence temporelle. Sortie :
  `reports/rolling_window_gates.json`.

## Autres contraintes (toujours « threshold transparency »)

- **Endpoint caveat.** Toute cellule dont le dernier point de données est à
  moins de $\lfloor \text{hi\_years}/2 \rfloor$ du bord du panel est marquée
  `endpoint_caveat = 1`. La phase est tout de même publiée mais le lecteur
  est explicitement averti que le filtre CF est instable à la frontière.
- **Adéquation de fréquence.** Les données WB sont annuelles ; Kitchin
  (3–5 ans) est borderline ; la borne basse (3 ans) est sous le seuil de
  Nyquist annuel. Le protocole fixe Kitchin uniquement sur la
  bande haute 4–5 ans ; l'upsample trimestriel (spline) est une variante
  de sensibilité, jamais le défaut.
- **Small-N Kondratieff.** Les séries WB commencent en 1960 (~65 ans, soit
  $\approx 1.0$–$1.5$ K-wave). La Porte 1 rejette fréquemment Kondratieff
  pour les agrégats à historique court ; c'est publié `separable = 0`, non
  réinterprété comme un signal caché. Seul **BoE Millennium** (1700–2016,
  *N* ≥ 240 obs.) admet un test Kondratieff complet en V3.
- **Pas de cherry-picking de bande.** Les bornes des bandes sont figées
  dans `ecowave/cycles/bands.py:CYCLE_BANDS` et ne sont jamais ajustées
  agrégat par agrégat (threshold transparency).
- **Threshold transparency vs pre-registration formelle.** Les bornes,
  surrogate counts, gate thresholds et regroupements sont **figés dans
  l'historique Git public avant ingestion des panels**. Ce n'est **pas**
  équivalent à une pre-registration formelle OSF / AEA RCT Registry,
  qui requiert un timestamp tiers hors du contrôle du chercheur. La V3
  emploie le terme « threshold transparency » pour ce niveau
  d'engagement et engage une OSF prospective pour la réplication
  out-of-sample post-2024.

## Échelle de verdict

| Verdict | Porte 1 | Porte 2 | Porte 3 | Phase publiée |
|---|---|---|---|---|
| **A** | ✓ | ✓ (4/4 d'accord) | ✓ (universal) | étiquette modale |
| **B** | ✓ | ✓ (3/4 d'accord) | ✓ | étiquette modale + dissident noté |
| **C** | ✓ | ✗ (`disputed`) ou ✓ + Porte 3 ✗ | — | cellule rapportée, verdict qualifié |
| **D** | ✗ | — | — | `rejected` (échec honnête) |

## Caveats

La discipline de **threshold transparency** implique que les bornes,
méthodes et seuils ci-dessus sont gelés en Git public avant ingestion
des panels ; toute modification ouvre la suspicion d'ajustement
*post hoc* aux données. Les modifications passées sont tracées
dans [Feuille de route](feuille_de_route.md) et dans l'historique git.
La V3 engage en outre une **OSF pre-registration prospective** pour
toute réplication out-of-sample post-2024 — soit le seul périmètre
sur lequel la V3 revendique le sens formel de « pre-registration ».

## Références

- [Christiano & Fitzgerald (2003)](../bibliographie.md#christiano-fitzgerald-2003)
- [Grinsted, Moore & Jevrejeva (2004)](../bibliographie.md#grinsted-moore-jevrejeva-2004)
- [Hamilton (1989)](../bibliographie.md#hamilton-1989)
- [Harding & Pagan (2002)](../bibliographie.md#harding-pagan-2002)
- [Killick, Fearnhead & Eckley (2012)](../bibliographie.md#killick-fearnhead-eckley-2012)
- [Theiler *et al.* (1992)](../bibliographie.md#theiler-et-al-1992)
- [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998)
