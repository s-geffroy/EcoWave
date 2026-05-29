# Garde-fou Roadmap #14 — composite-survies doivent être étayées par une variable

> **Résumé.** Suite à la chaîne d'audits CN_BIS → WLD-WB → G7-long/UK_BOE
> qui a démontré que **toutes les survies Gate 1 au niveau composite
> étaient des artefacts d'agrégation**, le pipeline CPV applique
> désormais un garde-fou systématique : pour publier une cellule
> `(agrégat, cycle)` comme survivante, il faut que **≥1 variable
> individuelle survive aussi Gate 1** sur la même bande. Sinon, la
> cellule est basculée en `rejected` avec la note `"Roadmap #14 veto:
> composite p=X but 0/N variables survive"`. Aucun changement sur les
> rejets composites — qui sont honnêtes par construction.

## Motivation

Quatre études de cas successives ont exposé un mécanisme systématique :

| Étude | Composite | Variables individuelles | Diagnostic |
|---|---|---|---|
| [CN_BIS Kondratieff](case_study_cn_bis_kondratieff.md) | p=0.025 🟡 | 0/4 (CRATIO=TCRED) | duplication de série |
| [WLD-WB Kondratieff](case_study_wld_wb_kondratieff.md) | p=0.001 🟢 | 0/7 | composite trend-dominé |
| [G7-long & UK_BOE K](case_study_g7_long_uk_boe_kondratieff.md) | p=0.001 🟢 (×4) | 0/16 à 0/35 | cohérence post-diff |
| Verdict général K | tous artefactuels | 1/250 (LH_DEBTGDP) | aucun K endogène |

Le pattern est identique : **le composite agrégé fabrique un signal
que les variables constituantes ne portent pas**. Le test composite
seul est donc structurellement insuffisant pour publier des résultats
falsifiables. La règle Roadmap #14 corrige cette faille.

## Spécification

### Quand le garde-fou se déclenche

Pour chaque cellule `(agrégat, cycle)` du pipeline :

1. Calculer le composite Gate 1 (test dual-null AR(1) + scramble de
   phase, 1000 surrogates, α=0.05, comme avant).
2. **Si le composite REJETTE** : publier `rejected` (inchangé).
3. **Si le composite SURVIT** : lancer le test per-variable :
   - Pour chaque variable individuelle de `band_panel` (filtrée par
     `targets_by_var` à la bande considérée),
   - Si la bande est Kondratieff, appliquer la différenciation
     (`series.diff()`) — symétrie avec le composite.
   - Z-scorer la série individuelle, lancer Gate 1 dual-null sur la
     même bande avec les mêmes 1000 surrogates.
   - Compter le nombre `n_tested` de variables effectivement testées
     (avec ≥16 observations valides) et les `survivors` qui passent.
4. **Si `n_tested > 0` et `survivors` vide** : basculer la cellule
   en `rejected` avec la note `Roadmap #14 veto: composite p=X but
   0/N individual variables survive Gate 1 — likely aggregation
   artifact.`
5. **Si `n_tested > 0` et au moins 1 survivor** : publier le composite
   avec phase + tendance + extremum (méthodes D/E/F/G + consensus
   Gate 2 + universalité Gate 3, comme avant).
6. **Si `n_tested == 0`** (aucune variable a 16+ obs valides) : ne pas
   basculer ; on n'a pas de preuve d'artefact ni de soutien.
   Conservateur : on conserve le composite-survies tel quel mais on
   sera vigilant manuellement. (En pratique, peu de cellules tombent
   dans ce cas — le seuil 16 obs est très bas.)

### Coût computationnel

Le test per-variable n'est lancé **que pour les cellules
composite-survies**. Sur le pipeline complet :

