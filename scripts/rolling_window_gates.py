"""Gate 1 verdicts on rolling windows — temporal-stability map.

The referee critique R5 noted that the window-sensitivity reported in
the paper (1870-2007 vs 1870-2020 on JST; 1700-1945 vs 1700-2016 on
BoE) is too coarse to detect a cycle that lives in one epoch but is
absent in another (Belle Epoque vs Trente Glorieuses vs post-2008).

This script runs Gate 1 on rolling windows of fixed length (default 50
years on annual panels, 80 years for Kondratieff) with a configurable
step (default 25 years). The output is a panel of (panel, group,
variable, cycle, window_start, window_end, p1, gate1) cells suitable
for a heat-map of cycle presence across history.

Output: reports/rolling_window_gates.json

Usage (inside Docker):

    python scripts/rolling_window_gates.py --panels jst,boe \
        --window 50 --step 25
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ecowave.cycles.surrogate import ar1_bootstrap_null
from ecowave.cycles.long_history import JST_VARS, load_jst
from ecowave.cycles.boe_millennium import load_boe_long_format


BANDS = {
    "kitchin":     (3.0, 5.0),
    "juglar":      (7.0, 11.0),
    "kuznets":     (15.0, 25.0),
    "kondratieff": (40.0, 60.0),
}

# Minimum window per cycle: ~5x the upper band edge so the spectral
# resolution can resolve it.
MIN_WINDOWS = {
    "kitchin":     30,
    "juglar":      50,
    "kuznets":     100,
    "kondratieff": 200,
}


def _iter_jst(xlsx_path: Path, start_year: int = 1870):
    jst = load_jst(xlsx_path)
    jst = jst[jst["year"] >= start_year]
    for country, grp in jst.groupby("country"):
        for cpv_code, (col_name, _label) in JST_VARS.items():
            if col_name not in grp.columns:
                continue
            sub = grp.sort_values("year")[["year", col_name]].dropna()
            if sub.shape[0] < 32:
                continue
            yield "JST_R6", country, cpv_code, sub.rename(
                columns={col_name: "value"}), 1.0


def _iter_boe(csv_path: Path):
    long_df = load_boe_long_format(csv_path)
    for var_id, grp in long_df.groupby("variable_id"):
        sub = (grp.sort_values("year")
                  .drop_duplicates("year", keep="last")
                  .dropna(subset=["value"])
                  [["year", "value"]])
        if sub.shape[0] < 32:
            continue
        yield "BoE_Millennium", "GBR", str(var_id), sub, 1.0


def _windows(years: np.ndarray, window: int, step: int):
    y_min, y_max = int(years.min()), int(years.max())
    start = y_min
    while start + window - 1 <= y_max:
        yield start, start + window - 1
        start += step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panels", default="jst,boe")
    parser.add_argument("--cycles", default="juglar,kuznets,kitchin,kondratieff")
    parser.add_argument("--jst-xlsx",
                        default="/app/data_raw/macrohistory/jst_r6.xlsx")
    parser.add_argument("--boe-csv",
                        default="/app/data_raw/boe/annual.csv")
    parser.add_argument("--n-surrogates", type=int, default=300)
    parser.add_argument("--window", type=int, default=50,
                        help="default rolling window length in years")
    parser.add_argument("--step", type=int, default=25)
    parser.add_argument("--start-year", type=int, default=1700)
    parser.add_argument("--out", default="reports/rolling_window_gates.json")
    args = parser.parse_args()

    panels = [p.strip().lower() for p in args.panels.split(",") if p.strip()]
    cycles = [c.strip().lower() for c in args.cycles.split(",") if c.strip() in BANDS]
    cells: list[dict] = []
    seed = 0

    for panel in panels:
        if panel == "jst":
            it = _iter_jst(Path(args.jst_xlsx), args.start_year)
        elif panel == "boe":
            it = _iter_boe(Path(args.boe_csv))
        else:
            print(f"Panel {panel}: skipped (loader not wired)")
            continue
        for panel_name, group, variable, sub, spy in it:
            years = sub["year"].to_numpy()
            values = sub["value"].to_numpy()
            for cycle in cycles:
                lo, hi = BANDS[cycle]
                window_len = max(args.window, MIN_WINDOWS[cycle])
                for w_lo, w_hi in _windows(years, window_len, args.step):
                    mask = (years >= w_lo) & (years <= w_hi)
                    if mask.sum() < MIN_WINDOWS[cycle]:
                        continue
                    seed += 1
                    res = ar1_bootstrap_null(pd.Series(values[mask]),
                                              lo, hi,
                                              samples_per_year=spy,
                                              n_surrogates=args.n_surrogates,
                                              seed=seed)
                    cells.append({
                        "panel": panel_name, "group": group,
                        "variable": variable, "cycle": cycle,
                        "window_start": int(w_lo), "window_end": int(w_hi),
                        "n_obs": int(mask.sum()),
                        "p1": res.p_value, "gate1": not res.reject_cycle,
                    })

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "n_cells": len(cells),
        "n_surrogates": args.n_surrogates,
        "window_default": args.window,
        "step": args.step,
        "min_windows_per_cycle": MIN_WINDOWS,
        "cells": cells,
    }
    out_path.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {out_path} ({len(cells)} cells)")


if __name__ == "__main__":
    main()
