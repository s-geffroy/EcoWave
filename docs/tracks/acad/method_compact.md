# Méthode CPV en langage théoricien

> *Formalisation statistique du protocole CPV. Pour économistes qui
> veulent en lire la rigueur méthodologique sans dépendre de la
> documentation tutorielle.*

## Position dans la littérature

Le protocole CPV (Cycle Position Vector) s'inscrit dans trois
traditions méthodologiques convergentes :

1. **Tradition Box-Jenkins étendue aux processus à longue mémoire** —
   Granger-Joyeux 1980, Hosking 1981, Beran 1994. Le paramètre `d` de
   différenciation fractionnaire formalise l'intuition que les chocs
   macroéconomiques s'étendent sur des temps caractéristiques bien
   supérieurs aux fréquences cycliques canoniques.
2. **Tradition Theiler-Vyushin-Kushner pour la null hypothesis
   structurée** — Theiler 1992, Vyushin-Kushner 2009. Le bootstrap
   AR(1) absorbe une partie du contenu cyclique dans le paramètre de
   persistance `φ` ; le phase-scrambling préserve exactement le spectre
   mais détruit la phase. La dual null AR(1) + phase-scrambling
   constitue un test conservateur plus strict que chaque null
   individuel.
3. **Tradition Hamilton-Killick-Bry-Boschan pour le consensus
   multi-méthode** — Hamilton 1989 (Markov-switching), Killick-
   Fearnhead-Eckley 2012 (PELT), Christiano-Fitzgerald 2003 (band-pass
   filter), Harding-Pagan 2002 (Bry-Boschan turning points). Voter sur
   4 méthodes aux hypothèses génératives différentes permet de séparer
   le signal cyclique réel des artefacts spécifiques à chaque méthode.

## Les trois portes formellement

### Gate 1 — Dual null hypothesis test

Soit `X_t` une série macroéconomique observée sur `T` périodes. Soit
`B(ω; X)` la band-power dans une bande fréquentielle `ω = [ω_1, ω_2]`
correspondant à un cycle candidat (Kitchin : `ω ∈ [2π/5, 2π/3]`, etc.).

**Test 1 — AR(1) bootstrap.** On ajuste un AR(1) sur `X` :
`X_t = c + φ X_{t-1} + ε_t`. On simule `B = 1 000` trajectoires
indépendantes du même AR(1). Pour chaque trajectoire on calcule
`B(ω; X^{(b)})`. La p-value est la fraction des simulations où
`B(ω; X^{(b)}) ≥ B(ω; X)`.

**Test 2 — Phase-scrambling.** On calcule la DFT de `X`, on randomise
les phases en préservant le module, on inverse la DFT pour obtenir
`X^{(s)}`. On répète `B = 1 000` fois. La p-value est analogue.

**Dual null.** La cellule passe Gate 1 ssi `p_{AR(1)} < α` ET
`p_{phase} < α` avec α = 0.05.

Code : `ecowave/cycles/surrogate.py` → `dual_null`.

### Gate 2 — Consensus multi-méthode

Soit quatre méthodes de décomposition `M_1, M_2, M_3, M_4` aux
hypothèses génératives différentes :

- `M_1` = PELT (Killick-Fearnhead-Eckley 2012)
- `M_2` = Markov-switching (Hamilton 1989)
- `M_3` = Christiano-Fitzgerald + Hilbert (Christiano-Fitzgerald 2003)
- `M_4` = Bry-Boschan (Harding-Pagan 2002)

Chaque méthode vote sur la phase courante du cycle :
`v_k = M_k(X) ∈ {contraction, expansion, peak, trough}`.

**Critère** : la phase modale est publiée ssi `|{k : v_k = mode}| ≥ 3`.

Code : `ecowave/cycles/consensus.py`.

### Gate 3 — Cross-aggregate universality

Soit `G = {WLD, HIC, UMC, LMC, LIC}` les 5 agrégats de revenu standard
WB. Pour chaque agrégat `g ∈ G`, on calcule la phase courante
`φ_g(X^{(g)})` après Gates 1 et 2.

