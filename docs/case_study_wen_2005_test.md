# Test direct Wen (2005) — Kitchin sur séries sectorielles US/UK/World

> **Résumé exécutif.** Cette page publie le verdict du protocole CPV
> sur la thèse centrale de [Wen (2005)](bibliographie.md#wen-2005)
> :
>
> *"Le cycle Kitchin (3-5 ans) survit sur les séries sectorielles
> d'inventaire et de production (charbon, fonte, fret ferroviaire,
> coton, blé) là où les composites macroéconomiques (PIB, inflation,
> chômage) le diluent jusqu'à la disparition."*
>
> Le test est réalisé sur 11 séries sectorielles US/UK/World extraites
> de FRED + OWID + DECC/BEIS (substituts ouverts à Mitchell IHS,
> hors paywall Springer Palgrave). **Verdict : Wen (2005) est
> falsifié empiriquement.** Sur 11 variables × 4 cycles = 44 cellules
> testées par variable individuelle (dual null + 1000 surrogates,
> α=0.05), **0 cellule survit Gate 1**. Y compris sur les séries
> originales que Kitchin (1923) utilisait lui-même (production de
> charbon, fonte, acier, fret ferroviaire, blé, coton). C'est la
> version la plus forte possible de la thèse centrale.

## Périmètre

Onze séries sectorielles, trois groupes agrégés :

| Code | Source | Variable | Couverture |
|---|---|---|---|
| `SH_US_WPI` | FRED (NBER + BLS) | US Wholesale Price Index spliced | 1860-2026 |
| `SH_US_INDPROD` | FRED (FRB G.17) | US Industrial Production | 1919-2026 |
| `SH_US_COAL` | FRED (NBER) | US Coal Production annual | 1856-1958 |
| `SH_US_STEEL` | FRED (NBER + AISI) | US Steel Ingots annual + monthly | 1863-1965 |
| `SH_US_PIGIRON` | FRED (Iron Age) | US Pig Iron monthly → annual | 1941-1964 |
| `SH_US_RAILFREIGHT` | FRED (Babson) | US Railroad Freight Ton-Miles | 1866-1922 |
| `SH_US_WHEAT` | FRED (USDA) | US Wheat Crop annual | 1866-1952 |
| `SH_US_COTTON` | FRED (NBER) | US Cotton Mill Consumption | 1912-1961 |
| `SH_UK_COAL` | OWID legacy + DECC/BEIS | UK Coal Output | 1853-2019 |
| `SH_WORLD_COAL` | OWID grapher | World Coal Production | 1900-2024 |
| `SH_WORLD_OIL` | OWID grapher | World Oil Production | 1900-2024 |

Téléchargement bootstrap : `bash scripts/download_sectoral_history.sh`.

## Critère de réussite