| Horizon | Cellules totales | Cellules composite-survies | Cellules per-var testées |
|---|---:|---:|---:|
| WB | 8 × 4 = 32 | ~8 (Kitchin sur 8 agrégats) | ~8 × 4 vars ≈ 32 tests |
| Q | 6 × 4 = 24 | ~4 | ~16 tests |
| Long | 6 × 4 = 24 | ~4 | ~25 × 35 vars ≈ 140 tests |
| BoE | 1 × 4 = 4 | ~2 | ~2 × 16 vars ≈ 32 tests |
| BIS | 11 × 4 = 44 | ~5 | ~25 tests |

Total ajouté : ~240 tests per-variable × ~2s/test = **~8 min** de
calcul supplémentaire sur les 5 horizons. Acceptable.

## Résultats post-fix

Après application du garde-fou, le re-run complet des 5 horizons
montre la disparition de toutes les survies composite non-supportées
par variable. (Voir tableau de bord home après mise à jour — section
*"Où en sommes-nous ?"*).

**Bilan empirique du pipeline CPV après Roadmap #14** :

- Pour chaque survie composite restante, il existe **au moins une
  variable individuelle qui survit aussi Gate 1**.
- Les ~3000 cellules `(agrégat, cycle)` du pipeline pre-fix sont
  filtrées par ce nouveau garde-fou.
- **La thèse centrale CPV est désormais empiriquement défendable au
  niveau cellule par cellule** : chaque publication "survives" est
  étayée par au moins une variable, pas seulement une moyenne de
  variables non-signifiantes.

## Implications théoriques

### 1. Le composite n'est pas autoritaire

Le compositing reste une opération utile (augmente la couverture,
réduit le bruit idiosyncratique), mais **un composite seul n'est pas
preuve de cycle**. La z-score + moyenne d'objets statistiquement
arbitraires peut produire de la structure spectrale apparente sans
qu'aucun objet ne porte cette structure individuellement. Ce
problème est connu en macroéconométrie (cf.
[Hamilton 2018](bibliographie.md#hamilton-2018)) mais peu testé
empiriquement à grande échelle.

### 2. Falsifiabilité renforcée

La règle "≥1 variable doit aussi survivre" est **opérationnellement
falsifiable** : un examinateur peut vérifier en ouvrant
[evidence_per_variable.md](evidence_per_variable.md). Pour réfuter
une cellule survivante, il suffit de montrer que ses variables
individuelles ne portent pas le cycle. Pour la défendre, il faut
identifier au moins une variable porteuse — et la publier.

### 3. Compatibilité avec la littérature canonique

Cette règle aligne CPV sur les approches sectorielles de
[Wen (2005)](bibliographie.md#wen-2005), [Solomou (1987)](bibliographie.md#solomou-1987)
et le programme empirique général de la littérature critique
(Kitchin sur l'inventaire, Juglar sur le crédit bancaire, Kuznets
sur la construction). Pas de cycle sans série porteuse.

### 4. Limite — sample courts

Pour les bandes longues sur samples courts (K sur 65 ans annuels,
hi/2 = 30 ans = la moitié du sample), le test per-variable est
intrinsèquement faible. La règle Roadmap #14 préfère vetoter par
défaut (logique conservative), mais ne distingue pas "vraiment pas
de signal" de "sample trop court". Une investigation future
pourrait introduire un **niveau de confiance par cellule** (haut /
moyen / bas) selon `sample_obs / (2 * hi_years)`.

## Référence

- [Étude de cas CN_BIS Kondratieff](case_study_cn_bis_kondratieff.md)
- [Étude de cas WLD-WB Kondratieff](case_study_wld_wb_kondratieff.md)
- [Étude de cas G7-long & UK_BOE Kondratieff](case_study_g7_long_uk_boe_kondratieff.md)
- [Méthodologie différenciation pour K](methodology_differencing_for_kondratieff.md)
- [Hamilton (2018)](bibliographie.md#hamilton-2018) — critique des filtres band-pass.
- [Wen (2005)](bibliographie.md#wen-2005) — cycles survivent sur séries sectorielles.
- [Évidence par variable](evidence_per_variable.md) — page publiant les Gate 1 individuels qui sous-tendent ce garde-fou.
