# Garde-fous anti-pseudoscience

> **Résumé.** Ces règles gouvernent le cadre *Cycle Position Vector* (CPV).
> Elles sont les garde-fous anti-pseudoscience du projet : toute phase
> cyclique publiée par EcoWave doit respecter **toutes** les contraintes
> ci-dessous. Les violations sont des bugs, pas des compromis acceptables.

## Notation

| Symbole | Sens |
|---|---|
| $\alpha$ | Seuil de rejet du null (Porte 1) ; figé à $0.05$ |
| $k$ | Nombre minimum d'accord pour la Porte 2 ; figé à $3$ |
| $q$ | Nombre minimum d'accord pour la Porte 3 ; figé à $4$ |

## Interdictions

- **Publier une phase qui ne bat pas le null surrogate AR(1) + scramble de
  phase.** Un cycle « visible » dans du bruit rouge n'est pas un cycle.
  Voir [Trois portes](trois_portes.md).
- **Publier la phase d'une méthode unique alors que les autres divergent.**
  Le consensus à $\geq 3$ méthodes sur 4 est obligatoire ; en-dessous,
  publier `disputed`.
- **Cacher des données manquantes ou les imputer silencieusement.** Les
  cellules sans data sont marquées explicitement.
- **Choisir bandes, paramètres surrogate ou seuils de méthode *après* avoir
  vu le résultat.** Tous les paramètres sont figés dans le code :
  `ecowave/cycles/bands.py`, `ecowave/cycles/surrogate.py`,
  `ecowave/waves/model_f_cycles.py`, `ecowave/waves/model_g_bryboschan.py`.
- **Présenter des sorties exploratoires comme finales.** Les runs `--mode
  draft` ne génèrent pas de note signée.
- **Réinterpréter un `rejected` en cycle latent.** Si la Porte 1 rejette,
  c'est un échec honnête ; pas un signal caché.

## Obligations

- **Méthodes concurrentes** (D PELT, E Markov-switching, F CF+Hilbert,
  G Bry-Boschan), appliquées identiquement à chaque agrégat et chaque bande.
- **Raisons de rejet explicites** : `rejected`, `disputed`, `regional`,
  `endpoint_caveat`. Aucun rejet silencieux.
- **Grades de confiance** sur chaque indicateur ingéré (A–D), figés dans
  `cycles_manifest.json`.
- **Manifest de sources unique source de vérité** (`cycles_manifest.json`,
  `sources_manifest.json`).
- **Valeurs brutes conservées** à côté des transformations (CSV brut sous
  `data_raw/`).
- **Test de surrogate sur chaque phase publiée** (Porte 1, voir
  [Trois portes](trois_portes.md)).
- **Au moins un pilote de crise pré-enregistré hors-échantillon** (2020 ou
  2022 ; champ `registered_at` sur la dataclass `Pilot`).

## Détection des violations

- Tout test `pytest` détectant un paramètre tuné après run échoue le CI.
- Toute modification de `CYCLE_BANDS`, des seuils $\alpha, k, q$ ou des
  fenêtres surrogate génère un PR review obligatoire (cf.
  [Feuille de route](feuille_de_route.md)).
- L'audit `--strict` de MkDocs casse le build si une référence
  bibliographique pointe vers une ancre inexistante dans
  [Bibliographie](../bibliographie.md).

## Caveats

Les garde-fous n'éliminent pas le risque épistémique, ils le rendent
auditable. Une discipline de pré-enregistrement (publier les bandes, les
méthodes et les fenêtres *avant* d'observer les résultats finaux) est
indispensable pour que ces règles aient une force réelle. L'historique git
de `methodology/` et `ecowave/cycles/` joue ce rôle.

## Références

- Bailey, D. H., & López de Prado, M. (2014). The deflated Sharpe ratio.
- Ioannidis, J. P. A. (2005). Why most published research findings are false.
  *PLoS Medicine*.
- [Theiler *et al.* (1992)](../bibliographie.md#theiler-et-al-1992).
