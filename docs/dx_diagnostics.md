# Diagnostics non-cycliques — Tier 1 du toolkit "au-delà des cycles"

> **Page générée par le pipeline.** Cette page est régénérée par
> `ecowave dx-diagnostics` (cf. [feuille de route
> #15](methodology/feuille_de_route.md#item-15-diagnostics-non-cycliques)).
> Le contenu ci-dessous est le placeholder statique avant le premier run —
> il sera remplacé par les heatmaps et tables réelles dès la première
> exécution du CLI.

## Préambule

Le pipeline CPV a rejeté les 4 cycles canoniques (Kitchin, Juglar, Kuznets,
Kondratieff) sur 100 % des cellules après les garde-fous Roadmap #14 — cf.
[Évidence par variable](evidence_per_variable.md). Cette défaite empirique
posée, la question devient : **si pas un cycle, quoi alors ?**

La page panoramique [Au-delà des cycles — cadres physiques
alternatifs](methodology_beyond_cycles.md) recense 21 familles candidates.
**La présente page implémente le Tier 1 — 11 diagnostics couvrant 11 des
21 familles**, plus la famille G (RMT) au niveau panel.

## Familles couvertes

| Famille | Diagnostic | Statistique |
|---|---|---|
| A — SOC (1/f^β) | `spectrum_slope` | β (slope log-log du PSD) |
| A — queues de loi de puissance | `hill_tail_exponent` | α_Hill |
| B — Multifractalité | `mfdfa_spectrum` | Δα (largeur spectre f(α)) |
| C — Longue mémoire | `hurst_dfa` | H (Peng et al. 1994) |
| E — Critical slowing down | `critical_slowdown` | Kendall τ rolling variance |
| G — RMT | `rmt_panel` | modes > λ_max Marchenko-Pastur |
| I — Information | `permutation_entropy_complexity` | H_perm + C_stat |
| J — Lévy flights | `levy_stable_fit` | α (McCulloch 1986) |
| P — Cascades K41 | `k41_scaling` | ζ(6)/ζ(3) |
| R — Diffusion anormale | `msd_log_log` | γ (slope MSD) |
| S — Réflexivité (transversal) | `reflexivity_drift` | KS deux-échantillons |
| T — Non-extensivité Tsallis | `tsallis_q_gaussian` | q (indice entropique) |

Chaque diagnostic est scoré contre un null AR(1) ou phase-scramble
(Theiler 1992) à α = 0.05, reproduisant la philosophie Gate 1 du protocole
CPV sur le terrain non-cyclique.

## Lecture transversale — réflexivité (famille S)

Conformément à PR #22, la famille S — **réflexivité** (Soros 1987 ;
Friston 2010 ; Akerlof-Shiller 2009) — est traitée comme **composante
transversale obligatoire**. Le diagnostic `reflexivity_drift` (KS
deux-échantillons entre les deux moitiés de chaque série) sert
d'**indicateur de validité** des 10 autres : quand il rejette le null,
les statistiques structurelles (Hurst, β, Δα, …) sont valables
**uniquement sur la fenêtre analysée**, pas comme lois universelles
transhistoriques.

## Lancer le pipeline

```bash
docker compose run --rm --entrypoint ecowave ecowave \
  dx-diagnostics --as-of 2026-05 --horizons wb,q,long,boe,bis,sh \
  --n-surrogates 200
```

Sorties :

- `reports/dx_diagnostics_2026_05_{horizon}.json` — résultats per-variable
- `reports/dx_rmt_2026_05_{horizon}.json` — résultats panel-level RMT
- `docs/dx_diagnostics.md` — cette page (regénérée avec les heatmaps)
