# Étude de cas — CN_BIS Kondratieff : l'artefact d'agrégation démasqué

> **Résumé exécutif.** Le seul Kondratieff survivant hors `WLD-WB` dans
> tout le pipeline CPV était `CN_BIS` à `p=0.025` (peak phase, projection
> d'un minimum dans ~13 ans). Le diagnostic par variable montre que
> **aucune des séries de crédit chinoises individuelles ne porte de
> signal K** (toutes p ≥ 0.108). La survie au niveau composite est un
> **artefact d'agrégation** créé par (1) la duplication de la série
> crédit-PIB privé sous deux noms BIS différents, (2) la transition
> structurelle 1985-2025 du crédit chinois (CAGR 3.2 %/an) capturée par
> le filtre band-pass comme une demi-période K. Cohérent avec la
> critique [Maddison (1991)](bibliographie.md#maddison-1991) et
> [Solomou (1987)](bibliographie.md#solomou-1987) — les apparentes
> K-waves émergent de transitions exogènes, pas de cycles endogènes.

## Le point de départ — un signal anormal

La Phase 2 du Roadmap #13 a fait surgir un résultat surprenant dans le
tableau de bord home :

| Cellule | p-value Gate 1 | Phase | Tendance | Prochain extremum |
|---|---|---|---|---|
| `CN_BIS` Kondratieff | **0.025 🟡** | peak | rising (post-peak) | 📉 min dans 13 ans |

C'est la **seule cellule Kondratieff survivante** hors `WLD-WB` (panel
Banque mondiale, 1960-2024). Pour rappel, sur 316 ans de données UK
(BoE Millennium), Kondratieff est rejeté à `p=0.892`. Sur l'agrégat
`ADV18` (18 économies avancées, 1870-2020, ~150 ans), `p=0.300`. Sur
tous les autres agrégats EM individuels (BR, IN, MX, KR, TR, ZA, RU,
ID), Kondratieff est rejeté avec `p > 0.45`. Pourquoi la Chine ferait
exception ?

## Diagnostic — 5 vérifications

### 1. Couverture du sample

```text
BIS_CRATIO (CN) :  1985Q4 → 2025Q3   (40 ans = ~0.7 cycle K)
BIS_TCRED  (CN) :  1985Q4 → 2025Q3   (40 ans)
BIS_CGAP   (CN) :  1995Q4 → 2025Q3   (30 ans)
BIS_RPP    (CN) :  2005Q2 → 2025Q4   (20 ans)
```

**40 ans = moins d'un cycle Kondratieff complet** (période 40-60
ans). Le marqueur ⚠️ endpoint-caveat est plus que cosmétique :
`hi_years/2 = 30 ans`, donc **les 30 dernières années sur 40** sont
dominées par les artefacts de bord du filtre Christiano-Fitzgerald.

### 2. Forme des séries

```text
BIS_CRATIO (CN) : 62.4 → 201.4
  log-linear R²  = 0.956   ← série quasi-purement exponentielle
  CAGR           = 3.2 %/an
  lag-1 ACF      = 0.998   ← autocorrélation maximale

BIS_TCRED  (CN) : 62.4 → 201.4  ← IDENTIQUE à BIS_CRATIO !
  ...mêmes statistiques...

BIS_CGAP   (CN) : -14.7 → 25.5
  range autour de 0 (HP-filter détrended par construction)
  lag-1 ACF = 0.958

BIS_RPP    (CN) : 86.8 → 113.0
  range étroit, sample court (20 ans)
```

**`BIS_CRATIO` et `BIS_TCRED` sont identiques.** Les filtres BIS du
loader produisent la même série
*Credit to Private non-financial sector from All sectors at Market
value - Percentage of GDP - Adjusted for breaks* sous deux codes CPV
distincts. Le composite z-scoré pondère donc cette série **2 fois sur
4** — soit 50 % du poids.

### 3. Votes inter-méthode Gate 2

```text
CN_BIS Kondratieff :
  D (PELT change-point)    = expansion
  E (Markov-switching)     = peak
  F (CF + Hilbert)         = peak
  G (Bry-Boschan)          = contraction
```

Plurality : 2/4 votes pour `peak`. La règle Gate 2 standard demande
**≥3/4** d'accord. Or la cellule est publiée comme `peak` non
`disputed` — c'est parce que la bande Kondratieff a une règle
relâchée `min_agreement=2` (justifié par la difficulté intrinsèque
de détection K). Mais **2/4 méthodes en accord est un consensus
faible**, plus proche du bruit que d'une régularité scientifique.

### 4. Évidence par variable (le coup de grâce)

`ecowave evidence-per-variable --horizons bis --null dual
--n-surrogates 1000` teste Gate 1 directement sur **chaque variable
individuelle**, sans compositing :

| Variable | p-value Gate 1 | Survit ? |
|---|---:|:---:|
| BIS_CRATIO | **1.000** | ❌ rejeté maximalement |
| BIS_TCRED | **1.000** | ❌ rejeté maximalement |
| BIS_RPP | 0.108 | ❌ marginal (>0.10) |
| BIS_CGAP | 0.335 | ❌ rejeté |

**Aucune** des 4 variables ne porte de signal Kondratieff
détectable. Le composite `CN_BIS Kondratieff p=0.025` émerge donc
**de la combinaison**, pas des constituants.

### 5. Mécanisme de l'artefact

La z-score standardise chaque série à variance unitaire, puis le
composite est la moyenne. Avec :

- `BIS_CRATIO` et `BIS_TCRED` identiques (ACF=0.998, exponentielle
  pure) → 2 colonnes z-scorées hautement colinéaires,
- `BIS_CGAP` détrendé (cycle court financier),
- `BIS_RPP` court et plat,

la moyenne reproduit essentiellement `CRATIO_zscored` avec un peu
de bruit. Le filtre band-pass CF [40-60y] capture **un seul demi-
cycle** dans la fenêtre 40 ans : la montée monotone du ratio
crédit-PIB chinois de 62 % (1985) à 200 % (2025).

Cette montée est **structurelle** (transition économique chinoise
post-Deng-Xiaoping), pas **cyclique** (mécanisme endogène
auto-générateur). Mais le test Gate 1 dual-null teste seulement
"y a-t-il plus de puissance dans la bande K que dans un AR(1)
bootstrap ?". Une rampe exponentielle a effectivement plus de
puissance basse-fréquence qu'un AR(1) (qui décroît plus vite) →
le test rejette le null sans pour autant valider l'hypothèse
cyclique.

## Action correctrice — décomposition sectorielle du crédit

Bug confirmé dans `load_total_credit` (filtre
`TC_BORROWERS='P'` = aggregate privé all). Remplacé par
décomposition Mian-Sufi (2018) :

```python
sector_to_code = {
    "H": "BIS_HHCRED",   # households
    "C": "BIS_BUSCRED",  # corporates (non-fin)
    "G": "BIS_GVCRED",   # general government
}
```

Sur CN_BIS, le panel passe de 4 vars (avec duplication) à 5 vars
distinctes :

```text
BIS_CRATIO  (CN) : 160 obs, 62 → 202
BIS_BUSCRED (CN) : 120 obs, 95 → 296   ← corporate seul, sans agrégat P
BIS_HHCRED  (CN) :  79 obs, 11 → 61    ← household credit, montée post-2009
BIS_CGAP    (CN) : 120 obs, -15 → 25
BIS_RPP     (CN) :  83 obs, 87 → 113
```

(`BIS_GVCRED` non disponible pour CN dans le bulk BIS.)

## Test du fix — résultat

Le re-run `position-cycles --horizon bis` avec le manifest corrigé
(BIS_TCRED → BIS_HHCRED + BIS_BUSCRED + BIS_GVCRED) confirme
l'hypothèse :

| Cycle | p Gate 1 **avant** (CRATIO=TCRED dupliqué) | p Gate 1 **après** (décomposition sectorielle) | Δ |
|---|---:|---:|---|
| Kitchin | 0.044 🟡 (survives) | **0.091 🟠** | survies → marginal-rejected |
| Juglar | 0.878 🔴 | 0.885 🔴 | inchangé |
| Kuznets | 0.337 🔴 | 0.301 🔴 | inchangé |
| **Kondratieff** | **0.025 🟡 (phase=peak)** | **0.051 🟠 (rejected)** | **survie → rejected** |

Le Kondratieff CN_BIS passe de `p=0.025` (clairement survivant à
α=0.05) à `p=0.051` (juste sous le seuil — rejeté avec α=0.05,
mais resterait survivant à α=0.10 macro-laxe). **Le doublement de
poids sur le crédit-PIB chinois explosif (CRATIO+TCRED identiques)
était responsable de ~2.5 % de marge de p-value** — la moitié de
la zone borderline du test Gate 1.

**Diagnostic résiduel** : même corrigé, `p=0.051` reste près du
seuil. Cela suggère que la transition structurelle 1985-2025 du
crédit chinois projette une faible signature résiduelle dans la
bande K, **insuffisante pour passer Gate 1 strict**. Cohérent
avec Maddison (1991) — les phases macroéconomiques visibles ne
respectent pas la périodicité K. L'apparente K-signature est un
**effet de bord** du structural break, pas un cycle endogène.

→ **Voir le tableau de bord home** pour le verdict actuel sur
`CN_BIS Kondratieff` (devrait afficher des cellules `—`).

## Implications pour le protocole CPV

1. **Renforcement de la thèse centrale** ([[cpv-central-thesis]]).
   Quand on examine une survivance Gate 1 à la loupe, elle se
   révèle artefactuelle. Cohérent avec
   [Garvy (1943)](bibliographie.md#garvy-1943),
   [Solomou (1987)](bibliographie.md#solomou-1987),
   [Maddison (1991)](bibliographie.md#maddison-1991) : les
   "K-waves" empiriques résultent de transitions structurelles
   exogènes (guerres, transitions économiques), pas de mécanismes
   cycliques endogènes.

2. **L'évidence par variable est un garde-fou critique**. Le
   composite Gate 1 seul aurait laissé passer `CN_BIS K p=0.025`
   comme un résultat publiable. Le test
   [`evidence-per-variable`](evidence_per_variable.md) révèle que
   l'agrégation manufacture le signal. À intégrer
   systématiquement dans toute lecture future.

3. **Garde-fou sur le sample**. Pour Kondratieff (40-60y), exiger
   un minimum de N ≥ 2 cycles dans la fenêtre = **120 ans
   minimum**. Le CN_BIS (40 ans) est en-dessous du seuil de
   détectabilité statistique honnête. À renforcer dans la
   documentation méthodologique.

4. **Hygiène du compositing**. Chaque variable du composite doit
   être un canal **distinct** du cycle visé. Une duplication
   passe inaperçue mais corrompt le test. À ajouter aux contrôles
   automatiques du runner.

## Référence bibliographique

- [Garvy (1943)](bibliographie.md#garvy-1943) — démolition contemporaine de Kondratieff sur les prix.
- [Maddison (1991)](bibliographie.md#maddison-1991) — les phases 1820-1989 ne respectent pas la périodicité K.
- [Mansfield (1983)](bibliographie.md#mansfield-1983) — les grappes d'innovations ne montrent pas de périodicité K.
- [Solomou (1987)](bibliographie.md#solomou-1987) — analyse spectrale formelle : K-waves non distinctes du bruit.
- [Wen (2005)](bibliographie.md#wen-2005) — les cycles survivent sur séries sectorielles, pas sur composites.

Le diagnostic CN_BIS est un *cas d'école* de chacune de ces critiques.
