"""Empirical calibration of the dual-null Gate 1 protocol.

Runs N replicates of synthetic series under three families of generative
alternatives, applies Gate 1 (AR(1) + phase-coherence dual null), and
records the empirical detection power at each signal-to-noise ratio.

Output: reports/calibration_v1.json with per-(family, SNR) rejection
rates. The paper Appendix B references this file.

Usage (inside the docker container):

    python scripts/calibrate_dual_null.py --n-replicates 100 --n-surrogates 200
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

from ecowave.cycles.surrogate import dual_null


# ============================================================
# Generative families
# ============================================================


def gen_ar1_plus_cosine(t: np.ndarray, period: float, snr: float,
                        rng: np.random.Generator,
                        phi: float = 0.5) -> np.ndarray:
    """Family I: AR(1) noise + sinusoid in the canonical band.

    SNR is the variance share of the cosine component:
        SNR = var(cosine) / (var(cosine) + var(noise))
    """
    n = t.size
    sigma_noise = 1.0
    noise = np.zeros(n)
    for i in range(1, n):
        noise[i] = phi * noise[i - 1] + rng.normal(scale=sigma_noise)
    # Noise has theoretical variance sigma^2 / (1-phi^2)
    var_noise = sigma_noise ** 2 / (1.0 - phi ** 2)
    # cos has variance amp^2 / 2; choose amp so amp^2/2 / (amp^2/2 + var_noise) = snr
    amp_sq = 2.0 * snr * var_noise / max(1.0 - snr, 1e-6)
    amp = np.sqrt(amp_sq)
    phase0 = rng.uniform(0, 2 * np.pi)
    return amp * np.cos(2 * np.pi * t / period + phase0) + noise


def gen_ms_ar1(t: np.ndarray, period: float, snr: float,
               rng: np.random.Generator) -> np.ndarray:
    """Family II: Two-regime Markov-switching AR(1).

    The mean shift between regimes is proportional to SNR; expected
    regime dwell time matches the canonical band period.
    """
    n = t.size
    p_switch = 1.0 / period  # probability of switching per step
    regime = 0
    means = [-snr, +snr]  # mean shift proportional to SNR
    y = np.zeros(n)
    for i in range(1, n):
        if rng.random() < p_switch:
            regime = 1 - regime
        y[i] = 0.5 * y[i - 1] + means[regime] + rng.normal(scale=1.0)
    return y


def gen_mfrw(t: np.ndarray, period: float, snr: float,
             rng: np.random.Generator,
             lambda_sq: float = 0.02) -> np.ndarray:
    """Family III: Multifractal random walk with cyclical modulation.

    A simplified Bacry-Muzy-Delour MFRW where the log-volatility
    contains a slow cosine modulation at the canonical band frequency
    with amplitude proportional to SNR.
    """
    n = t.size
    # Log-volatility: AR(1) + cyclical modulation
    log_vol = np.zeros(n)
    for i in range(1, n):
        log_vol[i] = 0.95 * log_vol[i - 1] + rng.normal(scale=np.sqrt(lambda_sq))
    # Add cyclical modulation
    phase0 = rng.uniform(0, 2 * np.pi)
    log_vol = log_vol + snr * np.cos(2 * np.pi * t / period + phase0)
    sigma_t = np.exp(log_vol)
    return sigma_t * rng.standard_normal(n)


GENERATORS: dict[str, Callable] = {
    "ar1_plus_cosine": gen_ar1_plus_cosine,
    "ms_ar1": gen_ms_ar1,
    "mfrw": gen_mfrw,
}


# ============================================================
# Calibration loop
# ============================================================


@dataclass
class CalibCell:
    family: str
    snr: float
    n_replicates: int
    rejection_rate_ar1: float
    rejection_rate_dual: float
    median_p_ar1: float
    median_p_coherence: float


def run_calibration(family: str, generator: Callable, snrs: list[float],
                    period: float, lo_years: float, hi_years: float,
                    n_replicates: int, n_surrogates: int, t_len: int,
                    base_seed: int = 0) -> list[CalibCell]:
    cells = []
    t = np.arange(t_len)
    for snr in snrs:
        rejections_ar1 = 0
        rejections_dual = 0
        ps_ar1 = []
        ps_co = []
        t0 = time.time()
        for r in range(n_replicates):
            rng = np.random.default_rng(base_seed + r)
            y = generator(t, period, snr, rng)
            series = pd.Series(y)
            try:
                d = dual_null(series, lo_years, hi_years,
                              n_surrogates=n_surrogates,
                              seed=base_seed + r * 1000)
            except Exception:
                continue
            if not d["ar1"].reject_cycle:
                rejections_ar1 += 1  # AR(1) null rejected -> cycle detected
            if not d["reject_cycle"]:
                rejections_dual += 1
            ps_ar1.append(d["ar1"].p_value)
            ps_co.append(d["phase_scramble"].p_value)
        elapsed = time.time() - t0
        cell = CalibCell(
            family=family,
            snr=float(snr),
            n_replicates=n_replicates,
            rejection_rate_ar1=rejections_ar1 / max(n_replicates, 1),
            rejection_rate_dual=rejections_dual / max(n_replicates, 1),
            median_p_ar1=float(np.median(ps_ar1)) if ps_ar1 else float("nan"),
            median_p_coherence=float(np.median(ps_co)) if ps_co else float("nan"),
        )
        cells.append(cell)
        print(f"  {family} SNR={snr:.2f}  detect(AR1)={cell.rejection_rate_ar1:.2f}  "
              f"detect(dual)={cell.rejection_rate_dual:.2f}  ({elapsed:.1f}s)")
    return cells


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-replicates", type=int, default=100)
    parser.add_argument("--n-surrogates", type=int, default=200)
    parser.add_argument("--t-len", type=int, default=150,
                         help="annual observations (matches JST R6 length)")
    parser.add_argument("--out",
                         default="reports/calibration_v1.json")
    parser.add_argument("--families", nargs="+",
                         default=["ar1_plus_cosine", "ms_ar1", "mfrw"])
    args = parser.parse_args()

    snrs = [0.2, 0.3, 0.5, 1.0, 2.0]
    # Use Juglar band (7-11y) with period at band centre = 8y.
    period = 8.0
    lo_years, hi_years = 7.0, 11.0

    all_cells = []
    for family_name in args.families:
        if family_name not in GENERATORS:
            print(f"WARN: unknown family {family_name}; skipping")
            continue
        print(f"Family: {family_name}")
        cells = run_calibration(family_name, GENERATORS[family_name],
                                snrs=snrs, period=period,
                                lo_years=lo_years, hi_years=hi_years,
                                n_replicates=args.n_replicates,
                                n_surrogates=args.n_surrogates,
                                t_len=args.t_len)
        all_cells.extend(cells)

    output = {
        "version": "v1",
        "n_replicates": args.n_replicates,
        "n_surrogates": args.n_surrogates,
        "t_len": args.t_len,
        "band_lo_years": lo_years,
        "band_hi_years": hi_years,
        "period_at_centre": period,
        "alpha": 0.05,
        "cells": [asdict(c) for c in all_cells],
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
