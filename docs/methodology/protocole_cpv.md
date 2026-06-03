# Protocole CPV — décomposition multi-cycles

> **Résumé.** Le protocole *Cycle Position Vector* (CPV) décompose une série
> macroéconomique en quatre bandes canoniques (Kitchin, Juglar, Kuznets,
> Kondratieff) en combinant filtrage passe-bande, analyse en ondelettes et
> extraction de phase instantanée. Quatre méthodes hétérogènes votent ; le
> verdict final passe par trois portes de falsifiabilité. Ce document
> spécifie chaque étape, son implémentation Python et ses références.

## Notation

| Symbole | Sens | Unité |
|---|---|---|
| $x(t)$ | Série composite z-normalisée par bande | sans dim. |
| $\omega$ | Pulsation centrale de la bande | rad / an |
| $\varphi(t)$ | Phase instantanée de Hilbert | rad $\in (-\pi, \pi]$ |
| $A(t)$ | Amplitude instantanée de Hilbert | sans dim. |
| $P_{\text{band}}$ | Puissance dans la bande CF | sans dim. |
| $p_{\text{dual}}$ | $p$-value combinée (AR(1) + ARFIMA(0, $\hat d_{\mathrm{GPH}}$, 0)) | $\in [0, 1]$ |
| $\alpha$ | Seuil de rejet du null | $0.05$ |

## Bandes de cycle (threshold transparency, figées)

