.PHONY: build init-db check-config check-config-strict run-pilot run-pilot-strict run-pilot-2016-strict pilots-strict report test shell clean site docs-serve

build:
	docker compose build

init-db:
	docker compose run --rm --entrypoint ecowave ecowave init-db

check-config:
	docker compose run --rm --entrypoint ecowave ecowave check-config --mode exploratory

check-config-strict:
	docker compose run --rm --entrypoint ecowave ecowave check-config --mode strict

run-pilot:
	docker compose run --rm --entrypoint ecowave ecowave run-pilot 2008 --mode exploratory

run-pilot-strict:
	docker compose run --rm --entrypoint ecowave ecowave run-pilot 2008 --mode strict

run-pilot-2016-strict:
	docker compose run --rm --entrypoint ecowave ecowave run-pilot 2016 --mode strict

pilots-strict: run-pilot-strict run-pilot-2016-strict

site:
	docker compose run --rm --entrypoint bash ecowave scripts/sync_docs.sh
	docker compose run --rm --entrypoint mkdocs ecowave build --strict

docs-serve:
	docker compose run --rm --service-ports --entrypoint mkdocs ecowave serve -a 0.0.0.0:8000

report:
	docker compose run --rm --entrypoint ecowave ecowave generate-report --pilot 2008 --mode exploratory

test:
	docker compose run --rm --entrypoint pytest ecowave

shell:
	docker compose run --rm --entrypoint bash ecowave

clean:
	rm -f db/ecowave.db
	rm -rf data_processed/* reports/* figures/*
