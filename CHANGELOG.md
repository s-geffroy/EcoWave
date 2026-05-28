# Changelog

All notable changes to the project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased] — Cycle Position Vector (CPV) framework

### Path 5 — Quarterly Kitchin extension (Roadmap #9 — IMPLÉMENTÉ)

Adds a third data horizon `position-cycles --horizon quarterly` that
lifts Kitchin (3-5 y) above the practical Nyquist threshold, the
limitation that was forcing every Kitchin cell in the 2026-05 World
Bank run to publish as `rejected`. The annual `--horizon wb` path keeps
its narrow 4-5 y diagnostic attempt unchanged (non-regression).

- **New module** `ecowave/cycles/quarterly.py` — fetchers for FRED
  (JSON observations), Eurostat (JSON-stat 2.0 via
  `statistics/1.0/data`), and OECD (SDMX 2.1 REST at `sdmx.oecd.org`
  with DSD introspection that probes three structure-endpoint
  variants). GDP-weighted multi-country aggregation;
  `PeriodIndex(freq="Q")`-aware panel construction. Tagged silent
  fetch failures bubble up as a stderr summary per group.
- **OECD path is experimental** — `sdmx.oecd.org`'s compound DSD refs
  (`DSD_X@DF_Y`) return empty payloads under the standard
  `/datastructure/{agency}/{id}/{version}` and `/dataflow/.../?references=descendants`
  endpoints, blocking automatic dimension-order discovery. The v1
  manifest uses FRED-hosted OECD/IFS mirror series for JPN/GBR/CAN
  (`JPNRGDPEXP`, `NGDPRSAXDCGBQ`, `NGDPRSAXDCCAQ`,
  `JPNCPIALLMINMEI`, `GBRCPIALLMINMEI`,
  `LRUNTTTTJPM156S`, `LRUN64TTGBQ156S`) — same underlying source data,
  one API surface to maintain. The native OECD fetcher remains
  callable for users with known dim mappings.
- **CF bandpass NaN robustness** — `ecowave/cycles/decompose.cf_bandpass`
  now drops NaN before calling `cffilter`, then reindexes to the
  original index. `statsmodels.cffilter` propagates any single NaN
  to all outputs; the previous behaviour broke Gate 2 on multi-country
  composites that picked up a 1-quarter alignment hole. Surfaced by
  Path 5 testing on G7Q.
- **New manifest** `quarterly_manifest.json` — three variables
  (`Q_GDP`, `Q_CPI`, `Q_UNRATE`), six groups (USA, EA, JPN, GBR, G7Q,
  OECDQ). EA aggregate starts 1995 (Eurostat `EA20` native).
- **Runner threading** — `samples_per_year` plumbed through
  `_composite_panel`, `_run_gate1`, `_analyse_and_render`. Kitchin
  band gate is now conditional: `samples_per_year <= 1.0` → narrow
  (4, 5); `samples_per_year > 1.0` → full (3, 5). New
  `report_suffix` kwarg replaces the substring-based horizon sniff so
  the quarterly report lands at
  `reports/cycle_position_<as_of>_q.md`.
- **DB schema 0.5.0 → 0.5.1** — new table
  `cycle_observations_quarterly(group_code, variable_code, year,
  quarter, value, source_id)` with `UNIQUE(group, var, year, quarter)`
  and `CHECK(quarter BETWEEN 1 AND 4)`. The annual
  `cycle_observations` table is unchanged. `migrate_db` is now
  idempotent and handles in-place 0.5.0 → 0.5.1 upgrades. New helper
  `upsert_cycle_observation_quarterly`.
- **CLI** — `--horizon` accepts `wb | long | quarterly`; per-horizon
  defaults for `--manifest` and `--groups`.
- **Tests** — `tests/test_quarterly_panel.py`,
  `tests/test_samples_per_year_thread.py`,
  `tests/test_kitchin_gate_conditional.py`,
  `tests/test_runner_quarterly_smoke.py`.
- **Docs** — `methodology/feuille_de_route.md` Item #9 flipped to
  IMPLÉMENTÉ; `docs/cycles/kitchin.md` adds a "Chemin trimestriel
  natif" subsection.

### Schema version: 0.5.1 (was 0.5.0)



The project's active framework. Decomposes macroeconomic time-series into the
four canonical economic cycles (Kitchin / Juglar / Kuznets / Kondratieff) and
publishes per-group phase labels under three falsifiability gates
(existence / consensus / universality).

### Site rewrite — French academic edition (2026-05)

The published documentation site is rewritten in French with an academic
template (Résumé / Notation / Méthode / Résultats / Caveats / Références)
and a figures-forward layout. The code, commit messages, and this
CHANGELOG remain in English by design.

- **mkdocs.yml**: `language: fr`, indigo palette, MathJax via
  `pymdownx.arithmatex`, footnotes, navigation tabs + indexes. Nav restructured
  to Accueil / Protocole CPV / Cycles canoniques / Groupes / Résultats /
  Analyses approfondies / Validation EWS / Sources / Bibliographie.
- **New consolidated bibliography** (`docs/bibliographie.md`) with stable
  author-year anchors. All site pages cite into this single file.
- **Four new figure functions** in `ecowave/cycles/report.py`:
  `plot_amplitude_heatmap`, `plot_pvalue_heatmap`, `plot_phase_polar_diagram`,
  `plot_next_extremum_timeline`. Wired into `runner.py:_analyse_and_render`
  so they ship with every `position-cycles` run on both horizons.
