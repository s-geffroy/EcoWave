# Group glossary

CPV publishes phases per **group** — an aggregate of countries. Some are
official World Bank aggregates (one series per indicator served directly by
the WB API); others are GDP-weighted composites recomputed by the pipeline.

## Income classifications (World Bank 2024–2025)

The four income classes use the per-capita GNI thresholds set by the World
Bank for fiscal year 2024–2025. The thresholds are applied annually; a
country can change class between two CPV runs.

| Code | Name | GNI/cap threshold (Atlas method, current USD) |
|---|---|---|
| `WLD` | World | n/a (global aggregate) |
| `HIC` | High-income countries | > 14 005 |
| `UMC` | Upper-middle-income countries | 4 516 – 14 005 |
| `LMC` | Lower-middle-income countries | 1 146 – 4 515 |
| `LIC` | Low-income countries | ≤ 1 145 |

These are the five income-stratification aggregates used by Gate 3
(universality) — a cycle is qualified `universal` only when ≥ 4 of these 5
share the same modal phase. See
[Cycle validation rules](methodology/cycle_validation_rules.md).

## Other aggregates

| Code | Name | Composition |
|---|---|---|
| `OECD` (`OED`) | OECD members | 38 countries; official WB aggregate |
| `G7` | G7 | USA, GBR, FRA, DEU, ITA, JPN, CAN — recomputed GDP-weighted |
| `G20` | G20 sample | 19 countries (EU represented by DEU+FRA+ITA to avoid double-counting) |
| `BRICS` | BRICS+ | BRA, RUS, IND, CHN, ZAF + EGY, ARE, ETH, IRN, IDN (post-2025 membership, 10 countries) — recomputed GDP-weighted |

OECD and the income classes use the official WB aggregate (one series per
indicator); G7, G20 and BRICS are recomputed by the pipeline using current-USD
GDP as the weight (`NY.GDP.MKTP.CD`).

## Why these aggregates

- **WLD + 4 income classes** — the canonical stratification used by Gate 3
  to qualify a cycle as global vs. regional.
- **OECD** — historic "developed economies" benchmark; useful for comparison
  with HIC because the two overlap but do not coincide.
- **G7, BRICS, G20** — economic-policy aggregates regularly cited in the
  literature; reported for context, not part of Gate 3.

Country lists are frozen in `ecowave/cycles/bands.py:GROUPS`; changing them
requires a methodology review (pre-registration discipline).
