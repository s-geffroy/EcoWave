# Diagnostics non-cycliques — au-delà des cycles, structure statistique du panel

> **Pourquoi cette page existe.** Le pipeline CPV a rejeté les 4 cycles canoniques (Kitchin, Juglar, Kuznets, Kondratieff) sur 100 % des cellules après les garde-fous Roadmap #14 — cf. [Évidence par variable](evidence_per_variable.md). Cette défaite empirique posée, la question devient : **si pas un cycle, quoi alors ?** La page panoramique [Au-delà des cycles — cadres physiques alternatifs](methodology_beyond_cycles.md) recense 21 familles ; **la présente page implémente le Tier 1 — 10 diagnostics couvrant 10 des 21 familles**, plus une famille de panel-level (G — RMT). Chaque diagnostic est scoré contre un null AR(1) ou phase-scramble pour reproduire la philosophie Gate 1 sur le terrain non-cyclique.

**Lecture de l'encart 🟢🟡🟠🔴.** 🟢 = p ≤ 0.01 (diagnostic rejette le null avec haute confiance) · 🟡 = 0.01 < p ≤ 0.05 (rejet standard CPV) · 🟠 = 0.05 < p ≤ 0.10 (marginal) · 🔴 = p > 0.10 (compatible avec le null). Statistique = valeur observée du diagnostic ; on en tire l'orientation de la famille physique.

!!! note "Pas de découpage 4-cycles dans cette page"
    Par construction, les diagnostics Tier 1 mesurent des propriétés **structurelles globales** de chaque série (Hurst, multifractalité, slope 1/f, entropie, ralentissement critique, queues lourdes, ζ(p) de turbulence, diffusion anormale, non-extensivité Tsallis). Réintroduire un axe `cycle ∈ {kitchin, juglar, kuznets, kondratieff}` reviendrait à recréer le scaffold cyclique précisément falsifié. Pour la lecture cyclique, voir les pages Gate 1.

## Synthèse cross-horizon

Pour chaque diagnostic, taux de rejet du null sur l'ensemble (variable × groupe × horizon). Le bloc Tier 1 (11 diagnostics) couvre les familles A, B, C, E, G, I, J, P, R, S, T du panorama ; Tier 2 ajoute D (Lyapunov + BDS) et une variante multi-régime de S.

| Diagnostic | Famille | Taux de rejet null | n cellules | Références |
|---|---|---:|---:|---|
| `hurst_dfa` | C — longue mémoire | 51% | 674 | Peng et al. 1994; Hurst 1951; Mandelbrot-Van Ness 1968 |
| `mfdfa_spectrum` | B — multifractalité | 27% | 674 | Kantelhardt et al. 2002; Bacry-Muzy-Delour 2001 |
| `spectrum_slope` | A — SOC (1/f^β) | 15% | 674 | Bak-Tang-Wiesenfeld 1987; Bak 1996 |
| `hill_tail_exponent` | A — queues de loi de puissance | 41% | 674 | Hill 1975; Mantegna-Stanley 1999 |
| `permutation_entropy_complexity` | I — information | 69% | 674 | Bandt-Pompe 2002; López-Ruiz-Mancini-Calbet 1995 |
| `critical_slowdown` | E — tipping point | 30% | 674 | Scheffer et al. 2009; Dakos et al. 2008 |
| `levy_stable_fit` | J — vols de Lévy | 32% | 674 | McCulloch 1986; Mantegna-Stanley 1999 |
| `k41_scaling` | P — cascades K41 | 36% | 674 | Kolmogorov 1941; Frisch 1995; Ghashghaie et al. 1996 |
| `msd_log_log` | R — diffusion anormale | 42% | 674 | Metzler-Klafter 2000; Mantegna-Stanley 1999 |
| `tsallis_q_gaussian` | T — non-extensivité | 43% | 674 | Tsallis 1988; Tsallis 2009 |
| `reflexivity_drift` | S — réflexivité (transversal) | 51% | 674 | Soros 1987; Akerlof-Shiller 2009; Friston 2010 |
| `lyapunov_exponent` | D — chaos déterministe (Tier 2) | 19% | 674 | Rosenstein-Collins-De Luca 1993; Wolf et al. 1985 |
| `bds_independence` | D — non-linéarité IID (Tier 2) | 88% | 674 | Brock-Dechert-Scheinkman 1996 |
| `reflexivity_multi_window` | S — réflexivité multi-régime (Tier 2) | 30% | 674 | Soros 1987; Akerlof-Shiller 2009; Friston 2010 |

## Panel Banque mondiale (1960-2024)

### BRICS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.57 | 🔴 1.14 | 🔴 1.73 | 🟡 3.44 | 🟢 0.73 | 🔴 0.11 | 🔴 1.78 | 🟡 1.59 | 🔴 1.17 | 🔴 0.91 | 🟡 0.94 | 🔴 0.04 | 🟢 3.42 | — — |
| `CY_GDP` | 🔴 0.82 | 🔴 0.63 | 🔴 0.70 | 🟡 2.23 | 🔴 0.99 | 🔴 -0.42 | 🟢 1.14 | 🔴 2.90 | 🔴 0.18 | 🟢 1.58 | 🔴 0.25 | 🔴 0.03 | 🟡 0.61 | — — |
| `CY_INF` | 🟢 1.55 | 🟡 1.78 | 🔴 1.13 | 🟢 0.73 | 🔴 0.99 | 🔴 0.30 | 🟢 0.50 | 🔴 1.45 | 🔴 0.48 | 🟢 1.76 | 🟠 0.48 | 🟢 0.12 | 🟢 2.28 | — — |
| `CY_INV` | 🔴 1.42 | 🔴 0.51 | 🟢 2.32 | 🔴 8.41 | 🟠 0.91 | 🔴 0.49 | 🔴 2.00 | 🟢 0.85 | 🔴 0.86 | 🔴 0.77 | 🔴 0.70 | 🔴 0.08 | 🟢 2.91 | — — |
| `CY_POP` | 🟠 1.75 | 🟠 1.48 | 🔴 1.81 | 🔴 9.60 | 🟢 0.69 | 🔴 -0.81 | 🔴 2.00 | 🟢 1.19 | 🟢 1.46 | 🔴 0.61 | 🔴 0.88 | 🔴 0.02 | 🟢 3.51 | — — |
| `CY_PRD` | 🟠 1.69 | 🟢 2.59 | 🔴 1.63 | 🔴 14.28 | 🟢 0.73 | 🔴 -0.36 | 🟠 1.35 | 🔴 1.87 | 🟠 1.38 | 🔴 0.85 | 🔴 0.53 | 🟠 0.08 | 🟢 3.27 | — — |
| `CY_TRD` | 🔴 1.63 | 🟢 2.73 | 🔴 1.85 | 🔴 9.08 | 🔴 0.92 | 🔴 0.14 | 🔴 2.00 | 🟢 0.99 | 🔴 0.91 | 🔴 0.60 | 🟢 1.00 | 🔴 0.05 | 🟡 2.93 | — — |
| `CY_UEM` | 🔴 1.55 | — — | 🔴 1.79 | 🔴 3.28 | 🔴 0.87 | — — | 🔴 2.00 | — — | — — | 🔴 0.82 | 🔴 0.88 | — — | 🟢 1.93 | — — |

### BRICS:ARE

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.88 | — — | 🔴 0.92 | 🟢 1.91 | 🔴 0.99 | — — | 🟢 0.50 | — — | — — | 🟢 1.74 | 🔴 0.37 | — — | 🟢 0.91 | — — |
| `CY_POP` | 🟢 2.11 | 🔴 0.75 | 🔴 1.58 | 🔴 4.34 | 🟢 0.43 | 🔴 0.21 | 🔴 2.00 | 🔴 1.99 | 🟢 1.67 | 🔴 0.83 | 🔴 0.39 | 🟢 0.13 | 🟢 3.45 | — — |
| `CY_PRD` | 🔴 1.35 | — — | 🟡 2.38 | 🔴 3.94 | 🔴 0.92 | — — | 🟠 1.53 | — — | — — | 🔴 0.93 | 🟠 0.85 | — — | 🟡 2.86 | — — |
| `CY_UEM` | 🟠 1.74 | — — | 🔴 1.20 | 🔴 3.12 | 🟡 0.84 | — — | 🔴 2.00 | — — | — — | 🟡 1.29 | 🔴 0.30 | — — | 🟢 1.55 | — — |

### BRICS:BRA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.27 | — — | 🔴 1.13 | 🟠 2.99 | 🟢 0.82 | 🔴 -0.22 | 🔴 2.00 | — — | — — | 🟢 1.39 | 🔴 0.40 | — — | 🟢 2.65 | — — |
| `CY_GDP` | 🔴 1.12 | 🔴 0.34 | 🔴 0.93 | 🔴 6.54 | 🔴 1.00 | 🔴 -0.83 | 🟠 1.71 | 🔴 1.96 | 🔴 0.27 | 🔴 0.96 | 🟠 0.44 | 🔴 0.03 | 🔴 0.57 | — — |
| `CY_INF` | 🟡 1.47 | — — | 🔴 0.96 | 🟢 0.91 | 🔴 0.95 | — — | 🟢 0.50 | — — | — — | 🟢 1.65 | 🟡 0.73 | — — | 🟢 1.43 | — — |
| `CY_INV` | 🔴 1.18 | 🔴 0.65 | 🔴 1.45 | 🔴 4.11 | 🔴 0.97 | 🔴 -0.27 | 🔴 2.00 | 🟠 1.57 | 🔴 0.46 | 🔴 0.89 | 🔴 0.51 | 🔴 0.07 | 🔴 1.08 | — — |
| `CY_POP` | 🟢 2.12 | 🔴 0.67 | 🔴 1.78 | 🔴 6.18 | 🟢 -0.00 | 🔴 -1.00 | 🔴 2.00 | 🔴 1.97 | 🟢 2.01 | 🔴 0.70 | 🟡 1.00 | 🔴 -0.02 | 🟢 3.93 | — — |
| `CY_PRD` | 🟠 1.75 | 🟡 1.83 | 🔴 1.70 | 🔴 10.14 | 🟢 0.76 | 🔴 -0.13 | 🔴 2.00 | 🔴 2.01 | 🟢 1.54 | 🔴 0.75 | 🟠 0.91 | 🔴 0.04 | 🟢 3.70 | — — |
| `CY_TRD` | 🔴 1.33 | 🔴 0.50 | 🔴 1.63 | 🟡 2.59 | 🟠 0.91 | 🔴 0.61 | 🔴 2.00 | 🔴 1.89 | 🔴 0.68 | 🔴 0.97 | 🔴 0.73 | 🔴 0.07 | 🟢 2.48 | — — |
| `CY_UEM` | 🔴 1.85 | — — | 🔴 2.01 | 🔴 3.53 | 🔴 0.89 | — — | 🔴 2.00 | — — | — — | 🔴 0.68 | 🔴 0.33 | — — | 🔴 1.31 | — — |

### BRICS:CHN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟠 1.76 | — — | 🔴 1.76 | 🔴 4.84 | 🟢 0.80 | — — | 🔴 1.85 | — — | — — | 🔴 0.81 | 🔴 0.88 | — — | 🟢 2.92 | — — |
| `CY_GDP` | 🔴 0.77 | 🟢 2.15 | 🔴 0.90 | 🟠 2.77 | 🟡 0.94 | 🔴 -0.83 | 🟢 0.50 | 🔴 2.84 | 🔴 0.09 | 🟢 1.73 | 🔴 0.22 | 🔴 0.04 | 🟢 1.02 | — — |
| `CY_INF` | 🔴 0.74 | — — | 🟢 2.20 | 🟡 1.63 | 🔴 0.98 | — — | 🟢 1.02 | — — | — — | 🟢 1.39 | 🔴 0.42 | — — | 🟢 1.54 | — — |
| `CY_INV` | 🔴 1.47 | 🟠 1.71 | 🟡 2.05 | 🔴 3.30 | 🟡 0.90 | 🔴 -0.15 | 🔴 1.84 | 🟢 0.10 | 🔴 0.51 | 🟠 1.12 | 🟠 0.76 | 🔴 0.04 | 🟢 2.39 | — — |
| `CY_POP` | 🟢 2.08 | 🔴 0.55 | 🔴 1.86 | 🔴 5.74 | 🟢 0.48 | 🟡 0.98 | 🔴 2.00 | 🔴 1.91 | 🟢 1.96 | 🔴 0.66 | 🟡 1.00 | 🔴 0.09 | 🟢 3.89 | — — |
| `CY_PRD` | 🟢 1.95 | 🔴 0.13 | 🔴 1.75 | 🟡 2.87 | 🟢 0.27 | 🟢 1.00 | 🔴 1.94 | 🔴 1.92 | 🟢 1.87 | 🔴 1.08 | 🟡 1.00 | 🔴 0.09 | 🟢 3.93 | — — |
| `CY_TRD` | 🟡 1.80 | 🟢 3.34 | 🔴 1.91 | 🔴 4.60 | 🔴 0.91 | 🔴 0.23 | 🔴 2.00 | 🟠 1.76 | 🔴 1.24 | 🔴 0.70 | 🟡 1.00 | 🔴 0.06 | 🟡 3.09 | — — |
| `CY_UEM` | 🟠 1.90 | — — | 🔴 1.94 | 🔴 2.99 | 🟡 0.81 | — — | 🔴 2.00 | — — | — — | 🔴 0.84 | 🟠 0.83 | — — | 🟢 2.56 | — — |

### BRICS:EGY

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟡 1.80 | 🔴 0.36 | 🟡 2.14 | 🟠 3.55 | 🟠 0.89 | 🔴 0.32 | 🔴 1.74 | 🟡 1.76 | 🟡 1.33 | 🔴 0.94 | 🔴 0.69 | 🔴 0.04 | 🔴 2.99 | — — |
| `CY_GDP` | 🔴 1.05 | 🟡 1.36 | 🔴 0.69 | 🔴 3.02 | 🔴 0.98 | 🔴 -0.89 | 🟢 1.27 | 🔴 2.78 | 🔴 0.18 | 🟡 1.21 | 🔴 0.31 | 🔴 0.03 | 🟡 0.67 | — — |
| `CY_INF` | 🔴 0.95 | 🔴 1.10 | 🔴 1.21 | 🟡 2.67 | 🔴 0.94 | 🔴 -0.37 | 🔴 2.00 | 🟡 1.25 | 🔴 0.43 | 🟠 1.15 | 🔴 0.22 | 🔴 0.05 | 🟢 1.23 | — — |
| `CY_INV` | 🔴 1.23 | 🟠 1.92 | 🔴 1.85 | 🔴 5.92 | 🟡 0.91 | 🔴 -0.92 | 🟠 1.46 | 🔴 1.95 | 🔴 0.96 | 🔴 0.89 | 🔴 0.50 | 🔴 0.02 | 🟡 2.34 | — — |
| `CY_POP` | 🟢 2.06 | 🔴 0.38 | 🔴 1.64 | 🟢 1.42 | 🟢 0.52 | 🔴 -0.88 | 🟢 1.09 | 🔴 2.01 | 🟢 1.58 | 🟢 1.53 | 🔴 0.59 | 🔴 0.04 | 🟢 3.61 | — — |
| `CY_PRD` | 🟢 1.99 | 🔴 0.40 | 🔴 1.76 | 🟠 4.52 | 🟢 0.38 | 🟠 0.85 | 🔴 2.00 | 🔴 1.84 | 🟢 1.81 | 🔴 0.64 | 🟡 1.00 | 🔴 0.05 | 🟢 3.78 | — — |
| `CY_TRD` | 🔴 1.44 | 🔴 0.88 | 🟡 2.17 | 🔴 3.94 | 🟢 0.84 | 🔴 -0.57 | 🔴 2.00 | 🔴 1.83 | 🔴 0.73 | 🔴 0.90 | 🔴 0.22 | 🔴 0.06 | 🟠 1.79 | — — |
| `CY_UEM` | 🟡 2.43 | — — | 🔴 2.02 | 🔴 8.54 | 🔴 0.90 | — — | 🔴 2.00 | — — | — — | 🔴 0.69 | 🔴 0.39 | — — | 🔴 1.32 | — — |

### BRICS:ETH

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.72 | — — | 🔴 1.99 | 🔴 11.62 | 🟡 0.86 | — — | 🔴 2.00 | — — | — — | 🔴 0.79 | 🔴 0.56 | — — | 🟢 3.19 | — — |
| `CY_GDP` | 🔴 0.74 | — — | 🔴 0.83 | 🔴 3.17 | 🔴 0.98 | 🔴 0.22 | 🔴 1.92 | — — | — — | 🟠 1.17 | 🟢 0.62 | — — | 🟢 0.90 | — — |
| `CY_INF` | 🔴 0.99 | — — | 🔴 0.45 | 🔴 4.90 | 🔴 0.98 | — — | 🟡 1.41 | — — | — — | 🟠 1.16 | 🔴 0.29 | — — | 🟢 0.70 | — — |
| `CY_INV` | 🟠 1.82 | — — | 🟠 2.19 | 🔴 5.13 | 🟢 0.54 | — — | 🔴 2.00 | — — | — — | 🔴 0.67 | 🔴 0.64 | — — | 🟢 3.02 | — — |
| `CY_POP` | 🟢 2.06 | 🔴 0.15 | 🔴 1.73 | 🟠 4.40 | 🟢 0.09 | 🟡 0.97 | 🔴 2.00 | 🔴 1.91 | 🟢 1.91 | 🔴 0.73 | 🟡 1.00 | 🔴 0.03 | 🟢 3.88 | — — |
| `CY_PRD` | 🟡 1.85 | 🔴 0.94 | 🔴 1.72 | 🟢 2.49 | 🟢 0.75 | 🟢 0.94 | 🟢 0.50 | 🔴 2.04 | 🟢 1.77 | 🟡 1.23 | 🔴 0.59 | 🟢 0.15 | 🟢 3.84 | — — |
| `CY_UEM` | 🔴 1.73 | — — | 🟠 2.27 | 🔴 5.10 | 🟢 0.80 | — — | 🔴 2.00 | — — | — — | 🔴 0.65 | 🔴 0.43 | — — | 🟡 1.86 | — — |

### BRICS:IDN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🟢 1.23 | 🟢 1.77 | 🟢 1.23 | 🟢 2.00 | 🟡 0.94 | 🔴 -0.08 | 🟡 1.40 | 🔴 1.74 | 🔴 0.13 | 🟢 1.76 | 🟡 0.47 | 🔴 0.03 | 🟡 0.65 | — — |
| `CY_INF` | 🟢 1.36 | 🟢 1.80 | 🔴 0.57 | 🟢 0.90 | 🔴 0.98 | 🔴 -0.35 | 🟢 0.50 | 🟢 -8.95 | 🟡 -0.08 | 🟢 1.92 | 🟢 0.51 | 🔴 -0.04 | 🟢 1.26 | — — |
| `CY_INV` | 🔴 1.58 | 🔴 0.50 | 🔴 1.64 | 🔴 3.52 | 🔴 0.94 | 🔴 -0.48 | 🔴 1.98 | 🟡 1.65 | 🔴 1.11 | 🔴 0.86 | 🔴 0.69 | 🔴 0.04 | 🟢 3.01 | — — |
| `CY_POP` | 🟢 2.11 | 🔴 0.35 | 🔴 1.79 | 🔴 8.35 | 🟢 -0.00 | 🔴 0.27 | 🔴 2.00 | 🔴 1.98 | 🟢 2.05 | 🔴 0.41 | 🟡 1.00 | 🔴 0.03 | 🟢 3.87 | — — |
| `CY_PRD` | 🟡 1.79 | 🟡 1.81 | 🔴 1.73 | 🟡 3.83 | 🟢 0.49 | 🟠 0.85 | 🔴 2.00 | 🔴 1.81 | 🟢 1.75 | 🔴 0.83 | 🟡 1.00 | 🔴 0.06 | 🟢 3.83 | — — |
| `CY_TRD` | 🔴 1.29 | 🔴 0.74 | 🔴 0.91 | 🟠 3.05 | 🔴 0.98 | 🔴 0.01 | 🔴 1.67 | 🟡 0.94 | 🔴 0.61 | 🟢 1.30 | 🔴 0.38 | 🔴 0.03 | 🟢 2.15 | — — |
| `CY_UEM` | 🔴 1.77 | — — | 🟠 2.39 | 🔴 2.75 | 🔴 0.89 | — — | 🔴 2.00 | — — | — — | 🔴 0.73 | 🔴 0.54 | — — | 🔴 1.85 | — — |

### BRICS:IND

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟢 2.11 | 🟢 2.80 | 🔴 1.71 | 🔴 4.87 | 🟢 0.81 | 🔴 0.39 | 🔴 2.00 | 🟢 1.25 | 🟡 1.37 | 🔴 0.70 | 🔴 0.76 | 🟠 0.11 | 🟢 3.45 | — — |
| `CY_GDP` | 🔴 0.46 | 🟠 1.10 | 🔴 -0.29 | 🟠 2.33 | 🔴 0.99 | 🔴 -0.62 | 🔴 1.87 | 🔴 2.33 | 🔴 -0.07 | 🟢 1.36 | 🟢 0.44 | 🔴 0.03 | 🔴 0.03 | — — |
| `CY_INF` | 🟠 1.06 | 🟢 2.17 | 🔴 0.62 | 🟡 2.42 | 🔴 0.99 | 🔴 -0.79 | 🔴 2.00 | 🟡 -4.61 | 🔴 0.06 | 🟢 1.57 | 🔴 0.25 | 🔴 0.04 | 🟢 0.77 | — — |
| `CY_INV` | 🔴 1.40 | 🔴 0.29 | 🔴 1.63 | 🔴 3.59 | 🔴 0.97 | 🔴 0.47 | 🔴 2.00 | 🔴 2.01 | 🔴 0.89 | 🔴 0.72 | 🟠 0.82 | 🔴 0.08 | 🟠 2.38 | — — |
| `CY_POP` | 🟢 2.09 | 🔴 0.52 | 🔴 1.76 | 🔴 13.49 | 🟢 -0.00 | 🔴 0.08 | 🔴 2.00 | 🔴 1.97 | 🟢 2.00 | 🔴 0.63 | 🟡 1.00 | 🔴 0.02 | 🟢 3.83 | — — |
| `CY_PRD` | 🟡 1.84 | 🔴 0.59 | 🔴 1.69 | 🟡 3.33 | 🟢 0.54 | 🟢 1.00 | 🔴 2.00 | 🔴 1.89 | 🟢 1.68 | 🔴 1.06 | 🟡 1.00 | 🔴 0.07 | 🟢 3.94 | — — |
| `CY_TRD` | 🔴 1.65 | 🔴 0.68 | 🔴 1.89 | 🟡 4.10 | 🟡 0.87 | 🔴 0.71 | 🔴 2.00 | 🔴 1.93 | 🔴 1.26 | 🔴 0.58 | 🟡 1.00 | 🔴 0.06 | 🟢 3.61 | — — |
| `CY_UEM` | 🔴 1.65 | — — | 🔴 1.92 | 🟢 1.00 | 🔴 0.93 | — — | 🟡 0.50 | — — | — — | 🟡 1.44 | 🔴 0.33 | — — | 🟢 1.85 | — — |

### BRICS:IRN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.49 | — — | 🔴 1.60 | 🟠 3.71 | 🟠 0.91 | — — | 🔴 1.61 | — — | — — | 🔴 0.98 | 🔴 0.61 | — — | 🟢 3.17 | — — |
| `CY_GDP` | 🔴 0.81 | 🔴 0.73 | 🔴 1.11 | 🟠 2.90 | 🔴 1.00 | 🔴 -0.95 | 🟠 1.63 | 🔴 1.63 | 🔴 0.28 | 🟡 1.21 | 🟠 0.44 | 🔴 0.02 | 🟢 0.85 | — — |
| `CY_INF` | 🔴 0.95 | 🟢 2.78 | 🔴 1.57 | 🔴 3.01 | 🔴 0.96 | 🔴 0.11 | 🔴 1.74 | 🔴 1.93 | 🔴 0.35 | 🔴 1.00 | 🔴 0.47 | 🔴 0.07 | 🟡 1.21 | — — |
| `CY_INV` | 🟠 1.36 | 🔴 0.18 | 🔴 1.21 | 🔴 7.26 | 🔴 0.95 | 🔴 -0.84 | 🟠 1.61 | 🔴 1.53 | 🔴 0.42 | 🔴 0.90 | 🔴 0.38 | 🔴 0.05 | 🟢 1.09 | — — |
| `CY_POP` | 🟢 2.14 | 🔴 0.25 | 🔴 1.77 | 🔴 9.03 | 🟢 -0.00 | 🔴 -1.00 | 🔴 2.00 | 🔴 1.96 | 🟢 2.01 | 🔴 0.56 | 🟡 1.00 | 🔴 -0.01 | 🟢 3.87 | — — |
| `CY_PRD` | 🟡 1.91 | 🔴 1.12 | 🔴 1.78 | 🔴 4.93 | 🟢 0.74 | 🔴 -0.70 | 🔴 2.00 | 🔴 1.80 | 🟡 1.29 | 🔴 0.86 | 🔴 0.38 | 🔴 0.08 | 🟢 2.99 | — — |
| `CY_TRD` | 🟠 1.62 | 🔴 0.19 | 🟡 2.04 | 🟡 2.11 | 🟡 0.89 | 🔴 -0.75 | 🔴 1.73 | 🔴 1.80 | 🔴 0.88 | 🟡 1.22 | 🔴 0.44 | 🔴 0.06 | 🟢 2.07 | — — |
| `CY_UEM` | 🔴 1.54 | — — | 🔴 1.90 | 🔴 3.35 | 🟢 0.80 | — — | 🔴 2.00 | — — | — — | 🔴 0.86 | 🔴 0.27 | — — | 🔴 0.96 | — — |

### BRICS:RUS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.94 | — — | 🔴 1.36 | 🔴 2.55 | 🔴 0.96 | — — | 🔴 2.00 | — — | — — | 🔴 1.02 | 🔴 0.42 | — — | 🔴 0.56 | — — |
| `CY_INF` | 🔴 1.30 | — — | 🔴 0.62 | 🟢 1.43 | 🔴 0.94 | — — | 🟢 0.50 | — — | — — | 🟢 1.83 | 🟢 0.81 | — — | 🟢 2.02 | — — |
| `CY_INV` | 🔴 1.38 | — — | 🔴 1.44 | 🟢 1.34 | 🔴 0.96 | — — | 🟢 1.04 | — — | — — | 🟡 1.25 | 🔴 0.34 | — — | 🟢 1.48 | — — |
| `CY_POP` | 🟢 2.09 | 🔴 0.13 | 🔴 1.73 | 🟡 2.99 | 🟢 0.40 | 🔴 -0.81 | 🔴 1.54 | 🔴 2.00 | 🟢 1.88 | 🟠 1.09 | 🔴 0.88 | 🔴 -0.01 | 🟢 3.95 | — — |
| `CY_PRD` | 🟠 1.95 | — — | 🟠 2.31 | 🔴 5.25 | 🟠 0.84 | — — | 🔴 2.00 | — — | — — | 🔴 0.52 | 🟠 1.00 | — — | 🟢 2.37 | — — |
| `CY_TRD` | 🔴 0.92 | — — | 🔴 0.33 | 🟢 1.47 | 🟡 0.91 | — — | 🟠 1.39 | — — | — — | 🟢 1.69 | 🟢 0.67 | — — | 🟢 1.60 | — — |
| `CY_UEM` | 🔴 1.82 | — — | 🟠 2.30 | 🟠 2.23 | 🟡 0.84 | — — | 🔴 1.46 | — — | — — | 🔴 1.04 | 🔴 0.66 | — — | 🟡 1.79 | — — |

### BRICS:ZAF

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.39 | — — | 🔴 2.11 | 🔴 8.83 | 🟡 0.89 | — — | 🔴 2.00 | — — | — — | 🔴 0.36 | 🔴 0.90 | — — | 🟢 3.10 | — — |
| `CY_GDP` | 🔴 0.88 | 🔴 0.85 | 🔴 0.98 | 🔴 4.03 | 🔴 0.98 | 🔴 -0.56 | 🔴 2.00 | 🟢 -20.87 | 🔴 0.17 | 🟠 1.16 | 🔴 0.34 | 🔴 0.04 | 🟠 0.46 | — — |
| `CY_INF` | 🔴 1.28 | 🔴 0.20 | 🟡 1.99 | 🔴 4.94 | 🔴 0.94 | 🔴 -0.45 | 🔴 2.00 | 🟡 1.63 | 🔴 0.89 | 🔴 0.76 | 🔴 0.53 | 🔴 0.05 | 🔴 2.12 | — — |
| `CY_INV` | 🔴 1.36 | 🔴 0.71 | 🔴 1.54 | 🔴 5.74 | 🔴 0.95 | 🔴 -0.38 | 🔴 2.00 | 🟡 1.69 | 🔴 0.85 | 🔴 0.89 | 🟠 0.81 | 🔴 0.06 | 🟠 2.36 | — — |
| `CY_POP` | 🟢 2.15 | 🟠 1.52 | 🔴 1.82 | 🔴 47.13 | 🟢 -0.00 | 🔴 0.64 | 🔴 2.00 | 🔴 1.97 | 🟢 2.00 | 🔴 0.38 | 🟡 1.00 | 🔴 0.04 | 🟢 3.83 | — — |
| `CY_PRD` | 🟢 1.94 | 🔴 0.84 | 🔴 1.83 | 🔴 17.03 | 🟢 0.81 | 🟠 0.72 | 🔴 2.00 | 🔴 1.75 | 🟢 1.47 | 🔴 0.63 | 🔴 0.58 | 🟡 0.11 | 🟢 3.12 | — — |
| `CY_TRD` | 🔴 1.30 | 🔴 0.78 | 🔴 1.78 | 🔴 3.64 | 🟡 0.89 | 🟠 0.75 | 🔴 2.00 | 🟢 1.19 | 🔴 0.69 | 🔴 0.92 | 🔴 0.48 | 🔴 0.07 | 🟢 2.06 | — — |
| `CY_UEM` | 🟠 2.01 | — — | 🔴 1.91 | 🟡 1.56 | 🔴 0.91 | — — | 🔴 1.88 | — — | — — | 🔴 1.07 | 🔴 0.94 | — — | 🟢 2.70 | — — |

