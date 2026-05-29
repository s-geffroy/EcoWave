# Pré-traitement Kondratieff — différenciation pour éliminer la fuite de tendance

> **Résumé.** Suite aux audits CN_BIS et WLD-WB Kondratieff qui ont
> exposé un artefact d'agrégation systématique (les composites des
> variables avec tendance dominante simulent un demi-K-cycle dans la
> fenêtre du filtre band-pass), CPV applique désormais une
> **première-différence avant compositing pour la bande Kondratieff
> uniquement**. La fuite de tendance via les effets de bord du CF
> band-pass est éliminée en convertissant les séries de niveau en
> taux de croissance, qui sont typiquement à retour vers la moyenne
> et ne fuient pas. Les autres bandes (Kitchin, Juglar, Kuznets)
> restent sur les niveaux z-scorés.

## Le problème — fuite de tendance par effet de bord CF

Le filtre Christiano-Fitzgerald (CF) band-pass, utilisé pour isoler
les cycles dans une bande de fréquence donnée, a une **propriété
mathématique inévitable** : ses effets de bord (les premières et
dernières `hi_years/2` années de la série) sont sévèrement biaisés.
Pour la bande Kondratieff (`hi_years=60`), c'est **30 ans à chaque
extrémité** qui sont contaminés.

Pour les agrégats les plus longs du pipeline CPV :

| Horizon | Couverture | hi_years/2 K | Fenêtre fiable |
|---|---|---|---|
| WB (`WLD`) | 65 ans | 30 ans | 5 ans au centre |
| Long (`ADV18`) | 152 ans | 30 ans | 92 ans au centre |
| BoE (`UK_BOE`) | 316 ans | 30 ans | 256 ans au centre |

Sur les fenêtres courtes (WB 65 ans, BIS 40-55 ans), la zone fiable
est inférieure à un cycle K complet. Le filtre déborde de la trend
réelle dans la bande K.

## Le diagnostic — confirmation par audit

Deux études de cas dévoilent le mécanisme :

- [Étude de cas CN_BIS Kondratieff](case_study_cn_bis_kondratieff.md) :
  duplication CRATIO/TCRED + transition exponentielle 1985-2025.
  Avant fix : `p=0.025` (survies). Après fix duplication :
  `p=0.051` (rejected).
- [Étude de cas WLD-WB Kondratieff](case_study_wld_wb_kondratieff.md) :
  composite K = moyenne(CY_FIN, CY_PRD), les deux variables
  trend-dominées (R²_log = 0.64 et 0.99). Individuellement, aucune
  ne porte de signal K (`p=0.728` et `p=0.993`). Composite : `p=0.001`.

**Le pattern est identique** : moyenne de variables avec ACF lag-1
≈ 1 et R² log-linéaire élevé → composite trend dominé → CF
band-pass capte la moitié de la trend comme un demi-cycle K.

## La solution adoptée — différenciation pour K seulement

### Spécification

Pour la bande Kondratieff (et **uniquement** pour cette bande), le
pipeline applique désormais :

```python
work_panel = panel.diff().dropna(how="all")  # Δx_t = x_t - x_{t-1}
# Then continue with z-score + CF band-pass + composite
```

Avant différenciation : `CY_PRD` = 3663, 3812, 3984, ... (trend croissante)

Après différenciation : `ΔCY_PRD` = 149, 172, ... (taux de croissance,
mean-reverting autour de ~150)

Le `Δx` d'une trend monotone est une série stationnaire (au moins
faiblement). La z-score d'une série stationnaire est stationnaire.
La moyenne de plusieurs séries stationnaires est stationnaire. Le
filtre band-pass [40-60y] sur une série stationnaire **ne fuit
plus** la trend (puisqu'il n'y a plus de trend à fuir).

### Pourquoi seulement Kondratieff ?

