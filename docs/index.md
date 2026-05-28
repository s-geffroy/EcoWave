# CPV — Cycle Position Vector

> A reproducible, containerised research pipeline that decomposes
> macroeconomic time-series into the four canonical economic cycles and
> publishes per-group phase labels under a three-gate falsifiability protocol.

## The cycles

| Cycle | Period | Phenomenon | Reference |
|---|---|---|---|
| **Kitchin** | 3–5 years | Inventory cycle | Kitchin 1923 |
| **Juglar** | 7–11 years | Fixed investment cycle | Juglar 1862; Schumpeter 1939 |
| **Kuznets** | 15–25 years | Infrastructure / demographic swing | Kuznets 1930 |
| **Kondratieff** | 40–60 years | Techno-economic long wave | Kondratieff 1925; Korotayev 2010 |

## The three gates of falsifiability

A phase is published for a (group, cycle, month) cell only when **all three**
gates pass:

1. **Existence (Gate 1)** — the band's power beats AR(1) red noise at α = 0.05.
2. **Consensus (Gate 2)** — ≥ 3 of 4 methods agree on the phase label.
3. **Universality (Gate 3)** — ≥ 4 of 5 income groups concur (for the
   "global cycle" qualification).

Cells that fail Gate 1 are published as `rejected`. Cells that pass Gate 1
but fail Gate 2 are published as `disputed`. The protocol publishes honest
failures rather than fabricated phases. See [Cycle validation rules](methodology/cycle_validation_rules.md).

## The four votant methods

| Code | Method | Source |
|---|---|---|
| **D** | PELT change-point detection | Killick et al. 2012 |
| **E** | Markov-switching AR(1) | Hamilton 1989 |
| **F** | Christiano-Fitzgerald band-pass + Hilbert phase | Christiano-Fitzgerald 2003 |
| **G** | Bry-Boschan / Harding-Pagan turning-point dating | Harding & Pagan 2002 |

The four methods embed very different generative assumptions; concordance
across them is evidence that no single method's artefact drives the result.
Full survey: [Cycle-methods survey](methodology/cycle_methods_survey.md).

## Two entry points

| Command | What it does |
|---|---|
| `ecowave position-cycles --as-of YYYY-MM` | World Bank long-horizon decomposition across WLD, OECD, HIC/UMC/LMC/LIC, G7, BRICS. |
| `ecowave run-pilot <code>` | Same four-method stack on a crisis window (2008, 2016, 2020, 2022, 2000). |

## Current snapshot

[**May 2026 cycle position report**](reports/cycle_position_2026_05.md) —
per-group × per-cycle phase matrix with AR(1) p-values, per-method consensus
votes, and the cross-group universality verdict.

## Quick start

```bash
docker compose build
docker compose run --rm --entrypoint ecowave ecowave init-db
docker compose run --rm --entrypoint ecowave ecowave position-cycles --as-of 2026-05
```

Full instructions: see the [GitHub repository](https://github.com/s-geffroy/EcoWave).
