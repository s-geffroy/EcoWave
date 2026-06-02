"""Convert reports/calibration_v1.json into a LaTeX tabularx row block.

Usage: python scripts/calibration_to_latex.py
Outputs a snippet ready to paste into Appendix B of the paper.
"""
import json
import sys
from pathlib import Path


FAMILY_LABEL = {
    "ar1_plus_cosine": "Family I --- AR(1) + cosine",
    "ms_ar1":          "Family II --- MS-AR(1)",
    "mfrw":            "Family III --- MFRW + modulation",
}


def main() -> None:
    p = Path(sys.argv[1] if len(sys.argv) > 1 else "reports/calibration_v1.json")
    with p.open() as f:
        data = json.load(f)
    cells = data["cells"]
    snrs = sorted({c["snr"] for c in cells})
    families = sorted({c["family"] for c in cells},
                       key=lambda x: list(FAMILY_LABEL).index(x))

    print(f"% Source: {p}")
    print(f"% n_replicates={data['n_replicates']}  "
          f"n_surrogates={data['n_surrogates']}  "
          f"T={data['t_len']}  band=[{data['band_lo_years']},{data['band_hi_years']}]")
    print()
    for fam in families:
        rates = []
        for snr in snrs:
            match = next((c for c in cells if c["family"] == fam and c["snr"] == snr), None)
            rate = match["rejection_rate_ar1"] if match else None
            rates.append(f"{rate:.2f}" if rate is not None else "?")
        print(f"{FAMILY_LABEL[fam]:30s} & " + " & ".join(rates) + r" \\")


if __name__ == "__main__":
    main()
