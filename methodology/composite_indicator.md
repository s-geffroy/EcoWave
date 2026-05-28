# Composite synthetic indicator — two indices, three weightings

## Why two indices, not one

EcoWave's grammar (`dow_elliott_adaptation.md`) treats a wave as real *only if
independent curves confirm a phase change*. Collapsing the five E/D/S/L/I
stress percentiles into a single composite (e.g. CISS-style with EWMA cross
correlations) folds **intensity** and **diffusion** into one number, which
makes the "confirmed by independent curves" criterion invisible. We keep them
separate:

| Index | Definition | Role |
|---|---|---|
| **I_intensity** | Weighted mean of the 5 stress percentiles, in [0, 100] | The continuous series on which Elliott waves are detected |
| **I_diffusion** | `#{d : stress_d > 80}` over the available curves | Confirmation filter: an Elliott wave is `confirmed` only if `diffusion ≥ 3` at the wave's terminal pivot |

Minimum gate: a month is `scored` only if at least 3 of the 5 curves are
available, consistent with the methodological warning in the README that the
verdict stays provisional until S and I are populated.

## Three weighting variants (computed in parallel)

The JRC-OECD Handbook (Nardo et al. 2008, §weighting) explicitly recommends
presenting several weighting schemes when no canonical choice is forced by
theory. EcoWave publishes three.

### `equal` — reference

Each curve gets weight `1/5 = 0.20`. This is the variant rendered in reports
and used as the canonical Elliott input. It carries no a-priori, is fully
auditable, and is unaffected by data revisions.

### `pca` — empirical co-movement

Loadings of the first principal component (PC1) of a rolling 60-month window
of the 5 stress percentiles, normalised in absolute value to sum to 1.
Captures the dominant common factor; if the `pca` weights diverge markedly
from `equal`, that is a diagnostic signal that one curve is dominating
empirically (worth investigating). Degraded to a 36-month window when the
pilot's history is short; if the covariance matrix is degenerate, falls back
to `equal`.

### `favar` — predictive content

Bernanke, Boivin & Eliasz (2005) FAVAR, restricted to a univariate "anchor
regression" specification à la Hatzius et al. (2010) / GS-FCI:

```
anchor_{t+h} = a_d + Σ_{k=0}^{K} b_{d,k} · stress_{d, t-k} + ε
```

with `h = 6` months, `K = 2` lags, rolling 60-month window. The weight on
curve `d` is its in-sample R², clipped at 0 and normalised across curves. The
anchor **must be exogenous to the 5 curves** to avoid circularity, so neither
E4 (GDP) nor L2 (world trade) of the panel is reused.

**Anchor priority cascade** (`ecowave/ingest/anchors.py`):

1. **FRED `OECDLOLITONOSTSAM`** — OECD + Major 6 NME composite leading
   indicator, normalised, SA, monthly. Broad global coverage.
2. **G4 industrial production composite** — GDP-weighted average of `INDPRO`
   (US), `PRMNTO01EZQ661N` (EA), `JPNPROINDMISMEI` (JP), `GBRPROINDMISMEI`
   (UK), weights from 2007 nominal GDP (World Bank).
3. **FRED `IGREA`** — Kilian (2009) Index of Global Real Economic Activity.

Each candidate series is transformed to YoY growth, standardised, and
sign-flipped so that contractions push the anchor up (`higher_is_stress`
convention).

### Fallback chain when FAVAR is not available

```
favar -> pca -> equal
```

The column `weighting_actual` in the `global_indices` table records the path
actually taken (e.g. `favar->pca` if FAVAR returned `None` and PCA was used,
or `favar` if FAVAR resolved). This keeps the published `weighting` label
stable while making the runtime substitution auditable.

## Smoothings for Elliott

Three views of `I_intensity` are persisted side-by-side:

- **raw**: monthly weighted mean — used for headline charts.
- **MA3**: centered 3-month moving average — primary input for Elliott
  detection (removes high-frequency noise without phase distortion).
- **HP cycle + trend**: Hodrick-Prescott with `λ = 129 600` (standard for
  monthly data). The **cycle** component is a second Elliott input; the
  **trend** is intended for a Dow-style structural regime read.

## Elliott on the composite — confirmation rule

`ecowave/scoring/elliott_on_composite.py` enumerates alternating trough-peak
pivots on the smoothed series, applies canonical constraints (wave 2 doesn't
undercut the impulse start, wave 4 doesn't overlap wave 1, wave 3 isn't the
shortest of 1/3/5, wave 5 makes a new high) and selects the candidate with
the largest total amplitude. Each wave's terminal pivot is annotated with
`diffusion_at_end`; the wave is `confirmed=True` only if
`diffusion_at_end ≥ 3`. This is the literal quantification of the rule "a
wave exists only if independent curves confirm". Outputs are persisted to
the `elliott_waves` SQLite table and rendered in
`figures/global_indices_{pilot}.png`.

## Why these choices, in literature terms

The setup matches the JRC-OECD Handbook's recommended *transparent +
multiple-weighting* posture, while plugging in a Hatzius/GS-FCI predictive
calibration for `favar` and a Holló-Kremer-Lo-Duca-style **diffusion** signal
(without their EWMA cross-correlation aggregation, which would re-merge the
two indices). Mahalanobis turbulence (Kritzman-Li) was considered and
rejected — it produces sharp spikes that defeat Elliott impulse detection.
The orthodox FAVAR (multi-equation VAR + IRF/FEVD) was rejected for a
5-variable panel: it would be over-parameterised.

## References

- Bernanke, B., Boivin, J. & Eliasz, P. (2005). *Measuring the Effects of
  Monetary Policy: A FAVAR Approach.* QJE.
- Hatzius, J., Hooper, P., Mishkin, F., Schoenholtz, K. & Watson, M. (2010).
  *Financial Conditions Indexes: A Fresh Look after the Financial Crisis.*
  NBER WP 16150.
- Holló, D., Kremer, M. & Lo Duca, M. (2012). *CISS — A Composite Indicator
  of Systemic Stress in the Financial System.* ECB WP 1426.
- Kilian, L. (2009). *Not All Oil Price Shocks Are Alike: Disentangling
  Demand and Supply Shocks in the Crude Oil Market.* AER.
- Nardo, M. *et al.* (2008). *Handbook on Constructing Composite Indicators:
  Methodology and User Guide.* OECD-JRC.
- Hodrick, R. & Prescott, E. (1997). *Postwar U.S. Business Cycles: An
  Empirical Investigation.* JMCB.
