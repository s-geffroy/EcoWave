# EcoWave — Pilote 2008

**EcoWave** est un pilote de recherche reproductible et conteneurisé qui teste une
adaptation prudente de la **théorie de Dow** et des **vagues d'Elliott** à la crise
systémique **2007-2012** (crise financière globale + crise de la dette souveraine euro).

Site de documentation : <https://s-geffroy.github.io/EcoWave/>

## Périmètre

- **Contexte Dow** : 2001-2006 (régime structurel)
- **Fenêtre Elliott active** : 2007-2012
- **Pilote 2 prévu** : 2011-2016

## Hypothèses concurrentes

| Modèle | Hypothèse |
|---|---|
| A | Un cycle Elliott unique 2007-2012 |
| B | Deux cycles imbriqués : 2007-2009 puis 2010-2012 (**champion provisoire**) |
| C | Dow sur 2007-2012, Elliott limité au choc aigu 2008 |

A et C attaquent B selon les **mêmes critères** C1–C6 (voir `scoring_rules.md`).

## Données réellement ingérées en V1

| Courbe | Variables avec données réelles | Source |
|---|---|---|
| E (économique) | E1 VIX, E2 TED, E3 drawdown actions, E4 PIB, E5 chômage, E6 inflation | FRED |
| D (institutionnel) | D1 CISS, D2 spread IT-DE, D3 interventions (events) | ECB SDMX / FRED / events |
| L (logistique) | L1 pétrole Brent | FRED |
| S / I | — (aucune source automatisable en V1) | `missing` |

Les variables sans source (S1, S2, L2, I1, I2) sont marquées `missing`.
Le verdict final reste **provisional/blocked** par construction (règles anti-pseudoscience).

## Architecture V1

- Docker obligatoire · CLI = source de vérité · Streamlit désactivé
- SQLite (état/métadonnées/provenance) + CSV (audit) + Parquet (analytique)
- `.env` pour les secrets (jamais committé) · DuckDB et Docker secrets prévus pour V1.5

## Démarrage rapide

```bash
cp .env.example .env
# Renseigner FRED_API_KEY dans .env pour le mode strict réel.

docker compose build
docker compose run --rm --entrypoint ecowave ecowave init-db
docker compose run --rm --entrypoint ecowave ecowave check-config --mode exploratory
docker compose run --rm --entrypoint pytest ecowave
```

Avec un `.env` réel (clé FRED) :

```bash
docker compose run --rm --entrypoint ecowave ecowave check-config --mode strict
docker compose run --rm --entrypoint ecowave ecowave run-pilot 2008 --mode strict
```

En mode `strict`, l'absence d'une source critique fait échouer le run **bruyamment**
en expliquant pourquoi.

## Site de documentation (GitHub Pages)

Site en ligne : <https://s-geffroy.github.io/EcoWave/>

Prévisualisation locale (dans le container) :

```bash
make site         # synchronise docs/ puis build MkDocs --strict
make docs-serve   # prévisualisation sur http://localhost:8000
```

Le site est déployé automatiquement sur GitHub Pages à chaque push sur `main`
(workflow `.github/workflows/pages.yml`, actions sur Node 24).

### Procédure de publication (première fois)

```bash
# 1. Créer le dépôt public et pousser
gh repo create s-geffroy/EcoWave --public --source . --remote origin --push

# 2. Activer GitHub Pages avec la source "GitHub Actions"
gh api -X POST repos/s-geffroy/EcoWave/pages -f build_type=workflow
```

Ensuite, chaque push sur `main` reconstruit et redéploie le site. Pour publier
des rapports fraîchement générés, lancer `make run-pilot-strict` puis `make site`
(qui copie `reports/` dans `docs/reports/`) avant de committer et pousser.

## Avertissement méthodologique

Tant que les couches sociale `S` et informationnelle `I` ne sont pas intégrées,
et tant que les critères qualitatifs C2/C4/C5/C6 ne sont pas évalués par un analyste,
**aucun verdict final** sur Elliott/Dow n'est présenté comme robuste.
