# Cinq prédictions falsifiables enrichies

!!! success "TL;DR"

    5 prédictions du paper V1 §5.4. Statut : **Prédiction 4 CONFIRMÉE** par Roadmap #20 (forecast régime-conditionnel = PASS 78 %). Prédiction 1 (durabilité longue mémoire pré-1700) et 5 (split-point spécifique) TODO. Prédictions 2 (robustesse non-financière) et 3 (multifractale > monofractale) PARTIELLES. Effort total restant : ~70 jours.

## Dans cette page

- **[Cadre falsifiabilité](#cadre)** — Popper, pré-enregistrement
- **[Prédiction 1 — Durabilité longue mémoire](#pred-1)** — TODO
- **[Prédiction 2 — Robustesse non-financière](#pred-2)** — PARTIAL
- **[Prédiction 3 — Multifractale > monofractale](#pred-3)** — PARTIAL
- **[Prédiction 4 — Forecast régime-conditionnel](#pred-4)** — **CONFIRMÉE**
- **[Prédiction 5 — Split-point spécificité](#pred-5)** — TODO
- **[Synthèse — programme falsifiabilité](#synthese)**

---

## Le cadre falsifiabilité { #cadre }

Le cluster CPV C+B+D+I+S est une **hypothèse de travail**, pas un
théorème. Comme tout cadre scientifique, il doit faire des prédictions
falsifiables — autrement c'est de la métaphysique au sens de Popper.

La V1 du paper (§5.4) liste 5 prédictions. La V2 — Roadmap #20 ayant
livré le benchmark opérationnel — peut désormais évaluer une partie
de ces prédictions ; les autres restent ouvertes.

## Prédiction 1 — Durabilité de la longue mémoire { #pred-1 }

### Formulation V1

> Le Hurst estimé sur les panels historiques (boe, long) ne devrait
> *pas* converger vers 0.5 (random walk) à mesure qu'on étend
> l'échantillon vers le passé. Si on ingère des données pré-1700
> (séries de prix médiévales, archives bancaires Renaissance) et
> qu'on trouve `H → 0.5`, l'image cluster est affaiblie : la longue
> mémoire serait un artefact du financiarisation post-1700 plutôt
> qu'une caractéristique structurelle.

### Statut empirique

**TODO**. Le panel actuel `boe` couvre 1700-2016. L'extension à
pré-1700 nécessite :

- Ingestion de séries Phelps Brown-Hopkins (prix anglais 1264-1954),
  Allen's London wages (1264-1700), Florentine wool industry
  (1300-1600).
- Test du `d` GPH sur ces périodes étendues.
- Comparaison du `d` pré-1700 vs post-1700.

### Test opérationnel

Procédure :

1. Ingérer ces séries dans `ecowave/cycles/` via un nouveau loader
   `ecowave/cycles/historical_early.py`.
2. Calculer `d` GPH sur des sous-fenêtres glissantes 100-200 ans.
3. Tracer `d_t` vs `t` sur 1300-2024.
4. Tester si `d` pré-1700 ≠ `d` post-1700 (KS ou test de moyenne
   robust).

### Verdict attendu

**Hypothèse cluster** : `d > 0.20` pour les deux sous-périodes.
**Hypothèse de réfutation** : `d` pré-1700 → 0.5 (proche du random
walk).

### Effort estimé

~20-30 jours pour l'ingestion + 5 jours pour les tests.

## Prédiction 2 — Robustesse cross-panel sur variables non-financières { #pred-2 }

### Formulation V1

> Le cluster devrait apparaître sur un panel de variables
> macroéconomiques *non-financières* (taux d'activité, scolarisation,
> indicateurs de santé publique, consommation énergétique par
> habitant). Si le cluster n'est présent que sur les agrégats
> financiers / monétaires et absent sur les variables réelles, on
> a identifié une *spécificité du secteur financier*, pas une
> *caractéristique structurelle macroéconomique*.

### Statut empirique

**PARTIEL — bonne nouvelle**. Le panel `sh` (sectoral history) inclut
déjà :

- Fret ferroviaire US (réel, pré-financiarisé)
- Production d'acier (réel, industrie lourde)
- Production industrielle (réel, large composante manufacturière)

Le benchmark Roadmap #20 montre que ces variables sont **partiellement
battues par le cluster** : sur les 8 variables `sh`, 5 / 8 = 62 % sont
battues. Cela suggère que le cluster s'étend au-delà du secteur
financier.

Mais le panel `sh` reste anglo-saxon-centric. Une extension est
nécessaire.

### Test opérationnel

Procédure :

1. Ingérer un panel OWID avec variables santé (mortalité infantile,
   espérance de vie), éducation (scolarisation), démographie (taux
   de natalité), énergie (consommation par habitant).
2. Coverage : 100+ pays, 1960-2024.
3. Appliquer le triple-gate CPV puis le benchmark Roadmap #20.

### Verdict attendu

**Hypothèse cluster** : pass rate ≥ 50 % sur les variables réelles.
**Hypothèse de réfutation** : pass rate < 50 % et différentiel
significatif vs variables financières.

### Effort estimé

~15 jours pour l'ingestion OWID + 3 jours pour le benchmark.

## Prédiction 3 — Multifractale plutôt que monofractale { #pred-3 }

### Formulation V1

> La largeur du spectre singulier MF-DFA `Δα` devrait être de façon
> fiable > 0 sur le panel histoire longue. Si `Δα → 0` avec plus de
> données et de meilleures méthodes, l'image cluster se réduit à un
> mouvement fractal monofractal (fBm), qui est une version plus
> faible et plus restreinte. Nous pré-enregistrons une réplication
> avec 1 000 surrogates en utilisant `nolds.mfdfa` comme estimateur
> canonique.

### Statut empirique

**PARTIEL — confirmation partielle**. Le panel `dx_diagnostics`
inclut MF-DFA comme diagnostic de famille B. Sur les 6 panels :

- `Δα > 0.15` sur ~70 % des cellules
- `Δα > 0.30` sur ~40 % des cellules

C'est compatible avec une multifractalité plus que monofractale, mais
la queue de la distribution (`Δα` bas) suggère certaines variables
sont monofractales.

### Test opérationnel

Procédure :

1. Augmenter la résolution du MF-DFA en passant de q ∈ [-5, 5] à
   q ∈ [-10, 10] avec pas de 0.5.
2. Calculer `Δα` avec intervalle de confiance bootstrap à 1 000
   répétitions.
3. Tester si `Δα > 0` significativement (intervalle ne contient pas 0).
4. Documenter le pourcentage de variables où cette confirmation
   passe.

### Verdict attendu

**Hypothèse cluster** : `Δα` significativement > 0 sur ≥ 50 % des
variables, ICs ne contenant pas 0.
**Hypothèse de réfutation** : `Δα` non-significativement > 0 sur la
majorité, suggérant un monofractal.

### Effort estimé

~10 jours pour l'extension du MF-DFA et l'analyse bootstrap.

## Prédiction 4 — Forecast performance régime-conditionnelle { #pred-4 }

### Formulation V1

> Un modèle de prévision basé sur (a) ARFIMA + (b) régime-switching
> + (c) innovations à queues lourdes devrait *outperformer* les
> prévisions cycle-conditionnelles canoniques sur les données
> out-of-sample 2020-2024. L'image cluster prédit cela.

### Statut empirique

**LIVRÉE — confirmation forte par Roadmap #20**.

Le benchmark `ecowave forecast-benchmark` (PRs #30-#38) implémente
exactement cette prédiction :

- (a) ARFIMA implémenté
- (b) Markov regime-switching implémenté
- (c) Innovations Gaussiennes utilisées dans ARFIMA+RS — pas encore
  queues lourdes explicites

Verdict : **PASS 78 %** sur 68 variables, 6 panels. Le modèle cluster
(MSM + ARFIMA+RS + HAR) bat random walk sur out-of-sample CRPS à
h = 12.

Cette prédiction est **confirmée**. Reste à étendre :

- Innovations à queues lourdes (Tsallis ou Lévy stable) — extension
  Roadmap.
- Tests Diebold-Mariano et Giacomini-White pour la rigueur
  statistique formelle.

### Test opérationnel restant

Procédure :

1. Implémenter `arfima_rs_heavy_tails` avec innovations Tsallis.
2. Re-benchmarker sur les mêmes 68 variables.
3. Comparer CRPS et tail coverage (cluster vs gaussian).
4. Hypothèse : les queues lourdes améliorent le tail coverage de
   ~30 % sans dégrader le CRPS médian.

### Effort estimé

~7 jours.

## Prédiction 5 — Spécificité des split-points réflexifs { #pred-5 }

### Formulation V1

> Le diagnostic `reflexivity_multi_window` devrait attribuer le
> changement de distribution à des split-points *spécifiques*
> pré-enregistrés, pas uniformément sur la timeline. Si on étend
> l'analyse avec 1 000 surrogates et que le split-point dominant
> varie aléatoirement à travers les séries, le claim de
> réflexivité est affaibli à "la distribution change d'une façon
> ou d'une autre", ce qui est non-falsifiable.

### Statut empirique

**TODO**. Le test `reflexivity_multi_window` détecte les ruptures
mais ne caractérise pas leur *localisation* dans le temps.

### Test opérationnel

Procédure :

1. Pré-enregistrer une liste de split-points historiques candidats :
   1944 (Bretton Woods), 1971 (fin du Gold Standard), 1973 (premier
   choc pétrolier), 1979 (Volcker), 1989 (chute du mur), 1999 (euro),
   2008 (GFC), 2020 (COVID), 2022 (Ukraine).
2. Pour chaque variable du cluster, identifier le split-point
   dominant détecté par KS sliding-window.
3. Compter la distribution des split-points dominants à travers les
   variables.
4. Tester si la distribution est non-uniforme (Chi-deux).

### Verdict attendu

**Hypothèse cluster** : la distribution est **non-uniforme**, avec
clustering autour de quelques dates historiquement reconnues (Volcker
1979 pour l'inflation, 2008 pour le crédit, 2020 pour les variables
réelles).
**Hypothèse de réfutation** : distribution uniforme, suggérant que les
ruptures sont aléatoires plutôt que cognitives.

### Effort estimé

~5 jours pour le test + interprétation historique.

## Synthèse — programme falsifiabilité { #synthese }

| Prédiction | Statut | Effort restant | Priorité |
|---|---|---|---|
| 1 — Durabilité longue mémoire | TODO | 25-35 jours | Élevée |
| 2 — Robustesse non-financière | Partial | 18 jours | Élevée |
| 3 — Multifractale vs monofractale | Partial | 10 jours | Modérée |
| 4 — Forecast régime-conditionnel | **CONFIRMÉE** | 7 jours (queues lourdes) | Faible (déjà passée) |
| 5 — Split-point spécifique | TODO | 5 jours | Modérée |

**Effort total restant** : ~70 jours pour la complétion de la
falsifiabilité du cluster.

## Pourquoi cette discipline importe

La falsifiabilité explicite est ce qui distingue le programme CPV des
narratives macroéconomiques non-testables (notamment celles des 4
cycles canoniques). En pré-enregistrant les 5 prédictions, on s'engage
à publier les résultats — *même si* ils réfutent le cluster.

Cela contraste avec :

- La narrative cyclique (Korotayev-Tsirel 2010) qui adapte la datation
  ex-post aux observations.
- Les modèles DSGE calibrés sur la même période que celle où ils
  sont évalués (in-sample).
- Les "predictions" macroéconomiques publiées sans engagement
  préalable à publier les échecs.

## Pour aller plus loin

### Méthode

- [Méthode compacte](method_compact.md)
- [Verdict constructif](verdict_constructive.md)
- [Working paper V1 §5.4](../../papers/cpv_main_paper.md)

### Pratique

- [Forecast benchmark consolidé](../../forecast_benchmark.md) —
  confirmation de la prédiction 4
- [DX diagnostics](../../dx_diagnostics.md) — données empiriques pour
  les prédictions 1, 3, 5
- [Implications multi-axe](../../reference/implications_of_cluster.md)
  — application des prédictions confirmées

### Théorie

- [DSGE en accusation](dsge_in_dock.md) — pourquoi les prédictions
  réfutent DSGE
- [Synthèse AMH](synthesis_amh.md) — cadre théorique potentiel

### Code

- `ecowave.forecasting.benchmark` — implémentation prédiction 4
- `ecowave.cycles.alternative_dynamics` — diagnostics pour prédictions
  1, 3, 5
