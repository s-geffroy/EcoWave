# SQLite database

`ecowave.db` is the local application state database.

It stores:

- source metadata
- variable registry
- ingestion runs
- raw file registry
- curated events
- analyst notes
- wave candidates
- model scores
- validation errors

It does **not** replace Parquet as the analytical storage format for monthly panels.
