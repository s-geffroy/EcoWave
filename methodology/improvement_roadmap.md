# EcoWave — Methodology improvement roadmap

This roadmap addresses the epistemological weaknesses of the original design:
EcoWave applied Elliott-wave grammar (widely judged non-falsifiable and
subjective) to macro crises while claiming to avoid pseudoscience, but the test
could not actually *fail*. The leverage points below are ordered by impact, not
effort. Levers #1–#3 are implemented; #4–#6 are scoped for later.

Each lever: the problem, the established method it borrows, the source, the
acceptance criterion, and its status.

---

## #1 — Null / surrogate test (falsifiability) · IMPLEMENTED

- **Problem.** Nothing distinguished "the Elliott grammar describes the crisis"
  from "any segmentation describes it". Without a benchmark the test cannot fail.
- **Method.** Surrogate-data testing: compare the champion's auto-computed
  evidence (C1 synchronisation + C3 robustness) against (a) random segmentations
  of the same phase count, and (b) the same windows on per-variable
  circularly-shifted stress (preserves each series' marginal/autocorrelation,
  destroys cross-curve alignment). Report a percentile and add-one-smoothed
  p-value; red-flag the champion when p ≥ 0.05.
- **Source.** Surrogate data testing (Theiler et al. 1992;
  https://en.wikipedia.org/wiki/Surrogate_data_testing).
- **Code.** `ecowave/scoring/null_test.py`; wired into `pipeline.py`; rendered in
  `model_comparison_<pilot>.md`. Only the auto-computed criteria are surrogated —
  C2/C4/C5/C6 (analyst) cannot be and are excluded by design.
- **Acceptance.** Pilot reports show the champion's phase-separation (mean η²) vs
  both nulls. *After redefining C1/C3 (#6), the gate discriminates: the Elliott
  champion beats both nulls for 2016 (p=0.03/0.02) and 2020 (p=0.002/0.046), but is
  red-flagged for 2008 (random p=0.40), 2022 (shift p=0.26) and 2000 (shift p=0.50).*
  The early version, using raw high-stress counts, gave p=1.0 everywhere — any
  segmentation of a crisis window passed; that failure motivated #6.

## #2 — Non-Elliott benchmark (Model D) · IMPLEMENTED

- **Problem.** A/B/C are three Elliott variants. Nothing tested whether Elliott
  beats an automatic regime detector.
- **Method.** Multivariate change-point detection (PELT, L2 cost) on the
  curve-level stress matrix, turned into `candidate_phases` and scored by the
  same pipeline. Documented alternative (not enabled): Markov-switching on an
  aggregate stress index (statsmodels `MarkovRegression`).
- **Source.** Killick et al. 2012 (PELT); ruptures library
  (https://centre-borelli.github.io/ruptures-docs/); asynchronous multivariate
  change-points (arXiv:2506.15801).
- **Code.** `ecowave/waves/model_d_regime.py`; injected as model "D" in
  `pipeline.py`; D carries the computed criteria only and is shown as a
  benchmark (not part of the A/B/C weighted verdict).
- **Acceptance.** Reports list A/B/C/D. *Observed (2008): D ties champion B on
  C1/C3 (3/2) — Elliott adds no measurable structure over PELT.*

## #3 — More crises + out-of-sample EWS validation · IMPLEMENTED

- **Problem.** N=2 pilots cannot support a transferability claim; all scoring was
  in-sample.
- **Method.** New pilots (2020 COVID, 2022 energy/inflation, 2000 dot-com)
  reusing the manifest with per-pilot reference-window overrides. Two pilots are
  **pre-registered holdouts** (`holdout=True`, `registered_at`). Objective
  validation: AUROC of monthly mean stress vs independent crisis dating, pooled
  and per pilot.
- **Source.** ECB cyclical systemic-risk EWS
  (https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart201805_2.en.html);
  Laeven & Valencia banking-crisis database; NBER / CEPR-EABCN dating;
  backtest-overfitting (Bailey/López de Prado, SSRN 2326253); pre-registration
  for predictive modelling (arXiv:2311.18807).
- **Code.** `ecowave/pilots.py` (fields `precrisis/structural/crisis_months/
  registered_at/holdout`); `ecowave/evaluation.py`; CLI `evaluate-ews`.
- **Acceptance.** *Observed: pooled AUROC = 0.78 (>0.5); holdouts 2020 = 0.84,
  2022 = 0.92 — the stress **measurement** is valid out-of-sample even though
  the Elliott **segmentation** is not (#1).*

---

## #4 — Missing variables (coverage) · TODO

- S2 (anti-austerity protests): Mass Mobilization Project / ACLED (post-2020 only
  — needs manual curation for older crises). I2 (media tone): GDELT tone, aligned
  with Shiller's narrative economics
  (https://blog.gdeltproject.org/macroeconomic-forecasting-through-news-emotions-and-narrative/).
- Symmetric US/EA coverage for the S and D curves.

## #5 — Markov-switching alternative for Model D · TODO

- Add statsmodels `MarkovRegression` on an aggregate stress index as a second
  non-Elliott benchmark, to confirm #2 is not PELT-specific.

## #6 — Null-calibrated C1/C3 · IMPLEMENTED (partial)

- **Problem.** The original C1/C3 counted high-stress months, so in a
  crisis-dominated window any segmentation passed and the null gate red-flagged
  every pilot (#1).
- **Method.** Redefined C1/C3 as **phase-separation calibrated against the null**
  (`ecowave/scoring/segmentation.py`): per-curve eta-squared of stress across the
  model's phases, scored only when it beats the (1-α) percentile of random
  segmentations of the same shape. Calibration is per phase-count, so extra phases
  do not inflate the score. C1 = #curves confirming (pre-crisis); C3 = share
  confirming on both windows.
- **Code.** `ecowave/scoring/segmentation.py`; `_computed_criteria` in
  `model_scores.py`; `null_test.py` now tests the same η² statistic.
- **Acceptance.** *Observed (2008): D (PELT) C1=3/C3=2 beats the null; Elliott
  A/B/C now score C1≤1 and are **rejected** — the redefined C1 enforces the
  project's own "waves in only one curve" rule, which the old C1 could not. The
  gate is no longer saturated (see #1 for the per-pilot p-values).*

- **Verdict thresholds recalibrated** for the new scale: `strong` now requires
  `T ≥ 2.2` **and** C1 ≥ 2 **and** C3 ≥ 2 (the falsifiable evidence must be solid,
  not just the narrative); `usable` ≥ 1.5; else `fragile` (see `scoring_rules.md`).

### Still TODO
- Sensitivity analysis on the weights (0.25/0.20/…); bootstrap confidence intervals
  on the weighted verdict; inter-annotator agreement (≥2 analysts, Cohen's κ) for
  C2/C4/C5/C6.
