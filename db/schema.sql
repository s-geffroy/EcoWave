PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

INSERT OR REPLACE INTO schema_meta(key, value) VALUES
('schema_version', '0.5.0'),
('created_for', 'cpv_2026');

CREATE TABLE IF NOT EXISTS sources (
  id INTEGER PRIMARY KEY,
  provider TEXT NOT NULL,
  dataset_name TEXT NOT NULL,
  series_id TEXT,
  url TEXT,
  license_notes TEXT,
  access_method TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS variables (
  code TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  curve TEXT NOT NULL CHECK(curve IN ('E','D','S','L','I','M')),
  source_id INTEGER,
  frequency_raw TEXT,
  frequency_used TEXT,
  stress_orientation TEXT NOT NULL,
  transformation_notes TEXT,
  confidence TEXT NOT NULL CHECK(confidence IN ('A','B','C','D')),
  phase TEXT NOT NULL DEFAULT 'phase_1',
  is_critical INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
  id INTEGER PRIMARY KEY,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  status TEXT NOT NULL CHECK(status IN ('started','success','failed','partial')),
  mode TEXT NOT NULL CHECK(mode IN ('strict','exploratory')),
  notes TEXT
);

CREATE TABLE IF NOT EXISTS raw_files (
  id INTEGER PRIMARY KEY,
  ingestion_run_id INTEGER,
  variable_code TEXT,
  path TEXT NOT NULL,
  checksum_sha256 TEXT,
  created_at TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'available',
  FOREIGN KEY(ingestion_run_id) REFERENCES ingestion_runs(id),
  FOREIGN KEY(variable_code) REFERENCES variables(code)
);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY,
  event_date TEXT NOT NULL,
  event_name TEXT NOT NULL,
  event_type TEXT NOT NULL,
  affected_curves TEXT NOT NULL,
  phase_candidate TEXT,
  confidence TEXT NOT NULL CHECK(confidence IN ('A','B','C','D')),
  notes TEXT
);

