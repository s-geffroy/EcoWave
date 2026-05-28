"""Fetch the exogenous activity anchor used by the FAVAR weighting.

Priority cascade (each falls back if the previous fails):

1. OECD + Major 6 NME Composite Leading Indicator, normalised, SA, monthly
   (FRED ``OECDLOLITONOSTSAM``). Broad OECD coverage including Brazil, China,
   India, Indonesia, Russia and South Africa.
2. GDP-weighted composite of G4 industrial production (US/EA/JP/UK).
3. Kilian Index of Global Real Economic Activity (FRED ``IGREA``).

Output: monthly Series indexed by ``YYYY-MM`` (strings), already oriented
``higher_is_stress`` — i.e. the negative of standardised YoY growth so that
contractions push the index up, consistent with the rest of EcoWave.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from ecowave.ingest.fred import fetch_fred_series
from ecowave.normalize.monthly import daily_to_monthly
from ecowave.db import upsert_source

ANCHOR_VARIABLE_CODE = "ANCHOR"

# GDP weights (World Bank 2007 nominal GDP, USD trillions). Frozen mid-pre-crisis
# so the fallback composite is comparable across pilots without revisions.
G4_GDP_WEIGHTS = {
    "INDPRO": 14.45,            # US
    "PRMNTO01EZQ661N": 12.34,   # Euro Area (OECD via FRED)
    "JPNPROINDMISMEI": 4.52,    # Japan
    "GBRPROINDMISMEI": 3.07,    # United Kingdom
}


@dataclass(frozen=True)
class AnchorResult:
    series: pd.Series
    label: str
    source_id: int | None


def _to_higher_is_stress_yoy(monthly: pd.Series) -> pd.Series:
    yoy = monthly.pct_change(12) * 100.0
    yoy = yoy.dropna()
    if yoy.empty:
        return yoy
    mu = float(yoy.mean())
    sigma = float(yoy.std(ddof=0)) or 1.0
    return -((yoy - mu) / sigma)


def _fetch_anchor_series(series_id: str, api_key: str, data_raw_dir: Path,
                         run_id: int, observation_start: str) -> pd.Series | None:
    """Fetch a FRED series for the FAVAR anchor. Persists raw to disk for audit,
    but does NOT register in ``raw_files`` (that table is FK-bound to the
    panel variables and the anchor is an exogenous side-source)."""
    try:
        raw = fetch_fred_series(series_id, api_key, observation_start)
    except (requests.HTTPError, ValueError):
        return None
    if raw is None or raw.empty:
        return None
    target_dir = data_raw_dir / "anchors"
    target_dir.mkdir(parents=True, exist_ok=True)
    raw.to_csv(target_dir / f"{series_id}_run{run_id}.csv", index=False)
    monthly = daily_to_monthly(raw).set_index("month")["monthly_avg"]
    return monthly.dropna()


def _try_single_fred_anchor(series_id: str, api_key: str, data_raw_dir: Path,
                            con: sqlite3.Connection, run_id: int,
                            observation_start: str) -> AnchorResult | None:
    monthly = _fetch_anchor_series(series_id, api_key, data_raw_dir, run_id, observation_start)
    if monthly is None or monthly.empty:
        return None
    oriented = _to_higher_is_stress_yoy(monthly)
    if oriented.empty:
        return None
    source_id = upsert_source(
        con, provider="FRED", dataset_name=f"FAVAR anchor: {series_id}",
        series_id=series_id, url=f"https://fred.stlouisfed.org/series/{series_id}",
        license_notes="FRED — verify before redistribution",
        access_method="api_json",
    )
    return AnchorResult(oriented, f"FRED:{series_id}", source_id)


def _try_composite_g4(api_key: str, data_raw_dir: Path, con: sqlite3.Connection,
                      run_id: int, observation_start: str) -> AnchorResult | None:
    fetched: dict[str, pd.Series] = {}
    for code in G4_GDP_WEIGHTS:
        s = _fetch_anchor_series(code, api_key, data_raw_dir, run_id, observation_start)
        if s is not None and not s.empty:
            fetched[code] = s
    if len(fetched) < 2:
        return None
    df = pd.concat(fetched, axis=1).sort_index()
    weights = np.array([G4_GDP_WEIGHTS[c] for c in df.columns], dtype=float)
    weights /= weights.sum()
    composite = df.mul(weights, axis=1).sum(axis=1, min_count=2)
    oriented = _to_higher_is_stress_yoy(composite)
    if oriented.empty:
        return None
    source_id = upsert_source(
        con, provider="FRED", dataset_name="FAVAR anchor: G4 industrial production composite (GDP-weighted)",
        series_id="G4_IP_COMPOSITE",
        url="https://fred.stlouisfed.org/",
        license_notes="FRED — verify before redistribution",
        access_method="api_json_composite",
    )
    return AnchorResult(oriented, "FRED:G4_IP_COMPOSITE", source_id)


def fetch_anchor(api_key: str, data_raw_dir: Path, con: sqlite3.Connection,
                 run_id: int, observation_start: str = "1990-01-01") -> AnchorResult | None:
    """Run the priority cascade and return the first anchor that resolves.

    Returns None only if every source fails — the caller is expected to fall back
    to a non-FAVAR weighting (pca or equal).
    """
    primary = _try_single_fred_anchor("OECDLOLITONOSTSAM", api_key, data_raw_dir, con,
                                      run_id, observation_start)
    if primary is not None:
        return primary
    fallback1 = _try_composite_g4(api_key, data_raw_dir, con, run_id, observation_start)
    if fallback1 is not None:
        return fallback1
    return _try_single_fred_anchor("IGREA", api_key, data_raw_dir, con, run_id, observation_start)
