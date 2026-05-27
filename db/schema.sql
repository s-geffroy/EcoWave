PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

INSERT OR REPLACE INTO schema_meta(key, value) VALUES
('schema_version', '0.1.0'),
('created_for', 'ecowave_2008_pilot');

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

CREATE TABLE IF NOT EXISTS wave_candidates (
  id INTEGER PRIMARY KEY,
  model_code TEXT NOT NULL CHECK(model_code IN ('A','B','C')),
  wave_label TEXT NOT NULL,
  start_month TEXT NOT NULL,
  end_month TEXT NOT NULL,
  supporting_curves TEXT NOT NULL,
  robustness_score TEXT NOT NULL CHECK(robustness_score IN ('A','B','C','D')),
  rejection_reason TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS model_scores (
  id INTEGER PRIMARY KEY,
  model_code TEXT NOT NULL CHECK(model_code IN ('A','B','C')),
  criterion_code TEXT NOT NULL,
  raw_score INTEGER NOT NULL CHECK(raw_score BETWEEN 0 AND 3),
  weight REAL NOT NULL,
  weighted_score REAL NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS model_comparisons (
  id INTEGER PRIMARY KEY,
  model_code TEXT NOT NULL CHECK(model_code IN ('A','B','C')),
  c1_sync INTEGER NOT NULL CHECK(c1_sync BETWEEN 0 AND 3),
  c2_boundaries INTEGER NOT NULL CHECK(c2_boundaries BETWEEN 0 AND 3),
  c3_robustness INTEGER NOT NULL CHECK(c3_robustness BETWEEN 0 AND 3),
  c4_parsimony INTEGER NOT NULL CHECK(c4_parsimony BETWEEN 0 AND 3),
  c5_added_value INTEGER NOT NULL CHECK(c5_added_value BETWEEN 0 AND 3),
  c6_transferability INTEGER NOT NULL CHECK(c6_transferability BETWEEN 0 AND 3),
  weighted_score REAL NOT NULL,
  verdict TEXT NOT NULL CHECK(verdict IN ('strong','usable','fragile','rejected','blocked','provisional')),
  notes TEXT
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
