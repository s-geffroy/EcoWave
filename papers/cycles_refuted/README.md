# Cycles Refuted — LaTeX Paper

A short, defensible paper demonstrating that the four canonical economic
cycles (Kitchin, Juglar, Kuznets, Kondratieff) fail to survive a pre-registered
three-gate falsifiable protocol across six panels spanning 1700–2024.

The paper is companion to the broader CPV (Critique du Paradigme des Cycles)
methodology developed in `/Users/sge/ecowave/ecowave/docs/` and points to the
alternative empirical signature (cluster C+B+D+I+S) without developing it.

Target outlet: Physica A / Journal of Economic Behavior & Organization
(econophysics angle).

## Build

The build is fully containerised. No local TeXLive installation is required.

```bash
make image        # build the texlive docker image
make pdf          # compile cycles_refuted.pdf
make validate     # validate every DOI / ISBN in references.bib
make consistency  # cross-check \cite{} keys against references.bib
make clean        # remove latex intermediates
make distclean    # remove intermediates + final PDF
```

## Layout

| File / dir | Purpose |
|------------|---------|
| `cycles_refuted.tex` | main paper (elsarticle.cls) |
| `sections/` | §1 to §7 |
| `appendices/` | A: data, B: methods, C: criteria, D: per-variable evidence |
| `references.bib` | BibTeX bibliography (biblatex / biber) |
| `figures/` | figures (heatmaps, tables) — populated from `../../reports/` |
| `scripts/` | bibliography validation scripts |
| `Dockerfile` | reproducible build environment (texlive-full + python3) |
| `Makefile` | build entry points |
