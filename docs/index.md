# CPV — la macroéconomie n'est pas cyclique

> **La macroéconomie est une cascade multifractale non-linéaire à mémoire
> longue avec dérive de régime cognitif.** Nous l'avons démontré
> empiriquement (cluster diagnostique C+B+D+I+S, 9 436 cellules, 6 panels)
> et validé opérationnellement (benchmark out-of-sample **PASS 78 %** vs
> random walk sur 68 variables).

---

## En une page

**Le verdict empirique** — Les quatre cycles canoniques (Kitchin, Juglar,
Kuznets, Kondratieff) ne survivent pas à un protocole falsifiable
rigoureux. Sur 6 panels macro couvrant 1700–2024, le triple-gate
Gate 1 (dual null AR(1) + phase-scramble) + Gate 2 (consensus 4 méthodes)
+ Gate 3 (universalité cross-aggregates) **rejette systématiquement la
mécanique cyclique**.

**Ce qui émerge à la place** — un cluster diagnostique stable de cinq
familles statistiques :

- **C** — *long memory* (ACF lag-1 ≈ 1)
- **B** — *multifractalité* (singularity spectrum non trivial)
- **D** — *non-linéarité* (BDS, dependence statistic)
- **I** — *information structurée* (entropie, permutation, sample)
- **S** — *reflexive regime drift* (régime cognitif glissant)

**La preuve opérationnelle** — le benchmark Roadmap #20 montre que les
modèles qui reproduisent ce cluster (MSM Calvet-Fisher, ARFIMA+RS
Bhardwaj-Swanson, HAR Corsi) **battent le random walk en out-of-sample
CRPS à horizon 12 sur 52 / 68 variables macro** (78 %, robuste à
n_origins = 12). Les baselines AR(1) / ARMA(1,1) ne gagnent jamais
quand un modèle du cluster est compétent.

| Modèle cluster | Wins | Part |
|---|---|---|
| MSM (Calvet-Fisher) | 23 | 43 % |
| HAR (Corsi 2009) | 16 | 30 % |
| ARFIMA + regime-switching | 14 | 26 % |

---

## Choisir son point d'entrée

Le site est organisé par **audience cible** plutôt que par ordre logique
de la recherche. Choisis ta porte d'entrée — chaque track parle ta
langue et termine par un document phare.

<div class="grid cards" markdown>

-   :material-school: **[Académique →](tracks/acad/index.md)**

    DSGE en accusation, AMH comme méta-cadre, Friston-MRW-AMH comme
    synthèse théorique manquante. *Document phare : paper V2 ~12 000 mots*.

-   :material-bank: **[Banque centrale →](tracks/bc/index.md)**

    Crédibilité monétaire via `d`-GPH, forward guidance réflexif,
    EWS sur tipping points, ARFIMA+RS pour horizons longs.
    *Document phare : note BC ~5 000 mots*.

-   :material-code-tags: **[Quants →](tracks/quants/index.md)**

    MSM / ARFIMA+RS / HAR specs et code, reproduction du PASS 78 %,
    API publique `ecowave.forecasting`, failure modes.
    *Document phare : note quants ~5 000 mots*.

-   :material-book-open-variant: **[Public éclairé →](tracks/public/index.md)**

    Le cycle est mort — voici ce qui le remplace. Vulgarisation
    accessible sans bagage technique. *Document phare : essai
    ~2 500 mots*.

</div>

---

## Si tu cherches le détail technique

- **[Méthode (détail technique)](methodology/protocole_cpv.md)** — les
  trois portes de falsifiabilité, les méthodes de décomposition,
  l'indicateur composite, les garde-fous anti-pseudoscience.
- **[Verdict (preuves détaillées)](forecast_benchmark.md)** — le
  benchmark consolidé multi-panels, les synthèses par horizon, les
  notes signées par panel.
- **[Réfutation des cycles (appendice historique)](cycles/kitchin.md)** —
  où va chacun des 4 cycles canoniques quand on le teste sérieusement.
- **[Référence](groupes.md)** — groupes agrégés, sources de données,
  bibliographie complète, implications détaillées du verdict.
- **[Working paper V1](papers/cpv_main_paper.md)** — version
  réfutation-first de décembre 2025, archivée. Le pivot constructif est
  V2 multi-track (en cours de livraison).

---

!!! info "Reproductibilité"

    Le code Python est entièrement conteneurisé. Un seul `docker
    compose run --rm ecowave forecast-benchmark-consolidate` régénère
    le verdict consolidé à partir des sidecars JSON par panel. Tous
    les chiffres affichés sur cette page sont citables avec leur
    `as_of`. Voir [reproduction (Quants)](tracks/quants/index.md).
