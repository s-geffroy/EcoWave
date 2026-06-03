# Kuznets (15–25 ans)

!!! success "Verdict V3 (juin 2026) — Kuznets empiriquement vivant"

    Source : `papers/cycles_refuted/sections/{01_introduction,05_results}.tex`.

    Sur le panel **JST R6 1870–2020** (529 cellules testables, *B* = 1 000 surrogates), **51 cellules passent Gate 1 unadjusted**, soit **1.9× l'excès sur null**. Concentration sur les canaux substantifs prédits par [Kuznets (1930)](../bibliographie.md#kuznets-1930) :

    - `LH_HPI` (prix immobiliers) : **46 % des pays testables** (6 / 13).
    - `LH_POP` (population) : **39 %** (7 / 18).
    - `LH_CREDIT` (crédit bancaire total) : **41 %** (7 / 17).
    - `LH_MORT` (crédit hypothécaire) : 5 ; `LH_DEBTGDP` et `LH_CA` : 4 chacune.

    Sur **BoE Millennium**, UK debt / GDP passe Gate 1 sur la bande Kuznets (*p*<sub>1</sub> = 0.006) ; les real-effective et nominal-effective exchange rates passent les **deux nulls**.

    Le **Quarterly** ne peut pas tester Kuznets (15-25y requiert *N* > 400 trimestres ; max 2 307 sur G7Q, en-deçà du seuil de [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998) pour le plus long agrégat et bien en-dessous pour les pays individuels).

    **Lecture V3** : la vindication substantive de Kuznets sur **housing + démographie + crédit hypothécaire** — exactement les canaux qu'il a identifiés comme porteurs des long swings — est tenue. La lecture universaliste Kuznets-sur-tout reste rejetée BH-FDR.

> **Résumé historique.** La vague infrastructure / démographie.
> [Kuznets (1930)](../bibliographie.md#kuznets-1930) l'identifie sur les
> données de construction et d'immigration américaines ; réinterprétée
> ensuite à travers le cadre Lewis du dualisme économique comme cycle de
> transformation structurelle, et plus récemment comme la bande du **cycle
> financier** ([Borio & Drehmann, 2009](../bibliographie.md#borio-drehmann-2009)).

## Diagramme de phase polaire — panel Banque mondiale 2026

Le panel WB 1960-2024 ne couvre qu'environ 2.5–4 cycles Kuznets, ce qui
rend la Porte 1 difficile à passer. Sur le run mai 2026 avec
$B = 1\,000$ surrogates et null dual, **aucun agrégat ne survit à la
Porte 1** sur la bande Kuznets, d'où l'absence de diagramme polaire pour
cette bande sur le panel WB. C'est une **conséquence honnête** du faible
nombre de cycles disponibles, pas un échec à dissimuler.

## Ce que mesure CPV

Le pipeline applique les quatre méthodes votantes (D, E, F, G) sur la
bande Kuznets $[15, 25]$ années. C'est la bande des longs cycles de
construction, des transitions démographiques et — dans la lecture
moderne — du cycle financier ([Borio & Drehmann, 2009](../bibliographie.md#borio-drehmann-2009)).

Le modèle H (cycle financier Borio) est ajouté conditionnellement au pool
votant quand suffisamment de données crédit + immobilier sont disponibles
(panel d'histoire longue JST principalement).

## Indicateurs moteurs

- `NE.TRD.GNFS.ZS` (commerce extérieur, % PIB) — long cycle
  d'intégration commerciale.
- `SP.URB.TOTL.IN.ZS` (population urbaine, % total) — proxy de
  transformation structurelle Lewis-Kuznets.
- (Histoire longue) `LH_CREDIT` + `LH_HPI` — composante financière du
  cycle Kuznets.

## Caveats

- **Small-N (WB)** : 2.5–4 cycles seulement → Porte 1 fréquemment
  rejetée.
- **Endpoint CF sévère** : les 12–13 dernières années sont
  potentiellement instables. `endpoint_caveat = 1` systématique pour les
  cellules survivant à la Porte 1.
- **Recouvrement avec le cycle financier** : la bande Kuznets recouvre
  partiellement la bande du cycle financier Borio-Drehmann (~15–20 ans) ;
  les deux peuvent être en désaccord sur la phase. Le protocole publie
  les votes individuels dans `cycle_consensus`.

## Références

- [Kuznets (1930)](../bibliographie.md#kuznets-1930)
- Lewis, W. A. (1954). Economic development with unlimited supplies of
  labour. *The Manchester School*, 22(2), 139–191.
- [Borio & Drehmann (2009)](../bibliographie.md#borio-drehmann-2009)
- [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010)
- [Reinhart & Rogoff (2009)](../bibliographie.md#reinhart-rogoff-2009)

## Voir aussi

- [Protocole CPV](../methodology/protocole_cpv.md)
- [Résultats panel Banque mondiale 2026-05](../reports/panel_banque_mondiale_2026.md)
- [Résultats panel d'histoire longue 2026-05](../reports/histoire_longue_2026.md)
