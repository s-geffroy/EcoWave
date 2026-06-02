# Implémenter le serveur

!!! success "TL;DR"

    Comment implémenter un serveur HTTP conforme à [`openapi.yaml`](openapi.yaml). Référence : **FastAPI** (Python, aligne avec la stack EcoWave existante). Pour chaque endpoint, on donne le **mapping vers la fonction Python** dans `ecowave.forecasting` qui fournit le résultat. Le contrat est indépendant du langage : on peut tout aussi bien implémenter en Go, Rust, ou Node.

## Dans cette page

- **[Architecture cible](#architecture)** — couche HTTP devant `ecowave.forecasting`
- **[Stack référence](#stack)** — FastAPI + Docker
- **[Mapping endpoints → fonctions Python](#mapping)** — un tableau, six lignes
- **[Snippets FastAPI minimaux](#snippets)** — un endpoint à la fois
- **[Tests de conformité](#tests)** — pytest + schemathesis
- **[Docker compose](#docker)** — service web dans le compose existant

---

## Architecture cible { #architecture }

```mermaid
flowchart LR
    Client[Client REST<br/>Python / JS / curl] --> HTTP[Couche HTTP<br/>FastAPI]
    HTTP --> Forecast[ecowave.forecasting<br/>module Python existant]
    Forecast --> Models[6 modèles<br/>RW · AR(1) · ARMA<br/>HAR · ARFIMA+RS · MSM]
    Forecast --> Sidecars[reports/forecast_benchmark_*.json<br/>verdict consolidé]
    style HTTP fill:#90caf9,stroke:#1565c0,stroke-width:3px
    style Sidecars fill:#fff59d,stroke:#f9a825
```

La couche HTTP est **mince** : elle (1) valide la requête contre la spec, (2) appelle la fonction Python existante, (3) sérialise le résultat selon le schéma OpenAPI.

Aucun code de modèle n'est réécrit. Les modèles, le scoring, le benchmark sont déjà testés (225+ tests). Le serveur les **wrappe**.

## Stack référence { #stack }

- **FastAPI** ≥ 0.110 — framework Python async, génération automatique d'OpenAPI à partir des type hints, validation Pydantic.
- **Pydantic v2** — modèles Python qui doivent correspondre aux `components/schemas` du contrat.
- **Docker** — un service `ecowave-api` ajouté au `docker-compose.yml` existant.

!!! warning "Conformité, pas génération"

    FastAPI **génère** un OpenAPI à partir des décorateurs Python. C'est utile localement, mais le contrat de référence reste `docs/api/openapi.yaml` (écrit à la main, indépendant). Avant chaque release, comparer le YAML généré par FastAPI au contrat de référence : ils doivent être équivalents (test de conformité, voir plus bas).

## Mapping endpoints → fonctions Python { #mapping }

| Endpoint OpenAPI | Fonction Python | Module |
|---|---|---|
| `POST /v1/forecast` | `random_walk_forecast` / `ar1_forecast` / `arma11_forecast` / `har_forecast` / `arfima_rs_forecast` / `msm_forecast` (dispatcher selon `model`) | `ecowave.forecasting.{baselines,har,arfima_rs,msm}` |
| `POST /v1/benchmark` | `run_benchmark(config, panel_data)` puis `evaluate_acceptance_criterion(...)` | `ecowave.forecasting.benchmark` |
| `GET /v1/verdict` | Lire `reports/forecast_benchmark_*.json` (le plus récent ou `as_of`), sérialiser selon le schéma `Verdict` | I/O + `ecowave.forecasting.consolidated_report` |
| `GET /v1/panels` | Lecture statique d'un manifeste `panels.json` (à créer côté serveur) | I/O |
| `GET /v1/panels/{panel}/variables` | Loader du panel + extraction de la liste de variables | I/O + loader interne |
| `GET /v1/diagnostics/{panel}/{variable}` | Lecture du sidecar `dx_diagnostics_*.json` correspondant | I/O |

## Snippets FastAPI minimaux { #snippets }

### `POST /v1/forecast`

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import numpy as np

from ecowave.forecasting import (
    random_walk_forecast, ar1_forecast, arma11_forecast,
    har_forecast, arfima_rs_forecast, msm_forecast,
)

app = FastAPI(title="EcoWave CPV API", version="1.0.0")

class ForecastRequest(BaseModel):
    model: Literal["rw", "ar1", "arma11", "har", "arfima_rs", "msm"]
    series: list[float] = Field(min_length=32)
    horizons: list[int] = Field(min_length=1, max_length=24)
    n_samples: int = Field(default=1000, ge=100, le=10000)
    seed: int = Field(default=0, ge=0)
    msm_components: int = Field(default=4, ge=1, le=8)

DISPATCH = {
    "rw": random_walk_forecast,
    "ar1": ar1_forecast,
    "arma11": arma11_forecast,
    "har": har_forecast,
    "arfima_rs": arfima_rs_forecast,
    "msm": msm_forecast,
}

@app.post("/v1/forecast")
def forecast(req: ForecastRequest) -> dict:
    fn = DISPATCH[req.model]
    history = np.asarray(req.series, dtype=float)
    horizons = tuple(req.horizons)
    try:
        result = fn(history, horizons, n_samples=req.n_samples, seed=req.seed)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {
        "horizons": list(result.horizons),
        "samples": result.samples.tolist(),
        "model_name": result.model_name,
        "metadata": result.metadata,
    }
```

### `POST /v1/benchmark`

```python
from ecowave.forecasting.benchmark import (
    BenchmarkConfig, run_benchmark, evaluate_acceptance_criterion,
)

class BenchmarkRequest(BaseModel):
    panel: Literal["wb", "q", "long", "boe", "bis", "sh"]
    models: list[str] = ["rw", "ar1", "arma11", "har", "arfima_rs", "msm"]
    horizons: list[int] = [1, 3, 6, 12]
    n_origins: int = 8
    n_samples: int = 1000
    beat_threshold: float = 0.50
    decision_horizon: int = 12
    seed: int = 0

@app.post("/v1/benchmark")
def benchmark(req: BenchmarkRequest) -> dict:
    panel_data = load_panel(req.panel)
    config = BenchmarkConfig(
        horizons=tuple(req.horizons),
        models=tuple(req.models),
        n_origins=req.n_origins,
        n_samples=req.n_samples,
        seed=req.seed,
    )
    results = run_benchmark(panel_data, config)
    verdict = evaluate_acceptance_criterion(
        results, decision_horizon=req.decision_horizon,
        beat_threshold=req.beat_threshold,
    )
    return serialize_report(results, verdict, panel=req.panel)
```

### `GET /v1/verdict`

```python
import json, glob, os
from datetime import date

@app.get("/v1/verdict")
def get_verdict(as_of: str | None = None) -> dict:
    pattern = "reports/forecast_benchmark_consolidated_*.json"
    candidates = sorted(glob.glob(pattern))
    if as_of:
        candidates = [c for c in candidates if as_of in os.path.basename(c)]
    if not candidates:
        raise HTTPException(status_code=404, detail="No verdict available")
    with open(candidates[-1]) as f:
        return json.load(f)
```

### Endpoints catalog (`/panels`, `/panels/{panel}/variables`, `/diagnostics/...`)

Implémentations triviales — loaders + sérialisation, ~10 lignes chacune.

## Tests de conformité { #tests }

Deux niveaux :

1. **Validation statique** — Spectral lint sur `openapi.yaml` (CI).
2. **Tests de conformité à l'exécution** — [Schemathesis](https://schemathesis.readthedocs.io/) génère des cas de test à partir de la spec et les exécute contre le serveur.

```bash
docker run --rm --network host -v $PWD/docs/api:/spec \
  schemathesis/schemathesis run /spec/openapi.yaml \
  --base-url http://localhost:8000
```

Doit passer 100 % des cas générés.

## Docker compose { #docker }

Ajouter au `docker-compose.yml` existant :

```yaml
services:
  ecowave-api:
    build: .
    command: uvicorn ecowave_api.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    volumes:
      - ./reports:/app/reports:ro
      - ./data:/app/data:ro
```

Lancement :

```bash
docker compose up -d ecowave-api
curl http://localhost:8000/v1/verdict
```

## Implémentations alternatives

Le contrat est indépendant du langage. Exemples :

- **Go** : `oapi-codegen` génère le squelette serveur depuis `openapi.yaml`. Wrapper appelle `ecowave` via gRPC ou CLI subprocess.
- **Node.js** : `express-openapi-validator` valide automatiquement contre la spec.
- **Rust** : `utoipa` ou `axum` + génération manuelle.

Dans tous les cas, le bloc *calcul* (modèles, scoring) reste Python — l'autre langage n'est qu'une couche réseau.

---

*Voir aussi :* [Vue d'ensemble API](index.md) · [Utilisation client](client.md) · [Module Python `ecowave.forecasting`](../tracks/quants/code_api.md).
