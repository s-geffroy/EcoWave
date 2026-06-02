"""Measure pairwise phase agreement of cycle estimators on null AR(1) panels.

The paper (App. C) claims that the four Gate 2 estimators are not
statistically independent: "pairwise phase agreement on null AR(1)
panels is in the range [0.42, 0.61]". This script provides the
empirical backing for that claim using two cheap estimators
(CF + Hilbert phase classifier; sign-of-velocity from a smoothed
band-passed series, a Bry-Boschan-style proxy).

The script is intentionally small: it pairs two estimators that share
some code path and one that doesn't, and runs them on N=200 null AR(1)
panels of length T=150 (matching JST R6). It is a calibration
artefact, not a substitute for the full four-method comparison which
would require running the heavier MS-AR(1) and PELT fits.

Output: reports/estimator_pairwise_v1.json
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from ecowave.cycles.decompose import cf_bandpass
from ecowave.cycles.phase import classify_phase, hilbert_phase


def _ar1(phi: float, sigma: float, n: int, rng: np.random.Generator) -> np.ndarray:
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = phi * y[t - 1] + rng.normal(scale=sigma)
    return y


def estimator_cf_hilbert(y: np.ndarray, lo_years: float,
                          hi_years: float) -> list[str]:
    bp = cf_bandpass(pd.Series(y), lo_years, hi_years,
                     samples_per_year=1.0).dropna()
    if bp.empty:
        return ["rejected"] * y.size
    phi = hilbert_phase(bp)
    labels = [classify_phase(p) for p in phi.values]
    # Pad to length n by repeating last label for trimmed edges.
    pad = y.size - len(labels)
    return list(labels) + [labels[-1]] * max(pad, 0)


def estimator_sign_of_velocity(y: np.ndarray, lo_years: float,
                                hi_years: float) -> list[str]:
    """Quick Bry-Boschan-style proxy: ascending = expansion-or-peak,
    descending = contraction-or-trough; refined by the sign of the second
    derivative.
    """
    bp = cf_bandpass(pd.Series(y), lo_years, hi_years,
                     samples_per_year=1.0).dropna().to_numpy()
    if bp.size < 3:
        return ["rejected"] * y.size
    d1 = np.gradient(bp)
    d2 = np.gradient(d1)
    labels = []
    for v, a in zip(d1, d2):
        if v > 0 and a < 0:
            labels.append("expansion")
        elif v > 0 and a > 0:
            labels.append("trough")  # turning up
        elif v < 0 and a < 0:
            labels.append("peak")  # turning down
        else:
            labels.append("contraction")
    pad = y.size - len(labels)
    return list(labels) + [labels[-1]] * max(pad, 0)


def pairwise_agreement(labels_a: list[str], labels_b: list[str]) -> float:
    n = min(len(labels_a), len(labels_b))
    if n == 0:
        return float("nan")
    agree = sum(1 for i in range(n) if labels_a[i] == labels_b[i])
    return agree / n


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-panels", type=int, default=200)
    parser.add_argument("--t-len", type=int, default=150)
    parser.add_argument("--phi", type=float, default=0.5,
                         help="AR(1) persistence of the null panel")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out",
                         default="reports/estimator_pairwise_v1.json")
    args = parser.parse_args()

    band = (7.0, 11.0)  # Juglar
    t0 = time.time()
    agreements_cf_sov: list[float] = []
    rng_master = np.random.default_rng(args.seed)
    for i in range(args.n_panels):
        rng = np.random.default_rng(int(rng_master.integers(0, 2**31)))
        y = _ar1(args.phi, 1.0, args.t_len, rng)
        a = estimator_cf_hilbert(y, *band)
        b = estimator_sign_of_velocity(y, *band)
        agreements_cf_sov.append(pairwise_agreement(a, b))
    elapsed = time.time() - t0
    mean_agreement = float(np.mean(agreements_cf_sov))
    median_agreement = float(np.median(agreements_cf_sov))
    print(f"CF+Hilbert vs sign-of-velocity (Bry-Boschan-style) — "
          f"AR(1) null, phi={args.phi}, T={args.t_len}, N={args.n_panels}")
    print(f"  mean agreement = {mean_agreement:.3f}")
    print(f"  median agreement = {median_agreement:.3f}")
    print(f"  ({elapsed:.1f}s)")

    output = {
        "version": "v1",
        "n_panels": args.n_panels,
        "t_len": args.t_len,
        "phi_null": args.phi,
        "band_lo_years": band[0],
        "band_hi_years": band[1],
        "pairs": [
            {
                "left": "cf_hilbert",
                "right": "sign_of_velocity",
                "mean_agreement": mean_agreement,
                "median_agreement": median_agreement,
                "agreement_distribution": agreements_cf_sov,
            }
        ],
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(output, f, indent=2)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
