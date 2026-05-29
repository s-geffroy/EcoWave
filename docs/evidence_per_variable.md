# Évidence par variable — où le cycle survit-il quand on ne moyenne pas ?

> **Thèse centrale CPV.** Quand Gate 1 rejette un cycle sur un agrégat composite, c'est cohérent avec la littérature critique moderne ([Wen 2005](bibliographie.md#wen-2005), [Solomou 1987](bibliographie.md#solomou-1987), [Maddison 1991](bibliographie.md#maddison-1991)) qui montre que les cycles canoniques sont **étroits** : ils survivent sur des séries sectorielles spécifiques (inventaire, investissement, crédit, prix), pas sur des composites macro. Cette page démonte le composite et publie Gate 1 sur **chaque variable individuellement**.

## Résultat global

Sur **548 cellules** testées au total (variable × agrégat × cycle, 3 horizons), seules **8 survivent Gate 1** dual-null à α = 0.05 — soit **1.5%**.

**Comparaison avec les composites** (cf. [home dashboard](index.md#ou-en-sommes-nous)) : Gate 1 sur les agrégats composites laisse passer environ 25-30% des cellules. L'écart s'explique mécaniquement — sommer plusieurs séries z-scorées crée des artefacts de variance autocorrélée qui battent un null AR(1), même quand aucune des séries n'a individuellement de signal cyclique. **C'est exactement le diagnostic posé par [Wen (2005)](bibliographie.md#wen-2005) sur le cycle d'inventaire et par [Solomou (1987)](bibliographie.md#solomou-1987) sur Kuznets/Kondratieff il y a 40 et 20 ans respectivement.**

**Implication pour le protocole CPV.** Cette page ne remplace pas le dashboard composite (qui répond à *"que fait le cycle quand il survit ?"*). Elle le **stress-teste** : si une cellule survit sur le composite mais pas sur aucune de ses variables constituantes, le composite hallucine et la cellule devrait être réinterprétée. À l'inverse, si une variable individuelle survit isolément (`Q_PRD` Kondratieff, `CY_INV` Kitchin, `CY_GDP` Kuznets ci-dessous), c'est la **fenêtre sectorielle** où le cycle persiste — exactement la lecture des découvreurs (Kitchin sur l'inventaire, Kuznets sur la construction, etc.).

## Lecture

Pour chaque cycle, le tableau ci-dessous compte combien d'agrégats du jeu de données voient ce cycle survivre Gate 1 (dual null, α=0.05, 1000 surrogates) sur **chaque variable**. Une variable avec un taux de survie élevé est une **fenêtre sectorielle** où le cycle reste visible ; une variable avec un taux nul confirme la dilution par compositing.

## Kitchin

_Référence critique : [Wen 2005](bibliographie.md#wen-2005) — Kitchin survit sur stocks d'inventaire / production manufacturière, pas sur PIB._

### Panel Banque mondiale (1960-2024)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `CY_INV` | 1 | 8 | 12% | 0.029 |
| `CY_UEM` | 0 | 8 | 0% | 0.272 |
| `CY_INF` | 0 | 2 | 0% | 0.274 |
| `CY_PRD` | 0 | 8 | 0% | 0.320 |
| `CY_GDP` | 0 | 8 | 0% | 0.467 |
| `CY_TRD` | 0 | 8 | 0% | 0.688 |
| `CY_FIN` | 0 | 8 | 0% | 0.963 |
| `CY_POP` | 0 | 8 | 0% | 1.000 |

### Panel trimestriel (Path 5)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `Q_PRD` | 0 | 4 | 0% | 0.100 |
| `Q_YIELD` | 0 | 6 | 0% | 0.172 |
| `Q_UNRATE` | 0 | 5 | 0% | 0.200 |
| `Q_INV` | 0 | 5 | 0% | 0.211 |
| `Q_GDP` | 0 | 6 | 0% | 0.398 |
| `Q_HPI` | 0 | 6 | 0% | 0.599 |
| `Q_CREDIT` | 0 | 6 | 0% | 0.625 |
| `Q_CPI` | 0 | 5 | 0% | 0.982 |

### Histoire longue (1870-2022)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `LH_EQUITY` | 0 | 6 | 0% | 0.353 |
| `LH_YIELD` | 0 | 6 | 0% | 0.436 |
| `LH_HPI` | 0 | 6 | 0% | 0.899 |
| `LH_CREDIT` | 0 | 6 | 0% | 0.991 |
| `LH_CPI` | 0 | 6 | 0% | 1.000 |
| `LH_GDP` | 0 | 6 | 0% | 1.000 |

## Juglar

_Référence critique : [Romer 1999](bibliographie.md#romer-1999), [Stock-Watson 2003](bibliographie.md#stock-watson-2003) — Juglar instable post-1945, masqué dans les composites post-Great-Moderation._

### Panel Banque mondiale (1960-2024)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `CY_GDP` | 0 | 8 | 0% | 0.251 |
| `CY_UEM` | 0 | 8 | 0% | 0.272 |
| `CY_INV` | 0 | 8 | 0% | 0.322 |
| `CY_INF` | 0 | 2 | 0% | 0.719 |
| `CY_FIN` | 0 | 8 | 0% | 0.855 |
| `CY_PRD` | 0 | 8 | 0% | 0.964 |
| `CY_TRD` | 0 | 8 | 0% | 0.965 |
| `CY_POP` | 0 | 8 | 0% | 1.000 |

### Panel trimestriel (Path 5)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `Q_HPI` | 0 | 6 | 0% | 0.152 |
| `Q_UNRATE` | 0 | 5 | 0% | 0.190 |
| `Q_GDP` | 0 | 6 | 0% | 0.247 |
| `Q_INV` | 0 | 5 | 0% | 0.359 |
| `Q_YIELD` | 0 | 6 | 0% | 0.460 |
| `Q_CREDIT` | 0 | 6 | 0% | 0.542 |
| `Q_PRD` | 0 | 4 | 0% | 0.770 |
| `Q_CPI` | 0 | 5 | 0% | 0.799 |

### Histoire longue (1870-2022)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `LH_EQUITY` | 0 | 6 | 0% | 0.393 |
| `LH_YIELD` | 0 | 6 | 0% | 0.413 |
| `LH_CREDIT` | 0 | 6 | 0% | 0.907 |
| `LH_HPI` | 0 | 6 | 0% | 0.952 |
| `LH_CPI` | 0 | 6 | 0% | 1.000 |
| `LH_GDP` | 0 | 6 | 0% | 1.000 |

## Kuznets

_Référence critique : [Solomou 1987](bibliographie.md#solomou-1987), [Klotz-Neal 1973](bibliographie.md#klotz-neal-1973) — Kuznets pas distinct du bruit sur les agrégats annuels._

### Panel Banque mondiale (1960-2024)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `CY_GDP` | 1 | 8 | 12% | 0.010 |
| `CY_INV` | 0 | 8 | 0% | 0.225 |
| `CY_INF` | 0 | 2 | 0% | 0.323 |
| `CY_UEM` | 0 | 8 | 0% | 0.400 |
| `CY_FIN` | 0 | 8 | 0% | 0.577 |
| `CY_TRD` | 0 | 8 | 0% | 0.742 |
| `CY_POP` | 0 | 8 | 0% | 1.000 |
| `CY_PRD` | 0 | 8 | 0% | 1.000 |

### Panel trimestriel (Path 5)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `Q_CREDIT` | 0 | 6 | 0% | 0.136 |
| `Q_HPI` | 0 | 6 | 0% | 0.177 |
| `Q_UNRATE` | 0 | 5 | 0% | 0.185 |
| `Q_PRD` | 0 | 4 | 0% | 0.255 |
| `Q_CPI` | 0 | 5 | 0% | 0.420 |
| `Q_YIELD` | 0 | 6 | 0% | 0.513 |
| `Q_GDP` | 0 | 6 | 0% | 0.651 |
| `Q_INV` | 0 | 5 | 0% | 0.667 |

### Histoire longue (1870-2022)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `LH_CREDIT` | 0 | 6 | 0% | 0.360 |
| `LH_EQUITY` | 0 | 6 | 0% | 0.483 |
| `LH_YIELD` | 0 | 6 | 0% | 0.937 |
| `LH_CPI` | 0 | 6 | 0% | 0.976 |
| `LH_HPI` | 0 | 6 | 0% | 0.995 |
| `LH_GDP` | 0 | 6 | 0% | 1.000 |

## Kondratieff

_Référence critique : [Garvy 1943](bibliographie.md#garvy-1943), [Mansfield 1983](bibliographie.md#mansfield-1983), [Maddison 1991](bibliographie.md#maddison-1991) — K-wave : pas de mécanisme endogène identifié, phases exogènes._

### Panel Banque mondiale (1960-2024)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `CY_GDP` | 2 | 8 | 25% | 0.001 |
| `CY_PRD` | 1 | 8 | 12% | 0.007 |
| `CY_UEM` | 1 | 8 | 12% | 0.039 |
| `CY_INF` | 0 | 2 | 0% | 0.209 |
| `CY_INV` | 0 | 8 | 0% | 0.393 |
| `CY_FIN` | 0 | 8 | 0% | 0.469 |
| `CY_TRD` | 0 | 8 | 0% | 0.831 |
| `CY_POP` | 0 | 8 | 0% | 0.960 |

### Panel trimestriel (Path 5)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `Q_PRD` | 2 | 4 | 50% | 0.040 |
| `Q_CPI` | 0 | 5 | 0% | 0.159 |
| `Q_YIELD` | 0 | 6 | 0% | 0.192 |
| `Q_UNRATE` | 0 | 5 | 0% | 0.373 |
| `Q_GDP` | 0 | 6 | 0% | 0.470 |
| `Q_CREDIT` | 0 | 6 | 0% | 0.549 |
| `Q_HPI` | 0 | 6 | 0% | 0.554 |
| `Q_INV` | 0 | 5 | 0% | 0.818 |

### Histoire longue (1870-2022)

| Variable | Survies Gate 1 | Total agrégats | Taux | p-value min |
|---|---:|---:|---:|---:|
| `LH_EQUITY` | 0 | 6 | 0% | 0.235 |
| `LH_CPI` | 0 | 6 | 0% | 0.500 |
| `LH_CREDIT` | 0 | 6 | 0% | 0.695 |
| `LH_YIELD` | 0 | 6 | 0% | 0.937 |
| `LH_HPI` | 0 | 6 | 0% | 0.940 |
| `LH_GDP` | 0 | 6 | 0% | 0.994 |

## Spotlight : variables porteuses par agrégat phare

Pour chaque cycle, on isole l'agrégat avec le plus de variables survivantes — c'est là que le cycle est le mieux documenté. Les cellules sont les p-values brutes ; vert (`p ≤ 0.05`) marque les variables porteuses.

### Kitchin → LIC (horizon `wb`)

| Variable | p-value Gate 1 | Survit ? | n observations |
|---|---:|:---:|---:|
| `CY_INV` | 0.029 | ✅ | 34 |
| `CY_UEM` | 0.272 | ❌ | 35 |
| `CY_PRD` | 0.320 | ❌ | 45 |
| `CY_GDP` | 0.467 | ❌ | 44 |
| `CY_TRD` | 0.736 | ❌ | 34 |
| `CY_FIN` | 0.963 | ❌ | 60 |
| `CY_POP` | 1.000 | ❌ | 65 |

### Kuznets → BRICS (horizon `wb`)

| Variable | p-value Gate 1 | Survit ? | n observations |
|---|---:|:---:|---:|
| `CY_GDP` | 0.010 | ✅ | 64 |
| `CY_INF` | 0.323 | ❌ | 65 |
| `CY_UEM` | 0.400 | ❌ | 34 |
| `CY_INV` | 0.891 | ❌ | 65 |
| `CY_TRD` | 0.990 | ❌ | 65 |
| `CY_FIN` | 1.000 | ❌ | 65 |
| `CY_POP` | 1.000 | ❌ | 65 |
| `CY_PRD` | 1.000 | ❌ | 65 |

### Kondratieff → BRICS (horizon `wb`)

| Variable | p-value Gate 1 | Survit ? | n observations |
|---|---:|:---:|---:|
| `CY_GDP` | 0.001 | ✅ | 64 |
| `CY_INF` | 0.347 | ❌ | 65 |
| `CY_PRD` | 0.572 | ❌ | 65 |
| `CY_UEM` | 0.834 | ❌ | 34 |
| `CY_FIN` | 0.951 | ❌ | 65 |
| `CY_TRD` | 0.969 | ❌ | 65 |
| `CY_INV` | 0.971 | ❌ | 65 |
| `CY_POP` | 0.974 | ❌ | 65 |

## Sign-off

- Date de la note : 2026-05-29T09:42:28+00:00
- As-of : 2026-05
- Pipeline : `ecowave evidence-per-variable`
- Null : dual (AR(1) + phase-scramble), 1000 surrogates, α=0.05
