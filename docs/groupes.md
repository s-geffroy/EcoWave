# Glossaire des agrégats

> **Résumé.** Le pipeline CPV publie des phases par **agrégat de pays**.
> Certains sont des agrégats officiels de la Banque mondiale (une série par
> indicateur, servie directement par l'API) ; d'autres sont des composites
> recalculés à partir d'une liste de pays, pondérés par leur PIB courant en
> USD (`NY.GDP.MKTP.CD`). Cette page donne le code, la composition et la
> source de chaque agrégat utilisé sur le site.

## Classifications par revenu (Banque mondiale 2024-2025)

Les quatre classes de revenu utilisent les seuils de RNB par habitant
définis par la Banque mondiale pour l'exercice 2024-2025 (méthode Atlas,
USD courants). Les seuils sont appliqués chaque année ; un pays peut donc
changer de classe entre deux exécutions CPV.

| Code | Nom | Seuil RNB/hab (Atlas, USD courants) |
|---|---|---|
| `WLD` | Monde | s.o. (agrégat global) |
| `HIC` | High-Income Countries | > 14 005 |
| `UMC` | Upper-Middle-Income Countries | 4 516 – 14 005 |
| `LMC` | Lower-Middle-Income Countries | 1 146 – 4 515 |
| `LIC` | Low-Income Countries | ≤ 1 145 |

Ces cinq agrégats par stratification de revenu sont ceux utilisés par la
**Porte 3** (universalité). Un cycle n'est qualifié `universal` que lorsque
≥ 4 des 5 agrégats partagent la même phase modale. Voir
[Trois portes](methodology/trois_portes.md).

## Autres agrégats

| Code | Nom | Composition |
|---|---|---|
| `OECD` (alias `OED`) | Membres de l'OCDE | 38 pays ; agrégat officiel WB |
| `G7` | G7 | USA, GBR, FRA, DEU, ITA, JPN, CAN — recompute pondéré PIB |
| `G20` | Échantillon G20 | 19 pays (l'UE est représentée par DEU+FRA+ITA pour éviter le double-comptage) |
| `BRICS` | BRICS+ | BRA, RUS, IND, CHN, ZAF + EGY, ARE, ETH, IRN, IDN (composition post-2025, 10 pays) — recompute pondéré PIB |

OECD et les classes de revenu utilisent l'agrégat officiel WB (une série
par indicateur) ; G7, G20 et BRICS+ sont recalculés par le pipeline en
pondérant chaque pays par son PIB courant en USD.

## Agrégats du panel d'histoire longue

Le panel Maddison + Jordà-Schularick-Taylor (1870-2020) couvre 18 économies
avancées. Les agrégats suivants y sont définis :

| Code | Nom | Composition |
|---|---|---|
| `ADV18` | Économies avancées JST | AUS, BEL, CAN, CHE, DEU, DNK, ESP, FIN, FRA, GBR, IRL, ITA, JPN, NLD, NOR, PRT, SWE, USA |
| `G7` | G7 (long-history) | USA, GBR, FRA, DEU, ITA, JPN, CAN |
| `USA` | États-Unis seuls | USA |
| `EU4` | Quatre grandes économies européennes | DEU, FRA, ITA, GBR |
| `ANGLO` | Économies anglophones | USA, GBR, CAN, AUS |
| `NORDIC` | Pays nordiques | DNK, FIN, NOR, SWE |

Ces agrégats sont **figés** dans `ecowave/cycles/bands.py:GROUPS` et
`ecowave/cycles/long_history.py:LONG_GROUPS`. Toute modification de
composition relève d'une revue méthodologique (discipline de
pré-enregistrement, cf. [Garde-fous](methodology/garde_fous.md)).

## Choix éditorial de cette liste

- **WLD + 4 classes de revenu** : stratification canonique utilisée par la
  Porte 3 pour distinguer un cycle global d'un cycle régional.
- **OECD** : benchmark historique des « économies développées » ; utile
  pour comparaison avec HIC dont l'intersection est forte mais non
  identique.
- **G7, BRICS+, G20** : agrégats de politique économique abondamment cités
  dans la littérature ; publiés pour contexte, **ne participent pas** à la
  Porte 3.
- **ADV18, ANGLO, NORDIC, EU4, USA** : panels du run long-histoire, calibrés
  pour examiner la K-wave et les Kuznets sur la profondeur historique
  maximale offerte par JST.

## Références

Voir [Bibliographie](bibliographie.md). En particulier :

- [Maddison Project Database (2023)](bibliographie.md#maddison-2023) — base
  PIB longue.
- [Jordà, Schularick & Taylor (2017)](bibliographie.md#jorda-schularick-taylor-2017) —
  base macrofinancière longue.
- [Kose, Otrok & Whiteman (2003)](bibliographie.md#kose-otrok-whiteman-2003) —
  justification des décompositions par agrégat (facteur global vs régional).
