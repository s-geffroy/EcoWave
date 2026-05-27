#!/usr/bin/env bash
set -euo pipefail

echo "== EcoWave apply_and_validate =="

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker is not installed or not in PATH." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: Docker Compose v2 is not available." >&2
  exit 1
fi

if [ ! -f ".env" ]; then
  echo "No .env found. Copying .env.example to .env."
  cp .env.example .env
  echo "WARNING: .env contains placeholder values. Strict pipeline will fail until secrets are configured."
fi

mkdir -p db data_raw data_processed events reports figures methodology

echo "Building Docker image..."
docker compose build

echo "Initializing SQLite database..."
docker compose run --rm --entrypoint ecowave ecowave init-db

echo "Running config check in exploratory mode..."
docker compose run --rm --entrypoint ecowave ecowave check-config --mode exploratory || true

echo "Running tests..."
docker compose run --rm --entrypoint pytest ecowave

cat <<'NEXT'

Validation finished.

Next steps:
1. Edit .env and replace FRED_API_KEY=replace_me with a real key.
2. Run:
   docker compose run --rm --entrypoint ecowave ecowave check-config --mode strict
3. Then run:
   docker compose run --rm --entrypoint ecowave ecowave run-pilot 2008 --mode strict

Important:
- Exploratory mode may produce provisional outputs.
- Strict mode is required for any serious analytical result.
NEXT
