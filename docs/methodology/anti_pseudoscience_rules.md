# Anti-pseudoscience rules — CPV protocol

These rules govern the Cycle Position Vector (CPV) framework. They are the
project's anti-pseudoscience guardrails: any cycle phase published by EcoWave
must obey *all* of the constraints below.

## Forbidden

- Reporting a cycle phase that does not beat the AR(1) surrogate null
  (a cycle "visible" in red noise is not a cycle).
- Reporting a phase from a single method when others disagree —
  consensus across ≥ 3 of 4 votant methods is mandatory.
- Hiding missing data sources or imputing them silently.
- Choosing cycle bands, surrogate parameters, or method thresholds *after*
  seeing the result. All parameters are frozen in code (`ecowave/cycles/bands.py`,
  `ecowave/cycles/surrogate.py`, `ecowave/waves/model_f_cycles.py`,
  `ecowave/waves/model_g_bryboschan.py`).
- Presenting exploratory outputs as final.

## Required

- Competing methods (D PELT, E Markov-switching, F CF+Hilbert, G Bry-Boschan),
  applied identically to every group and every cycle band.
- Explicit rejection reasons (`rejected`, `disputed`, `regional`,
  `endpoint_caveat`).
- Confidence grades on every ingested indicator (A–D, frozen in
  `cycles_manifest.json`).
- A source manifest as the single source of truth (`cycles_manifest.json`,
  `sources_manifest.json`).
- Raw values preserved alongside transforms (raw CSV in `data_raw/`).
- A surrogate null test on every published phase (Gate 1 in
  `cycle_validation_rules.md`).
- At least one pre-registered out-of-sample crisis pilot (2020 or 2022,
  `registered_at` field on the Pilot dataclass).
