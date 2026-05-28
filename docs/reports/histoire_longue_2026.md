# Position cyclique mondiale, mai 2026 — panel d'histoire longue (Maddison + JST)

> **Résumé.** Run CPV sur le panel d'histoire longue 1870-2022 (6 variables,
> 6 agrégats × 4 bandes, $B = 1\,000$ surrogates, null dual AR(1) + scramble).
> **8 cellules sur 24 survivent à la Porte 1** ; signaux principaux :
> Juglar USA / ANGLO / NORDIC ($p \leq 0.028$) ; Kondratieff ADV18 / EU4
> ($p = 0.002$ et $p = 0.018$, `disputed` au pic K5). Aucun cycle n'est
> qualifié `universal` au sens cross-revenu (le panel ne contient pas de
> stratification de revenu) ; le drapeau Porte 3 est calculé sur les
> 6 agrégats long-history disponibles. K3 et K4 historiques sont retrouvés
> à $\pm 5$ ans de la datation [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010).

## Notation et paramètres

| Symbole / paramètre | Valeur |
|---|---|
| Fenêtre | 1870 – 2022 (153 années) |
| Sources | Maddison Project 2023 + Jordà-Schularick-Taylor R6 |
| Variables | 6 (`LH_GDP`, `LH_CREDIT`, `LH_HPI`, `LH_EQUITY`, `LH_YIELD`, `LH_CPI`) |
| Agrégats | ADV18, G7, USA, EU4, ANGLO, NORDIC |
| Méthode passe-bande | Christiano-Fitzgerald asymétrique |
| Null | dual (AR(1) + scramble de phase) |
| $B$ (surrogates) | $1\,000$ |
| $\alpha$ (seuil Porte 1) | $0.05$ |
| $k$ (seuil Porte 2) | $3 / 4$ |
| $q$ (seuil Porte 3) | non applicable (pas de stratification de revenu) |

Composition des agrégats : voir [Groupes](../groupes.md). Notamment ADV18
réunit les 18 économies avancées couvertes par JST.

## Heatmap des phases (Porte 2 — consensus inter-méthode)

![Heatmap des phases — panel long-history mai 2026](../figures/cycle_phase_heatmap_2026_05_long.png){ width="95%" }

## Heatmap des amplitudes Hilbert

![Heatmap des amplitudes — panel long-history mai 2026](../figures/cycle_amplitude_heatmap_2026_05_long.png){ width="95%" }

## Heatmap des p-values dual-null (Porte 1)

![Heatmap des p-values dual — panel long-history mai 2026](../figures/cycle_pvalue_heatmap_2026_05_long.png){ width="95%" }

Sur 24 cellules, 8 sortent vertes (Juglar 4/6, Kondratieff 2/6).

## Frise des prochains extrema

![Frise des prochains extrema — panel long-history mai 2026](../figures/cycle_next_extremum_timeline_2026_05_long.png){ width="95%" }

Lecture rapide : USA et ANGLO convergent vers un pic Juglar à
~2 ans d'horizon (~2028) ; NORDIC est encore en contraction profonde
et projette son prochain pic vers 2030 ; EU4 projette un pic K5 vers
2030 également mais avec un caveat endpoint sévère.

## Matrice de phase (Porte 2)

| Agrégat | Kitchin | Juglar | Kuznets | Kondratieff |
|---|---|---|---|---|
| ADV18 | rejected | rejected | rejected | **disputed** |
| ANGLO | rejected | disputed | rejected | rejected |
| EU4 | rejected | rejected | rejected | **disputed** |
| G7 | rejected | disputed | rejected | rejected |
| NORDIC | rejected | **contraction** | rejected | rejected |
| USA | rejected | **expansion** | rejected | rejected |

## p-values dual-null (Porte 1)

| Agrégat | Kitchin | Juglar | Kuznets | Kondratieff |
|---|---:|---:|---:|---:|
| ADV18 | 0.259 | 0.086 | 0.152 | **0.002** |
| ANGLO | 0.760 | **0.001** | 0.202 | 0.854 |
| EU4 | 0.471 | 0.527 | 0.065 | **0.018** |
| G7 | 0.207 | **0.003** | 0.187 | 0.314 |
| NORDIC | 0.161 | **0.028** | 0.154 | 0.678 |
| USA | 0.098 | **0.001** | 0.306 | 0.774 |

## Votes par modèle (Porte 2, détail)

### Juglar

| Agrégat | D | E | F | G | Étiquette |
|---|---|---|---|---|---|
| ANGLO | contraction | trough | expansion | expansion | `disputed` (2/4 expansion) |
| G7 | peak | peak | contraction | contraction | `disputed` (2/4 peak) |
| NORDIC | contraction | contraction | contraction | contraction | **contraction (4/4)** |
| USA | peak | expansion | expansion | expansion | **expansion (3/4)** |

### Kondratieff

