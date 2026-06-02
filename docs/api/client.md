# Utilisation client

!!! success "TL;DR"

    Comment consommer le service depuis n'importe quel client. Trois exemples par endpoint : **curl** (terminal), **Python `httpx`** (script ou notebook), **JS `fetch`** (browser ou Node). Pour un client typé "production", générer automatiquement depuis [`openapi.yaml`](openapi.yaml) via `openapi-generator-cli`.

## Dans cette page

- **[Configuration](#config)** — base URL, headers communs
- **[Génération automatique de clients](#generation)** — Python, TypeScript, Go
- **[Exemples par endpoint](#exemples)** — curl, Python, JS pour chaque
- **[Gestion des erreurs](#erreurs)** — RFC 7807 Problem Details
- **[Versioning et compatibilité](#versioning)** — politique de breaking changes

---

## Configuration { #config }

| Variable | Valeur (local) | Valeur (prod) |
|---|---|---|
| Base URL | `http://localhost:8000/v1` | `https://api.ecowave.example.org/v1` |
| Content-Type (POST) | `application/json` | `application/json` |
| Accept | `application/json` | `application/json` |

Pas d'authentification en V1.

## Génération automatique de clients { #generation }

Le contrat OpenAPI est suffisant pour générer des clients typés dans la plupart des langages.

### Client Python

```bash
docker run --rm \
  -v $PWD/docs/api:/spec \
  -v $PWD/clients:/out \
  openapitools/openapi-generator-cli generate \
  -i /spec/openapi.yaml -g python \
  -o /out/python --package-name ecowave_client
```

Utilisation :

```python
from ecowave_client import ApiClient, Configuration
from ecowave_client.api import ForecastApi

config = Configuration(host="http://localhost:8000/v1")
api = ForecastApi(ApiClient(config))
result = api.forecast({
    "model": "msm",
    "series": [...],
    "horizons": [1, 6, 12],
    "n_samples": 1000,
})
```

### Client TypeScript

```bash
docker run --rm \
  -v $PWD/docs/api:/spec \
  -v $PWD/clients:/out \
  openapitools/openapi-generator-cli generate \
  -i /spec/openapi.yaml -g typescript-fetch \
  -o /out/typescript
```

### Autres langages

`openapi-generator-cli` supporte ~50 langages : Go, Rust, Java, C#, Ruby, Swift, Kotlin, etc. Lister :

```bash
docker run --rm openapitools/openapi-generator-cli list
```

## Exemples par endpoint { #exemples }

### `POST /v1/forecast`

**curl** :

```bash
curl -X POST http://localhost:8000/v1/forecast \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "msm",
    "series": [1.00, 1.02, 0.98, 1.05, 1.01, 0.99, 1.03],
    "horizons": [1, 6, 12],
    "n_samples": 1000,
    "seed": 42
  }'
```

**Python (`httpx`)** :

```python
import httpx

response = httpx.post(
    "http://localhost:8000/v1/forecast",
    json={
        "model": "msm",
        "series": history.tolist(),
        "horizons": [1, 6, 12],
        "n_samples": 1000,
        "seed": 42,
    },
    timeout=60.0,
)
response.raise_for_status()
forecast = response.json()
print(forecast["model_name"], forecast["metadata"])
```

**JavaScript (`fetch`)** :

```javascript
const response = await fetch("http://localhost:8000/v1/forecast", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    model: "msm",
    series: history,
    horizons: [1, 6, 12],
    n_samples: 1000,
    seed: 42,
  }),
});
const forecast = await response.json();
```

### `POST /v1/benchmark`

```bash
curl -X POST http://localhost:8000/v1/benchmark \
  -H 'Content-Type: application/json' \
  -d '{
    "panel": "wb",
    "models": ["rw", "msm", "har", "arfima_rs"],
    "horizons": [1, 6, 12],
    "n_origins": 8,
    "beat_threshold": 0.50,
    "decision_horizon": 12
  }'
```

Réponse : `BenchmarkReport` avec `verdict.pass_rate` et `verdict.passes`.

### `GET /v1/verdict`

```bash
curl http://localhost:8000/v1/verdict
curl 'http://localhost:8000/v1/verdict?as_of=2026-05-01'
```

```python
verdict = httpx.get("http://localhost:8000/v1/verdict").json()
print(f"Pass rate: {verdict['pass_rate']:.0%}")
for entry in verdict["leaderboard"]:
    print(f"  {entry['model']}: {entry['wins']} wins ({entry['share']:.0%})")
```

### `GET /v1/panels`

```bash
curl http://localhost:8000/v1/panels
```

Renvoie une liste de 6 `PanelInfo`.

### `GET /v1/panels/{panel}/variables`

```bash
curl http://localhost:8000/v1/panels/wb/variables
```

### `GET /v1/diagnostics/{panel}/{variable}`

```bash
curl http://localhost:8000/v1/diagnostics/wb/gdp_growth
```

Renvoie un `DiagnosticBundle` avec les 14 diagnostics dx (familles C+B+D+I+S).

## Gestion des erreurs { #erreurs }

Toutes les erreurs renvoient un payload **RFC 7807 Problem Details** :

```json
{
  "type": "about:blank",
  "title": "Validation failed",
  "status": 422,
  "detail": "series length 16 < minimum 32",
  "instance": "/v1/forecast"
}
```

Codes utilisés :

| Code | Signification |
|---|---|
| 400 | Payload mal formé (JSON invalide, champs manquants) |
| 404 | Panel ou variable inconnu |
| 422 | Payload valide mais sémantiquement invalide (série trop courte, modèle inconnu) |
| 500 | Erreur de fit côté serveur (ARMA non convergent, etc.) |
| 503 | Modèle non disponible sur cet endpoint |

Pattern client :

```python
import httpx

try:
    response = httpx.post(url, json=payload, timeout=60.0)
    response.raise_for_status()
    return response.json()
except httpx.HTTPStatusError as exc:
    problem = exc.response.json()
    print(f"[{problem['status']}] {problem['title']}: {problem.get('detail', '')}")
    raise
```

## Versioning et compatibilité { #versioning }

- **Namespace** `/v1/...` immédiat.
- **Changements compatibles** (restent dans `/v1/`) :
  - Nouveau champ optionnel dans une requête ou une réponse.
  - Nouvelle valeur ajoutée à un enum *en réponse* (clients robustes).
  - Nouvel endpoint.
- **Changements breaking** (forcent `/v2/...`) :
  - Suppression / renommage d'un champ.
  - Changement de type d'un champ.
  - Nouvelle valeur d'enum **en requête** (les clients existants ne la connaissent pas).
  - Changement du contrat d'erreurs.

Lors d'une migration `/v1/ → /v2/`, les deux namespaces coexistent au moins 6 mois.

## Outils utiles

- **Postman / Insomnia** : importer `openapi.yaml` directement → collection de requêtes prête.
- **HTTPie** : `http POST :8000/v1/forecast model=rw series:='[1,2,3,...]' horizons:='[1,6,12]'`
- **Swagger UI local** :

```bash
docker run --rm -p 8080:8080 \
  -e SWAGGER_JSON=/spec/openapi.yaml \
  -v $PWD/docs/api:/spec \
  swaggerapi/swagger-ui
```

Permet de tester chaque endpoint depuis un navigateur.

---

*Voir aussi :* [Vue d'ensemble API](index.md) · [Implémentation serveur](server.md) · [Module Python `ecowave.forecasting`](../tracks/quants/code_api.md).
