from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from ecowave.db import insert_event

REQUIRED_EVENT_COLUMNS = [
    "date",
    "event_name",
    "event_type",
    "affected_curves",
    "phase_candidate",
    "confidence",
    "source",
    "notes",
]


def load_events(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_EVENT_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing event columns: {missing}")
    return df


def ingest_events(path: Path, con: sqlite3.Connection) -> int:
    """Validate and insert events idempotently. Returns number of source rows processed."""
    df = load_events(path)
    for _, row in df.iterrows():
        insert_event(
            con,
            event_date=str(row["date"]),
            event_name=str(row["event_name"]),
            event_type=str(row["event_type"]),
            affected_curves=str(row["affected_curves"]),
            phase_candidate=str(row["phase_candidate"]),
            confidence=str(row["confidence"]),
            notes=str(row["notes"]),
            source_label=str(row["source"]),
        )
    return len(df)


def monthly_intervention_intensity(path: Path) -> pd.Series:
    """Derive D3: monthly count of D-curve institutional events (public_intervention/central_bank)."""
    df = load_events(path)
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    is_d = df["affected_curves"].str.contains("D", na=False)
    is_intervention = df["event_type"].isin(["public_intervention", "central_bank", "eurozone_sovereign"])
    selected = df[is_d & is_intervention]
    counts = selected.groupby("month").size().astype(float)
    counts.name = "monthly_value"
    return counts
