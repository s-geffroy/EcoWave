# EcoWave

**EcoWave** is a reproducible, Dockerized research pilot that tests whether
**Dow Theory** and **Elliott Wave** methodology can be adapted to the
**2007–2012 systemic crisis** — without falling into pseudoscience.

!!! warning "Provisional / blocked by design"
    EcoWave V1 does **not** issue a final analytical verdict. The social (S) and
    information (I) curves have no automatable data source in V1, and four of the
    six scoring criteria require analyst judgement. Every model is reported as
    **blocked**. This is a deliberate guardrail, not a bug.

## What it does

1. Ingests real macro-financial series (FRED, ECB SDMX) with full provenance.
2. Normalizes each variable against **two reference windows** (pre-crisis 1990–2006,
   structural 1990–2019) — z-scores and 0–100 stress percentiles.
3. Aggregates stress by curve (Economic, Diplomatic, Social, Logistics, Information).
4. Scores three competing models on identical criteria:
      - **A** — one unique Elliott cycle 2007–2012
      - **B** — two nested cycles 2007–2009 and 2010–2012 (*provisional champion*)
      - **C** — Elliott limited to the acute 2008 shock
5. Publishes auditable reports — with missing data and blocked verdicts shown openly.

## Principles

- The **CLI pipeline is the source of truth**; this site only renders its outputs.
- **Raw values are preserved**; nothing is silently imputed.
- A wave exists only if **independent curves confirm** a phase change.

See the [Methodology](methodology/dow_elliott_adaptation.md) section for the full framework
and [Reports](reports/report_2008_pilot.md) for the latest pilot output.