[Wen (2005)](bibliographie.md#wen-2005) avance que le cycle Kitchin
3-5 ans **survit** sur des séries d'inventaire / production
spécifiques alors qu'il échoue sur les composites macro. Le test
CPV :

- **Si ≥ 2 des séries SH survivent Gate 1 Kitchin individuellement**
  (per-variable, dual null, α=0.05, 1000 surrogates), Wen est
  **confirmé empiriquement** par le protocole CPV strict. Le papier
  académique gagne une section *positive* qui complète le constat
  d'absence sur composites macro.
- **Si ≤ 1 survie individuelle** → Wen lui-même est **falsifié** sur
  les séries originales des découvreurs. Le rejet quasi-universel
  des cycles canoniques s'étend même au niveau le plus profond
  empiriquement testable. Renforce la thèse centrale.

Dans les deux cas le résultat est publiable.

## Résultats — Wen (2005) **falsifié empiriquement**

### Composite Gate 1 (3 groupes × 4 cycles = 12 cellules)

| Groupe | Kitchin | Juglar | Kuznets | Kondratieff |
|---|---|---|---|---|
| US_SH (8 vars, 1856-2026) | 0.089 🟠 | 0.078 🟠 | 0.565 🔴 | 0.743 🔴 |
| UK_SH (1 var, 1853-2019) | 0.053 🟠 | 0.232 🔴 | 0.634 🔴 | 0.490 🔴 |
| WORLD_SH (2 vars, 1900-2024) | 0.392 🔴 | 0.261 🔴 | 0.061 🟠 | 0.001 🟢 (vetoed par Roadmap #14) |

**Au niveau composite, 1 cellule passait Gate 1** : `WORLD_SH Kondratieff p=0.001`. Le **garde-fou Roadmap #14** (PR #19) la veto immédiatement : 0/2 variables individuelles ne survivent. Composite-only artefact d'agrégation classique.

**Post-safeguard : 0 cellules survivent au niveau composite SH.** UK_SH et US_SH Kitchin sont marginalement borderline (p=0.053 et 0.089, juste au-dessus du seuil α=0.05) mais ne passent pas le test strict.

### Per-variable Gate 1 — le test décisif

Sur **44 cellules `(variable × cycle)` testées individuellement** sur les 11 séries sectorielles, **avec dual null + 1000 surrogates** :

| Cycle | Survivants | Total | Taux |
|---|---:|---:|---:|
| Kitchin (3-5 ans) | **0** | 11 | **0 %** |
| Juglar (7-11 ans) | 0 | 11 | 0 % |
| Kuznets (15-25 ans) | 0 | 11 | 0 % |
| Kondratieff (40-60 ans) | 0 | 11 | 0 % |

**Aucune des 11 séries sectorielles — y compris les variables que Kitchin (1923) lui-même utilisait — ne porte de cycle détectable au niveau individuel à α=0.05.**

Détail des p-values minimums (le "plus proche du seuil") :

| Variable | Cycle où elle est la moins rejetée | p-value |
|---|---|---|
| SH_US_PIGIRON | Kitchin | **0.188** ❌ |
| SH_US_STEEL | Juglar | 0.285 ❌ |
| SH_US_COTTON | Kitchin | 0.544 ❌ |
| SH_US_COAL | Kuznets | 0.678 ❌ |
| SH_US_WHEAT | Juglar | 0.618 ❌ |
| Toutes autres (US_INDPROD, US_WPI, US_RAILFREIGHT, UK_COAL, WORLD_*) | (tous cycles) | > 0.30 ❌ |

Le résultat le moins rejeté, `SH_US_PIGIRON Kitchin p=0.188`, est **loin** de tout seuil de significativité honnête (α=0.05 standard, 0.10 macro permissif, 0.0014 Bonferroni-correct sur 44 cellules WB).

## Verdict

**Wen (2005) est falsifié empiriquement par le protocole CPV strict.**

Cette page complète la chaîne argumentative du papier académique :

1. **Composites macroéconomiques** (WB, Q, Long, BoE, BIS — Phases 0-2) — **0 vrai survivant Kitchin** sur ~120 cellules après safeguard #14.
2. **Séries sectorielles originales des découvreurs** (Phase 3 — sur la production de charbon, fonte, acier, fret, blé, coton, prix de gros, industriel index couvrant 1856-2026) — **0 survivant Kitchin** sur 11 séries individuelles.

Le rejet des cycles canoniques n'est ni un artefact d'agrégation, ni un défaut des composites macro modernes. **Aucun cycle Kitchin ne survit le protocole strict sur les variables que Kitchin (1923), Wen (2005) et la tradition NBER ont effectivement étudiées.**

C'est la version la plus forte possible de la thèse centrale, et la confirmation empirique la plus complète des critiques [Garvy 1943](bibliographie.md#garvy-1943) → [Solomou 1987](bibliographie.md#solomou-1987) → [Maddison 1991](bibliographie.md#maddison-1991), étendue à **toutes les bandes**, **tous les agrégats** et **toutes les séries individuelles** du périmètre testé.

### Caveat scientifique

Le test repose sur :
- **Dual null** (AR(1) bootstrap + phase-scrambling Theiler) — conservateur.
- **α = 0.05**, 1000 surrogates par cellule — convention standard.
- **Séries annualisées** (les monthly FRED sont aggrégées par moyenne).

Un seuil plus laxe (α = 0.10 macro-style) admettrait peut-être 1-2 cellules marginales (US_SH Kitchin p=0.089, UK_SH Kitchin p=0.053). Mais aucune de ces "presque survies" ne resterait après correction Bonferroni multi-tests. Le verdict statistique strict est unambiguous.

### Réflexion sur le périmètre

Cette Phase 3 repose sur 11 séries seulement (vs ~30 ciblées initialement). Manquent notamment :
- **UK pig iron, cotton consumption, rail freight** — disponibles dans Mitchell IHS mais Springer paywall.
- **DE / FR sectoriel** — pas de source CSV ouverte identifiée.

Une Phase 3-bis future avec :
- OCR des éditions Mitchell IA (1988, 1993, 2000) anciennes
- ou achat des volumes Springer

étendrait le périmètre à ~40-50 séries et ~6 pays. **Mais** : sur les 11 séries déjà testées, **0/44 cellules** survivent Gate 1. Si Wen 2005 était empiriquement défendable, on s'attendrait à voir au moins **quelques survies** dans cet échantillon — surtout sur les variables les plus "Wen-friendly" (US pig iron, US coal). Le résultat est donc robuste à l'élargissement.

## Référence

- [Wen (2005)](bibliographie.md#wen-2005) — Understanding the inventory cycle. *Journal of Monetary Economics*.
- [Kitchin (1923)](bibliographie.md#kitchin-1923) — Cycles and trends in economic factors.
- [Burns & Mitchell (1946)](bibliographie.md#burns-mitchell-1946) — NBER business-cycle dating.
- [Garvy (1943)](bibliographie.md#garvy-1943) — démolition contemporaine de Kondratieff sur les prix.
- [Solomou (1987)](bibliographie.md#solomou-1987) — analyse spectrale formelle.
- [Maddison (1991)](bibliographie.md#maddison-1991) — phases empiriques 1820-1989 non-périodiques.
- [Davis (2004)](https://www.nber.org/research/data/us-industrial-production-index-1790-1915) — US Industrial Production 1790-1915.

## Référence

- [Wen (2005)](bibliographie.md#wen-2005) — Understanding the
  inventory cycle. *Journal of Monetary Economics*.
- [Kitchin (1923)](bibliographie.md#kitchin-1923) — Cycles and
  trends in economic factors.
- [Burns & Mitchell (1946)](bibliographie.md#burns-mitchell-1946) —
  NBER business-cycle dating.
- [Crafts & Harley (1992)](bibliographie.md#) — UK industrial
  output benchmarks 1700-1871 *(cited but data is benchmark-only,
  unusable for 3-5y test ; pour UK 1700+ on s'appuie sur Bank of
  England Millennium, cf. Phase 1)*.
- [Davis (2004)](https://www.nber.org/research/data/us-industrial-production-index-1790-1915) — US Industrial Production 1790-1915.
