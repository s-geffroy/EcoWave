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

### BRICS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### G20

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### G7

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### HIC

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | disputed | rising | 📈 max dans 1.6 ans |

### LIC

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | contraction | rising (post-trough) | 📈 max dans 1.5 ans |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### LMC

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | disputed | falling | 📈 max dans 4.2 ans |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### OECD

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | disputed | rising | 📈 max dans 1.2 ans |

### UMC

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | contraction | falling | 📉 min dans 6 mois |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### WLD

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | contraction | falling | 📈 max dans 4.5 ans |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | disputed | rising | 📈 max dans 7.3 ans |

_⚠️ = effet endpoint CF dominant (les dernières hi_years/2 années sont moins fiables ; la prévision donne l'ordre de grandeur, pas la date exacte)._

## Matrice de phase (Gate 2 — consensus inter-méthode)

| group_code   | kitchin     | juglar      | kuznets   | kondratieff   |
|:-------------|:------------|:------------|:----------|:--------------|
| BRICS        | rejected    | rejected    | rejected  | rejected      |
| G20          | rejected    | rejected    | rejected  | rejected      |
| G7           | rejected    | rejected    | rejected  | rejected      |
| HIC          | rejected    | rejected    | rejected  | disputed      |
| LIC          | contraction | rejected    | rejected  | rejected      |
| LMC          | rejected    | disputed    | rejected  | rejected      |
| OECD         | rejected    | rejected    | rejected  | disputed      |
| UMC          | rejected    | contraction | rejected  | rejected      |
| WLD          | rejected    | contraction | rejected  | disputed      |

## p-values AR(1) (Gate 1 — existence du cycle)

| group_code   |   kitchin |   juglar |   kuznets |   kondratieff |
|:-------------|----------:|---------:|----------:|--------------:|
| BRICS        |     0.078 |    0.019 |     0.001 |         0.999 |
| G20          |     0.128 |    0.453 |     0.086 |         0.845 |
| G7           |     0.578 |    0.388 |     0.359 |         0.055 |
| HIC          |     0.472 |    0.66  |     0.005 |         0.001 |
| LIC          |     0.001 |    0.234 |     0.32  |         0.506 |
| LMC          |     0.554 |    0.027 |     0.507 |         0.063 |
| OECD         |     0.675 |    0.461 |     0.002 |         0.001 |
| UMC          |     0.778 |    0.001 |     0.031 |         0.38  |
| WLD          |     0.892 |    0.001 |     0.02  |         0.001 |

## Drapeau d'universalité par cycle (Gate 3 — cross-group)

| cycle       | modal_phase   |   n_groups_concording |   n_groups_total | status   |
|:------------|:--------------|----------------------:|-----------------:|:---------|
| kitchin     | contraction   |                     1 |                5 | regional |
| juglar      | contraction   |                     2 |                5 | regional |
| kuznets     | rejected      |                     0 |                5 | regional |
| kondratieff | rejected      |                     0 |                5 | regional |

## Votes par modèle (D/E/F/G) — détail Gate 2

### Kitchin

| group_code   | D           | E           | F      | G           |
|:-------------|:------------|:------------|:-------|:------------|
| LIC          | contraction | contraction | trough | contraction |

### Juglar

| group_code   | D           | E        | F           | G           |
|:-------------|:------------|:---------|:------------|:------------|
| BRICS        | rejected    | rejected | rejected    | rejected    |
| LMC          | peak        | peak     | contraction | contraction |
| UMC          | contraction | peak     | contraction | contraction |
| WLD          | contraction | peak     | contraction | contraction |

### Kuznets

| group_code   | D        | E        | F        | G        |
|:-------------|:---------|:---------|:---------|:---------|
| BRICS        | rejected | rejected | rejected | rejected |
| HIC          | rejected | rejected | rejected | rejected |
| OECD         | rejected | rejected | rejected | rejected |
| UMC          | rejected | rejected | rejected | rejected |
| WLD          | rejected | rejected | rejected | rejected |

### Kondratieff

| group_code   | D    | E    | F         | G           |
|:-------------|:-----|:-----|:----------|:------------|
| HIC          | peak | peak | expansion | contraction |
| OECD         | peak | peak | expansion | contraction |
| WLD          | peak | peak | expansion | contraction |

## Figures

![Heatmap des phases](../figures/cycle_phase_heatmap_2026_05_wb.png)

![CF band-pass par cycle](../figures/cycle_cf_trajectories_2026_05_wb.png)

![Spectre wavelet (WLD)](../figures/cycle_wavelet_power_2026_05_wb.png)

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

- Date de la note : 2026-05-28T14:11:46+00:00
- As-of : 2026-05
- Schema EcoWave : `0.5.0`
- Pipeline : `ecowave position-cycles`
