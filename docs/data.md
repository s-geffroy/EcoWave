# Data panels

The analytical panel is produced by the CLI (`ecowave run-pilot 2008`) and stored in
two forms:

- `monthly_panel_2007_2012.csv` — human-auditable.
- `monthly_panel_2007_2012.parquet` — analytical.

Each row carries: `month`, `variable_code`, `raw_value`, `z_precrisis`,
`stress_precrisis`, `z_structural`, `stress_structural`, `status`, `source`,
`confidence`, `notes`.

## Status values

| Status | Meaning |
|---|---|
| `available` | Real value ingested and normalized against the reference windows |
| `partial` | Value present but no reference window available (e.g. event-derived D3) |
| `missing` | No automatable source in V1 (S2, I1, I2, L2, S1) |

## Provenance

Every raw payload is saved under `data_raw/<provider>/<series>_run<id>.csv` and
registered in SQLite (`ingestion_runs`, `raw_files` with SHA-256). Raw data is
**never overwritten** — each run gets a new id.

!!! note
    Raw API payloads are not published on this site (licensing). The aggregated
    monthly panels are derived public statistics.
