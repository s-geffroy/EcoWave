from __future__ import annotations

from pathlib import Path

import pytest

from ecowave.config import Settings
from ecowave.validation import check_config


def _settings(tmp_path: Path, fred_key: str, db_name: str = "ecowave.db") -> Settings:
    return Settings(
        mode="strict",
        pilot="2008",
        fred_api_key=fred_key,
        ecb_api_base="https://data-api.ecb.europa.eu/service",
        gdelt_enabled=False,
        gdelt_api_base="",
        world_bank_api_base="",
        db_path=tmp_path / db_name,
        data_raw_dir=tmp_path / "data_raw",
        data_processed_dir=tmp_path / "data_processed",
        events_dir=tmp_path / "events",
        reports_dir=tmp_path / "reports",
        figures_dir=tmp_path / "figures",
        annotations_dir=tmp_path / "annotations",
        dethrone_margin=0.30,
    )


def test_strict_fails_on_placeholder_key(tmp_path):
    settings = _settings(tmp_path, "replace_me")
    result = check_config(settings, "strict")
    assert not result.ok
    assert any(item.label == "FRED_API_KEY" and not item.ok for item in result.items)


def test_exploratory_allows_placeholder_key(tmp_path):
    settings = _settings(tmp_path, "replace_me")
    result = check_config(settings, "exploratory")
    assert result.ok  # db absent is tolerated in exploratory


def test_strict_passes_with_real_key_after_init(initialized_db):
    settings = _settings(initialized_db.parent, "real-key-1234")
    result = check_config(settings, "strict")
    assert result.ok


def test_invalid_mode_raises(tmp_path):
    with pytest.raises(ValueError):
        check_config(_settings(tmp_path, "k"), "banana")
