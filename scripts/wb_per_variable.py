"""Per-variable Gate 1 on the World Bank annual panel.

Loads the already-ingested WB series from db/ecowave.db (table
``cycle_observations``) and runs the AR(1) bootstrap component of
Gate 1 on each (group, variable, cycle band) cell. Output:
``reports/wb_per_variable.json`` — the empirical backing for the
WB Kitchin / Juglar / Kuznets / Kondratieff claims of §5 Results.

Kondratieff cannot be tested at all on the WB panel either: the
1960--2025 window yields at most ~65 annual observations, well
short of our threshold ``N > 4 * 60 = 240``. The WB verdict
therefore covers Kitchin, Juglar and Kuznets only.
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

# The 7 income-stratified / regional aggregates used as the WB panel.
WB_GROUPS = ("WLD", "OECD", "HIC", "UMC", "LMC", "LIC", "BRICS")


def load_wb_series(db_path: Path, groups: list[str]) -> dict[tuple[str, str], pd.Series]:
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    out: dict[tuple[str, str], pd.Series] = {}
    placeholders = ",".join("?" for _ in groups)
    query = f"""
        select group_code, variable_code, year, value
        from cycle_observations
        where group_code in ({placeholders})
        order by group_code, variable_code, year
    """
    for group, var, year, value in cur.execute(query, groups):
        if value is None:
            continue
        key = (group, var)
        out.setdefault(key, []).append((year, float(value)))
    # Build pandas Series
    series_map: dict[tuple[str, str], pd.Series] = {}
    for key, rows in out.items():
        years = [r[0] for r in rows]
        values = [r[1] for r in rows]
        idx = pd.to_datetime([f"{y}-01-01" for y in years])
        series_map[key] = pd.Series(values, index=idx, name=f"{key[0]}_{key[1]}")
    return series_map


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="/app/db/ecowave.db")
    parser.add_argument("--n-surrogates", type=int, default=500)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--groups", default=",".join(WB_GROUPS))
    parser.add_argument("--out", default="reports/wb_per_variable.json")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"DB not found: {db_path}")
    groups = [g.strip() for g in args.groups.split(",") if g.strip()]
    series_map = load_wb_series(db_path, groups)
    print(f"Loaded {len(series_map)} (group, variable) series from {db_path}")

    cells = []
    for (group, var), series in sorted(series_map.items()):
        n = series.size
        if n < 30:
            continue
        period = f"{series.index.min().year}--{series.index.max().year}"
        for cycle, (lo, hi) in BANDS.items():
            if n < 4 * hi:
                cells.append({
                    "group": group, "variable": var, "cycle": cycle,
                    "n_obs": n, "panel_period": period, "p1": None,
                    "p_coh": None, "skip_reason": "n_obs < 4*hi_years"})
                continue
            try:
                d = dual_null(series, lo, hi, samples_per_year=1.0,
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

    # Summary
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
        median = float(np.median(ps))
        print(f"{cycle:12s}  N={n:4d}  median p1={median:.3f}  "
              f"detect={n_reject}/{n} (E[H0]={expected:.1f})")

    out = {
        "version": "v1",
        "db": str(db_path),
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