### G20

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟠 1.77 | 🔴 0.95 | 🔴 1.67 | 🔴 8.94 | 🟢 0.79 | 🔴 -0.41 | 🔴 2.00 | 🟠 1.70 | 🟠 1.31 | 🔴 0.48 | 🟡 0.97 | 🔴 0.08 | 🟢 3.57 | — — |
| `CY_GDP` | 🔴 0.67 | 🔴 0.58 | 🟡 0.82 | 🔴 2.93 | 🔴 1.00 | 🔴 -0.33 | 🟡 1.38 | 🔴 3.77 | 🔴 -0.05 | 🟢 1.33 | 🟡 0.44 | 🔴 0.02 | 🟢 0.55 | — — |
| `CY_INF` | 🟡 1.42 | 🔴 0.99 | 🔴 1.25 | 🟢 0.95 | 🟢 0.87 | 🔴 0.44 | 🟢 0.50 | 🔴 1.46 | 🔴 0.44 | 🟢 1.73 | 🟡 0.51 | 🟢 0.18 | 🟢 1.73 | — — |
| `CY_INV` | 🔴 1.31 | 🔴 0.48 | 🟡 2.03 | 🔴 3.64 | 🟢 0.87 | 🔴 0.15 | 🔴 2.00 | 🟢 1.27 | 🔴 0.60 | 🔴 0.92 | 🔴 0.20 | 🔴 0.05 | 🟢 1.68 | — — |
| `CY_POP` | 🟢 2.03 | 🔴 0.25 | 🔴 1.64 | 🟢 2.48 | 🟢 0.57 | 🔴 -1.00 | 🔴 2.00 | 🔴 1.79 | 🟢 1.66 | 🔴 0.87 | 🟢 1.00 | 🔴 0.01 | 🟢 3.83 | — — |
| `CY_PRD` | 🟢 2.11 | 🔴 1.02 | 🔴 1.70 | 🔴 5.55 | 🟢 0.50 | 🔴 -0.62 | 🔴 2.00 | 🔴 1.81 | 🟢 1.62 | 🔴 0.60 | 🟡 1.00 | 🔴 0.02 | 🟢 3.73 | — — |
| `CY_TRD` | 🔴 1.44 | 🔴 1.35 | 🔴 1.67 | 🔴 15.41 | 🟠 0.90 | 🔴 0.33 | 🔴 2.00 | 🟡 1.60 | 🔴 1.03 | 🔴 0.57 | 🟠 0.88 | 🔴 0.08 | 🟢 3.21 | — — |
| `CY_UEM` | 🔴 0.76 | — — | 🔴 1.83 | 🟢 1.54 | 🟢 0.71 | — — | 🔴 1.58 | — — | — — | 🔴 0.97 | 🔴 0.47 | — — | 🟢 1.32 | — — |

### G20:ARG

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.29 | 🔴 1.22 | 🔴 1.19 | 🟡 2.24 | 🔴 0.95 | 🔴 -0.53 | 🔴 2.00 | 🟢 -0.67 | 🔴 0.47 | 🟢 1.40 | 🔴 0.34 | 🔴 0.06 | 🟢 2.02 | — — |
| `CY_GDP` | 🔴 0.67 | 🔴 0.23 | 🔴 -0.38 | 🔴 6.16 | 🔴 0.99 | 🔴 0.56 | 🔴 2.00 | 🔴 -1.66 | 🔴 0.06 | 🔴 0.76 | 🔴 0.16 | 🟡 0.06 | 🔴 0.24 | — — |
| `CY_INV` | 🔴 1.25 | 🔴 0.48 | 🔴 1.52 | 🟠 2.64 | 🟠 0.92 | 🔴 -0.55 | 🟠 1.47 | 🔴 1.79 | 🔴 0.59 | 🟠 1.13 | 🟠 0.66 | 🔴 0.04 | 🔴 1.68 | — — |
| `CY_POP` | 🟢 2.17 | 🔴 0.40 | 🔴 1.74 | 🟡 3.02 | 🟢 -0.00 | 🔴 -1.00 | 🔴 2.00 | 🔴 1.99 | 🟢 1.90 | 🔴 0.82 | 🟡 1.00 | 🔴 -0.03 | 🟢 3.94 | — — |
| `CY_PRD` | 🔴 1.58 | 🔴 0.92 | 🔴 1.69 | 🔴 10.20 | 🔴 0.94 | 🔴 0.59 | 🔴 2.00 | 🔴 2.18 | 🔴 0.97 | 🔴 0.69 | 🔴 0.82 | 🔴 0.07 | 🟢 2.97 | — — |
| `CY_TRD` | 🔴 1.43 | 🔴 1.43 | 🔴 1.85 | 🟠 3.13 | 🔴 0.98 | 🔴 0.46 | 🔴 2.00 | 🟢 1.02 | 🔴 0.91 | 🔴 0.76 | 🟠 0.91 | 🔴 0.07 | 🟢 3.12 | — — |
| `CY_UEM` | 🔴 1.55 | — — | 🔴 2.13 | 🔴 2.97 | 🟡 0.86 | — — | 🔴 2.00 | — — | — — | 🔴 0.88 | 🔴 0.77 | — — | 🟡 1.67 | — — |

### G20:AUS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟢 1.95 | 🟡 1.88 | 🔴 1.87 | 🔴 7.06 | 🟢 0.73 | 🔴 0.53 | 🔴 2.00 | 🟠 1.72 | 🟢 1.73 | 🔴 0.40 | 🟡 1.00 | 🔴 0.06 | 🟢 3.70 | — — |
| `CY_GDP` | 🔴 0.63 | 🔴 0.69 | 🔴 0.43 | 🔴 4.10 | 🔴 0.96 | 🔴 -0.89 | 🟢 1.32 | 🟡 -0.22 | 🔴 0.10 | 🟠 1.20 | 🔴 0.28 | 🔴 0.02 | 🟠 0.35 | — — |
| `CY_INF` | 🔴 1.24 | 🔴 1.08 | 🟡 1.91 | 🟠 2.47 | 🔴 0.96 | 🔴 -0.70 | 🔴 1.88 | 🔴 1.85 | 🔴 0.76 | 🟡 1.15 | 🔴 0.60 | 🔴 0.07 | 🟡 2.02 | — — |
| `CY_INV` | 🔴 1.15 | 🔴 0.88 | 🔴 1.59 | 🔴 8.53 | 🔴 0.96 | 🔴 -0.82 | 🔴 1.62 | 🟡 1.48 | 🔴 0.61 | 🔴 0.85 | 🟠 0.69 | 🔴 0.02 | 🟢 1.91 | — — |
| `CY_POP` | 🟢 2.16 | 🔴 1.07 | 🔴 1.50 | 🟡 2.79 | 🟢 0.56 | 🔴 0.05 | 🟢 0.50 | 🔴 1.91 | 🟢 1.67 | 🟢 1.25 | 🔴 0.52 | 🟢 0.11 | 🟢 3.90 | — — |
| `CY_PRD` | 🟢 2.09 | 🔴 0.47 | 🔴 1.81 | 🔴 16.45 | 🟢 0.47 | 🔴 0.56 | 🔴 2.00 | 🔴 1.97 | 🟢 1.86 | 🔴 0.49 | 🟡 0.97 | 🔴 0.01 | 🟢 3.80 | — — |
| `CY_TRD` | 🔴 1.15 | 🔴 0.93 | 🔴 1.66 | 🔴 7.28 | 🔴 0.94 | 🔴 0.01 | 🔴 2.00 | 🟠 1.55 | 🔴 0.80 | 🔴 0.49 | 🟡 1.00 | 🔴 0.04 | 🟢 3.11 | — — |
| `CY_UEM` | 🔴 1.56 | — — | 🔴 2.08 | 🔴 3.20 | 🟢 0.81 | — — | 🟠 1.31 | — — | — — | 🔴 1.04 | 🔴 0.65 | — — | 🟢 2.03 | — — |

### G20:BRA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.27 | — — | 🔴 1.13 | 🟠 2.99 | 🟢 0.82 | 🔴 -0.22 | 🔴 2.00 | — — | — — | 🟢 1.39 | 🔴 0.40 | — — | 🟢 2.65 | — — |
| `CY_GDP` | 🔴 1.12 | 🔴 0.34 | 🔴 0.93 | 🔴 6.54 | 🔴 1.00 | 🔴 -0.83 | 🟠 1.71 | 🔴 1.96 | 🔴 0.27 | 🔴 0.96 | 🟠 0.44 | 🔴 0.03 | 🔴 0.57 | — — |
| `CY_INF` | 🟡 1.47 | — — | 🔴 0.96 | 🟢 0.91 | 🔴 0.95 | — — | 🟢 0.50 | — — | — — | 🟢 1.65 | 🟡 0.73 | — — | 🟢 1.43 | — — |
| `CY_INV` | 🔴 1.18 | 🔴 0.65 | 🔴 1.45 | 🔴 4.11 | 🔴 0.97 | 🔴 -0.27 | 🔴 2.00 | 🟠 1.57 | 🔴 0.46 | 🔴 0.89 | 🔴 0.51 | 🔴 0.07 | 🔴 1.08 | — — |
| `CY_POP` | 🟢 2.12 | 🔴 0.67 | 🔴 1.78 | 🔴 6.18 | 🟢 -0.00 | 🔴 -1.00 | 🔴 2.00 | 🔴 1.97 | 🟢 2.01 | 🔴 0.70 | 🟡 1.00 | 🔴 -0.02 | 🟢 3.93 | — — |
| `CY_PRD` | 🟠 1.75 | 🟡 1.83 | 🔴 1.70 | 🔴 10.14 | 🟢 0.76 | 🔴 -0.13 | 🔴 2.00 | 🔴 2.01 | 🟢 1.54 | 🔴 0.75 | 🟠 0.91 | 🔴 0.04 | 🟢 3.70 | — — |
| `CY_TRD` | 🔴 1.33 | 🔴 0.50 | 🔴 1.63 | 🟡 2.59 | 🟠 0.91 | 🔴 0.61 | 🔴 2.00 | 🔴 1.89 | 🔴 0.68 | 🔴 0.97 | 🔴 0.73 | 🔴 0.07 | 🟢 2.48 | — — |
| `CY_UEM` | 🔴 1.85 | — — | 🔴 2.01 | 🔴 3.53 | 🔴 0.89 | — — | 🔴 2.00 | — — | — — | 🔴 0.68 | 🔴 0.33 | — — | 🔴 1.31 | — — |

### G20:CAN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟢 2.32 | — — | 🔴 1.81 | 🔴 4.51 | 🟢 0.69 | — — | 🔴 1.69 | — — | — — | 🔴 0.86 | 🔴 0.88 | — — | 🟢 3.16 | — — |
| `CY_GDP` | 🔴 0.78 | 🔴 0.69 | 🟢 1.10 | 🟡 2.50 | 🔴 0.99 | 🔴 -0.50 | 🟢 1.39 | 🔴 5.60 | 🔴 0.03 | 🟢 1.32 | 🟡 0.41 | 🔴 0.04 | 🔴 0.22 | — — |
| `CY_INF` | 🔴 1.32 | 🔴 0.52 | 🔴 1.76 | 🟢 2.01 | 🔴 0.97 | 🔴 -0.61 | 🟡 1.35 | 🔴 1.67 | 🔴 0.79 | 🟡 1.19 | 🟠 0.69 | 🟠 0.09 | 🟡 2.20 | — — |
| `CY_INV` | 🔴 1.32 | 🔴 0.30 | 🔴 1.40 | 🔴 4.90 | 🟡 0.92 | 🔴 -0.29 | 🔴 2.00 | 🟡 1.03 | 🔴 0.58 | 🔴 0.84 | 🔴 0.19 | 🔴 0.07 | 🟡 1.66 | — — |
| `CY_POP` | 🟢 2.15 | 🟠 1.67 | 🔴 1.64 | 🟠 3.59 | 🟢 0.22 | 🔴 0.35 | 🔴 2.00 | 🔴 2.06 | 🟢 1.58 | 🔴 0.96 | 🟡 1.00 | 🔴 0.01 | 🟢 3.84 | — — |
| `CY_PRD` | 🟢 1.96 | 🔴 0.11 | 🔴 1.83 | 🔴 6.53 | 🟢 0.54 | 🔴 0.03 | 🔴 2.00 | 🟠 1.73 | 🟢 1.60 | 🔴 0.56 | 🟠 0.91 | 🔴 0.00 | 🟢 3.69 | — — |
| `CY_TRD` | 🔴 1.50 | 🔴 0.26 | 🔴 1.68 | 🔴 8.89 | 🟠 0.92 | 🔴 -0.12 | 🔴 2.00 | 🔴 2.03 | 🟡 1.24 | 🔴 0.66 | 🟢 1.00 | 🔴 0.04 | 🟢 3.11 | — — |
| `CY_UEM` | 🔴 1.01 | — — | 🔴 1.83 | 🔴 3.55 | 🟢 0.84 | — — | 🔴 1.60 | — — | — — | 🔴 0.95 | 🔴 0.43 | — — | 🟢 1.53 | — — |

### G20:CHN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟠 1.76 | — — | 🔴 1.76 | 🔴 4.84 | 🟢 0.80 | — — | 🔴 1.85 | — — | — — | 🔴 0.81 | 🔴 0.88 | — — | 🟢 2.92 | — — |
| `CY_GDP` | 🔴 0.77 | 🟢 2.15 | 🔴 0.90 | 🟠 2.77 | 🟡 0.94 | 🔴 -0.83 | 🟢 0.50 | 🔴 2.84 | 🔴 0.09 | 🟢 1.73 | 🔴 0.22 | 🔴 0.04 | 🟢 1.02 | — — |
| `CY_INF` | 🔴 0.74 | — — | 🟢 2.20 | 🟡 1.63 | 🔴 0.98 | — — | 🟢 1.02 | — — | — — | 🟢 1.39 | 🔴 0.42 | — — | 🟢 1.54 | — — |
| `CY_INV` | 🔴 1.47 | 🟠 1.71 | 🟡 2.05 | 🔴 3.30 | 🟡 0.90 | 🔴 -0.15 | 🔴 1.84 | 🟢 0.10 | 🔴 0.51 | 🟠 1.12 | 🟠 0.76 | 🔴 0.04 | 🟢 2.39 | — — |
| `CY_POP` | 🟢 2.08 | 🔴 0.55 | 🔴 1.86 | 🔴 5.74 | 🟢 0.48 | 🟡 0.98 | 🔴 2.00 | 🔴 1.91 | 🟢 1.96 | 🔴 0.66 | 🟡 1.00 | 🔴 0.09 | 🟢 3.89 | — — |
| `CY_PRD` | 🟢 1.95 | 🔴 0.13 | 🔴 1.75 | 🟡 2.87 | 🟢 0.27 | 🟢 1.00 | 🔴 1.94 | 🔴 1.92 | 🟢 1.87 | 🔴 1.08 | 🟡 1.00 | 🔴 0.09 | 🟢 3.93 | — — |
| `CY_TRD` | 🟡 1.80 | 🟢 3.34 | 🔴 1.91 | 🔴 4.60 | 🔴 0.91 | 🔴 0.23 | 🔴 2.00 | 🟠 1.76 | 🔴 1.24 | 🔴 0.70 | 🟡 1.00 | 🔴 0.06 | 🟡 3.09 | — — |
| `CY_UEM` | 🟠 1.90 | — — | 🔴 1.94 | 🔴 2.99 | 🟡 0.81 | — — | 🔴 2.00 | — — | — — | 🔴 0.84 | 🟠 0.83 | — — | 🟢 2.56 | — — |

### G20:DEU

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.68 | 🔴 0.64 | 🔴 0.43 | 🔴 2.86 | 🟢 0.90 | 🔴 0.12 | 🔴 2.00 | 🔴 3.45 | 🔴 -0.03 | 🟡 1.25 | 🟡 0.47 | 🔴 0.03 | 🟢 0.47 | — — |
| `CY_INF` | 🔴 1.19 | 🔴 0.70 | 🟡 1.85 | 🔴 4.06 | 🟡 0.90 | 🔴 -0.59 | 🔴 1.61 | 🔴 1.49 | 🔴 0.42 | 🔴 0.96 | 🔴 0.51 | 🔴 0.05 | 🟠 1.38 | — — |
| `CY_INV` | 🔴 1.46 | — — | 🔴 1.61 | 🟠 2.62 | 🔴 0.95 | — — | 🔴 1.77 | — — | — — | 🟡 1.17 | 🟡 0.86 | — — | 🟢 2.46 | — — |
| `CY_POP` | 🟢 2.15 | 🔴 1.41 | 🔴 1.41 | 🟡 2.34 | 🟢 -0.00 | 🔴 0.02 | 🟢 0.50 | 🔴 2.07 | 🟢 1.41 | 🟢 1.50 | 🟢 1.00 | 🔴 0.00 | 🟢 3.92 | — — |
| `CY_PRD` | 🟢 2.03 | 🔴 0.85 | 🔴 1.81 | 🔴 12.90 | 🟢 0.56 | 🔴 -0.83 | 🔴 2.00 | 🟡 1.68 | 🟢 1.69 | 🔴 0.55 | 🟡 0.97 | 🔴 0.00 | 🟢 3.64 | — — |
| `CY_TRD` | 🔴 1.49 | — — | 🔴 2.00 | 🔴 10.22 | 🟡 0.87 | — — | 🔴 2.00 | — — | — — | 🔴 0.44 | 🟡 1.00 | — — | 🟢 3.14 | — — |
| `CY_UEM` | 🟡 2.17 | — — | 🟢 2.88 | 🔴 8.19 | 🟡 0.80 | — — | 🔴 2.00 | — — | — — | 🔴 0.50 | 🔴 0.83 | — — | 🔴 1.99 | — — |

### G20:FRA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.71 | 🟡 1.37 | 🔴 0.46 | 🔴 3.61 | 🔴 0.98 | 🔴 -0.14 | 🔴 2.00 | 🔴 3.52 | 🔴 -0.02 | 🟢 1.47 | 🟡 0.56 | 🔴 0.04 | 🟢 1.60 | — — |
| `CY_INF` | 🔴 1.40 | 🔴 0.60 | 🔴 1.83 | 🟠 3.04 | 🟠 0.92 | 🔴 -0.45 | 🟠 1.46 | 🟠 1.66 | 🔴 0.95 | 🟠 1.14 | 🟡 0.91 | 🔴 0.06 | 🟠 2.42 | — — |
| `CY_INV` | 🔴 1.33 | 🔴 0.18 | 🔴 1.71 | 🔴 8.35 | 🔴 0.95 | 🔴 -0.76 | 🔴 2.00 | 🟢 1.43 | 🔴 0.82 | 🔴 0.73 | 🔴 0.78 | 🔴 0.05 | 🟠 2.46 | — — |
| `CY_POP` | 🟢 2.27 | 🟠 1.96 | 🔴 1.67 | 🟢 1.70 | 🟢 0.24 | 🔴 -0.41 | 🟡 1.38 | 🔴 2.02 | 🟢 1.59 | 🟢 1.26 | 🟡 1.00 | 🔴 0.00 | 🟢 3.88 | — — |
| `CY_PRD` | 🟢 1.99 | 🔴 0.10 | 🔴 1.75 | 🔴 5.74 | 🟢 0.40 | 🔴 -0.74 | 🔴 2.00 | 🟡 1.47 | 🟢 1.67 | 🔴 0.61 | 🟡 1.00 | 🔴 -0.01 | 🟢 3.81 | — — |
| `CY_TRD` | 🔴 1.52 | 🟠 1.54 | 🔴 1.85 | 🔴 11.45 | 🟢 0.84 | 🔴 0.16 | 🔴 2.00 | 🟢 1.17 | 🔴 0.96 | 🔴 0.74 | 🔴 0.85 | 🔴 0.05 | 🟢 3.09 | — — |
| `CY_UEM` | 🔴 1.50 | — — | 🟠 2.36 | 🔴 4.99 | 🔴 0.89 | — — | 🔴 1.74 | — — | — — | 🔴 0.79 | 🔴 0.42 | — — | 🟠 1.56 | — — |

### G20:GBR

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟡 1.79 | 🟠 1.78 | 🟡 2.06 | 🔴 4.90 | 🟢 0.79 | 🔴 0.04 | 🔴 2.00 | 🟢 1.60 | 🟡 1.39 | 🔴 0.51 | 🟠 0.91 | 🔴 0.09 | 🟢 3.44 | — — |
| `CY_GDP` | 🔴 0.65 | 🟡 1.71 | 🔴 -0.06 | 🟡 2.15 | 🔴 0.99 | 🔴 -0.11 | 🟢 1.28 | 🔴 3.80 | 🔴 -0.09 | 🟢 1.62 | 🔴 0.16 | 🔴 0.05 | 🟡 0.47 | — — |
| `CY_INF` | 🔴 1.26 | 🔴 0.84 | 🔴 1.58 | 🟢 1.22 | 🟡 0.92 | 🔴 -0.64 | 🟡 1.28 | 🔴 2.04 | 🔴 0.70 | 🟢 1.49 | 🟡 0.75 | 🔴 0.04 | 🟡 2.19 | — — |
| `CY_INV` | 🔴 1.26 | — — | 🔴 1.88 | 🔴 4.68 | 🔴 0.97 | — — | 🔴 2.00 | — — | — — | 🔴 0.87 | 🟡 0.89 | — — | 🟢 2.46 | — — |
| `CY_POP` | 🟢 2.06 | 🔴 0.14 | 🔴 1.94 | 🟡 3.77 | 🟢 0.46 | 🟡 0.94 | 🔴 2.00 | 🔴 1.98 | 🟢 1.77 | 🔴 0.75 | 🟡 0.91 | 🔴 0.08 | 🟢 3.71 | — — |
| `CY_PRD` | 🟢 1.96 | 🔴 0.49 | 🔴 1.80 | 🔴 22.31 | 🟢 0.51 | 🔴 0.23 | 🔴 2.00 | 🟢 1.41 | 🟢 1.54 | 🔴 0.39 | 🟡 0.97 | 🔴 0.02 | 🟢 3.77 | — — |
| `CY_TRD` | 🔴 1.17 | — — | 🔴 1.70 | 🔴 4.50 | 🔴 0.94 | — — | 🔴 2.00 | — — | — — | 🔴 0.87 | 🔴 0.50 | — — | 🟢 1.69 | — — |
| `CY_UEM` | 🔴 1.35 | — — | 🔴 2.16 | 🔴 3.41 | 🟡 0.83 | — — | 🔴 2.00 | — — | — — | 🔴 0.74 | 🔴 0.39 | — — | 🟢 1.87 | — — |

### G20:IDN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🟢 1.23 | 🟢 1.77 | 🟢 1.23 | 🟢 2.00 | 🟡 0.94 | 🔴 -0.08 | 🟡 1.40 | 🔴 1.74 | 🔴 0.13 | 🟢 1.76 | 🟡 0.47 | 🔴 0.03 | 🟡 0.65 | — — |
| `CY_INF` | 🟢 1.36 | 🟢 1.80 | 🔴 0.57 | 🟢 0.90 | 🔴 0.98 | 🔴 -0.35 | 🟢 0.50 | 🟢 -8.95 | 🟡 -0.08 | 🟢 1.92 | 🟢 0.51 | 🔴 -0.04 | 🟢 1.26 | — — |
| `CY_INV` | 🔴 1.58 | 🔴 0.50 | 🔴 1.64 | 🔴 3.52 | 🔴 0.94 | 🔴 -0.48 | 🔴 1.98 | 🟡 1.65 | 🔴 1.11 | 🔴 0.86 | 🔴 0.69 | 🔴 0.04 | 🟢 3.01 | — — |
| `CY_POP` | 🟢 2.11 | 🔴 0.35 | 🔴 1.79 | 🔴 8.35 | 🟢 -0.00 | 🔴 0.27 | 🔴 2.00 | 🔴 1.98 | 🟢 2.05 | 🔴 0.41 | 🟡 1.00 | 🔴 0.03 | 🟢 3.87 | — — |
| `CY_PRD` | 🟡 1.79 | 🟡 1.81 | 🔴 1.73 | 🟡 3.83 | 🟢 0.49 | 🟠 0.85 | 🔴 2.00 | 🔴 1.81 | 🟢 1.75 | 🔴 0.83 | 🟡 1.00 | 🔴 0.06 | 🟢 3.83 | — — |
| `CY_TRD` | 🔴 1.29 | 🔴 0.74 | 🔴 0.91 | 🟠 3.05 | 🔴 0.98 | 🔴 0.01 | 🔴 1.67 | 🟡 0.94 | 🔴 0.61 | 🟢 1.30 | 🔴 0.38 | 🔴 0.03 | 🟢 2.15 | — — |
| `CY_UEM` | 🔴 1.77 | — — | 🟠 2.39 | 🔴 2.75 | 🔴 0.89 | — — | 🔴 2.00 | — — | — — | 🔴 0.73 | 🔴 0.54 | — — | 🔴 1.85 | — — |

### G20:IND

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟢 2.11 | 🟢 2.80 | 🔴 1.71 | 🔴 4.87 | 🟢 0.81 | 🔴 0.39 | 🔴 2.00 | 🟢 1.25 | 🟡 1.37 | 🔴 0.70 | 🔴 0.76 | 🟠 0.11 | 🟢 3.45 | — — |
| `CY_GDP` | 🔴 0.46 | 🟠 1.10 | 🔴 -0.29 | 🟠 2.33 | 🔴 0.99 | 🔴 -0.62 | 🔴 1.87 | 🔴 2.33 | 🔴 -0.07 | 🟢 1.36 | 🟢 0.44 | 🔴 0.03 | 🔴 0.03 | — — |
| `CY_INF` | 🟠 1.06 | 🟢 2.17 | 🔴 0.62 | 🟡 2.42 | 🔴 0.99 | 🔴 -0.79 | 🔴 2.00 | 🟡 -4.61 | 🔴 0.06 | 🟢 1.57 | 🔴 0.25 | 🔴 0.04 | 🟢 0.77 | — — |
| `CY_INV` | 🔴 1.40 | 🔴 0.29 | 🔴 1.63 | 🔴 3.59 | 🔴 0.97 | 🔴 0.47 | 🔴 2.00 | 🔴 2.01 | 🔴 0.89 | 🔴 0.72 | 🟠 0.82 | 🔴 0.08 | 🟠 2.38 | — — |
| `CY_POP` | 🟢 2.09 | 🔴 0.52 | 🔴 1.76 | 🔴 13.49 | 🟢 -0.00 | 🔴 0.08 | 🔴 2.00 | 🔴 1.97 | 🟢 2.00 | 🔴 0.63 | 🟡 1.00 | 🔴 0.02 | 🟢 3.83 | — — |
| `CY_PRD` | 🟡 1.84 | 🔴 0.59 | 🔴 1.69 | 🟡 3.33 | 🟢 0.54 | 🟢 1.00 | 🔴 2.00 | 🔴 1.89 | 🟢 1.68 | 🔴 1.06 | 🟡 1.00 | 🔴 0.07 | 🟢 3.94 | — — |
| `CY_TRD` | 🔴 1.65 | 🔴 0.68 | 🔴 1.89 | 🟡 4.10 | 🟡 0.87 | 🔴 0.71 | 🔴 2.00 | 🔴 1.93 | 🔴 1.26 | 🔴 0.58 | 🟡 1.00 | 🔴 0.06 | 🟢 3.61 | — — |
| `CY_UEM` | 🔴 1.65 | — — | 🔴 1.92 | 🟢 1.00 | 🔴 0.93 | — — | 🟡 0.50 | — — | — — | 🟡 1.44 | 🔴 0.33 | — — | 🟢 1.85 | — — |

### G20:ITA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.61 | 🟠 1.25 | 🔴 0.43 | 🔴 2.96 | 🟢 0.90 | 🔴 -0.12 | 🟡 1.45 | 🔴 3.81 | 🟠 -0.06 | 🟢 1.33 | 🟢 0.62 | 🔴 0.04 | 🟢 1.18 | — — |
| `CY_INF` | 🔴 1.34 | 🔴 1.79 | 🟠 2.02 | 🔴 3.77 | 🔴 0.94 | 🔴 -0.67 | 🟡 1.18 | 🟠 1.73 | 🔴 0.92 | 🟡 1.16 | 🔴 0.66 | 🔴 0.05 | 🟠 2.43 | — — |
| `CY_INV` | 🔴 1.05 | — — | 🔴 1.49 | 🔴 5.16 | 🔴 0.96 | — — | 🔴 1.86 | — — | — — | 🔴 1.03 | 🟡 0.71 | — — | 🟡 1.85 | — — |
| `CY_POP` | 🟢 2.17 | 🟠 1.90 | 🔴 1.66 | 🟢 1.84 | 🟢 0.46 | 🔴 -0.09 | 🟢 0.50 | 🔴 2.03 | 🟢 1.73 | 🟡 1.21 | 🟠 0.85 | 🔴 0.03 | 🟢 3.90 | — — |
| `CY_PRD` | 🟢 2.05 | 🔴 0.13 | 🔴 1.72 | 🔴 4.63 | 🟢 0.49 | 🔴 -0.97 | 🔴 2.00 | 🟡 1.45 | 🟢 1.58 | 🔴 0.65 | 🟡 0.97 | 🔴 0.00 | 🟢 3.79 | — — |
| `CY_TRD` | 🔴 1.46 | — — | 🔴 1.78 | 🔴 3.54 | 🔴 0.93 | — — | 🔴 2.00 | — — | — — | 🔴 0.91 | 🟡 0.93 | — — | 🟢 2.41 | — — |
| `CY_UEM` | 🟡 2.10 | — — | 🔴 1.46 | 🔴 4.71 | 🟢 0.76 | — — | 🔴 2.00 | — — | — — | 🔴 0.59 | 🔴 0.21 | — — | 🟡 1.61 | — — |

### G20:JPN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟠 1.85 | — — | 🔴 1.68 | 🔴 8.27 | 🟢 0.85 | — — | 🔴 2.00 | — — | — — | 🔴 0.68 | 🔴 0.63 | — — | 🟢 2.90 | — — |
| `CY_GDP` | 🔴 0.82 | 🟠 1.32 | 🔴 0.85 | 🟡 2.46 | 🔴 0.98 | 🔴 -0.63 | 🟡 1.43 | 🟢 -0.87 | 🔴 0.16 | 🟠 1.10 | 🟢 0.84 | 🔴 0.02 | 🟢 1.57 | — — |
| `CY_INF` | 🔴 1.18 | 🔴 1.23 | 🔴 1.53 | 🟢 1.82 | 🟡 0.92 | 🔴 -0.62 | 🔴 2.00 | 🔴 1.90 | 🔴 0.45 | 🟢 1.69 | 🟢 0.79 | 🔴 0.06 | 🟢 2.51 | — — |
| `CY_INV` | 🔴 1.73 | — — | 🔴 1.63 | 🟡 2.63 | 🟠 0.89 | — — | 🔴 2.00 | — — | — — | 🔴 0.83 | 🟡 0.96 | — — | 🟢 3.05 | — — |
| `CY_POP` | 🟢 2.12 | 🔴 0.73 | 🔴 1.74 | 🔴 8.22 | 🟢 -0.00 | 🔴 0.49 | 🔴 2.00 | 🔴 1.91 | 🟢 1.82 | 🔴 0.68 | 🟡 1.00 | 🔴 -0.01 | 🟢 3.78 | — — |
| `CY_PRD` | 🟢 2.10 | 🔴 0.27 | 🔴 1.76 | 🟠 3.60 | 🟢 0.57 | 🔴 -0.93 | 🔴 2.00 | 🔴 1.91 | 🟢 1.73 | 🔴 0.62 | 🟡 0.97 | 🔴 0.01 | 🟢 3.83 | — — |
| `CY_TRD` | 🔴 1.41 | — — | 🔴 1.61 | 🟠 3.02 | 🟠 0.91 | — — | 🔴 2.00 | — — | — — | 🟠 1.02 | 🔴 0.64 | — — | 🟢 2.26 | — — |
| `CY_UEM` | 🔴 1.26 | — — | 🟢 3.02 | 🔴 4.02 | 🟢 0.73 | — — | 🔴 2.00 | — — | — — | 🔴 0.51 | 🔴 0.32 | — — | 🔴 1.88 | — — |

