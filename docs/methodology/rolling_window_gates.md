# R5 — Rolling-window Gate 1

> **Résumé.** V3 (recommandation R5 du referee TSE) ajoute un test de
> stabilité temporelle : Gate 1 est appliqué sur **fenêtres
> glissantes 50 ans (200 ans pour Kondratieff)** avec step 25-40 ans,
> pour cartographier la **présence temporelle** des cycles. Cas V3
> majeur : la **heat-map Kondratieff localise la puissance maximale
> post-1815** (amortissement napoléonien) **et post-1945** (build-up
> WWII), windows que la lecture **Reinhart-Rogoff** anticipe.

## Pourquoi ce test

Gate 1 sur la fenêtre complète d'un panel teste la nulle « le cycle
est présent **en moyenne** sur la fenêtre ». Mais un cycle peut être
**présent par intermittence** plutôt que stationnaire — actif pendant
certaines périodes historiques et absent pendant d'autres.

Le rolling-window R5 transforme Gate 1 en cartographie temporelle :
pour chaque fenêtre glissante, on calcule le verdict Gate 1 et son
*p*-value. On en déduit :

- un **pass-rate temporel** (fraction de fenêtres qui rejettent le
  null) — modestement élevé au-dessus du nominal 5 % = présence
  intermittente ;
- une **heat-map** localisant les fenêtres les plus signifiantes —
  utile pour rattacher le signal à des chronologies historiques
  spécifiques.

## Protocole V3

| Cycle | Fenêtre | Step |
|---|---|---|
| Kitchin (3-5y) | 50y | 25y |
| Juglar (7-11y) | 50y | 25y |
| Kuznets (15-25y) | 80y | 40y |
| Kondratieff (40-60y) | 80-200y | 40y |

Pour chaque cellule (panel × group × variable) et chaque fenêtre, on
applique Gate 1 dual null (AR(1) + ARFIMA) avec le même surrogate
count que le run principal. Sortie : pass-rate temporel + heat-map
*p*-values.

## Résultats empiriques V3

Source : `papers/cycles_refuted/sections/05_results.tex`
§sec:appendix_rolling et `reports/rolling_window_gates.json`.

### Pass-rates BoE Millennium (80y window, 40y step, 1 646 cellules)

| Cycle | Pass / fenêtres | Pass-rate | Lecture |
|---|---|---|---|
| Juglar | 57 / 466 | **12.2 %** | excès modéré sur 5 % nominal |
| Kitchin | 40 / 466 | 8.6 % | léger excès |
| Kuznets | 39 / 430 | 9.1 % | léger excès |
| Kondratieff | **40 / 284** | **14.1 %** | excès clair |

Tous ces pass-rates sont **modestement élevés au-dessus du nominal
5 %**, cohérent avec **présence intermittente** plutôt que cyclicité
stationnaire sur 1700-2016. Aucun cycle n'est continûment présent ;
chacun apparaît et disparaît selon des régimes historiques.

### Heat-map Kondratieff BoE — chronologie Reinhart-Rogoff

Le pass-rate Kondratieff de 14.1 % se concentre sur deux régions
historiques :

- **Post-1815** — amortissement des dettes napoléoniennes (UK debt /
  GDP descend de ~250 % à ~25 % sur 1815-1914).
- **Post-1945** — build-up des dettes de la seconde guerre mondiale.

Ces deux windows sont **précisément** ce que la lecture
[Reinhart-Rogoff (2009)](../bibliographie.md#reinhart-rogoff-2009)
de chronologie de dette de guerre anticipe. Le rolling-window R5
confirme donc *à la fois* :

1. que le signal Kondratieff est **réel** (excès post-1815 / post-1945
   au-dessus du nominal 5 %), et
2. qu'il est **non-stationnaire** (intermittent, lié à des chocs
   exogènes spécifiques), donc **incompatible** avec la lecture
   endogène de [Kondratieff (1925)](../bibliographie.md#kondratieff-1925).

Voir [cycle Kondratieff — verdict V3](../cycles/kondratieff.md).

## Implémentation

Script : `scripts/rolling_window_gates.py`.

```bash
docker compose run --rm ecowave \
  scripts/rolling_window_gates.py --panels boe,jst \
  --window 80 --step 40 --n-surrogates 300 --seed 0
```

Sortie : `reports/rolling_window_gates.json` avec schéma
`{panel, group, variable, cycle, window_start, window_end, p1_AR1, p1_ARFIMA, pass: bool}`.

Cible Makefile : `referee-r5`. Run V3 documenté : 1 646 cellules sur
BoE, 80y window, 40y step.

## Voir aussi

- [Gate 1 dual null AR(1) + ARFIMA](arfima_dual_null.md)
- [Band-edge sensitivity R4](band_sensitivity.md)
- [Cycle Kondratieff — verdict V3 recast](../cycles/kondratieff.md)
- [Verdict V3 portail](../papers/cycles_refuted_v3.md)

## Références

- [Reinhart & Rogoff (2009)](../bibliographie.md#reinhart-rogoff-2009)
- [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998)
