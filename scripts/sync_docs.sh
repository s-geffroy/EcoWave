#!/usr/bin/env bash
# Refresh the MkDocs content from canonical sources before building the site.
# Run inside the container: docker compose run --rm --entrypoint bash ecowave scripts/sync_docs.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Cited data-sources page (generated from the manifest)
ecowave sources --output docs/sources.md --manifest sources_manifest.json

# Methodology (static canonical docs)
mkdir -p docs/methodology
cp methodology/*.md docs/methodology/

# Generated CPV report + EWS validation
mkdir -p docs/reports
shopt -s nullglob
for f in reports/cycle_position_*.md reports/ews_validation.md; do
  cp "$f" "docs/reports/$(basename "$f")"
done

# Generated figures (cycle heatmap + CF trajectories + wavelet power + curve stress + intensities)
mkdir -p docs/figures
for f in figures/cycle_phase_heatmap_*.png \
         figures/cycle_cf_trajectories_*.png \
         figures/cycle_wavelet_power_*.png \
         figures/curve_stress_*.png \
         figures/global_indices_*.png; do
  cp "$f" "docs/figures/$(basename "$f")"
done
shopt -u nullglob

echo "docs/ synchronized."