### G20:KOR

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟢 2.11 | 🟡 1.86 | 🔴 1.79 | 🟡 4.00 | 🟢 0.84 | 🔴 0.68 | 🔴 2.00 | 🟢 1.51 | 🟢 1.45 | 🔴 0.57 | 🟠 0.91 | 🔴 0.05 | 🟢 3.73 | — — |
| `CY_GDP` | 🔴 0.72 | 🔴 0.85 | 🔴 0.70 | 🔴 4.69 | 🔴 0.99 | 🔴 -0.12 | 🔴 2.00 | 🟠 0.27 | 🔴 0.15 | 🔴 0.93 | 🟡 0.69 | 🔴 0.04 | 🟢 0.95 | — — |
| `CY_INF` | 🔴 1.03 | 🔴 0.48 | 🔴 1.36 | 🟢 1.57 | 🔴 0.96 | 🔴 -0.73 | 🔴 1.68 | 🟡 1.20 | 🔴 0.20 | 🟢 1.28 | 🟢 0.75 | 🔴 0.04 | 🟢 2.25 | — — |
| `CY_INV` | 🔴 1.50 | 🔴 0.22 | 🔴 1.65 | 🟠 2.26 | 🟡 0.90 | 🔴 -0.65 | 🟢 0.50 | 🔴 1.78 | 🔴 0.81 | 🟡 1.26 | 🔴 0.44 | 🔴 0.02 | 🟢 2.62 | — — |
| `CY_POP` | 🟢 2.19 | 🔴 0.17 | 🔴 1.82 | 🔴 5.53 | 🟢 0.33 | 🔴 -0.95 | 🔴 2.00 | 🔴 1.96 | 🟢 2.01 | 🔴 0.69 | 🟡 1.00 | 🔴 -0.06 | 🟢 3.90 | — — |
| `CY_PRD` | 🟢 2.04 | 🔴 0.98 | 🔴 1.79 | 🔴 5.44 | 🟢 0.23 | 🟠 0.87 | 🔴 2.00 | 🔴 1.86 | 🟢 1.93 | 🔴 0.56 | 🟡 1.00 | 🔴 0.04 | 🟢 3.84 | — — |
| `CY_TRD` | 🟡 1.73 | 🔴 0.55 | 🔴 1.59 | 🔴 8.72 | 🟡 0.89 | 🔴 0.20 | 🟡 1.36 | 🔴 1.69 | 🔴 1.00 | 🔴 0.92 | 🔴 0.66 | 🔴 0.08 | 🟢 2.92 | — — |
| `CY_UEM` | 🔴 0.92 | — — | 🔴 1.30 | 🟡 1.66 | 🟠 0.90 | — — | 🔴 1.59 | — — | — — | 🟢 1.59 | 🔴 0.35 | — — | 🟢 1.36 | — — |

### G20:MEX

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.85 | 🔴 0.14 | 🔴 0.62 | 🔴 2.98 | 🔴 0.98 | 🔴 -0.49 | 🟢 1.33 | 🟢 -21.44 | 🔴 0.06 | 🟡 1.23 | 🟡 0.44 | 🔴 0.04 | 🟢 0.62 | — — |
| `CY_INF` | 🔴 1.40 | 🔴 0.18 | 🟡 2.20 | 🟢 0.86 | 🔴 0.95 | 🔴 -0.59 | 🟢 0.50 | 🟡 1.12 | 🔴 0.70 | 🟢 1.62 | 🔴 0.41 | 🔴 0.02 | 🟢 1.90 | — — |
| `CY_INV` | 🔴 1.18 | 🔴 0.19 | 🔴 1.47 | 🔴 6.18 | 🟡 0.92 | 🔴 -0.87 | 🔴 2.00 | 🟡 1.56 | 🔴 0.49 | 🔴 0.84 | 🔴 0.41 | 🔴 0.05 | 🟢 1.54 | — — |
| `CY_POP` | 🟢 2.14 | 🔴 1.14 | 🔴 1.74 | 🟠 3.79 | 🟢 -0.00 | 🔴 -1.00 | 🔴 2.00 | 🔴 2.00 | 🟢 1.94 | 🔴 0.79 | 🟡 1.00 | 🔴 -0.03 | 🟢 3.97 | — — |
| `CY_PRD` | 🔴 1.68 | 🔴 0.26 | 🔴 1.77 | 🟡 3.28 | 🟢 0.67 | 🔴 -0.81 | 🔴 2.00 | 🔴 1.86 | 🟠 1.26 | 🔴 0.81 | 🟠 0.91 | 🔴 0.04 | 🟢 3.39 | — — |
| `CY_TRD` | 🔴 1.64 | 🔴 1.09 | 🔴 1.90 | 🔴 6.57 | 🔴 0.91 | 🟡 0.94 | 🔴 2.00 | 🟢 1.40 | 🔴 1.13 | 🔴 0.67 | 🟡 0.91 | 🔴 0.07 | 🟢 3.36 | — — |
| `CY_UEM` | 🔴 1.44 | — — | 🔴 1.62 | 🔴 4.66 | 🟢 0.84 | — — | 🔴 2.00 | — — | — — | 🟡 1.20 | 🔴 0.32 | — — | 🟡 1.10 | — — |

### G20:RUS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.94 | — — | 🔴 1.36 | 🔴 2.55 | 🔴 0.96 | — — | 🔴 2.00 | — — | — — | 🔴 1.02 | 🔴 0.42 | — — | 🔴 0.56 | — — |
| `CY_INF` | 🔴 1.30 | — — | 🔴 0.62 | 🟢 1.43 | 🔴 0.94 | — — | 🟢 0.50 | — — | — — | 🟢 1.83 | 🟢 0.81 | — — | 🟢 2.02 | — — |
| `CY_INV` | 🔴 1.38 | — — | 🔴 1.44 | 🟢 1.34 | 🔴 0.96 | — — | 🟢 1.04 | — — | — — | 🟡 1.25 | 🔴 0.34 | — — | 🟢 1.48 | — — |
| `CY_POP` | 🟢 2.09 | 🔴 0.13 | 🔴 1.73 | 🟡 2.99 | 🟢 0.40 | 🔴 -0.81 | 🔴 1.54 | 🔴 2.00 | 🟢 1.88 | 🟠 1.09 | 🔴 0.88 | 🔴 -0.01 | 🟢 3.95 | — — |
| `CY_PRD` | 🟠 1.95 | — — | 🟠 2.31 | 🔴 5.25 | 🟠 0.84 | — — | 🔴 2.00 | — — | — — | 🔴 0.52 | 🟠 1.00 | — — | 🟢 2.37 | — — |
| `CY_TRD` | 🔴 0.92 | — — | 🔴 0.33 | 🟢 1.47 | 🟡 0.91 | — — | 🟠 1.39 | — — | — — | 🟢 1.69 | 🟢 0.67 | — — | 🟢 1.60 | — — |
| `CY_UEM` | 🔴 1.82 | — — | 🟠 2.30 | 🟠 2.23 | 🟡 0.84 | — — | 🔴 1.46 | — — | — — | 🔴 1.04 | 🔴 0.66 | — — | 🟡 1.79 | — — |

### G20:SAU

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.22 | — — | 🔴 1.85 | 🟡 2.88 | 🔴 0.90 | — — | 🔴 2.00 | — — | — — | 🔴 0.85 | 🔴 0.86 | — — | 🟢 3.09 | — — |
| `CY_GDP` | 🔴 1.02 | 🟡 1.31 | 🔴 0.61 | 🟢 1.95 | 🔴 0.98 | 🔴 -0.75 | 🔴 1.73 | 🔴 1.38 | 🔴 0.20 | 🟢 1.73 | 🟡 0.44 | 🔴 0.02 | 🟢 0.99 | — — |
| `CY_INF` | 🟠 1.48 | — — | 🟢 2.05 | 🟢 1.13 | 🔴 0.97 | 🔴 -0.64 | 🟢 0.50 | — — | — — | 🟢 1.72 | 🔴 0.17 | — — | 🟡 1.51 | — — |
| `CY_INV` | 🟢 1.22 | — — | 🔴 0.41 | 🟠 2.48 | 🟡 0.93 | — — | 🔴 2.00 | — — | — — | 🟢 1.76 | 🔴 0.23 | — — | 🟢 1.13 | — — |
| `CY_POP` | 🟢 2.19 | 🔴 0.05 | 🔴 1.78 | 🟠 3.54 | 🟢 -0.00 | 🔴 -1.00 | 🔴 2.00 | 🔴 2.00 | 🟢 1.96 | 🔴 0.94 | 🟡 1.00 | 🔴 -0.05 | 🟢 3.96 | — — |
| `CY_PRD` | 🟡 1.85 | 🔴 0.46 | 🟢 2.31 | 🔴 7.03 | 🟡 0.88 | 🔴 -0.81 | 🟡 0.50 | 🟠 1.73 | 🟢 1.45 | 🟡 1.16 | 🔴 0.60 | 🔴 0.01 | 🟡 3.32 | — — |
| `CY_TRD` | 🟢 1.70 | — — | 🔴 0.96 | 🔴 4.41 | 🔴 0.96 | — — | 🔴 2.00 | — — | — — | 🟠 1.11 | 🔴 0.38 | — — | 🟢 1.83 | — — |
| `CY_UEM` | 🔴 1.88 | — — | 🔴 0.91 | 🟠 2.23 | 🟡 0.84 | — — | 🟢 1.06 | — — | — — | 🟠 1.11 | 🔴 0.30 | — — | 🟢 1.67 | — — |

### G20:TUR

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🟠 0.81 | 🔴 0.14 | 🔴 -0.27 | 🔴 3.06 | 🔴 0.99 | 🟡 0.68 | 🟡 1.40 | 🟠 -8.05 | 🔴 0.02 | 🔴 1.09 | 🔴 0.19 | 🔴 0.05 | 🔴 0.06 | — — |
| `CY_INF` | 🔴 1.35 | 🟡 2.26 | 🔴 1.68 | 🟠 2.82 | 🔴 0.96 | 🔴 0.63 | 🔴 2.00 | 🟡 1.43 | 🔴 0.87 | 🔴 0.79 | 🔴 0.22 | 🔴 0.06 | 🟢 2.75 | — — |
| `CY_INV` | 🔴 1.09 | 🔴 1.62 | 🔴 1.97 | 🔴 8.81 | 🔴 0.97 | 🔴 -0.29 | 🔴 2.00 | 🟠 1.72 | 🔴 0.63 | 🔴 0.64 | 🟠 0.81 | 🔴 0.03 | 🟢 2.38 | — — |
| `CY_POP` | 🟢 2.20 | 🟢 2.48 | 🔴 1.81 | 🔴 45.02 | 🟢 0.20 | 🔴 0.22 | 🔴 2.00 | 🔴 1.76 | 🟢 1.89 | 🔴 0.67 | 🟡 1.00 | 🔴 0.02 | 🟢 3.83 | — — |
| `CY_PRD` | 🟡 1.86 | 🔴 0.43 | 🔴 1.73 | 🟡 2.92 | 🟢 0.63 | 🟡 0.98 | 🔴 2.00 | 🔴 1.78 | 🟢 1.60 | 🔴 0.99 | 🟡 1.00 | 🔴 0.04 | 🟢 3.77 | — — |
| `CY_TRD` | 🔴 1.43 | 🔴 0.77 | 🔴 1.95 | 🔴 5.89 | 🟠 0.91 | 🔴 -0.23 | 🔴 2.00 | 🟡 1.68 | 🔴 0.89 | 🔴 0.67 | 🟠 0.91 | 🔴 0.05 | 🟢 3.13 | — — |
| `CY_UEM` | 🟡 2.08 | — — | 🟠 2.13 | 🔴 2.48 | 🟢 0.79 | — — | 🔴 1.68 | — — | — — | 🔴 0.94 | 🔴 0.54 | — — | 🟡 1.30 | — — |

### G20:USA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.68 | 🟠 1.56 | 🔴 1.70 | 🔴 7.20 | 🟢 0.84 | 🔴 0.39 | 🔴 2.00 | 🟡 1.50 | 🔴 1.17 | 🔴 0.40 | 🟡 0.97 | 🔴 0.07 | 🟢 3.57 | — — |
| `CY_GDP` | 🔴 0.77 | 🔴 0.94 | 🔴 0.67 | 🔴 4.12 | 🔴 0.99 | 🔴 -0.75 | 🟠 1.50 | 🟢 -9.95 | 🔴 0.02 | 🔴 1.08 | 🟡 0.41 | 🔴 0.03 | 🟡 0.36 | — — |
| `CY_INF` | 🔴 1.28 | 🔴 0.43 | 🟡 1.95 | 🟢 2.14 | 🟡 0.93 | 🔴 -0.65 | 🟢 1.25 | 🔴 2.03 | 🔴 0.58 | 🟢 1.38 | 🔴 0.54 | 🔴 0.04 | 🟡 1.60 | — — |
| `CY_INV` | 🔴 1.27 | — — | 🔴 1.64 | 🔴 3.02 | 🟢 0.87 | — — | 🔴 1.82 | — — | — — | 🟠 1.08 | 🔴 0.31 | — — | 🔴 1.19 | — — |
| `CY_POP` | 🟢 2.16 | 🟡 2.25 | 🔴 1.73 | 🔴 5.45 | 🟢 0.32 | 🔴 0.23 | 🔴 2.00 | 🔴 1.98 | 🟢 1.85 | 🔴 0.42 | 🟡 1.00 | 🔴 0.04 | 🟢 3.81 | — — |
| `CY_PRD` | 🟢 1.99 | 🔴 1.36 | 🔴 1.74 | 🔴 8.78 | 🟢 0.56 | 🔴 0.27 | 🔴 2.00 | 🟠 1.68 | 🟢 1.70 | 🔴 0.56 | 🟡 1.00 | 🔴 0.02 | 🟢 3.77 | — — |
| `CY_TRD` | 🔴 1.73 | — — | 🔴 1.82 | 🔴 5.92 | 🟢 0.85 | — — | 🔴 2.00 | — — | — — | 🔴 0.78 | 🟡 0.93 | — — | 🟢 2.61 | — — |
| `CY_UEM` | 🔴 1.12 | — — | 🔴 1.43 | 🔴 2.77 | 🟢 0.66 | — — | 🔴 1.79 | — — | — — | 🔴 0.95 | 🔴 0.28 | — — | 🟢 1.39 | — — |

### G20:ZAF

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.39 | — — | 🔴 2.11 | 🔴 8.83 | 🟡 0.89 | — — | 🔴 2.00 | — — | — — | 🔴 0.36 | 🔴 0.90 | — — | 🟢 3.10 | — — |
| `CY_GDP` | 🔴 0.88 | 🔴 0.85 | 🔴 0.98 | 🔴 4.03 | 🔴 0.98 | 🔴 -0.56 | 🔴 2.00 | 🟢 -20.87 | 🔴 0.17 | 🟠 1.16 | 🔴 0.34 | 🔴 0.04 | 🟠 0.46 | — — |
| `CY_INF` | 🔴 1.28 | 🔴 0.20 | 🟡 1.99 | 🔴 4.94 | 🔴 0.94 | 🔴 -0.45 | 🔴 2.00 | 🟡 1.63 | 🔴 0.89 | 🔴 0.76 | 🔴 0.53 | 🔴 0.05 | 🔴 2.12 | — — |
| `CY_INV` | 🔴 1.36 | 🔴 0.71 | 🔴 1.54 | 🔴 5.74 | 🔴 0.95 | 🔴 -0.38 | 🔴 2.00 | 🟡 1.69 | 🔴 0.85 | 🔴 0.89 | 🟠 0.81 | 🔴 0.06 | 🟠 2.36 | — — |
| `CY_POP` | 🟢 2.15 | 🟠 1.52 | 🔴 1.82 | 🔴 47.13 | 🟢 -0.00 | 🔴 0.64 | 🔴 2.00 | 🔴 1.97 | 🟢 2.00 | 🔴 0.38 | 🟡 1.00 | 🔴 0.04 | 🟢 3.83 | — — |
| `CY_PRD` | 🟢 1.94 | 🔴 0.84 | 🔴 1.83 | 🔴 17.03 | 🟢 0.81 | 🟠 0.72 | 🔴 2.00 | 🔴 1.75 | 🟢 1.47 | 🔴 0.63 | 🔴 0.58 | 🟡 0.11 | 🟢 3.12 | — — |
| `CY_TRD` | 🔴 1.30 | 🔴 0.78 | 🔴 1.78 | 🔴 3.64 | 🟡 0.89 | 🟠 0.75 | 🔴 2.00 | 🟢 1.19 | 🔴 0.69 | 🔴 0.92 | 🔴 0.48 | 🔴 0.07 | 🟢 2.06 | — — |
| `CY_UEM` | 🟠 2.01 | — — | 🔴 1.91 | 🟡 1.56 | 🔴 0.91 | — — | 🔴 1.88 | — — | — — | 🔴 1.07 | 🔴 0.94 | — — | 🟢 2.70 | — — |

### G7

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟠 1.69 | 🔴 0.85 | 🔴 1.62 | 🔴 10.35 | 🟢 0.79 | 🔴 -0.41 | 🔴 2.00 | 🟡 1.63 | 🔴 1.21 | 🔴 0.44 | 🟡 1.00 | 🔴 0.04 | 🟢 3.54 | — — |
| `CY_GDP` | 🔴 0.70 | 🔴 0.94 | 🟡 1.10 | 🔴 3.71 | 🔴 0.98 | 🔴 -0.20 | 🔴 1.70 | 🔴 4.99 | 🔴 -0.02 | 🟢 1.32 | 🟢 0.66 | 🔴 0.02 | 🟢 0.84 | — — |
| `CY_INF` | 🔴 1.35 | 🔴 0.30 | 🟡 1.95 | 🟡 2.23 | 🔴 0.96 | 🔴 -0.58 | 🟡 1.34 | 🔴 1.74 | 🔴 0.71 | 🟢 1.34 | 🟠 0.66 | 🔴 0.07 | 🟢 2.27 | — — |
| `CY_INV` | 🔴 1.26 | 🟡 2.48 | 🔴 1.45 | 🔴 6.60 | 🟠 0.90 | 🔴 0.52 | 🔴 2.00 | 🟢 1.13 | 🔴 0.59 | 🔴 0.72 | 🟡 0.97 | 🔴 0.05 | 🟡 2.41 | — — |
| `CY_POP` | 🟢 2.11 | 🔴 0.58 | 🔴 1.76 | 🔴 4.53 | 🟢 0.44 | 🔴 0.43 | 🔴 2.00 | 🔴 1.97 | 🟢 1.83 | 🔴 0.62 | 🟡 1.00 | 🔴 -0.01 | 🟢 3.79 | — — |
| `CY_PRD` | 🟢 2.05 | 🔴 0.71 | 🔴 1.74 | 🔴 9.34 | 🟢 0.52 | 🔴 0.34 | 🔴 2.00 | 🟡 1.66 | 🟢 1.67 | 🔴 0.57 | 🟡 1.00 | 🔴 0.02 | 🟢 3.80 | — — |
| `CY_TRD` | 🔴 1.38 | 🔴 0.31 | 🔴 1.55 | 🔴 7.76 | 🔴 0.92 | 🔴 0.37 | 🔴 2.00 | 🟢 0.12 | 🔴 0.64 | 🔴 0.73 | 🔴 0.79 | 🟡 0.11 | 🟢 2.97 | — — |
| `CY_UEM` | 🔴 0.77 | — — | 🔴 1.66 | 🔴 2.90 | 🟢 0.79 | — — | 🔴 1.47 | — — | — — | 🔴 0.92 | 🔴 0.47 | — — | 🟢 1.33 | — — |

### G7:CAN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟢 2.32 | — — | 🔴 1.81 | 🔴 4.51 | 🟢 0.69 | — — | 🔴 1.69 | — — | — — | 🔴 0.86 | 🔴 0.88 | — — | 🟢 3.16 | — — |
| `CY_GDP` | 🔴 0.78 | 🔴 0.69 | 🟢 1.10 | 🟡 2.50 | 🔴 0.99 | 🔴 -0.50 | 🟢 1.39 | 🔴 5.60 | 🔴 0.03 | 🟢 1.32 | 🟡 0.41 | 🔴 0.04 | 🔴 0.22 | — — |
| `CY_INF` | 🔴 1.32 | 🔴 0.52 | 🔴 1.76 | 🟢 2.01 | 🔴 0.97 | 🔴 -0.61 | 🟡 1.35 | 🔴 1.67 | 🔴 0.79 | 🟡 1.19 | 🟠 0.69 | 🟠 0.09 | 🟡 2.20 | — — |
| `CY_INV` | 🔴 1.32 | 🔴 0.30 | 🔴 1.40 | 🔴 4.90 | 🟡 0.92 | 🔴 -0.29 | 🔴 2.00 | 🟡 1.03 | 🔴 0.58 | 🔴 0.84 | 🔴 0.19 | 🔴 0.07 | 🟡 1.66 | — — |
| `CY_POP` | 🟢 2.15 | 🟠 1.67 | 🔴 1.64 | 🟠 3.59 | 🟢 0.22 | 🔴 0.35 | 🔴 2.00 | 🔴 2.06 | 🟢 1.58 | 🔴 0.96 | 🟡 1.00 | 🔴 0.01 | 🟢 3.84 | — — |
| `CY_PRD` | 🟢 1.96 | 🔴 0.11 | 🔴 1.83 | 🔴 6.53 | 🟢 0.54 | 🔴 0.03 | 🔴 2.00 | 🟠 1.73 | 🟢 1.60 | 🔴 0.56 | 🟠 0.91 | 🔴 0.00 | 🟢 3.69 | — — |
| `CY_TRD` | 🔴 1.50 | 🔴 0.26 | 🔴 1.68 | 🔴 8.89 | 🟠 0.92 | 🔴 -0.12 | 🔴 2.00 | 🔴 2.03 | 🟡 1.24 | 🔴 0.66 | 🟢 1.00 | 🔴 0.04 | 🟢 3.11 | — — |
| `CY_UEM` | 🔴 1.01 | — — | 🔴 1.83 | 🔴 3.55 | 🟢 0.84 | — — | 🔴 1.60 | — — | — — | 🔴 0.95 | 🔴 0.43 | — — | 🟢 1.53 | — — |

### G7:DEU

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.68 | 🔴 0.64 | 🔴 0.43 | 🔴 2.86 | 🟢 0.90 | 🔴 0.12 | 🔴 2.00 | 🔴 3.45 | 🔴 -0.03 | 🟡 1.25 | 🟡 0.47 | 🔴 0.03 | 🟢 0.47 | — — |
| `CY_INF` | 🔴 1.19 | 🔴 0.70 | 🟡 1.85 | 🔴 4.06 | 🟡 0.90 | 🔴 -0.59 | 🔴 1.61 | 🔴 1.49 | 🔴 0.42 | 🔴 0.96 | 🔴 0.51 | 🔴 0.05 | 🟠 1.38 | — — |
| `CY_INV` | 🔴 1.46 | — — | 🔴 1.61 | 🟠 2.62 | 🔴 0.95 | — — | 🔴 1.77 | — — | — — | 🟡 1.17 | 🟡 0.86 | — — | 🟢 2.46 | — — |
| `CY_POP` | 🟢 2.15 | 🔴 1.41 | 🔴 1.41 | 🟡 2.34 | 🟢 -0.00 | 🔴 0.02 | 🟢 0.50 | 🔴 2.07 | 🟢 1.41 | 🟢 1.50 | 🟢 1.00 | 🔴 0.00 | 🟢 3.92 | — — |
| `CY_PRD` | 🟢 2.03 | 🔴 0.85 | 🔴 1.81 | 🔴 12.90 | 🟢 0.56 | 🔴 -0.83 | 🔴 2.00 | 🟡 1.68 | 🟢 1.69 | 🔴 0.55 | 🟡 0.97 | 🔴 0.00 | 🟢 3.64 | — — |
| `CY_TRD` | 🔴 1.49 | — — | 🔴 2.00 | 🔴 10.22 | 🟡 0.87 | — — | 🔴 2.00 | — — | — — | 🔴 0.44 | 🟡 1.00 | — — | 🟢 3.14 | — — |
| `CY_UEM` | 🟡 2.17 | — — | 🟢 2.88 | 🔴 8.19 | 🟡 0.80 | — — | 🔴 2.00 | — — | — — | 🔴 0.50 | 🔴 0.83 | — — | 🔴 1.99 | — — |

### G7:FRA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.71 | 🟡 1.37 | 🔴 0.46 | 🔴 3.61 | 🔴 0.98 | 🔴 -0.14 | 🔴 2.00 | 🔴 3.52 | 🔴 -0.02 | 🟢 1.47 | 🟡 0.56 | 🔴 0.04 | 🟢 1.60 | — — |
| `CY_INF` | 🔴 1.40 | 🔴 0.60 | 🔴 1.83 | 🟠 3.04 | 🟠 0.92 | 🔴 -0.45 | 🟠 1.46 | 🟠 1.66 | 🔴 0.95 | 🟠 1.14 | 🟡 0.91 | 🔴 0.06 | 🟠 2.42 | — — |
| `CY_INV` | 🔴 1.33 | 🔴 0.18 | 🔴 1.71 | 🔴 8.35 | 🔴 0.95 | 🔴 -0.76 | 🔴 2.00 | 🟢 1.43 | 🔴 0.82 | 🔴 0.73 | 🔴 0.78 | 🔴 0.05 | 🟠 2.46 | — — |
| `CY_POP` | 🟢 2.27 | 🟠 1.96 | 🔴 1.67 | 🟢 1.70 | 🟢 0.24 | 🔴 -0.41 | 🟡 1.38 | 🔴 2.02 | 🟢 1.59 | 🟢 1.26 | 🟡 1.00 | 🔴 0.00 | 🟢 3.88 | — — |
| `CY_PRD` | 🟢 1.99 | 🔴 0.10 | 🔴 1.75 | 🔴 5.74 | 🟢 0.40 | 🔴 -0.74 | 🔴 2.00 | 🟡 1.47 | 🟢 1.67 | 🔴 0.61 | 🟡 1.00 | 🔴 -0.01 | 🟢 3.81 | — — |
| `CY_TRD` | 🔴 1.52 | 🟠 1.54 | 🔴 1.85 | 🔴 11.45 | 🟢 0.84 | 🔴 0.16 | 🔴 2.00 | 🟢 1.17 | 🔴 0.96 | 🔴 0.74 | 🔴 0.85 | 🔴 0.05 | 🟢 3.09 | — — |
| `CY_UEM` | 🔴 1.50 | — — | 🟠 2.36 | 🔴 4.99 | 🔴 0.89 | — — | 🔴 1.74 | — — | — — | 🔴 0.79 | 🔴 0.42 | — — | 🟠 1.56 | — — |

### G7:GBR

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟡 1.79 | 🟠 1.78 | 🟡 2.06 | 🔴 4.90 | 🟢 0.79 | 🔴 0.04 | 🔴 2.00 | 🟢 1.60 | 🟡 1.39 | 🔴 0.51 | 🟠 0.91 | 🔴 0.09 | 🟢 3.44 | — — |
| `CY_GDP` | 🔴 0.65 | 🟡 1.71 | 🔴 -0.06 | 🟡 2.15 | 🔴 0.99 | 🔴 -0.11 | 🟢 1.28 | 🔴 3.80 | 🔴 -0.09 | 🟢 1.62 | 🔴 0.16 | 🔴 0.05 | 🟡 0.47 | — — |
| `CY_INF` | 🔴 1.26 | 🔴 0.84 | 🔴 1.58 | 🟢 1.22 | 🟡 0.92 | 🔴 -0.64 | 🟡 1.28 | 🔴 2.04 | 🔴 0.70 | 🟢 1.49 | 🟡 0.75 | 🔴 0.04 | 🟡 2.19 | — — |
| `CY_INV` | 🔴 1.26 | — — | 🔴 1.88 | 🔴 4.68 | 🔴 0.97 | — — | 🔴 2.00 | — — | — — | 🔴 0.87 | 🟡 0.89 | — — | 🟢 2.46 | — — |
| `CY_POP` | 🟢 2.06 | 🔴 0.14 | 🔴 1.94 | 🟡 3.77 | 🟢 0.46 | 🟡 0.94 | 🔴 2.00 | 🔴 1.98 | 🟢 1.77 | 🔴 0.75 | 🟡 0.91 | 🔴 0.08 | 🟢 3.71 | — — |
| `CY_PRD` | 🟢 1.96 | 🔴 0.49 | 🔴 1.80 | 🔴 22.31 | 🟢 0.51 | 🔴 0.23 | 🔴 2.00 | 🟢 1.41 | 🟢 1.54 | 🔴 0.39 | 🟡 0.97 | 🔴 0.02 | 🟢 3.77 | — — |
| `CY_TRD` | 🔴 1.17 | — — | 🔴 1.70 | 🔴 4.50 | 🔴 0.94 | — — | 🔴 2.00 | — — | — — | 🔴 0.87 | 🔴 0.50 | — — | 🟢 1.69 | — — |
| `CY_UEM` | 🔴 1.35 | — — | 🔴 2.16 | 🔴 3.41 | 🟡 0.83 | — — | 🔴 2.00 | — — | — — | 🔴 0.74 | 🔴 0.39 | — — | 🟢 1.87 | — — |

### G7:ITA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_GDP` | 🔴 0.61 | 🟠 1.25 | 🔴 0.43 | 🔴 2.96 | 🟢 0.90 | 🔴 -0.12 | 🟡 1.45 | 🔴 3.81 | 🟠 -0.06 | 🟢 1.33 | 🟢 0.62 | 🔴 0.04 | 🟢 1.18 | — — |
| `CY_INF` | 🔴 1.34 | 🔴 1.79 | 🟠 2.02 | 🔴 3.77 | 🔴 0.94 | 🔴 -0.67 | 🟡 1.18 | 🟠 1.73 | 🔴 0.92 | 🟡 1.16 | 🔴 0.66 | 🔴 0.05 | 🟠 2.43 | — — |
| `CY_INV` | 🔴 1.05 | — — | 🔴 1.49 | 🔴 5.16 | 🔴 0.96 | — — | 🔴 1.86 | — — | — — | 🔴 1.03 | 🟡 0.71 | — — | 🟡 1.85 | — — |
| `CY_POP` | 🟢 2.17 | 🟠 1.90 | 🔴 1.66 | 🟢 1.84 | 🟢 0.46 | 🔴 -0.09 | 🟢 0.50 | 🔴 2.03 | 🟢 1.73 | 🟡 1.21 | 🟠 0.85 | 🔴 0.03 | 🟢 3.90 | — — |
| `CY_PRD` | 🟢 2.05 | 🔴 0.13 | 🔴 1.72 | 🔴 4.63 | 🟢 0.49 | 🔴 -0.97 | 🔴 2.00 | 🟡 1.45 | 🟢 1.58 | 🔴 0.65 | 🟡 0.97 | 🔴 0.00 | 🟢 3.79 | — — |
| `CY_TRD` | 🔴 1.46 | — — | 🔴 1.78 | 🔴 3.54 | 🔴 0.93 | — — | 🔴 2.00 | — — | — — | 🔴 0.91 | 🟡 0.93 | — — | 🟢 2.41 | — — |
| `CY_UEM` | 🟡 2.10 | — — | 🔴 1.46 | 🔴 4.71 | 🟢 0.76 | — — | 🔴 2.00 | — — | — — | 🔴 0.59 | 🔴 0.21 | — — | 🟡 1.61 | — — |

