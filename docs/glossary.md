# Glossaire

!!! success "TL;DR"

    Glossaire des termes techniques utilisés cross-track. Organisation alphabétique. Chaque entrée pointe vers une page détaillée. Termes les plus consultés : [CRPS](#crps-continuous-ranked-probability-score) · [Cluster C+B+D+I+S](#cluster-cbdis) · [Dual null](#dual-null) · [GPH](#gph-geweke-porter-hudak-1983) · [MSM](#msm-markov-switching-multifractal) · [ProbabilisticForecast](#probabilisticforecast).

## Index rapide

- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w)

---

## A

### Acceptance criterion (Roadmap #20)

Le critère falsifiable du benchmark : "≥ 1 modèle du cluster doit
battre random walk en out-of-sample CRPS à h = 12 sur ≥ 50 % des
variables". Vérifié à PASS 78 % (53/68) sur les 6 panels. Voir
[verdict consolidé](forecast_benchmark.md).

### AMH (Adaptive Markets Hypothesis)

Cadre conceptuel de Lo (2017) qui voit les marchés comme écosystèmes
évolutifs d'agents bornés rationnels. Englobe S + B + I + apprentissage
mais n'est pas calibrable directement. Couvre 4/5 piliers du cluster
CPV. Voir [synthèse AMH](tracks/acad/synthesis_amh.md).

### AR(1)

Modèle autorégressif d'ordre 1 : `X_t = c + φ X_{t-1} + ε_t`. Utilisé
comme baseline stationnaire dans le benchmark Roadmap #20. Fallback
vers random walk si `|φ| ≥ 0.999`.

### ARFIMA(p, d, q)

ARMA généralisé à intégration fractionnaire. `d ∈ (-0.5, 0.5)` capture
la longue mémoire exacte. Notre implémentation est ARFIMA(0, d, 0)
avec Markov regime-switching à 2 états sur le résidu. Voir
[arfima_rs](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/arfima_rs.py).

## B

### BDS test (Brock-Dechert-Scheinkman 1996)

Test non-paramétrique de non-linéarité contre l'hypothèse IID. Rejette
sur ~75 % des cellules CPV. Composante de la famille D du cluster.
Voir [diagnostics](dx_diagnostics.md).

### Bry-Boschan

Méthode classique de détection de turning points dans les séries
macroéconomiques (Harding-Pagan 2002). Utilisée comme l'une des 4
méthodes votantes de Gate 2 du protocole CPV.

## C

### Cluster C+B+D+I+S

Signature empirique stable identifiée par les 14 diagnostics non-
cycliques Tier 1+2 sur les 6 panels CPV. Cinq familles co-apparentes
sur ≥ 60 % des cellules : long memory (C), multifractalité (B),
non-linéarité (D), information structurée (I), reflexive regime
drift (S). Voir [verdict constructif](tracks/acad/verdict_constructive.md).

### Consensus multi-méthode (Gate 2)

Quatre méthodes de décomposition aux hypothèses génératives
différentes (PELT, Markov-switching, Christiano-Fitzgerald + Hilbert,
Bry-Boschan) votent sur la phase courante du cycle. Au moins 3 sur 4
doivent s'accorder pour publier la phase. Voir
[méthode](methodology/trois_portes.md).

### Coverage 95 %

Indicateur binaire (0 ou 1) : la réalisation est-elle dans
l'intervalle de prédiction central 95 % ? Calculé à partir des
quantiles empiriques des Monte Carlo samples. Voir
[scoring](tracks/quants/code_api.md).

### CRPS (Continuous Ranked Probability Score)

Règle de scoring strictement propre de Gneiting-Raftery 2007.
Identité : `CRPS = E|X - y| - 0.5 * E|X - X'|`. Implémentée en O(N log N)
via formule rank-based. Lower = better. C'est la métrique principale
du benchmark Roadmap #20.

### Cycle Position Vector (CPV)

Le pipeline de recherche reproductible qui :
1. Teste les 4 cycles canoniques via 3 portes falsifiables (Gate 1
   dual null + Gate 2 consensus + Gate 3 universalité).
2. Identifie le cluster diagnostique C+B+D+I+S via 14 tests Tier 1+2.
3. Bat random walk via les modèles HAR/ARFIMA+RS/MSM sur 78 % des
   variables.

Voir [méthode complète](methodology/protocole_cpv.md).

