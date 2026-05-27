# Scoring rules

## Model comparison criteria

| Code | Criterion | Weight |
|---|---|---:|
| C1 | Synchronisation multi-courbes | 0.25 |
| C2 | Clarté des ruptures | 0.20 |
| C3 | Robustesse des fenêtres | 0.20 |
| C4 | Parcimonie | 0.10 |
| C5 | Valeur ajoutée vs chronologie | 0.15 |
| C6 | Transférabilité vers 2011-2016 | 0.10 |

Raw criterion scores:

- 0 = non confirmé
- 1 = faible / narratif
- 2 = plausible
- 3 = robuste

## Computed vs annotated criteria

- **C1** and **C3** are auto-computed from the real panel (synchronisation count and
  dual-window robustness share).
- **C2, C4, C5, C6** are qualitative: filled by an analyst in
  `annotations/model_scores_qualitative.csv`, **with a mandatory justification**.
  No score is accepted without evidence; a model stays `blocked` until all six are set.

## Verdict thresholds

Weighted total `T = Σ raw_score × weight` (range 0–3), computed only when all six
criteria are filled:

| Condition | Verdict |
|---|---|
| any criterion empty | `blocked` |
| C1 ≤ 1, or C3 = 0, or C5 = 0 (auto-rejection) | `rejected` |
| T ≥ 2.4 | `strong` |
| T ≥ 1.8 | `usable` |
| otherwise | `fragile` |

## Automatic rejection

A model is rejected if:

1. its waves are visible in only one curve (mapped to **C1 ≤ 1**);
2. it depends on only one reference window (mapped to **C3 = 0**);
3. it requires too many narrative exceptions (analyst lowers **C2/C4**);
4. it fails to distinguish 2007-2009 from 2010-2012 when claiming two cycles (analyst, B);
5. it adds no explanatory value beyond chronology (mapped to **C5 = 0**).

## Champion / challenger

Model **B** is the provisional champion. A challenger (A or C) dethrones B if either:

1. it beats B on **≥ 4 of 6** criteria; **or**
2. it beats B on **≥ 3 of 6** criteria **and** its weighted score exceeds B's by at
   least **0.30** (relaxed rule for a clearly diverging weighted score).

Adjudicated only once all models are fully scored. The dethroner with the highest
weighted score becomes the provisional champion.
