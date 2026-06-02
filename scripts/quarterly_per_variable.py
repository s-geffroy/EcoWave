"""Per-variable Gate 1 on the quarterly panel (FRED / Eurostat / OECD / BIS).

Loads the already-ingested quarterly series from
db/ecowave.db (table ``cycle_observations_quarterly``) and runs the
AR(1) bootstrap component of Gate 1 on each (group, variable, cycle
band) cell. Output: ``reports/quarterly_per_variable.json``.

At ``samples_per_year=4``, a series of length ``N`` quarters covers
``N/4`` calendar years; the threshold ``N/4 > 4*hi_years``
(\emph{i.e.} ``N > 16*hi_years``) is enforced cell-by-cell.

The quarterly panel can test Kitchin (3--5y, need N>80 quarters) on
nearly every group and Juglar (7--11y, need N>176 quarters) on most
groups. Kuznets (15--25y, need N>400 quarters) is borderline and only
a few long-running aggregates (G7Q, OECDQ) admit it. Kondratieff
(40--60y, need N>960 quarters \(\sim\) 240 years) is not testable on
quarterly at all.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from ecowave.cycles.surrogate import dual_null


BANDS = {
    "kitchin":     (3.0, 5.0),
    "juglar":      (7.0, 11.0),
    "kuznets":     (15.0, 25.0),
    "kondratieff": (40.0, 60.0),
}


# Quarterly aggregate / country codes worth testing. We exclude
# BIS_EM / BIS_AE composites (already covered by BoE/JST style runs in
# other scripts) but keep individual emerging-market BIS country codes
# for completeness.
Q_GROUPS = (
    "USA", "EA", "GBR", "JPN",
    "G7Q", "OECDQ",
    "BR_BIS", "CN_BIS", "IN_BIS", "KR_BIS", "MX_BIS",
    "RU_BIS", "TR_BIS", "ZA_BIS", "ID_BIS",
)

SAMPLES_PER_YEAR = 4


def load_quarterly_series(db_path: Path, groups: list[str]
                           ) -> dict[tuple[str, str], pd.Series]:
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    out: dict[tuple[str, str], list[tuple[int, int, float]]] = {}
    placeholders = ",".join("?" for _ in groups)
    query = f"""
        select group_code, variable_code, year, quarter, value
        from cycle_observations_quarterly
        where group_code in ({placeholders})
        order by group_code, variable_code, year, quarter
    """
    for group, var, year, quarter, value in cur.execute(query, groups):
        if value is None:
            continue
        out.setdefault((group, var), []).append((int(year), int(quarter), float(value)))
    series_map: dict[tuple[str, str], pd.Series] = {}
    for key, rows in out.items():
        idx = pd.PeriodIndex(
            [pd.Period(f"{y}Q{q}", freq="Q") for y, q, _ in rows]
        ).to_timestamp(how="start")
        values = [r[2] for r in rows]
        series_map[key] = pd.Series(values, index=idx,
                                     name=f"{key[0]}_{key[1]}")
    return series_map


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="/app/db/ecowave.db")
    parser.add_argument("--n-surrogates", type=int, default=300)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--groups", default=",".join(Q_GROUPS))
    parser.add_argument("--out",
                         default="reports/quarterly_per_variable.json")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"DB not found: {db_path}")
    groups = [g.strip() for g in args.groups.split(",") if g.strip()]
    series_map = load_quarterly_series(db_path, groups)
    print(f"Loaded {len(series_map)} (group, variable) quarterly series")

    cells = []
    for (group, var), series in sorted(series_map.items()):
        n = series.size
        if n < 16:  # cf_bandpass minimum
            continue
        period = f"{series.index.min().year}--{series.index.max().year}"
        for cycle, (lo, hi) in BANDS.items():
            min_n = int(4 * hi * SAMPLES_PER_YEAR)
            if n < min_n:
                cells.append({
                    "group": group, "variable": var, "cycle": cycle,
                    "n_obs": n, "panel_period": period, "p1": None,
                    "p_coh": None,
                    "skip_reason": f"n_obs < {min_n}"})
                continue
            try:
                d = dual_null(series, lo, hi,
                               samples_per_year=float(SAMPLES_PER_YEAR),
                               n_surrogates=args.n_surrogates,
                               seed=args.seed)
                cells.append({
                    "group": group, "variable": var, "cycle": cycle,
                    "n_obs": n, "panel_period": period,
                    "p1": float(d["ar1"].p_value),
                    "p_coh": float(d["phase_scramble"].p_value),
                    "reject_existence": bool(d["reject_cycle"])})
            except Exception as e:
                cells.append({
                    "group": group, "variable": var, "cycle": cycle,
                    "n_obs": n, "panel_period": period, "p1": None,
                    "p_coh": None, "skip_reason": str(e)})

    print()
    by_cycle: dict[str, list[float]] = {}
    for c in cells:
        if c.get("p1") is None:
            continue
        by_cycle.setdefault(c["cycle"], []).append(c["p1"])
    for cycle in ("kitchin", "juglar", "kuznets", "kondratieff"):
        ps = by_cycle.get(cycle, [])
        if not ps:
            continue
        n = len(ps)
        n_reject = sum(1 for p in ps if p < 0.05)
        expected = 0.05 * n
        med = float(np.median(ps))
        print(f"{cycle:12s}  N={n:4d}  median p1={med:.3f}  "
              f"detect={n_reject}/{n} (E[H0]={expected:.1f})")

    out = {
        "version": "v1",
        "db": str(db_path),
        "samples_per_year": SAMPLES_PER_YEAR,
        "n_surrogates": args.n_surrogates,
        "seed": args.seed,
        "groups_run": groups,
        "bands": BANDS,
        "cells": cells,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