## D

### `d` (paramètre de différenciation fractionnaire)

Paramètre de l'opérateur `(1-L)^d`. Pour `d ∈ (-0.5, 0.5)` le processus
est stationnaire mais à longue mémoire. Estimé par GPH ou local-Whittle.
Indicateur principal de la famille C du cluster. Voir
[credibility radar](tracks/bc/credibility_radar.md).

### DSGE (Dynamic Stochastic General Equilibrium)

Cadre dominant en macroéconomie BC depuis Smets-Wouters 2003. Repose
sur 3 hypothèses (chocs AR(1)/IID, paramètres deep stables,
distributions gaussiennes) que le cluster CPV réfute. Voir
[DSGE en accusation](tracks/acad/dsge_in_dock.md).

### DX diagnostics

Module `ecowave/cycles/alternative_dynamics.py` qui implémente les 14
diagnostics non-cycliques Tier 1+2 (11 familles théoriques). Output
JSON sidecars `reports/dx_diagnostics_*.json`. Voir
[dx_diagnostics.md](dx_diagnostics.md).

### Dual null

Le test Gate 1 du protocole CPV : la cellule passe ssi *les deux*
nulls (AR(1) bootstrap + phase scrambling) rejettent l'hypothèse
d'absence de cycle. Plus conservateur que chaque null individuel.
Voir [trois portes](methodology/trois_portes.md).

## E

### EWS (Early Warning System)

Système d'alerte précoce. Notre implémentation est un test KS sliding-
window qui détecte les changements de régime de la distribution avec
~3 mois d'avance moyenne sur les retournements 1979-2024. Voir
[tipping point detection](tracks/bc/tipping_point_detection.md).

## F

### Falsifiabilité

Critère poppérien : une hypothèse scientifique doit pouvoir être
réfutée par des observations spécifiques. Le projet CPV publie 5
prédictions falsifiables (§5.4 paper V1). Voir
[5 prédictions](tracks/acad/falsifiable_predictions.md).

### Forecast benchmark (Roadmap #20)

Le test out-of-sample qui compare 6 modèles (3 baselines + 3 cluster)
sur 68 variables × 6 panels × horizons (1, 3, 6, 12). Verdict
opérationnel PASS 78 %. Voir [verdict consolidé](forecast_benchmark.md).

### Free-energy principle (Friston)

Principe de Friston (2010) selon lequel tout système biologique ou
cognitif minimise la free-energy variationnelle entre son modèle
interne du monde et les observations. Cadre théorique candidat pour
formaliser S + I du cluster. Couvre 3/5 piliers. Voir
[synthèse AMH](tracks/acad/synthesis_amh.md).

## G

### Gate 1 / Gate 2 / Gate 3

Les trois portes falsifiables du protocole CPV :
- **Gate 1** : dual null (AR(1) + phase scramble)
- **Gate 2** : consensus 4 méthodes (3/4)
- **Gate 3** : universalité cross-aggregates (4/5)

Voir [méthode trois portes](methodology/trois_portes.md).

### GPH (Geweke-Porter-Hudak 1983)

Estimateur de `d` par régression log-periodogramme :
`log I(λ_j) = c - d log(4 sin²(λ_j/2)) + ε_j` pour les basses
fréquences. Bandwidth `m = T^{0.5}` ou `T^{0.8}`. Voir
[fractional.py](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/fractional.py).

## H

### HAR (Heterogeneous Autoregressive)

Modèle Corsi 2009 : régression OLS sur 3 moyennes glissantes
`(short, medium, long)`. Par défaut `(1, 3, 12)` mensuel ; `(1, 2, 4)`
trimestriel. Workhorse industriel. Domine le quarterly contemporain
dans notre benchmark. Voir
[catalogue](tracks/quants/models_catalog.md).

### Hosking recursion

Récursion `ψ_0 = 1, ψ_k = ψ_{k-1} · (k - 1 - d) / k` pour les
coefficients de l'expansion binomiale `(1 - L)^d`. Permet d'implémenter
fractional_difference et fractional_integrate sans inverser de
matrices. Voir Hosking 1981 *Biometrika*.

## I

### Information structurée (famille I)

Cluster CPV. Détectée par les entropies (permutation, sample,
approximate) qui restent significativement réduites par rapport aux
nulls AR(1) ou phase-scramble. Indique une *prédictibilité partielle*
exploitable par les bons modèles.

