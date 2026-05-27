from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    mode: str
    pilot: str
    fred_api_key: str
    ecb_api_base: str
    gdelt_enabled: bool
    gdelt_api_base: str
    world_bank_api_base: str
    db_path: Path
    data_raw_dir: Path
    data_processed_dir: Path
    events_dir: Path
    reports_dir: Path
    figures_dir: Path

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            mode=os.getenv("ECOWAVE_MODE", "strict"),
            pilot=os.getenv("ECOWAVE_PILOT", "2008"),
            fred_api_key=os.getenv("FRED_API_KEY", ""),
            ecb_api_base=os.getenv("ECB_API_BASE", ""),
            gdelt_enabled=os.getenv("GDELT_ENABLED", "false").lower() in {"1", "true", "yes"},
            gdelt_api_base=os.getenv("GDELT_API_BASE", ""),
            world_bank_api_base=os.getenv("WORLD_BANK_API_BASE", ""),
            db_path=Path(os.getenv("ECOWAVE_DB_PATH", "/app/db/ecowave.db")),
            data_raw_dir=Path(os.getenv("DATA_RAW_DIR", "/app/data_raw")),
            data_processed_dir=Path(os.getenv("DATA_PROCESSED_DIR", "/app/data_processed")),
            events_dir=Path(os.getenv("EVENTS_DIR", "/app/events")),
            reports_dir=Path(os.getenv("REPORTS_DIR", "/app/reports")),
            figures_dir=Path(os.getenv("FIGURES_DIR", "/app/figures")),
        )


def is_placeholder(value: str) -> bool:
    return value.strip() in {"", "replace_me", "changeme", "todo"}
