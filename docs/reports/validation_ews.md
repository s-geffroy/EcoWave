# Validation EWS — AUROC contre datation indépendante des crises

> **Résumé.** Le signal de stress mensuel produit par CPV (composante
> $I_{\text{intensity}}$) est testé hors-échantillon contre une datation
> indépendante des crises (NBER, CEPR/EABCN, Laeven-Valencia, ECB CISS).
> L'AUROC poolé moyen est de **$0.777$** sur 5 pilotes ; les deux pilotes
> pré-enregistrés en holdout (2020, 2022) atteignent $0.835$ et $0.921$
> respectivement. Hypothèse nulle : AUROC $= 0.5$ (signal sans valeur
> informationnelle).

## Notation

| Symbole | Sens |
|---|---|
| AUROC | Aire sous la courbe ROC du signal de stress |
| mean-stress | Moyenne des 5 percentiles de stress (E/D/S/L/I) |
| curve-count | Nombre de courbes simultanément en stress > 80 |
| holdout | Pilote pré-enregistré hors-échantillon |

## Résultats

**AUROC poolé (mean-stress, tous pilotes) : $0.777$.**

| Pilote | Holdout | AUROC mean-stress | AUROC curve-count | Mois en crise | Mois calmes |
|---|---|---:|---:|---:|---:|
| 2008 | non | $0.745$ | $0.720$ | 52 | 20 |
| 2016 | non | $0.970$ | $0.746$ | 15 | 57 |
| **2020** | **oui** | $0.835$ | $0.673$ | 11 | 49 |
| **2022** | **oui** | $0.921$ | $0.923$ | 11 | 37 |
| 2000 | non | $0.622$ | $0.527$ | 26 | 46 |

## Observations

- Les pilotes 2020 et 2022 sont des **holdouts pré-enregistrés**
  ([Feuille de route #4](../methodology/feuille_de_route.md)). Leur AUROC
  élevé indique que le signal n'est pas le produit d'un ajustement
  intra-échantillon.
- Le pilote 2000 (crise dot-com) est le plus faible : la dynamique du
  marché actions y prend le pas sur le stress macroéconomique mesuré
  par les indicateurs WB, et la curve-count en particulier descend à
  $0.527$ (proche du hasard).
- La méthode `mean-stress` domine `curve-count` sur 4 pilotes sur 5,
  cohérent avec une diffusion lente du stress à travers les courbes.

## Caveats

- **N petit** : 5 pilotes, $\leq 100$ mois chacun. Les intervalles de
  confiance sont larges ; les comparaisons par pilote sont indicatives.
- **Datation des crises** : NBER et CEPR utilisent des conventions
  différentes (l'un détecte les récessions, l'autre les pics
  d'inversion). La comparaison est sensible au choix de chronologie.

## Références

- [Laeven & Valencia (2018)](../bibliographie.md#laeven-valencia-2018) —
  banking crises chronology.
- [Reinhart & Rogoff (2009)](../bibliographie.md#reinhart-rogoff-2009) —
  cyclicité des crises.

---
*As-of : 2026-05. Schéma DB : 0.5.0. Pipeline : `evaluation.py:ews_metrics`
sur les pilotes pré-enregistrés.*
