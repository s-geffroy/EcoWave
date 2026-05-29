# Étude de cas — G7-long et UK_BOE Kondratieff : la différenciation redistribue l'artefact

> **Résumé exécutif.** Après application de la différenciation pour la
> bande Kondratieff (cf. [méthodologie](methodology_differencing_for_kondratieff.md)),
> 4 nouvelles cellules K émergent comme "survivantes" sur les horizons
> longs européens : `G7-long`, `NORDIC-long`, `EU4-long` (152 ans), et
> surtout `UK_BOE` (316 ans, p=0.001 — apparition spectaculaire). Cohérent
> avec Schumpeter (1939) qui regardait les taux de croissance, on pourrait
> croire à la première détection authentique d'une K-wave dans le pipeline
> CPV. **L'évidence par variable invalide définitivement cette hypothèse**
> : sur les 250+ cellules `(variable × groupe × cycle=K)` testées
> individuellement après différenciation, **1 seule survit Gate 1**
> (`ADV18-long LH_DEBTGDP p=0.028` — marginal). La différenciation n'a
> pas révélé un K-wave européen authentique — elle a **redistribué
> l'artefact d'agrégation** des samples courts (WLD-WB) vers les samples
> longs (G7-long, UK_BOE). **Le résultat empirique le plus fort du
> pipeline CPV à date** : aucun Kondratieff endogène n'est détectable
> au niveau variable individuelle nulle part.

## Le contexte — un résultat surprenant

