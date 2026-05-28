# Cycle-decomposition methods — survey

This document records the seven falsifiable methods considered for the CPV
framework, the four that became active votant components, and the three
references kept for context.

## Decision matrix

| # | Method | Falsifiability | Horizon | Surrogate compat. | WB-data adequacy | Status |
|---|---|---|---|---|---|---|
| 1 | CF band-pass + Morlet + Hilbert | AR(1) bootstrap | All cycles | Yes (Torrence-Compo) | Yes | **Active (Model F)** |
| 2 | Bry-Boschan / Harding-Pagan | Deterministic | Business cycle | Yes | Yes | **Active (Model G)** |
| 3 | Markov-switching (Hamilton 1989) | LR test, BIC | Multi-régime | Yes (simulate) | Yes | **Active (Model E)** |
| 4 | PELT change-point (Killick 2012) | BIC penalty + η² null | Multi-régime | Yes | Yes | **Active (Model D)** |
| 5 | Borio/Drehmann financial cycle | Laeven-Valencia comparison | ~15–20 years | Indirect | Partial | Conditional (Model H) |
| 6 | State-space UCM / Hamilton 2018 | Likelihood ratio | Trend + cycle | Yes | Yes | Survey only |
| 7 | Wavelet coherence networks | Cone + bootstrap | All cycles, multivar | Yes | Yes | Inside Model F figure |
| — | EMD / Hilbert-Huang | Mode-mixing | All | Weak | Yes | **Rejected** |
| — | Goldstein / Modelski long cycles | Narrative | Kondratieff | No | Limited | **Rejected** |
| — | Mensch / civilizational waves | None | Centennial | No | None | **Rejected** |

## Why four methods rather than one

CPV does not bet on any single decomposition. The three-gate falsifiability
stack means that a cycle phase is published only when:

1. **Gate 1 — Existence**: the band's power exceeds AR(1) red noise (Method 1
   alone gates this).
2. **Gate 2 — Method consensus**: ≥ 3 of 4 of {F (CF+Hilbert), G (Bry-Boschan),
   E (Markov-switching), D (PELT)} agree on the label. The four methods embed
   four very different generative assumptions, so concordance is evidence
   that no method-specific artefact drives the result.
3. **Gate 3 — Universality across income groups**: ≥ 4 of 5 income groups
   concur. C6 transferability applied across the income dimension rather
   than the temporal dimension.

Method 7 (wavelet coherence) is computed but does not vote — it appears as a
publication figure ("wavelet power") that lets a reader independently
inspect the spectral evidence behind Method 1's verdict.

## References by method

- **CF band-pass** — Christiano, L. J., & Fitzgerald, T. J. (2003).
- **Wavelet (Morlet)** — Torrence, C., & Compo, G. P. (1998); Aguiar-Conraria
  & Soares (2014).
- **Bry-Boschan / Harding-Pagan** — Bry, G., & Boschan, C. (1971); Harding,
  D., & Pagan, A. (2002).
- **Markov-switching** — Hamilton, J. (1989).
- **PELT** — Killick, R., Fearnhead, P., & Eckley, I. A. (2012).
- **Borio / Drehmann** — Borio, C., & Drehmann, M. (2009).
- **State-space UCM** — Harvey, A. C. (1989); Hamilton, J. D. (2018).
- **Wavelet coherence** — Grinsted, A. et al. (2004).
- **EMD / HHT (rejected)** — Huang, N. E. et al. (1998); mode-mixing
  documented in Wu & Huang (2009).
- **Goldstein long cycles (rejected as primary)** — Goldstein, J. S. (1988).
- **Modelski (rejected as primary)** — Modelski, G. (1996).
