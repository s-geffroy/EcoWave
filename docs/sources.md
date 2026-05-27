# Data sources

All series below are ingested automatically with full provenance: each raw payload is stored under `data_raw/<provider>/` and registered in SQLite (`sources`, `raw_files` with SHA-256). This page is generated from `sources_manifest.json` — the single source of truth.

## Ingested variables

| Variable | Curve | Dataset | Provider | Series ID | Confidence | License note |
|---|---|---|---|---|---|---|
| E1 | E | CBOE Volatility Index: VIX | FRED | `VIXCLS` | A | verify before redistribution |
| E2 | E | TED Spread (discontinued 2022; 2007-2012 history available) | FRED | `TEDRATE` | A | verify before redistribution |
| E3 | E | NASDAQ Composite Index (broad equity drawdown proxy) | FRED | `NASDAQCOM` | A | verify before redistribution |
| E4 | E | Real GDP QoQ growth — composite US + Euro Area (quarterly) | FRED | `GDPC1 + CLVMNACSCAB1GQEA19` | B | US (GDPC1) + Euro Area (CLVMNACSCAB1GQEA19); each normalized vs own history |
| E5 | E | Unemployment rate — composite US + Euro Area (monthly) | FRED | `UNRATE + LRHUTTTTEZM156S` | B | US (UNRATE) + Euro Area (LRHUTTTTEZM156S) |
| E6 | E | Inflation YoY deviation from 2% — composite US + Euro Area (monthly) | FRED | `CPIAUCSL + CP0000EZ19M086NEST` | B | US (CPIAUCSL) + Euro Area HICP (CP0000EZ19M086NEST); target assumed 2% |
| D1 | D | Composite Indicator of Systemic Stress (Euro Area, daily) | ECB | `CISS/D.U2.Z0Z.4F.EC.SS_CIN.IDX` | A | ECB Data Portal; verify before redistribution |
| D2 | D | Euro periphery 10Y sovereign spreads vs Germany — basket IT/ES/PT (monthly) | FRED | `IRLTLT01ITM156N−IRLTLT01DEM156N + IRLTLT01ESM156N−IRLTLT01DEM156N + IRLTLT01PTM156N−IRLTLT01DEM156N` | B | OECD long-term rates via FRED; periphery basket vs Germany |
| S1 | S | Youth unemployment rate, ages 15-24, Euro Area (monthly) | FRED | `LRHU24TTEZM156S` | B | OECD/Eurostat via FRED; activates the social (S) curve |
| L1 | L | Crude Oil Prices: Brent - Europe (daily) | FRED | `DCOILBRENTEU` | A | verify before redistribution |
| D3 | D | Public intervention intensity (monthly count of D-curve institutional events) | EVENTS_DERIVED | `—` | C | Derived from events_master.csv; no pre-crisis baseline -> partial status |
| L2 | L | World imports of goods and services, volume (World Bank, WLD, annual) | WORLD_BANK | `NE.IMP.GNFS.KD` | B | World Bank Open Data (CC BY 4.0); annual world trade volume, YoY contraction = stress |
| I1 | I | Crisis media volume — news-based Economic Policy Uncertainty, US + Europe (monthly) | FRED | `USEPUINDXM + EUEPUINDXM` | C | Baker-Bloom-Davis EPU via FRED (newspaper-article counts); GDELT-free proxy for I1 |

## Not automatable in V1

| Variable | Reason |
|---|---|
| S2 | Anti-austerity protests: no open monthly source for 2010-2012 (UN does not track protests; ACLED covers Europe only from ~2020). Manual curation only. |
| I2 | Media tone/negativity: needs sentiment data (e.g. GDELT tone); no UN/World Bank substitute |

## Providers & citations

- **ECB** — European Central Bank — ECB Data Portal, <https://data.ecb.europa.eu>. CISS: Hollo, Kremer & Lo Duca (2012), ECB Working Paper 1426.
- **EVENTS_DERIVED** — EcoWave curated events (`events/events_master.csv`) — manual curation, sources to be verified per row.
- **FRED** — Federal Reserve Bank of St. Louis — FRED® (Federal Reserve Economic Data), <https://fred.stlouisfed.org>. Terms: <https://fred.stlouisfed.org/legal/>.
- **WORLD_BANK** — World Bank — World Development Indicators / World Bank Open Data, <https://data.worldbank.org>. Licence: CC BY 4.0.

## Upstream sources (credited beyond the API host)

- **Economic Policy Uncertainty (I1)** — Baker, S. R., Bloom, N., & Davis, S. J. (2016), *Measuring Economic Policy Uncertainty*, Quarterly Journal of Economics 131(4). Series `USEPUINDXM`, `EUEPUINDXM` via FRED.
- **Long-term government bond yields (D2)** — OECD Main Economic Indicators, via FRED (`IRLTLT01{IT,ES,PT,DE}M156N`).
- **Euro Area HICP (E6) and real GDP (E4)** — Eurostat, via FRED (`CP0000EZ19M086NEST`, `CLVMNACSCAB1GQEA19`).
- **CBOE Volatility Index (E1)** — Cboe Global Markets, via FRED (`VIXCLS`).

!!! warning "Redistribution"
    Raw API payloads are **not** redistributed on this site. Verify each provider's licence before redistributing raw data. Aggregated monthly panels are derived statistics.