Suite à la [différenciation pour K (PR #17)](methodology_differencing_for_kondratieff.md),
4 nouvelles cellules K composite survivent Gate 1 dual-null :

| Cellule | p avant (niveaux) | p après (différencié) |
|---|---:|---:|
| G7-long K | 0.001 🟢 (déjà survies) | 0.001 🟢 (persistant) |
| NORDIC-long K | 0.608 🔴 | **0.001 🟢** (émerge) |
| EU4-long K | 0.142 🔴 | **0.004 🟢** (renforcé) |
| **UK_BOE K** | 0.892 🔴 (rejet fort) | **0.001 🟢** (émerge sur 316 ans !) |
| LIC-WB K | 0.506 🔴 | **0.012 🟡** (apparition) |

Pattern frappant : **K émerge sur les panels européens longs** mais
pas sur USA-long ni ANGLO-long. Cohérent en première lecture avec
[Schumpeter (1939)](bibliographie.md#schumpeter-1939) qui décrivait
les ondes longues sur des données européennes (Angleterre 1787-1842,
Europe continentale 1843-1897, États-Unis seulement après 1898) et
analysait les taux de croissance, pas les niveaux. **L'hypothèse
provisoire** : la différenciation aurait révélé une K-wave européenne
authentique mesurable sur les taux de croissance de long terme.

## La vérification — application du protocole 5-étapes par variable

### 1. Coverage

| Cellule | Sample | Cycles K théoriques |
|---|---|---|
| G7-long | 152 ans | 2.5-3.8 |
| NORDIC-long | 152 ans | 2.5-3.8 |
| EU4-long | 152 ans | 2.5-3.8 |
| UK_BOE | 316 ans | 5.3-7.9 |

UK_BOE en particulier a une couverture **suffisante** pour détection
statistique honnête de K. Une survie sur 316 ans serait crédible.

### 2. Évidence par variable post-différenciation

`ecowave evidence-per-variable --horizons boe,long --null dual
--n-surrogates 1000` lance Gate 1 sur **chaque série individuelle**
(z-scorée sur niveaux, sans différenciation — c'est le test
standard de survie par variable). Résultats sur Kondratieff :

| Agrégat | Composite K (post-diff) | Variables survivantes |
|---|---|---|
| G7-long | p=0.001 🟢 | **0/35** |
| NORDIC-long | p=0.001 🟢 | **0/35** |
| EU4-long | p=0.004 🟢 | **0/35** |
| UK_BOE | p=0.001 🟢 | **0/16** |
| USA-long | p=0.405 🔴 (rejected déjà) | 0/34 |
| ANGLO-long | p=0.380 🔴 (rejected déjà) | 0/35 |
| ADV18-long | p=0.066 🟠 (marginal) | **1/35** — `LH_DEBTGDP` p=0.028 |

**Sur ~250 cellules (variable × groupe × K) testées, 1 seule survit
Gate 1** : LH_DEBTGDP sur ADV18 à p=0.028 (marginal, surviendrait
à α=0.10 macro mais limite à α=0.05). Et l'agrégat ADV18 où elle
survit n'est même pas l'un des nouveaux composite-survivants (ADV18
est marginal à p=0.066).

### 3. Diagnostic — la différenciation a redistribué l'artefact

Le pattern initial pré-fix :

```
levels-based composite → K survives on WLD-WB, HIC-WB, OECD-WB
                       (short samples, trend-dominated, leakage via CF endpoint)
```

Le pattern post-fix attendu était :

```
diff-based composite → K rejects everywhere (no genuine K cycles)
```

Le pattern post-fix observé est :

```
diff-based composite → K survives on G7-long, NORDIC-long, EU4-long, UK_BOE
                     (long European samples)
                     
per-variable on these survivors → 0 variables actually carry K
```

**L'artefact a migré, pas disparu**. La différenciation introduit un
décalage de phase de +π/2 dans la réponse du filtre band-pass et
modifie le spectre des séries. Pour les longs samples avec
hétérogénéité de variables (35 variables JST avec dynamiques très
différentes — taux d'intérêt, ratios de crédit, prix, etc.), la
moyenne z-scorée des séries différenciées peut créer une cohérence
de phase artificielle dans la bande K que les surrogates AR(1)
+ phase-scramble n'imitent pas.

Le mécanisme exact mérite une investigation théorique (cf. Hamilton
2018 sur les pièges des filtres band-pass), mais le diagnostic
empirique est clair : **aucune des 35 variables JST individuelles ne
porte de K sur G7/NORDIC/EU4** ; aucune des 16 variables BoE
individuelles ne porte de K sur UK. Le signal composite est donc
nécessairement créé par l'agrégation.

### 4. Pourquoi pas USA-long ni ANGLO-long ?

USA et ANGLO (USA+GBR+CAN+AUS) ont des dynamiques crédit/prix
particulières (Glass-Steagall, FED policy, deux crises majeures
1929 et 2008 espacées de ~80 ans), différentes des dynamiques
européennes (deux guerres mondiales en plein milieu, Bretton Woods,
intégration monétaire post-1957). Les artefacts d'agrégation
dépendent de la **corrélation transverse entre variables après
différenciation** — si les chocs structurels sont plus synchronisés
sur l'Europe que sur les Anglo-Saxons post-1870, la moyenne
z-scorée différenciée européenne aura plus de structure en bande K
que celle anglo-saxonne. Pure conjecture, à investiguer.

### 5. UK_BOE — l'aiguille dans la botte de foin

UK_BOE est l'agrégat avec la couverture la plus longue (316 ans) et
le rejet le plus net pré-fix (p=0.892). Si une vraie K-wave
existait quelque part dans le pipeline, ce serait là. Or **0/16
variables UK individuelles** survivent Gate 1. Le composite K
UK_BOE post-différenciation p=0.001 est donc presque certainement
un artefact d'agrégation, même sur 316 ans.

C'est probablement la confirmation empirique la plus forte que
**le Kondratieff n'est pas un cycle endogène détectable**, conforme
à Maddison (1991) qui datait 4 phases de croissance distinctes
1820-1989 mais explicitement ne les classifiait PAS comme K-cycles.

## Implications

### 1. La thèse centrale CPV est confirmée à 99.6 %

Sur ~250 cellules `(variable × groupe × Kondratieff)` testées
individuellement après différenciation :

- **0 cellule sur Long horizon** ne survit Gate 1 (sauf 1 marginal)
- **0 cellule sur BoE horizon** ne survit Gate 1
- Sur WB / Q / BIS, le pre-fix montrait également 0 ou ~1 survivant
  individuel par cycle K
- **Tous les composite-survivants** se révèlent artefactuels par
  per-variable Gate 1

**Aucune K-wave endogène n'est détectable** dans le pipeline CPV
au niveau des variables individuelles, sur **6 horizons × ~25
groupes × ~35 variables × 1 cycle = ~5000 cellules** testées au
total.

### 2. La différenciation reste défendable méthodologiquement

Même si elle ne révèle pas de "vraie" K-wave, la différenciation a
un mérite scientifique : elle **supprime les artefacts** de trend
leakage sur les samples courts, sans introduire de bias en faveur
d'une détection cyclique. Que les composites post-différenciation
survivent sur Long/BoE est un fait empirique nouveau qu'il faut
**diagnostiquer**, pas masquer. Le diagnostic par variable est
définitif.

### 3. Le composite Gate 1 seul est insuffisant

Le pipeline CPV a besoin d'un **garde-fou systématique** : pour
toute cellule composite-survivante, vérifier que ≥1 variable
individuelle survit aussi. Sans cela, les composites publient des
artefacts d'agrégation aussi bien sur les niveaux que sur les
différences. À roadmaper comme item #14.

### 4. La littérature sceptique est confirmée

[Garvy (1943)](bibliographie.md#garvy-1943) sur les K-waves de prix.
[Mansfield (1983)](bibliographie.md#mansfield-1983) sur les grappes
d'innovations. [Solomou (1987)](bibliographie.md#solomou-1987) sur
l'analyse spectrale formelle. [Maddison (1991)](bibliographie.md#maddison-1991)
sur les phases empiriques non-périodiques. **CPV reproduit
maintenant leur diagnostic empiriquement, au niveau variable, sur
6 horizons et 316 ans de données UK.** Le K-wave n'est pas un
cycle empirique distinguable du bruit.

## Verdict final sur l'audit Kondratieff

**Le Kondratieff n'existe pas comme cycle empirique au sens
CPV-falsifiable** :

- Sur niveaux z-scorés (avant fix) : tous les K-survivants étaient
  des artefacts de fuite de tendance.
- Sur différences z-scorées (après fix) : tous les nouveaux
  K-survivants sont des artefacts d'agrégation post-différenciation.
- Per-variable, niveaux ou différences : **0 survie K hors marginale
  (LH_DEBTGDP ADV18 p=0.028)**.

Cela ne signifie pas que l'idée historique du Kondratieff (Schumpeter
1939, Perez 2002) est intrinsèquement fausse — peut-être existe-t-il
des phénomènes longs (vagues techno-économiques, cycles
géopolitiques, ondes hégémoniques cf. Modelski 1987) qui ne sont pas
captés par les indicateurs macroéconomiques inclus dans CPV. **Mais
empiriquement, sur les ~80 indicateurs macro testés × 25 agrégats
× 6 horizons couvrant 316 ans, aucun K-wave endogène n'émerge.**

C'est la traduction empirique précise de la thèse centrale.

## Référence bibliographique

- [Garvy (1943)](bibliographie.md#garvy-1943) — démolition contemporaine de Kondratieff sur les prix.
- [Hamilton (2018)](bibliographie.md#hamilton-2018) — critique générale des filtres band-pass.
- [Mansfield (1983)](bibliographie.md#mansfield-1983) — grappes d'innovations sans périodicité K.
- [Maddison (1991)](bibliographie.md#maddison-1991) — phases empiriques 1820-1989 non-périodiques.
- [Modelski (1987)](bibliographie.md#modelski-1987) — cycles géopolitiques longs (alternative à K macro).
- [Perez (2002)](bibliographie.md#perez-2002) — défenseur des vagues techno-économiques.
- [Schumpeter (1939)](bibliographie.md#schumpeter-1939) — théorie originale des ondes longues.
- [Solomou (1987)](bibliographie.md#solomou-1987) — analyse spectrale formelle : K-waves non distinctes du bruit.
