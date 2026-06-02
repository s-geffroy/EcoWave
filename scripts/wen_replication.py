"""Empirical Wen (2005) replication on the sectoral panel.

Loads each sectoral CSV directly (no DB ingestion) and runs the AR(1)
bootstrap Gate 1 on the four canonical cycle bands. Output: a JSON
sidecar that backs Table D.3 of the paper.

Why not the full position-cycles pipeline? That pipeline fits the
four Gate 2 estimators and computes consensus; we only need Gate 1
existence per variable here, which is much cheaper.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from ecowave.cycles.surrogate import ar1_bootstrap_null, dual_null


BANDS = {
    "kitchin":     (3.0, 5.0),
    "juglar":      (7.0, 11.0),
    "kuznets":     (15.0, 25.0),
    "kondratieff": (40.0, 60.0),
}


def _load_fred_csv(path: Path) -> pd.Series:
    """FRED single-series CSV: DATE column, one value column."""
    df = pd.read_csv(path)
    date_col = [c for c in df.columns if c.lower().startswith("date") or c.lower() == "observation_date"][0]
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col]).sort_values(date_col)
    val_col = [c for c in df.columns if c != date_col][0]
    s = pd.to_numeric(df[val_col], errors="coerce")
    s.index = df[date_col]
    s.name = path.stem
    return s.dropna()


def _annualise(series: pd.Series) -> pd.Series:
    """Resample to annual frequency by taking the yearly mean."""
    if series.empty:
        return series
    return series.resample("Y").mean().dropna()


def _load_owid_csv(path: Path, entity: str, value_col: str) -> pd.Series:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    # Long format: Entity / Year / value_col
    if "Entity" in df.columns and "Year" in df.columns:
        sub = df[df["Entity"] == entity]
        idx = pd.to_datetime(sub["Year"].astype(int).astype(str) + "-01-01")
        s = pd.to_numeric(sub[value_col], errors="coerce")
        s.index = idx
        return s.dropna()
    raise ValueError(f"unrecognised OWID layout: {path}")


def _load_owid_wide(path: Path, value_col: str) -> pd.Series:
    """OWID legacy 'wide' CSV: Year column + columns per dataset."""
    df = pd.read_csv(path)
    if "Year" in df.columns and value_col in df.columns:
        idx = pd.to_datetime(df["Year"].astype(int).astype(str) + "-01-01")
        s = pd.to_numeric(df[value_col], errors="coerce")
        s.index = idx
        return s.dropna()
    raise ValueError(f"missing {value_col} in {path}")


def _splice(*series: pd.Series) -> pd.Series:
    """Concatenate series taking later observations where overlap occurs."""
    out = pd.Series(dtype=float)
    for s in series:
        if s.empty:
            continue
        s = s[~s.index.duplicated()]
        out = pd.concat([out, s[~s.index.isin(out.index)]])
    return out.sort_index()


def load_sectoral_variables(data_dir: Path) -> dict[str, pd.Series]:
    """Return {variable_code: annual-frequency series} for the sectoral panel."""
    out: dict[str, pd.Series] = {}

    def f(name: str) -> Path:
        return data_dir / name

    try:
        nber = _load_fred_csv(f("us_wpi_nber_1860_1939.csv"))
        bls = _load_fred_csv(f("us_wpi_bls_1913_now.csv"))
        out["SH_US_WPI"] = _annualise(_splice(nber, bls))
    except Exception:
        pass

    for code, csv in [
        ("SH_US_INDPROD", "us_indprod_1919_now.csv"),
        ("SH_US_COAL", "us_coal_1856_1958.csv"),
        ("SH_US_PIGIRON", "us_pigiron_1941_1964.csv"),
        ("SH_US_RAILFREIGHT", "us_railfreight_1866_1922.csv"),
        ("SH_US_WHEAT", "us_wheat_1866_1952.csv"),
        ("SH_US_COTTON", "us_cotton_1912_1961.csv"),
    ]:
        try:
            out[code] = _annualise(_load_fred_csv(f(csv)))
        except Exception:
            pass

    try:
        a = _load_fred_csv(f("us_steel_1863_1919.csv"))
        b = _load_fred_csv(f("us_steel_ingot_1932_1965.csv"))
        out["SH_US_STEEL"] = _annualise(_splice(a, b))
    except Exception:
        pass

    try:
        out["SH_UK_COAL"] = _load_owid_wide(
            f("uk_coal_beis_1700_2019.csv"),
            value_col="Coal Output (DECC (2018))")
    except Exception:
        pass

    for code, csv, ent, vcol in [
        ("SH_WORLD_COAL", "world_coal_owid.csv", "World", "Coal"),
        ("SH_WORLD_OIL", "world_oil_owid.csv", "World", "Oil"),
    ]:
        try:
            out[code] = _load_owid_csv(f(csv), entity=ent, value_col=vcol)
        except Exception:
            pass

    # Keep only series with at least 30 annual observations
    return {k: s for k, s in out.items() if s.size >= 30}


def run_wen_replication(data_dir: Path, n_surrogates: int, seed: int) -> dict:
    variables = load_sectoral_variables(data_dir)
    print(f"Loaded {len(variables)} sectoral variables")
    cells = []
    for code, series in sorted(variables.items()):
        n = series.size
        period = (
            f"{series.index.min().year}--{series.index.max().year}")
        for cycle, (lo, hi) in BANDS.items():
            if n < 4 * hi:
                # Series too short relative to the band; record skip.
                cells.append({
                    "variable": code, "cycle": cycle, "n_obs": n,
                    "panel_period": period, "p1": None, "p_coh": None,
                    "skip_reason": "n_obs < 4*hi_years"})
                continue
            try:
                d = dual_null(series, lo, hi, samples_per_year=1.0,
                               n_surrogates=n_surrogates, seed=seed)
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
    return {
        "version": "v1",
        "n_surrogates": n_surrogates,
        "seed": seed,
        "bands": BANDS,
        "variables": list(sorted(variables.keys())),
        "cells": cells,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir",
                         default="/app/data_raw/sectoral_history")
    parser.add_argument("--n-surrogates", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out",
                         default="reports/wen_replication_per_variable.json")
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        raise SystemExit(f"data dir not found: {data_dir}")
    result = run_wen_replication(data_dir, args.n_surrogates, args.seed)
    # Summary
    by_cycle = {}
    for c in result["cells"]:
        if c["p1"] is None:
            continue
        by_cycle.setdefault(c["cycle"], []).append(c["p1"])
    print()
    for cycle, ps in sorted(by_cycle.items()):
        n = len(ps)
        n_reject_null = sum(1 for p in ps if p < 0.05)
        med = float(np.median(ps)) if ps else float("nan")
        print(f"{cycle:12s}  median p1={med:.3f}  detect={n_reject_null}/{n}")
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
