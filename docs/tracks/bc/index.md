# Track banque centrale

> *Pour praticiens de la politique monétaire, économistes BC, analystes
> macroprudentiels.* Si vous calibrez un modèle DSGE pour votre comité
> de politique monétaire, projetez des forecasts d'inflation à 8 trimestres,
> ou supervisez des stress tests bancaires, **cette page est écrite pour
> vous**.

## La proposition opérationnelle

1. **La crédibilité monétaire est mesurable** par le paramètre de longue
   mémoire `d` GPH appliqué à l'inflation. Pays avec `d > 0.5` sur
   l'inflation : crédibilité plus faible. Volcker 1979–82 a **cassé** la
   persistance — c'est l'opérationnalisation empirique d'un changement
   de régime cognitif (S). Une BC qui tracke `d` sur sa série
   d'inflation tracke en temps réel sa propre crédibilité.
2. **Le forward guidance est un acte réflexif**, pas un signal
   informatif neutre. Soros' reflexivity rejoint ici notre famille S :
   la communication d'une BC *change* le régime cognitif que les agents
   utilisent pour anticiper. Cela ne disqualifie pas le forward guidance,
   mais impose de le **modéliser comme tel**.
3. **Le ciblage de l'inflation doit être horizon-aware.** La longue
   mémoire dans l'inflation rend les forecasts AR(1) inadéquats au-delà
   de 3 trimestres. Notre benchmark Roadmap #20 montre que ARFIMA+RS
   bat random walk à h = 12 ans sur les variables long-mémoire ; HAR
   les bat à h = 1–3 trimestres. Une BC qui calibre son horizon
   monétaire (h = 6–8 trimestres typiquement) doit utiliser **les
   deux familles**, pas une seule.
4. **Les tipping points de régime sont détectables.** Le diagnostic S
   (Kolmogorov-Smirnov sliding-window sur les statistiques d'ordre
   supérieur) signale les changements de régime cognitif avec une
   avance moyenne empirique de 3-6 mois (sur historique 1960–2024).
   Application directe : système d'alerte précoce sur les retournements
   macro.
5. **Les booms de crédit ont des ombres très longues.** Le `d` GPH sur
   `LH_CREDIT` (Jordà-Schularick-Taylor 1870–2020) atteint 0.40 sur
   ADV18 — proche de la borne d'intégration fractionnaire. Le
   credit-to-GDP gap de Borio (BIS 2014) est un proxy utile mais incomplet ;
   un *Hurst-based credit cycle* extraperait directement la persistance
   et anticiperait mieux l'accumulation de risque systémique.

## Contenu (en cours de livraison)

| Page | Statut |
|---|---|
| Méthode CPV pour praticiens BC | *à venir* |
| Credibility radar — `d`-GPH inflation par pays | *à venir* |
| Forward guidance comme acte réflexif | *à venir* |
| Tipping point detection (EWS régime drift) | *à venir* |
| Horizon-aware targeting (ARFIMA+RS vs HAR) | *à venir* |
| **Note BC (~5 000 mots, langue praticien)** | *en cours* |

## En attendant

- La **[page implications du verdict (multi-axe)](../../reference/implications_of_cluster.md)**
  contient les sections 1 (politique monétaire) et 2 (macroprudentiel)
  qui préfigurent la note BC.
- La **[méthode trois portes](../../methodology/trois_portes.md)**
  documente le triple-gate falsifiable.
- Le **[forecast benchmark consolidé](../../forecast_benchmark.md)**
  livre le verdict opérationnel PASS 78 % cross-panel.
- La **[bibliographie](../../bibliographie.md)** liste les références
  pertinentes (Borio 2014 financial cycle ; Drehmann-Borio-Tsatsaronis
  2012 credit gap ; Bhardwaj-Swanson 2006 ARFIMA macro forecasting ;
  Calvet-Fisher pour volatilité long-horizon).
