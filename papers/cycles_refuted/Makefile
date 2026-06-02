PAPER := cycles_refuted
IMAGE := ecowave-latex
DOCKER := docker run --rm -v $(CURDIR):/workspace -w /workspace $(IMAGE)

.PHONY: image pdf validate consistency clean distclean shell

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
