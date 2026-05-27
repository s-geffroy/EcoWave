from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "db" / "schema.sql"
SEED_PATH = REPO_ROOT / "db" / "seed_variables.sql"


@pytest.fixture
def schema_paths() -> tuple[Path, Path]:
    return SCHEMA_PATH, SEED_PATH


@pytest.fixture
def initialized_db(tmp_path, schema_paths):
    from ecowave.db import init_db

    db_path = tmp_path / "ecowave.db"
    schema, seed = schema_paths
    init_db(db_path, schema, seed)
    return db_path
