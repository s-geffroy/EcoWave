# R4 — Band-edge sensitivity

> **Résumé.** V3 (recommandation R4 du referee TSE) ajoute un test de
> robustesse band-edge : on perturbe les bornes des bandes canoniques
> de ±1 an (Kitchin / Juglar) ou ±2 ans (Kuznets / Kondratieff), on
> relance Gate 1, on compare les pass-rates. **Un cycle substantif
> survit ; un artefact de bande s'effondre asymétriquement.** Cas V3
> majeur : **BoE Kitchin déclassé** (pass-rate 7.7 % sur `[3,5]` →
> **0.0 % sous `[4,5]`**, 16.9 % sous `[3,6]`).

## Pourquoi ce test

Les bornes des bandes canoniques sont fixées dans
`ecowave/cycles/bands.py:CYCLE_BANDS` (Kitchin 3-5 ; Juglar 7-11 ;
Kuznets 15-25 ; Kondratieff 40-60). Elles sont ancrées dans la
littérature primaire ([Kitchin 1923](../bibliographie.md#kitchin-1923) ;
[Juglar 1862](../bibliographie.md#juglar-1862) ; [Kuznets 1930](../bibliographie.md#kuznets-1930) ;
[Kondratieff 1925](../bibliographie.md#kondratieff-1925)).

Le risque : un signal de bande qui dépend **fortement de l'orientation
exacte** des bornes est suspect. Un vrai cycle de période ≈ 4 ans
survit aux bornes `[3,5]`, `[4,5]`, `[3,6]`, `[4,6]` — sa puissance
de bande pivote peu sous perturbation d'1 an. Un **artefact de bande**
(p.ex. effet de filtre, biais d'agrégat composite) s'effondre
asymétriquement parce que la bande perturbée écarte la fréquence
artefactuelle.

Référence méthodologique parallèle dans la littérature ondelettes :
[Aguiar-Conraria & Soares (2014)](../bibliographie.md#aguiar-conraria-soares-2014) sur la sensibilité des
verdicts cycliques aux choix de bandes.

## Protocole V3

Pour chaque cellule passant Gate 1, on calcule six perturbations par
cycle :

| Cycle | Bande de base | Perturbations |
|---|---|---|
| Kitchin (±1y) | `[3, 5]` | `[2, 5]` `[4, 5]` `[3, 4]` `[3, 6]` `[2, 4]` `[4, 6]` |
| Juglar (±1y) | `[7, 11]` | `[6, 11]` `[8, 11]` `[7, 10]` `[7, 12]` `[6, 10]` `[8, 12]` |
| Kuznets (±2y) | `[15, 25]` | `[13, 25]` `[17, 25]` `[15, 23]` `[15, 27]` `[13, 23]` `[17, 27]` |
| Kondratieff (±2y) | `[40, 60]` | `[38, 60]` `[42, 60]` `[40, 58]` `[40, 62]` `[38, 58]` `[42, 62]` |

Pour chaque perturbation, Gate 1 est relancé avec le même null dual
AR(1) + ARFIMA. La cellule est **band-stable** si elle survit aux six
perturbations ; **band-edge artefact** si elle ne survit que dans une
direction de perturbation et s'effondre asymétriquement dans l'autre.

## Résultats empiriques V3

Source : `papers/cycles_refuted/sections/05_results.tex`
§sec:appendix_band_sensitivity et
`reports/band_sensitivity.json`.

### Kuznets, Kondratieff, Juglar — stables à ±2y

Les pass-rates Kuznets / Kondratieff / Juglar sur les panels JST et
BIS varient dans une **fourchette de ~6 points** autour de l'ancre.
Les vindications V3 sur ces cycles sont **robustes** au test R4.

### Kitchin — **très instable** sur BoE

Sur **BoE Millennium**, le pass-rate Kitchin de base est 7.7 % (5 / 65
cellules sur `[3,5]`). Les perturbations :

| Bande | Pass-rate Kitchin | Interprétation |
|---|---|---|
| `[3, 5]` (base) | 7.7 % | léger excès sur 5 % nominal |
| `[4, 5]` (resserrage low) | **0.0 %** | effondrement asymétrique |
| `[2, 5]` (élargissement low) | 9.2 % | quasi-stable |
| `[3, 6]` (élargissement high) | **16.9 %** | doublement |
| `[3, 4]` (resserrage high) | 4.6 % | léger effondrement |

L'asymétrie est **massive** : resserrer la borne basse efface
l'ensemble du signal ; élargir la borne haute le double. Ce pattern
est la signature d'un **artefact de filtre** plutôt que d'un cycle
substantif. La cellule BoE Kitchin est **déclassée** et exclue du
support à la vindication Kitchin V3.

### Kitchin sur BIS — stable

Sur le panel **BIS quarterly** (5.3× excès sur 93 cellules), les
perturbations Kitchin laissent le pass-rate dans une fourchette de
~5 points autour de la valeur de base. La vindication Kitchin V3 sur
les agrégats crédit BIS marchés émergents est robuste R4.

## Implémentation

Script : `scripts/band_sensitivity.py`.

```bash
docker compose run --rm ecowave \
  scripts/band_sensitivity.py --panels boe,bis,jst \
  --n-surrogates 300 --seed 0
```

Sortie : `reports/band_sensitivity.json` avec schéma
`{panel, group, variable, cycle, band_base, perturbation, p1_AR1, p1_ARFIMA, pass: bool}`.

Cible Makefile : `referee-r4`. Run V3 documenté : 1 541 cellules sur
BoE, 27 agrégats, 300 surrogates par perturbation.

## Voir aussi

- [Gate 1 dual null AR(1) + ARFIMA](arfima_dual_null.md)
- [Rolling-window R5](rolling_window_gates.md)
- [Cycle Kitchin — verdict V3](../cycles/kitchin.md)
- [Verdict V3 portail](../papers/cycles_refuted_v3.md)

## Références

- [Aguiar-Conraria & Soares (2014)](../bibliographie.md#aguiar-conraria-soares-2014)
- [Christiano & Fitzgerald (2003)](../bibliographie.md#christiano-fitzgerald-2003)
- [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998)
