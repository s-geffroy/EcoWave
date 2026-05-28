# Multi-cycle decomposition — CPV protocol

The CPV method. Decomposes a macroeconomic time-series into the four
canonical cycle bands (Kitchin, Juglar, Kuznets, Kondratieff) using a
combination of band-pass filtering, wavelet analysis, and instantaneous-phase
extraction. The full protocol carries three gates of falsifiability — see
`improvement_roadmap.md` and `cycle_validation_rules.md`.

## Cycle bands (pre-registered, frozen)

| Cycle | Period band (years) | Source |
|---|---|---|
| Kitchin | 3–5 | Kitchin 1923 ; Diebolt & Doliger 2008 |
| Juglar | 7–11 | Juglar 1862 ; Schumpeter 1939 |
| Kuznets | 15–25 | Kuznets 1930 ; Korotayev & Tsirel 2010 |
| Kondratieff | 40–60 | Kondratieff 1925 ; Modelski 1996 ; Korotayev 2010 |

Bounds are frozen in `ecowave/cycles/bands.py:CYCLE_BANDS`. Changes require a
methodology review.

## Step 1 — band-pass filtering (Christiano-Fitzgerald)

Implementation: `ecowave/cycles/decompose.py:cf_bandpass`, wrapping
`statsmodels.tsa.filters.cf_filter.cffilter`.

Why CF rather than HP or Baxter-King:
- CF is asymmetric and full-sample — handles the right endpoint better than
  Baxter-King (which loses `q` samples at each end).
- The Hodrick-Prescott filter, while widely used, has been refuted by Hamilton
  (2018, *"Why You Should Never Use the Hodrick-Prescott Filter"*) for inducing
  spurious cycles. We keep HP only for the diagnostic `intensity_hp_cycle`
  column in `global_indices`, never for the verdict.

Endpoint caveat: the last `hi_years/2` samples are flagged `endpoint_caveat=1`
in `cycle_positions.notes`.

## Step 2 — wavelet decomposition (Continuous Morlet)

Implementation: `ecowave/cycles/decompose.py:morlet_wavelet`, via
`pywt.cwt(..., wavelet="cmor...")`.

Parameters frozen at `ω₀=6.0`, `dj=0.125` (Torrence & Compo 1998 default).
The scaleogram is restricted to the band of interest; band-power is the mean
of |W(s, t)|² across in-band scales. Used to:
1. Verify that the CF band actually carries power (cross-check against Gate 1).
2. Produce a publication-quality figure per group.

The cone-of-influence (`ecowave/cycles/decompose.py:cone_of_influence`)
returns a Boolean mask of reliable samples.

## Step 3 — Hilbert instantaneous phase

Implementation: `ecowave/cycles/phase.py:hilbert_phase`, via
`scipy.signal.hilbert`. The instantaneous phase φ(t) ∈ (-π, π] of the band-
passed signal is mapped to one of four labels (cosine convention, peak at φ=0):

| Quadrant | Label |
|---|---|
| φ ∈ [-π/2, 0) | expansion |
| φ ∈ [0, π/2) | peak |
| φ ∈ [π/2, π] ∪ [-π, -3π/4) | contraction |
| φ ∈ [-3π/4, -π/2) | trough |

Rule frozen in `PHASE_BOUNDS` (in `phase.py`).

## Step 4 — surrogate null (Gate 1, existence)

Implementation: `ecowave/cycles/surrogate.py:ar1_bootstrap_null`.

For each (group, indicator, band), the band-power of the band-passed series is
compared against B=1000 simulated AR(1) red-noise paths with the same mean,
variance, and persistence as the input. If `p ≥ 0.05`, the cycle is not
distinguishable from red noise and the cell is published as `phase = rejected`,
`separable = 0`. Source: Torrence & Compo 1998 ; Grinsted et al. 2004.

## Step 5 — method consensus (Gate 2)

Implementation: `ecowave/cycles/consensus.py:compute_phase_consensus`.

Four models vote: F (CF + Hilbert), G (Bry-Boschan), E (Markov-switching),
D (PELT). The consensus phase is published only when ≥ 3 of 4 agree; otherwise
the cell is `phase = disputed`. Disagreement is information, not a failure
mode to hide.

## Step 6 — cross-group universality (Gate 3)

Implementation: `ecowave/cycles/universality.py:compute_cross_group_concordance`.

A cycle is qualified `universal` for a given month only if ≥ 4 of 5 income
groups (WLD + HIC + UMC + LMC + LIC) share the same modal phase. Otherwise
the cycle is `regional/idiosyncratic` and the universality flag in
`cycle_universality.universal` is 0.

## Variables ingested (WB)

8 indicators in `cycles_manifest.json`, all from World Bank Open Data:

- `NY.GDP.MKTP.KD.ZG` — Real GDP growth
- `NE.GDI.TOTL.ZS` — Gross capital formation, % GDP (Juglar)
- `FP.CPI.TOTL.ZG` — CPI inflation
- `SL.UEM.TOTL.ZS` — Unemployment
- `NE.TRD.GNFS.ZS` — Trade, % GDP
- `SP.URB.TOTL.IN.ZS` — Urban population, % total (Kuznets)
- `FS.AST.PRVT.GD.ZS` — Domestic credit / GDP (long credit cycle)
- `NY.GDP.PCAP.KD` — GDP per capita, constant 2015 USD (Kondratieff)

Aggregation to groups uses official WB aggregate codes (WLD, OED, HIC, UMC,
LMC, LIC) where available, GDP-weighted recompute for G7/G20/BRICS.

## References

- Aguiar-Conraria, L., & Soares, M. J. (2014). The Continuous Wavelet Transform.
- Borio, C., & Drehmann, M. (2009). Towards an operational framework for
  financial stability. *BIS Working Papers*.
- Christiano, L. J., & Fitzgerald, T. J. (2003). The Band Pass Filter.
  *International Economic Review*.
- Diebolt, C., & Doliger, C. (2008). Economic cycles under test.
- Grinsted, A., Moore, J. C., & Jevrejeva, S. (2004). Application of the cross
  wavelet transform.
- Hamilton, J. D. (2018). Why You Should Never Use the Hodrick-Prescott Filter.
- Harding, D., & Pagan, A. (2002). Dissecting the cycle: a methodological
  investigation. *Journal of Monetary Economics*.
- Korotayev, A. V., & Tsirel, S. V. (2010). A spectral analysis of world GDP
  dynamics.
- Torrence, C., & Compo, G. P. (1998). A Practical Guide to Wavelet Analysis.
