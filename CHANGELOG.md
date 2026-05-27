# Changelog

All notable changes to EcoWave are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - 2026-05-27

### Added
- Project bootstrapped as **EcoWave** from the `geowave_2008_pilot` source skeleton
  (full rename: package, CLI, `ECOWAVE_*` env vars, `ecowave.db`).
- Real **FRED** ingestion with provenance: raw payloads versioned by run id under
  `data_raw/fred/`, registered in SQLite (`ingestion_runs`, `raw_files` with SHA-256),
  never overwritten. Series driven by `sources_manifest.json`.
- Real **ECB SDMX** ingestion (CISS) via the ECB Data Portal CSV endpoint.
- Curated **events** ingestion into SQLite (`events`, `event_sources`) and D3
  intervention-intensity derivation.
- Real **monthly panel** assembly (2007-2012) with dual-window normalization
  (pre-crisis 1990-2006, structural 1990-2019): z-scores and 0-100 stress percentiles,
  per-variable value transforms (level, drawdown, pct_change, inflation deviation).
- **Model scoring** A/B/C: C1 (multi-curve synchronisation) and C3 (window robustness)
  auto-computed from real data; C2/C4/C5/C6 left **blocked** (no fabrication).
- Three reports (`report_2008_pilot.md`, `model_comparison.md`, `validation_summary.md`)
  with explicit `provisional/blocked` verdict, source completeness and missing data.
- Extended **pytest** suite: schema init, config strict/exploratory, ingestion mocks,
  normalization, missing-data behavior, blocked scoring conditions.
- **MkDocs Material** documentation site + GitHub Actions workflow deploying to
  GitHub Pages on push to `main`.

### Notes
- Variables S1, S2, L2, I1, I2 have no automatable source in V1 → `missing`.
- E-curve uses US series in V1 (Euro Area not yet integrated).
