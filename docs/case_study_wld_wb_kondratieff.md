# Étude de cas — WLD-WB Kondratieff : trends agrégées simulant un demi-K-cycle

> **Résumé exécutif.** Après le démasquage de [CN_BIS Kondratieff comme
> artefact d'agrégation](case_study_cn_bis_kondratieff.md), le même
> protocole appliqué à `WLD-WB Kondratieff p=0.001` (le seul autre
> survivant K du pipeline) révèle un **artefact mécaniquement
> équivalent**, plus subtil. Le composite K consomme uniquement 2
> variables (CY_FIN et CY_PRD), **toutes deux des tendances
> structurelles pures** (R² log-lin = 0.66 et 0.99, ACF lag-1 ≈ 0.97
> et 1.000). Individuellement, aucune ne survit Gate 1 (p = 0.728 et
> 0.993). Leur moyenne z-scorée crée néanmoins un signal au filtre
> band-pass [40-60y] qui ressemble à un demi-K-cycle. **Ni le crédit
> chinois ni la financiarisation/productivité mondiale ne supportent
> empiriquement une K-wave**. Confirme la
> [thèse centrale](bibliographie.md#critiques-et-scepticisme-empirique-par-cycle)
> : les K-waves apparentes émergent de transitions exogènes (great
> moderation, globalisation, financiarisation, transition chinoise),
> pas de mécanismes cycliques endogènes.

## Le point de départ — l'unique K survivant restant

Après élimination de l'artefact CN_BIS, le tableau de bord home ne
publie plus qu'**une seule cellule Kondratieff survivante** sur tout
le pipeline CPV :

| Cellule | p-value Gate 1 | Phase | Tendance | Prochain extremum |
|---|---|---|---|---|
| `WLD` (Banque mondiale 1960-2024) | **0.001 🟢** | contraction | rising | 📈 max dans 7.3 ans |

Le doute est légitime : pourquoi le composite WB-WLD verrait-il un K-wave
alors que :
- UK_BoE (316 ans, 16 vars) → `p=0.892` (rejected)
- ADV18 (152 ans, 35 vars Phase 0) → `p=0.300` (rejected)
- Tous les EM individuels BIS → `p > 0.45` (rejected)
- WLD-WB sur 65 ans = 1.1-1.6 K-cycles ?

Application du même protocole en 5 étapes.

## Diagnostic en 5 étapes

### 1. Couverture du sample

| Variable | Coverage | N obs | Cycles K théoriques (40-60y) |
|---|---|---|---|
| CY_GDP | 1960-2025 | 64 | 1.1 - 1.6 |
| CY_INV | 1960-2025 | 55 | 0.9 - 1.4 |
| CY_FIN | 1960-2025 | 45 | 0.7 - 1.1 |
| CY_PRD | 1960-2025 | 65 | 1.1 - 1.6 |
| CY_POP | 1960-2025 | 65 | 1.1 - 1.6 |
| CY_TRD | 1960-2025 | 55 | 0.9 - 1.4 |
| CY_UEM | 1960-2025 | 35 | 0.5 - 0.9 |
| CY_INF | 1960-2025 | **0 non-NaN** | — (la BM n'agrège pas l'inflation au niveau mondial) |

**~1 K-cycle maximum dans la fenêtre**. Détection statistique de
Kondratieff à 65 ans est intrinsèquement précaire.

### 2. Forme des séries WLD

| Variable | Range | R² log-lin | ACF lag-1 | Verdict |
|---|---|---:|---:|---|
| CY_GDP (real growth %) | -2.9 → 6.6 | 0.14 | 0.21 | stationnaire |
| CY_INV (% PIB) | 23.0 → 27.5 | 0.00 | 0.81 | stationnaire (mean-reverting) |
| CY_UEM (%) | 4.8 → 6.6 | 0.07 | 0.78 | stationnaire |
| **CY_FIN** | 69 → 146 | **0.64** | **0.97** | **TENDANCE — financiarisation** |
| **CY_TRD** (% PIB) | 26 → 62 | **0.89** | **0.97** | **TENDANCE — globalisation** |
| **CY_PRD** | 3663 → 11852 | **0.99** | **0.998** | **TENDANCE — productivité 3.2 %/an** |
| **CY_POP** | 34M → 57M | **1.00** | **1.000** | **TENDANCE pure** |

**4 variables sur 7 ont une trend dominante (R² log-lin > 0.60)**.
Toutes captent la grande accélération post-1980 (productivité,
globalisation, financiarisation) — un phénomène structurel, pas un
cycle.

### 3. Votes inter-méthode Gate 2 (matrice WLD K)

```text
D (PELT change-point)    = peak
E (Markov-switching)     = contraction
F (CF + Hilbert)         = expansion
G (Bry-Boschan)          = contraction
```

Plurality : 2/4 votes pour `contraction` (E + G). Comme pour CN_BIS,
c'est en-deçà du `min_agreement=3` standard mais accepté par la règle
relâchée Kondratieff `min_agreement=2`. **Aucune méthode ne s'aligne
nettement** ; D voit un pic, F voit une expansion, E et G voient une
contraction. Pas de structure cyclique cohérente.

### 4. Évidence par variable — l'effondrement

`ecowave evidence-per-variable --horizons wb` teste Gate 1 sur chaque
variable individuelle sans compositing. Sur `WLD-WB Kondratieff` :

| Variable | n obs | p-value Gate 1 | Survit ? |
|---|---:|---:|:---:|
| CY_UEM | 35 | 0.039 | ✅ (marginal, sample court) |
| CY_INV | 55 | 0.393 | ❌ |
| CY_GDP | 64 | 0.661 | ❌ |
| **CY_FIN** | 45 | **0.728** | ❌ |
| CY_POP | 65 | 1.000 | ❌ |
| CY_TRD | 55 | 1.000 | ❌ |
| **CY_PRD** | 65 | **0.993** | ❌ |

**Le composite K WLD ne consomme que CY_FIN et CY_PRD** (les deux
variables avec `cycle_targets=['kondratieff']` dans le manifest WB).
Or :

- CY_FIN seule → `p=0.728` (rejeté)
- CY_PRD seule → `p=0.993` (rejeté maximalement)

**Aucun signal K dans les constituants**. La survie composite à
`p=0.001` est créée par l'agrégation.

### 5. Mécanisme de l'artefact

Le composite Kondratieff WLD = moyenne_z(CY_FIN, CY_PRD).

Chaque variable est une trend monotone z-scorée. La z-score d'une
trend est elle-même une trend (recentrée, rescalée). La moyenne de 2
trends z-scorées reste une trend, légèrement bruitée. Cette
trend-composite a :

- **plus de puissance basse-fréquence** qu'un AR(1) bootstrap (qui
  décroît exponentiellement),
- **plus de puissance basse-fréquence** qu'un phase-scramble (qui
  préserve la PSD mais détruit la phase),

