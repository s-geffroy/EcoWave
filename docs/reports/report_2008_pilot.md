# EcoWave — Pilot 2008

Generated: 2026-05-27T18:30:21.333604+00:00  ·  Mode: `strict`

## Final verdict: SCORED (analyst-annotated)

All six criteria are filled for every model (C1/C3 computed, C2/C4/C5/C6 analyst-annotated). Verdicts and the champion/challenger adjudication below are therefore decisive for this evidence base. Remaining data gaps (I2 media tone, S2 protests) are documented as limitations.

## Source completeness

- Variables with real data: **13**
- Variables missing (no V1 source): **5**
- Ingestion failures this run: **0** 

### Curve coverage
| Curve | variables with real data |
|---|---:|
| E | 6 |
| D | 3 |
| S | 1 |
| L | 2 |
| I | 1 |

### Per-variable status (months 2007-01 .. 2012-12)
| Variable | available | partial | missing |
|---|---:|---:|---:|
| D1 | 72 | 0 | 0 |
| D2 | 72 | 0 | 0 |
| D3 | 3 | 0 | 69 |
| E1 | 72 | 0 | 0 |
| E2 | 72 | 0 | 0 |
| E3 | 72 | 0 | 0 |
| E4 | 24 | 0 | 48 |
| E5 | 72 | 0 | 0 |
| E6 | 72 | 0 | 0 |
| I1 | 72 | 0 | 0 |
| I2 | 0 | 0 | 72 |
| L1 | 72 | 0 | 0 |
| L2 | 6 | 0 | 66 |
| S1 | 72 | 0 | 0 |
| S2 | 0 | 0 | 72 |

## Method

- Dow context window: 2001-2006 (regime context)
- Elliott active window: 2007-2012
- Competing models: A (unique cycle), B (nested cycles, provisional champion), C (acute shock only)
- Dual reference windows: pre-crisis 1990-2006, structural 1990-2019 (Covid/Ukraine excluded)

## Computed criteria (honest, data-driven)

Only C1 (multi-curve synchronisation) and C3 (reference-window robustness) are
auto-computed from the real panel. See `model_comparison.md`.

## Known structural limitations

- E-curve combines US + Euro Area (composite); E4 GDP is quarterly only.
- D-curve structural window is short (ECB CISS starts 1999) → C3 weak for D.
- D3 derived from curated events only → no pre-crisis baseline (status `partial`).
- I1 is a news-based EPU proxy (not GDELT); I2 (tone) and S2 (protests) still missing.