**Critère** : le cycle est qualifié `universal` ssi
`|{g ∈ G : φ_g(X^{(g)}) = mode}| ≥ 4`.

Code : `ecowave/cycles/universality.py`.

## La safeguard Roadmap #14

Une faiblesse du protocole standard : la composite Gate 1 z-score puis
moyenne. Sur des agrégats où une seule variable domine en variance, le
composite hérite de cette variable et masque la diversité. Roadmap #14
introduit une safeguard per-variable :

**Critère étendu** : la phase composite n'est publiée que si **au
moins 50 %** des variables composantes survivent individuellement aux
trois portes. Sinon le composite est marqué `aggregation_artifact`.

Code : `ecowave/cycles/evidence.py` → `compute_per_variable_evidence`.

## La pré-différenciation pour Kondratieff

Sur les bandes Kondratieff (40-60 ans) on observe que la simple
band-power du composite est dominée par les **tendances de long
terme** plutôt que par d'éventuels cycles. La pré-différenciation
first-difference avant Gate 1 isole la composante cyclique vraie de
la tendance.

Code : voir [`methodology_differencing_for_kondratieff.md`](../../methodology_differencing_for_kondratieff.md).

## Les 14 diagnostics non-cycliques (Tier 1+2)

En complément des 3 portes, le protocole calcule 14 statistiques
diagnostiques non-cycliques regroupées en 11 familles théoriques (A
SOC, B multifractality, C long memory, E critical slowdown, G RMT, I
information, J Lévy flights, P K41 turbulence, R anomalous diffusion,
T Tsallis non-extensivity, S reflexivity).

Chaque diagnostic est scoré contre une null AR(1) ou phase-scramble
au même seuil α = 0.05. Un cluster diagnostique stable émerge sur les
6 panels : C+B+D+I+S (5 familles), qu'aucun cadre théorique unique ne
prédit conjointement à partir de premiers principes.

Code : `ecowave/cycles/alternative_dynamics.py`.

Détail : voir [`dx_diagnostics.md`](../../dx_diagnostics.md).

## Le band-agnostic design

Tous les diagnostics non-cycliques sont calculés **sans présupposer
une bande fréquentielle cible**. Contrairement aux Gates 1-3 qui
testent l'existence d'un cycle à une fréquence donnée, les diagnostics
détectent des propriétés statistiques globales de la série.

Cela offre un complément falsifiable au Gate 1 : si Gate 1 rejette
mais les diagnostics confirment une structure non-cyclique forte
(`d > 0`, multifractality, BDS, etc.), on a une description positive
du processus génératif.

Voir [`methodology_safeguard_roadmap_14.md`](../../methodology_safeguard_roadmap_14.md).

## Reproductibilité technique

L'ensemble du protocole est conteneurisé Docker :

```bash
docker compose run --rm ecowave position-cycles --horizon long
docker compose run --rm ecowave dx-diagnostics --as-of 2026-05
```

Tests : 225 passing. mkdocs strict : passing.

Tout est public sous licence MIT sur
[GitHub](https://github.com/s-geffroy/EcoWave).

## Pour aller plus loin

### Méthode

- [Le protocole CPV complet](../../methodology/protocole_cpv.md)
- [Les 3 portes en détail](../../methodology/trois_portes.md)
- [Garde-fous anti-pseudoscience](../../methodology/garde_fous.md)
- [Au-delà des cycles — 21 familles](../../methodology_beyond_cycles.md)

### Verdict empirique

- [Verdict constructif](verdict_constructive.md) — cluster + benchmark
- [Forecast benchmark consolidé](../../forecast_benchmark.md) — PASS 78 %
- [Évidence par variable](../../evidence_per_variable.md) — Wen 2005

### Théorie

- [DSGE en accusation](dsge_in_dock.md) — 3 modifications structurelles requises
- [Synthèse AMH](synthesis_amh.md) — Friston + MRW + AMH comme méta-cadre
- [5 prédictions falsifiables](falsifiable_predictions.md)
- [Paper V2 académique](paper_v2_academic.md) — ~12 000 mots, dramaturgie constructive
- [Paper V1 archive](../../papers/cpv_main_paper.md) — réfutation-first, décembre 2025
