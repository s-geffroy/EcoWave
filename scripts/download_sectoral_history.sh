#!/usr/bin/env bash
# Download Phase 3 sectoral history data: FRED + OWID open CSVs.
# Roadmap #13 Phase 3 substitute for Mitchell IHS (Springer Palgrave blocked).
# Source verification dates listed inline (per agent reports 2026-05).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/data_raw/sectoral_history"
mkdir -p "$DEST"
echo "Downloading sectoral history CSVs into $DEST..."

# --- FRED (US, NBER Macrohistory + BLS + BEA, CC0 public domain) ----------
# Each CSV: observation_date, <series_id>. No auth required. Annual or monthly.
fred() {
  local id="$1"
  local out="$2"
  curl -sL -o "$DEST/$out" \
    "https://fred.stlouisfed.org/graph/fredgraph.csv?id=$id&cosd=1700-01-01&coed=2030-12-31"
  echo "  FRED $id → $out ($(wc -l < "$DEST/$out") rows)"
}

# US Wholesale Price Index — splice pre/post 1913 (NBER + BLS PPIACO)
fred "M04051USM324NNBR" "us_wpi_nber_1860_1939.csv"  # NBER General Price Level
fred "PPIACO"           "us_wpi_bls_1913_now.csv"     # BLS PPI All Commodities
# US Industrial Production (1919+)
fred "INDPRO"           "us_indprod_1919_now.csv"
# US Total Coal (annual long span)
fred "A01210USA448NNBR" "us_coal_1856_1958.csv"
# US Steel Ingots (annual 1863-1919) + US Steel Ingot monthly 1932-1965
fred "A01208USA576NNBR" "us_steel_1863_1919.csv"
fred "M0135BUSM585NNBR" "us_steel_ingot_1932_1965.csv"
# US Pig Iron monthly 1941-1964 (limited but worth including)
fred "M0130BUSM583NNBR" "us_pigiron_1941_1964.csv"
# US Railway Freight Ton-Miles monthly 1866-1922
fred "M03003USM253SNBR" "us_railfreight_1866_1922.csv"
# US Wheat Production annual 1866-1952
fred "A01009USA391NNBR" "us_wheat_1866_1952.csv"
# US Cotton Consumption monthly 1912-1961
fred "M01089USM596NNBR" "us_cotton_1912_1961.csv"

# --- OWID grapher (CC BY 4.0, no auth) -----------------------------------
# Coal production by country, TWh, 1900-2024
curl -sL -o "$DEST/world_coal_owid.csv" \
  "https://ourworldindata.org/grapher/coal-production-by-country.csv?v=1&csvType=full&useColumnShortNames=false"
echo "  OWID coal-production-by-country → world_coal_owid.csv"

# Oil production by country, TWh, 1900-2024
curl -sL -o "$DEST/world_oil_owid.csv" \
  "https://ourworldindata.org/grapher/oil-production-by-country.csv?v=1&csvType=full&useColumnShortNames=false"
echo "  OWID oil-production-by-country → world_oil_owid.csv"

# --- UK long-history coal (BEIS / DECC via OWID legacy GitHub) -----------
# UK coal output 1700-2019 (million tonnes), DECC/BEIS via the deprecated
# owid-datasets repo. Critical for Wen 2005 UK Kitchin test.
curl -sL -o "$DEST/uk_coal_beis_1700_2019.csv" \
  "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Coal%20output%20and%20employment%20in%20UK%20-%20BEIS%20(2020)/Coal%20output%20and%20employment%20in%20UK%20-%20BEIS%20(2020).csv"
echo "  OWID legacy UK coal BEIS → uk_coal_beis_1700_2019.csv"

echo "All downloads complete."
ls -lh "$DEST" | tail -n +2
