# Fenêtres de référence

> **Résumé.** Le pipeline calcule chaque indicateur sur deux fenêtres de
> référence distinctes — l'une *pré-crise* (1990-2006), l'autre
> *structurelle* (1990-2019, hors Covid / Ukraine). Cette redondance teste
> la sensibilité du verdict cyclique à la fenêtre retenue.

## Notation

| Fenêtre | Bornes | Exclusions | Code |
|---|---|---|---|
| Pré-crise | 1990-01-01 – 2006-12-31 | aucune | `pre_crisis` |
| Structurelle | 1990-01-01 – 2019-12-31 | Covid (2020-2021), Ukraine (2022+) | `structural` |

## Fenêtre pré-crise (`pre_crisis`)

- **Bornes** : 1990 – 2006.
- **Objectif** : empêcher la crise 2007-2012 de se normaliser elle-même.
  Sans cette précaution, le z-score d'un indicateur calculé sur la
  fenêtre complète moyenne le pic de crise dans la baseline, ce qui
  *minore* l'écart-type apparent du choc.

## Fenêtre structurelle (`structural`)

- **Bornes** : 1990 – 2019.
- **Exclusions** : Covid (2020-2021) et choc Ukraine (2022+).
- **Objectif** : tester la robustesse contre une fenêtre historique plus
  longue, sans laisser deux chocs idiosyncratiques majeurs (Covid et
  Ukraine) contaminer la baseline.

## Cellules à fenêtre dégradée

Pour les indicateurs WB démarrant après 1990 (typique sur LIC, certains
indicateurs JST avant 1900) :

- Si la fenêtre pré-crise contient < 10 années : le z-score est calculé sur
  la plus longue fenêtre pré-2007 disponible et marqué
  `reference_window_caveat = "short_pre_crisis"`.
- Si la fenêtre structurelle contient < 15 années : idem,
  `reference_window_caveat = "short_structural"`.

## Caveats

- **Stationnarité** : les deux fenêtres supposent que la variable est
  approximativement stationnaire ou que sa dérive est négligeable
  devant l'amplitude cyclique. Pour les variables croissant fortement
  (PIB nominal, certaines variables JST en log-niveau), le z-score est
  remplacé par une différence cyclique CF avant comparaison.
- **Reproductibilité** : changer les bornes ouvre la suspicion
  d'ajustement *post hoc*. Toute modification doit passer par un commit
  séparé documenté dans [Feuille de route](feuille_de_route.md).

## Références

- [Laeven & Valencia (2018)](../bibliographie.md#laeven-valencia-2018) —
  banking crises chronology.
- [Reinhart & Rogoff (2009)](../bibliographie.md#reinhart-rogoff-2009) —
  cyclicité des crises de dette.