### G7:JPN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟠 1.85 | — — | 🔴 1.68 | 🔴 8.27 | 🟢 0.85 | — — | 🔴 2.00 | — — | — — | 🔴 0.68 | 🔴 0.63 | — — | 🟢 2.90 | — — |
| `CY_GDP` | 🔴 0.82 | 🟠 1.32 | 🔴 0.85 | 🟡 2.46 | 🔴 0.98 | 🔴 -0.63 | 🟡 1.43 | 🟢 -0.87 | 🔴 0.16 | 🟠 1.10 | 🟢 0.84 | 🔴 0.02 | 🟢 1.57 | — — |
| `CY_INF` | 🔴 1.18 | 🔴 1.23 | 🔴 1.53 | 🟢 1.82 | 🟡 0.92 | 🔴 -0.62 | 🔴 2.00 | 🔴 1.90 | 🔴 0.45 | 🟢 1.69 | 🟢 0.79 | 🔴 0.06 | 🟢 2.51 | — — |
| `CY_INV` | 🔴 1.73 | — — | 🔴 1.63 | 🟡 2.63 | 🟠 0.89 | — — | 🔴 2.00 | — — | — — | 🔴 0.83 | 🟡 0.96 | — — | 🟢 3.05 | — — |
| `CY_POP` | 🟢 2.12 | 🔴 0.73 | 🔴 1.74 | 🔴 8.22 | 🟢 -0.00 | 🔴 0.49 | 🔴 2.00 | 🔴 1.91 | 🟢 1.82 | 🔴 0.68 | 🟡 1.00 | 🔴 -0.01 | 🟢 3.78 | — — |
| `CY_PRD` | 🟢 2.10 | 🔴 0.27 | 🔴 1.76 | 🟠 3.60 | 🟢 0.57 | 🔴 -0.93 | 🔴 2.00 | 🔴 1.91 | 🟢 1.73 | 🔴 0.62 | 🟡 0.97 | 🔴 0.01 | 🟢 3.83 | — — |
| `CY_TRD` | 🔴 1.41 | — — | 🔴 1.61 | 🟠 3.02 | 🟠 0.91 | — — | 🔴 2.00 | — — | — — | 🟠 1.02 | 🔴 0.64 | — — | 🟢 2.26 | — — |
| `CY_UEM` | 🔴 1.26 | — — | 🟢 3.02 | 🔴 4.02 | 🟢 0.73 | — — | 🔴 2.00 | — — | — — | 🔴 0.51 | 🔴 0.32 | — — | 🔴 1.88 | — — |

### G7:USA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.68 | 🟠 1.56 | 🔴 1.70 | 🔴 7.20 | 🟢 0.84 | 🔴 0.39 | 🔴 2.00 | 🟡 1.50 | 🔴 1.17 | 🔴 0.40 | 🟡 0.97 | 🔴 0.07 | 🟢 3.57 | — — |
| `CY_GDP` | 🔴 0.77 | 🔴 0.94 | 🔴 0.67 | 🔴 4.12 | 🔴 0.99 | 🔴 -0.75 | 🟠 1.50 | 🟢 -9.95 | 🔴 0.02 | 🔴 1.08 | 🟡 0.41 | 🔴 0.03 | 🟡 0.36 | — — |
| `CY_INF` | 🔴 1.28 | 🔴 0.43 | 🟡 1.95 | 🟢 2.14 | 🟡 0.93 | 🔴 -0.65 | 🟢 1.25 | 🔴 2.03 | 🔴 0.58 | 🟢 1.38 | 🔴 0.54 | 🔴 0.04 | 🟡 1.60 | — — |
| `CY_INV` | 🔴 1.27 | — — | 🔴 1.64 | 🔴 3.02 | 🟢 0.87 | — — | 🔴 1.82 | — — | — — | 🟠 1.08 | 🔴 0.31 | — — | 🔴 1.19 | — — |
| `CY_POP` | 🟢 2.16 | 🟡 2.25 | 🔴 1.73 | 🔴 5.45 | 🟢 0.32 | 🔴 0.23 | 🔴 2.00 | 🔴 1.98 | 🟢 1.85 | 🔴 0.42 | 🟡 1.00 | 🔴 0.04 | 🟢 3.81 | — — |
| `CY_PRD` | 🟢 1.99 | 🔴 1.36 | 🔴 1.74 | 🔴 8.78 | 🟢 0.56 | 🔴 0.27 | 🔴 2.00 | 🟠 1.68 | 🟢 1.70 | 🔴 0.56 | 🟡 1.00 | 🔴 0.02 | 🟢 3.77 | — — |
| `CY_TRD` | 🔴 1.73 | — — | 🔴 1.82 | 🔴 5.92 | 🟢 0.85 | — — | 🔴 2.00 | — — | — — | 🔴 0.78 | 🟡 0.93 | — — | 🟢 2.61 | — — |
| `CY_UEM` | 🔴 1.12 | — — | 🔴 1.43 | 🔴 2.77 | 🟢 0.66 | — — | 🔴 1.79 | — — | — — | 🔴 0.95 | 🔴 0.28 | — — | 🟢 1.39 | — — |

### HIC

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.57 | — — | 🔴 1.67 | 🔴 3.11 | 🟢 0.76 | — — | 🔴 1.64 | — — | — — | 🔴 0.96 | 🔴 0.65 | — — | 🟢 2.72 | — — |
| `CY_GDP` | 🔴 0.68 | 🔴 0.97 | 🟡 0.98 | 🔴 2.91 | 🔴 0.98 | 🔴 -0.21 | 🔴 1.79 | 🔴 4.60 | 🔴 -0.01 | 🟢 1.35 | 🟡 0.53 | 🔴 0.02 | 🟢 0.80 | — — |
| `CY_INV` | 🔴 1.07 | — — | 🔴 1.69 | 🔴 4.47 | 🔴 0.92 | — — | 🔴 2.00 | — — | — — | 🔴 0.81 | 🟢 0.93 | — — | 🟢 2.15 | — — |
| `CY_POP` | 🟢 2.16 | 🔴 0.70 | 🔴 1.74 | 🟡 3.22 | 🟢 -0.00 | 🔴 -1.00 | 🔴 2.00 | 🔴 2.00 | 🟢 1.91 | 🔴 0.79 | 🟡 1.00 | 🔴 -0.03 | 🟢 3.91 | — — |
| `CY_PRD` | 🟢 2.04 | 🔴 0.89 | 🔴 1.75 | 🔴 9.88 | 🟢 0.35 | 🔴 0.33 | 🔴 2.00 | 🟡 1.61 | 🟢 1.75 | 🔴 0.55 | 🟡 1.00 | 🔴 0.01 | 🟢 3.81 | — — |
| `CY_TRD` | 🔴 1.53 | — — | 🔴 1.90 | 🔴 6.08 | 🟡 0.88 | — — | 🔴 2.00 | — — | — — | 🔴 0.56 | 🟡 1.00 | — — | 🟢 2.96 | — — |
| `CY_UEM` | 🔴 0.79 | — — | 🔴 1.79 | 🔴 2.58 | 🟡 0.82 | — — | 🔴 2.00 | — — | — — | 🔴 0.76 | 🔴 0.55 | — — | 🟢 1.69 | — — |

### LIC

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.35 | — — | 🔴 1.37 | 🔴 4.61 | 🟡 0.88 | 🟢 0.97 | 🔴 2.00 | — — | — — | 🔴 0.76 | 🔴 0.57 | — — | 🟢 2.61 | — — |
| `CY_GDP` | 🔴 0.96 | — — | 🔴 1.05 | 🔴 3.45 | 🔴 0.95 | — — | 🔴 2.00 | — — | — — | 🔴 0.97 | 🔴 0.18 | — — | 🟠 0.52 | — — |
| `CY_INV` | 🔴 1.58 | — — | 🔴 1.72 | 🔴 7.07 | 🔴 0.90 | — — | 🔴 2.00 | — — | — — | 🔴 0.65 | 🟡 1.00 | — — | 🟢 1.76 | — — |
| `CY_POP` | 🟢 2.10 | 🔴 0.08 | 🔴 1.73 | 🔴 10.59 | 🟢 -0.00 | 🔴 -0.79 | 🔴 2.00 | 🔴 1.96 | 🟢 1.95 | 🔴 0.63 | 🟡 1.00 | 🔴 0.01 | 🟢 3.87 | — — |
| `CY_PRD` | 🟢 1.96 | — — | 🟡 2.41 | 🟠 3.03 | 🟡 0.83 | — — | 🔴 1.89 | — — | — — | 🔴 0.90 | 🔴 0.51 | — — | 🟠 2.13 | — — |
| `CY_TRD` | 🔴 1.45 | — — | 🔴 1.46 | 🔴 3.23 | 🔴 0.97 | — — | 🔴 2.00 | — — | — — | 🔴 0.82 | 🟠 0.82 | — — | 🟢 1.60 | — — |
| `CY_UEM` | 🔴 1.57 | — — | 🔴 1.93 | 🔴 2.45 | 🟡 0.87 | — — | 🔴 2.00 | — — | — — | 🟡 1.32 | 🔴 0.60 | — — | 🔴 1.04 | — — |

### LMC

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟡 1.79 | 🔴 0.09 | 🔴 1.77 | 🔴 20.28 | 🟢 0.80 | 🔴 0.55 | 🔴 2.00 | 🔴 1.78 | 🟢 1.50 | 🔴 0.49 | 🔴 0.85 | 🔴 0.05 | 🟢 3.52 | — — |
| `CY_GDP` | 🔴 0.73 | 🟢 2.06 | 🔴 0.65 | 🔴 3.55 | 🟠 0.95 | 🔴 -0.25 | 🔴 2.00 | 🔴 2.94 | 🔴 -0.03 | 🟢 1.49 | 🟢 0.56 | 🔴 0.03 | 🟠 0.29 | — — |
| `CY_INV` | 🔴 1.33 | 🔴 0.69 | 🔴 1.49 | 🔴 7.36 | 🔴 0.95 | 🔴 0.37 | 🔴 2.00 | 🟡 1.69 | 🔴 0.80 | 🔴 0.55 | 🔴 0.79 | 🔴 0.05 | 🟢 2.56 | — — |
| `CY_POP` | 🟢 2.10 | 🔴 0.17 | 🔴 1.76 | 🔴 11.68 | 🟢 -0.00 | 🔴 0.34 | 🔴 2.00 | 🔴 1.99 | 🟢 2.00 | 🔴 0.62 | 🟡 1.00 | 🔴 0.01 | 🟢 3.87 | — — |
| `CY_PRD` | 🟢 1.91 | 🔴 1.00 | 🔴 1.72 | 🟡 4.01 | 🟢 0.53 | 🟡 0.96 | 🔴 2.00 | 🔴 1.93 | 🟢 1.78 | 🔴 0.95 | 🟡 1.00 | 🔴 0.05 | 🟢 3.97 | — — |
| `CY_TRD` | 🔴 1.60 | — — | 🟠 2.09 | 🔴 17.10 | 🟢 0.77 | 🔴 0.39 | 🔴 2.00 | — — | — — | 🔴 0.48 | 🟡 1.00 | — — | 🟢 3.16 | — — |
| `CY_UEM` | 🔴 1.35 | — — | 🔴 1.76 | 🟢 1.08 | 🔴 0.94 | — — | 🟢 0.50 | — — | — — | 🟢 1.46 | 🔴 0.55 | — — | 🟢 1.83 | — — |

### OECD

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.58 | — — | 🔴 1.68 | 🔴 2.99 | 🟢 0.72 | — — | 🟡 1.31 | — — | — — | 🟠 1.13 | 🔴 0.64 | — — | 🟢 2.67 | — — |
| `CY_GDP` | 🔴 0.69 | 🔴 1.12 | 🟡 1.01 | 🔴 2.90 | 🔴 0.99 | 🔴 -0.08 | 🔴 1.70 | 🔴 4.33 | 🔴 -0.01 | 🟢 1.38 | 🟢 0.56 | 🔴 0.03 | 🟢 0.75 | — — |
| `CY_INV` | 🔴 1.06 | — — | 🔴 1.66 | 🔴 4.04 | 🔴 0.92 | — — | 🔴 2.00 | — — | — — | 🔴 0.84 | 🟡 0.85 | — — | 🟢 2.07 | — — |
| `CY_POP` | 🟢 2.17 | 🔴 1.02 | 🔴 1.75 | 🔴 5.10 | 🟢 -0.00 | 🔴 -0.27 | 🔴 2.00 | 🔴 1.99 | 🟢 1.94 | 🔴 0.67 | 🟡 1.00 | 🔴 -0.02 | 🟢 3.87 | — — |
| `CY_PRD` | 🟢 2.04 | 🔴 0.88 | 🔴 1.74 | 🔴 11.25 | 🟢 0.35 | 🔴 -0.00 | 🔴 2.00 | 🟡 1.60 | 🟢 1.73 | 🔴 0.54 | 🟡 1.00 | 🔴 0.01 | 🟢 3.78 | — — |
| `CY_TRD` | 🔴 1.46 | — — | 🔴 1.86 | 🔴 4.95 | 🟠 0.90 | — — | 🔴 2.00 | — — | — — | 🔴 0.58 | 🟡 1.00 | — — | 🟢 2.87 | — — |
| `CY_UEM` | 🔴 0.78 | — — | 🔴 1.55 | 🔴 4.02 | 🟢 0.73 | — — | 🔴 1.85 | — — | — — | 🔴 0.80 | 🔴 0.44 | — — | 🟢 1.51 | — — |

### UMC

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🟡 2.18 | — — | 🔴 1.76 | 🔴 4.65 | 🟡 0.71 | — — | 🔴 2.00 | — — | — — | 🔴 0.62 | 🟠 1.00 | — — | 🟢 2.47 | — — |
| `CY_GDP` | 🔴 0.87 | 🔴 0.54 | 🔴 0.62 | 🔴 5.10 | 🔴 0.96 | 🔴 -0.00 | 🔴 1.99 | 🔴 1.06 | 🟠 0.28 | 🔴 0.98 | 🔴 0.19 | 🔴 0.02 | 🟢 0.70 | — — |
| `CY_INV` | 🔴 1.44 | 🔴 0.33 | 🟢 2.67 | 🔴 7.94 | 🟡 0.88 | 🔴 0.51 | 🔴 2.00 | 🟢 1.04 | 🔴 0.96 | 🔴 0.77 | 🔴 0.64 | 🔴 0.11 | 🟢 3.16 | — — |
| `CY_POP` | 🟢 2.13 | 🔴 0.44 | 🔴 1.82 | 🔴 6.52 | 🟢 0.14 | 🟡 0.96 | 🔴 2.00 | 🔴 1.95 | 🟢 2.01 | 🔴 0.56 | 🟡 1.00 | 🔴 0.04 | 🟢 3.84 | — — |
| `CY_PRD` | 🟢 1.98 | 🔴 0.21 | 🔴 1.74 | 🟡 3.45 | 🟢 0.18 | 🟡 0.96 | 🔴 2.00 | 🔴 1.87 | 🟢 1.87 | 🔴 0.95 | 🟡 1.00 | 🔴 0.05 | 🟢 3.97 | — — |
| `CY_TRD` | 🟠 1.76 | 🟢 2.76 | 🔴 1.88 | 🔴 9.43 | 🔴 0.93 | 🔴 0.15 | 🔴 2.00 | 🟡 1.61 | 🟠 1.28 | 🔴 0.53 | 🟡 1.00 | 🔴 0.05 | 🟢 3.31 | — — |
| `CY_UEM` | 🟠 1.93 | — — | 🔴 1.98 | 🟡 1.78 | 🟢 0.81 | — — | 🟢 1.06 | — — | — — | 🟡 1.24 | 🔴 0.42 | — — | 🟢 1.85 | — — |

