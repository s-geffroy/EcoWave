#!/usr/bin/env bash
# Refresh the MkDocs content from canonical sources before building the site.
# Run inside the container: docker compose run --rm --entrypoint bash ecowave scripts/sync_docs.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# docs/sources.md is now maintained manually in French (cf. plan).
# To regenerate from the manifest (English template), uncomment:
#   ecowave sources --output docs/sources.md --manifest sources_manifest.json

# Methodology (static canonical docs, French slugs)
mkdir -p docs/methodology
cp methodology/*.md docs/methodology/

# Generated CPV reports + EWS validation (French slugs)
mkdir -p docs/reports
shopt -s nullglob
for f in reports/panel_banque_mondiale_2026.md \
         reports/histoire_longue_2026.md \
         reports/panel_trimestriel_2026.md \
         reports/juglar_us_anglo_nordic_2026.md \
         reports/kondratieff_adv18_eu4_2026.md \
         reports/validation_ews.md \
         reports/cycle_position_2026_05_wb.md \
         reports/cycle_position_2026_05_q.md \
         reports/cycle_position_2026_05_long.md \
         reports/cycle_position_synthesis.md; do
  [[ -f "$f" ]] && cp "$f" "docs/reports/$(basename "$f")"
done

# Generated figures: CPV cycle outputs + legacy pilot curves
mkdir -p docs/figures
for f in figures/cycle_phase_heatmap_*.png \
         figures/cycle_amplitude_heatmap_*.png \
         figures/cycle_pvalue_heatmap_*.png \
         figures/cycle_next_extremum_timeline_*.png \
         figures/cycle_phase_polar_*.png \
         figures/cycle_cf_trajectories_*.png \
         figures/cycle_wavelet_power_*.png \
         figures/curve_stress_*.png \
         figures/global_indices_*.png \
         figures/juglar_us_anglo_nordic_*.png \
         figures/kondratieff_adv18_eu4_*.png; do
  cp "$f" "docs/figures/$(basename "$f")"
done
shopt -u nullglob

echo "docs/ synchronized."
