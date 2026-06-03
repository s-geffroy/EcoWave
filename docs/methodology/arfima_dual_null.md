# Gate 1 dual null — AR(1) + ARFIMA(0, *d̂*, 0)

> **Résumé.** En V3 du papier *Cycles Refuted*, Gate 1 utilise un dual
> null : **AR(1) bootstrap** (primaire) et **ARFIMA(0, *d̂*<sub>GPH</sub>, 0)**
> (robustesse long-memory, recommandation R1 du referee TSE). L'AR(1)
> seul est mis-spécifié sur les niveaux bruts à mémoire longue
> (*97-100 %* des cellules JST R6 / BoE Millennium ont *|d̂|* > 0.1), donc
> la lecture **load-bearing** sur ces cellules est la lecture
> **ARFIMA-conditional**.

## Pourquoi un dual null

### Le problème avec l'AR(1) seul

L'AR(1) bootstrap est le null standard de Gate 1 depuis la V1
([Torrence & Compo 1998](../bibliographie.md#torrence-compo-1998) ;
[Grinsted *et al.* 2004](../bibliographie.md#grinsted-moore-jevrejeva-2004)).
Il modélise la persistance par un seul paramètre `φ ∈ (-1, 1)` et
suppose une décroissance exponentielle de l'ACF :
`ρ(k) = φ^k`.

Sur des séries macro à **mémoire longue**, l'ACF décroît plutôt comme
une loi de puissance : `ρ(k) ~ k^{2d-1}` pour `d ∈ (0, 0.5)`. L'AR(1)
ne peut pas capturer cette décroissance lente, et :

- soit fitte un `φ` proche de 1 et **sur-estime la persistance courte
  terme**, ce qui rend le null trop puissant et **augmente le risque
  de faux positifs Gate 1** (la puissance de bande empirique apparaît
  significativement supérieure au null AR(1) mal calibré) ;
- soit fitte un `φ` modéré et **manque la persistance long terme**,
  ce qui à l'inverse peut masquer un signal cyclique réel.

### Le problème avec le phase scrambling

Le phase scrambling
([Theiler *et al.* 1992](../bibliographie.md#theiler-et-al-1992))
préserve exactement le spectre de puissance et randomise les phases.
**Conséquence Parseval** : la puissance de bande de chaque surrogate
est strictement égale à celle de la série originale. Le null
phase-scramble est donc **dégénéré contre la puissance de bande**
— il ne peut jamais rejeter sur cette statistique. La V3 le rapporte
en diagnostic mais ne le laisse plus gater Gate 1.

### Pourquoi ARFIMA(0, *d̂*<sub>GPH</sub>, 0)

ARFIMA(0, *d*, 0) est le modèle canonique de mémoire longue
([Granger & Joyeux 1980](../bibliographie.md#granger-joyeux1980) ;
Hosking 1981 ; [Baillie 1996](../bibliographie.md#baillie1996)).
Le paramètre `d` capte la mémoire longue exacte : pour `d ∈ (0, 0.5)`,
le processus est stationnaire avec une ACF en loi de puissance ; pour
`d ∈ (0.5, 1)`, le processus est non-stationnaire mais d-différenciable
en quelque chose de stationnaire.

`d̂` est estimé par GPH sur la série brute, puis le simulateur Hosking
génère `B` trajectoires sous ARFIMA(0, *d̂*, 0). On recalcule la
puissance de bande CF et on rejette si la puissance empirique excède
le percentile `1 - α` du surrogate.

**Avantage clé** : ARFIMA capte la persistance long-terme que l'AR(1)
manque. Si la cellule passe les deux nulls, le signal de bande est
**robuste à la mis-spécification long-memory**. Si elle passe AR(1)
seulement, c'est un **faux positif probable** sous mémoire longue.

## Lecture load-bearing en V3

| Cellule | $p_{1,\mathrm{AR(1)}}$ | $p_{1,\mathrm{ARFIMA}}$ | $\hat d_{\mathrm{GPH}}$ | Verdict V3 |
|---|---|---|---|---|
| Passe AR(1), passe ARFIMA, $|\hat d| > 0.1$ | < α | < α | > 0.1 | ✅ Robuste long-mémoire |
| Passe AR(1), échoue ARFIMA, $|\hat d| > 0.1$ | < α | ≥ α | > 0.1 | ⚠️ Faux positif long-mémoire — déclassé |
| Passe AR(1), $|\hat d| < 0.1$ | < α | n/a | < 0.1 | ✅ Standard (AR(1) suffisant) |
| Échoue AR(1) | ≥ α | n/a | — | ❌ Rejet Gate 1 |

Sur BoE Millennium, **16 cellules** sont déclassées par cette lecture
ARFIMA-conditional. Sur les positifs robustes :

- **UK chômage (Juglar)** : $p_{1,\mathrm{AR(1)}} = 0.004$,
  $p_{1,\mathrm{ARFIMA}} = 0.002$ à $\hat d = 0.49$. La cellule
  load-bearing du verdict Juglar BoE.
- **UK dette publique (Kondratieff)** : $p_{1,\mathrm{AR(1)}} = 0.002$,
  $p_{1,\mathrm{ARFIMA}} = 0.022$ à $\hat d = +0.436$. Le seul
  positif Kondratieff (recasté Reinhart-Rogoff).
- **UK dette gouv. centrale (Kondratieff)** : $p_{1,\mathrm{AR(1)}} = 0.032$,
  $p_{1,\mathrm{ARFIMA}} = 0.048$ à $\hat d = +0.468$.
- **Real USD-GBP (Juglar)** : $p_{1,\mathrm{AR(1)}} = 0.006$,
  $p_{1,\mathrm{ARFIMA}} = 0.002$ à $\hat d = 0.428$.

## Implémentation

Module : `ecowave/cycles/surrogate.py` et
`ecowave/cycles/surrogate_generators.py`.

- `estimate_d_gph(series, m=None) -> d_hat` — estimateur GPH du
  paramètre `d`.
- `_hosking_coeffs(d, n) -> coeffs` — coefficients de l'expansion
  binomiale `(1 - L)^d`.
- `simulate_arfima(d, sigma, n, seed) -> series` — un tirage ARFIMA(0,d,0).
- `fit_arfima_d_sigma(series) -> (d_hat, sigma_hat)` — estimation
  conjointe pour le bootstrap.
- `arfima_surrogate_series(series, B, seed) -> array(B, n)` — `B`
  surrogates ARFIMA.
- `arfima_bootstrap_null(series, band, B) -> p_value` — Gate 1 sous
  ARFIMA.

Script CLI : `scripts/arfima_null_per_cell.py --panels boe` (et
`jst`, `wb`, `q`, `sh`). Sortie :
`reports/arfima_null_per_cell.json`. Cible Makefile : `referee-r1`.

## Voir aussi

- [Diagnostics par cellule (ADF/KPSS/GPH/DFA)](long_memory_diagnostics.md)
- [Trois portes V3](trois_portes.md)
- [Protocole CPV — étape 4](protocole_cpv.md)
- [Verdict V3 portail](../papers/cycles_refuted_v3.md)

## Références

- [Granger & Joyeux (1980)](../bibliographie.md#granger-joyeux1980)
- Hosking, J. R. M. (1981). Fractional differencing. *Biometrika*, 68(1), 165–176.
- [Baillie (1996)](../bibliographie.md#baillie1996)
- [Geweke & Porter-Hudak (1983)](../bibliographie.md#geweke-porter-hudak1983)
- [Theiler *et al.* (1992)](../bibliographie.md#theiler-et-al-1992) — phase scrambling (statut V3 : diagnostique)
- [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998)
