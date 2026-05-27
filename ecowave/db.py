from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _nn(value):
    """Coerce pandas NaN/NaT to None so SQLite stores NULL, not a NaN float."""
    if value is None:
        return None
    try:
        if isinstance(value, float) and value != value:  # NaN
            return None
    except TypeError:
        pass
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON;")
    return con


def init_db(db_path: Path, schema_path: Path, seed_path: Path) -> None:
    con = connect(db_path)
    try:
        con.executescript(schema_path.read_text(encoding="utf-8"))
        con.executescript(seed_path.read_text(encoding="utf-8"))
        con.commit()
    finally:
        con.close()


def get_schema_version(db_path: Path) -> str | None:
    if not db_path.exists():
        return None
    con = connect(db_path)
    try:
        row = con.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()
        return row["value"] if row else None
    finally:
        con.close()


def log_validation(db_path: Path, severity: str, component: str, message: str, mode_effect: str, variable_code: str | None = None) -> None:
    con = connect(db_path)
    try:
        con.execute(
            """
            INSERT INTO validation_errors(created_at, severity, component, variable_code, message, mode_effect)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (_now(), severity, component, variable_code, message, mode_effect),
        )
        con.commit()
    finally:
        con.close()


# --- Ingestion run / provenance helpers -----------------------------------

def start_ingestion_run(con: sqlite3.Connection, mode: str, notes: str = "") -> int:
    cur = con.execute(
        "INSERT INTO ingestion_runs(started_at, status, mode, notes) VALUES (?, 'started', ?, ?)",
        (_now(), mode, notes),
    )
    con.commit()
    return int(cur.lastrowid)


def finish_ingestion_run(con: sqlite3.Connection, run_id: int, status: str, notes: str = "") -> None:
    con.execute(
        "UPDATE ingestion_runs SET finished_at=?, status=?, notes=? WHERE id=?",
        (_now(), status, notes, run_id),
    )
    con.commit()


def upsert_source(con: sqlite3.Connection, provider: str, dataset_name: str, series_id: str | None,
                  url: str | None, license_notes: str | None, access_method: str) -> int:
    row = con.execute(
        "SELECT id FROM sources WHERE provider=? AND dataset_name=? AND IFNULL(series_id,'')=IFNULL(?,'')",
        (provider, dataset_name, series_id),
    ).fetchone()
    if row:
        return int(row["id"])
    cur = con.execute(
        """INSERT INTO sources(provider, dataset_name, series_id, url, license_notes, access_method, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (provider, dataset_name, series_id, url, license_notes, access_method, _now()),
    )
    con.commit()
    return int(cur.lastrowid)


def register_raw_file(con: sqlite3.Connection, run_id: int, variable_code: str, path: Path) -> None:
    con.execute(
        """INSERT INTO raw_files(ingestion_run_id, variable_code, path, checksum_sha256, created_at, status)
           VALUES (?, ?, ?, ?, ?, 'available')""",
        (run_id, variable_code, str(path), sha256_file(path), _now()),
    )
    con.commit()


def upsert_monthly_observation(con: sqlite3.Connection, month: str, variable_code: str,
                               raw_value, z_precrisis, stress_precrisis, z_structural,
                               stress_structural, status: str, source_id: int | None, notes: str) -> None:
    con.execute(
        """INSERT INTO monthly_observation_index
           (month, variable_code, raw_value, z_precrisis, stress_precrisis, z_structural,
            stress_structural, status, source_id, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(month, variable_code) DO UPDATE SET
             raw_value=excluded.raw_value, z_precrisis=excluded.z_precrisis,
             stress_precrisis=excluded.stress_precrisis, z_structural=excluded.z_structural,
             stress_structural=excluded.stress_structural, status=excluded.status,
             source_id=excluded.source_id, notes=excluded.notes""",
        (month, variable_code, _nn(raw_value), _nn(z_precrisis), _nn(stress_precrisis),
         _nn(z_structural), _nn(stress_structural), status, _nn(source_id), notes),
    )


def insert_event(con: sqlite3.Connection, event_date: str, event_name: str, event_type: str,
                 affected_curves: str, phase_candidate: str, confidence: str, notes: str,
                 source_label: str) -> None:
    exists = con.execute(
        "SELECT id FROM events WHERE event_date=? AND event_name=?", (event_date, event_name)
    ).fetchone()
    if exists:
        return
    cur = con.execute(
        """INSERT INTO events(event_date, event_name, event_type, affected_curves, phase_candidate, confidence, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (event_date, event_name, event_type, affected_curves, phase_candidate, confidence, notes),
    )
    con.execute(
        "INSERT INTO event_sources(event_id, source_label, source_url, quote_or_note) VALUES (?, ?, NULL, ?)",
        (int(cur.lastrowid), source_label, notes),
    )
    con.commit()


def replace_curve_scores(con: sqlite3.Connection, rows: list[dict]) -> None:
    con.execute("DELETE FROM curve_scores")
    for r in rows:
        con.execute(
            """INSERT INTO curve_scores(month, curve, stress_precrisis, stress_structural,
                 variables_available, variables_expected, status, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (r["month"], r["curve"], _nn(r["stress_precrisis"]), _nn(r["stress_structural"]),
             r["variables_available"], r["variables_expected"], r["status"], r.get("notes", "")),
        )
    con.commit()


def replace_model_scores(con: sqlite3.Connection, rows: list[dict]) -> None:
    """Persist only honestly-computed integer scores (schema forbids NULL raw_score)."""
    con.execute("DELETE FROM model_scores")
    for r in rows:
        con.execute(
            """INSERT INTO model_scores(model_code, criterion_code, raw_score, weight, weighted_score, notes)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (r["model_code"], r["criterion_code"], r["raw_score"], r["weight"],
             r["weighted_score"], r.get("notes", "")),
        )
    con.commit()


def add_analyst_note(con: sqlite3.Connection, object_type: str, object_id: str, note: str,
                     author: str = "ecowave-pipeline") -> None:
    con.execute(
        "INSERT INTO analyst_notes(created_at, author, object_type, object_id, note) VALUES (?, ?, ?, ?, ?)",
        (_now(), author, object_type, object_id, note),
    )
    con.commit()