## J

### JST (Jordà-Schularick-Taylor)

Base de données macro-financière historique couvrant 18 économies
avancées 1870-2020 (crédit, prix immobiliers, équités, taux longs,
CPI, monnaie). Source principale du panel `long`. Voir
[sources](sources.md).

## K

### Kitchin / Juglar / Kuznets / Kondratieff

Les 4 cycles canoniques de la macroéconomie classique (3-5, 7-11,
15-25, 40-60 ans). Aucun ne survit aux 3 portes CPV sur les 6 panels
testés. Voir [Kitchin](cycles/kitchin.md) et pages connexes.

### Kolmogorov-Smirnov (KS)

Test non-paramétrique de l'égalité de deux distributions empiriques.
Utilisé en sliding-window pour la famille S (reflexive regime drift)
et pour le test EWS BC. Voir
[tipping point](tracks/bc/tipping_point_detection.md).

## L

### Lévy stable

Distribution à queues lourdes (paramètre `α ∈ (0, 2)`). Identifiée
empiriquement sur certaines variables financières et macro. Notre
test Hill estime `α` directement.

### Long memory (famille C)

Cluster CPV. Détectée par `d > 0` GPH ou local-Whittle. ACF lag-1
proche de 1. Décroissance polynomiale plutôt qu'exponentielle.
Quasi-universelle sur les séries macro (~85 % des cellules).

## M

### Markov regime-switching

Mécanisme où les paramètres d'un modèle changent selon un état
latent suivant une chaîne de Markov. Référence : Hamilton 1989. Notre
ARFIMA+RS utilise 2 régimes (mean + variance switching). Sims-Zha
2006 et Bianchi-Ilut 2017 étendent au DSGE.

### MF-DFA (Multifractal Detrended Fluctuation Analysis)

Méthode de Kantelhardt et al. 2002 pour mesurer la multifractalité.
Sortie principale : `Δα` = largeur du spectre singulier. `Δα > 0`
indique une multifractalité significative. Voir
[diagnostics](dx_diagnostics.md).

### MRW (Multifractal Random Walk)

Modèle de Bacry-Muzy-Delour 2001 : processus log-normal multifractal
avec corrélation logarithmique de la variance. Cadre canonique de la
multifractalité financière. Couvre 2/5 piliers du cluster CPV. Voir
[synthèse AMH](tracks/acad/synthesis_amh.md).

### MSM (Markov-Switching Multifractal)

