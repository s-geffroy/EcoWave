# Synthèse multi-horizons — CPV 2026-05

> Note signée — agrégation des trois horizons CPV (Banque mondiale,
> trimestriel, histoire longue) pour répondre à la question :
> **"où en sommes-nous dans chaque cycle, et où allons-nous ?"**.
> Chaque cellule provient d'une ligne SQLite `cycle_positions`
> traçable ; aucune agrégation inter-dataset n'est effectuée.

!!! info "Mise à jour V3 (juin 2026) — lecture composite vs variable-spécifique"

    Les tableaux ci-dessous (cellules `rejected` au niveau composite + endpoint caveat) sont la **vue composite** par agrégat. Le verdict V3 de *Cycles Refuted* travaille au niveau **per-variable** : sur 1 456 cellules testables, 166 positifs Gate 1 unadjusted (excès 2.3×) concentrés sur les canaux substantifs prédits par chaque théorie d'origine — Juglar sur investissement-PIB / chômage, Kuznets sur HPI / population / crédit, Kitchin sur crédit BIS marchés émergents. **Kondratieff recasté** chronologie Reinhart-Rogoff (UK dette uniquement). **Lecture universaliste sinusoïdale-sur-tout rejetée** par BH-FDR sur grille jointe. Cf. [verdict V3 portail](../papers/cycles_refuted_v3.md) et la colonne **V3 status** ajoutée ci-dessous.

## Position canonique par cycle (V3)

| Cycle | Verdict V3 | Pass / testable | Canaux porteurs | Lecture |
|---|---|---|---|---|
| Kitchin (3-5 ans) | ✅ Vindiqué | 25 / 93 BIS Q (+ 5 / 50 WB, + 3 / 26 sectoral) | crédit BIS EM (KR/CN/MX/ZA/TR/RU/ID) | BoE Kitchin déclassé band-edge R4 |
| Juglar (7-11 ans) | ✅ Vindiqué | 67 / 605 JST (+ 12 / 55 Q) | LH_INV 39 %, LH_UNRATE 33 %, LH_BUSCREDIT 33 % | UK chômage BoE passe les 2 nulls |
| Kuznets (15-25 ans) | ✅ Vindiqué | 51 / 529 JST | LH_HPI 46 %, LH_POP 39 %, LH_CREDIT 41 % | recouvrement avec cycle financier Borio |
| Kondratieff (40-60 ans) | ♻️ Recasté | 2 / 16 BoE UK | UK dette publique + centrale brute | Reinhart-Rogoff war-debt chronology |
| **Universaliste** | ❌ Rejetée | 0 (BH-FDR) | n/a | floor 1/(B+1) > p* = 3.4·10⁻⁵ |

Le tableau ci-dessous (vue composite) reste comme **diagnostic
d'agrégation** : la nature `rejected` des composites confirme la
faille démontrée par la chaîne d'audits Roadmap #14 — c'est dans le
per-variable que la signature des trois cycles substantifs apparaît.

## Position canonique par cycle (vue composite, diagnostic)

### Position actuelle des 4 cycles canoniques — 2026-05

| Cycle | Source canonique | Agrégat | Phase | Tendance | Prochain extremum |
|---|---|---|---|---|---|
| Kitchin ⚠️ | Panel Banque mondiale (1960-2024) | `WLD` | rejected | — | — |
| Juglar ⚠️ | Histoire longue G7 (Maddison + JST, 1870-2022) | `G7` | rejected | — | — |
| Kuznets ⚠️ | Histoire longue G7 (Maddison + JST, 1870-2022) | `G7` | rejected | — | — |
| Kondratieff ⚠️ | Panel Banque mondiale (1960-2024) | `WLD` | rejected | — | — |

_⚠️ = effet endpoint CF dominant sur les dernières `hi_years/2` années ; la prévision donne l'ordre de grandeur, pas la date exacte._

Détails par agrégat : [Panel Banque mondiale](cycle_position_2026_05_wb.md) · [Panel trimestriel](cycle_position_2026_05_q.md) · [Histoire longue](cycle_position_2026_05_long.md).

## Lecture par cycle

- **Kitchin** (WLD, source `wb`) — phase `rejected`, tendance `—`, —.
- **Juglar** (G7, source `long`) — phase `rejected`, tendance `—`, —.
- **Kuznets** (G7, source `long`) — phase `rejected`, tendance `—`, —.
- **Kondratieff** (WLD, source `wb`) — phase `rejected`, tendance `—`, —.

## Panels étendus par horizon

### Banque mondiale (1960-2024)

### BRICS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### G7

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### OECD

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### WLD

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

_⚠️ = effet endpoint CF dominant (les dernières hi_years/2 années sont moins fiables ; la prévision donne l'ordre de grandeur, pas la date exacte)._

### Trimestriel (Path 5, 1960-Q1 2026)

### EA

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### G7Q

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### JPN

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### USA

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

_⚠️ = effet endpoint CF dominant (les dernières hi_years/2 années sont moins fiables ; la prévision donne l'ordre de grandeur, pas la date exacte)._

### Histoire longue (1870-2022)

### ADV18

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### ANGLO

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### EU4

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | contraction | falling | 📈 max dans 22 ans |

### G7

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | expansion | rising | 📈 max dans 7.2 ans |

### NORDIC

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | peak | rising (post-peak) | 📉 min dans 13 ans |

_⚠️ = effet endpoint CF dominant (les dernières hi_years/2 années sont moins fiables ; la prévision donne l'ordre de grandeur, pas la date exacte)._

### Bank of England Millennium (1700-2016)

_Aucun agrégat canonique disponible pour cet horizon._

### BIS macroprudential (1970-2025, EM+AE)

_Aucun agrégat canonique disponible pour cet horizon._

### Sectoral history (FRED+OWID+BEIS, 1850-present)

_Aucun agrégat canonique disponible pour cet horizon._

## Sign-off

- Date de la note : 2026-05-29T12:54:13+00:00
- As-of : 2026-05
- Schema EcoWave : `0.5.1`
- Pipeline : `ecowave home-synthesis`
