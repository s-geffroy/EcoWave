# Normalization rules

Each variable must preserve:

- raw value
- z-score against pre-crisis reference
- stress percentile 0-100 against pre-crisis reference
- z-score against structural reference
- stress percentile 0-100 against structural reference

## Reference windows

- Main score: 1990-2006 when available, otherwise longest available pre-2007 window.
- Robustness score: 1990-2019 when available, excluding Covid/Ukraine.

## Cross-curve synthesis

Per-variable normalisation is the entry point; per-curve averaging
(`scoring/curve_scores.py`) produces a stress per curve. The synthetic
global indicator (intensity + diffusion, three weightings — `equal`, `pca`,
`favar`) is documented in `composite_indicator.md` and is what Elliott
detection runs on at the composite level.