CREATE TABLE IF NOT EXISTS event_sources (
  id INTEGER PRIMARY KEY,
  event_id INTEGER NOT NULL,
  source_label TEXT NOT NULL,
  source_url TEXT,
  quote_or_note TEXT,
  FOREIGN KEY(event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS analyst_notes (
  id INTEGER PRIMARY KEY,
  created_at TEXT NOT NULL,
  author TEXT NOT NULL DEFAULT 'analyst',
  object_type TEXT NOT NULL,
  object_id TEXT NOT NULL,
  note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS monthly_observation_index (
  id INTEGER PRIMARY KEY,
  month TEXT NOT NULL,
  variable_code TEXT NOT NULL,
  raw_value REAL,
  z_precrisis REAL,
  stress_precrisis REAL,
  z_structural REAL,
  stress_structural REAL,
  status TEXT NOT NULL CHECK(status IN ('available','partial','proxy','missing','invalid')),
  source_id INTEGER,
  notes TEXT,
  UNIQUE(month, variable_code),
  FOREIGN KEY(variable_code) REFERENCES variables(code),
  FOREIGN KEY(source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS curve_scores (
  id INTEGER PRIMARY KEY,
  month TEXT NOT NULL,
  curve TEXT NOT NULL CHECK(curve IN ('E','D','S','L','I','M')),
  stress_precrisis REAL,
  stress_structural REAL,
  variables_available INTEGER NOT NULL,
  variables_expected INTEGER NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('scored','provisional','blocked')),
  notes TEXT,
  UNIQUE(month, curve)
);

CREATE TABLE IF NOT EXISTS model_scores (
  id INTEGER PRIMARY KEY,
  model_code TEXT NOT NULL CHECK(model_code IN ('D','E','F','G','H')),
  criterion_code TEXT NOT NULL,
  raw_score INTEGER NOT NULL CHECK(raw_score BETWEEN 0 AND 3),
  weight REAL NOT NULL,
  weighted_score REAL NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS model_verdicts (
  id INTEGER PRIMARY KEY,
  model_code TEXT NOT NULL CHECK(model_code IN ('D','E','F','G','H')),
  c1_sync INTEGER NOT NULL CHECK(c1_sync BETWEEN 0 AND 3),
  c3_robustness INTEGER NOT NULL CHECK(c3_robustness BETWEEN 0 AND 3),
  weighted_score REAL NOT NULL,
  verdict TEXT NOT NULL CHECK(verdict IN ('strong','usable','fragile','rejected','blocked')),
  notes TEXT,
  UNIQUE(model_code)
);

CREATE TABLE IF NOT EXISTS validation_errors (
  id INTEGER PRIMARY KEY,
  created_at TEXT NOT NULL,
  severity TEXT NOT NULL CHECK(severity IN ('info','warning','error')),
  component TEXT NOT NULL,
  variable_code TEXT,
  message TEXT NOT NULL,
  mode_effect TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS global_indices (
  id INTEGER PRIMARY KEY,
  month TEXT NOT NULL,
  ref TEXT NOT NULL CHECK(ref IN ('precrisis','structural')),
  weighting TEXT NOT NULL CHECK(weighting IN ('equal','pca','favar')),
  weighting_actual TEXT NOT NULL,
  intensity REAL,
  intensity_ma3 REAL,
  intensity_hp_cycle REAL,
  intensity_hp_trend REAL,
  diffusion INTEGER NOT NULL,
  curves_scored INTEGER NOT NULL,
  weights_json TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('scored','blocked')),
  UNIQUE(month, ref, weighting)
);

CREATE TABLE IF NOT EXISTS external_anchors (
  id INTEGER PRIMARY KEY,
  month TEXT NOT NULL UNIQUE,
  value REAL NOT NULL,
  source_label TEXT NOT NULL,
  source_id INTEGER,
  FOREIGN KEY(source_id) REFERENCES sources(id)
);

-- ECPV (EcoWave Cycle Position Vector) — multi-cycle decomposition tables.
-- Schema 0.4.0. Long-horizon WB annual data per country/group + per-cycle
-- phase classification + cross-method consensus + cross-group universality.

CREATE TABLE IF NOT EXISTS cycle_observations (
  id INTEGER PRIMARY KEY,
  group_code TEXT NOT NULL,
  variable_code TEXT NOT NULL,
  year INTEGER NOT NULL,
  value REAL,
  source_id INTEGER,
  UNIQUE(group_code, variable_code, year),
  FOREIGN KEY(source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS cycle_positions (
  id INTEGER PRIMARY KEY,
  as_of_month TEXT NOT NULL,
  group_code TEXT NOT NULL,
  cycle TEXT NOT NULL CHECK(cycle IN ('kitchin','juglar','kuznets','kondratieff')),
  phase TEXT NOT NULL CHECK(phase IN ('expansion','peak','contraction','trough','rejected','disputed')),
  phi_rad REAL,
  amplitude REAL,
  ar1_p_value REAL,
  separable INTEGER NOT NULL CHECK(separable IN (0,1)),
  endpoint_caveat INTEGER NOT NULL DEFAULT 0 CHECK(endpoint_caveat IN (0,1)),
  notes TEXT,
  UNIQUE(as_of_month, group_code, cycle)
);

CREATE TABLE IF NOT EXISTS cycle_consensus (
  id INTEGER PRIMARY KEY,
  as_of_month TEXT NOT NULL,
  group_code TEXT NOT NULL,
  cycle TEXT NOT NULL CHECK(cycle IN ('kitchin','juglar','kuznets','kondratieff')),
  model_code TEXT NOT NULL CHECK(model_code IN ('D','E','F','G','H')),
  phase TEXT NOT NULL,
  p_value REAL,
  notes TEXT,
  UNIQUE(as_of_month, group_code, cycle, model_code)
);

CREATE TABLE IF NOT EXISTS cycle_universality (
  id INTEGER PRIMARY KEY,
  as_of_month TEXT NOT NULL,
  cycle TEXT NOT NULL CHECK(cycle IN ('kitchin','juglar','kuznets','kondratieff')),
  modal_phase TEXT NOT NULL,
  n_groups_concording INTEGER NOT NULL,
  n_groups_total INTEGER NOT NULL,
  universal INTEGER NOT NULL CHECK(universal IN (0,1)),
  notes TEXT,
  UNIQUE(as_of_month, cycle)
);