### WLD

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CY_FIN` | 🔴 1.65 | — — | 🔴 1.65 | 🔴 4.22 | 🟡 0.84 | — — | 🟢 1.07 | — — | — — | 🔴 0.94 | 🔴 0.55 | — — | 🟢 2.66 | — — |
| `CY_GDP` | 🔴 0.65 | 🔴 0.92 | 🟡 0.77 | 🔴 3.14 | 🔴 0.99 | 🔴 -0.24 | 🟠 1.52 | 🔴 3.63 | 🔴 -0.02 | 🟢 1.39 | 🟡 0.44 | 🔴 0.03 | 🟢 0.46 | — — |
| `CY_INV` | 🔴 1.11 | — — | 🔴 1.85 | 🔴 3.17 | 🟢 0.87 | — — | 🔴 2.00 | — — | — — | 🔴 0.77 | 🔴 0.25 | — — | 🟠 1.57 | — — |
| `CY_POP` | 🟢 2.15 | 🔴 0.16 | 🔴 1.78 | 🔴 7.36 | 🟢 0.09 | 🟡 0.97 | 🔴 2.00 | 🔴 1.96 | 🟢 2.02 | 🔴 0.57 | 🟡 1.00 | 🔴 0.02 | 🟢 3.87 | — — |
| `CY_PRD` | 🟢 2.01 | 🔴 0.88 | 🔴 1.72 | 🔴 7.13 | 🟢 0.36 | 🔴 0.75 | 🔴 2.00 | 🟡 1.67 | 🟢 1.73 | 🔴 0.69 | 🟡 0.97 | 🔴 0.01 | 🟢 3.81 | — — |
| `CY_TRD` | 🔴 1.59 | — — | 🔴 1.87 | 🔴 4.77 | 🟢 0.83 | — — | 🔴 2.00 | — — | — — | 🔴 0.52 | 🟡 1.00 | — — | 🟢 3.08 | — — |
| `CY_UEM` | 🔴 1.10 | — — | 🔴 1.90 | 🔴 2.45 | 🟡 0.85 | — — | 🟡 1.18 | — — | — — | 🔴 1.05 | 🔴 0.25 | — — | 🟢 1.59 | — — |

## Panel trimestriel (Path 5)

### EA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `Q_CREDIT` | 🔴 0.97 | 🔴 0.45 | 🔴 0.81 | 🟡 2.82 | 🔴 1.00 | 🟠 0.50 | 🟠 1.73 | 🔴 2.30 | 🔴 0.16 | 🟢 1.36 | 🟢 0.64 | 🟡 0.07 | 🟢 0.81 | 🟢 0.53 |
| `Q_GDP` | 🟢 0.99 | 🟢 1.57 | 🔴 -0.45 | 🟢 1.08 | 🔴 1.00 | 🔴 0.40 | 🟡 1.49 | 🔴 3.87 | 🟠 -0.07 | 🟢 1.91 | 🟡 0.23 | 🟠 0.06 | 🟢 1.47 | 🟢 0.30 |
| `Q_HPI` | 🟢 1.04 | 🔴 0.58 | 🟢 1.05 | 🔴 3.62 | 🔴 0.99 | 🔴 -0.27 | 🔴 2.00 | 🔴 1.72 | 🟡 0.23 | 🔴 1.06 | 🔴 0.10 | 🟡 0.07 | 🔴 0.82 | 🔴 0.22 |
| `Q_INV` | 🟢 0.64 | 🟢 1.80 | 🔴 -0.36 | 🟢 1.65 | 🔴 0.98 | 🟢 0.76 | 🟢 1.10 | 🔴 2.16 | 🟢 -0.15 | 🟢 1.81 | 🟡 0.23 | 🟢 0.08 | 🟢 1.93 | 🟢 0.35 |
| `Q_PRD` | 🟠 0.64 | 🟠 0.59 | 🔴 -0.01 | 🟢 1.72 | 🔴 1.00 | 🔴 0.34 | 🟠 1.68 | 🔴 5.87 | 🔴 -0.01 | 🟢 1.63 | 🟡 0.24 | 🔴 0.05 | 🟢 0.63 | 🟠 0.22 |
| `Q_YIELD` | 🔴 1.56 | 🔴 0.56 | 🟢 2.32 | 🔴 8.61 | 🟢 0.88 | 🔴 -0.32 | 🔴 2.00 | 🔴 1.90 | 🔴 1.14 | 🔴 0.68 | 🟢 0.99 | 🔴 0.10 | 🟠 6.62 | 🔴 0.84 |

### G7Q

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `Q_CPI` | 🔴 0.95 | 🔴 0.15 | 🔴 0.98 | 🟢 2.32 | 🔴 0.99 | 🔴 -0.39 | 🟢 1.51 | 🔴 2.33 | 🟡 0.26 | 🟢 1.59 | 🟢 0.42 | 🔴 0.06 | 🟢 2.31 | 🟡 0.35 |
| `Q_CREDIT` | 🟢 0.74 | 🟢 0.94 | 🟢 0.38 | 🟢 2.46 | 🟠 0.99 | 🔴 -0.48 | 🟢 1.59 | 🔴 18.08 | 🔴 0.02 | 🟢 1.54 | 🟢 0.23 | 🔴 0.06 | 🟢 1.40 | 🟢 0.33 |
| `Q_GDP` | 🟢 0.69 | 🟢 1.32 | 🔴 -0.12 | 🟢 2.00 | 🔴 1.00 | 🔴 -0.31 | 🟢 1.21 | 🔴 2.72 | 🟢 -0.10 | 🟢 1.92 | 🟢 0.31 | 🔴 0.06 | 🟢 1.93 | 🟢 0.35 |
| `Q_HPI` | 🟢 1.10 | 🔴 0.59 | 🔴 0.71 | 🟢 2.70 | 🔴 1.00 | 🔴 -0.45 | 🟢 1.48 | 🔴 2.15 | 🔴 0.20 | 🟢 1.35 | 🔴 0.23 | 🔴 0.06 | 🟢 1.96 | 🔴 0.25 |
| `Q_INV` | 🟡 0.69 | 🟢 0.76 | 🔴 0.06 | 🟢 2.14 | 🟢 0.99 | 🔴 -0.40 | 🟢 1.44 | 🔴 4.09 | 🟡 -0.05 | 🟢 1.67 | 🟡 0.20 | 🔴 0.05 | 🟢 1.19 | 🟢 0.36 |
| `Q_PRD` | 🟠 0.66 | 🟢 0.82 | 🟠 0.26 | 🟡 3.26 | 🔴 1.00 | 🔴 -0.51 | 🟢 1.47 | 🔴 5.65 | 🔴 0.01 | 🟢 1.49 | 🟢 0.36 | 🔴 0.06 | 🟢 0.93 | 🟢 0.41 |
| `Q_UNRATE` | 🟡 1.62 | 🟠 0.67 | 🟢 2.20 | 🟠 4.09 | 🟢 0.82 | 🔴 -0.16 | 🟡 1.28 | 🟢 1.32 | 🔴 1.00 | 🟡 1.20 | 🔴 0.13 | 🟢 0.16 | 🟢 7.34 | 🔴 0.35 |
| `Q_YIELD` | 🟠 1.59 | 🔴 0.61 | 🟢 2.24 | 🟠 4.94 | 🟢 0.90 | 🔴 -0.27 | 🔴 2.00 | 🟠 1.82 | 🟠 1.19 | 🔴 0.83 | 🔴 0.59 | 🔴 0.12 | 🔴 7.51 | 🔴 0.86 |

### GBR

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `Q_CPI` | 🟡 1.01 | 🔴 0.22 | 🔴 0.96 | 🟢 2.29 | 🔴 0.98 | 🔴 -0.45 | 🟢 1.38 | 🔴 2.31 | 🟡 0.26 | 🟢 1.62 | 🟢 0.47 | 🔴 0.06 | 🟢 1.74 | 🟠 0.33 |
| `Q_CREDIT` | 🟡 0.69 | 🟡 0.75 | 🔴 0.07 | 🟢 2.71 | 🔴 0.99 | 🔴 -0.48 | 🔴 2.00 | 🔴 2.74 | 🔴 -0.01 | 🟢 1.60 | 🟠 0.16 | 🔴 0.05 | 🟢 0.61 | 🟢 0.35 |
| `Q_GDP` | 🟢 0.70 | 🟢 1.36 | 🔴 -0.40 | 🟢 1.72 | 🔴 1.00 | 🔴 -0.27 | 🟢 1.19 | 🔴 2.29 | 🟢 -0.10 | 🟢 1.95 | 🟢 0.23 | 🟠 0.06 | 🟢 1.10 | 🟢 0.22 |
| `Q_HPI` | 🟢 1.06 | 🔴 0.37 | 🔴 0.84 | 🟢 3.10 | 🟡 0.96 | 🔴 -0.50 | 🔴 1.89 | 🔴 2.03 | 🔴 0.20 | 🟢 1.27 | 🔴 0.15 | 🔴 0.06 | 🔴 1.03 | 🔴 0.28 |
| `Q_INV` | 🟡 0.61 | 🔴 0.30 | 🔴 -0.10 | 🟢 2.53 | 🔴 1.00 | 🔴 -0.03 | 🟡 1.62 | 🔴 4.03 | 🟡 -0.05 | 🟢 1.66 | 🔴 0.09 | 🟢 0.06 | 🟢 0.48 | 🟡 0.25 |
| `Q_UNRATE` | 🟢 1.81 | 🟡 0.86 | 🟢 2.68 | 🟠 5.12 | 🟢 0.80 | 🔴 -0.35 | 🔴 2.00 | 🟢 1.85 | 🟢 1.36 | 🔴 0.78 | 🔴 0.45 | 🟠 0.16 | 🟡 6.57 | 🔴 0.57 |
| `Q_YIELD` | 🔴 1.48 | 🔴 0.57 | 🟢 2.03 | 🔴 8.02 | 🟢 0.92 | 🔴 -0.30 | 🔴 2.00 | 🟡 1.80 | 🔴 1.02 | 🔴 0.76 | 🔴 0.77 | 🔴 0.10 | 🔴 6.88 | 🔴 0.91 |

### JPN

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `Q_CPI` | 🟠 0.97 | 🔴 0.19 | 🔴 0.88 | 🟢 2.57 | 🟡 0.97 | 🔴 -0.64 | 🟠 1.77 | 🔴 2.84 | 🟡 0.22 | 🟢 1.71 | 🟢 0.54 | 🔴 0.06 | 🟢 1.38 | 🟢 0.53 |
| `Q_CREDIT` | 🔴 0.79 | 🔴 0.47 | 🟡 0.84 | 🔴 3.93 | 🟢 0.96 | 🔴 -0.27 | 🔴 1.87 | 🔴 6.40 | 🔴 0.07 | 🟢 1.41 | 🟢 0.27 | 🔴 0.06 | 🟠 0.63 | 🔴 0.15 |
| `Q_GDP` | 🟢 0.74 | 🟡 0.67 | 🔴 -0.27 | 🟢 1.99 | 🔴 1.00 | 🟠 0.51 | 🟡 1.55 | 🔴 7.98 | 🔴 -0.00 | 🟢 1.77 | 🔴 0.09 | 🔴 0.05 | 🟢 0.42 | 🔴 0.14 |
| `Q_HPI` | 🟡 1.05 | 🔴 0.53 | 🔴 1.09 | 🟡 3.33 | 🔴 0.97 | 🔴 -0.21 | 🔴 2.00 | 🟡 1.64 | 🔴 0.22 | 🟡 1.15 | 🟢 0.59 | 🔴 0.07 | 🟢 2.53 | 🟢 0.67 |
| `Q_UNRATE` | 🟢 1.75 | 🟢 1.09 | 🟢 2.34 | 🔴 5.74 | 🟢 0.91 | 🟡 0.37 | 🔴 1.75 | 🟢 1.72 | 🟡 1.25 | 🔴 0.84 | 🔴 0.68 | 🔴 0.12 | 🔴 7.42 | 🔴 0.78 |
| `Q_YIELD` | 🟠 1.64 | 🔴 0.80 | 🟡 2.08 | 🟡 3.41 | 🟢 0.91 | 🔴 -0.46 | 🟢 1.09 | 🟢 1.75 | 🔴 1.13 | 🟡 1.20 | 🔴 0.72 | 🔴 0.08 | 🟢 5.38 | 🔴 0.74 |

### OECDQ

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `Q_CPI` | 🔴 0.95 | 🔴 0.15 | 🔴 0.98 | 🟢 2.32 | 🔴 0.99 | 🔴 -0.39 | 🟢 1.51 | 🔴 2.33 | 🟡 0.26 | 🟢 1.59 | 🟢 0.42 | 🔴 0.06 | 🟢 2.31 | 🟡 0.35 |
| `Q_CREDIT` | 🟢 0.74 | 🟢 0.94 | 🟢 0.38 | 🟢 2.46 | 🟠 0.99 | 🔴 -0.48 | 🟢 1.59 | 🔴 18.08 | 🔴 0.02 | 🟢 1.54 | 🟢 0.23 | 🔴 0.06 | 🟢 1.40 | 🟢 0.33 |
| `Q_GDP` | 🟢 0.69 | 🟢 1.32 | 🔴 -0.12 | 🟢 2.00 | 🔴 1.00 | 🔴 -0.31 | 🟢 1.21 | 🔴 2.72 | 🟢 -0.10 | 🟢 1.92 | 🟢 0.31 | 🔴 0.06 | 🟢 1.93 | 🟢 0.35 |
| `Q_HPI` | 🟢 1.10 | 🔴 0.59 | 🔴 0.71 | 🟢 2.70 | 🔴 1.00 | 🔴 -0.45 | 🟢 1.48 | 🔴 2.15 | 🔴 0.20 | 🟢 1.35 | 🔴 0.23 | 🔴 0.06 | 🟢 1.96 | 🔴 0.25 |
| `Q_INV` | 🟡 0.69 | 🟢 0.76 | 🔴 0.06 | 🟢 2.14 | 🟢 0.99 | 🔴 -0.40 | 🟢 1.44 | 🔴 4.09 | 🟡 -0.05 | 🟢 1.67 | 🟡 0.20 | 🔴 0.05 | 🟢 1.19 | 🟢 0.36 |
| `Q_PRD` | 🟠 0.66 | 🟢 0.82 | 🟠 0.26 | 🟡 3.26 | 🔴 1.00 | 🔴 -0.51 | 🟢 1.47 | 🔴 5.65 | 🔴 0.01 | 🟢 1.49 | 🟢 0.36 | 🔴 0.06 | 🟢 0.93 | 🟢 0.41 |
| `Q_UNRATE` | 🟡 1.62 | 🟠 0.67 | 🟢 2.20 | 🟠 4.09 | 🟢 0.82 | 🔴 -0.16 | 🟡 1.28 | 🟢 1.32 | 🔴 1.00 | 🟡 1.20 | 🔴 0.13 | 🟢 0.16 | 🟢 7.34 | 🔴 0.35 |
| `Q_YIELD` | 🟠 1.59 | 🔴 0.61 | 🟢 2.24 | 🟠 4.94 | 🟢 0.90 | 🔴 -0.27 | 🔴 2.00 | 🟠 1.82 | 🟠 1.19 | 🔴 0.83 | 🔴 0.59 | 🔴 0.12 | 🔴 7.51 | 🔴 0.86 |

### USA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `Q_CPI` | 🟠 1.13 | 🔴 0.41 | 🔴 1.11 | 🟢 2.60 | 🔴 1.00 | 🔴 -0.01 | 🟢 1.20 | 🟢 0.47 | 🟠 0.36 | 🟢 1.42 | 🟡 0.38 | 🔴 0.08 | 🟢 3.14 | 🔴 0.28 |
| `Q_CREDIT` | 🟢 0.93 | 🟡 0.76 | 🟢 0.93 | 🔴 4.96 | 🔴 0.99 | 🔴 -0.24 | 🟠 1.80 | 🟢 0.84 | 🟡 0.12 | 🟡 1.13 | 🔴 0.15 | 🔴 0.06 | 🟢 0.80 | 🟢 0.46 |
| `Q_GDP` | 🟢 0.74 | 🟢 0.93 | 🔴 0.04 | 🟢 2.84 | 🔴 1.00 | 🔴 -0.11 | 🟢 1.29 | 🔴 3.38 | 🟡 -0.04 | 🟢 1.86 | 🟢 0.20 | 🔴 0.05 | 🟢 0.99 | 🟡 0.24 |
| `Q_HPI` | 🟡 1.19 | 🔴 0.61 | 🔴 0.97 | 🟡 2.99 | 🔴 0.98 | 🔴 -0.08 | 🔴 1.74 | 🔴 1.73 | 🟡 0.42 | 🟢 1.43 | 🔴 0.27 | 🔴 0.07 | 🟢 2.41 | 🔴 0.17 |
| `Q_INV` | 🟡 0.98 | 🟡 0.86 | 🔴 0.63 | 🟢 2.35 | 🔴 0.99 | 🔴 -0.31 | 🟢 1.55 | 🟢 0.50 | 🔴 0.11 | 🟢 1.50 | 🔴 0.17 | 🔴 0.06 | 🟢 1.24 | 🔴 0.22 |
| `Q_PRD` | 🔴 0.60 | 🟢 0.89 | 🟡 0.20 | 🔴 5.19 | 🔴 1.00 | 🔴 -0.20 | 🟢 1.41 | 🔴 3.34 | 🔴 -0.01 | 🟢 1.36 | 🔴 0.11 | 🔴 0.05 | 🟡 0.42 | 🔴 0.20 |
| `Q_UNRATE` | 🟢 1.50 | 🟢 1.20 | 🔴 1.37 | 🟡 2.84 | 🟢 0.82 | 🔴 0.24 | 🔴 2.00 | 🟢 0.10 | 🔴 0.63 | 🟢 1.16 | 🔴 0.31 | 🟢 0.15 | 🟢 6.52 | 🔴 0.36 |
| `Q_YIELD` | 🔴 1.50 | 🟡 0.87 | 🟢 2.24 | 🟡 3.41 | 🟢 0.91 | 🔴 -0.26 | 🔴 1.69 | 🟢 1.75 | 🔴 1.03 | 🟠 1.09 | 🔴 0.60 | 🔴 0.12 | 🔴 6.81 | 🔴 0.82 |

## Histoire longue (1870-2022)

### ADV18

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `LH_BANKDEBT` | 🟢 2.03 | 🟡 1.09 | 🔴 1.86 | 🟡 2.82 | 🟢 0.60 | 🟢 0.91 | 🟢 0.50 | 🟡 1.80 | 🟢 1.47 | 🟢 1.44 | 🟡 0.99 | 🟢 0.15 | 🟢 5.64 | 🟡 1.00 |
| `LH_BILLRATE` | 🔴 1.29 | 🟢 1.16 | 🔴 1.25 | 🟢 1.92 | 🟢 0.83 | 🟢 0.78 | 🔴 1.44 | 🟡 1.25 | 🟢 0.25 | 🟢 1.94 | 🟡 0.95 | 🟢 0.10 | 🟢 4.48 | 🟡 1.00 |
| `LH_BONDRATE` | 🔴 1.29 | 🟢 1.48 | 🔴 1.25 | 🟢 1.94 | 🟢 0.83 | 🟢 0.78 | 🔴 1.45 | 🟡 1.25 | 🟢 0.25 | 🟢 1.94 | 🟡 0.95 | 🟢 0.10 | 🟢 4.49 | 🟡 1.00 |
| `LH_BONDTR` | 🔴 1.29 | 🟢 1.44 | 🔴 1.25 | 🟢 1.94 | 🟢 0.84 | 🟢 0.80 | 🔴 1.46 | 🟡 1.25 | 🟢 0.25 | 🟢 1.94 | 🟡 0.95 | 🟢 0.09 | 🟢 4.49 | 🟡 1.00 |
| `LH_BUSCREDIT` | 🟢 1.91 | 🟢 1.33 | 🟠 2.00 | 🟡 3.14 | 🟢 0.62 | 🟢 0.96 | 🟢 0.50 | 🟠 1.83 | 🟡 1.27 | 🟢 1.51 | 🟡 0.96 | 🟢 0.15 | 🟢 5.68 | 🟡 1.00 |
| `LH_CA` | 🔴 1.41 | 🟢 2.55 | 🟢 2.11 | 🟢 2.00 | 🔴 0.96 | 🟢 0.98 | 🟢 0.50 | 🟢 1.65 | 🔴 0.54 | 🟢 1.77 | 🔴 0.50 | 🟢 0.13 | 🟢 4.44 | 🔴 0.64 |
| `LH_CPI` | 🔴 1.24 | 🟢 2.16 | 🔴 1.41 | 🟢 1.43 | 🟢 0.54 | 🟢 0.80 | 🔴 2.00 | 🟢 1.13 | 🟢 0.32 | 🟢 1.92 | 🟢 1.00 | 🟢 0.11 | 🟢 2.35 | 🟡 1.00 |
| `LH_CREDIT` | 🔴 1.48 | 🟢 1.39 | 🔴 1.89 | 🟡 3.93 | 🟢 0.55 | 🟢 0.93 | 🟢 0.50 | 🟢 1.12 | 🔴 0.86 | 🟢 1.48 | 🟡 0.95 | 🔴 0.11 | 🟢 5.14 | 🟠 0.94 |
| `LH_DEBTGDP` | 🟡 1.63 | 🔴 0.23 | 🔴 1.89 | 🟡 3.65 | 🟢 0.79 | 🔴 0.17 | 🔴 2.00 | 🔴 1.88 | 🔴 1.13 | 🔴 1.03 | 🔴 0.31 | 🔴 0.13 | 🟢 4.89 | 🔴 0.54 |
| `LH_EQDIVP` | 🔴 1.29 | 🟢 1.28 | 🔴 1.26 | 🟢 1.98 | 🟢 0.85 | 🟢 0.79 | 🔴 1.44 | 🟡 1.24 | 🟢 0.25 | 🟢 1.94 | 🟡 0.95 | 🟢 0.08 | 🟢 4.53 | 🟡 1.00 |
| `LH_EQTR` | 🟢 1.04 | 🟢 1.92 | 🔴 -0.00 | 🟡 2.99 | 🟢 0.83 | 🔴 0.25 | 🟡 1.52 | 🔴 1.00 | 🟡 0.07 | 🟢 1.97 | 🟢 0.93 | 🔴 0.06 | 🔴 -0.02 | 🟢 0.99 |
| `LH_EQUITY` | 🟢 1.04 | 🟢 1.93 | 🔴 -0.00 | 🟡 2.98 | 🟢 0.84 | 🔴 0.24 | 🟢 1.49 | 🔴 1.00 | 🟡 0.07 | 🟢 1.97 | 🟢 0.91 | 🟢 0.07 | 🔴 -0.02 | 🟢 0.97 |
| `LH_EXP` | 🟢 1.97 | 🔴 0.18 | 🔴 1.53 | 🟡 3.02 | 🟢 0.72 | 🟢 0.97 | 🟢 0.50 | 🟢 1.53 | 🟢 1.50 | 🟡 1.33 | 🟡 1.00 | 🟢 0.13 | 🟢 5.85 | 🟡 1.00 |
| `LH_EXPORTS` | 🟢 1.98 | 🟡 1.10 | 🟡 2.14 | 🟡 2.68 | 🟢 0.63 | 🟢 0.97 | 🟢 0.50 | 🟢 1.66 | 🟢 1.47 | 🟢 1.43 | 🟡 0.97 | 🟠 0.13 | 🟢 5.66 | 🟡 1.00 |
| `LH_GDP` | 🟢 1.90 | 🔴 0.62 | 🟢 2.21 | 🔴 8.35 | 🟢 0.63 | 🟢 0.89 | 🔴 2.00 | 🟢 0.14 | 🔴 0.94 | 🔴 0.98 | 🟡 0.97 | 🔴 0.04 | 🟢 5.95 | 🟡 0.98 |
| `LH_GDPNOM` | 🟢 2.02 | 🔴 0.17 | 🟠 2.00 | 🟠 5.58 | 🟢 0.56 | 🟢 0.95 | 🟢 0.50 | 🟡 1.79 | 🟢 1.65 | 🟡 1.30 | 🟡 1.00 | 🔴 0.11 | 🟢 5.81 | 🟡 1.00 |
| `LH_HHCREDIT` | 🟢 2.11 | 🟡 0.99 | 🔴 1.91 | 🟡 3.63 | 🟢 0.57 | 🟢 0.97 | 🟢 0.50 | 🟢 1.77 | 🟢 1.51 | 🟢 1.46 | 🟠 0.93 | 🟠 0.12 | 🟢 5.41 | 🟡 1.00 |
| `LH_HOUSECG` | 🔴 1.28 | 🟠 0.86 | 🔴 1.35 | 🟢 1.92 | 🟢 0.83 | 🟢 0.76 | 🔴 1.54 | 🟡 1.25 | 🟢 0.25 | 🟢 1.94 | 🟡 0.93 | 🟢 0.11 | 🟢 4.36 | 🟡 0.99 |
| `LH_HOUSINGTR` | 🔴 1.27 | 🔴 0.56 | 🔴 1.34 | 🟢 1.91 | 🟢 0.85 | 🟢 0.74 | 🔴 1.52 | 🟡 1.25 | 🟢 0.25 | 🟢 1.94 | 🟡 0.92 | 🟢 0.11 | 🟢 4.35 | 🟡 0.99 |
| `LH_HPI` | 🟢 1.75 | 🔴 0.68 | 🟡 2.05 | 🟡 3.60 | 🟢 0.66 | 🟢 0.91 | 🟢 1.12 | 🟢 1.25 | 🔴 1.17 | 🟢 1.32 | 🟢 1.00 | 🔴 0.08 | 🟢 5.96 | 🟡 1.00 |
| `LH_IMPORTS` | 🟢 1.89 | 🟢 1.73 | 🟡 2.09 | 🟡 3.94 | 🟢 0.77 | 🟢 0.95 | 🟢 0.50 | 🟢 1.75 | 🟡 1.41 | 🟡 1.37 | 🟡 0.99 | 🟡 0.13 | 🟢 5.71 | 🟡 1.00 |
| `LH_INV` | 🔴 1.26 | 🔴 0.55 | 🔴 1.89 | 🔴 5.50 | 🟠 0.93 | 🔴 -0.04 | 🔴 2.00 | 🟢 1.50 | 🔴 0.83 | 🔴 0.42 | 🟢 0.97 | 🟡 0.11 | 🟢 5.29 | 🟠 0.96 |
| `LH_LEV` | 🔴 1.12 | 🟢 1.81 | 🔴 1.21 | 🟢 1.50 | 🟢 0.89 | 🟢 0.62 | 🟢 0.50 | 🟡 1.22 | 🟢 0.22 | 🟢 1.94 | 🟡 0.92 | 🟡 0.07 | 🟢 1.94 | 🟡 1.00 |
| `LH_MONEY` | 🟢 2.00 | 🟢 1.25 | 🔴 1.73 | 🟡 2.92 | 🟢 0.41 | 🟢 0.97 | 🟢 0.50 | 🔴 1.87 | 🟢 1.57 | 🟢 1.40 | 🟡 1.00 | 🔴 0.10 | 🟢 5.77 | 🟡 1.00 |
| `LH_MORT` | 🟢 1.77 | 🟢 1.55 | 🟡 2.09 | 🟢 0.98 | 🟢 0.47 | 🟢 0.96 | 🟢 0.50 | 🟢 1.53 | 🔴 1.00 | 🟢 1.61 | 🟡 0.99 | 🔴 0.14 | 🟢 5.31 | 🟠 1.00 |
| `LH_NARROW` | 🟢 1.96 | 🟢 2.01 | 🔴 1.61 | 🟡 2.51 | 🟢 0.55 | 🟢 0.97 | 🟢 0.50 | 🔴 1.87 | 🟠 1.23 | 🟢 1.69 | 🟡 0.97 | 🟢 0.13 | 🟢 5.30 | 🟡 1.00 |
| `LH_POP` | 🟢 1.84 | 🟢 1.26 | 🔴 1.80 | 🔴 15.71 | 🟢 0.74 | 🔴 0.10 | 🔴 2.00 | 🟢 1.43 | 🟢 1.46 | 🔴 0.52 | 🟠 0.93 | 🔴 0.06 | 🟢 5.67 | 🟡 1.00 |
| `LH_RCONS` | 🟢 1.98 | 🔴 0.54 | 🔴 1.92 | 🔴 10.77 | 🟢 0.68 | 🟢 0.85 | 🔴 2.00 | 🟢 1.72 | 🟢 1.80 | 🔴 0.80 | 🟡 0.99 | 🔴 0.07 | 🟢 6.04 | 🟡 1.00 |
| `LH_REV` | 🟢 1.92 | 🔴 0.47 | 🔴 1.85 | 🟡 3.70 | 🟢 0.61 | 🟢 0.96 | 🟢 0.50 | 🟡 1.77 | 🟢 1.58 | 🟡 1.29 | 🟡 1.00 | 🟢 0.13 | 🟢 5.81 | 🟡 1.00 |
| `LH_RGDP_BARRO` | 🟢 1.97 | 🔴 0.42 | 🔴 1.88 | 🔴 11.05 | 🟢 0.64 | 🟢 0.88 | 🔴 2.00 | 🟠 1.83 | 🟢 1.80 | 🔴 0.80 | 🟠 0.96 | 🔴 0.04 | 🟢 6.05 | 🟡 1.00 |
| `LH_STIR` | 🔴 1.53 | 🔴 0.11 | 🔴 1.85 | 🟡 3.57 | 🟠 0.94 | 🟢 0.80 | 🟢 0.50 | 🔴 1.81 | 🔴 1.05 | 🟡 1.27 | 🔴 0.30 | 🔴 0.11 | 🟢 4.56 | 🔴 0.42 |
| `LH_UNRATE` | 🔴 1.41 | 🟡 1.20 | 🟢 2.14 | 🟡 2.89 | 🟢 0.89 | 🔴 -0.09 | 🔴 2.00 | 🟡 1.69 | 🔴 0.73 | 🟡 1.11 | 🔴 0.26 | 🟡 0.11 | 🟢 3.78 | 🟠 0.78 |
| `LH_WAGE` | 🟢 2.07 | 🔴 0.30 | 🔴 1.79 | 🟡 3.90 | 🟢 0.44 | 🟢 0.94 | 🟠 1.45 | 🔴 1.98 | 🟢 1.92 | 🟠 1.17 | 🟡 1.00 | 🔴 0.09 | 🟢 6.02 | 🟡 1.00 |
| `LH_XRUSD` | 🔴 1.51 | 🟢 2.28 | 🔴 1.88 | 🟡 4.75 | 🟡 0.92 | 🟢 0.66 | 🔴 2.00 | 🟡 1.75 | 🔴 0.95 | 🔴 0.68 | 🟡 1.00 | 🟡 0.13 | 🟢 5.51 | 🟡 1.00 |
| `LH_YIELD` | 🟡 1.66 | 🟢 1.41 | 🟢 2.13 | 🟡 4.05 | 🟢 0.91 | 🟢 0.71 | 🟢 1.25 | 🟢 1.62 | 🟠 1.13 | 🟢 1.31 | 🔴 0.45 | 🔴 0.11 | 🟢 4.90 | 🔴 0.47 |

### ANGLO

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `LH_BANKDEBT` | 🟢 1.76 | 🟢 1.41 | 🔴 1.78 | 🟢 1.56 | 🟢 0.63 | 🟢 0.94 | 🟢 0.50 | 🟠 1.84 | 🟢 1.61 | 🟢 1.52 | 🟡 1.00 | 🟢 0.18 | 🟢 5.08 | 🟡 1.00 |
| `LH_BILLRATE` | 🔴 1.48 | 🟢 1.56 | 🔴 1.34 | 🟡 3.04 | 🟢 0.74 | 🟢 0.69 | 🔴 2.00 | 🟡 1.19 | 🟢 0.31 | 🟢 1.88 | 🟡 0.97 | 🟢 0.09 | 🟢 5.93 | 🟡 1.00 |
| `LH_BONDRATE` | 🔴 1.52 | 🟢 1.49 | 🔴 1.34 | 🟡 3.04 | 🟢 0.76 | 🟢 0.72 | 🔴 2.00 | 🟡 1.19 | 🟢 0.31 | 🟢 1.88 | 🟡 0.99 | 🟢 0.09 | 🟢 5.95 | 🟡 1.00 |
| `LH_BONDTR` | 🔴 1.51 | 🟢 1.30 | 🔴 1.35 | 🟡 3.03 | 🟢 0.79 | 🟢 0.76 | 🔴 2.00 | 🟡 1.19 | 🟢 0.31 | 🟢 1.88 | 🟡 0.99 | 🟢 0.09 | 🟢 5.94 | 🟡 1.00 |
| `LH_BUSCREDIT` | 🔴 1.53 | 🔴 0.55 | 🔴 1.75 | 🟢 1.16 | 🟢 0.69 | 🟢 0.93 | 🟢 0.50 | 🔴 1.85 | 🟢 1.51 | 🟢 1.60 | 🟡 1.00 | 🟢 0.19 | 🟢 5.07 | 🟡 1.00 |
| `LH_CA` | 🔴 1.49 | 🔴 0.55 | 🔴 1.74 | 🟡 2.62 | 🔴 0.99 | 🟢 0.97 | 🟢 0.50 | 🟢 1.28 | 🔴 0.52 | 🟢 1.50 | 🟠 0.79 | 🟠 0.10 | 🟢 5.23 | 🟡 0.93 |
| `LH_CPI` | 🟢 2.04 | 🔴 0.36 | 🔴 1.80 | 🟡 4.08 | 🟢 0.61 | 🟢 0.79 | 🔴 1.87 | 🔴 1.95 | 🟢 1.90 | 🟠 1.08 | 🟡 0.99 | 🔴 0.11 | 🟢 6.02 | 🟡 1.00 |
| `LH_CREDIT` | 🟢 2.07 | 🟢 1.63 | 🔴 1.72 | 🟢 1.02 | 🟢 0.63 | 🟢 0.93 | 🟢 0.50 | 🔴 1.96 | 🟢 1.58 | 🟢 1.64 | 🟡 0.96 | 🟢 0.14 | 🟢 5.18 | 🟡 1.00 |
| `LH_DEBTGDP` | 🟡 1.65 | 🔴 0.16 | 🟠 1.97 | 🟡 2.57 | 🟢 0.79 | 🔴 0.02 | 🔴 2.00 | 🟡 1.80 | 🔴 1.16 | 🟡 1.19 | 🔴 0.53 | 🟢 0.15 | 🟢 5.26 | 🔴 0.70 |
| `LH_EQDIVP` | 🔴 1.52 | 🟢 1.49 | 🔴 1.37 | 🟡 3.04 | 🟢 0.76 | 🟢 0.72 | 🔴 2.00 | 🟡 1.19 | 🟢 0.31 | 🟢 1.88 | 🟡 0.99 | 🟢 0.09 | 🟢 5.94 | 🟡 1.00 |
| `LH_EQTR` | 🔴 1.52 | 🟢 1.33 | 🔴 1.36 | 🟡 3.04 | 🟢 0.76 | 🟢 0.72 | 🔴 2.00 | 🟡 1.19 | 🟢 0.31 | 🟢 1.88 | 🟡 0.99 | 🟢 0.09 | 🟢 5.94 | 🟡 1.00 |
| `LH_EQUITY` | 🔴 1.52 | 🟢 1.33 | 🔴 1.36 | 🟡 3.04 | 🟢 0.76 | 🟢 0.72 | 🔴 2.00 | 🟡 1.19 | 🟢 0.31 | 🟢 1.88 | 🟡 0.99 | 🟢 0.09 | 🟢 5.94 | 🟡 1.00 |
| `LH_EXP` | 🟢 1.94 | 🟡 1.04 | 🔴 1.60 | 🟢 1.17 | 🟢 0.61 | 🟢 0.96 | 🟢 0.50 | 🟢 0.17 | 🔴 0.71 | 🟢 1.59 | 🟢 0.96 | 🟢 0.17 | 🟢 5.44 | 🟢 1.00 |
| `LH_EXPORTS` | 🟢 1.92 | 🔴 0.70 | 🔴 1.78 | 🟢 1.23 | 🟢 0.86 | 🟢 0.94 | 🟢 0.50 | 🔴 1.84 | 🟡 1.34 | 🟢 1.59 | 🟡 0.99 | 🟡 0.11 | 🟢 5.56 | 🟡 1.00 |
| `LH_GDP` | 🟢 1.85 | 🔴 0.16 | 🔴 1.77 | 🔴 9.57 | 🟢 0.72 | 🟢 0.84 | 🔴 2.00 | 🟠 1.81 | 🟢 1.73 | 🔴 0.87 | 🟡 0.95 | 🔴 0.07 | 🟢 6.08 | 🟡 1.00 |
| `LH_GDPNOM` | 🟢 2.05 | 🔴 0.51 | 🔴 1.72 | 🟢 1.54 | 🟢 0.48 | 🟢 0.95 | 🟢 0.50 | 🔴 1.94 | 🟢 1.68 | 🟢 1.52 | 🟡 0.97 | 🟢 0.14 | 🟢 5.78 | 🟡 1.00 |
| `LH_HHCREDIT` | 🔴 1.41 | 🟡 0.96 | 🔴 1.71 | 🟢 1.14 | 🟢 0.40 | 🟢 1.00 | 🟢 0.50 | 🔴 1.96 | 🟢 1.61 | 🟢 1.62 | 🟡 1.00 | 🟢 0.16 | 🟢 5.12 | 🟡 1.00 |
| `LH_HOUSECG` | 🔴 1.48 | 🔴 0.72 | 🔴 1.43 | 🟡 3.01 | 🟢 0.79 | 🟢 0.70 | 🔴 2.00 | 🟢 1.19 | 🟢 0.31 | 🟢 1.88 | 🟡 0.92 | 🟢 0.11 | 🟢 5.88 | 🟡 1.00 |
| `LH_HOUSINGTR` | 🔴 1.54 | 🟡 0.93 | 🔴 1.31 | 🟢 2.92 | 🟢 0.80 | 🔴 0.39 | 🔴 2.00 | 🟡 1.19 | 🟢 0.32 | 🟢 1.89 | 🔴 0.77 | 🟢 0.13 | 🟢 5.78 | 🟡 1.00 |
| `LH_HPI` | 🟢 2.05 | 🟢 2.08 | 🔴 1.72 | 🟡 2.59 | 🟢 0.73 | 🟢 0.81 | 🟢 0.50 | 🔴 1.92 | 🟢 1.61 | 🟢 1.46 | 🟡 1.00 | 🟡 0.12 | 🟢 5.86 | 🟡 1.00 |
| `LH_IMPORTS` | 🟢 1.97 | 🔴 0.09 | 🔴 1.89 | 🟡 2.37 | 🟢 0.80 | 🟢 0.95 | 🟢 0.50 | 🟡 1.79 | 🟢 1.46 | 🟢 1.41 | 🟡 0.96 | 🟠 0.13 | 🟢 5.49 | 🟡 1.00 |
| `LH_INV` | 🔴 1.33 | 🔴 0.51 | 🟡 2.02 | 🟡 3.19 | 🟡 0.91 | 🔴 -0.14 | 🔴 2.00 | 🟡 1.70 | 🔴 0.82 | 🔴 0.81 | 🟢 0.93 | 🔴 0.08 | 🟢 5.18 | 🟠 0.92 |
| `LH_LEV` | 🟢 1.73 | 🔴 0.64 | 🔴 1.74 | 🟡 3.27 | 🟢 0.86 | 🔴 -0.63 | 🔴 2.00 | 🟢 1.62 | 🟢 1.38 | 🔴 1.03 | 🟡 0.96 | 🔴 0.07 | 🟢 5.75 | 🟡 0.97 |
| `LH_MONEY` | 🟢 2.07 | 🟢 1.79 | 🔴 1.60 | 🟢 0.96 | 🟢 0.41 | 🟢 0.97 | 🟢 0.50 | 🔴 1.82 | 🟢 1.52 | 🟢 1.64 | 🟡 1.00 | 🟡 0.11 | 🟢 5.37 | 🟡 1.00 |
| `LH_MORT` | 🟢 2.05 | 🟢 2.00 | 🔴 1.69 | 🟢 0.98 | 🟢 0.50 | 🟢 0.94 | 🟢 0.50 | 🔴 1.96 | 🟢 1.56 | 🟢 1.66 | 🟠 0.91 | 🟢 0.16 | 🟢 5.19 | 🟡 1.00 |
| `LH_NARROW` | 🟢 1.93 | 🟢 1.44 | 🔴 1.37 | 🟢 0.97 | 🟢 0.63 | 🟢 0.94 | 🟢 0.50 | 🟡 1.69 | 🔴 1.15 | 🟢 1.77 | 🟡 1.00 | 🟢 0.15 | 🟢 5.16 | 🟡 1.00 |
| `LH_POP` | 🟢 2.00 | 🔴 0.47 | 🔴 1.77 | 🔴 8.44 | 🟢 0.58 | 🔴 0.39 | 🔴 2.00 | 🔴 1.86 | 🟢 1.81 | 🔴 0.60 | 🟡 0.99 | 🔴 0.02 | 🟢 5.84 | 🟡 1.00 |
| `LH_RCONS` | 🟢 1.94 | 🔴 0.42 | 🔴 1.92 | 🔴 7.61 | 🟢 0.69 | 🟢 0.93 | 🔴 2.00 | 🟡 1.77 | 🟢 1.77 | 🔴 0.93 | 🟡 1.00 | 🔴 0.07 | 🟢 6.05 | 🟡 1.00 |
| `LH_REV` | 🟢 1.95 | 🟡 1.05 | 🔴 1.79 | 🟢 1.31 | 🟢 0.62 | 🟢 0.98 | 🟢 0.50 | 🟢 0.12 | 🔴 0.73 | 🟢 1.57 | 🟢 1.00 | 🟢 0.17 | 🟢 5.17 | 🟢 1.00 |
| `LH_RGDP_BARRO` | 🟢 1.93 | 🔴 0.20 | 🔴 1.88 | 🔴 8.32 | 🟢 0.70 | 🟢 0.86 | 🔴 2.00 | 🔴 1.85 | 🟢 1.75 | 🔴 0.84 | 🟠 0.96 | 🔴 0.07 | 🟢 6.03 | 🟡 1.00 |
| `LH_STIR` | 🔴 1.40 | 🟡 1.46 | 🟠 1.88 | 🟢 1.97 | 🔴 0.96 | 🟢 0.72 | 🟢 1.19 | 🔴 1.86 | 🔴 0.85 | 🟢 1.37 | 🔴 0.35 | 🟠 0.10 | 🟢 3.94 | 🔴 0.48 |
| `LH_UNRATE` | 🔴 1.33 | 🟡 1.11 | 🔴 1.51 | 🟢 2.41 | 🟢 0.85 | 🔴 -0.33 | 🔴 1.90 | 🔴 1.91 | 🔴 0.57 | 🟢 1.42 | 🔴 0.17 | 🔴 0.08 | 🟢 3.20 | 🔴 0.59 |
| `LH_WAGE` | 🟢 2.07 | 🔴 0.53 | 🔴 1.75 | 🟡 3.20 | 🟢 0.48 | 🟢 0.96 | 🟠 1.45 | 🔴 1.96 | 🟢 1.86 | 🟡 1.22 | 🟡 1.00 | 🔴 0.09 | 🟢 6.02 | 🟡 1.00 |
| `LH_XRUSD` | 🔴 1.38 | 🟢 1.41 | 🔴 1.66 | 🔴 5.18 | 🔴 0.95 | 🟢 0.63 | 🔴 2.00 | 🟢 1.54 | 🔴 0.75 | 🔴 0.81 | 🟢 1.00 | 🔴 0.08 | 🟢 5.17 | 🟡 1.00 |
| `LH_YIELD` | 🟢 1.76 | 🔴 0.82 | 🟡 2.03 | 🟡 3.85 | 🟢 0.91 | 🟢 0.68 | 🟡 1.26 | 🟡 1.77 | 🟡 1.25 | 🟡 1.32 | 🔴 0.54 | 🔴 0.12 | 🟢 5.24 | 🔴 0.57 |

### EU4

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `LH_BANKDEBT` | 🔴 1.48 | 🟡 0.99 | 🔴 1.87 | 🔴 5.79 | 🟢 0.64 | 🟢 0.98 | 🟡 0.50 | 🟡 1.78 | 🟡 1.37 | 🟢 1.44 | 🟡 0.97 | 🟢 0.19 | 🟢 5.25 | 🟡 1.00 |
| `LH_BILLRATE` | 🔴 1.47 | 🔴 0.56 | 🔴 1.86 | 🟡 3.38 | 🔴 0.95 | 🟢 0.66 | 🟢 0.50 | 🔴 1.83 | 🔴 0.96 | 🟢 1.38 | 🔴 0.32 | 🔴 0.10 | 🟢 4.81 | 🔴 0.45 |
| `LH_BONDRATE` | 🟡 1.65 | 🟢 1.46 | 🟡 2.00 | 🟡 3.33 | 🟡 0.92 | 🟢 0.55 | 🔴 1.57 | 🔴 1.90 | 🔴 1.05 | 🟡 1.33 | 🔴 0.39 | 🔴 0.11 | 🟢 4.78 | 🔴 0.42 |
| `LH_BONDTR` | 🟢 0.80 | 🟡 0.78 | 🔴 0.10 | 🟡 2.85 | 🟠 0.99 | 🟢 0.69 | 🟢 1.51 | 🔴 9.69 | 🟠 0.05 | 🟢 1.36 | 🔴 0.17 | 🟠 0.06 | 🟢 1.02 | 🟢 0.33 |
| `LH_BUSCREDIT` | 🟡 1.92 | 🔴 0.60 | 🟡 2.10 | 🟢 2.20 | 🟢 0.50 | 🟢 0.91 | 🔴 1.73 | 🔴 1.85 | 🟠 1.41 | 🟠 1.12 | 🟡 1.00 | 🟢 0.15 | 🟢 4.09 | 🟠 1.00 |
| `LH_CA` | 🔴 1.43 | 🟢 2.77 | 🟢 2.20 | 🟢 1.82 | 🔴 0.96 | 🟢 0.94 | 🟢 0.50 | 🟢 1.66 | 🔴 0.55 | 🟢 1.80 | 🟠 0.68 | 🟢 0.14 | 🟢 4.39 | 🔴 0.68 |
| `LH_CPI` | 🟢 2.03 | 🔴 0.53 | 🔴 1.82 | 🔴 5.72 | 🟢 0.59 | 🟢 0.84 | 🔴 1.99 | 🔴 1.93 | 🟢 1.92 | 🔴 1.01 | 🟠 0.96 | 🟡 0.13 | 🟢 6.02 | 🟡 1.00 |
| `LH_CREDIT` | 🟢 2.00 | 🔴 0.50 | 🟠 1.98 | 🟡 3.93 | 🟢 0.56 | 🟢 0.97 | 🟢 0.50 | 🟡 1.80 | 🟡 1.32 | 🟢 1.52 | 🟡 0.99 | 🟢 0.20 | 🟢 5.40 | 🟡 1.00 |
| `LH_DEBTGDP` | 🟡 1.57 | 🟢 1.83 | 🟢 2.07 | 🟠 3.72 | 🟢 0.85 | 🔴 -0.03 | 🔴 2.00 | 🟢 1.50 | 🔴 0.85 | 🟠 1.09 | 🔴 0.62 | 🔴 0.10 | 🟢 4.73 | 🔴 0.60 |
| `LH_EQDIVP` | 🔴 1.19 | 🔴 0.48 | 🔴 1.25 | 🟠 3.34 | 🔴 0.97 | 🔴 0.32 | 🔴 2.00 | 🟡 1.71 | 🔴 0.46 | 🟠 1.12 | 🟡 0.51 | 🔴 0.07 | 🟢 2.72 | 🟠 0.55 |
| `LH_EQTR` | 🟢 1.02 | 🔴 0.35 | 🔴 0.00 | 🟡 2.99 | 🟠 0.99 | 🔴 0.02 | 🟢 1.47 | 🔴 1.00 | 🟢 0.07 | 🟢 1.97 | 🟠 0.20 | 🟢 0.15 | 🔴 -0.02 | 🟠 0.25 |
| `LH_EQUITY` | 🟢 1.02 | 🔴 0.35 | 🔴 0.00 | 🟡 2.99 | 🟡 0.99 | 🔴 0.03 | 🟡 1.49 | 🔴 1.00 | 🟢 0.07 | 🟢 1.97 | 🟠 0.20 | 🟢 0.13 | 🔴 -0.02 | 🟢 0.28 |
| `LH_EXP` | 🟢 1.93 | 🔴 0.46 | 🔴 1.60 | 🟡 2.79 | 🟢 0.81 | 🟢 0.96 | 🟢 0.50 | 🟢 1.74 | 🟢 1.46 | 🟡 1.35 | 🟡 0.99 | 🟢 0.16 | 🟢 5.79 | 🟡 1.00 |
| `LH_EXPORTS` | 🟢 1.99 | 🔴 0.81 | 🟡 2.19 | 🟡 2.55 | 🟢 0.69 | 🟢 0.92 | 🟢 0.50 | 🟢 1.62 | 🟡 1.44 | 🟢 1.48 | 🟠 0.96 | 🟠 0.12 | 🟢 5.58 | 🟡 1.00 |
| `LH_GDP` | 🟢 1.88 | 🔴 0.20 | 🔴 1.79 | 🔴 11.18 | 🟢 0.61 | 🟢 0.82 | 🔴 2.00 | 🟡 1.76 | 🟢 1.76 | 🔴 0.81 | 🟡 0.92 | 🔴 0.06 | 🟢 6.08 | 🟡 1.00 |
| `LH_GDPNOM` | 🟢 2.03 | 🔴 0.14 | 🟠 2.01 | 🔴 6.00 | 🟢 0.70 | 🟢 0.95 | 🟢 0.50 | 🟠 1.80 | 🟢 1.62 | 🟡 1.34 | 🟡 1.00 | 🟡 0.13 | 🟢 5.78 | 🟡 1.00 |
| `LH_HHCREDIT` | 🟡 1.98 | 🔴 0.26 | 🔴 2.00 | 🔴 5.02 | 🟢 0.53 | 🟢 0.93 | 🔴 1.78 | 🔴 1.78 | 🟢 1.65 | 🔴 0.93 | 🟡 1.00 | 🟢 0.19 | 🟢 4.11 | 🟠 1.00 |
| `LH_HOUSECG` | 🔴 0.92 | 🔴 0.66 | 🟡 1.35 | 🟢 1.63 | 🔴 0.99 | 🔴 -0.11 | 🔴 1.82 | 🔴 1.87 | 🔴 0.31 | 🟢 1.84 | 🟠 0.36 | 🔴 0.05 | 🟢 1.69 | 🔴 0.38 |
| `LH_HOUSINGTR` | 🔴 0.81 | 🔴 0.57 | 🔴 0.64 | 🟡 2.75 | 🔴 0.99 | 🔴 -0.07 | 🔴 2.00 | 🔴 1.36 | 🟠 0.20 | 🟢 1.27 | 🔴 0.24 | 🔴 0.05 | 🟢 1.14 | 🔴 0.32 |
| `LH_HPI` | 🟢 2.01 | 🔴 0.74 | 🔴 1.75 | 🔴 8.89 | 🟢 0.66 | 🟢 0.84 | 🟡 1.27 | 🔴 1.85 | 🟢 1.56 | 🟡 1.24 | 🔴 0.80 | 🟡 0.13 | 🟢 5.96 | 🟡 1.00 |
| `LH_IMPORTS` | 🟢 1.87 | 🔴 0.61 | 🟡 2.14 | 🟡 3.88 | 🟢 0.79 | 🟢 0.93 | 🟢 0.50 | 🟢 1.74 | 🟡 1.35 | 🟢 1.40 | 🟡 0.97 | 🟢 0.13 | 🟢 5.55 | 🟡 1.00 |
| `LH_INV` | 🔴 1.24 | 🔴 0.80 | 🔴 1.82 | 🔴 14.60 | 🟠 0.93 | 🔴 -0.13 | 🔴 2.00 | 🟡 1.71 | 🔴 0.79 | 🔴 0.50 | 🟢 0.93 | 🔴 0.09 | 🟢 4.57 | 🟡 0.92 |
| `LH_LEV` | 🔴 1.54 | 🟡 1.15 | 🟡 2.12 | 🔴 6.11 | 🔴 0.94 | 🔴 -0.41 | 🔴 2.00 | 🟢 1.65 | 🔴 1.11 | 🔴 0.66 | 🟠 0.93 | 🔴 0.09 | 🟢 5.53 | 🔴 0.95 |
| `LH_MONEY` | 🟢 2.02 | 🟢 1.36 | 🔴 1.72 | 🟡 2.85 | 🟢 0.67 | 🟢 0.97 | 🟢 0.50 | 🔴 1.87 | 🟢 1.51 | 🟢 1.43 | 🟡 0.99 | 🟢 0.14 | 🟢 5.76 | 🟡 1.00 |
| `LH_MORT` | 🟢 1.71 | 🔴 0.53 | 🟠 1.99 | 🟢 0.86 | 🟢 0.65 | 🟢 0.97 | 🟢 0.50 | 🟢 1.42 | 🔴 0.85 | 🟢 1.65 | 🟢 0.99 | 🟢 0.24 | 🔴 4.56 | 🟢 1.00 |
| `LH_NARROW` | 🟢 1.97 | 🟢 1.83 | 🔴 1.59 | 🟡 2.38 | 🟢 0.74 | 🟢 0.93 | 🟢 0.50 | 🔴 1.85 | 🔴 1.20 | 🟢 1.70 | 🟡 0.99 | 🟢 0.14 | 🟢 5.15 | 🟡 1.00 |
| `LH_POP` | 🟢 1.91 | 🟢 1.54 | 🔴 1.72 | 🔴 12.63 | 🟢 0.47 | 🔴 0.27 | 🔴 2.00 | 🟢 1.07 | 🟡 1.25 | 🔴 0.70 | 🔴 0.75 | 🔴 0.11 | 🟢 5.60 | 🟡 1.00 |
| `LH_RCONS` | 🟢 1.93 | 🔴 0.14 | 🔴 1.95 | 🔴 20.33 | 🟢 0.74 | 🟢 0.69 | 🔴 2.00 | 🟢 1.71 | 🟢 1.80 | 🔴 0.70 | 🟠 0.92 | 🔴 0.06 | 🟢 6.03 | 🟡 1.00 |
| `LH_REV` | 🟢 1.85 | 🔴 0.12 | 🟠 2.01 | 🟡 3.82 | 🟢 0.70 | 🟢 0.96 | 🟢 0.50 | 🟢 1.73 | 🟡 1.44 | 🟡 1.31 | 🟡 0.97 | 🔴 0.12 | 🟢 5.76 | 🟡 1.00 |
| `LH_RGDP_BARRO` | 🟢 1.85 | 🔴 0.26 | 🔴 1.91 | 🔴 13.26 | 🟢 0.58 | 🟢 0.79 | 🔴 2.00 | 🟢 1.58 | 🟢 1.66 | 🔴 0.77 | 🔴 0.85 | 🔴 0.07 | 🟢 6.03 | 🟡 1.00 |
| `LH_STIR` | 🔴 1.48 | 🔴 0.25 | 🔴 1.84 | 🟠 3.69 | 🔴 0.96 | 🟢 0.67 | 🟢 0.50 | 🔴 1.82 | 🔴 0.96 | 🟢 1.37 | 🔴 0.32 | 🔴 0.10 | 🟢 4.77 | 🔴 0.45 |
| `LH_UNRATE` | 🔴 1.39 | 🟡 1.07 | 🔴 1.57 | 🔴 5.62 | 🟢 0.90 | 🔴 0.03 | 🔴 2.00 | 🟢 1.66 | 🔴 0.75 | 🔴 0.69 | 🔴 0.52 | 🔴 0.08 | 🟢 3.83 | 🟡 0.90 |
| `LH_WAGE` | 🟢 2.05 | 🟡 1.00 | 🔴 1.86 | 🟠 4.98 | 🟢 0.62 | 🟢 0.90 | 🔴 1.58 | 🔴 1.94 | 🟢 1.93 | 🟠 1.09 | 🟡 0.97 | 🟡 0.12 | 🟢 6.01 | 🟡 1.00 |
| `LH_XRUSD` | 🔴 1.41 | 🔴 0.55 | 🔴 1.89 | 🟠 5.45 | 🟡 0.91 | 🟢 0.67 | 🔴 2.00 | 🔴 1.84 | 🔴 0.95 | 🔴 0.75 | 🟡 1.00 | 🟢 0.16 | 🟢 5.58 | 🟡 1.00 |
| `LH_YIELD` | 🟡 1.66 | 🟢 1.40 | 🔴 1.95 | 🟡 3.38 | 🟠 0.93 | 🟢 0.59 | 🔴 1.59 | 🔴 1.91 | 🔴 1.05 | 🟡 1.33 | 🔴 0.44 | 🔴 0.10 | 🟢 4.86 | 🔴 0.43 |

### G7

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `LH_BANKDEBT` | 🟢 1.98 | 🔴 0.52 | 🔴 1.86 | 🔴 7.36 | 🟢 0.63 | 🟢 0.93 | 🟢 0.50 | 🟡 1.82 | 🟢 1.72 | 🟡 1.24 | 🟡 1.00 | 🟢 0.16 | 🟢 5.69 | 🟡 1.00 |
| `LH_BILLRATE` | 🔴 1.40 | 🟢 1.09 | 🔴 1.27 | 🟢 2.32 | 🟢 0.83 | 🟢 0.67 | 🔴 2.00 | 🟡 1.17 | 🟢 0.24 | 🟢 1.93 | 🟡 0.97 | 🟢 0.12 | 🟢 5.06 | 🟡 1.00 |
| `LH_BONDRATE` | 🔴 1.39 | 🟢 1.62 | 🔴 1.27 | 🟢 2.33 | 🟢 0.84 | 🟢 0.66 | 🔴 2.00 | 🟡 1.17 | 🟢 0.24 | 🟢 1.93 | 🟡 0.97 | 🟢 0.11 | 🟢 5.06 | 🟡 1.00 |
| `LH_BONDTR` | 🔴 1.39 | 🟢 1.53 | 🔴 1.28 | 🟢 2.33 | 🟢 0.83 | 🟢 0.65 | 🔴 2.00 | 🟡 1.17 | 🟢 0.24 | 🟢 1.93 | 🟡 0.97 | 🟢 0.11 | 🟢 5.06 | 🟡 1.00 |
| `LH_BUSCREDIT` | 🟢 1.82 | 🔴 0.28 | 🔴 1.90 | 🟠 4.90 | 🟢 0.70 | 🟢 0.90 | 🟡 1.10 | 🟡 1.83 | 🟢 1.53 | 🟡 1.22 | 🟡 1.00 | 🟢 0.17 | 🟢 5.64 | 🟡 1.00 |
| `LH_CA` | 🔴 1.17 | 🟡 1.14 | 🔴 1.31 | 🟢 1.82 | 🔴 0.99 | 🟢 1.00 | 🟢 0.50 | 🟢 1.42 | 🟠 0.37 | 🟢 1.65 | 🟠 0.53 | 🟢 0.13 | 🟢 4.18 | 🔴 0.53 |
| `LH_CPI` | 🔴 1.24 | 🟢 1.91 | 🔴 1.41 | 🟢 1.48 | 🟢 0.55 | 🟢 0.81 | 🔴 2.00 | 🟢 1.13 | 🟢 0.32 | 🟢 1.92 | 🟢 1.00 | 🟢 0.11 | 🟢 2.35 | 🟡 1.00 |
| `LH_CREDIT` | 🔴 1.54 | 🟢 1.38 | 🔴 1.81 | 🔴 4.80 | 🟢 0.56 | 🟢 0.95 | 🟢 0.50 | 🟢 0.78 | 🔴 0.82 | 🟢 1.34 | 🟢 1.00 | 🟠 0.12 | 🟢 5.48 | 🟠 0.99 |
| `LH_DEBTGDP` | 🟢 1.71 | 🔴 0.59 | 🔴 1.79 | 🟡 4.12 | 🟢 0.82 | 🔴 0.14 | 🔴 2.00 | 🔴 1.86 | 🔴 1.15 | 🔴 1.01 | 🔴 0.28 | 🟡 0.14 | 🟢 5.28 | 🔴 0.51 |
| `LH_EQDIVP` | 🔴 1.40 | 🟢 1.52 | 🔴 1.29 | 🟢 2.33 | 🟢 0.82 | 🟢 0.68 | 🔴 2.00 | 🟡 1.17 | 🟢 0.24 | 🟢 1.93 | 🟡 0.97 | 🟢 0.11 | 🟢 5.08 | 🟡 1.00 |
| `LH_EQTR` | 🟢 1.04 | 🟢 2.07 | 🔴 -0.00 | 🟡 2.99 | 🟢 0.82 | 🔴 0.17 | 🔴 2.00 | 🔴 1.00 | 🟡 0.07 | 🟢 1.97 | 🟢 0.96 | 🟢 0.11 | 🔴 -0.02 | 🟢 0.99 |
| `LH_EQUITY` | 🟢 1.04 | 🟢 2.04 | 🔴 -0.00 | 🟡 2.98 | 🟢 0.82 | 🔴 0.17 | 🔴 2.00 | 🔴 1.00 | 🟡 0.07 | 🟢 1.97 | 🟢 0.94 | 🟢 0.11 | 🔴 -0.02 | 🟢 0.97 |
| `LH_EXP` | 🟢 1.96 | 🔴 0.77 | 🔴 1.50 | 🟠 5.41 | 🟢 0.71 | 🟢 0.88 | 🟡 1.16 | 🟢 1.49 | 🟢 1.51 | 🟠 1.10 | 🟡 1.00 | 🟢 0.15 | 🟢 5.89 | 🟡 1.00 |
| `LH_EXPORTS` | 🟢 1.86 | 🔴 0.41 | 🟡 2.05 | 🟡 3.77 | 🟢 0.70 | 🟢 0.93 | 🟢 0.50 | 🟢 1.74 | 🟢 1.49 | 🟡 1.27 | 🟡 0.99 | 🟢 0.16 | 🟢 5.74 | 🟡 1.00 |
| `LH_GDP` | 🟢 1.84 | 🔴 0.61 | 🟢 2.46 | 🔴 11.00 | 🟢 0.62 | 🟢 0.79 | 🔴 2.00 | 🟢 0.22 | 🔴 1.00 | 🔴 0.80 | 🟡 0.94 | 🔴 0.05 | 🟢 6.01 | 🟡 0.98 |
| `LH_GDPNOM` | 🟢 1.99 | 🔴 0.57 | 🟠 1.97 | 🔴 13.93 | 🟢 0.51 | 🟢 0.93 | 🟢 0.50 | 🔴 1.86 | 🟢 1.79 | 🟠 1.15 | 🟡 1.00 | 🟡 0.13 | 🟢 5.89 | 🟡 1.00 |
| `LH_HHCREDIT` | 🟢 1.83 | 🟢 1.26 | 🔴 1.85 | 🟠 5.28 | 🟢 0.48 | 🟢 0.99 | 🟢 0.50 | 🟡 1.79 | 🟢 1.65 | 🟢 1.39 | 🟡 1.00 | 🟢 0.15 | 🟢 5.55 | 🟡 1.00 |
| `LH_HOUSECG` | 🔴 1.36 | 🟢 1.14 | 🔴 1.36 | 🟢 2.26 | 🟢 0.85 | 🟠 0.52 | 🔴 2.00 | 🟡 1.17 | 🟢 0.24 | 🟢 1.93 | 🟡 0.92 | 🟢 0.13 | 🟢 4.66 | 🟠 0.98 |
| `LH_HOUSINGTR` | 🔴 1.37 | 🟢 1.34 | 🔴 1.36 | 🟢 2.24 | 🟢 0.85 | 🟠 0.50 | 🔴 2.00 | 🟡 1.17 | 🟢 0.24 | 🟢 1.93 | 🟡 0.92 | 🟢 0.13 | 🟢 4.60 | 🟠 0.97 |
| `LH_HPI` | 🟢 1.89 | 🟢 5.22 | 🔴 1.89 | 🔴 5.64 | 🟢 0.75 | 🟢 0.81 | 🟠 1.39 | 🟢 1.59 | 🟢 1.52 | 🟢 1.21 | 🟢 1.00 | 🔴 0.10 | 🟢 6.05 | 🟡 1.00 |
| `LH_IMPORTS` | 🟢 1.82 | 🟠 0.85 | 🟡 2.09 | 🟠 5.02 | 🟢 0.79 | 🟢 0.93 | 🟢 0.50 | 🟢 1.77 | 🟡 1.40 | 🟡 1.28 | 🟡 1.00 | 🟢 0.16 | 🟢 5.77 | 🟡 1.00 |
| `LH_INV` | 🔴 1.33 | 🔴 0.77 | 🔴 1.84 | 🔴 5.55 | 🟢 0.91 | 🔴 -0.07 | 🔴 2.00 | 🟡 1.55 | 🔴 0.87 | 🔴 0.55 | 🟢 0.95 | 🔴 0.09 | 🟢 5.16 | 🟡 0.94 |
| `LH_LEV` | 🟢 1.76 | 🔴 0.74 | 🔴 1.86 | 🟠 4.26 | 🟢 0.87 | 🔴 -0.45 | 🔴 2.00 | 🟢 1.65 | 🟡 1.38 | 🔴 0.82 | 🟠 0.95 | 🔴 0.09 | 🟢 5.61 | 🟠 0.96 |
| `LH_MONEY` | 🟢 2.04 | 🔴 0.67 | 🔴 1.68 | 🟡 2.39 | 🟢 0.41 | 🟢 0.98 | 🟢 0.50 | 🔴 1.85 | 🟢 1.67 | 🟡 1.39 | 🟡 1.00 | 🟢 0.14 | 🟢 5.89 | 🟡 1.00 |
| `LH_MORT` | 🟢 2.10 | 🟡 1.03 | 🔴 1.74 | 🟡 2.51 | 🟢 0.49 | 🟢 0.99 | 🟢 0.50 | 🔴 1.89 | 🟢 1.57 | 🟢 1.45 | 🟡 0.97 | 🟠 0.12 | 🟢 5.63 | 🟡 1.00 |
| `LH_NARROW` | 🟢 1.97 | 🔴 0.39 | 🔴 1.63 | 🟡 2.67 | 🟢 0.37 | 🟢 1.00 | 🟢 0.50 | 🔴 1.83 | 🟢 1.52 | 🟢 1.48 | 🟡 1.00 | 🟡 0.12 | 🟢 5.84 | 🟡 1.00 |
| `LH_POP` | 🟢 2.02 | 🔴 0.74 | 🔴 1.76 | 🔴 10.01 | 🟢 0.38 | 🟢 0.57 | 🔴 2.00 | 🟡 1.76 | 🟢 1.83 | 🔴 0.62 | 🟠 0.96 | 🔴 0.01 | 🟢 5.84 | 🟡 1.00 |
| `LH_RCONS` | 🟢 1.99 | 🔴 0.17 | 🔴 1.92 | 🔴 11.28 | 🟢 0.60 | 🟢 0.80 | 🔴 2.00 | 🟢 1.72 | 🟢 1.85 | 🔴 0.80 | 🟡 1.00 | 🔴 0.07 | 🟢 6.05 | 🟡 1.00 |
| `LH_REV` | 🟢 2.06 | 🟠 0.93 | 🔴 1.76 | 🟠 4.74 | 🟢 0.65 | 🟢 0.92 | 🟢 0.50 | 🟡 1.81 | 🟢 1.72 | 🟠 1.12 | 🟡 1.00 | 🟢 0.14 | 🟢 5.86 | 🟡 1.00 |
| `LH_RGDP_BARRO` | 🟢 1.92 | 🔴 0.47 | 🔴 1.90 | 🔴 9.93 | 🟢 0.63 | 🟢 0.79 | 🔴 2.00 | 🟡 1.79 | 🟢 1.76 | 🔴 0.77 | 🟠 0.95 | 🔴 0.04 | 🟢 6.03 | 🟡 1.00 |
| `LH_STIR` | 🔴 1.39 | 🔴 0.09 | 🔴 1.70 | 🟡 2.99 | 🟡 0.93 | 🟢 0.73 | 🟢 1.24 | 🔴 1.82 | 🔴 0.87 | 🟢 1.32 | 🔴 0.28 | 🔴 0.10 | 🟢 4.03 | 🔴 0.39 |
| `LH_UNRATE` | 🔴 1.28 | 🟡 1.13 | 🟠 1.67 | 🟠 3.50 | 🟢 0.91 | 🔴 -0.35 | 🔴 2.00 | 🔴 1.86 | 🔴 0.50 | 🟡 1.26 | 🔴 0.22 | 🔴 0.09 | 🟢 3.10 | 🟡 0.69 |
| `LH_WAGE` | 🟢 2.05 | 🔴 0.14 | 🔴 1.80 | 🟡 4.54 | 🟢 0.51 | 🟢 0.88 | 🔴 1.83 | 🔴 1.97 | 🟢 1.92 | 🟠 1.09 | 🟡 1.00 | 🔴 0.09 | 🟢 6.03 | 🟡 1.00 |
| `LH_XRUSD` | 🔴 1.46 | 🟡 1.08 | 🔴 1.90 | 🟠 5.19 | 🟢 0.90 | 🟢 0.66 | 🔴 2.00 | 🟡 1.74 | 🔴 0.96 | 🔴 0.66 | 🟡 1.00 | 🟢 0.14 | 🟢 5.59 | 🟡 1.00 |
| `LH_YIELD` | 🟡 1.64 | 🟢 1.63 | 🟢 2.18 | 🟡 3.25 | 🟢 0.91 | 🟢 0.75 | 🟢 1.24 | 🟢 1.66 | 🟠 1.12 | 🟢 1.33 | 🔴 0.51 | 🔴 0.11 | 🟢 5.12 | 🔴 0.49 |

### NORDIC

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `LH_BANKDEBT` | 🟢 2.07 | 🟠 0.82 | 🔴 1.75 | 🟢 1.51 | 🟢 0.52 | 🟢 0.84 | 🟢 0.50 | 🟡 1.74 | 🟢 1.61 | 🟢 1.49 | 🔴 0.87 | 🟢 0.13 | 🟢 5.74 | 🟡 1.00 |
| `LH_BILLRATE` | 🟡 1.59 | 🔴 0.36 | 🟠 1.99 | 🟠 4.37 | 🟡 0.92 | 🟢 0.74 | 🟢 0.50 | 🔴 1.85 | 🔴 1.11 | 🟡 1.31 | 🔴 0.30 | 🔴 0.10 | 🟢 4.59 | 🔴 0.41 |
| `LH_BONDRATE` | 🟢 1.74 | 🔴 0.77 | 🔴 1.83 | 🟡 4.27 | 🟠 0.93 | 🟢 0.80 | 🟡 1.38 | 🔴 1.88 | 🟡 1.22 | 🟡 1.21 | 🔴 0.54 | 🟠 0.12 | 🟢 5.10 | 🔴 0.53 |
| `LH_BONDTR` | 🟡 0.72 | 🔴 0.27 | 🔴 0.11 | 🟢 2.51 | 🔴 0.99 | 🟠 0.52 | 🟡 1.62 | 🟡 -2.18 | 🟢 0.07 | 🟢 1.34 | 🟡 0.22 | 🟡 0.06 | 🟢 0.71 | 🟢 0.34 |
| `LH_BUSCREDIT` | 🟢 1.89 | 🟠 1.37 | 🔴 1.77 | 🟠 5.61 | 🟢 0.42 | 🟢 1.00 | 🔴 2.00 | 🟠 1.74 | 🟢 1.66 | 🔴 0.95 | 🟡 1.00 | 🟢 0.14 | 🟢 4.03 | — — |
| `LH_CA` | 🟡 1.67 | 🔴 0.83 | 🔴 1.63 | 🟡 2.16 | 🔴 0.94 | 🟢 0.97 | 🟢 0.50 | 🟡 1.79 | 🔴 0.95 | 🟢 1.51 | 🔴 0.45 | 🟢 0.13 | 🟢 5.00 | 🔴 0.69 |
| `LH_CPI` | 🟢 2.02 | 🔴 0.15 | 🔴 1.80 | 🟠 5.10 | 🟢 0.48 | 🟢 0.76 | 🔴 2.00 | 🔴 1.93 | 🟢 1.93 | 🔴 1.00 | 🟡 0.99 | 🟠 0.12 | 🟢 6.02 | 🟡 1.00 |
| `LH_CREDIT` | 🟢 2.04 | 🟡 0.99 | 🔴 1.71 | 🟢 1.37 | 🟢 0.39 | 🟢 0.90 | 🟢 0.50 | 🔴 1.95 | 🟢 1.59 | 🟢 1.57 | 🟡 1.00 | 🟢 0.12 | 🟢 5.79 | 🟡 1.00 |
| `LH_DEBTGDP` | 🔴 1.54 | 🔴 0.78 | 🔴 1.82 | 🟠 4.29 | 🟢 0.87 | 🟢 0.57 | 🔴 2.00 | 🟢 1.65 | 🔴 0.97 | 🔴 0.77 | 🔴 0.64 | 🟡 0.12 | 🟢 5.22 | 🔴 0.88 |
| `LH_EQDIVP` | 🔴 1.33 | 🔴 0.58 | 🔴 1.23 | 🔴 4.78 | 🟠 0.94 | 🔴 0.08 | 🔴 1.73 | 🟢 1.51 | 🔴 0.61 | 🟢 1.25 | 🟠 0.55 | 🟡 0.10 | 🟢 3.58 | 🟠 0.76 |
| `LH_EQTR` | 🔴 0.52 | 🔴 0.17 | 🔴 0.10 | 🟡 2.93 | 🟡 0.98 | 🟡 0.64 | 🟢 1.37 | 🔴 4.47 | 🟠 -0.02 | 🟢 1.41 | 🟢 0.29 | 🟢 0.06 | 🟢 0.93 | 🟢 0.37 |
| `LH_EQUITY` | 🔴 0.54 | 🔴 0.18 | 🔴 0.17 | 🟡 3.12 | 🟡 0.98 | 🟡 0.64 | 🟢 1.26 | 🔴 4.54 | 🔴 -0.02 | 🟢 1.41 | 🟢 0.35 | 🔴 0.05 | 🟢 0.95 | 🟢 0.40 |
| `LH_EXP` | 🟢 2.05 | 🔴 0.13 | 🔴 1.64 | 🟢 1.98 | 🟢 0.64 | 🟢 0.97 | 🟢 0.50 | 🟡 1.77 | 🟢 1.64 | 🟢 1.46 | 🟡 0.97 | 🟢 0.13 | 🟢 5.83 | 🟡 1.00 |
| `LH_EXPORTS` | 🟢 1.92 | 🔴 0.56 | 🟠 1.98 | 🟡 3.47 | 🟢 0.79 | 🟢 0.91 | 🟢 0.50 | 🟡 1.76 | 🟡 1.40 | 🟡 1.37 | 🟡 0.99 | 🔴 0.11 | 🟢 5.75 | 🟡 1.00 |
| `LH_GDP` | 🟢 1.98 | 🟡 1.01 | 🔴 1.78 | 🔴 9.42 | 🟢 0.45 | 🟢 0.96 | 🔴 1.78 | 🔴 1.92 | 🟢 1.83 | 🟠 1.07 | 🟢 1.00 | 🔴 0.05 | 🟢 6.11 | 🟡 1.00 |
| `LH_GDPNOM` | 🟢 2.06 | 🔴 0.26 | 🔴 1.83 | 🟡 2.27 | 🟢 0.52 | 🟢 0.95 | 🟢 0.50 | 🔴 1.93 | 🟢 1.74 | 🟢 1.41 | 🟡 1.00 | 🟡 0.13 | 🟢 5.86 | 🟡 1.00 |
| `LH_HHCREDIT` | 🔴 1.60 | 🟢 2.35 | 🔴 1.70 | 🟢 1.64 | 🟢 0.31 | 🟢 0.99 | 🟢 0.50 | 🔴 1.96 | 🟢 1.57 | 🟢 1.59 | 🔴 0.68 | 🟢 0.21 | 🟢 5.36 | 🟠 1.00 |
| `LH_HOUSECG` | 🟡 0.81 | 🟢 1.33 | 🔴 0.25 | 🟡 3.10 | 🟠 0.98 | 🔴 -0.14 | 🔴 2.00 | 🔴 4.24 | 🔴 0.03 | 🟢 1.67 | 🟢 0.55 | 🟠 0.06 | 🟢 1.31 | 🟢 0.57 |
| `LH_HOUSINGTR` | 🟢 0.87 | 🟢 1.19 | 🔴 0.24 | 🟠 3.34 | 🔴 0.99 | 🔴 0.17 | 🔴 2.00 | 🔴 3.39 | 🔴 0.05 | 🟢 1.75 | 🟢 0.41 | 🟡 0.06 | 🟢 1.46 | 🟢 0.44 |
| `LH_HPI` | 🟢 2.08 | 🔴 0.16 | 🔴 1.74 | 🟢 1.95 | 🟢 0.70 | 🟢 0.90 | 🟢 0.50 | 🔴 1.88 | 🟢 1.62 | 🟢 1.49 | 🟡 1.00 | 🟢 0.13 | 🟢 5.82 | 🟡 1.00 |
| `LH_IMPORTS` | 🟢 1.97 | 🔴 0.20 | 🔴 1.84 | 🟡 2.16 | 🟢 0.77 | 🟢 0.91 | 🟢 0.50 | 🟠 1.82 | 🟢 1.47 | 🟢 1.44 | 🟡 0.97 | 🟡 0.12 | 🟢 5.82 | 🟡 1.00 |
| `LH_INV` | 🔴 1.22 | 🟡 1.23 | 🔴 1.55 | 🔴 14.33 | 🟢 0.91 | 🔴 -0.01 | 🔴 2.00 | 🟢 1.35 | 🔴 0.65 | 🔴 0.49 | 🟢 0.91 | 🔴 0.08 | 🟢 4.46 | 🟡 0.90 |
| `LH_LEV` | 🟢 1.69 | 🔴 0.74 | 🔴 1.73 | 🟡 2.55 | 🔴 0.94 | 🔴 -0.49 | 🔴 2.00 | 🟢 1.60 | 🟠 1.12 | 🔴 0.88 | 🟢 1.00 | 🔴 0.08 | 🟢 5.63 | 🟢 1.00 |
| `LH_MONEY` | 🟢 2.07 | 🟡 1.04 | 🔴 1.61 | 🟢 1.42 | 🟢 0.26 | 🟢 0.94 | 🟢 0.50 | 🟡 1.78 | 🟢 1.55 | 🟢 1.56 | 🟡 1.00 | 🟡 0.11 | 🟢 5.76 | 🟡 1.00 |
| `LH_MORT` | 🟢 2.04 | 🟢 1.67 | 🔴 1.69 | 🟢 1.25 | 🟢 0.24 | 🟢 1.00 | 🟢 0.50 | 🔴 1.98 | 🟢 1.58 | 🟢 1.60 | 🟡 1.00 | 🔴 0.09 | 🟢 5.63 | 🟡 1.00 |
| `LH_NARROW` | 🟢 1.96 | 🟠 0.91 | 🔴 1.51 | 🟢 2.01 | 🟢 0.61 | 🟢 0.97 | 🟢 0.50 | 🟢 1.60 | 🟡 1.41 | 🟢 1.51 | 🟡 1.00 | 🟢 0.13 | 🟢 5.85 | 🟡 1.00 |
| `LH_POP` | 🟢 2.04 | 🟡 1.04 | 🔴 1.77 | 🔴 14.86 | 🟢 0.28 | 🔴 -0.23 | 🔴 2.00 | 🔴 1.92 | 🟢 1.91 | 🔴 0.48 | 🟡 1.00 | 🔴 0.01 | 🟢 5.91 | 🟡 1.00 |
| `LH_RCONS` | 🟢 1.98 | 🔴 0.48 | 🔴 1.88 | 🔴 6.22 | 🟢 0.64 | 🟢 0.85 | 🔴 2.00 | 🟡 1.81 | 🟢 1.69 | 🔴 0.80 | 🟡 0.99 | 🔴 0.04 | 🟢 5.99 | 🟡 1.00 |
| `LH_REV` | 🟢 2.06 | 🔴 0.32 | 🔴 1.89 | 🟡 2.34 | 🟢 0.56 | 🟢 0.99 | 🟢 0.50 | 🔴 1.87 | 🟢 1.59 | 🟢 1.43 | 🟡 1.00 | 🟢 0.13 | 🟢 5.76 | 🟡 1.00 |
| `LH_RGDP_BARRO` | 🟢 1.97 | 🔴 0.59 | 🔴 1.84 | 🔴 13.25 | 🟢 0.51 | 🟢 0.87 | 🔴 2.00 | 🟠 1.84 | 🟢 1.80 | 🔴 0.76 | 🟡 0.99 | 🔴 0.05 | 🟢 6.03 | 🟡 1.00 |
| `LH_STIR` | 🟡 1.59 | 🔴 0.30 | 🔴 1.82 | 🔴 5.11 | 🟠 0.93 | 🟢 0.76 | 🟢 0.50 | 🟢 1.78 | 🔴 1.12 | 🟡 1.27 | 🔴 0.30 | 🔴 0.12 | 🟢 4.70 | 🔴 0.41 |
| `LH_UNRATE` | 🔴 1.35 | 🔴 0.61 | 🟠 1.89 | 🟢 2.34 | 🟡 0.92 | 🔴 0.28 | 🔴 2.00 | 🟢 1.55 | 🔴 0.81 | 🔴 0.96 | 🔴 0.28 | 🔴 0.09 | 🟢 4.61 | 🔴 0.76 |
| `LH_WAGE` | 🟢 2.07 | 🔴 0.40 | 🔴 1.78 | 🟡 2.81 | 🟢 0.40 | 🟢 0.92 | 🟡 1.16 | 🔴 1.98 | 🟢 1.87 | 🟡 1.27 | 🟡 1.00 | 🟠 0.12 | 🟢 5.99 | 🟡 1.00 |
| `LH_XRUSD` | 🔴 1.30 | 🟢 2.32 | 🟠 1.91 | 🔴 4.55 | 🟡 0.93 | 🔴 0.44 | 🔴 2.00 | 🔴 1.93 | 🔴 0.58 | 🔴 0.64 | 🟢 0.95 | 🔴 0.08 | 🟢 4.55 | 🟡 0.93 |
| `LH_YIELD` | 🟢 1.72 | 🔴 0.79 | 🔴 1.87 | 🟡 4.43 | 🟠 0.93 | 🟢 0.79 | 🟠 1.45 | 🔴 1.89 | 🟠 1.21 | 🟡 1.22 | 🔴 0.54 | 🔴 0.12 | 🟢 5.11 | 🔴 0.53 |

### USA

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `LH_BANKDEBT` | 🟢 1.82 | 🟠 1.00 | 🔴 1.66 | 🟢 2.56 | 🟢 0.38 | 🟢 1.00 | 🟠 1.46 | 🔴 1.90 | 🟢 1.65 | 🟡 1.26 | 🟢 1.00 | 🔴 0.09 | 🟢 4.89 | 🟡 1.00 |
| `LH_BILLRATE` | 🟡 1.50 | 🟢 10.26 | 🔴 1.76 | 🟡 2.84 | 🟢 0.84 | 🟡 0.65 | 🟡 1.51 | 🔴 1.88 | 🔴 0.79 | 🟢 1.46 | 🔴 0.33 | 🟢 0.19 | 🟢 4.38 | 🔴 0.51 |
| `LH_BONDRATE` | 🟢 1.71 | 🟡 1.29 | 🔴 1.83 | 🟡 2.12 | 🟠 0.93 | 🟢 0.65 | 🟡 1.34 | 🟢 1.71 | 🟠 1.10 | 🟢 1.46 | 🔴 0.42 | 🟡 0.13 | 🟢 4.98 | 🔴 0.55 |
| `LH_BONDTR` | 🔴 0.59 | 🟡 0.69 | 🔴 -0.05 | 🟡 2.63 | 🔴 0.99 | 🟢 0.83 | 🟢 1.19 | 🔴 2.43 | 🔴 -0.02 | 🟢 1.40 | 🟢 0.31 | 🔴 0.05 | 🟢 0.96 | 🟢 0.43 |
| `LH_BUSCREDIT` | 🟠 1.75 | 🔴 0.71 | 🔴 1.64 | 🟢 2.56 | 🟢 0.45 | 🟢 1.00 | 🔴 2.00 | 🔴 1.97 | 🟢 1.51 | 🟠 1.15 | 🟡 1.00 | 🔴 0.09 | 🟢 4.11 | 🟡 1.00 |
| `LH_CA` | 🔴 1.53 | 🔴 0.71 | 🔴 1.69 | 🟡 2.83 | 🟡 0.93 | 🟢 0.91 | 🟢 0.50 | 🟢 1.67 | 🔴 0.93 | 🟢 1.52 | 🔴 0.60 | 🟢 0.12 | 🟢 5.17 | 🔴 0.89 |
| `LH_CPI` | 🔴 1.24 | 🟢 2.61 | 🔴 1.41 | 🟢 1.35 | 🟢 0.60 | 🟢 0.78 | 🔴 2.00 | 🟢 1.15 | 🟢 0.32 | 🟢 1.91 | 🟢 1.00 | 🟢 0.11 | 🟢 2.35 | 🟡 1.00 |
| `LH_CREDIT` | 🟡 1.55 | 🟢 2.09 | 🔴 1.67 | 🟢 2.75 | 🟢 0.51 | 🟢 0.89 | 🟢 0.50 | 🟢 -0.67 | 🔴 0.56 | 🟢 1.47 | 🟢 0.99 | 🔴 0.10 | 🟢 5.67 | 🟡 0.95 |
| `LH_DEBTGDP` | 🟢 1.79 | 🟢 2.34 | 🔴 1.76 | 🟡 4.23 | 🟢 0.85 | 🔴 0.24 | 🔴 2.00 | 🟢 1.71 | 🔴 1.14 | 🔴 0.96 | 🔴 0.81 | 🟢 0.14 | 🟢 5.26 | 🔴 0.96 |
| `LH_EQDIVP` | 🔴 1.12 | 🟢 1.47 | 🔴 1.26 | 🔴 5.25 | 🔴 0.97 | 🔴 -0.25 | 🔴 1.91 | 🟢 1.50 | 🔴 0.35 | 🔴 1.07 | 🟡 0.64 | 🟠 0.08 | 🟢 2.78 | 🟡 0.67 |
| `LH_EQTR` | 🔴 0.53 | 🟠 0.63 | 🔴 -0.00 | 🟠 3.32 | 🟢 0.98 | 🔴 -0.11 | 🔴 1.96 | 🔴 24.46 | 🔴 -0.04 | 🔴 1.01 | 🔴 0.15 | 🔴 0.05 | 🟡 0.18 | 🔴 0.19 |
| `LH_EQUITY` | 🔴 0.50 | 🟡 0.67 | 🔴 0.10 | 🟠 3.41 | 🟡 0.98 | 🔴 -0.10 | 🔴 2.00 | 🔴 109.81 | 🔴 -0.01 | 🔴 1.01 | 🟡 0.22 | 🔴 0.06 | 🟢 0.27 | 🔴 0.24 |
| `LH_EXP` | 🟢 2.04 | 🟡 1.17 | 🔴 1.32 | 🟡 2.02 | 🟢 0.73 | 🟢 0.96 | 🟢 1.02 | 🟢 1.41 | 🔴 1.18 | 🟢 1.54 | 🟠 0.96 | 🟢 0.13 | 🟢 5.93 | 🟡 1.00 |
| `LH_EXPORTS` | 🟢 2.02 | 🟠 0.92 | 🟡 2.05 | 🟢 1.71 | 🟢 0.77 | 🟢 0.93 | 🟢 0.50 | 🟡 1.78 | 🟢 1.46 | 🟢 1.45 | 🟡 0.97 | 🔴 0.12 | 🟢 5.77 | 🟡 1.00 |
| `LH_GDP` | 🟢 1.77 | 🟡 1.33 | 🟢 2.48 | 🔴 8.86 | 🟢 0.81 | 🟢 0.78 | 🔴 2.00 | 🟢 0.01 | 🔴 0.95 | 🔴 0.83 | 🟡 0.94 | 🔴 0.05 | 🟢 5.96 | 🟠 0.98 |
| `LH_GDPNOM` | 🟢 2.03 | 🟢 1.26 | 🔴 1.81 | 🟡 2.97 | 🟢 0.56 | 🟢 0.97 | 🟢 0.50 | 🔴 1.94 | 🟢 1.77 | 🟡 1.36 | 🟡 1.00 | 🔴 0.09 | 🟢 5.94 | 🟡 1.00 |
| `LH_HHCREDIT` | 🟢 1.91 | 🟠 1.25 | 🔴 1.70 | 🟠 4.24 | 🟢 0.26 | 🟢 1.00 | 🔴 2.00 | 🔴 1.87 | 🟢 1.76 | 🔴 0.88 | 🟡 1.00 | 🔴 0.06 | 🟢 4.23 | 🟡 1.00 |
| `LH_HOUSECG` | 🟢 0.92 | 🟢 1.59 | 🔴 0.15 | 🟡 2.40 | 🟡 0.98 | 🔴 -0.74 | 🟢 1.19 | 🔴 5.22 | 🔴 0.04 | 🟢 1.51 | 🟢 0.28 | 🔴 0.04 | 🟢 1.73 | 🟢 0.36 |
| `LH_HOUSINGTR` | 🟢 0.91 | 🟢 1.57 | 🔴 0.16 | 🟡 2.74 | 🟡 0.98 | 🔴 -0.76 | 🟢 1.26 | 🔴 4.73 | 🔴 0.03 | 🟢 1.52 | 🟢 0.29 | 🔴 0.03 | 🟢 1.71 | 🟢 0.38 |
| `LH_HPI` | 🟢 1.91 | 🟢 1.37 | 🔴 1.93 | 🟠 5.27 | 🟢 0.67 | 🔴 0.40 | 🔴 2.00 | 🟢 1.26 | 🔴 1.13 | 🟠 1.10 | 🔴 0.74 | 🔴 0.11 | 🟢 5.93 | 🔴 0.82 |
| `LH_IMPORTS` | 🟢 2.00 | 🔴 0.29 | 🟠 1.97 | 🟡 2.85 | 🟢 0.77 | 🟢 0.92 | 🟢 0.50 | 🟢 1.73 | 🟢 1.46 | 🟢 1.41 | 🟡 0.97 | 🔴 0.11 | 🟢 5.71 | 🟡 1.00 |
| `LH_INV` | 🔴 1.23 | 🟡 1.39 | 🔴 1.59 | 🟢 2.40 | 🟢 0.91 | 🔴 -0.13 | 🟠 1.69 | 🟢 1.56 | 🔴 0.61 | 🟡 1.28 | 🟡 0.76 | 🟠 0.09 | 🟢 4.15 | 🟠 0.75 |
| `LH_LEV` | 🔴 1.53 | 🟢 1.61 | 🔴 1.59 | 🟠 3.78 | 🟢 0.90 | 🔴 -0.40 | 🔴 2.00 | 🟢 1.39 | 🟠 1.04 | 🔴 1.01 | 🟡 0.87 | 🔴 0.08 | 🟢 5.56 | 🟠 0.89 |
| `LH_MONEY` | 🟢 2.00 | 🟢 1.84 | 🔴 1.54 | 🟢 1.62 | 🟢 0.28 | 🟢 0.98 | 🟢 0.50 | 🟢 1.67 | 🟢 1.47 | 🟢 1.57 | 🟡 1.00 | 🔴 0.09 | 🟢 5.89 | 🟡 1.00 |
| `LH_MORT` | 🟢 1.81 | 🟢 1.25 | 🔴 1.66 | 🟠 6.01 | 🟢 0.31 | 🟢 0.94 | 🟢 0.99 | 🔴 1.82 | 🟢 1.61 | 🟢 1.37 | 🟡 1.00 | 🔴 0.10 | 🟢 5.70 | 🟡 1.00 |
| `LH_NARROW` | 🟢 1.87 | 🟢 3.31 | 🔴 1.35 | 🟢 0.64 | 🟢 0.49 | 🟢 0.95 | 🟢 0.50 | 🟡 1.66 | 🔴 1.06 | 🟢 1.71 | 🟡 1.00 | 🔴 0.09 | 🟢 5.07 | 🟡 1.00 |
| `LH_POP` | 🟢 2.07 | 🔴 0.14 | 🔴 1.79 | 🔴 7.30 | 🟢 -0.00 | 🟢 0.67 | 🔴 2.00 | 🔴 1.98 | 🟢 2.00 | 🔴 0.62 | 🟡 1.00 | 🔴 0.01 | 🟢 5.95 | 🟡 1.00 |
| `LH_RCONS` | 🟢 1.93 | 🟡 1.09 | 🔴 1.85 | 🔴 9.78 | 🟢 0.74 | 🟢 0.80 | 🔴 2.00 | 🔴 1.89 | 🟢 1.78 | 🔴 0.90 | 🟡 1.00 | 🔴 0.05 | 🟢 6.04 | 🟡 1.00 |
| `LH_REV` | 🟢 1.84 | 🔴 0.19 | 🔴 1.81 | 🟡 2.81 | 🟢 0.75 | 🟢 0.98 | 🟢 1.06 | 🟡 1.78 | 🟢 1.46 | 🟡 1.34 | 🟡 0.99 | 🟢 0.13 | 🟢 5.90 | 🟡 1.00 |
| `LH_RGDP_BARRO` | 🟢 1.89 | 🟢 1.44 | 🔴 1.85 | 🔴 8.53 | 🟢 0.78 | 🟢 0.83 | 🔴 2.00 | 🔴 1.87 | 🟢 1.67 | 🔴 0.78 | 🟡 0.97 | 🔴 0.05 | 🟢 5.91 | 🟡 1.00 |
| `LH_STIR` | 🔴 1.20 | 🟢 2.21 | 🔴 1.39 | 🟢 2.41 | 🟢 0.92 | 🔴 0.47 | 🔴 1.99 | 🟢 1.30 | 🔴 0.52 | 🟢 1.39 | 🔴 0.17 | 🔴 0.08 | 🟢 2.67 | 🔴 0.32 |
| `LH_UNRATE` | 🔴 1.35 | 🔴 0.21 | 🟠 1.71 | 🟢 2.23 | 🟢 0.89 | 🔴 -0.40 | 🟢 1.00 | 🔴 1.86 | 🔴 0.59 | 🟢 1.50 | 🔴 0.28 | 🔴 0.06 | 🟢 2.77 | 🔴 0.33 |
| `LH_WAGE` | 🟢 2.07 | 🔴 0.27 | 🔴 1.72 | 🟡 3.39 | 🟢 0.35 | 🟢 0.97 | 🔴 1.77 | 🔴 1.85 | 🟢 1.82 | 🟡 1.19 | 🟡 1.00 | 🔴 0.07 | 🟢 6.04 | 🟡 1.00 |
| `LH_XRUSD` | 🔴 -0.00 | 🔴 0.00 | — — | — — | 🟢 -0.00 | 🔴 0.00 | — — | — — | — — | — — | 🔴 0.00 | — — | — — | 🔴 0.00 |
| `LH_YIELD` | 🟡 1.65 | 🟢 1.43 | 🟠 1.97 | 🟢 2.14 | 🟠 0.93 | 🟢 0.67 | 🟡 1.30 | 🟢 1.67 | 🟡 1.06 | 🟢 1.46 | 🔴 0.42 | 🟡 0.13 | 🟢 4.81 | 🔴 0.52 |

## Bank of England Millennium (1700-2016)

### UK_BOE

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BOE_CPI` | 🟢 1.84 | 🔴 0.11 | 🔴 1.78 | 🟢 1.70 | 🟢 0.80 | 🟢 0.58 | 🟢 0.50 | 🔴 1.92 | 🟢 1.66 | 🟢 1.60 | 🔴 0.63 | 🔴 0.10 | 🟢 7.56 | 🟡 1.00 |
| `BOE_CREDIT` | 🟢 1.82 | 🟢 1.43 | 🔴 1.74 | 🟢 1.83 | 🟢 0.50 | 🟢 0.95 | 🟡 0.50 | 🔴 1.86 | 🟢 1.66 | 🟢 1.48 | 🟢 1.00 | 🔴 0.10 | 🟢 5.45 | 🟠 1.00 |
| `BOE_DEBTGDP` | 🔴 1.35 | 🟢 2.27 | 🔴 1.62 | 🟢 0.71 | 🟢 0.73 | 🟢 0.66 | 🟢 0.50 | 🔴 1.91 | 🔴 1.08 | 🟢 1.87 | 🔴 0.67 | 🟢 0.13 | 🟢 6.15 | 🟡 1.00 |
| `BOE_EQUITY` | 🔴 1.44 | 🔴 0.23 | 🔴 1.66 | 🟢 0.68 | 🟢 0.87 | 🟢 0.82 | 🟢 0.50 | 🟡 1.71 | 🔴 1.01 | 🟢 1.71 | 🟢 1.00 | 🔴 0.09 | 🟢 6.95 | 🟡 1.00 |
| `BOE_GDP` | 🟢 1.87 | 🔴 0.61 | 🔴 1.76 | 🟢 1.91 | 🟢 0.80 | 🟢 0.95 | 🟢 0.50 | 🔴 1.95 | 🟢 1.65 | 🟡 1.46 | 🟢 0.99 | 🔴 0.04 | 🟢 8.48 | 🟡 1.00 |
| `BOE_GDP_LONG` | 🟢 1.87 | 🔴 0.60 | 🔴 1.76 | 🟢 1.93 | 🟢 0.79 | 🟢 0.95 | 🟢 0.50 | 🔴 1.94 | 🟢 1.64 | 🟡 1.46 | 🟢 0.99 | 🔴 0.04 | 🟢 8.51 | 🟡 1.00 |
| `BOE_HPI` | 🟡 1.67 | 🔴 0.65 | 🔴 1.68 | 🟢 1.19 | 🟢 0.77 | 🟢 0.97 | 🟡 0.50 | 🔴 1.93 | 🟡 1.46 | 🟢 1.55 | 🟠 0.93 | 🟢 0.12 | 🟢 5.95 | 🟡 1.00 |
| `BOE_INV` | 🟡 1.72 | 🔴 0.61 | 🔴 1.78 | 🔴 5.68 | 🟢 0.78 | 🟢 0.78 | 🔴 2.00 | 🟢 1.58 | 🟢 1.39 | 🔴 1.00 | 🟡 0.96 | 🔴 0.09 | 🟢 6.66 | 🟡 0.99 |
| `BOE_MONEY` | 🟡 1.66 | 🟢 1.32 | 🔴 1.69 | 🟢 1.45 | 🟢 0.49 | 🟢 0.92 | 🟢 0.50 | 🔴 1.91 | 🟢 1.63 | 🟢 1.59 | 🟡 0.98 | 🔴 0.10 | 🟢 5.94 | 🟡 1.00 |
| `BOE_POP` | 🟢 2.02 | 🔴 0.24 | 🔴 1.78 | 🔴 8.84 | 🟢 0.25 | 🟢 0.47 | 🔴 2.00 | 🔴 1.96 | 🟢 1.96 | 🔴 0.45 | 🟢 1.00 | 🔴 0.03 | 🟢 8.69 | 🟡 1.00 |
| `BOE_PRD` | 🟢 1.98 | 🔴 0.34 | 🔴 1.81 | 🔴 6.70 | 🟢 0.64 | 🟢 0.72 | 🔴 2.00 | 🔴 1.93 | 🟢 1.82 | 🔴 0.94 | 🟢 1.00 | 🔴 0.04 | 🟢 6.27 | 🟡 1.00 |
| `BOE_RCONS` | 🟢 1.97 | 🔴 0.48 | 🔴 1.76 | 🟢 2.80 | 🟢 0.57 | 🟢 0.85 | 🟡 1.24 | 🔴 1.97 | 🟢 1.73 | 🟢 1.27 | 🟡 0.98 | 🔴 0.05 | 🟢 6.72 | 🟡 1.00 |
| `BOE_STIR` | 🔴 1.20 | 🟢 1.80 | 🔴 1.24 | 🟢 1.57 | 🟢 0.72 | 🟢 0.68 | 🟢 0.50 | 🔴 1.82 | 🔴 0.43 | 🟢 1.63 | 🟠 0.31 | 🔴 0.08 | 🟢 4.75 | 🟠 0.55 |
| `BOE_UNRATE` | 🔴 1.27 | 🔴 0.54 | 🔴 1.57 | 🔴 4.29 | 🟢 0.92 | 🟡 0.36 | 🟠 1.69 | 🟢 1.46 | 🔴 0.52 | 🟡 1.17 | 🔴 0.22 | 🔴 0.09 | 🟢 4.31 | 🔴 0.49 |
| `BOE_WPI` | 🟢 1.86 | 🔴 0.33 | 🔴 1.80 | 🟢 1.98 | 🟢 0.83 | 🟢 0.70 | 🟢 0.50 | 🔴 1.91 | 🟢 1.65 | 🟢 1.57 | 🔴 0.49 | 🟢 0.13 | 🟢 7.54 | 🟡 1.00 |
| `BOE_YIELD` | 🟡 1.54 | 🟡 0.72 | 🔴 1.81 | 🟢 1.62 | 🟢 0.93 | 🟠 0.29 | 🟡 1.18 | 🟢 1.60 | 🔴 0.84 | 🟢 1.58 | 🔴 0.20 | 🟠 0.12 | 🟢 6.83 | 🔴 0.62 |

