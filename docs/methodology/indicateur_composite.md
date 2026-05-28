# Indicateur synthétique composite

> **Résumé.** Pour chaque agrégat de pays et chaque bande cyclique, le
> pipeline construit un *composite par bande* : filtrage CF de chaque
> indicateur individuel dans la bande cible, puis z-score et moyenne. Cette
> composite est l'entrée des quatre méthodes votantes. Deux indices
> diagnostiques annexes (intensité, diffusion) restent publiés pour la
> validation EWS sur les pilotes de crise historiques.

## Notation

| Symbole | Sens |
|---|---|
| $x_i(t)$ | Indicateur $i$ pour l'agrégat considéré, fréquence annuelle (WB) |
| $\tilde x_i(t)$ | Composante CF de $x_i$ dans la bande $[\text{lo}, \text{hi}]$ |
| $z_i(t)$ | $\tilde x_i(t)$ z-normalisé sur son propre historique |
| $c(t)$ | Composite par bande, moyenne des $z_i$ |
| $I_{\text{intensity}}$ | Indice synthétique pilote-fenêtre |
| $I_{\text{diffusion}}$ | Nombre de courbes en stress (pilotes EWS) |

## Composite par bande (CPV long-horizon)

Pour chaque cycle de bornes $(\text{lo}, \text{hi})$, le composite par
bande $c_{\text{band}}(t)$ est calculé par :

1. Pour chaque indicateur $x_i$ du manifest, calculer
   $\tilde x_i(t) = \text{CF}_{\text{lo},\text{hi}}(x_i)$.
2. Standardiser : $z_i(t) = (\tilde x_i(t) - \bar{\tilde x_i}) / \sigma(\tilde x_i)$.
3. Moyenne : $c_{\text{band}}(t) = \frac{1}{|\mathcal{I}|} \sum_{i \in \mathcal{I}} z_i(t)$.

Cette construction concentre la puissance dans la bande cible : la SNR
mesurée par la Porte 1 a été substantiellement améliorée par cette étape
(voir [Feuille de route #6](feuille_de_route.md)). Implémentation :
`ecowave/cycles/runner.py:_composite_panel(panel, band=...)`.

## Indices pilote-fenêtre (validation EWS)

Le pipeline pilote historique (fenêtres 2007-2012, 2016, 2020, 2022, 2000)
agrège les cinq percentiles de stress par courbe (E/D/S/L/I) en deux
indices diagnostiques :

| Index | Définition | Rôle |
|---|---|---|
| **$I_{\text{intensity}}$** | Moyenne pondérée des 5 percentiles de stress, $\in [0, 100]$ | Série continue sur laquelle opèrent D / E / F / G en mode pilote |
| **$I_{\text{diffusion}}$** | $\#\{d : \text{stress}_d > 80\}$ sur les courbes disponibles | Coïncidence cross-courbes |

Un mois n'est `scored` que si au moins 3 courbes sur 5 sont disponibles
(`MIN_CURVES_SCORED = 3`) ; sinon la ligne est `blocked`.

### Variantes de pondération

Trois variantes sont calculées en parallèle :

- **`equal`** — uniforme à 0.20 par courbe. Toujours définie ; fallback par
  défaut.
- **`pca`** — première composante principale du panel glissant à 60 mois,
  loadings normalisés en valeur absolue. `None` si la covariance est
  dégénérée.
- **`favar`** — $R^2$ prédictif d'une régression d'ancrage (style FAVAR :
  indicateur composite avancé OECD ou production industrielle G4 pondérée
  par PIB comme ancre exogène). `None` si aucune courbe n'a de contenu
  prédictif.

Cascade de fallback : `favar → pca → equal`. Le chemin emprunté est tracé
dans la colonne `global_indices.weighting_actual`.

### Variantes de lissage

- **MA3** — moyenne mobile centrée 3 mois ; entrée par défaut de D/E/F/G.
- **HP cycle** — décomposition Hodrick-Prescott avec $\lambda = 129\,600$
  (convention mensuelle). Utilisée uniquement pour l'overlay graphique et
  la colonne `intensity_hp_cycle` ; *jamais* en entrée du verdict
  (Hamilton, 2018 démontre que HP induit des cycles spurieux).

## Caveats

- **Étape de standardisation après CF** : standardiser après filtrage CF
  (et non avant) signifie que les unités sont écrasées avant le passe-bande.
  Justification : les indicateurs de croissance, taux et niveaux ont des
  variances incomparables ; appliquer CF sur la variable brute préserve la
  saisonnalité cyclique avant écrasement.
- **Indicateurs absents** : si moins de 2 indicateurs ont des données dans
  la bande pour l'agrégat, le composite par bande retombe sur le composite
  cross-bande (z-score full-history → moyenne).

## Références

- [Christiano & Fitzgerald (2003)](../bibliographie.md#christiano-fitzgerald-2003)
- Hatzius, Hooper, Mishkin, Schoenholtz & Watson (2010). *FAVAR financial
  conditions index*. NBER Working Paper.
- Hamilton, J. D. (2018). *Why You Should Never Use the Hodrick-Prescott
  Filter*. *Review of Economics and Statistics*.
- Hodrick, R., & Prescott, E. C. (1997). Postwar U.S. business cycles : an
  empirical investigation.
