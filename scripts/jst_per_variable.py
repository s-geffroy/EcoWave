"""Per-variable Gate 1 on the Jordà-Schularick-Taylor R6 panel.

Loads ``data_raw/macrohistory/jst_r6.xlsx`` via the project's existing
JST loader and runs the AR(1) bootstrap component of Gate 1 on each
(country, variable, cycle band) cell. Output:
``reports/jst_per_variable.json``, the empirical backing for the
JST R6 Kondratieff and Juglar claims of §5 Results and Appendix D.

To keep runtime tractable, the default uses ``B=200`` surrogates.
The result is qualitatively invariant for ``B>=100``; the BH-FDR
threshold is essentially set by the smallest cell p-value.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ecowave.cycles.long_history import JST_VARS, load_jst
from ecowave.cycles.surrogate import dual_null


BANDS = {
    "kitchin":     (3.0, 5.0),
    "juglar":      (7.0, 11.0),
    "kuznets":     (15.0, 25.0),
    "kondratieff": (40.0, 60.0),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xlsx",
                         default="/app/data_raw/macrohistory/jst_r6.xlsx")
    parser.add_argument("--start-year", type=int, default=1870)
    parser.add_argument("--n-surrogates", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--bands",
                         default="kondratieff,kuznets,juglar,kitchin",
                         help="comma-separated bands to test")
    parser.add_argument("--variables", default="",
                         help="comma-separated LH_ codes (default: all)")
    parser.add_argument("--countries", default="",
                         help="comma-separated ISO3 codes (default: all)")
    parser.add_argument("--out", default="reports/jst_per_variable.json")
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx)
    if not xlsx_path.exists():
        raise SystemExit(f"JST xlsx not found: {xlsx_path}")
    jst = load_jst(xlsx_path)
    jst = jst[jst["year"] >= args.start_year]

    bands_to_run = [b.strip() for b in args.bands.split(",") if b.strip() in BANDS]
    var_filter = [v.strip() for v in args.variables.split(",") if v.strip()]
    var_codes = var_filter if var_filter else list(JST_VARS.keys())
    countries_filter = [c.strip() for c in args.countries.split(",") if c.strip()]
    countries = countries_filter if countries_filter else sorted(jst["country"].unique())

    print(f"JST R6 loaded: {len(jst)} rows, {len(countries)} countries, "
          f"{len(var_codes)} variables, {len(bands_to_run)} bands")
    print(f"Running ~{len(countries) * len(var_codes) * len(bands_to_run)} cells...")

    cells = []
    cell_count = 0
    for var_code in var_codes:
        if var_code not in JST_VARS:
            continue
        jst_col, _ = JST_VARS[var_code]
        if jst_col not in jst.columns:
            continue
        for country in countries:
            sub = jst[(jst["country"] == country)].copy()
            if sub.empty or jst_col not in sub.columns:
                continue
            sub[jst_col] = pd.to_numeric(sub[jst_col], errors="coerce")
            sub = sub.dropna(subset=[jst_col]).sort_values("year")
            if sub.empty:
                continue
            idx = pd.to_datetime(sub["year"].astype(int).astype(str) + "-01-01")
            series = pd.Series(sub[jst_col].to_numpy(), index=idx)
            n = series.size
            period = f"{series.index.min().year}--{series.index.max().year}"
            for cycle in bands_to_run:
                lo, hi = BANDS[cycle]
                if n < 4 * hi:
                    continue
                try:
                    d = dual_null(series, lo, hi, samples_per_year=1.0,
                                   n_surrogates=args.n_surrogates,
                                   seed=args.seed)
                    cells.append({
                        "country": country, "variable": var_code,
                        "cycle": cycle, "n_obs": n, "panel_period": period,
                        "p1": float(d["ar1"].p_value),
                        "p_coh": float(d["phase_scramble"].p_value),
                        "reject_existence": bool(d["reject_cycle"])})
                    cell_count += 1
                    if cell_count % 200 == 0:
                        print(f"  {cell_count} cells done")
                except Exception as e:
                    cells.append({
                        "country": country, "variable": var_code,
                        "cycle": cycle, "n_obs": n, "panel_period": period,
                        "p1": None, "p_coh": None, "skip_reason": str(e)})

    # Summary
    print()
    by_cycle: dict[str, list[float]] = {}
    for c in cells:
        if c.get("p1") is None:
            continue
        by_cycle.setdefault(c["cycle"], []).append(c["p1"])
    for cycle in ("kitchin", "juglar", "kuznets", "kondratieff"):
        ps = by_cycle.get(cycle, [])
        n = len(ps)
        if n == 0:
            continue
        n_reject = sum(1 for p in ps if p < 0.05)
        med = float(np.median(ps))
        expected = 0.05 * n
        print(f"{cycle:12s}  N={n:4d}  median p1={med:.3f}  "
              f"detect={n_reject}/{n} (E[H0]={expected:.1f})")

    out = {
        "version": "v1",
        "xlsx": str(xlsx_path),
        "start_year": args.start_year,
        "n_surrogates": args.n_surrogates,
        "seed": args.seed,
        "bands_run": bands_to_run,
        "variables_run": var_codes,
        "countries_run": countries,
        "cells": cells,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