## BIS macroprudential (EM + AE, 1970-2025)

### BIS_AE

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟢 1.86 | 🟡 0.90 | 🔴 1.81 | 🔴 7.39 | 🟢 0.87 | 🟠 0.32 | 🔴 2.00 | 🟢 1.39 | 🟢 1.38 | 🔴 0.49 | 🟢 1.00 | 🔴 0.08 | 🟢 6.94 | 🟢 1.00 |
| `BIS_CGAP` | 🟡 1.67 | 🟡 1.01 | 🟢 2.40 | 🔴 6.86 | 🟠 0.95 | 🟠 0.32 | 🔴 1.87 | 🟢 1.42 | 🔴 1.00 | 🔴 0.98 | 🔴 0.32 | 🔴 0.13 | 🟢 6.00 | 🔴 0.57 |
| `BIS_CRATIO` | 🟢 1.90 | 🔴 0.78 | 🔴 1.82 | 🔴 8.56 | 🟢 0.85 | 🔴 0.17 | 🔴 2.00 | 🟢 1.48 | 🟢 1.53 | 🔴 0.46 | 🟢 0.98 | 🔴 0.08 | 🟢 7.02 | 🟢 1.00 |
| `BIS_GVCRED` | 🟢 1.72 | 🟠 0.87 | 🔴 1.87 | 🔴 5.46 | 🟢 0.91 | 🟠 0.33 | 🔴 2.00 | 🟢 1.55 | 🟡 1.24 | 🔴 0.68 | 🟠 0.90 | 🔴 0.11 | 🟢 6.85 | 🟠 0.94 |
| `BIS_HHCRED` | 🟢 1.84 | 🔴 0.51 | 🔴 1.81 | 🔴 12.45 | 🟢 0.82 | 🔴 0.11 | 🔴 2.00 | 🟡 1.78 | 🟢 1.65 | 🔴 0.36 | 🟢 1.00 | 🔴 0.04 | 🟢 7.10 | 🟡 0.99 |
| `BIS_RPP` | 🟡 1.68 | 🔴 0.71 | 🔴 1.82 | 🔴 6.43 | 🟢 0.81 | 🔴 0.17 | 🔴 1.76 | 🔴 1.88 | 🔴 1.12 | 🔴 0.95 | 🔴 0.80 | 🟡 0.13 | 🟢 6.76 | 🔴 0.83 |

