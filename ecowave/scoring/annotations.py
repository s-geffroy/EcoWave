from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["model_code", "criterion_code", "raw_score", "justification"]
VALID_MODELS = {"A", "B", "C"}
VALID_CRITERIA = {"C2", "C4", "C5", "C6"}


@dataclass(frozen=True)
class Annotation:
    raw_score: int
    justification: str
    analyst: str
    date: str


def load_annotations(path: Path) -> dict[tuple[str, str], Annotation]:
    """Load and validate qualitative annotations.

    Returns {(model_code, criterion_code): Annotation} for filled rows only.
    Raises ValueError on malformed input or a score without justification
    (anti-pseudoscience: no score is accepted without evidence).
    """
    if not path.exists():
        return {}

    df = pd.read_csv(path, dtype=str).fillna("")
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Annotation file missing columns: {missing}")

    out: dict[tuple[str, str], Annotation] = {}
    for i, row in df.iterrows():
        model = row["model_code"].strip()
        crit = row["criterion_code"].strip()
        score_raw = row["raw_score"].strip()
        justification = row["justification"].strip()

        if score_raw == "":
            continue  # unfilled -> stays blocked

        if model not in VALID_MODELS or crit not in VALID_CRITERIA:
            raise ValueError(f"Row {i}: invalid model/criterion '{model}/{crit}'")
        try:
            score = int(float(score_raw))
        except ValueError as exc:
            raise ValueError(f"Row {i} ({model}/{crit}): raw_score '{score_raw}' is not an integer") from exc
        if score not in {0, 1, 2, 3}:
            raise ValueError(f"Row {i} ({model}/{crit}): raw_score {score} out of range 0-3")
        if not justification:
            raise ValueError(
                f"Row {i} ({model}/{crit}): raw_score set without justification "
                "(no score is accepted without evidence)"
            )
        out[(model, crit)] = Annotation(
            raw_score=score,
            justification=justification,
            analyst=row.get("analyst", "").strip() or "unknown",
            date=row.get("date", "").strip(),
        )
    return out
