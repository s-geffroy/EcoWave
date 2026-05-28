# EcoWave — methodology roadmap

This roadmap tracks the design choices behind the current Cycle Position
Vector (CPV) framework. Only the items that are active in the current
pipeline are listed below.

---

## #1 — Surrogate null per published phase

- **Problem.** Without a null, a "cycle" found in any noisy series cannot be
  distinguished from coincidence.
- **Method.** AR(1) bootstrap (Torrence & Compo 1998; Grinsted et al. 2004):
  fit AR(1) on the input, simulate B = 1000 surrogate paths preserving mean,
  variance, and persistence; reject the cycle when the real band-power does
  not exceed the (1-α) percentile of surrogate band-power.
- **Code.** `ecowave/cycles/surrogate.py` (Gate 1 of CPV);
  `ecowave/scoring/null_test.py` (per-pilot η² null);
  `ecowave/waves/model_f_cycles.py` (model-level gate).
- **Acceptance.** Every cell of `cycle_positions` is published with a
  p-value; cells with `p ≥ 0.05` carry `phase = rejected`, `separable = 0`.

## #2 — Multi-method consensus

- **Problem.** Any single decomposition can be specific to its own
  parametric assumptions. A cycle that emerges only when one method is
  applied is not a robust cycle.
- **Method.** Four votant methods with very different generative assumptions
  vote on every phase:
  - D — PELT change-point detection (Killick et al. 2012)
  - E — Markov-switching AR(1) (Hamilton 1989)
  - F — Christiano-Fitzgerald Juglar band-pass + Hilbert phase
  - G — Bry-Boschan / Harding-Pagan turning-point dating
  Publish the modal phase only when ≥ 3 of 4 agree; otherwise `disputed`.
- **Code.** `ecowave/cycles/consensus.py` (Gate 2);
  `ecowave/scoring/null_test.py:all_models_null_report` (per-method panel).
- **Acceptance.** Per-method votes are stored in `cycle_consensus`; the
  CPV report lists every method's label for every published cell.

## #3 — Cross-group universality

- **Problem.** A cycle that is purely a high-income-country artefact is not
  a "global cycle".
- **Method.** A cycle is qualified `universal` for a given month only if
  ≥ 4 of 5 income groups (WLD + HIC + UMC + LMC + LIC) concur on the modal
  phase. Otherwise `regional / idiosyncratic`.
- **Code.** `ecowave/cycles/universality.py` (Gate 3); persisted in
  `cycle_universality`.
- **Acceptance.** Every cycle has a universality flag in the CPV report.

## #4 — Pre-registered out-of-sample holdouts

- **Problem.** In-sample tuning is the canonical source of macroeconomic
  false positives (Bailey & López de Prado 2014).
- **Method.** Pilots `2020` and `2022` are pre-registered holdouts (the
  `registered_at` and `holdout` fields on `Pilot`). They were frozen
  *before* the manifest's reference windows were finalised.
- **Code.** `ecowave/pilots.py`; `ecowave/evaluation.py` (EWS AUROC pooled
  + per-pilot, including holdouts).

## #5 — Missing variables (coverage)

- The `S` curve protest indicator (S2, Mass Mobilization / ACLED post-2020)
  and the `I` curve narrative-tone indicator (I2, GDELT tone) remain to
  ingest — both are listed as `not_automatable_v1` in `sources_manifest.json`.
- Symmetric US + Euro Area coverage on the S and D curves is partial; ECB
  CISS starts in 1999 which weakens C3 (dual-window robustness) for D.
