# Composite synthetic indicator

## Two indices, three weightings

The pilot-window pipeline collapses the five per-curve stress percentiles
(E/D/S/L/I) into two diagnostic indices:

| Index | Definition | Role |
|---|---|---|
| **I_intensity** | Weighted mean of the 5 stress percentiles, in [0, 100] | Continuous series on which Models D/E/F/G operate |
| **I_diffusion** | `#{d : stress_d > 80}` over the available curves | Cross-curve coincidence indicator |

A month is `scored` only when at least 3 of 5 curves are available
(`MIN_CURVES_SCORED = 3`); otherwise the row is `blocked`.

Three weighting variants are computed in parallel:

- **equal** — uniform 0.20 per curve. Always defined; default fallback.
- **pca** — first principal component of the rolling 60-month panel,
  absolute-value loadings normalised. `None` when the covariance is
  degenerate.
- **favar** — predictive R² from an anchor regression (FAVAR-style; OECD
  composite leading indicator or G4 GDP-weighted industrial production as
  the exogenous activity anchor). `None` when no curve has predictive content.

Fallback cascade: `favar → pca → equal`. The path taken is logged in
`global_indices.weighting_actual`.

## Smoothing variants

- **MA3** — centred 3-month moving average, the default series fed to
  Models D/E/F/G.
- **HP cycle** — Hodrick-Prescott decomposition with `λ = 129 600` (the
  monthly convention). Used only for the figure overlay and the
  `intensity_hp_cycle` column; *never* an input to the verdict (Hamilton
  2018 shows the HP filter induces spurious cycles).

## References

- Hatzius, Hooper, Mishkin, Schoenholtz & Watson (2010). FAVAR financial
  conditions index.
- Hamilton, J. D. (2018). *Why You Should Never Use the Hodrick-Prescott
  Filter*. The Review of Economics and Statistics.
- Hodrick, R., & Prescott, E. C. (1997). Postwar U.S. business cycles: an
  empirical investigation.
