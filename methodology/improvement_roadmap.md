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

## #5 — Long-history extension (Maddison + Jordà-Schularick-Taylor) — IMPLEMENTED

- **Problem.** 65 years of WB data ≈ 1.0–1.5 Kondratieff cycles. Gate 1
  (AR(1) bootstrap) cannot distinguish a real K-wave from a smooth red-noise
  excursion on so few cycles.
- **Method.** Add a second ingestion path that reads Maddison Project 2023
  (real GDP per capita 1820–2022) and Jordà-Schularick-Taylor R6 (credit,
  house prices, equity, sovereign yield, CPI, money for 18 advanced
  economies 1870–2020). 154 years × 18 countries gives ≥ 3 K-waves,
  ≥ 8 Kuznets, ≥ 17 Juglar.
- **Code.** `ecowave/cycles/long_history.py`; new
  `long_history_manifest.json`; CLI option `position-cycles --horizon long`.
- **Acceptance.** Long-horizon panel on the synthetic fixture shows the
  Juglar signal emerging cleanly at the expected 9-year period.

## #6 — Composite par-bande — IMPLEMENTED

- **Problem.** The original composite z-scored each indicator over its full
  history then averaged across indicators. Cyclical content at any one
  frequency is diluted by indicators not cyclical at that frequency.
- **Method.** For each cycle band, first CF-band-pass each indicator into
  the band, then z-score and average. The composite is now band-specific
  and concentrates cyclical power in the target band.
- **Code.** `ecowave/cycles/runner.py:_composite_panel(panel, band=...)`.
- **Acceptance.** On the WB panel with `--null dual`, the number of cells
  surviving Gate 1 increased from 4 to 7, with concrete phase labels
  (contraction / expansion) instead of just `disputed`.

## #7 — Dual null (AR(1) + phase-scrambling) — IMPLEMENTED

- **Problem.** AR(1) bootstrap absorbs cyclical content into the persistence
  parameter φ (Vyushin & Kushner 2009). Phase-scrambling (Theiler 1992)
  preserves the spectrum exactly; both are complementary.
- **Method.** Compute both nulls; a cell passes Gate 1 only when **both**
  reject. The conservative dual gate is closer to a "real cycle" test.
- **Code.** `ecowave/cycles/surrogate.py:phase_scramble_null` + `dual_null`.
  CLI option `--null dual`.
- **Acceptance.** Dual gate is by definition ≥ either single gate; it
  catches false positives from each null individually.

## #8 — Wavelet band-power as alternative test statistic — IMPLEMENTED

- **Problem.** CF band-power is endpoint-sensitive on the last `hi_years/2`
  samples — exactly where the most policy-relevant phase is.
- **Method.** Use Morlet wavelet scaleogram |W(s,t)|² integrated in-band
  as the test statistic; AR(1) bootstrap as the null distribution. Less
  edge-sensitive than CF.
- **Code.** `ecowave/cycles/surrogate.py:wavelet_bandpower_null`. CLI
  option `--null wavelet`.

## #9 — Quarterly extension for Kitchin — TODO

- **Problem.** Annual data caps Kitchin at the 4-5y upper edge (Nyquist).
- **Method (planned).** Add FRED quarterly real GDP (US: GDPC1) + Eurostat
  QNA + OECD QNA ingest paths for the major economies. Produces a 1947–
  present quarterly panel for HIC/OECD, allowing CF on the full Kitchin
  3-5y band.
- **Status.** Not implemented. Would require a new ingest module
  (`ecowave/cycles/quarterly.py`) and a new manifest. Estimated 1-day
  effort.

## #10 — Missing variables (coverage) — TODO

- The `S` curve protest indicator (S2, Mass Mobilization / ACLED post-2020)
  and the `I` curve narrative-tone indicator (I2, GDELT tone) remain to
  ingest — both are listed as `not_automatable_v1` in `sources_manifest.json`.
- Symmetric US + Euro Area coverage on the S and D curves is partial; ECB
  CISS starts in 1999 which weakens C3 (dual-window robustness) for D.
