#!/usr/bin/env bash
# Download the canonical long-history macro datasets used by the
# `position-cycles --horizon long` mode.
#
# Sources (Creative Commons / open-data):
#   - Maddison Project Database 2023 — real GDP per capita 1820-2022,
#     169 countries. https://www.rug.nl/ggdc/historicaldevelopment/maddison/
#   - Jordà-Schularick-Taylor Macrohistory Database R6 (2023) — annual
#     macro/finance for 18 advanced economies 1870-2020. https://www.macrohistory.net/database/
#
# Both URLs are stable as of mid-2026 but may change between releases.
# Update the URLs here if a newer release is published.
#
# Usage (inside the container):
#   docker compose run --rm --entrypoint bash ecowave scripts/download_macrohistory.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DST="$ROOT/data_raw/macrohistory"
mkdir -p "$DST"

MADDISON_URL="${MADDISON_URL:-https://dataverse.nl/api/access/datafile/421302}"
JST_URL="${JST_URL:-https://www.macrohistory.net/app/download/9834512569/JSTdatasetR6.xlsx?t=1763503850}"

echo "Downloading Maddison Project Database 2023 -> $DST/mpd2023.xlsx"
curl -fsSL -o "$DST/mpd2023.xlsx" "$MADDISON_URL" \
  || { echo "Maddison download failed. Check MADDISON_URL." >&2; exit 1; }

echo "Downloading JST Macrohistory R6 -> $DST/jst_r6.xlsx"
curl -fsSL -o "$DST/jst_r6.xlsx" "$JST_URL" \
  || { echo "JST download failed. Check JST_URL." >&2; exit 1; }

echo "Datasets ready under $DST/"
ls -lh "$DST"
