# Évidence par variable — où le cycle survit-il quand on ne moyenne pas ?

> **Thèse centrale CPV.** Quand Gate 1 rejette un cycle sur un agrégat composite, c'est cohérent avec la littérature critique moderne ([Wen 2005](bibliographie.md#wen-2005), [Solomou 1987](bibliographie.md#solomou-1987), [Maddison 1991](bibliographie.md#maddison-1991)) qui montre que les cycles canoniques sont **étroits** : ils survivent sur des séries sectorielles spécifiques (inventaire, investissement, crédit, prix), pas sur des composites macro. Cette page démonte le composite et publie Gate 1 sur **chaque variable individuellement**.

## Résultat global

Sur **1584 cellules** testées au total (variable × agrégat × cycle, 3 horizons), seules **21 survivent Gate 1** dual-null à α = 0.05 — soit **1.3%**.

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
| `LH_STIR` | 1 | 6 | 17% | 0.044 |
| `LH_UNRATE` | 0 | 6 | 0% | 0.214 |
| `LH_EQTR` | 0 | 6 | 0% | 0.353 |
| `LH_EQUITY` | 0 | 6 | 0% | 0.353 |
| `LH_YIELD` | 0 | 6 | 0% | 0.436 |
| `LH_BONDTR` | 0 | 6 | 0% | 0.499 |
| `LH_EQDIVP` | 0 | 6 | 0% | 0.536 |
| `LH_CA` | 0 | 6 | 0% | 0.566 |
| `LH_BILLRATE` | 0 | 6 | 0% | 0.789 |
| `LH_HOUSINGTR` | 0 | 6 | 0% | 0.813 |
| `LH_HPI` | 0 | 6 | 0% | 0.899 |
| `LH_HOUSECG` | 0 | 6 | 0% | 0.902 |
| `LH_DEBTGDP` | 0 | 6 | 0% | 0.942 |
| `LH_BONDRATE` | 0 | 6 | 0% | 0.950 |
| `LH_MORT` | 0 | 6 | 0% | 0.967 |
| `LH_CREDIT` | 0 | 6 | 0% | 0.991 |
| `LH_INV` | 0 | 6 | 0% | 0.992 |
| `LH_EXP` | 0 | 6 | 0% | 0.998 |
| `LH_REV` | 0 | 6 | 0% | 0.998 |
| `LH_BANKDEBT` | 0 | 6 | 0% | 1.000 |
| `LH_BUSCREDIT` | 0 | 6 | 0% | 1.000 |
| `LH_CPI` | 0 | 6 | 0% | 1.000 |
| `LH_EXPORTS` | 0 | 6 | 0% | 1.000 |
| `LH_GDP` | 0 | 6 | 0% | 1.000 |
| `LH_GDPNOM` | 0 | 6 | 0% | 1.000 |
| `LH_HHCREDIT` | 0 | 6 | 0% | 1.000 |
| `LH_IMPORTS` | 0 | 6 | 0% | 1.000 |
| `LH_LEV` | 0 | 6 | 0% | 1.000 |
| `LH_MONEY` | 0 | 6 | 0% | 1.000 |
| `LH_NARROW` | 0 | 6 | 0% | 1.000 |
| `LH_POP` | 0 | 6 | 0% | 1.000 |
| `LH_RCONS` | 0 | 6 | 0% | 1.000 |
| `LH_RGDP_BARRO` | 0 | 6 | 0% | 1.000 |
| `LH_WAGE` | 0 | 6 | 0% | 1.000 |
| `LH_XRUSD` | 0 | 5 | 0% | 1.000 |

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
| `LH_HOUSECG` | 0 | 6 | 0% | 0.094 |
| `LH_HOUSINGTR` | 0 | 6 | 0% | 0.098 |
| `LH_UNRATE` | 0 | 6 | 0% | 0.152 |
| `LH_CA` | 0 | 6 | 0% | 0.213 |
| `LH_BILLRATE` | 0 | 6 | 0% | 0.300 |
| `LH_EQUITY` | 0 | 6 | 0% | 0.393 |
| `LH_EQTR` | 0 | 6 | 0% | 0.401 |
| `LH_YIELD` | 0 | 6 | 0% | 0.413 |
| `LH_DEBTGDP` | 0 | 6 | 0% | 0.438 |
| `LH_BONDTR` | 0 | 6 | 0% | 0.646 |
| `LH_INV` | 0 | 6 | 0% | 0.662 |
| `LH_STIR` | 0 | 6 | 0% | 0.674 |
| `LH_BONDRATE` | 0 | 6 | 0% | 0.805 |
| `LH_EQDIVP` | 0 | 6 | 0% | 0.847 |
| `LH_CREDIT` | 0 | 6 | 0% | 0.907 |
| `LH_MORT` | 0 | 6 | 0% | 0.940 |
| `LH_HPI` | 0 | 6 | 0% | 0.952 |
| `LH_XRUSD` | 0 | 5 | 0% | 0.968 |
| `LH_LEV` | 0 | 6 | 0% | 0.984 |
| `LH_BANKDEBT` | 0 | 6 | 0% | 1.000 |
| `LH_BUSCREDIT` | 0 | 6 | 0% | 1.000 |
| `LH_CPI` | 0 | 6 | 0% | 1.000 |
| `LH_EXP` | 0 | 6 | 0% | 1.000 |
| `LH_EXPORTS` | 0 | 6 | 0% | 1.000 |
| `LH_GDP` | 0 | 6 | 0% | 1.000 |
| `LH_GDPNOM` | 0 | 6 | 0% | 1.000 |
| `LH_HHCREDIT` | 0 | 6 | 0% | 1.000 |
| `LH_IMPORTS` | 0 | 6 | 0% | 1.000 |
| `LH_MONEY` | 0 | 6 | 0% | 1.000 |
| `LH_NARROW` | 0 | 6 | 0% | 1.000 |
| `LH_POP` | 0 | 6 | 0% | 1.000 |
| `LH_RCONS` | 0 | 6 | 0% | 1.000 |
| `LH_REV` | 0 | 6 | 0% | 1.000 |
| `LH_RGDP_BARRO` | 0 | 6 | 0% | 1.000 |
| `LH_WAGE` | 0 | 6 | 0% | 1.000 |

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
| `LH_CA` | 1 | 6 | 17% | 0.002 |
| `LH_BUSCREDIT` | 0 | 6 | 0% | 0.227 |
| `LH_UNRATE` | 0 | 6 | 0% | 0.339 |
| `LH_CREDIT` | 0 | 6 | 0% | 0.360 |
| `LH_BANKDEBT` | 0 | 6 | 0% | 0.361 |
| `LH_EQTR` | 0 | 6 | 0% | 0.483 |
| `LH_EQUITY` | 0 | 6 | 0% | 0.483 |
| `LH_HOUSECG` | 0 | 6 | 0% | 0.503 |
| `LH_HHCREDIT` | 0 | 6 | 0% | 0.548 |
| `LH_MORT` | 0 | 6 | 0% | 0.582 |
| `LH_INV` | 0 | 6 | 0% | 0.668 |
| `LH_HOUSINGTR` | 0 | 6 | 0% | 0.737 |
| `LH_BONDTR` | 0 | 6 | 0% | 0.744 |
| `LH_LEV` | 0 | 6 | 0% | 0.744 |
| `LH_BONDRATE` | 0 | 6 | 0% | 0.745 |
| `LH_EQDIVP` | 0 | 6 | 0% | 0.747 |
| `LH_BILLRATE` | 0 | 6 | 0% | 0.749 |
| `LH_DEBTGDP` | 0 | 6 | 0% | 0.816 |
| `LH_YIELD` | 0 | 6 | 0% | 0.937 |
| `LH_EXP` | 0 | 6 | 0% | 0.970 |
| `LH_CPI` | 0 | 6 | 0% | 0.976 |
| `LH_REV` | 0 | 6 | 0% | 0.976 |
| `LH_STIR` | 0 | 6 | 0% | 0.980 |
| `LH_XRUSD` | 0 | 5 | 0% | 0.983 |
| `LH_HPI` | 0 | 6 | 0% | 0.995 |
| `LH_EXPORTS` | 0 | 6 | 0% | 1.000 |
| `LH_GDP` | 0 | 6 | 0% | 1.000 |
| `LH_GDPNOM` | 0 | 6 | 0% | 1.000 |
| `LH_IMPORTS` | 0 | 6 | 0% | 1.000 |
| `LH_MONEY` | 0 | 6 | 0% | 1.000 |
| `LH_NARROW` | 0 | 6 | 0% | 1.000 |
| `LH_POP` | 0 | 6 | 0% | 1.000 |
| `LH_RCONS` | 0 | 6 | 0% | 1.000 |
| `LH_RGDP_BARRO` | 0 | 6 | 0% | 1.000 |
| `LH_WAGE` | 0 | 6 | 0% | 1.000 |

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
| `LH_DEBTGDP` | 1 | 6 | 17% | 0.028 |
| `LH_UNRATE` | 0 | 6 | 0% | 0.055 |
| `LH_BONDTR` | 0 | 6 | 0% | 0.119 |
| `LH_CA` | 0 | 6 | 0% | 0.136 |
| `LH_HOUSINGTR` | 0 | 6 | 0% | 0.149 |
| `LH_EQUITY` | 0 | 6 | 0% | 0.235 |
| `LH_EQTR` | 0 | 6 | 0% | 0.286 |
| `LH_HOUSECG` | 0 | 6 | 0% | 0.333 |
| `LH_EQDIVP` | 0 | 6 | 0% | 0.488 |
| `LH_CPI` | 0 | 6 | 0% | 0.500 |
| `LH_LEV` | 0 | 6 | 0% | 0.517 |
| `LH_BILLRATE` | 0 | 6 | 0% | 0.529 |
| `LH_BONDRATE` | 0 | 6 | 0% | 0.529 |
| `LH_CREDIT` | 0 | 6 | 0% | 0.695 |
| `LH_INV` | 0 | 6 | 0% | 0.710 |
| `LH_MORT` | 0 | 6 | 0% | 0.756 |
| `LH_BUSCREDIT` | 0 | 6 | 0% | 0.773 |
| `LH_HHCREDIT` | 0 | 6 | 0% | 0.796 |
| `LH_REV` | 0 | 6 | 0% | 0.849 |
| `LH_EXP` | 0 | 6 | 0% | 0.867 |
| `LH_YIELD` | 0 | 6 | 0% | 0.937 |
| `LH_HPI` | 0 | 6 | 0% | 0.940 |
| `LH_NARROW` | 0 | 6 | 0% | 0.989 |
| `LH_GDP` | 0 | 6 | 0% | 0.994 |
| `LH_STIR` | 0 | 6 | 0% | 0.999 |
| `LH_BANKDEBT` | 0 | 6 | 0% | 1.000 |
| `LH_EXPORTS` | 0 | 6 | 0% | 1.000 |
| `LH_GDPNOM` | 0 | 6 | 0% | 1.000 |
| `LH_IMPORTS` | 0 | 6 | 0% | 1.000 |
| `LH_MONEY` | 0 | 6 | 0% | 1.000 |
| `LH_POP` | 0 | 6 | 0% | 1.000 |
| `LH_RCONS` | 0 | 6 | 0% | 1.000 |
| `LH_RGDP_BARRO` | 0 | 6 | 0% | 1.000 |
| `LH_WAGE` | 0 | 6 | 0% | 1.000 |
| `LH_XRUSD` | 0 | 5 | 0% | 1.000 |

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

