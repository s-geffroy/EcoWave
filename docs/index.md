# CPV — Cycle Position Vector

> **Résumé.** Le projet *Cycle Position Vector* (CPV) est un pipeline de
> recherche reproductible qui décompose les séries macroéconomiques en
> quatre cycles canoniques (Kitchin, Juglar, Kuznets, Kondratieff) et publie,
> pour chaque agrégat de pays, une étiquette de phase soumise à trois portes
> de falsifiabilité (existence du cycle vs bruit rouge ; consensus de quatre
> méthodes hétérogènes ; universalité cross-groupes). Le code, les données
> et les figures sont régénérables d'une seule commande Docker.

![Heatmap des phases — panel Banque mondiale, mai 2026](figures/cycle_phase_heatmap_2026_05_wb.png){ width="100%" }

## Vue d'ensemble

Quatre cycles, quatre méthodes votantes, trois portes de validation, neuf
agrégats. Pour chaque combinaison (groupe, cycle), le pipeline rend public
une phase parmi six étiquettes : `expansion`, `peak`, `contraction`,
`trough`, `disputed`, `rejected` (échec de la porte d'existence).

| Cycle | Période canonique | Phénomène économique | Référence princeps |
|---|---|---|---|
| **Kitchin** | 3–5 ans | Cycle d'inventaire | Kitchin (1923) |
| **Juglar** | 7–11 ans | Cycle d'investissement fixe | Juglar (1862) ; Schumpeter (1939) |
| **Kuznets** | 15–25 ans | Vague infrastructure / démographie | Kuznets (1930) |
| **Kondratieff** | 40–60 ans | Onde techno-économique longue | Kondratieff (1925) ; Korotayev & Tsirel (2010) |

## Les trois portes de falsifiabilité

Une phase n'est publiée pour une cellule (agrégat, cycle, mois) que si les
**trois portes** réussissent :

1. **Existence (Porte 1)** — la puissance dans la bande doit battre un null
   conservatif (AR(1) bootstrap + scramble de phase ; *dual null*) à un seuil
   α = 0.05.
2. **Consensus (Porte 2)** — ≥ 3 méthodes sur 4 (D / E / F / G) doivent
   converger sur la même étiquette.
3. **Universalité (Porte 3)** — ≥ 4 agrégats de revenu sur 5 (WLD / HIC / UMC
   / LMC / LIC) doivent partager la phase modale pour qu'un cycle soit
   qualifié de « global » plutôt que de « régional ».

Les cellules qui échouent à la Porte 1 sont publiées `rejected` ; celles qui
passent la Porte 1 mais échouent la Porte 2 sont publiées `disputed`. Le
protocole **publie ses échecs** — c'est ce qui le distingue de la littérature
classique sur les vagues longues (cf. [Garde-fous](methodology/garde_fous.md)).

## Les quatre méthodes votantes

| Code | Méthode | Référence |
|---|---|---|
| **D** | Détection de ruptures PELT | Killick *et al.* (2012) |
| **E** | Markov-switching AR(1) | Hamilton (1989) |
| **F** | Filtre Christiano-Fitzgerald + phase de Hilbert | Christiano & Fitzgerald (2003) |
| **G** | Datation de retournements Bry-Boschan / Harding-Pagan | Bry & Boschan (1971) ; Harding & Pagan (2002) |

Les quatre méthodes incarnent des **hypothèses génératives très
hétérogènes** : un consensus à 3/4 indique qu'aucun artéfact méthodologique
unique ne pilote le résultat. La survie sous la Porte 1 montre qu'aucun
bruit auto-corrélé ne pilote le résultat non plus. Survey complet et
matrice de décision sur [Méthodes de décomposition](methodology/methodes_decomposition.md).

## Résultats principaux — mai 2026

Sur le panel Banque mondiale (1960-2024, 9 agrégats × 4 bandes, 36 cellules,
1000 surrogates par cellule, dual null) :

| Cycle | Cellules en `rejected` | Phase modale | Cellules `disputed` |
|---|---:|---|---:|
| Kitchin | 8 / 9 | — | 0 |
| Juglar | 5 / 9 | contraction | 1 |
| Kuznets | 9 / 9 | — | 0 |
| Kondratieff | 9 / 9 | — | 0 |

Sur le panel d'histoire longue (Maddison Project 2023 + Jordà-Schularick-Taylor R6,
1870-2022, 6 agrégats × 4 bandes), la K-wave émerge sur ADV18 et EU4
(`disputed` au pic, φ ≈ 0 ; amplitude ≈ moitié des pics K3/K4 historiques) ;
voir [Kondratieff K5](reports/kondratieff_adv18_eu4_2026.md). La divergence
Juglar US/ANGLO (expansion, pic ~2024) vs NORDIC (contraction profonde,
creux fin-2023) est documentée sur [Juglar 2022-2026](reports/juglar_us_anglo_nordic_2026.md).

## Démarrage rapide

```bash
docker compose build
docker compose run --rm --entrypoint ecowave ecowave init-db
docker compose run --rm --entrypoint ecowave ecowave position-cycles \
  --as-of 2026-05 --null dual --n-surrogates 1000
```

Données ingérées automatiquement depuis l'API Banque mondiale. Pour la
fenêtre 1870-2022, ajouter `--horizon long --manifest /app/long_history_manifest.json` ;
les fichiers Maddison et JST R6 doivent avoir été téléchargés au préalable
(`scripts/download_macrohistory.sh`).

## Navigation

- [**Protocole CPV**](methodology/protocole_cpv.md) — spécification détaillée
- [**Cycles canoniques**](cycles/kitchin.md) — une page par bande
- [**Groupes**](groupes.md) — composition des agrégats
- [**Résultats**](reports/panel_banque_mondiale_2026.md) — notes signées
- [**Analyses approfondies**](reports/juglar_us_anglo_nordic_2026.md)
- [**Bibliographie**](bibliographie.md) — toutes les références consolidées
- [**Sources de données**](sources.md)

---

*Schéma de base de données : 0.5.0. Dépôt :
[s-geffroy/EcoWave](https://github.com/s-geffroy/EcoWave).
Méthodes empruntées à : Christiano & Fitzgerald (2003) ; Hamilton (1989) ;
Killick et al. (2012) ; Harding & Pagan (2002) ; Theiler et al. (1992) ;
Torrence & Compo (1998).*
