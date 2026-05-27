#!/usr/bin/env bash
# Refresh the MkDocs content from canonical sources before building the site.
# Run inside the container: docker compose run --rm --entrypoint bash ecowave scripts/sync_docs.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Cited data-sources page (generated from the manifest)
ecowave sources --output docs/sources.md --manifest sources_manifest.json

# Methodology (static canonical docs)
cp methodology/*.md docs/methodology/
cp variable_dictionary.md docs/methodology/variable_dictionary.md
cp scoring_rules.md docs/methodology/scoring_rules.md
cp model_comparison.md docs/methodology/model_comparison.md

# Generated reports, per pilot (report_<pilot>_pilot.md, model_comparison_<pilot>.md, ...)
mkdir -p docs/reports
shopt -s nullglob
for f in reports/report_*_pilot.md reports/model_comparison_*.md reports/validation_summary_*.md; do
  cp "$f" "docs/reports/$(basename "$f")"
done

# Generated figures, per pilot
mkdir -p docs/figures
for f in figures/curve_stress_*.png figures/model_windows_*.png; do
  cp "$f" "docs/figures/$(basename "$f")"
done
shopt -u nullglob

echo "docs/ synchronized."
