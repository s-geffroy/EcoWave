# Règles de normalisation

> **Résumé.** Chaque variable ingérée par le pipeline est conservée
> simultanément sous cinq formes : valeur brute, deux z-scores (pré-crise
> et structurel) et deux percentiles de stress 0–100. Cette redondance
> permet d'auditer le verdict cyclique et de tester sa robustesse selon la
> fenêtre de référence retenue.

## Cinq vues par variable

Chaque variable doit préserver :

| Vue | Définition |
|---|---|
| **Valeur brute** | Donnée originale, unité d'origine |
| **Z-score pré-crise** | $z = (x - \mu_{\text{pré}}) / \sigma_{\text{pré}}$ ; fenêtre 1990-2006 |
| **Percentile stress pré-crise** | Centile dans la distribution pré-crise, $\in [0, 100]$ |
| **Z-score structurel** | Fenêtre 1990-2019 (exclut Covid / Ukraine) |
| **Percentile stress structurel** | Centile dans la distribution structurelle |

## Fenêtres de référence

- **Score principal** : 1990-2006 lorsque disponible, sinon la plus longue
  fenêtre pré-2007 accessible. Empêche la crise 2007-2012 de se
  normaliser elle-même.
- **Score de robustesse** : 1990-2019 lorsque disponible, en excluant
  Covid et Ukraine. Teste la robustesse contre une fenêtre historique plus
  longue.

Détail des fenêtres : [Fenêtres de référence](fenetres_reference.md).

## Synthèse cross-courbes

La normalisation par variable est l'entrée ; la moyenne par courbe
(`scoring/curve_scores.py`) produit un stress par courbe. L'indicateur
synthétique global (intensité + diffusion, trois pondérations — `equal`,
`pca`, `favar`) est documenté dans [Indicateur composite](indicateur_composite.md)
et constitue ce sur quoi les méthodes D/E/F/G opèrent au niveau composite.

## Caveats

- **Asymétrie distributions** : les percentiles supposent une distribution
  unimodale ; pour les indicateurs très asymétriques (spreads de défaut,
  volatilités) la transformation reste valable comme rang mais perd
  l'interprétation distance-à-la-moyenne.
- **Fenêtres courtes (LIC)** : pour les indicateurs WB démarrant après
  1990 (typique sur LIC), la fenêtre pré-crise tombe en-dessous de 10 ans
  ; le z-score devient instable et est marqué `endpoint_caveat = 1`.

## Références

- Reinhart & Rogoff (2009) — *This Time is Different*.
- Laeven & Valencia (2018) — *Systemic banking crises revisited*.