donc le test dual-null rejette le bruit AR(1)+phase-scramble. **Le
CF band-pass [40-60y] capte la moitié de la rampe sur 65 ans
comme un demi-K-cycle.**

C'est mécaniquement **le même artefact que CN_BIS**, juste avec
2 variables-trends au lieu d'une série dupliquée. Plus subtil mais
identique structurellement.

## Implication méthodologique

Le filtre `targets_by_var` (Roadmap #11) censurait censément ce
problème en assignant les variables à leurs bandes appropriées. Mais
ici, **les variables pré-enregistrées comme "kondratieff targets"
sont précisément celles qui sont dominées par des tendances** :
CY_FIN (financiarisation) et CY_PRD (productivité). Ces choix
reflètent une **présupposition théorique** ([Perez 2002] sur les
vagues techno-économiques, [Schumpeter 1939] sur les ondes longues)
plus qu'une preuve empirique.

Trois options de garde-fou méthodologique restent à explorer (hors
scope de ce diagnostic, à valider scientifiquement) :

1. **Pre-detrending** — appliquer un linear detrending (ou HP-filter
   λ=400 000 pour annuel) à chaque variable AVANT la z-score. Force
   le composite à ne capter que les déviations à la trend, pas la
   trend elle-même.
2. **Exclusion sur ACF** — exclure du composite K les variables avec
   `ACF lag-1 > 0.95` (signe de non-stationnarité forte).
3. **Différenciation** — z-scorer la **première différence** des
   variables-niveau (CY_PRD → croissance productivité ; CY_FIN →
   variation crédit-PIB) avant le compositing.

Chacune des trois changerait le verdict CPV pour Kondratieff. **Aucune
n'est anodine** : elles correspondent à des modèles statistiques
implicitement différents pour ce qu'est "un cycle". Question pour la
suite : doit-on **transformer les séries pour qu'elles ressemblent à
des cycles** avant de tester si elles le sont, ou tester telles
quelles et accepter que les tendances structurelles fassent rejeter
les K-waves par défaut ?

## Verdict final sur WLD-WB Kondratieff

Le composite `WLD-WB Kondratieff p=0.001 (contraction, max 7.3 ans)`
est **un artefact d'agrégation de tendances**, exactement comme
[CN_BIS Kondratieff p=0.025](case_study_cn_bis_kondratieff.md). Il
**ne reflète pas un cycle endogène mondial de 40-60 ans**, mais la
signature spectrale des transitions structurelles post-1980 (financiarisation,
globalisation, productivité) captée à la fenêtre de bande passante K.

**Aucune cellule Kondratieff ne survit Gate 1 dual-null au niveau
des variables individuelles**, à l'exception marginale de `WLD-WB
CY_UEM p=0.039` (35 obs, ~0.5 K-cycle de couverture).

→ **Confirmation empirique massive de la thèse centrale CPV**. Les
critiques modernes ([Garvy 1943](bibliographie.md#garvy-1943),
[Mansfield 1983](bibliographie.md#mansfield-1983),
[Solomou 1987](bibliographie.md#solomou-1987),
[Maddison 1991](bibliographie.md#maddison-1991)) avaient raison :
**le Kondratieff n'est pas un cycle empiriquement distinct du
bruit**. Toutes les survies du pipeline CPV sont des artefacts
d'agrégation, de tendance structurelle, ou de sample court.

## Référence bibliographique

- [Garvy (1943)](bibliographie.md#garvy-1943) — démolition contemporaine de Kondratieff sur les prix.
- [Maddison (1991)](bibliographie.md#maddison-1991) — phases 1820-1989 ne respectent pas la périodicité K.
- [Mansfield (1983)](bibliographie.md#mansfield-1983) — grappes d'innovations sans périodicité K.
- [Perez (2002)](bibliographie.md#perez-2002) — défenseur des vagues techno-économiques (la présupposition théorique derrière les `cycle_targets`).
- [Schumpeter (1939)](bibliographie.md#schumpeter-1939) — théorie des ondes longues (la même présupposition).
- [Solomou (1987)](bibliographie.md#solomou-1987) — analyse spectrale formelle : K-waves non distinctes du bruit.
- [Wen (2005)](bibliographie.md#wen-2005) — cycles survivent sur séries sectorielles, pas sur composites.