### Juglar → RU_BIS (horizon `bis`)

| Variable | p-value Gate 1 | Survit ? | n observations |
|---|---:|:---:|---:|
| `BIS_BUSCRED` | 0.050 | ✅ | 112 |
| `BIS_CGAP` | 0.677 | ❌ | 82 |
| `BIS_CRATIO` | 1.000 | ❌ | 122 |
| `BIS_HHCRED` | 1.000 | ❌ | 111 |
| `BIS_RPP` | 1.000 | ❌ | 100 |

### Kuznets → MX_BIS (horizon `bis`)

| Variable | p-value Gate 1 | Survit ? | n observations |
|---|---:|:---:|---:|
| `BIS_RPP` | 0.001 | ✅ | 84 |
| `BIS_BUSCRED` | 0.019 | ✅ | 140 |
| `BIS_CGAP` | 0.338 | ❌ | 140 |
| `BIS_CRATIO` | 0.500 | ❌ | 180 |
| `BIS_HHCRED` | 0.807 | ❌ | 124 |

### Kondratieff → ID_BIS (horizon `bis`)

| Variable | p-value Gate 1 | Survit ? | n observations |
|---|---:|:---:|---:|
| `BIS_RPP` | 0.007 | ✅ | 96 |
| `BIS_BUSCRED` | 0.049 | ✅ | 96 |
| `BIS_CRATIO` | 0.384 | ❌ | 199 |
| `BIS_HHCRED` | 0.448 | ❌ | 96 |
| `BIS_CGAP` | 0.769 | ❌ | 159 |

## Sign-off

- Date de la note : 2026-05-29T12:54:11+00:00
- As-of : 2026-05
- Pipeline : `ecowave evidence-per-variable`
- Null : dual (AR(1) + phase-scramble), 1000 surrogates, α=0.05
