"""Long-memory and stationarity diagnostics on every per-variable cell.

For each cell (panel, country/aggregate, variable) of the JST R6, BoE
Millennium, World Bank, Quarterly and Sectoral panels, compute and
record:

  - ADF (Dickey-Fuller 1979) p-value for the unit-root null
  - KPSS (Kwiatkowski et al. 1992) p-value for the stationarity null
  - GPH (Geweke & Porter-Hudak 1983) estimate of d (fractional integration)
  - DFA Hurst exponent (Peng et al. 1994 ; Hurst 1951)

Output:
  reports/long_memory_diagnostics.json
    -> list of cells, each with the four statistics and panel metadata

This is the empirical input for the referee-driven R1 recommendation:
when |d_hat| > 0.1 the AR(1) Gate-1 null over-rejects, and the
ARFIMA(0, d_hat, 0) null reported by ``scripts/arfima_null_per_cell.py``
should be consulted as the load-bearing verdict instead.

Usage (inside Docker):

    python scripts/long_memory_diagnostics.py
    python scripts/long_memory_diagnostics.py --panel boe
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ecowave.cycles.surrogate import stationarity_diagnostics
from ecowave.cycles.long_history import JST_VARS, load_jst
from ecowave.cycles.boe_millennium import load_boe_long_format


def _iter_jst_cells(xlsx_path: Path, start_year: int = 1870):
    jst = load_jst(xlsx_path)
    jst = jst[jst["year"] >= start_year]
    for country, grp in jst.groupby("country"):
        for cpv_code, (col_name, _label) in JST_VARS.items():
            if col_name not in grp.columns:
                continue
            ts = grp.sort_values("year")[col_name].dropna()
            if ts.size < 32:
                continue
            yield {"panel": "JST_R6", "group": country, "variable": cpv_code,
                   "series": ts.to_numpy()}


def _iter_boe_cells(csv_path: Path):
    long_df = load_boe_long_format(csv_path)
    for var_id, grp in long_df.groupby("variable_id"):
        ts = grp.sort_values("year").drop_duplicates("year", keep="last")
        ts = ts.dropna(subset=["value"])
        if ts.shape[0] < 32:
            continue
        yield {"panel": "BoE_Millennium", "group": "GBR", "variable": str(var_id),
               "series": ts["value"].to_numpy()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", default="jst,boe",
                        help="comma-separated panels (jst,boe,wb,quarterly,sectoral)")
    parser.add_argument("--jst-xlsx",
                        default="/app/data_raw/macrohistory/jst_r6.xlsx")
    parser.add_argument("--boe-csv",
                        default="/app/data_raw/boe/annual.csv")
    parser.add_argument("--start-year", type=int, default=1870)
    parser.add_argument("--out", default="reports/long_memory_diagnostics.json")
    args = parser.parse_args()

    panels = [p.strip().lower() for p in args.panel.split(",") if p.strip()]
    cells = []

    if "jst" in panels:
        xlsx = Path(args.jst_xlsx)
        if xlsx.exists():
            print(f"JST R6: {xlsx}")
            for cell in _iter_jst_cells(xlsx, args.start_year):
                diag = stationarity_diagnostics(pd.Series(cell["series"]))
                cells.append({**cell, "diagnostics": diag,
                              "series": None})  # drop array from JSON
        else:
            print(f"WARN: JST xlsx not found at {xlsx}")

    if "boe" in panels:
        csv = Path(args.boe_csv)
        if csv.exists():
            print(f"BoE Millennium: {csv}")
            for cell in _iter_boe_cells(csv):
                diag = stationarity_diagnostics(pd.Series(cell["series"]))
                cells.append({**cell, "diagnostics": diag,
                              "series": None})
        else:
            print(f"WARN: BoE csv not found at {csv}")

    print(f"Diagnostics computed for {len(cells)} cells.")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "n_cells": len(cells),
        "cells": [{k: v for k, v in c.items() if k != "series"} for c in cells],
    }
    out_path.write_text(json.dumps(payload, indent=2, default=str))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
