# Analyst annotations — qualitative criteria (C2, C4, C5, C6)

EcoWave auto-computes only **C1** (multi-curve synchronisation) and **C3**
(reference-window robustness) from the data. The four qualitative criteria require
**analyst judgement** and are scored here, by hand, with a mandatory justification.

This is the anti-pseudoscience gate: **no score is accepted without a written
justification**, and a model stays `blocked` until all six criteria are filled.

## How to fill `model_scores_qualitative.csv`

One row per `(model, criterion)`. Edit only `raw_score`, `justification`,
`analyst`, `date`:

| Column | Rule |
|---|---|
| `raw_score` | integer **0–3** (see rubric). Leave **empty** to keep the criterion `blocked`. |
| `justification` | **required** if `raw_score` is set. One or two sentences of evidence. |
| `analyst` | your name/initials |
| `date` | ISO date, e.g. `2026-05-27` |

A row with a score but no justification is **rejected** (the run fails loudly).

## Raw-score rubric

- **0** — non confirmé (unconfirmed / contradicted)
- **1** — faible / narratif (weak, narrative only)
- **2** — plausible
- **3** — robuste

## Criterion definitions

- **C2 — clarté des ruptures**: how distinct/datable are the model's turning points?
- **C4 — parcimonie**: does the model explain with the fewest waves/exceptions?
- **C5 — valeur ajoutée vs chronologie**: does it explain more than a plain timeline?
- **C6 — transférabilité vers 2011-2016**: would the same grammar apply to the next crisis?

## Verdict (computed once all six criteria are set)

Weighted total `T = Σ raw_score × weight` (range 0–3). Then:

| Condition | Verdict |
|---|---|
| any criterion empty | `blocked` |
| C1 ≤ 1, or C3 = 0, or C5 = 0 | `rejected` (auto-rejection rules) |
| T ≥ 2.4 | `strong` |
| T ≥ 1.8 | `usable` |
| otherwise | `fragile` |

Champion **B** is dethroned only if a challenger (A or C) beats it on **≥ 4 of 6**
criteria. See `scoring_rules.md`.

## Apply

```bash
docker compose run --rm --entrypoint ecowave ecowave run-pilot 2008 --mode strict
```

The pipeline auto-loads this file (if present) and writes the completed verdicts to
`model_comparisons` in SQLite, `data_processed/model_verdicts.csv`, and the reports.
