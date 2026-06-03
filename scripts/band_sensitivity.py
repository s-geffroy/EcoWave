"""Sensitivity of Gate 1 verdicts to the canonical band edges.

For each canonical cycle, the band is anchored to the prior empirical
literature: Kitchin [3,5], Juglar [7,11], Kuznets [15,25], Kondratieff
[40,60]. The referee critique R4 asked: do the headline pass-rates
survive perturbation of the band edges by +/- 1 year (or +/- 1 quarter
for the quarterly panel)? Without this test the "threshold transparency"
commitment carries no statistical power.

This script reruns Gate 1 (AR(1) bootstrap) on each cell for a grid of
perturbed bands and reports the pass-rate at every (cycle, band variant)
combination.

Output: reports/band_sensitivity.json with, for each (panel, cycle):
  - the anchor band and pass-rate
  - 4 perturbations per cycle: tighten lo, loosen lo, tighten hi, loosen hi
  - 2 widened "extreme" perturbations: [lo-2, hi+2]

Usage (inside Docker):

    python scripts/band_sensitivity.py --panels jst,boe
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


ANCHOR_BANDS = {
    "kitchin":     (3.0, 5.0),
    "juglar":      (7.0, 11.0),
    "kuznets":     (15.0, 25.0),
    "kondratieff": (40.0, 60.0),
}


def _perturbed_bands(cycle: str) -> dict[str, tuple[float, float]]:
    lo, hi = ANCHOR_BANDS[cycle]
    delta = 1.0 if cycle in ("kitchin", "juglar") else 2.0
    return {
        "anchor":     (lo, hi),
        "tighten_lo": (lo + delta, hi),
        "loosen_lo":  (lo - delta, hi),
        "tighten_hi": (lo, hi - delta),
        "loosen_hi":  (lo, hi + delta),
        "widen":      (lo - delta, hi + delta),
        "narrow":     (lo + delta, hi - delta),
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
    parser.add_argument("--n-surrogates", type=int, default=500)
    parser.add_argument("--start-year", type=int, default=1870)
    parser.add_argument("--out", default="reports/band_sensitivity.json")
    args = parser.parse_args()

    panels = [p.strip().lower() for p in args.panels.split(",") if p.strip()]
    cycles = [c.strip().lower() for c in args.cycles.split(",")
              if c.strip() in ANCHOR_BANDS]
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
        for panel_name, group, variable, ts, spy in it:
            for cycle in cycles:
                for tag, (lo, hi) in _perturbed_bands(cycle).items():
                    if lo <= 0 or hi <= lo or ts.size < 4 * hi:
                        continue
                    seed += 1
                    res = ar1_bootstrap_null(ts, lo, hi,
                                              samples_per_year=spy,
                                              n_surrogates=args.n_surrogates,
                                              seed=seed)
                    cells.append({
                        "panel": panel_name, "group": group,
                        "variable": variable, "cycle": cycle,
                        "perturbation": tag, "band_lo": lo, "band_hi": hi,
                        "p1": res.p_value, "gate1": not res.reject_cycle,
                        "n_obs": int(ts.size),
                    })

    # Aggregate pass rates by (panel, cycle, perturbation).
    rows = pd.DataFrame(cells)
    if not rows.empty:
        agg = (rows.groupby(["panel", "cycle", "perturbation"])
                   .agg(n_cells=("gate1", "size"),
                        n_pass=("gate1", "sum"),
                        median_p1=("p1", "median"),
                        median_n_obs=("n_obs", "median"))
                   .reset_index())
        agg["pass_rate"] = agg["n_pass"] / agg["n_cells"]
        summary = agg.to_dict(orient="records")
    else:
        summary = []

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "n_cells": len(cells),
        "n_surrogates": args.n_surrogates,
        "anchor_bands": ANCHOR_BANDS,
        "summary": summary,
        "cells": cells,
    }
    out_path.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {out_path} ({len(cells)} cells, {len(summary)} aggregates)")


if __name__ == "__main__":
    main()
