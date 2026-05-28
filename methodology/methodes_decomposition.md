# Méthodes de décomposition cyclique — survey

> **Résumé.** Ce document recense les sept méthodes falsifiables envisagées
> pour le cadre CPV, les quatre qui sont devenues des composantes votantes
> actives (D, E, F, G) et les trois conservées pour contexte. Une matrice
> de décision croise falsifiabilité, horizon, compatibilité surrogate et
> adéquation aux données Banque mondiale annuelles.

## Notation

| Symbole | Sens |
|---|---|
| $D, E, F, G, H$ | Codes de méthode (voir lignes du tableau) |
| $B$ | Nombre de tirages surrogate ($B = 1\,000$ par défaut) |
| $\eta^2$ | Statistique de variance expliquée par la décomposition |
| LR | *Likelihood ratio* |

## Matrice de décision

| # | Méthode | Falsifiabilité | Horizon | Compat. surrogate | Adéquation données WB | Statut |
|---|---|---|---|---|---|---|
| 1 | CF band-pass + Morlet + Hilbert | Bootstrap AR(1) | Tous cycles | Oui (Torrence-Compo) | Oui | **Active (modèle F)** |
| 2 | Bry-Boschan / Harding-Pagan | Déterministe | Business cycle | Oui | Oui | **Active (modèle G)** |
| 3 | Markov-switching ([Hamilton, 1989](../bibliographie.md#hamilton-1989)) | Test LR, BIC | Multi-régime | Oui (simulation) | Oui | **Active (modèle E)** |
| 4 | Ruptures PELT ([Killick *et al.*, 2012](../bibliographie.md#killick-fearnhead-eckley-2012)) | Pénalité BIC + null $\eta^2$ | Multi-régime | Oui | Oui | **Active (modèle D)** |
| 5 | Cycle financier Borio-Drehmann | Comparaison Laeven-Valencia | ~15–20 ans | Indirect | Partielle | Conditionnel (modèle H) |
| 6 | UCM état-espace / [Hamilton (2018)](../bibliographie.md#hamilton-2018) | LR | Trend + cycle | Oui | Oui | Survey seulement |
| 7 | Cohérence en ondelettes (réseaux) | Cône + bootstrap | Tous, multivar | Oui | Oui | Inclus dans figure modèle F |
| — | EMD / Hilbert-Huang | Mode-mixing | Tous | Faible | Oui | **Rejetée** |
| — | Goldstein / Modelski long cycles | Narratif | Kondratieff | Non | Limitée | **Rejetée** |
| — | Mensch / vagues civilisationnelles | Aucune | Centennal | Non | Aucune | **Rejetée** |

## Pourquoi quatre méthodes plutôt qu'une

CPV refuse de parier sur une décomposition unique. La pile à trois portes
implique qu'une phase est publiée uniquement quand :

1. **Porte 1 — existence** : la puissance de la bande bat le bruit AR(1) +
   scramble de phase (la méthode F seule statue ici).
2. **Porte 2 — consensus inter-méthode** : $\geq 3$ sur 4 de
   $\{F, G, E, D\}$ s'accordent. Les quatre méthodes incarnent quatre
   hypothèses génératives très différentes ; un accord à 3/4 indique
   qu'aucun artéfact spécifique à une méthode ne pilote le résultat.
3. **Porte 3 — universalité cross-groupes** : $\geq 4$ sur 5 agrégats de
   revenu concordent. Transposition de la transférabilité C6 sur la
   dimension de stratification de revenu plutôt que temporelle.

La méthode 7 (cohérence en ondelettes) est calculée mais ne vote pas — elle
apparaît dans la figure « puissance wavelet » qui permet au lecteur
d'inspecter indépendamment l'évidence spectrale derrière le verdict de la
méthode F.

## Pourquoi rejeter EMD / Goldstein / Mensch

- **EMD (Empirical Mode Decomposition) / HHT.** Souffre d'un *mode-mixing*
  documenté (Wu & Huang, 2009) : une même IMF peut contenir plusieurs
  fréquences, ou inversement, ce qui rend la décomposition non-unique et
  difficilement falsifiable.
- **Goldstein / Modelski.** Théorie narrative géopolitique des cycles
  longs ; pas de procédure quantitative reproductible publiée sur les
  agrégats macroéconomiques (cf. [Goldstein (1988)](../bibliographie.md#goldstein-1988) ;
  [Modelski (1987)](../bibliographie.md#modelski-1987)).
- **Mensch.** Repose sur des regroupements d'innovations historiques sans
  protocole de test statistique ; non-falsifiable par construction.

## Références par méthode

- **CF band-pass** — [Christiano & Fitzgerald (2003)](../bibliographie.md#christiano-fitzgerald-2003).
- **Ondelettes (Morlet)** — [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998) ;
  [Aguiar-Conraria & Soares (2014)](../bibliographie.md#aguiar-conraria-soares-2014).
- **Bry-Boschan / Harding-Pagan** — [Bry & Boschan (1971)](../bibliographie.md#bry-boschan-1971) ;
  [Harding & Pagan (2002)](../bibliographie.md#harding-pagan-2002).
- **Markov-switching** — [Hamilton (1989)](../bibliographie.md#hamilton-1989).
- **PELT** — [Killick, Fearnhead & Eckley (2012)](../bibliographie.md#killick-fearnhead-eckley-2012).
- **Borio / Drehmann** — [Borio & Drehmann (2009)](../bibliographie.md#borio-drehmann-2009).
- **Cohérence en ondelettes** — [Grinsted *et al.* (2004)](../bibliographie.md#grinsted-moore-jevrejeva-2004).
- **Goldstein (rejeté comme méthode primaire)** — [Goldstein (1988)](../bibliographie.md#goldstein-1988).
- **Modelski (rejeté comme méthode primaire)** — [Modelski (1987)](../bibliographie.md#modelski-1987).
