# Diagnostics par cellule — long memory + stationarity (V3)

> **Résumé.** En V3 (recommandation R1 du referee TSE), chaque cellule
> reçoit quatre diagnostics par cellule : ADF, KPSS, GPH *d̂*, DFA
> Hurst *Ĥ*. Conclusion empirique : **97–100 %** des cellules JST R6 /
> BoE Millennium ont *|d̂|* > 0.1 ; **81–83 %** ne rejettent pas
> l'unit-root ADF ; **77–89 %** rejettent la stationnarité KPSS. Le
> null AR(1) sur la série brute est donc structurellement
> mis-spécifié — la lecture load-bearing est l'ARFIMA-conditional
> ([détail](arfima_dual_null.md)).

## Les quatre diagnostics

### ADF — Augmented Dickey-Fuller (1979)

Test de la nulle « la série a une racine unitaire » contre
l'alternative « la série est stationnaire » ([Dickey & Fuller 1979](../bibliographie.md#dickey_fuller1979)). Un *non-rejet* ADF
indique que la série est compatible avec un I(1) ; un *rejet* indique
qu'elle est compatible avec un I(0) après détrend déterministe.

### KPSS — Kwiatkowski-Phillips-Schmidt-Shin (1992)

Test de la nulle inverse (« la série est stationnaire ») contre
l'alternative racine unitaire ([KPSS 1992](../bibliographie.md#kpss1992)). Conventionnellement
rapporté en complément de l'ADF :

| ADF | KPSS | Lecture |
|---|---|---|
| Rejet | Non-rejet | Stationnaire (I(0)) |
| Non-rejet | Rejet | Unit-root (I(1)) |
| Rejet | Rejet | Long-mémoire ou rupture structurelle |
| Non-rejet | Non-rejet | Sample size insuffisante / indéterminé |

### GPH *d̂* — Geweke-Porter-Hudak (1983)

Estimateur du paramètre de différenciation fractionnaire `d` par
régression log-périodogramme aux basses fréquences ([Geweke &
Porter-Hudak 1983](../bibliographie.md#geweke-porter-hudak1983)).
Critère cellule long-memory en V3 : `|d̂| > 0.1`. `d̂ ∈ (0, 0.5)` →
long-mémoire stationnaire ; `d̂ ∈ (0.5, 1)` → quasi-non-stationnaire ;
`d̂ ≈ 1` → unit-root.

### DFA Hurst *Ĥ* — Peng et al. (1994)

*Detrended Fluctuation Analysis*. Estimateur du paramètre de Hurst
résistant aux trends non-stationnaires ([Peng *et al.* 1994](../bibliographie.md#peng-1994)). Lien : `Ĥ = d̂ + 0.5` en
approximation. `Ĥ = 0.5` → random walk ; `Ĥ > 0.5` → long-mémoire
persistante ; `Ĥ > 1` → quasi-non-stationnaire.

## Résultats empiriques V3

Source : `papers/cycles_refuted/sections/{05_results,07_conclusion}.tex`
et `reports/long_memory_diagnostics.json`.

### JST R6 (1870–2020, 611 cellules)

| Statistique | Valeur |
|---|---|
| Cellules avec `|d̂| > 0.1` | **97 %** |
| Cellules avec `|d̂| > 0.4` | 88 % |
| Médiane *Ĥ* | **1.76** |
| Cellules où ADF ne rejette pas unit-root | 81 % |
| Cellules où KPSS rejette stationnarité | 77 % |

### BoE Millennium (1700–2016, 65 cellules)

| Statistique | Valeur |
|---|---|
| Cellules avec `|d̂| > 0.1` | **100 %** |
| Cellules avec `|d̂| > 0.4` | 95 % |
| Médiane *Ĥ* | **1.64** |
| Cellules où ADF ne rejette pas unit-root | 83 % |
| Cellules où KPSS rejette stationnarité | 89 % |

### Conclusion empirique

Le null AR(1) sur les **niveaux bruts** est mis-spécifié sur la
majorité écrasante des cellules JST R6 et BoE Millennium. Conséquence
opérationnelle :

1. La cellule reçoit en V3 le flag `long_memory = True` si `|d̂| > 0.1`.
2. Pour ces cellules, Gate 1 exige le rejet sous le null
   ARFIMA(0, *d̂*, 0) en plus de AR(1) — la lecture load-bearing est
   l'ARFIMA-conditional ([détail](arfima_dual_null.md)).
3. Sur BoE, **16 cellules** passent AR(1) seul mais échouent ARFIMA
   et sont déclassées comme **faux positifs long-mémoire**.

## Implémentation

Module : `ecowave/cycles/surrogate.py:stationarity_diagnostics`.

Script CLI : `scripts/long_memory_diagnostics.py --panel jst,boe` (et
`wb`, `q`, `sh`). Sortie : `reports/long_memory_diagnostics.json` avec
schéma `{cell_id, ADF_p, KPSS_p, d_gph, H_dfa, long_memory: bool}`.

Cible Makefile : `referee-r1`.

## Voir aussi

- [Gate 1 dual null AR(1) + ARFIMA](arfima_dual_null.md)
- [Trois portes V3](trois_portes.md)
- [Verdict V3 portail](../papers/cycles_refuted_v3.md)

## Références

- [Dickey & Fuller (1979)](../bibliographie.md#dickey_fuller1979)
- [Kwiatkowski, Phillips, Schmidt & Shin (1992)](../bibliographie.md#kpss1992)
- [Geweke & Porter-Hudak (1983)](../bibliographie.md#geweke-porter-hudak1983)
- [Peng et al. (1994)](../bibliographie.md#peng-1994)
- Hurst, H. E. (1951). Long-term storage capacity of reservoirs.
  *Transactions of the American Society of Civil Engineers*, 116, 770–799.
