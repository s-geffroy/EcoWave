# CPV — Cycle Position Vector

**CPV** is a reproducible, containerised research pipeline that decomposes
macroeconomic time-series into the four canonical economic cycles
(Kitchin 3–5 y, Juglar 7–11 y, Kuznets 15–25 y, Kondratieff 40–60 y) and
publishes per-group phase labels under a layered falsifiability protocol.

Site de documentation : <https://s-geffroy.github.io/EcoWave/>

## Three-gate falsifiability protocol

1. **Existence** — AR(1) bootstrap null per (group, indicator, band): the band
   must beat red noise at α = 0.05, otherwise the phase is published as
   `rejected`.
2. **Consensus** — at least 3 of 4 votant methods must agree on the phase
   label, otherwise it is `disputed`.
3. **Universality** — at least 4 of 5 income groups
   (WLD + HIC + UMC + LMC + LIC) must concur, otherwise the cycle is
   `regional / idiosyncratic`.

Full specification: `methodology/multi_cycle_decomposition.md` and
`methodology/cycle_validation_rules.md`.

## The four votant methods

| Code | Method | Source |
|---|---|---|
| D | PELT change-point detection | Killick et al. 2012 |
| E | Markov-switching AR(1) | Hamilton 1989 |
| F | Christiano-Fitzgerald band-pass + Hilbert phase | Christiano-Fitzgerald 2003 |
| G | Bry-Boschan / Harding-Pagan turning-point dating | Harding & Pagan 2002 |

Survey of the seven candidates considered: `methodology/cycle_methods_survey.md`.

## Two entry points

- **`position-cycles`** — long-horizon multi-cycle decomposition on World Bank
  data, per group (WLD, OECD, HIC/UMC/LMC/LIC, G7, BRICS).
- **`run-pilot <code>`** — same four-method stack on a single crisis window
  (2008, 2016, 2020, 2022, 2000). Pilots 2020 and 2022 are pre-registered
  holdouts for out-of-sample EWS validation.

## V1 ingested data

The composite intensity I_intensity is built from five curves (E/D/S/L/I)
fed by FRED, ECB and World Bank:

| Curve | Variables with real data | Source |
|---|---|---|
| E (economic) | E1 VIX, E2 TED, E3 equity drawdown, E4 GDP (US+EA), E5 unemployment (US+EA), E6 inflation (US+EA) | FRED |
| D (institutional) | D1 CISS, D2 IT/ES/PT spreads, D3 interventions | ECB SDMX / FRED / events |
| S (social) | S1 euro youth unemployment | FRED |
| L (logistic) | L1 Brent, L2 world trade | FRED / World Bank |
| I (information) | I1 EPU US+EU (proxy) | FRED |

Variables still `missing` (no open source): S2 protests (Mass Mobilization),
I2 narrative tone (GDELT). See `methodology/improvement_roadmap.md`.

For long-horizon cycle decomposition the World Bank panel is independent
(8 indicators in `cycles_manifest.json`, 1960 → present, per country and
per aggregate group).

## Architecture

- Docker mandatory · CLI as source of truth
- SQLite (state / metadata / provenance) + CSV (audit) + Parquet (analytics)
- `.env` for secrets (never committed)

## Quick start

```bash
cp .env.example .env
# Fill in FRED_API_KEY for strict mode.

docker compose build
docker compose run --rm --entrypoint ecowave ecowave init-db
docker compose run --rm --entrypoint ecowave ecowave check-config --mode exploratory
docker compose run --rm --entrypoint pytest ecowave
```

With a real `.env` (FRED key):

```bash
docker compose run --rm --entrypoint ecowave ecowave check-config --mode strict

# Multi-cycle world positioning (the headline analysis).
docker compose run --rm --entrypoint ecowave ecowave position-cycles \
  --as-of 2026-05 \
  --groups "WLD,OECD,HIC,UMC,LMC,LIC,G7,BRICS"

# CPV stack on a single crisis window.
docker compose run --rm --entrypoint ecowave ecowave run-pilot 2008 --mode strict
```

In `strict` mode, a missing critical source fails the run loudly with
an explanation.

## Documentation site (GitHub Pages)

Online: <https://s-geffroy.github.io/EcoWave/>

Local preview (inside the container):

```bash
make site         # sync docs/ then build MkDocs --strict
make docs-serve   # preview on http://localhost:8000
```

The site is auto-deployed on every push to `main` (workflow
`.github/workflows/pages.yml`).

## Methodological caveats

- WB data is annual; Kitchin 3–5 y is borderline at the lower edge. Reported
  with `endpoint_caveat` flags where applicable.
- WB series start in 1960, ≈ 1.0–1.5 Kondratieff cycles of history — the AR(1)
  null frequently rejects Kondratieff for several income groups. This is
  published honestly as `separable = 0`, not reinterpreted.
- Pre-registered parameters live in code; any change requires a methodology
  review. See `methodology/anti_pseudoscience_rules.md`.
