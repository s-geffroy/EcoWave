from __future__ import annotations

from ecowave.ingest.manifest import IngestionSpec, Manifest

PROVIDER_CITATIONS = {
    "FRED": "Federal Reserve Bank of St. Louis — FRED® (Federal Reserve Economic Data), "
            "<https://fred.stlouisfed.org>. Terms: <https://fred.stlouisfed.org/legal/>.",
    "FRED_SPREAD": "Federal Reserve Bank of St. Louis — FRED® (computed spread between two FRED series).",
    "ECB": "European Central Bank — ECB Data Portal, <https://data.ecb.europa.eu>. "
           "CISS: Hollo, Kremer & Lo Duca (2012), ECB Working Paper 1426.",
    "WORLD_BANK": "World Bank — World Development Indicators / World Bank Open Data, "
                  "<https://data.worldbank.org>. Licence: CC BY 4.0.",
    "EVENTS_DERIVED": "EcoWave curated events (`events/events_master.csv`) — manual curation, "
                      "sources to be verified per row.",
}

# Underlying upstream providers worth crediting beyond the API host (FRED redistributes these).
UPSTREAM_NOTES = [
    "**Economic Policy Uncertainty (I1)** — Baker, S. R., Bloom, N., & Davis, S. J. (2016), "
    "*Measuring Economic Policy Uncertainty*, Quarterly Journal of Economics 131(4). "
    "Series `USEPUINDXM`, `EUEPUINDXM` via FRED.",
    "**Long-term government bond yields (D2)** — OECD Main Economic Indicators, via FRED "
    "(`IRLTLT01{IT,ES,PT,DE}M156N`).",
    "**Euro Area HICP (E6) and real GDP (E4)** — Eurostat, via FRED "
    "(`CP0000EZ19M086NEST`, `CLVMNACSCAB1GQEA19`).",
    "**CBOE Volatility Index (E1)** — Cboe Global Markets, via FRED (`VIXCLS`).",
]


def _series_label(spec: IngestionSpec) -> str:
    if spec.components:
        return " + ".join(
            (f"{c.series_id}−{c.minus_series_id}" if c.minus_series_id else c.series_id)
            for c in spec.components
        )
    if spec.series_key:
        return spec.series_key
    if spec.minus_series_id:
        return f"{spec.series_id}−{spec.minus_series_id}"
    return spec.series_id or "—"


def render_sources_markdown(manifest: Manifest) -> str:
    lines = [
        "# Data sources",
        "",
        "All series below are ingested automatically with full provenance: each raw payload "
        "is stored under `data_raw/<provider>/` and registered in SQLite "
        "(`sources`, `raw_files` with SHA-256). This page is generated from "
        "`sources_manifest.json` — the single source of truth.",
        "",
        "## Ingested variables",
        "",
        "| Variable | Curve | Dataset | Provider | Series ID | Confidence | License note |",
        "|---|---|---|---|---|---|---|",
    ]
    for spec in manifest.specs:
        lines.append(
            f"| {spec.variable_code} | {spec.variable_code[0]} | {spec.dataset_name} | "
            f"{spec.provider} | `{_series_label(spec)}` | {spec.confidence} | {spec.license_notes} |"
        )

    lines += ["", "## Not automatable in V1", "",
              "| Variable | Reason |", "|---|---|"]
    for code, reason in manifest.not_automatable.items():
        lines.append(f"| {code} | {reason} |")

    providers = sorted({spec.provider for spec in manifest.specs} | {"EVENTS_DERIVED"})
    lines += ["", "## Providers & citations", ""]
    for prov in providers:
        if prov in PROVIDER_CITATIONS:
            lines.append(f"- **{prov}** — {PROVIDER_CITATIONS[prov]}")

    lines += ["", "## Upstream sources (credited beyond the API host)", ""]
    lines += [f"- {note}" for note in UPSTREAM_NOTES]

    lines += ["", "!!! warning \"Redistribution\"",
              "    Raw API payloads are **not** redistributed on this site. Verify each "
              "provider's licence before redistributing raw data. Aggregated monthly panels "
              "are derived statistics.", ""]
    return "\n".join(lines)
