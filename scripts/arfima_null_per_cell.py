"""Gate 1 with the long-memory-aware ARFIMA(0, d_hat, 0) null.

Reruns Gate 1 on every per-variable cell with the AR(1) null *replaced*
by an ARFIMA(0, d_hat, 0) null whose d_hat is estimated by the
Geweke--Porter-Hudak log-periodogram method. The two p-values are
reported jointly so the reader can compare the AR(1)-conditional and
ARFIMA-conditional verdicts cell-by-cell.

Output: reports/arfima_null_per_cell.json
  -> list of cells with {panel, group, variable, cycle, d_hat,
                          p1_ar1, p1_arfima, gate1_ar1, gate1_arfima}

This is the empirical input for the R1 referee recommendation: cells
that pass AR(1) but fail ARFIMA should be downgraded; cells that pass
both gain credibility. The script supports a coarse default
(``--cycles juglar,kuznets``) and a full-grid mode.

Usage (inside Docker):

    python scripts/arfima_null_per_cell.py
    python scripts/arfima_null_per_cell.py --panels jst --cycles juglar
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ecowave.cycles.surrogate import ar1_bootstrap_null, arfima_bootstrap_null
from ecowave.cycles.surrogate_generators import estimate_d_gph
from ecowave.cycles.long_history import JST_VARS, load_jst
from ecowave.cycles.boe_millennium import load_boe_long_format


BANDS = {
    "kitchin":     (3.0, 5.0),
    "juglar":      (7.0, 11.0),
    "kuznets":     (15.0, 25.0),
    "kondratieff": (40.0, 60.0),
}


def _run_cell(series: pd.Series, lo: float, hi: float,
              samples_per_year: float, n_surrogates: int,
              seed: int) -> dict:
    y = series.dropna().astype(float).to_numpy()
    d_hat = float(estimate_d_gph(y)) if y.size >= 16 else 0.0
    ar1 = ar1_bootstrap_null(series, lo, hi, samples_per_year=samples_per_year,
                             n_surrogates=n_surrogates, seed=seed)
    arfima = arfima_bootstrap_null(series, lo, hi,
                                    samples_per_year=samples_per_year,
                                    n_surrogates=n_surrogates, seed=seed + 1,
                                    d_override=d_hat)
    return {
        "d_hat_gph": d_hat,
        "p1_ar1": ar1.p_value,
        "p1_arfima": arfima.p_value,
        "gate1_ar1": not ar1.reject_cycle,
        "gate1_arfima": not arfima.reject_cycle,
        "n_obs": int(y.size),
    }


def _iter_jst(xlsx_path: Path, start_year: int = 1870):
    jst = load_jst(xlsx_path)
    jst = jst[jst["year"] >= start_year]
    for country, grp in jst.groupby("country"):
        for cpv_code, (col_name, _label) in JST_VARS.items():
            if col_name not in grp.columns:
                continue
            ts = grp.sort_values("year")[col_name].dropna()
            if ts.size < 32:
                continue
            yield "JST_R6", country, cpv_code, ts, 1.0


def _iter_boe(csv_path: Path):
    long_df = load_boe_long_format(csv_path)
    for var_id, grp in long_df.groupby("variable_id"):
        ts = (grp.sort_values("year")
                 .drop_duplicates("year", keep="last")
                 .dropna(subset=["value"]))
        if ts.shape[0] < 32:
            continue
        yield "BoE_Millennium", "GBR", str(var_id), pd.Series(
            ts["value"].to_numpy(), index=ts["year"].to_numpy()), 1.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panels", default="jst,boe")
    parser.add_argument("--cycles", default="juglar,kuznets,kitchin,kondratieff")
    parser.add_argument("--jst-xlsx",
                        default="/app/data_raw/macrohistory/jst_r6.xlsx")
    parser.add_argument("--boe-csv",
                        default="/app/data_raw/boe/annual.csv")
    parser.add_argument("--n-surrogates", type=int, default=1000)
    parser.add_argument("--start-year", type=int, default=1870)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", default="reports/arfima_null_per_cell.json")
    args = parser.parse_args()

    panels = [p.strip().lower() for p in args.panels.split(",") if p.strip()]
    cycles = [c.strip().lower() for c in args.cycles.split(",") if c.strip() in BANDS]
    cells: list[dict] = []
    seed = args.seed

    for panel in panels:
        if panel == "jst":
            it = _iter_jst(Path(args.jst_xlsx), args.start_year)
        elif panel == "boe":
            it = _iter_boe(Path(args.boe_csv))
        else:
            print(f"Panel {panel}: skipped (loader not wired)")
            continue
        for panel_name, group, variable, ts, spy in it:
            for cycle in cycles:
                lo, hi = BANDS[cycle]
                if ts.size < 4 * hi:
                    continue
                seed += 2
                cell = _run_cell(ts, lo, hi, spy, args.n_surrogates, seed)
                cell.update({"panel": panel_name, "group": group,
                              "variable": variable, "cycle": cycle,
                              "band_lo": lo, "band_hi": hi})
                cells.append(cell)

    print(f"Computed {len(cells)} cells.")
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "n_cells": len(cells),
        "n_surrogates": args.n_surrogates,
        "method": "AR(1) vs ARFIMA(0, d_hat_GPH, 0) Gate 1 comparison",
        "cells": cells,
    }
    out_path.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
