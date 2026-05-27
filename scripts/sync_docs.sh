#!/usr/bin/env bash
# Refresh the MkDocs content from canonical sources before building the site.
# Run inside the container: docker compose run --rm --entrypoint bash ecowave scripts/sync_docs.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Methodology (static canonical docs)
cp methodology/*.md docs/methodology/
cp variable_dictionary.md docs/methodology/variable_dictionary.md
cp scoring_rules.md docs/methodology/scoring_rules.md
cp model_comparison.md docs/methodology/model_comparison.md

# Generated reports (only if a pilot run has produced them)
for f in report_2008_pilot model_comparison validation_summary; do
  if [ -f "reports/$f.md" ]; then
    cp "reports/$f.md" "docs/reports/$f.md"
  fi
done

echo "docs/ synchronized."
