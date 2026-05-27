from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MANIFEST_PATH = Path("/app/sources_manifest.json")


@dataclass(frozen=True)
class ComponentSpec:
    label: str
    provider: str
    value_transform: str
    series_id: str | None = None
    minus_series_id: str | None = None


@dataclass(frozen=True)
class IngestionSpec:
    variable_code: str
    provider: str
    dataset_name: str
    monthly_agg: str
    value_transform: str
    stress_orientation: str
    confidence: str
    series_id: str | None = None
    minus_series_id: str | None = None
    series_key: str | None = None
    requires_key: bool = False
    license_notes: str = ""
    components: tuple[ComponentSpec, ...] = ()

    @property
    def is_composite(self) -> bool:
        return bool(self.components)


@dataclass(frozen=True)
class ReferenceWindow:
    start: str
    end: str


@dataclass(frozen=True)
class Manifest:
    project: str
    precrisis: ReferenceWindow
    structural: ReferenceWindow
    panel_start: str
    panel_end: str
    specs: list[IngestionSpec]
    not_automatable: dict[str, str]


def load_manifest(path: Path = DEFAULT_MANIFEST_PATH) -> Manifest:
    data = json.loads(path.read_text(encoding="utf-8"))
    rw = data["reference_windows"]
    pw = data["panel_window"]
    specs = [
        IngestionSpec(
            variable_code=item["variable_code"],
            provider=item["provider"],
            dataset_name=item.get("dataset_name", item["variable_code"]),
            monthly_agg=item.get("monthly_agg", "avg"),
            value_transform=item.get("value_transform", "level"),
            stress_orientation=item["stress_orientation"],
            confidence=item.get("confidence", "C"),
            series_id=item.get("series_id"),
            minus_series_id=item.get("minus_series_id"),
            series_key=item.get("series_key"),
            requires_key=bool(item.get("requires_key", False)),
            license_notes=item.get("license_notes", ""),
            components=tuple(
                ComponentSpec(
                    label=c["label"],
                    provider=c.get("provider", "FRED"),
                    value_transform=c.get("value_transform", item.get("value_transform", "level")),
                    series_id=c.get("series_id"),
                    minus_series_id=c.get("minus_series_id"),
                )
                for c in item.get("components", [])
            ),
        )
        for item in data.get("ingestion_plan", [])
    ]
    not_automatable = {
        item["variable_code"]: item.get("reason", "")
        for item in data.get("not_automatable_v1", [])
    }
    return Manifest(
        project=data["project"],
        precrisis=ReferenceWindow(**rw["precrisis"]),
        structural=ReferenceWindow(**rw["structural"]),
        panel_start=pw["start"],
        panel_end=pw["end"],
        specs=specs,
        not_automatable=not_automatable,
    )