| Agrégat | D | E | F | G | Étiquette |
|---|---|---|---|---|---|
| ADV18 | peak | peak | expansion | contraction | `disputed` (2/4 peak) |
| EU4 | peak | peak | expansion | contraction | `disputed` (2/4 peak) |

Le `disputed` au pic K5 correspond à la configuration de votes attendue
au sommet d'un cycle : D et E (méthodes de régime) lisent un pic ;
F (méthode CF + Hilbert) lit encore l'expansion finale ; G (datation de
retournements) anticipe la contraction. Voir
[Kondratieff K5 — ADV18 / EU4](kondratieff_adv18_eu4_2026.md).

## Trajectoires CF par bande

![CF band-pass — panel long-history mai 2026](../figures/cycle_cf_trajectories_2026_05_long.png){ width="95%" }

## Spectre wavelet (ADV18)

![Puissance wavelet ADV18 — panel long-history mai 2026](../figures/cycle_wavelet_power_2026_05_long.png){ width="80%" }

Trois bandes ressortent visuellement : Juglar (7-11 ans, persistant
sur toute la fenêtre), Kuznets (15-25 ans, intermittent et de plus
faible amplitude), Kondratieff (40-60 ans, deux maxima vers 1920 et
1973, atténuation post-1990).

## Diagrammes de phase polaires

![Diagramme polaire Juglar — panel long-history mai 2026](../figures/cycle_phase_polar_juglar_2026_05_long.png){ width="90%" }

![Diagramme polaire Kondratieff — panel long-history mai 2026](../figures/cycle_phase_polar_kondratieff_2026_05_long.png){ width="90%" }

## Observations

1. **Juglar USA et ANGLO** sont en expansion (3/4 et 2/4 votes
   respectivement) avec $p \leq 0.001$. Prochain pic projeté à
   ~2 ans (mi-2028).
2. **Juglar NORDIC** est en contraction profonde (4/4 votes), $p = 0.028$.
   La trajectoire $\sim 1.6$ ans en avance de phase par rapport à USA
   correspond à la conjonction de trois chocs régionaux (Riksbank
   2022-2024, énergie norvégienne, choc commercial finlandais avec la
   Russie). Voir [Juglar US/ANGLO vs NORDIC](juglar_us_anglo_nordic_2026.md).
3. **Kondratieff ADV18 et EU4** sortent `disputed` au pic K5 ($\varphi
   \approx -0.03$ pour ADV18, $-0.48$ pour EU4 ; amplitude ~0.85, soit
   environ la moitié des pics K3 ~1.55 et K4 ~1.28 historiques). Cette
   atténuation du pic K5 est cohérente avec la thèse de la stagnation
   séculaire ([Summers, 2014](../bibliographie.md#summers-2014) ;
   [Gordon, 2016](../bibliographie.md#gordon-2016)). Voir
   [Kondratieff K5](kondratieff_adv18_eu4_2026.md).
4. **Validation historique** : K3 (pic ~1920) et K4 (pic ~1973) sont
   retrouvés par CPV à $\pm 5$ ans de la datation
   [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010), ce qui valide
   la méthode sur cette bande malgré le caveat endpoint sévère.
5. **Kuznets non détectable** sur aucun agrégat — 2.5–4 cycles sur 153
   ans, statistiquement insuffisant même pour le panel long.

## Caveats

- **Endpoint CF** : les $\lfloor \text{hi\_years}/2 \rfloor$ dernières
  années sont marquées `endpoint_caveat = 1` ; pour Kondratieff, cela
  inclut tout l'après-1992.
- **Recouvrement Maddison / JST** : les deux sources se recouvrent
  partiellement (PIB par habitant présent dans les deux). Le pipeline
  déduplique sur `(country, year)` en conservant la donnée la plus
  récente.
- **Composition ADV18 fixée** : 18 pays définis par JST R6 ;
  modifier la composition exige une revue méthodologique
  ([Garde-fous](../methodology/garde_fous.md)).
- **Univesalité** : la Porte 3 reportée ici est calculée sur 6 agrégats
  géographiquement définis, pas sur 5 classes de revenu comme pour le
  panel WB. Les statuts `regional` doivent être interprétés en
  conséquence (un cycle « régional » sur USA + EU4 est en réalité
  ADV18-spécifique).

## Références

- [Bolt & van Zanden / Maddison Project Database (2023)](../bibliographie.md#maddison-2023)
- [Jordà, Schularick & Taylor (2017)](../bibliographie.md#jorda-schularick-taylor-2017)
- [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010)
- [Gordon (2016)](../bibliographie.md#gordon-2016)
- [Summers (2014)](../bibliographie.md#summers-2014)
- [Perez (2002)](../bibliographie.md#perez-2002)

---
*As-of : 2026-05. Pipeline : `position-cycles --horizon long --null dual
--n-surrogates 1000 --manifest /app/long_history_manifest.json`. Schéma
DB : 0.5.0.*