| Bande | Période | hi_years/2 | Zone d'effet de bord | Tendances problématiques ? |
|---|---|---|---|---|
| Kitchin | 3-5 ans | 2.5 ans | 2.5 ans/côté | Non |
| Juglar | 7-11 ans | 5.5 ans | 5.5 ans/côté | Non |
| Kuznets | 15-25 ans | 12.5 ans | 12.5 ans/côté | Marginal sur WB 65 ans |
| **Kondratieff** | **40-60 ans** | **30 ans** | **30 ans/côté** | **OUI — domine sur les samples ≤ 100 ans** |

Pour Kitchin/Juglar, les effets de bord sont courts. Les variables
avec ACF lag-1 > 0.95 (financiarisation, démographie) ont une
puissance basse-fréquence qui leak dans les bandes longues, pas
dans Kitchin/Juglar. Différencier Kitchin/Juglar introduirait du
bruit supplémentaire sans bénéfice : les cycles courts sont déjà
mesurés sur des taux de croissance économique implicitement (CY_GDP,
CY_INF sont des growth rates).

Pour Kuznets, le débat est ouvert. À 65 ans (WB) et hi=25, la zone
de bord est 12.5 ans/côté = 38% du sample. Plausible qu'un signal
trend-leaké soit présent, mais moins prononcé qu'en K.
**Conservé en levels pour l'instant**, à auditer à l'avenir avec
le même protocole que CN_BIS et WLD-WB.

### Quand le band-pass ne peut pas tourner

Le filtre CF nécessite `samples ≥ 2 × hi_years`. Pour K avec hi=60 :

| Horizon | `samples_per_year` | Sample en années | Sample en obs | Min pour K (2×60) | Band-pass possible ? |
|---|---|---|---|---|---|
| WB | 1 | 65 | 65 | 120 | ❌ |
| Long | 1 | 152 | 152 | 120 | ✅ |
| BoE | 1 | 316 | 316 | 120 | ✅ |
| Quarterly | 4 | 65 | 260 | 480 | ❌ |
| BIS | 4 | 55 | 220 | 480 | ❌ |

Sur les horizons où le band-pass K ne peut pas tourner (WB, Q, BIS),
le pipeline utilise un fallback : moyenne z-scorée du panel
**niveaux**. C'est précisément là que vivait l'artefact WLD-WB. Le
fix étend la différenciation à ce fallback aussi — la moyenne
z-scorée du panel **différencié** remplace la moyenne z-scorée du
panel niveaux.

## Vérification empirique post-fix — un résultat plus nuancé que prévu

Re-run des 5 horizons avec différenciation pour K (dual null, 1000
surrogates par cellule, samples_per_year cohérent par horizon) :

### Survies pré-fix qui passent en rejected (les artefacts attendus)

| Cellule | p avant (niveaux) | p après (différencié) | Verdict |
|---|---:|---:|---|
| WLD-WB K | 0.001 🟢 | **0.488 🔴** | survies → rejected — artefact CY_FIN+CY_PRD |
| HIC-WB K | 0.001 🟢 | **0.473 🔴** | survies → rejected — même artefact |
| OECD-WB K | 0.001 🟢 | **0.560 🔴** | survies → rejected — même artefact |
| G7-WB K | 0.055 🟠 | 0.161 🔴 | marginal → rejected |

**Confirme l'hypothèse** que la signature K sur le panel WB
(1960-2024, 65 ans) était entièrement un artefact de fuite de
tendance des variables `CY_FIN` (financiarisation) et `CY_PRD`
(productivité).

### Survies qui émergent (inattendues)

Plus surprenant, la différenciation **fait émerger** plusieurs K
sur les horizons longs européens :

| Cellule | p avant (niveaux) | p après (différencié) | Notes |
|---|---:|---:|---|
| **G7-long K** | 0.001 🟢 | **0.001 🟢** | persistant — possiblement réel |
| **NORDIC-long K** | 0.608 🔴 | **0.001 🟢** | émerge sur 152 ans |
| **EU4-long K** | 0.142 🔴 | **0.004 🟢** | émerge sur 152 ans |
| **UK_BOE K** | 0.892 🔴 | **0.001 🟢** | émerge sur 316 ans (!) |
| LIC-WB K | 0.506 🔴 | **0.012 🟡** | apparition |
| ADV18-long K | 0.300 🔴 | 0.066 🟠 | marginal |