### BIS_EM

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟡 1.68 | 🔴 0.76 | 🔴 1.79 | 🔴 7.17 | 🟢 0.85 | 🟡 0.38 | 🟡 1.32 | 🟢 1.64 | 🟠 1.19 | 🔴 1.00 | 🔴 0.65 | 🔴 0.11 | 🟢 6.76 | 🔴 0.90 |
| `BIS_CGAP` | 🟢 1.71 | 🟡 1.19 | 🟢 2.12 | 🔴 12.24 | 🟡 0.92 | 🔴 0.13 | 🔴 2.00 | 🟢 1.51 | 🔴 0.99 | 🔴 0.76 | 🔴 0.39 | 🟠 0.13 | 🟢 5.62 | 🔴 0.35 |
| `BIS_CRATIO` | 🟢 1.75 | 🔴 0.70 | 🔴 1.79 | 🔴 15.19 | 🟢 0.86 | 🟠 0.32 | 🔴 2.00 | 🟢 1.72 | 🟢 1.37 | 🔴 0.66 | 🔴 0.77 | 🔴 0.10 | 🟢 7.11 | 🟢 1.00 |
| `BIS_GVCRED` | 🟢 1.75 | 🟠 1.04 | 🔴 1.96 | 🔴 26.65 | 🟢 0.85 | 🔴 -0.24 | 🔴 2.00 | 🟢 1.41 | 🟠 1.19 | 🔴 0.58 | 🔴 0.60 | 🔴 0.09 | 🟢 5.32 | 🔴 0.61 |
| `BIS_HHCRED` | 🟢 1.82 | 🟡 1.26 | 🔴 1.69 | 🔴 8.82 | 🟢 0.74 | 🔴 -0.15 | 🔴 2.00 | 🟢 0.82 | 🔴 1.12 | 🔴 0.64 | 🔴 0.62 | 🔴 0.11 | 🟢 6.82 | 🟡 0.99 |
| `BIS_RPP` | 🟢 1.73 | 🟢 1.40 | 🔴 1.79 | 🔴 5.07 | 🟢 0.81 | 🔴 -0.23 | 🟡 1.36 | 🟢 1.28 | 🔴 0.96 | 🟡 1.11 | 🔴 0.46 | 🔴 0.11 | 🟢 6.70 | 🔴 0.81 |

### BR_BIS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟡 1.69 | 🟠 0.99 | 🔴 1.73 | 🔴 9.07 | 🔴 0.94 | 🔴 0.33 | 🔴 2.00 | 🟡 1.64 | 🔴 1.19 | 🔴 0.58 | 🟠 0.91 | 🔴 0.07 | 🟢 4.71 | 🔴 0.74 |
| `BIS_CGAP` | 🟢 1.70 | 🔴 1.01 | 🟡 2.06 | 🔴 4.34 | 🟠 0.93 | 🔴 0.11 | 🔴 2.00 | 🔴 1.86 | 🔴 0.91 | 🔴 0.73 | 🔴 0.57 | 🔴 0.08 | 🔴 2.56 | — — |
| `BIS_CRATIO` | 🔴 1.62 | 🔴 0.11 | 🔴 1.87 | 🔴 8.03 | 🟡 0.90 | 🔴 0.47 | 🔴 2.00 | 🔴 1.85 | 🟠 1.20 | 🔴 0.48 | 🟡 1.00 | 🔴 0.09 | 🟢 4.92 | 🟡 0.95 |
| `BIS_HHCRED` | 🟢 1.85 | 🔴 0.63 | 🔴 1.82 | 🔴 8.24 | 🟢 0.68 | 🔴 0.08 | 🔴 2.00 | 🟢 1.41 | 🟢 1.62 | 🔴 0.46 | 🟡 1.00 | 🔴 0.08 | 🟢 5.09 | 🟡 1.00 |
| `BIS_RPP` | 🟢 2.05 | 🔴 0.89 | 🔴 1.80 | 🔴 37.15 | 🟢 0.25 | 🔴 -0.16 | 🔴 2.00 | 🔴 1.98 | 🟢 1.95 | 🔴 0.47 | 🟡 1.00 | 🔴 0.08 | 🟢 4.81 | — — |