Modèle Calvet-Fisher 2002. Cascade `σ_t = σ̄ · √(M_1 · ... · M_K)` avec
`K = 4` multiplicateurs Markoviens à 2 états. Reproduit B + C + queues
lourdes. 4 paramètres. Domine les panels longs dans notre benchmark
(43 % des wins cluster). Voir
[msm.py](https://github.com/s-geffroy/EcoWave/blob/main/ecowave/forecasting/msm.py).

### Multifractalité (famille B)

Cluster CPV. Auto-similarité où chaque échelle a sa propre dimension
fractale. Détectée par `Δα > 0` MF-DFA. Présente sur ~70 % des
cellules. Mandelbrot 1997 pour le cadre théorique financier.

## N

### Non-linéarité (famille D)

Cluster CPV. Détectée par le test BDS. Implique que cause et effet
ne sont pas proportionnels. Présente sur ~75 % des cellules.

## O

### Out-of-sample

Évaluation d'un modèle sur des données qu'il n'a pas vues pendant
l'estimation. Standard du benchmark Roadmap #20 via rolling-origin
sur les 25 % derniers points de chaque série.

## P

### PELT (Killick-Fearnhead-Eckley 2012)

Algorithme exact de détection de changepoints multiples optimal sous
pénalité linéaire. L'une des 4 méthodes votantes de Gate 2.

### Phase scrambling (Theiler 1992)

Méthode de simulation de surrogates : on randomise les phases de la
DFT en préservant le module (donc le spectre de puissance). Préserve
les propriétés linéaires de second ordre mais détruit la phase. L'un
des 2 nulls de Gate 1.

### `ProbabilisticForecast`

Dataclass pivot de `ecowave.forecasting.types`. Porte `samples` shape
`(n_samples, len(horizons))` sur le niveau + métadonnées. Tous les
modèles retournent un objet de ce type. Voir
[API publique](tracks/quants/code_api.md).

## Q

### `q` (panel)

Panel trimestriel contemporain 1995-2024 (USA, EA, JPN, GBR + agrégats
G7Q et OECDQ). Sources : FRED, Eurostat, OECD/IFS. Voir
[sources](sources.md).

## R

### Reflexivity (Soros)

Notion philosophique introduite par Soros : les croyances des
participants sur le système font partie du système. Formalisée
statistiquement par la famille S du cluster (KS sliding-window sur
moments d'ordre supérieur). Voir
[forward guidance réflexif](tracks/bc/forward_guidance_reflexive.md).

### Régime drift (famille S)

Cluster CPV. Détecté par KS sliding-window sur les statistiques
d'ordre supérieur. Présent sur ~60 % des cellules. Correspond aux
changements de régime cognitif identifiables historiquement (Volcker
1979, GFC 2008, COVID 2020).

### Roadmap #20

Le chantier de modélisation : benchmark forecast OOS pour valider le
cluster opérationnellement. Découpé en 4 PRs (#30 → #38) :
A baselines + HAR, B ARFIMA+RS, C MSM, D pipeline + CLI + verdict.
Résultat : PASS 78 %. Voir
[roadmap](methodology/feuille_de_route.md#item-20-modeling-benchmark).

### Roadmap #22

Le chantier de refonte hub multi-track : inverse la dramaturgie pour
mettre le constructif en frontline. 6 phases (1 fondations, 2 Public,
3 Quants, 4 BC, 5 Académique, 6 crossover + dashboard). Voir
[roadmap](methodology/feuille_de_route.md#item-22-hub-multitrack).

### Rolling-origin

Protocole d'évaluation OOS : on place plusieurs origines évenly-spaced
dans le hold-out, on fit le modèle à chaque origine, on score le
forecast contre la réalisation. Moyenne sur les origines. Standard du
benchmark Roadmap #20.

## S

### Sample-based representation

Représentation pivot de `ProbabilisticForecast` : matrice Monte Carlo
`(n_samples, n_horizons)` sur le niveau. Permet CRPS empirique +
coverage + tail coverage sans hypothèse paramétrique. Voir
[note Quants](tracks/quants/note_quants.md#linterface-commune).

### Sidecar JSON

Output JSON typé (`schema_version = 1`) des CLIs `forecast-benchmark`
et `forecast-benchmark-consolidate`. Contient config, verdict, cells,
failures. Sources de la page consolidée. Voir
[reproduction](tracks/quants/benchmark_reproducible.md#lecture-des-sidecars).

## T

### Tsallis non-extensivity

Famille de distributions q-Gaussiennes paramétrées par `q`. `q = 1` =
Gaussienne. `q > 1` = queues lourdes. Identifiée empiriquement sur
~45 % des cellules CPV. Composante des queues lourdes du cluster
(non-essentiel mais souvent présent).

## U

### Universalité (Gate 3)

Critère du triple-gate CPV : un cycle est qualifié `universal` ssi
≥ 4 / 5 agrégats de revenu (WLD, HIC, UMC, LMC, LIC) partagent la
même phase modale. Sinon `regional` ou `idiosyncratic`.

## V

### VaR (Value-at-Risk)

Quantile prédictif à un seuil de confiance (typiquement 99 %).
Utilisé par Bâle II. Critiqué pour non-cohérence sous-additive et
sous-estimation des queues sous distributions non-gaussiennes.

### Verdict consolidé

Page `docs/forecast_benchmark.md` générée par `ecowave
forecast-benchmark-consolidate` à partir des 6 sidecars par panel.
Affiche pass rate global, table par panel, leaderboard cluster,
lecture qualitative.

## W

### Working paper V1 vs V2

V1 : `docs/papers/cpv_main_paper.md`, ~10 000 mots, décembre 2025,
**dramaturgie réfutation-first** (les 4 cycles sont morts → cluster).
Archivé.

V2 : `docs/tracks/acad/paper_v2_academic.md`, ~4 500 mots,
**dramaturgie constructive** (benchmark PASS 78 % → cluster →
réfutation comme conséquence). Cible AER/JME/QJE.

## ψ (psi)

Coefficient d'expansion Hosking de `(1 - L)^d`. Notation utilisée dans
`fractional.py`. Voir [fractional API](tracks/quants/code_api.md).