| Cycle | Bande de période (années) | Référence |
|---|---|---|
| Kitchin | 3–5 | [Kitchin (1923)](../bibliographie.md#kitchin-1923) ; [Diebolt & Doliger (2008)](../bibliographie.md#diebolt-doliger-2008) |
| Juglar | 7–11 | [Juglar (1862)](../bibliographie.md#juglar-1862) ; [Schumpeter (1939)](../bibliographie.md#schumpeter-1939) |
| Kuznets | 15–25 | [Kuznets (1930)](../bibliographie.md#kuznets-1930) ; [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010) |
| Kondratieff | 40–60 | [Kondratieff (1925)](../bibliographie.md#kondratieff-1925) ; [Modelski (1987)](../bibliographie.md#modelski-1987) ; [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010) |

Les bornes sont figées dans `ecowave/cycles/bands.py:CYCLE_BANDS`. Toute
modification relève d'une revue méthodologique.

## Étape 1 — filtrage passe-bande (Christiano-Fitzgerald)

Implémentation : `ecowave/cycles/decompose.py:cf_bandpass`, enveloppe de
`statsmodels.tsa.filters.cf_filter.cffilter`.

Choix du filtre CF plutôt que HP ou Baxter-King :

- **CF** est asymétrique, full-sample et gère mieux le bord droit que
  Baxter-King (qui perd $q$ échantillons à chaque extrémité).
- Le filtre Hodrick-Prescott (HP), bien que largement utilisé, est réfuté
  par Hamilton (2018, *"Why You Should Never Use the Hodrick-Prescott
  Filter"*) pour son introduction de cycles spurieux. HP est conservé
  uniquement pour la colonne diagnostique `intensity_hp_cycle` dans la
  table `global_indices`, jamais pour le verdict.

**Caveat d'endpoint :** les $\lfloor \text{hi\_years} / 2 \rfloor$ derniers
échantillons sont marqués `endpoint_caveat = 1` dans `cycle_positions.notes`.

## Étape 2 — décomposition en ondelettes (Morlet continue)

Implémentation : `ecowave/cycles/decompose.py:morlet_wavelet`, via
`pywt.cwt(..., wavelet="cmor...")`.

Paramètres figés à $\omega_0 = 6.0$, $\Delta j = 0.125$
([Torrence & Compo, 1998](../bibliographie.md#torrence-compo-1998) défaut).
Le scaleogramme est restreint à la bande d'intérêt ; la puissance dans la
bande est la moyenne de $|W(s, t)|^2$ sur les échelles internes. Usages :

1. Vérifier que la bande CF porte effectivement de la puissance
   (cross-check avec la Porte 1).
2. Produire une figure publiable par agrégat.

Le cône d'influence (`ecowave/cycles/decompose.py:cone_of_influence`)
renvoie un masque booléen des échantillons fiables.

## Étape 3 — phase instantanée de Hilbert

Implémentation : `ecowave/cycles/phase.py:hilbert_phase`, via
`scipy.signal.hilbert`. La phase instantanée $\varphi(t) \in (-\pi, \pi]$ du
signal passe-bande est mappée à l'une de quatre étiquettes (convention
cosinus, pic à $\varphi = 0$) :

| Quadrant | Étiquette |
|---|---|
| $\varphi \in [-\pi/2, 0)$ | expansion |
| $\varphi \in [0, \pi/2)$ | peak |
| $\varphi \in [\pi/2, \pi] \cup [-\pi, -3\pi/4)$ | contraction |
| $\varphi \in [-3\pi/4, -\pi/2)$ | trough |

Règle figée dans `PHASE_BOUNDS` (dans `phase.py`).

## Étape 4 — null de surrogate (Porte 1, existence) — V3 dual

Implémentation : `ecowave/cycles/surrogate.py`. **Dual null V3** :

- `ar1_bootstrap_null` — ajuste un AR(1) de mêmes moyenne / variance /
  persistance que la série, simule $B = 1\,000$ trajectoires, compare la
  puissance dans la bande après filtrage CF (**primaire**).
- `arfima_bootstrap_null` — simule sous ARFIMA(0, $\hat d_{\mathrm{GPH}}$, 0)
  via récursion Hosking, compare la puissance dans la bande
  (**robustesse long-memory**, R1 referee TSE).
- `phase_scramble_null` — préserve le spectre, randomise les phases
  ([Theiler *et al.*, 1992](../bibliographie.md#theiler-et-al-1992)).
  **Statut V3 : diagnostique uniquement, ne gate plus le verdict** car
  dégénéré par Parseval contre la puissance de bande.

Si $p_{1,\mathrm{AR(1)}} \geq \alpha$, le cycle n'est pas distinguable
du bruit auto-corrélé et la cellule est publiée `phase = rejected`. Si
$p_{1,\mathrm{AR(1)}} < \alpha$ mais $p_{1,\mathrm{ARFIMA}} \geq \alpha$
avec $|\hat d| > 0.1$, la cellule est **déclassée comme faux positif
long-memory**. Voir [arfima_dual_null.md](arfima_dual_null.md) et
[long_memory_diagnostics.md](long_memory_diagnostics.md).

Référence : [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998) ;
[Grinsted *et al.* (2004)](../bibliographie.md#grinsted-moore-jevrejeva-2004) ;
[Granger & Joyeux (1980)](../bibliographie.md#granger-joyeux1980) ;
Hosking (1981) ; [Baillie (1996)](../bibliographie.md#baillie1996).

## Étape 5 — consensus inter-méthode (Porte 2)

Implémentation : `ecowave/cycles/consensus.py:compute_phase_consensus`.

Quatre méthodes votent :

- **F** — CF Juglar band-pass + phase de Hilbert ([Christiano & Fitzgerald, 2003](../bibliographie.md#christiano-fitzgerald-2003))
- **G** — Datation de retournements Bry-Boschan / Harding-Pagan
  ([Harding & Pagan, 2002](../bibliographie.md#harding-pagan-2002))
- **E** — Régimes Markov-switching AR(1) ([Hamilton, 1989](../bibliographie.md#hamilton-1989))
- **D** — Détection de ruptures PELT ([Killick *et al.*, 2012](../bibliographie.md#killick-fearnhead-eckley-2012))

La phase de consensus n'est publiée que si $\geq 3$ méthodes sur 4
s'accordent ; sinon la cellule est `phase = disputed`. Le désaccord est
**publié explicitement** dans la table de votes par méthode
(`cycle_consensus`) et jamais résolu en choisissant une méthode « amicale ».

## Étape 6 — concordance cross-agrégats (Porte 3)

Implémentation : `ecowave/cycles/universality.py:compute_cross_group_concordance`.

Pour chaque cycle et chaque mois `as_of`, Gate 3 compte combien
d'agrégats de revenu (WLD + HIC + UMC + LMC + LIC) partagent la même
phase modale. En V3, Gate 3 **ne traite pas l'asymétrie comme un échec
de gate** : la lecture universaliste sinusoïdale-sur-tout est testée
*séparément* par **BH-FDR sur la grille jointe** des 1 456 cellules
(`p* = 0.05 / 1456 ≈ 3.4·10⁻⁵`), et rejetée parce que le floor
empirique `1/(B+1)` est d'un ordre de grandeur au-dessus de `p*` aux
surrogate counts actuels (`B ≤ 1 000`). Le drapeau
`cycle_universality.universal` reste publié comme diagnostic
cross-agrégat ; le verdict universaliste est lu sur le BH-FDR.

## Étape 7 — robustesses V3 (R4 + R5)

Implémentation : `scripts/band_sensitivity.py` et
`scripts/rolling_window_gates.py`.

- **R4 band-edge sensitivity** : Gate 1 relancé sous perturbation
  ±1y (Kitchin/Juglar) / ±2y (Kuznets/Kondratieff) des bornes
  canoniques. Sortie : `reports/band_sensitivity.json`. Voir
  [band_sensitivity.md](band_sensitivity.md).
- **R5 rolling-window** : Gate 1 sur fenêtres glissantes 50–80y avec
  step 25–40y. Sortie : `reports/rolling_window_gates.json`. Voir
  [rolling_window_gates.md](rolling_window_gates.md).

## Variables ingérées (Banque mondiale)

Huit indicateurs dans `cycles_manifest.json`, tous issus de World Bank Open Data :

| Code | Série WB | Cible cyclique |
|---|---|---|
| CY_GDP | `NY.GDP.MKTP.KD.ZG` | Toutes bandes |
| CY_INV | `NE.GDI.TOTL.ZS` | Juglar (Schumpeter, 1939) |
| CY_INF | `FP.CPI.TOTL.ZG` | Kitchin / Juglar |
| CY_UEM | `SL.UEM.TOTL.ZS` | Juglar |
| CY_TRD | `NE.TRD.GNFS.ZS` | Juglar / Kuznets |
| CY_POP | `SP.URB.TOTL.IN.ZS` | Kuznets (Lewis structural) |
| CY_FIN | `FS.AST.PRVT.GD.ZS` | Juglar / Kondratieff (super-cycle de crédit) |
| CY_PRD | `NY.GDP.PCAP.KD` | Kondratieff (productivité longue) |

L'agrégation par groupe utilise les codes officiels Banque mondiale (WLD,
OED, HIC, UMC, LMC, LIC) lorsqu'ils existent, et un recompute pondéré par
PIB pour G7 / G20 / BRICS+.

## Variables ingérées (panel d'histoire longue)

Six variables `cpv_long_history_2026` (manifest `long_history_manifest.json`) :

- `LH_GDP` — PIB par habitant, Maddison Project Database 2023.
- `LH_CREDIT` — Crédit bancaire au secteur privé, JST R6.
- `LH_HPI` — Indice de prix immobilier réel, JST R6.
- `LH_EQUITY` — Indice d'actions réel, JST R6.
- `LH_YIELD` — Taux d'intérêt long, JST R6.
- `LH_CPI` — Indice des prix à la consommation, JST R6.

Voir [Sources & données](../sources.md).

## Caveats

- **Endpoint CF** : les dernières $\lfloor \text{hi\_years}/2 \rfloor$ années
  sont moins fiables (filtre asymétrique). Cellules marquées
  `endpoint_caveat = 1`.
- **Fréquence annuelle WB** : Kitchin (3–5 ans) est borderline ; la bande
  basse 3 ans est inutilisable annuellement (Nyquist).
- **Small-N Kondratieff** : WB (max *N* = 65) et JST (max *N* = 151) sont
  window-bound et **ne peuvent pas tester Kondratieff** ([Torrence & Compo 1998](../bibliographie.md#torrence-compo-1998) requièrent ≥ 240 obs. annuelles sur 40–60y). Seul **BoE Millennium 1700-2016** admet ce test en V3.
- **AR(1) mis-spécifié sur niveaux long-mémoire** : 97–100 % des
  cellules JST R6 / BoE Millennium ont $|\hat d| > 0.1$ ; la lecture
  load-bearing sur ces cellules est l'ARFIMA-conditional. Voir
  [long_memory_diagnostics.md](long_memory_diagnostics.md).

## Références

- [Aguiar-Conraria & Soares (2014)](../bibliographie.md#aguiar-conraria-soares-2014)
- [Borio & Drehmann (2009)](../bibliographie.md#borio-drehmann-2009)
- [Christiano & Fitzgerald (2003)](../bibliographie.md#christiano-fitzgerald-2003)
- [Diebolt & Doliger (2008)](../bibliographie.md#diebolt-doliger-2008)
- [Grinsted, Moore & Jevrejeva (2004)](../bibliographie.md#grinsted-moore-jevrejeva-2004)
- [Hamilton (1989)](../bibliographie.md#hamilton-1989)
- [Harding & Pagan (2002)](../bibliographie.md#harding-pagan-2002)
- [Killick, Fearnhead & Eckley (2012)](../bibliographie.md#killick-fearnhead-eckley-2012)
- [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010)
- [Theiler *et al.* (1992)](../bibliographie.md#theiler-et-al-1992)
- [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998)

---
*Pipeline : `position-cycles --null dual --n-surrogates 1000`. Schéma DB :
0.5.0. Implémentation : `ecowave/cycles/`.*
