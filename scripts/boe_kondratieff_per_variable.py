"""Per-variable Gate 1 on the Bank of England Millennium UK annual panel.

Loads ``data_raw/boe/annual.csv`` (long-format CSV: year, variable_id,
variable, section, unit, value), filters to the variable codes named
in ``boe_millennium_manifest.json``, and runs the AR(1) bootstrap
component of Gate 1 on each (variable, cycle band) cell. Output:
``reports/boe_per_variable.json``, the empirical backing of
Appendix D.4 of the paper.

The script truncates each series at 1700 (the manifest's
``start_year``); pre-1700 BoE data is benchmark-interpolated and the
project policy is to use 1700 as the continuous-reliability start.
"""
from __future__ import annotations

import argparse
import json
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


# Subset of variable codes from boe_millennium_manifest.json. We pick
# the BoE ids that are stable string identifiers in the long-format CSV.
BOE_VARIABLES: dict[str, str] = {
    "BOE_GDP":      "real-uk-gdp-at-market-prices-geographically-consistent",
    "BOE_GDP_LONG": "composite-estimate-of-english-and-geographically-consistent",
    "BOE_CPI":      "consumer-price-index",
    "BOE_WPI":      "wholesale-producer-price-index",
    "BOE_STIR":     "bank-rate",
    "BOE_YIELD":    "consols-long-term-government-bond-yields",
    "BOE_DEBTGDP":  "uk-public-sector-debt",
    "BOE_EQUITY":   "share-prices",
    "BOE_POP":      "population-gb-ni",
    "BOE_MONEY":    "broad-money",
    "BOE_CREDIT":   "credit",
    "BOE_HPI":      "house-price-index",
    "BOE_INV":      "real-investment",
    "BOE_UNRATE":   "unemployment-rate",
    "BOE_RCONS":    "real-consumption",
    "BOE_PRD":      "labour-productivity",
}


def load_boe_annual(csv_path: Path, start_year: int) -> dict[str, pd.Series]:
    df = pd.read_csv(csv_path, dtype={"variable_id": str})
    df = df[df["year"] >= start_year]
    out: dict[str, pd.Series] = {}
    for code, vid in BOE_VARIABLES.items():
        sub = df[df["variable_id"] == vid].copy()
        if sub.empty:
            continue
        sub["value"] = pd.to_numeric(sub["value"], errors="coerce")
        sub = sub.dropna(subset=["value"]).sort_values("year")
        if sub.empty:
            continue
        idx = pd.to_datetime(sub["year"].astype(int).astype(str) + "-01-01")
        s = pd.Series(sub["value"].to_numpy(), index=idx, name=code)
        out[code] = s
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="/app/data_raw/boe/annual.csv")
    parser.add_argument("--start-year", type=int, default=1700)
    parser.add_argument("--n-surrogates", type=int, default=500,
                        help="500 (default) for headline; 20000 for "
                             "BH-FDR-compatible p-value resolution.")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out",
                         default="reports/boe_per_variable.json")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"BoE CSV not found: {csv_path}")
    variables = load_boe_annual(csv_path, args.start_year)
    print(f"Loaded {len(variables)} BoE variables from {csv_path}")

    cells = []
    for code, series in sorted(variables.items()):
        n = series.size
        period = f"{series.index.min().year}--{series.index.max().year}"
        for cycle, (lo, hi) in BANDS.items():
            if n < 4 * hi:
                cells.append({
                    "variable": code, "cycle": cycle, "n_obs": n,
                    "panel_period": period, "p1": None, "p_coh": None,
                    "skip_reason": "n_obs < 4*hi_years"})
                continue
            try:
                d = dual_null(series, lo, hi, samples_per_year=1.0,
                               n_surrogates=args.n_surrogates,
                               seed=args.seed)
                cells.append({
                    "variable": code, "cycle": cycle, "n_obs": n,
                    "panel_period": period,
                    "p1": float(d["ar1"].p_value),
                    "p_coh": float(d["phase_scramble"].p_value),
                    "reject_existence": bool(d["reject_cycle"])})
            except Exception as e:
                cells.append({
                    "variable": code, "cycle": cycle, "n_obs": n,
                    "panel_period": period, "p1": None, "p_coh": None,
                    "skip_reason": str(e)})

    print()
    by_cycle: dict[str, list[float]] = {}
    for c in cells:
        if c["p1"] is None:
            continue
        by_cycle.setdefault(c["cycle"], []).append(c["p1"])
    for cycle in ("kitchin", "juglar", "kuznets", "kondratieff"):
        ps = by_cycle.get(cycle, [])
        n = len(ps)
        n_reject = sum(1 for p in ps if p < 0.05)
        med = float(np.median(ps)) if ps else float("nan")
        print(f"{cycle:12s}  median p1={med:.3f}  detect={n_reject}/{n}")

    result = {
        "version": "v1",
        "csv": str(csv_path),
        "start_year": args.start_year,
        "n_surrogates": args.n_surrogates,
        "seed": args.seed,
        "bands": BANDS,
        "variables": list(sorted(variables.keys())),
        "cells": cells,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