### CN_BIS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟢 1.91 | 🟢 1.31 | 🔴 1.78 | 🔴 6.80 | 🟢 0.71 | 🔴 0.27 | 🔴 2.00 | 🟡 1.67 | 🟢 1.54 | 🔴 0.52 | 🟠 0.95 | 🔴 0.06 | 🟢 5.18 | 🟠 0.93 |
| `BIS_CGAP` | 🟠 1.61 | 🟠 1.05 | 🟡 2.20 | 🔴 6.70 | 🟡 0.89 | 🔴 0.37 | 🔴 2.00 | 🟢 1.61 | 🔴 1.08 | 🔴 0.64 | 🔴 0.25 | 🔴 0.12 | 🔴 3.81 | 🔴 0.26 |
| `BIS_CRATIO` | 🟢 1.80 | 🔴 0.83 | 🔴 1.76 | 🔴 11.40 | 🟢 0.88 | 🔴 0.26 | 🔴 2.00 | 🟠 1.79 | 🟢 1.41 | 🔴 0.47 | 🔴 0.82 | 🔴 0.09 | 🟢 5.89 | 🟠 0.93 |
| `BIS_HHCRED` | 🟢 2.05 | 🟠 1.31 | 🔴 1.86 | 🔴 6.11 | 🟢 0.61 | 🔴 0.18 | 🔴 2.00 | 🟢 1.36 | 🟢 1.66 | 🔴 0.47 | 🟡 1.00 | 🔴 -0.02 | 🟢 4.15 | — — |
| `BIS_RPP` | 🔴 1.59 | 🔴 0.37 | 🟢 2.80 | 🔴 11.45 | 🟢 0.87 | 🔴 0.49 | 🔴 2.00 | 🔴 2.10 | 🟠 1.29 | 🔴 0.68 | 🔴 0.64 | 🟠 0.13 | 🔴 3.43 | — — |

### ID_BIS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟢 1.85 | 🟡 1.46 | 🔴 1.92 | 🔴 8.01 | 🟡 0.86 | 🔴 -0.51 | 🔴 2.00 | 🔴 1.84 | 🟢 1.52 | 🔴 0.76 | 🔴 0.58 | 🔴 0.11 | 🟡 4.12 | — — |
| `BIS_CGAP` | 🟢 1.67 | 🟢 1.92 | 🟡 2.08 | 🔴 5.13 | 🟡 0.91 | 🔴 -0.40 | 🟢 0.50 | 🟢 1.26 | 🔴 0.81 | 🟢 1.37 | 🔴 0.32 | 🟡 0.11 | 🟢 5.33 | 🔴 0.42 |
| `BIS_CRATIO` | 🟠 1.54 | 🟢 1.25 | 🟢 2.08 | 🟢 2.42 | 🟢 0.91 | 🔴 -0.24 | 🔴 1.82 | 🟢 1.66 | 🔴 0.88 | 🟢 1.67 | 🔴 0.39 | 🟢 0.13 | 🟢 6.30 | 🔴 0.38 |
| `BIS_HHCRED` | 🟢 1.84 | 🔴 0.20 | 🔴 1.87 | 🟡 3.47 | 🟡 0.85 | 🔴 -0.40 | 🔴 2.00 | 🔴 1.98 | 🟢 1.52 | 🔴 0.87 | 🟠 0.88 | 🔴 0.06 | 🟢 4.69 | — — |
| `BIS_RPP` | 🟢 2.11 | 🟢 2.81 | 🟡 1.74 | 🟢 0.81 | 🟢 0.82 | 🔴 -0.38 | 🟢 1.26 | 🟢 1.05 | 🔴 0.49 | 🟢 1.82 | 🟠 0.52 | 🔴 0.07 | 🟢 2.59 | — — |

### IN_BIS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟢 1.75 | 🔴 0.74 | 🔴 1.69 | 🔴 5.56 | 🟡 0.93 | 🔴 0.08 | 🔴 2.00 | 🟢 1.59 | 🟡 1.28 | 🔴 0.47 | 🟢 0.99 | 🔴 0.09 | 🟢 6.25 | 🟠 0.88 |
| `BIS_CGAP` | 🔴 1.48 | 🔴 0.43 | 🔴 1.79 | 🔴 7.84 | 🔴 0.97 | 🟢 0.53 | 🔴 1.73 | 🔴 1.93 | 🟠 1.12 | 🔴 0.98 | 🔴 0.35 | 🔴 0.11 | 🟠 5.79 | 🔴 0.57 |
| `BIS_CRATIO` | 🟢 1.75 | 🔴 0.08 | 🔴 1.75 | 🔴 17.20 | 🟠 0.94 | 🔴 0.12 | 🔴 2.00 | 🔴 1.95 | 🟢 1.37 | 🔴 0.52 | 🟡 0.92 | 🔴 0.07 | 🟢 6.95 | 🟢 0.99 |
| `BIS_HHCRED` | 🟢 1.80 | 🔴 0.28 | 🔴 1.76 | 🔴 9.60 | 🔴 0.97 | 🔴 0.20 | 🔴 2.00 | 🔴 1.88 | 🔴 1.17 | 🔴 0.50 | 🔴 0.30 | 🔴 0.10 | 🔴 3.09 | — — |
| `BIS_RPP` | 🟢 1.99 | 🔴 0.77 | 🔴 1.79 | 🔴 5.64 | 🔴 0.94 | 🔴 -0.73 | 🔴 1.54 | 🔴 1.89 | 🟢 1.62 | 🔴 0.98 | 🔴 0.68 | 🔴 0.02 | 🟢 3.72 | — — |

### KR_BIS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟢 1.87 | 🟠 0.89 | 🔴 1.74 | 🔴 31.00 | 🟢 0.77 | 🔴 0.13 | 🔴 2.00 | 🟠 1.79 | 🟢 1.53 | 🔴 0.60 | 🟡 1.00 | 🔴 0.10 | 🟢 5.51 | 🟡 1.00 |
| `BIS_CGAP` | 🟢 1.70 | 🟡 0.99 | 🟢 2.08 | 🔴 6.33 | 🟢 0.86 | 🔴 -0.11 | 🔴 2.00 | 🟢 1.67 | 🔴 1.00 | 🔴 0.78 | 🔴 0.18 | 🔴 0.13 | 🔴 5.53 | 🔴 0.41 |
| `BIS_CRATIO` | 🟢 1.85 | 🟡 0.97 | 🔴 1.82 | 🔴 24.59 | 🟢 0.78 | 🔴 -0.00 | 🔴 2.00 | 🟡 1.79 | 🟢 1.49 | 🔴 0.65 | 🟠 0.89 | 🔴 0.11 | 🟢 6.81 | 🟡 0.98 |
| `BIS_GVCRED` | 🟢 1.80 | 🟠 1.02 | 🔴 1.79 | 🔴 11.42 | 🟢 0.83 | 🔴 0.23 | 🔴 2.00 | 🟡 1.75 | 🟢 1.44 | 🔴 0.40 | 🟠 0.97 | 🔴 0.08 | 🟢 5.45 | 🟠 0.96 |
| `BIS_HHCRED` | 🟢 1.92 | 🔴 0.39 | 🔴 1.82 | 🔴 9.09 | 🟢 0.71 | 🟠 0.31 | 🔴 2.00 | 🟢 1.69 | 🟢 1.62 | 🔴 0.56 | 🟡 0.91 | 🔴 0.07 | 🟢 7.00 | 🟢 1.00 |
| `BIS_RPP` | 🟢 1.72 | 🔴 0.68 | 🟢 2.06 | 🟢 2.79 | 🟢 0.82 | 🔴 -0.54 | 🟢 1.31 | 🔴 1.89 | 🟢 1.21 | 🟡 1.17 | 🔴 0.34 | 🔴 0.13 | 🟢 5.99 | 🔴 0.45 |

### MX_BIS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟡 1.71 | 🟠 0.88 | 🔴 1.95 | 🔴 7.78 | 🟢 0.83 | 🔴 -0.18 | 🔴 2.00 | 🔴 1.82 | 🟢 1.38 | 🔴 0.52 | 🔴 0.56 | 🟡 0.13 | 🟢 5.15 | 🔴 0.54 |
| `BIS_CGAP` | 🟢 1.82 | 🟠 1.09 | 🟢 2.24 | 🔴 19.37 | 🟢 0.83 | 🔴 -0.39 | 🔴 1.98 | 🟡 1.85 | 🟢 1.46 | 🔴 0.75 | 🔴 0.40 | 🔴 0.11 | 🔴 4.94 | 🔴 0.41 |
| `BIS_CRATIO` | 🟢 1.70 | 🔴 0.75 | 🟢 2.25 | 🟠 4.67 | 🟢 0.86 | 🔴 -0.39 | 🔴 2.00 | 🟢 1.61 | 🟠 1.21 | 🔴 0.65 | 🔴 0.26 | 🔴 0.12 | 🟠 5.36 | 🔴 0.52 |
| `BIS_HHCRED` | 🟢 1.94 | 🔴 0.37 | 🔴 1.61 | 🔴 10.28 | 🟢 0.79 | 🔴 -0.47 | 🔴 2.00 | 🟢 1.64 | 🟢 1.51 | 🔴 0.51 | 🔴 0.85 | 🔴 0.09 | 🟢 5.03 | 🟡 0.98 |
| `BIS_RPP` | 🟢 1.93 | 🟠 1.35 | 🟡 1.82 | 🟢 0.85 | 🟢 0.81 | 🔴 -0.47 | 🔴 1.69 | 🟢 1.03 | 🔴 0.50 | 🟢 1.80 | 🟠 0.60 | 🟢 0.09 | 🟢 2.56 | — — |

### RU_BIS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟢 1.73 | 🔴 0.32 | 🟡 2.11 | 🟠 3.69 | 🟢 0.88 | 🔴 -0.18 | 🔴 2.00 | 🔴 1.86 | 🔴 0.93 | 🟠 1.02 | 🔴 0.70 | 🟢 0.13 | 🟢 4.40 | 🔴 0.45 |
| `BIS_CGAP` | 🔴 1.60 | 🟠 1.36 | 🟢 4.52 | 🔴 5.54 | 🟢 0.86 | 🟡 0.71 | 🔴 2.00 | 🟠 1.79 | 🔴 1.02 | 🔴 0.86 | 🔴 0.51 | 🔴 0.08 | 🔴 3.11 | — — |
| `BIS_CRATIO` | 🟡 1.74 | 🔴 0.84 | 🔴 1.77 | 🔴 16.47 | 🟢 0.84 | 🔴 0.08 | 🔴 2.00 | 🔴 1.80 | 🟡 1.31 | 🔴 0.39 | 🔴 0.85 | 🔴 0.08 | 🟢 5.06 | 🟡 1.00 |
| `BIS_HHCRED` | 🟢 1.88 | 🔴 0.86 | 🔴 1.83 | 🔴 40.04 | 🟢 0.71 | 🔴 -0.28 | 🔴 2.00 | 🔴 1.87 | 🟢 1.59 | 🔴 0.51 | 🟡 0.98 | 🟠 0.12 | 🟢 4.68 | 🟡 0.97 |
| `BIS_RPP` | 🟢 1.90 | 🟢 2.96 | 🟡 2.14 | 🔴 6.79 | 🟢 0.79 | 🔴 -0.81 | 🔴 1.72 | 🟢 1.50 | 🟡 1.39 | 🔴 0.91 | 🔴 0.48 | 🔴 0.12 | 🟢 4.19 | — — |

### TR_BIS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟡 1.62 | 🟠 1.10 | 🟡 2.16 | 🔴 6.94 | 🟠 0.92 | 🔴 0.41 | 🔴 2.00 | 🟢 1.66 | 🔴 0.94 | 🔴 0.81 | 🔴 0.70 | 🔴 0.10 | 🟡 3.47 | — — |
| `BIS_CGAP` | 🔴 1.57 | 🔴 0.24 | 🟠 1.98 | 🟡 4.63 | 🟠 0.93 | 🔴 0.31 | 🟡 1.46 | 🟠 1.83 | 🔴 1.15 | 🟡 1.25 | 🔴 0.30 | 🟠 0.12 | 🟢 4.34 | 🔴 0.46 |
| `BIS_CRATIO` | 🟢 1.70 | 🔴 0.34 | 🔴 1.84 | 🔴 10.94 | 🟡 0.91 | 🟡 0.53 | 🔴 2.00 | 🟡 1.76 | 🟡 1.32 | 🔴 0.55 | 🟠 0.97 | 🔴 0.10 | 🟢 5.87 | 🟡 1.00 |
| `BIS_GVCRED` | 🟢 1.71 | 🔴 0.34 | 🟢 3.16 | 🟠 3.79 | 🟢 0.89 | 🔴 -0.37 | 🟡 1.30 | 🟢 0.81 | 🔴 0.97 | 🟠 1.11 | 🔴 0.78 | 🔴 0.06 | 🟢 4.09 | — — |
| `BIS_HHCRED` | 🟢 1.80 | 🟢 2.97 | 🔴 1.83 | 🔴 9.99 | 🟢 0.66 | 🟠 0.47 | 🔴 2.00 | 🔴 1.87 | 🟢 1.54 | 🔴 0.35 | 🟡 1.00 | 🔴 0.12 | 🟢 5.94 | 🟡 0.97 |
| `BIS_RPP` | 🟡 1.86 | 🟡 2.22 | 🔴 1.89 | 🔴 5.20 | 🟢 0.75 | 🔴 0.50 | 🟡 1.32 | 🔴 1.90 | 🟢 1.57 | 🔴 0.97 | 🔴 0.59 | 🟢 0.21 | 🟢 3.71 | — — |

### ZA_BIS

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BIS_BUSCRED` | 🟢 1.74 | 🔴 0.61 | 🔴 1.79 | 🔴 4.78 | 🟢 0.89 | 🟡 0.38 | 🟠 1.39 | 🟢 1.76 | 🟠 1.20 | 🔴 1.01 | 🔴 0.75 | 🟠 0.12 | 🟢 6.71 | 🔴 0.90 |
| `BIS_CGAP` | 🟡 1.61 | 🟠 0.93 | 🔴 1.86 | 🟡 3.50 | 🔴 0.96 | 🔴 -0.10 | 🔴 1.85 | 🟠 1.86 | 🔴 0.93 | 🟠 1.07 | 🔴 0.33 | 🔴 0.12 | 🟢 5.31 | 🔴 0.59 |
| `BIS_CRATIO` | 🟡 1.64 | 🟠 0.83 | 🔴 1.96 | 🔴 7.59 | 🟢 0.92 | 🔴 -0.03 | 🔴 2.00 | 🔴 1.93 | 🔴 1.10 | 🔴 0.60 | 🔴 0.83 | 🔴 0.09 | 🟠 6.45 | 🟠 0.95 |
| `BIS_HHCRED` | 🟠 1.68 | 🔴 0.57 | 🔴 1.58 | 🟠 3.47 | 🟢 0.85 | 🔴 -0.38 | 🔴 2.00 | 🟠 1.64 | 🟠 1.26 | 🔴 0.76 | 🟡 0.94 | 🔴 0.08 | 🟢 3.69 | — — |
| `BIS_RPP` | 🔴 1.38 | 🔴 0.71 | 🟢 2.51 | 🟢 2.89 | 🟢 0.84 | 🔴 -0.22 | 🟢 0.50 | 🟡 1.81 | 🔴 0.68 | 🟢 1.38 | 🔴 0.21 | 🔴 0.09 | 🟢 4.98 | 🔴 0.38 |

## Sectoral history (FRED+OWID+BEIS, 1900-2024)

### UK_SH

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `SH_UK_COAL` | 🔴 1.29 | 🟢 2.48 | 🔴 1.70 | 🔴 16.10 | 🟡 0.88 | 🔴 0.15 | 🔴 2.00 | 🟢 1.52 | 🔴 0.69 | 🔴 0.54 | 🟠 0.84 | 🔴 0.06 | 🟢 4.11 | 🟠 0.93 |

### US_SH

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `SH_US_COAL` | 🔴 1.53 | 🟢 1.72 | 🔴 1.93 | 🔴 25.61 | 🟢 0.84 | 🔴 0.26 | 🔴 2.00 | 🟡 1.62 | 🔴 0.95 | 🔴 0.38 | 🟡 0.96 | 🔴 0.05 | 🟢 4.17 | — — |
| `SH_US_COTTON` | 🔴 1.12 | — — | 🔴 0.84 | 🔴 3.38 | 🔴 0.97 | — — | 🔴 2.00 | — — | — — | 🟡 1.29 | 🟢 0.96 | — — | 🟢 2.36 | — — |
| `SH_US_INDPROD` | 🟡 1.72 | 🔴 0.29 | 🔴 1.81 | 🔴 34.60 | 🟢 0.77 | 🟡 0.63 | 🔴 2.00 | 🟡 1.71 | 🟢 1.54 | 🔴 0.46 | 🟡 0.98 | 🔴 0.05 | 🟢 4.85 | 🟡 0.98 |
| `SH_US_RAILFREIGHT` | 🟡 1.85 | — — | 🔴 1.84 | 🟡 3.13 | 🟢 0.51 | — — | 🔴 2.00 | — — | — — | 🔴 0.77 | 🟠 0.93 | — — | 🟢 3.48 | — — |
| `SH_US_STEEL` | 🟢 1.78 | 🔴 0.60 | 🟡 2.13 | 🟡 2.17 | 🟢 0.82 | 🟠 0.52 | 🟢 0.50 | 🟢 1.05 | 🔴 0.91 | 🟢 1.41 | 🔴 0.47 | 🔴 0.08 | 🟢 4.08 | 🟠 0.79 |
| `SH_US_WHEAT` | 🔴 1.13 | 🔴 0.83 | 🔴 1.43 | 🔴 4.86 | 🔴 0.96 | 🔴 0.35 | 🔴 1.79 | 🔴 1.96 | 🔴 0.46 | 🔴 0.98 | 🟠 0.66 | 🔴 0.05 | 🟢 2.13 | — — |
| `SH_US_WPI` | 🟠 1.31 | 🟢 2.75 | 🔴 0.97 | 🟠 3.48 | 🟢 0.81 | 🔴 0.14 | 🔴 2.00 | 🟢 0.49 | 🔴 0.42 | 🔴 1.03 | 🔴 0.33 | 🟢 0.12 | 🟢 4.96 | 🟢 0.79 |

### WORLD_SH

| Variable | hurst_dfa | mfdfa_spectrum | spectrum_slope | hill_tail_exponent | permutation_entropy_complexity | critical_slowdown | levy_stable_fit | k41_scaling | msd_log_log | tsallis_q_gaussian | reflexivity_drift | lyapunov_exponent | bds_independence | reflexivity_multi_window |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `SH_WORLD_COAL` | 🟠 1.65 | 🔴 0.28 | 🔴 1.75 | 🔴 8.41 | 🟢 0.80 | 🟢 0.90 | 🔴 2.00 | 🔴 1.96 | 🟢 1.48 | 🔴 0.96 | 🟡 0.98 | 🔴 0.07 | 🟢 5.34 | 🟡 1.00 |
| `SH_WORLD_OIL` | 🟢 1.93 | 🟢 1.36 | 🔴 1.79 | 🔴 10.11 | 🟢 0.64 | 🟠 0.46 | 🔴 2.00 | 🔴 1.96 | 🟢 1.69 | 🔴 0.36 | 🟡 1.00 | 🔴 0.06 | 🟢 5.32 | 🟡 1.00 |

## Spectre RMT (panel-level) — famille G

Décomposition de la matrice de covariance des variables de chaque groupe. Sous Marchenko-Pastur (matrice de Wishart), les valeurs propres doivent rester dans [λ_min, λ_max]. Les valeurs propres au-dessus de λ_max indiquent des modes de corrélation **structurés** (signal RMT, [Laloux 1999](bibliographie.md)).

| Horizon | Groupe | n obs | n var | λ_max théorique | λ top observé | Modes au-dessus | % bulk |
|---|---|---:|---:|---:|---:|---:|---:|
| `boe` | `UK_BOE` | 317 | 8 | 1.34 | 6.06 | 1 | 12% |
| `long` | `ADV18` | 154 | 6 | 1.43 | 2.96 | 1 | 50% |
| `long` | `ANGLO` | 153 | 9 | 1.54 | 8.54 | 1 | 0% |
| `long` | `G7` | 154 | 6 | 1.43 | 2.94 | 1 | 50% |
| `long` | `USA` | 154 | 6 | 1.43 | 2.80 | 1 | 50% |
| `q` | `G7Q` | 316 | 2 | 1.17 | 1.01 | 0 | 100% |
| `q` | `OECDQ` | 316 | 2 | 1.17 | 1.01 | 0 | 100% |
| `q` | `USA` | 266 | 2 | 1.18 | 1.01 | 0 | 100% |
| `sh` | `WORLD_SH` | 125 | 2 | 1.27 | 1.92 | 1 | 0% |
| `wb` | `BRICS` | 65 | 6 | 1.70 | 4.27 | 1 | 17% |
| `wb` | `G20` | 65 | 6 | 1.70 | 3.77 | 1 | 33% |
| `wb` | `G7` | 65 | 6 | 1.70 | 4.55 | 1 | 17% |

## Mapping retour vers le panorama

Pour chaque famille du panorama Tier 1, le diagnostic implémenté ici qui la teste empiriquement.

| Famille (panorama) | Diagnostic | Lecture |
|---|---|---|
| A — SOC (1/f^β) | `spectrum_slope` | β > 0 statistiquement → spectre rouge structuré |
| A — queues de loi de puissance | `hill_tail_exponent` | α_Hill < 3 → tail lourde compatible SOC |
| B — Multifractalité | `mfdfa_spectrum` | Δα > 0 → spectre f(α) large (multifractal) |
| C — Longue mémoire | `hurst_dfa` | H > 0.5 → persistance significative |
| E — Critical slowing down | `critical_slowdown` | τ_var > 0 + p < 0.05 → variance qui monte → tipping en approche |
| G — RMT | `rmt_panel` | λ_top > λ_max MP → mode de corrélation structurel |
| I — Information | `permutation_entropy_complexity` | H_perm < 1 + C > 0.3 → structuré mais non-périodique |
| J — Lévy flights | `levy_stable_fit` | α < 2 → distribution stable Lévy (non-Gaussienne) |
| P — Cascades K41 | `k41_scaling` | ζ(6)/ζ(3) < 2 → cascade multifractale (anomalous scaling) |
| R — Diffusion anormale | `msd_log_log` | γ ≠ 1 → super- ou sub-diffusion |
| T — Non-extensivité Tsallis | `tsallis_q_gaussian` | q > 1.3 → distribution q-Gaussienne (non-Boltzmann) |
| S — Réflexivité (transversal) | `reflexivity_drift` | KS > 0 + p < 0.05 → distribution drift entre les deux moitiés → changement de régime cognitif |

## Réflexivité (famille S) — lecture transversale

Conformément à la décision design de PR #22 (panorama 21 familles), la **famille S — réflexivité** (Soros 1987 ; Friston 2010 ; Akerlof-Shiller 2009) n'est pas un test isolé mais une **composante transversale obligatoire**. Le diagnostic `reflexivity_drift` (KS deux-échantillons entre les deux moitiés de chaque série) sert d'**indicateur de validité** des 10 autres diagnostics : quand il rejette le null AR(1), cela signifie que la distribution marginale a dérivé sur la fenêtre d'observation. Dans ce cas, les statistiques structurelles (Hurst, β, Δα, etc.) sont valables **uniquement sur la fenêtre analysée**, pas comme lois universelles transhistoriques.

**Variables où la réflexivité est statistiquement significative** (drift rejette null AR(1) à α=0.05) : les autres diagnostics sur ces variables doivent être lus avec un encart "valable sur 1960-2024" (ou la fenêtre concernée). Le rejet du null ici est *attendu* sur les variables financières post-1980 (régime néolibéral) et les variables d'inflation post-Volcker.

| Horizon | Groupe | Variable | KS | p-value |
|---|---|---|---:|---:|
| `bis` | `BIS_AE` | `BIS_BUSCRED` | 1.000 | 0.010 |
| `bis` | `BIS_AE` | `BIS_CRATIO` | 0.982 | 0.010 |
| `bis` | `BIS_AE` | `BIS_HHCRED` | 1.000 | 0.010 |
| `bis` | `BR_BIS` | `BIS_CRATIO` | 1.000 | 0.020 |
| `bis` | `BR_BIS` | `BIS_HHCRED` | 1.000 | 0.020 |
| `bis` | `BR_BIS` | `BIS_RPP` | 1.000 | 0.030 |
| `bis` | `CN_BIS` | `BIS_HHCRED` | 1.000 | 0.040 |
| `bis` | `IN_BIS` | `BIS_BUSCRED` | 0.989 | 0.010 |
| `bis` | `IN_BIS` | `BIS_CRATIO` | 0.920 | 0.040 |
| `bis` | `KR_BIS` | `BIS_BUSCRED` | 1.000 | 0.030 |
| `bis` | `KR_BIS` | `BIS_HHCRED` | 0.911 | 0.050 |
| `bis` | `RU_BIS` | `BIS_HHCRED` | 0.982 | 0.020 |
| `bis` | `TR_BIS` | `BIS_HHCRED` | 1.000 | 0.040 |
| `bis` | `ZA_BIS` | `BIS_HHCRED` | 0.943 | 0.030 |
| `boe` | `UK_BOE` | `BOE_CREDIT` | 1.000 | 0.010 |
| `boe` | `UK_BOE` | `BOE_EQUITY` | 1.000 | 0.010 |
| `boe` | `UK_BOE` | `BOE_GDP` | 0.994 | 0.010 |
| `boe` | `UK_BOE` | `BOE_GDP_LONG` | 0.994 | 0.010 |
| `boe` | `UK_BOE` | `BOE_INV` | 0.957 | 0.050 |
| `boe` | `UK_BOE` | `BOE_MONEY` | 0.977 | 0.050 |
| `boe` | `UK_BOE` | `BOE_POP` | 1.000 | 0.010 |
| `boe` | `UK_BOE` | `BOE_PRD` | 1.000 | 0.010 |
| `boe` | `UK_BOE` | `BOE_RCONS` | 0.979 | 0.030 |
| `long` | `ADV18` | `LH_BANKDEBT` | 0.987 | 0.040 |
| `long` | `ADV18` | `LH_BILLRATE` | 0.947 | 0.040 |
| `long` | `ADV18` | `LH_BONDRATE` | 0.947 | 0.040 |
| `long` | `ADV18` | `LH_BONDTR` | 0.947 | 0.040 |
| `long` | `ADV18` | `LH_BUSCREDIT` | 0.961 | 0.050 |
| `long` | `ADV18` | `LH_CPI` | 1.000 | 0.010 |
| `long` | `ADV18` | `LH_CREDIT` | 0.948 | 0.020 |

_… et 312 autres lignes._

## Synthèse Q méta — clusters d'universalité

La famille Q (universalité / RG / MaxEnt) opère comme méta-cadre : elle regroupe les variables par **signature multi-diagnostique partagée**. Pour la première livraison, on publie une heuristique simple : pour chaque variable, compter combien de diagnostics rejettent le null AR(1)/phase-scramble.

| Horizon | Variable | Diagnostics rejetant | Famille dominante |
|---|---|---:|---|
| `bis` | `BIS_RPP` | 67 / 154 | I — information |
| `bis` | `BIS_HHCRED` | 61 / 154 | C — longue mémoire |
| `bis` | `BIS_BUSCRED` | 59 / 154 | C — longue mémoire |
| `bis` | `BIS_CRATIO` | 59 / 154 | C — longue mémoire |
| `bis` | `BIS_CGAP` | 46 / 154 | T — non-extensivité |
| `bis` | `BIS_GVCRED` | 20 / 56 | C — longue mémoire |
| `boe` | `BOE_MONEY` | 11 / 14 | B — multifractalité |
| `boe` | `BOE_CREDIT` | 10 / 14 | C — longue mémoire |
| `boe` | `BOE_GDP` | 10 / 14 | C — longue mémoire |
| `boe` | `BOE_GDP_LONG` | 10 / 14 | C — longue mémoire |
| `boe` | `BOE_HPI` | 10 / 14 | A — queues de loi de puissance |
| `boe` | `BOE_RCONS` | 10 / 14 | C — longue mémoire |
| `boe` | `BOE_WPI` | 10 / 14 | C — longue mémoire |
| `boe` | `BOE_CPI` | 9 / 14 | C — longue mémoire |
| `boe` | `BOE_DEBTGDP` | 9 / 14 | B — multifractalité |
| `boe` | `BOE_EQUITY` | 9 / 14 | A — queues de loi de puissance |
| `long` | `LH_IMPORTS` | 72 / 84 | C — longue mémoire |
| `long` | `LH_EXPORTS` | 71 / 84 | C — longue mémoire |
| `long` | `LH_MONEY` | 71 / 84 | C — longue mémoire |
| `long` | `LH_EXP` | 69 / 84 | C — longue mémoire |
| `long` | `LH_NARROW` | 68 / 84 | C — longue mémoire |
| `long` | `LH_REV` | 68 / 84 | C — longue mémoire |
| `long` | `LH_BANKDEBT` | 67 / 84 | C — longue mémoire |
| `long` | `LH_CREDIT` | 64 / 84 | B — multifractalité |
| `long` | `LH_MORT` | 64 / 84 | C — longue mémoire |
| `long` | `LH_GDPNOM` | 62 / 84 | C — longue mémoire |
| `q` | `Q_GDP` | 50 / 84 | C — longue mémoire |
| `q` | `Q_INV` | 46 / 70 | C — longue mémoire |
| `q` | `Q_CREDIT` | 42 / 84 | S — réflexivité multi-régime (Tier 2) |
| `q` | `Q_UNRATE` | 38 / 70 | I — information |
| `q` | `Q_CPI` | 34 / 70 | A — queues de loi de puissance |
| `q` | `Q_HPI` | 30 / 84 | C — longue mémoire |
| `q` | `Q_PRD` | 23 / 56 | A — queues de loi de puissance |
| `q` | `Q_YIELD` | 22 / 84 | A — SOC (1/f^β) |
| `sh` | `SH_US_INDPROD` | 8 / 14 | I — information |
| `sh` | `SH_US_STEEL` | 8 / 14 | C — longue mémoire |
| `sh` | `SH_WORLD_OIL` | 7 / 14 | C — longue mémoire |
| `sh` | `SH_US_WPI` | 6 / 14 | B — multifractalité |
| `sh` | `SH_WORLD_COAL` | 6 / 14 | I — information |
| `sh` | `SH_US_COAL` | 5 / 14 | B — multifractalité |
| `sh` | `SH_UK_COAL` | 4 / 14 | B — multifractalité |
| `sh` | `SH_US_RAILFREIGHT` | 4 / 14 | I — information |
| `sh` | `SH_US_COTTON` | 3 / 14 | S — réflexivité (transversal) |
| `sh` | `SH_US_WHEAT` | 1 / 14 | D — non-linéarité IID (Tier 2) |
| `wb` | `CY_POP` | 260 / 630 | I — information |
| `wb` | `CY_PRD` | 235 / 630 | B — multifractalité |
| `wb` | `CY_INF` | 165 / 518 | C — longue mémoire |
| `wb` | `CY_GDP` | 154 / 630 | D — non-linéarité IID (Tier 2) |
| `wb` | `CY_TRD` | 122 / 602 | B — multifractalité |
| `wb` | `CY_FIN` | 112 / 448 | P — cascades K41 |
| `wb` | `CY_INV` | 95 / 616 | A — SOC (1/f^β) |
| `wb` | `CY_UEM` | 95 / 630 | D — non-linéarité IID (Tier 2) |

## Sign-off

- Date de la note : 2026-05-30T07:07:09+00:00
- As-of : 2026-05
- Pipeline : `ecowave dx-diagnostics`
- Nulls : AR(1) bootstrap (Torrence-Compo 1998) + phase-scramble (Theiler 1992), α = 0.05
- Diagnostics : Tier 1 du panorama [Au-delà des cycles](methodology_beyond_cycles.md), spec [feuille de route #15](methodology/feuille_de_route.md#item-15-diagnostics-non-cycliques)