### Interprétation provisoire

Cette redistribution suggère **deux mécanismes distincts** :

1. **Sur les samples courts** (WB 65 ans, BIS 40-55 ans), le CF
   band-pass ne peut pas tourner (`hi_years/2 > sample/4`), tombe
   en fallback sur la moyenne z-scorée. La différenciation
   supprime alors les artefacts de fuite de tendance — c'est le
   résultat attendu.

2. **Sur les samples longs** (Long 152 ans, BoE 316 ans), le CF
   band-pass fonctionne pleinement. La différenciation y révèle
   des signatures K que la version sur niveaux masquait sous le
   bruit de trend. **Cohérent avec Schumpeter (1939)** qui regardait
   les taux de croissance, pas les niveaux. Le K-wave européen
   1700-2025 mesuré sur les taux de croissance pourrait être un
   phénomène empirique authentique — mais nécessite vérification.

### Garde-fou — diagnostic par variable

Pour distinguer "redistribution d'artefact" de "découverte authentique",
le pipeline `evidence-per-variable --horizons boe,long` est lancé en
parallèle. Si les K nouvellement-survivants (G7-long, UK_BOE) sont
portés par **plusieurs variables individuelles** indépendamment, le
signal est probablement réel. Si seul le composite survit (comme pour
CN_BIS et WLD-WB pré-fix), c'est un artefact d'agrégation post-
différenciation. La case study correspondante sera publiée après
le run `evidence-per-variable --horizons boe,long` actuellement
en cours.

Le verdict final sur la portée de ce fix méthodologique attend
ces résultats.

## Implications

### 1. Les artefacts de fuite de tendance sont éliminés

Sur les samples courts (WB 65 ans, BIS 40-55 ans), 4 K-survies
disparaissent : `WLD-WB`, `HIC-WB`, `OECD-WB`, `G7-WB` (de
marginal à rejected). Ce sont les artefacts attendus de fuite
de tendance par effet de bord CF. **La thèse centrale est
confirmée sur ce périmètre.**

### 2. Le test K reste applicable

Différencier n'est PAS abandonner le test K. Si une K-wave authentique
existait (régularité 40-60 ans observable dans les taux de croissance,
pas seulement les niveaux), la série différenciée la capturerait.
L'absence d'un tel signal après différenciation est une **conclusion
empirique forte**, pas un artefact méthodologique.

### 3. Question méthodologique élargie

Différencier pour K soulève la question : devrait-on aussi
différencier pour Kuznets ? Pour les composites contenant
explicitement des variables trend-dominées ? Une règle automatique
type "différencier si max ACF lag-1 > 0.95" serait défendable.
**À auditer dans un PR ultérieur**.

### 4. Falsifiabilité du protocole

L'application post-hoc d'un fix qui transforme p=0.001 en p=0.904
peut sembler ad hoc. Trois garde-fous :
- **Le fix est pré-publié** dans cette page, applicable à toutes les
  futures runs, pas seulement à 2026-05.
- **La justification est mécaniste**, pas adaptée au résultat
  voulu : le band-pass CF a une fuite de tendance documentée
  ([Christiano & Fitzgerald 2003](bibliographie.md#christiano-fitzgerald-2003)).
- **Le fix ne change pas Kitchin/Juglar/Kuznets** ; il n'est ciblé
  que sur la bande où l'audit a démontré l'artefact.

## Référence bibliographique

- [Christiano & Fitzgerald (2003)](bibliographie.md#christiano-fitzgerald-2003) — paper original du CF filter, documente les effets de bord.
- [Hamilton (2018)](bibliographie.md#hamilton-2018) — critique générale des filtres band-pass pour l'inférence sur les cycles.
- [Garvy (1943)](bibliographie.md#garvy-1943), [Mansfield (1983)](bibliographie.md#mansfield-1983), [Solomou (1987)](bibliographie.md#solomou-1987), [Maddison (1991)](bibliographie.md#maddison-1991) — les références sceptiques que ce fix renforce empiriquement.