- **Methodology renamed + translated**: 8 pages (`protocole_cpv`,
  `trois_portes`, `methodes_decomposition`, `indicateur_composite`,
  `normalisation`, `garde_fous`, `fenetres_reference`, `feuille_de_route`).
- **Result reports rewritten** in academic French with figures-forward
  layout: `panel_banque_mondiale_2026.md`, `histoire_longue_2026.md`,
  `validation_ews.md`.
- **Deep-dive analyses academised**: Résumé / Notation / Références
  sections added to `juglar_us_anglo_nordic_2026.md` and
  `kondratieff_adv18_eu4_2026.md`.
- **Cycles pages** (Kitchin / Juglar / Kuznets / Kondratieff) translated
  and each lead with the polar phase diagram for its band.
- **Sync + CI**: `scripts/sync_docs.sh` updated for the new figure
  patterns and French slugs; `.github/workflows/pages.yml` description
  updated.

`mkdocs build --strict` passes cleanly. Site name stays *CPV — Cycle
Position Vector* with the French subtitle « Décomposition multi-cycles
falsifiable des indicateurs macroéconomiques ».

### Schema version: 0.5.0 (initial CPV schema)

DB schema is rebuilt from scratch. Tables:

- `sources`, `variables`, `ingestion_runs`, `raw_files`, `events`,
  `event_sources`, `analyst_notes`, `monthly_observation_index`,
  `curve_scores` — pilot-window panel.
- `global_indices` — composite intensity + diffusion across three weightings.
- `model_scores`, `model_verdicts` — CPV stack outputs (one row per
  D/E/F/G/H method).
- `cycle_observations`, `cycle_positions`, `cycle_consensus`,
  `cycle_universality` — CPV long-horizon outputs.
- `external_anchors`, `validation_errors`, `schema_meta`.

### CPV stack (Models D / E / F / G)

- **Model D** — PELT change-point detection (`waves/model_d_regime.py`).
- **Model E** — Markov-switching AR(1) (`waves/model_e_markov.py`).
- **Model F** — Christiano-Fitzgerald Juglar band-pass + Hilbert phase
  (`waves/model_f_cycles.py`).
- **Model G** — Bry-Boschan / Harding-Pagan turning-point dating
  (`waves/model_g_bryboschan.py`).

### CPV module (`ecowave/cycles/`)

- `bands.py` — frozen 4 cycle bands + 9 group codes (WLD, OECD, HIC, UMC,
  LMC, LIC, G7, G20, BRICS).
- `manifest.py` — `CycleSpec` + `CycleManifest` loader.
- `ingest.py` — multi-country WB ingestion with GDP-weighted aggregation.
- `decompose.py` — CF band-pass + continuous Morlet wavelet + COI.
- `phase.py` — Hilbert instantaneous phase + 4-quadrant classification.
- `surrogate.py` — AR(1) bootstrap null (Gate 1).
- `consensus.py` — method consensus (Gate 2).
- `universality.py` — cross-group concordance (Gate 3).
- `report.py` — signed-note rendering + figures.
- `runner.py` — end-to-end pipeline.

### CLI

- `ecowave init-db` — initialize the SQLite database.
- `ecowave check-config` — validate sources and storage.
- `ecowave position-cycles` — multi-cycle world positioning.
- `ecowave run-pilot <code>` — CPV stack on a crisis window.
- `ecowave evaluate-ews` — out-of-sample AUROC validation.
- `ecowave sources` — render the data-sources page.
- `ecowave generate-report` — render the pilot report.

### Manifests

- `sources_manifest.json` — pilot-window FRED/ECB/WorldBank panel.
- `cycles_manifest.json` — long-horizon 8-indicator World Bank panel.

### Methodology

- `methodology/multi_cycle_decomposition.md` — CPV protocol spec.
- `methodology/cycle_validation_rules.md` — three falsifiability gates.
- `methodology/cycle_methods_survey.md` — decision matrix.
- `methodology/composite_indicator.md` — intensity + diffusion.
- `methodology/anti_pseudoscience_rules.md` — CPV guardrails.
- `methodology/improvement_roadmap.md` — design history.
- `methodology/normalization_rules.md`.
- `methodology/reference_windows.md`.

### Reports & analyses (2026-05)

- `reports/cycle_position_2026_05_wb.md` — World Bank panel run
  (9 groups, 1000 surrogates, dual null).
- `reports/cycle_position_2026_05_long.md` — long-history run
  (Maddison Project 2023 + Jordà-Schularick-Taylor R6, 1870-2022,
  ADV18 / G7 / USA / EU4 / ANGLO / NORDIC).
- `reports/juglar_us_anglo_nordic_2026.md` — signed deep-dive on the
  Juglar divergence between USA/ANGLO (expansion, peak ~2024) and
  NORDIC (contraction, trough late-2023, peak ~mid-2026).
- `reports/kondratieff_adv18_eu4_2026.md` — signed deep-dive on the
  K5 peak in 2018-2022, K3/K4 historical retrieval at ±5 years,
  amplitude (~0.85) at half of K3/K4 (~1.55/1.28).

### Dependencies

`typer`, `click`, `pydantic`, `pandas`, `numpy`, `scipy`, `ruptures`,
`statsmodels`, `requests`, `matplotlib`, `jinja2`, `pyarrow`, `pywavelets`,
`tabulate`, `pytest`, `ruff`, `mkdocs-material`.
