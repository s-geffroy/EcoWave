from __future__ import annotations


def require_columns(columns: list[str], required: list[str]) -> None:
    missing = [col for col in required if col not in columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
