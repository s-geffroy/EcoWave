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

### BIS_AE

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### BIS_EM

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | disputed | falling | 📉 min dans 8 mois |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | disputed | rising (post-trough) | 📈 max dans 6.3 ans |
| Kondratieff ⚠️ | rejected | — | — |

### BR_BIS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### CN_BIS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | contraction | falling | 📉 min dans 4 mois |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | peak | rising (post-peak) | 📉 min dans 13 ans |

### ID_BIS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | disputed | rising (post-peak) | 📉 min dans 1.7 ans |
| Juglar ⚠️ | expansion | rising (post-trough) | 📈 max dans 3.3 ans |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### IN_BIS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | expansion | rising | 📈 max dans 1.5 ans |
| Kondratieff ⚠️ | rejected | — | — |

### KR_BIS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | expansion | rising | 📈 max dans 1 mois |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | disputed | rising (post-trough) | 📈 max dans 6.8 ans |
| Kondratieff ⚠️ | rejected | — | — |

### MX_BIS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | contraction | falling | 📉 min dans 11 mois |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### RU_BIS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | disputed | rising (post-peak) | 📉 min dans 4.0 ans |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### TR_BIS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | peak | rising (post-peak) | 📉 min dans 1.3 ans |
| Juglar ⚠️ | rejected | — | — |
| Kuznets ⚠️ | rejected | — | — |
| Kondratieff ⚠️ | rejected | — | — |

### ZA_BIS

| Cycle | Phase | Tendance | Prochain extremum |
|---|---|---|---|
| Kitchin ⚠️ | rejected | — | — |
| Juglar ⚠️ | disputed | rising (post-peak) | 📉 min dans 3.8 ans |
| Kuznets ⚠️ | disputed | rising | 📈 max dans 2.6 ans |
| Kondratieff ⚠️ | rejected | — | — |

_⚠️ = effet endpoint CF dominant (les dernières hi_years/2 années sont moins fiables ; la prévision donne l'ordre de grandeur, pas la date exacte)._

## Matrice de phase (Gate 2 — consensus inter-méthode)

| group_code   | kitchin     | juglar    | kuznets   | kondratieff   |
|:-------------|:------------|:----------|:----------|:--------------|
| BIS_AE       | rejected    | rejected  | rejected  | rejected      |
| BIS_EM       | disputed    | rejected  | disputed  | rejected      |
| BR_BIS       | rejected    | rejected  | rejected  | rejected      |
| CN_BIS       | contraction | rejected  | rejected  | peak          |
| ID_BIS       | disputed    | expansion | rejected  | rejected      |
| IN_BIS       | rejected    | rejected  | expansion | rejected      |
| KR_BIS       | expansion   | rejected  | disputed  | rejected      |
| MX_BIS       | contraction | rejected  | rejected  | rejected      |
| RU_BIS       | rejected    | disputed  | rejected  | rejected      |
| TR_BIS       | peak        | rejected  | rejected  | rejected      |
| ZA_BIS       | rejected    | disputed  | disputed  | rejected      |

## p-values AR(1) (Gate 1 — existence du cycle)

| group_code   |   kitchin |   juglar |   kuznets |   kondratieff |
|:-------------|----------:|---------:|----------:|--------------:|
| BIS_AE       |     0.757 |    0.36  |     0.188 |         0.979 |
| BIS_EM       |     0.001 |    0.094 |     0.001 |         0.965 |
| BR_BIS       |     0.679 |    0.68  |     0.474 |         0.997 |
| CN_BIS       |     0.044 |    0.878 |     0.337 |         0.025 |
| ID_BIS       |     0.007 |    0.021 |     0.313 |         0.541 |
| IN_BIS       |     0.171 |    0.173 |     0.001 |         1     |
| KR_BIS       |     0.001 |    0.126 |     0.007 |         0.825 |
| MX_BIS       |     0.015 |    0.092 |     0.414 |         0.739 |
| RU_BIS       |     0.199 |    0.006 |     0.658 |         0.994 |
| TR_BIS       |     0.001 |    0.706 |     0.447 |         1     |
| ZA_BIS       |     0.223 |    0.005 |     0.001 |         0.457 |

## Drapeau d'universalité par cycle (Gate 3 — cross-group)

| cycle       | modal_phase   |   n_groups_concording |   n_groups_total | status   |
|:------------|:--------------|----------------------:|-----------------:|:---------|
| kitchin     | contraction   |                     2 |               11 | regional |
| juglar      | expansion     |                     1 |               11 | regional |
| kuznets     | expansion     |                     1 |               11 | regional |
| kondratieff | peak          |                     1 |               11 | regional |

## Votes par modèle (D/E/F/G) — détail Gate 2

### Kitchin

| group_code   | D           | E           | F           | G           |
|:-------------|:------------|:------------|:------------|:------------|
| BIS_EM       | expansion   | peak        | contraction | contraction |
| CN_BIS       | contraction | contraction | contraction | contraction |
| ID_BIS       | contraction | expansion   | peak        | expansion   |
| KR_BIS       | contraction | expansion   | expansion   | expansion   |
| MX_BIS       | expansion   | contraction | contraction | contraction |
| TR_BIS       | contraction | peak        | peak        | contraction |

### Juglar

| group_code   | D         | E           | F      | G         |
|:-------------|:----------|:------------|:-------|:----------|
| ID_BIS       | expansion | expansion   | trough | expansion |
| RU_BIS       | expansion | contraction | peak   | expansion |
| ZA_BIS       | trough    | expansion   | peak   | expansion |

### Kuznets

| group_code   | D           | E         | F         | G         |
|:-------------|:------------|:----------|:----------|:----------|
| BIS_EM       | contraction | expansion | trough    | expansion |
| IN_BIS       | expansion   | expansion | expansion | expansion |
| KR_BIS       | contraction | trough    | trough    | expansion |
| ZA_BIS       | trough      | trough    | expansion | expansion |

### Kondratieff

| group_code   | D         | E    | F    | G           |
|:-------------|:----------|:-----|:-----|:------------|
| CN_BIS       | expansion | peak | peak | contraction |

## Figures

![Heatmap des phases (consensus)](../figures/cycle_phase_heatmap_2026_05_bis.png)

![Heatmap des amplitudes](../figures/cycle_amplitude_heatmap_2026_05_bis.png)

![Heatmap des p-values (Gate 1)](../figures/cycle_pvalue_heatmap_2026_05_bis.png)

![Frise des prochains extrema](../figures/cycle_next_extremum_timeline_2026_05_bis.png)

![CF band-pass par cycle](../figures/cycle_cf_trajectories_2026_05_bis.png)

![Spectre wavelet (BIS_EM)](../figures/cycle_wavelet_power_2026_05_bis.png)

![Diagramme polaire — Kitchin](../figures/cycle_phase_polar_kitchin_2026_05_bis.png)

![Diagramme polaire — Juglar](../figures/cycle_phase_polar_juglar_2026_05_bis.png)

![Diagramme polaire — Kuznets](../figures/cycle_phase_polar_kuznets_2026_05_bis.png)

![Diagramme polaire — Kondratieff](../figures/cycle_phase_polar_kondratieff_2026_05_bis.png)

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

- Date de la note : 2026-05-29T10:11:47+00:00
- As-of : 2026-05
- Schema EcoWave : `0.5.1`
- Pipeline : `ecowave position-cycles`
