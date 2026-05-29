# Où se situe le monde en 2026-05 dans les 4 cycles canoniques ?

> Note signée — sortie du protocole CPV (Cycle Position Vector).
> Méthode : CF band-pass + Morlet wavelet + Hilbert phase + Markov-switching
> + Bry-Boschan, avec 3 gates de falsifiabilité (existence AR(1), consensus
> méthodologique ≥3/4, universalité cross-group ≥4/5). Voir
> `methodology/multi_cycle_decomposition.md` pour la spécification complète.

## Glossaire des agrégats

| Code | Définition |
|---|---|
| `WLD` | Monde — agrégat World Bank (population + GDP pondérés) |
| `OECD` | OECD — 38 pays membres de l'Organisation de Coopération et de Développement Économiques |
| `HIC` | High-Income Countries — RNB/hab > 14 005 USD (seuil WB 2024-2025) |
| `UMC` | Upper-Middle-Income — RNB/hab entre 4 516 et 14 005 USD |
| `LMC` | Lower-Middle-Income — RNB/hab entre 1 146 et 4 515 USD |
| `LIC` | Low-Income Countries — RNB/hab ≤ 1 145 USD |
| `G7` | G7 — USA, GBR, FRA, DEU, ITA, JPN, CAN (recompute pondéré PIB) |
| `G20` | G20 — 19 pays principaux (zone UE traitée par DEU+FRA+ITA) |
| `BRICS` | BRICS+ — Brésil, Russie, Inde, Chine, Afrique du Sud, Égypte, Émirats arabes unis, Éthiopie, Iran, Indonésie (10 pays, expansion Jan-2024 + Jan-2025) |

## Récapitulatif par agrégat (position, tendance, prochain extremum)

Pour chaque groupe, position du cycle, tendance instantanée et
ETA du prochain pic/creux (calculé via la fréquence instantanée Hilbert :
Δt = ((φ_cible − φ) mod 2π) / ω, où ω = 2π / période centrale de la bande).

### EA

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### G7Q

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### GBR

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### JPN

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### OECDQ

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### USA

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

_⚠️ = effet endpoint CF dominant (les dernières hi_years/2 années sont moins fiables ; la prévision donne l'ordre de grandeur, pas la date exacte)._

## Matrice de phase (Gate 2 — consensus inter-méthode)

| group_code   | kitchin   | juglar   | kuznets   | kondratieff   |
|:-------------|:----------|:---------|:----------|:--------------|
| EA           | rejected  | rejected | rejected  | rejected      |
| G7Q          | rejected  | rejected | rejected  | rejected      |
| GBR          | rejected  | rejected | rejected  | rejected      |
| JPN          | rejected  | rejected | rejected  | rejected      |
| OECDQ        | rejected  | rejected | rejected  | rejected      |
| USA          | rejected  | rejected | rejected  | rejected      |

## p-values AR(1) (Gate 1 — existence du cycle)

| group_code   |   kitchin |   juglar |   kuznets |   kondratieff |
|:-------------|----------:|---------:|----------:|--------------:|
| EA           |     0.388 |    0.252 |     0.428 |         0.551 |
| G7Q          |     0.106 |    0.531 |     0.12  |         0.516 |
| GBR          |     0.297 |    0.025 |     0.004 |         0.945 |
| JPN          |     0.001 |    0.528 |     0.041 |         0.302 |
| OECDQ        |     0.106 |    0.531 |     0.12  |         0.516 |
| USA          |     0.185 |    0.421 |     0.001 |         0.476 |

## Drapeau d'universalité par cycle (Gate 3 — cross-group)

| cycle       | modal_phase   |   n_groups_concording |   n_groups_total | status   |
|:------------|:--------------|----------------------:|-----------------:|:---------|
| kitchin     | rejected      |                     0 |                6 | regional |
| juglar      | rejected      |                     0 |                6 | regional |
| kuznets     | rejected      |                     0 |                6 | regional |
| kondratieff | rejected      |                     0 |                6 | regional |

## Figures

![Heatmap des phases (consensus)](../figures/cycle_phase_heatmap_2026_05_q.png)

![Heatmap des amplitudes](../figures/cycle_amplitude_heatmap_2026_05_q.png)

![Heatmap des p-values (Gate 1)](../figures/cycle_pvalue_heatmap_2026_05_q.png)

![Frise des prochains extrema](../figures/cycle_next_extremum_timeline_2026_05_q.png)

![CF band-pass par cycle](../figures/cycle_cf_trajectories_2026_05_q.png)

![Spectre wavelet (USA)](../figures/cycle_wavelet_power_2026_05_q.png)

![Diagramme polaire — Kitchin](../figures/cycle_phase_polar_kitchin_2026_05_q.png)

![Diagramme polaire — Juglar](../figures/cycle_phase_polar_juglar_2026_05_q.png)

![Diagramme polaire — Kuznets](../figures/cycle_phase_polar_kuznets_2026_05_q.png)

![Diagramme polaire — Kondratieff](../figures/cycle_phase_polar_kondratieff_2026_05_q.png)

## Lecture par cycle (ancrage littérature)

- **Kitchin (3-5 ans)** — cycle d'inventaire. Référence : Kitchin (1923) ;
  contestation moderne : Diebolt & Doliger (2008).
- **Juglar (7-11 ans)** — cycle d'investissement fixe. Référence :
  Schumpeter (1939) ; opérationalisation : Harding & Pagan (2002).
- **Kuznets (15-25 ans)** — cycle infrastructure/démographie. Référence :
  Kuznets (1930) ; lecture financière : Borio & Drehmann (2009).
- **Kondratieff (40-60 ans)** — vague techno-économique longue. Référence :
  Kondratieff (1925) ; lecture quantitative : Korotayev & Tsirel (2010).

## Caveats

- **Effet endpoint CF** : les dernières `hi_years/2` années sont moins
  fiables (filtre asymétrique). Les cellules concernées sont marquées
  `endpoint_caveat=1` dans la table `cycle_positions`.
- **Fréquence annuelle WB** : Kitchin (3-5 ans) est borderline ; la bande
  basse 3a est inutilisable annuellement (Nyquist).
- **Small-N Kondratieff** : WB démarre en 1960, soit ≈ 1.0-1.5 K-wave. Le
  null AR(1) peut rejeter Kondratieff (`separable=0`) pour plusieurs
  groupes : c'est honnête, pas un échec.

## Sign-off

- Date de la note : 2026-05-29T12:08:25+00:00
- As-of : 2026-05
- Schema EcoWave : `0.5.1`
- Pipeline : `ecowave position-cycles`
