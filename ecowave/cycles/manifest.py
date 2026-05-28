"""Cycle manifest loader. Mirrors the structure of ``ingest.manifest`` but for
long-horizon multi-country WB indicators rather than short crisis-window panels.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

DEFAULT_CYCLE_MANIFEST_PATH = Path("/app/cycles_manifest.json")


@dataclass(frozen=True)
class CycleSpec:
    variable_code: str
    series_id: str
    dataset_name: str
    value_transform: str  # "level", "pct_change", "log", "log_diff"
    cycle_targets: tuple[str, ...]
    confidence: str = "B"
    license_notes: str = ""
    notes: str = ""


@dataclass(frozen=True)
class CycleManifest:
    project: str
    as_of_month: str
    start_year: int
    specs: list[CycleSpec]


def load_cycle_manifest(path: Path = DEFAULT_CYCLE_MANIFEST_PATH) -> CycleManifest:
    data = json.loads(path.read_text(encoding="utf-8"))
    specs = [
        CycleSpec(
            variable_code=item["variable_code"],
            series_id=item["series_id"],
            dataset_name=item.get("dataset_name", item["variable_code"]),
            value_transform=item.get("value_transform", "level"),
            cycle_targets=tuple(item.get("cycle_targets", [])),
            confidence=item.get("confidence", "B"),
            license_notes=item.get("license_notes", ""),
            notes=item.get("notes", ""),
        )
        for item in data.get("ingestion_plan", [])
    ]
    return CycleManifest(
        project=data.get("project", "ecowave_cycles"),
        as_of_month=data.get("as_of_month", "2026-05"),
        start_year=int(data.get("start_year", 1960)),
        specs=specs,
    )
