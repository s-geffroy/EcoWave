PAPER := cycles_refuted
IMAGE := ecowave-latex
DOCKER := docker run --rm -v $(CURDIR):/workspace -w /workspace $(IMAGE)

# Python pipeline image (built from repository root).
PY_IMAGE := ecowave
ROOT     := $(abspath $(CURDIR)/../..)
PY_DOCKER := docker run --rm -v $(ROOT):/app -w /app $(PY_IMAGE) python

.PHONY: image pdf validate consistency clean distclean shell \
        referee-r1 referee-r2 referee-r4 referee-r5 referee-all

image:
	docker build -t $(IMAGE) .

pdf: image
	$(DOCKER) latexmk -pdf -bibtex -interaction=nonstopmode -halt-on-error $(PAPER).tex

validate: image
	$(DOCKER) python3 scripts/validate_bib.py references.bib

consistency: image
	$(DOCKER) python3 scripts/check_bib_consistency.py $(PAPER).tex references.bib

shell: image
	docker run --rm -it -v $(CURDIR):/workspace -w /workspace $(IMAGE) bash

clean:
	$(DOCKER) latexmk -c $(PAPER).tex
	rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.toc *.fls *.fdb_latexmk

distclean: clean
	rm -f $(PAPER).pdf

# ------------------------------------------------------------------
# Referee-driven reruns. Each target produces one JSON sidecar in
# /app/reports/ that the LaTeX consumes (or will consume) for the
# corresponding paragraph of Section~5 and Appendix D.
# Run from the paper directory: ``make referee-r1`` etc.
# ``make referee-all`` runs the full sweep (long; budget hours).
# ------------------------------------------------------------------

referee-r1:  ## R1: long-memory diagnostics + ARFIMA Gate-1 null
	$(PY_DOCKER) scripts/long_memory_diagnostics.py --panel jst,boe
	$(PY_DOCKER) scripts/arfima_null_per_cell.py --panels jst,boe --n-surrogates 1000

referee-r2:  ## R2: high-resolution surrogates for BH-FDR-compatible p-values
	$(PY_DOCKER) scripts/jst_per_variable.py --n-surrogates 20000 \
	    --out reports/jst_per_variable_b20000.json
	$(PY_DOCKER) scripts/boe_kondratieff_per_variable.py --n-surrogates 20000 \
	    --out reports/boe_per_variable_b20000.json

referee-r4:  ## R4: sensitivity of Gate 1 to canonical-band edge perturbation
	$(PY_DOCKER) scripts/band_sensitivity.py --panels jst,boe --n-surrogates 500

referee-r5:  ## R5: rolling-window Gate 1 (temporal stability map)
	$(PY_DOCKER) scripts/rolling_window_gates.py --panels jst,boe \
	    --window 50 --step 25 --n-surrogates 300

referee-all: referee-r1 referee-r2 referee-r4 referee-r5  ## Full referee sweep
