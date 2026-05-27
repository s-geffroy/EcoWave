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

- **C1** and **C3** are auto-computed from the real panel and **calibrated against a
  surrogate null** (`ecowave/scoring/segmentation.py`). For each curve we measure the
  phase-separation of stress (eta-squared: share of variance explained by the model's
  phases) and compare it to the (1-α) percentile of random segmentations of the same
  shape (α=0.05). A curve "confirms" only when it beats that null — so a random
  segmentation of a crisis window scores ~0 and a model cannot win by adding phases.
  - **C1** (synchronisation) = number of curves that confirm on the pre-crisis window
    (capped at 3). This finally enforces the rejection rule "waves visible in only one
    curve" (C1 ≤ 1).
  - **C3** (robustness) = share of data-carrying curves that confirm on **both**
    reference windows (≥0.5→3, ≥0.3→2, >0→1, else 0).
- **C2, C4, C5, C6** are qualitative: filled by an analyst in
  `annotations/model_scores_qualitative.csv`, **with a mandatory justification**.
  No score is accepted without evidence; a model stays `blocked` until all six are set.

## Verdict thresholds

Weighted total `T = Σ raw_score × weight` (range 0–3), computed only when all six
criteria are filled:

Thresholds are recalibrated for the null-calibrated C1/C3 scale (which is now hard to
score high): `strong` additionally requires the falsifiable computed evidence to be
solid, not just a strong narrative.

| Condition | Verdict |
|---|---|
| any criterion empty | `blocked` |
| C1 ≤ 1, or C3 = 0, or C5 = 0 (auto-rejection) | `rejected` |
| T ≥ 2.2 **and** C1 ≥ 2 **and** C3 ≥ 2 | `strong` |
| T ≥ 1.5 | `usable` |
| otherwise | `fragile` |

The `strong` floor (C1 ≥ 2, C3 ≥ 2) means a model cannot be `strong` on narrative alone:
its phase structure must beat the surrogate null on at least two curves and hold across
both reference windows.

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

## Non-Elliott benchmark (Model D)

A fourth model **D** is added automatically: its phases come from multivariate
change-point detection (PELT) on the curve-level stress matrix, not from an
analyst. D is scored on the auto-computed criteria (C1/C3) by the same pipeline,
but it does **not** receive the weighted verdict or take part in the
champion/challenger adjudication — it is a yardstick. If D matches or beats the
Elliott champion on C1/C3, Elliott adds no measurable structure over an automatic
detector. See `methodology/improvement_roadmap.md` (#2).

## Null / surrogate test (falsifiability gate)

After scoring, the champion's auto-computed evidence (C1+C3) is compared against
two nulls: random segmentations of the same phase count, and per-variable
circularly-shifted stress. The report shows a percentile and p-value per null and
raises a **red flag** when p ≥ 0.05 (champion not distinguishable from chance).
Only auto-computed criteria are surrogated; C2/C4/C5/C6 (analyst) are excluded.
See `methodology/improvement_roadmap.md` (#1).
