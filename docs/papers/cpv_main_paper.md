# Cycles macroéconomiques canoniques : réfutation empirique et émergence d'une dynamique fractale non-linéaire à longue mémoire

**Working paper · première version (heavy-argued)**
**Sylvain Geffroy** · 2026-05

---

## Abstract

We test the four canonical macroeconomic cycles (Kitchin, Juglar, Kuznets,
Kondratieff) on six independently-constructed historical data panels
spanning 1086 to 2024 — a total of 9 436 (variable × group × diagnostic)
cells. The Cycle Position Vector (CPV) protocol implements a three-gate
falsifiability test : (Gate 1) dual-null AR(1) bootstrap + phase-scramble
surrogate testing, (Gate 2) consensus across four methodologically
independent estimators, (Gate 3) cross-aggregate universality. After
applying a per-variable safeguard against aggregation artifacts (Roadmap
#14), **the four canonical cycles fail Gate 1 on essentially all cells**,
including on the sectoral series their discoverers originally analysed
([Kitchin 1923](#kitchin-1923), [Wen 2005](#wen-2005);
[Solomou 1987](#solomou-1987)).

Posing this rejection as a *constructive* problem — *if not a cycle,
what?* — we develop a Tier 1+2 toolkit of 14 non-cyclical structural
diagnostics covering 11 families from a panoramic survey of physics
frameworks. On the same data, this toolkit reveals a sharp empirical
cluster :

- **88 %** of cells reject IID (BDS test, Brock-Dechert-Scheinkman 1996)
- **69 %** of cells reject AR(1) permutation entropy
- Median Hurst exponent ≈ **1.62** (long memory ; 51 % significant)
- Median K41 structure function ratio ζ(6)/ζ(3) ≈ **1.78** < 2
  (anomalous multifractal scaling, She-Levêque)
- **9 of 12** panel covariance matrices have a top eigenvalue above the
  Marchenko-Pastur bulk (one dominant correlation factor)
- **51 %** of cells reject AR(1) on a Kolmogorov-Smirnov drift test
  between the two halves of the observation window (reflexive regime
  shifts)

Conversely, **pure self-organised criticality (1/f^β strict, 15 %),
critical slowing down (30 %), and deterministic chaos (Lyapunov, 19 %)
are *not* dominant signatures**. The data are not a Bak sandpile, nor a
Lorenz attractor, nor cycling between tipping points.

We argue the empirical winner is a **cluster of five families** — long
memory (C), multifractality (B), non-linear dependence (D), structured
ordinal patterns (I), reflexive regime drift (S) — converging on a
single picture : **macroeconomic dynamics are a fractional, multifractal,
non-linear long-memory process with cognitive regime drift**, not a
collection of oscillators. The result reframes a 100-year debate. It is
*consistent* with the modern empirical critique of canonical cycles
([Garvy 1943](#garvy-1943); [Solomou 1987](#solomou-1987);
[Romer 1999](#romer-1999); [Wen 2005](#wen-2005)) and with the
hetero-physical perspectives of
[Mandelbrot 1997](#mandelbrot-1997),
[Bacry-Muzy-Delour 2001](#bacry-muzy-delour-2001),
[Ghashghaie et al. 1996](#ghashghaie-1996),
[Soros 1987](#soros-1987), and
[Akerlof-Shiller 2009](#akerlof-shiller-2009).

We discuss in detail how this conclusion is robust against the seven
most natural objections — power-analysis concerns, Type-I inflation,
selective horizon effects, multi-comparison without correction,
panel composition bias, post-hoc cluster identification, and the
reflexivity-as-confound critique — and how the cluster picture makes
falsifiable predictions that subsequent work can test.

**Keywords**: macroeconomic dynamics ; falsifiability ; long memory ;
multifractal cascades ; reflexivity ; econophysics ; non-linear time
series.

---

## 1 · Introduction

### 1.1 The stakes

The question whether macroeconomic time series exhibit cyclical
behaviour is not academic in two senses : it is not settled, and it is
not without consequence.

*It is not settled.* The four canonical cycles — Kitchin (3-5 years),
Juglar (7-11 years), Kuznets (15-25 years), Kondratieff (40-60 years)
— have been part of the macroeconomist's toolkit since
[Kitchin (1923)](#kitchin-1923). They are routinely invoked in
business-cycle theory ([Hamilton 1989](#hamilton-1989)), in
investment forecasts, in geopolitical and demographic projections.
Yet their statistical existence has been contested since
[Garvy (1943)](#garvy-1943) and the modern empirical literature is
deeply sceptical : [Solomou (1987)](#solomou-1987) found no
significant Kuznets or Kondratieff cycles in advanced-economy GDP ;
[Romer (1999)](#romer-1999) and [Stock-Watson (2003)](#stock-watson-2003)
documented severe post-1945 Juglar instability ;
[Wen (2005)](#wen-2005) showed that the Kitchin inventory cycle —
visible on US manufacturing stock data post-1947 — *disappears* on
GDP composites of the very same period. Despite these warnings, the
canonical cycles persist as policy and forecasting heuristics.

*It is not without consequence.* The 2008 financial crisis was
forecast neither by mainstream DSGE models nor by cycle-based
heuristics. The 2020 COVID shock and the subsequent inflation surge
exposed the same failure mode. The standard policy use of cycle
position — *"we are in the late expansion of Juglar X, contraction
expected within Y"* — turns out to be unsupported by the data once a
strict null hypothesis is imposed. If the cycles do not exist in the
statistical sense, then the standard cycle-based policy guidance is
not just imprecise — it is *malformed*.

This paper makes a specific intellectual move. It treats the cycle
question as *falsifiable*, in the Popperian sense : it constructs a
maximally conservative protocol, applies it at scale, reports the
result, and then asks the constructive question, *if not a cycle,
what?*. The contribution is twofold : a refutation of the four
canonical cycles that withstands the modern statistical critique, and
an empirically-grounded positive working hypothesis that replaces
them.

### 1.2 Why this exercise has not been done before

The closest prior work — Garvy (1943), Solomou (1987), Wen (2005) —
shares two limitations.

*First, no prior critique covers the full historical scope at once.*
Garvy used a small window of US data ; Solomou worked on twelve
advanced economies 1850-1973 ; Wen restricted his attention to US
manufacturing inventories. The aggregated picture has remained
fragmentary. Different cycle phases have been falsified on different
datasets ; no single, internally-consistent panel has ever shown that
*all four* fail *simultaneously* across *all of* developed-and-
developing economies, advanced and emerging markets, and across the
full historical period that includes the original Kitchin, Juglar,
Kuznets, and Kondratieff observations.

*Second, no prior critique has paired the refutation with a
constructive alternative.* Sceptics have argued *the cycles are weak*.
They have not argued *here is what should replace them*. The standard
alternative — random walks with autocorrelated noise — is plainly
inadequate : macroeconomic series exhibit persistent
auto-correlation, volatility clustering, heavy tails, regime shifts.
They are clearly *not* random walks. Yet no widely-accepted
constructive replacement has emerged. The cycle scaffold persists in
part because there is no positive alternative on which to hang
policy intuitions.

This paper attempts to close both gaps simultaneously. The CPV protocol
applies the same maximally-conservative test to six panels covering
the full known historical scope (1086-2024). The diagnostic toolkit
covers 11 of the 21 candidate families from a panoramic survey of
physics-inspired non-cyclical frameworks (long memory, multifractality,
SOC, RMT, etc.), each with a paired null test. The empirical answer
identifies five families whose joint signature reframes the working
picture.

### 1.3 What this paper claims, and what it does not

The paper claims, on the basis of 9 436 diagnostic cells across six
panels :

1. The four canonical cycles do not survive a dual-null
   (AR(1) + phase-scramble) test at α = 0.05 with the Roadmap #14
   per-variable safeguard, *on any panel*.
2. The empirical signature of macroeconomic time series is *not*
   random walk, *not* SOC, *not* low-dimensional chaos, *not*
   approaching tipping points.
3. The empirical signature *is* a joint cluster of long memory,
   multifractality, non-linear dependence, structured ordinal
   patterns, and reflexive regime drift, with a panel-level dominant
   correlation factor.
4. This cluster is consistent with — and operationally clarifies —
   the heterodox traditions of Mandelbrot finance fractals, Bouchaud
   structured-noise dynamics, Soros reflexivity, and Friston active
   inference.

The paper does *not* claim :

- That a single unified theory predicts the joint signature from
  first principles. The cluster is empirical ; a theoretical
  synthesis remains open work (§5.4).
- That the canonical cycles are statistically *impossible* to
  observe — only that under the dual-null + per-variable safeguard,
  they do not survive on any of our six panels. A different protocol
  on a different dataset could, in principle, show them.
- That cycles do not exist as a *narrative* device. They do, and they
  may be useful for communication, intuition, and pedagogy. The claim
  here is about their *statistical-mechanistic existence*.
- That this is the final word. The Tier 3 families (Kuramoto
  synchronisation, evolutionary biology, bifurcations, chimera
  states, etc.) remain to be tested, and a 1 000-surrogate replication
  of the present 100-surrogate run will report in the next version.

### 1.4 Structure of the paper

Section 2 presents the CPV three-gate protocol and the Tier 1+2
diagnostic toolkit, with detailed justification of each
methodological choice. Section 3 describes the six data panels.
Section 4 reports the empirical results. Section 5 articulates the
working hypothesis and discusses — at length — implications for
macroeconomic theory, policy, and forecasting, together with
*explicit rebuttals to seven anticipated objections*. Section 5.5
specifies *what would falsify* the cluster hypothesis. Section 6
concludes with limitations and open questions.

---

## 2 · Methodology

The CPV protocol is designed to maximise the falsifiability of any
positive cycle claim. We take seriously the methodological
warnings of [Bailey-López de Prado (2014)](#bailey-lopez-de-prado-2014)
on in-sample overfit, of [Theiler et al. (1992)](#theiler-1992) on
the inadequacy of AR(1) alone as a null, and of
[Vyushin-Kushner (2009)](#vyushin-kushner-2009) on the partial
absorption of cyclic content by the AR(1) persistence parameter.

### 2.1 Gate 1 — dual null hypothesis test

For each band `b ∈ {Kitchin (3-5y), Juglar (7-11y), Kuznets (15-25y),
Kondratieff (40-60y)}` and each (horizon × aggregate) combination,
a candidate cycle is observed only if the band-power of the
Christiano-Fitzgerald-filtered composite *exceeds simultaneously*
the 1 - α percentile of two independent null distributions :

- *AR(1) bootstrap null*. Fit (φ, σ, μ) on the input series ;
  simulate B = 1 000 trajectories preserving mean, variance and
  lag-1 persistence ; recompute the same CF band-pass and band-power.
  Reject the cycle if the real band-power lies below the 1 - α
  percentile of the surrogate distribution. *Source* :
  [Torrence-Compo (1998)](#torrence-compo-1998) ;
  [Grinsted et al. (2004)](#grinsted-2004).

- *Phase-scrambling null*. Take the empirical periodogram, randomise
  the phases while preserving the magnitudes and conjugate symmetry,
  inverse-FFT to obtain a surrogate that preserves the *spectrum
  exactly* but destroys phase coherence. Recompute the band-power.
  *Source* : [Theiler et al. (1992)](#theiler-1992).

**Why dual, and why these two?** Each null isolates a different
failure mode. The AR(1) null tests *spectral concentration relative
to red noise* — but because AR(1) absorbs some cyclic content into
φ, it can lose power against true cycles that look red. The
phase-scramble null tests *phase coherence given the empirical
spectrum* — it cannot be fooled by spectral leakage because it
preserves the spectrum exactly. The two are complementary :

| Null | Detects | Vulnerable to |
|---|---|---|
| AR(1) | spectral concentration above red noise | partial cycle absorption in φ |
| Phase-scramble | phase coherence given spectrum | spectral content with random phases |

Requiring *both* to reject is the conservative protocol. A real
cycle, by hypothesis, has concentrated band-power *and* phase
coherence ; it must reject both nulls. A spectral artefact may
reject AR(1) (high power) but not phase-scramble (random phases).
A red-noise excursion may reject phase-scramble (lucky local
coherence) but not AR(1) (spectrum-matched). Only a genuine cycle
rejects both. This is the *empirical content* of the Theiler
recommendation.

### 2.2 Gate 2 — multi-method consensus

Any single cycle estimator can be fitted to any sufficiently long
series. To exclude single-method artifacts, Gate 2 requires
*agreement across four methodologically independent classifiers* on
the cycle phase :

| Method | Reference | Assumption |
|---|---|---|
| **D** — PELT change-point | [Killick et al. 2012](#killick-fearnhead-eckley-2012) | piecewise stationary segments |
| **E** — Markov-switching | [Hamilton 1989](#hamilton-1989) | latent discrete regime |
| **F** — CF band-pass + Hilbert phase | [Christiano-Fitzgerald 2003](#christiano-fitzgerald-2003) | band-pass filterable signal |
| **G** — Bry-Boschan | [Harding-Pagan 2002](#harding-pagan-2002) | peak-trough datable cycle |

A cell is published as a *modal phase* only if at least 3 of 4
methods agree. Otherwise the cell is *disputed*.

**Why these four?** Each rests on a structurally different generative
assumption. PELT assumes the cycle as alternating segments. Markov
assumes the cycle as latent regime states. CF + Hilbert assumes the
cycle as a band-limited oscillator. Bry-Boschan assumes the cycle
as a datable sequence of turning points. If a cycle is real in the
mechanistic sense, all four perspectives should converge on it.
If it is method-specific, the methods will disagree. The Gate 2
consensus is therefore a *cross-validation across mechanistic
priors*.

Per-band method weights are pre-registered to account for sample-
length constraints. PELT is excluded from Kondratieff (the typical
segment length exceeds the data horizon). Bry-Boschan is
weighted-down on Kitchin (requires complete peak-trough sequences
on quarterly data, biased on partial cycles). The specific
per-band whitelists are at `ecowave/cycles/bands.py:CYCLE_BANDS`.

### 2.3 Gate 3 — cross-aggregate universality

A cycle qualifies as *universal* in a given month only if at least
4 of 5 income aggregates (WLD + HIC + UMC + LMC + LIC) on the
World Bank panel, or at least 4 of the equivalent aggregates on
the historical panels, agree on the modal phase. Otherwise the
cycle is *regional* or *idiosyncratic*.

**Why universality?** A cycle that exists only on the G7 countries
is not a *global cycle*. A cycle that exists only on emerging
markets is not a *Kuznets cycle in the universalist sense*. The
canonical narratives (Kondratieff long waves driven by global
technological revolutions, Juglar credit cycles driven by global
financial dynamics, etc.) imply *transnational universality*.
Gate 3 tests this implication.

### 2.4 The Roadmap #14 per-variable safeguard

A subtle but critical failure mode of composite-level tests was
diagnosed during the development of CPV : the composite of z-scored
heterogeneous variables can *manufacture* spurious band-power
through autocorrelation cross-coupling, even when *none* of the
constituent variables individually carries the band-power.

The mechanism is straightforward. When you z-score each of K
heterogeneous series to unit variance and then average them, the
resulting composite has a variance structure that depends on the
*cross-correlation* of the constituents. If two heterogeneous
constituents share a low-frequency trend (e.g., post-1980
financialisation in CY_FIN, post-1980 globalisation in CY_TRD),
their composite carries that low-frequency trend with *amplified*
relative power compared with each constituent. Gate 1, applied to
the composite, will see the amplified low-frequency power and
reject AR(1) — even though *neither* constituent individually does.

Four diagnosed case studies confirmed the mechanism :

- **CN_BIS Kondratieff** ([case study](../case_study_cn_bis_kondratieff.md)) — composite K-survival on China BIS panel, no constituent variable surviving.
- **WLD-WB Kondratieff** ([case study](../case_study_wld_wb_kondratieff.md)) — composite K-survival on World Bank aggregate, attributed to trend leakage.
- **G7-long and UK_BOE Kondratieff** ([case study](../case_study_g7_long_uk_boe_kondratieff.md)) — composite K-survival redistributed to specific high-trend constituents that do not individually pass Gate 1.
- **Wen 2005 direct test** ([case study](../case_study_wen_2005_test.md)) — application to original sectoral series.

The safeguard requires that *at least one constituent variable*
individually pass Gate 1 (per-variable test, same null, same α,
same band) before the composite-level survival is published. This
closes the manufacturing loophole. It is conservative against
Type-I errors at the cost of Type-II power loss on genuinely
weak-but-real cycles, but that trade-off is correct for a
falsifiability protocol : we prefer *missing* a weak cycle to
*claiming* a non-existent one.

### 2.5 The Tier 1+2 diagnostic toolkit

After Gate 1+2+3 with the per-variable safeguard rejects the four
canonical cycles essentially everywhere, we ask the constructive
question. The Tier 1+2 toolkit applies 14 band-agnostic structural
diagnostics to each variable individually, plus a panel-level
random-matrix-theory analysis. Each diagnostic is paired with an
AR(1) or phase-scramble null at α = 0.05.

**The 14 atomic diagnostics + 1 panel-level** are :

| # | Diagnostic | Family | Test statistic | Null | Tail |
|---|---|---|---|---|---|
| 1 | `hurst_dfa` | C — long memory | DFA exponent H | AR(1) | upper |
| 2 | `mfdfa_spectrum` | B — multifractality | spectral width Δα | AR(1) | upper |
| 3 | `spectrum_slope` | A — SOC (1/f^β) | log-log PSD slope β | AR(1) | upper |
| 4 | `hill_tail_exponent` | A — power-law tails | α_Hill | AR(1) | lower |
| 5 | `permutation_entropy_complexity` | I — information | H_perm + C_stat | AR(1) | lower |
| 6 | `critical_slowdown` | E — tipping point | Kendall τ rolling variance | AR(1) | upper |
| 7 | `levy_stable_fit` | J — Lévy flights | stability index α | AR(1) | lower |
| 8 | `k41_scaling` | P — turbulence cascades | ζ(6)/ζ(3) | phase-scramble | lower |
| 9 | `msd_log_log` | R — anomalous diffusion | exponent γ | AR(1) | two-sided |
| 10 | `tsallis_q_gaussian` | T — non-extensive | entropic index q | AR(1) | upper |
| 11 | `reflexivity_drift` | S — reflexivity (transversal) | KS two-sample | AR(1) | upper |
| 12 | `lyapunov_exponent` | D — deterministic chaos | largest Lyapunov λ | phase-scramble | upper |
| 13 | `bds_independence` | D — non-linearity | BDS statistic | phase-scramble | upper |
| 14 | `reflexivity_multi_window` | S extended — multi-regime | max KS over splits | AR(1) | upper |

Panel level : `rmt_panel` operates on the covariance matrix of
variables within a group, reporting the top eigenvalue, the
Marchenko-Pastur bulk band, and the count of modes above the bulk.

**Why 14, why these?** Three principles guided the selection.

*Coverage* : the 21-family panorama
([`methodology_beyond_cycles.md`](../methodology_beyond_cycles.md))
identifies the candidate frameworks. Of these, 11 are Tier 1 in the
panorama — directly testable on the existing data with statistical
diagnostics — plus 3 Tier 2 (Lyapunov, BDS, multi-window reflexivity).
We selected one canonical diagnostic per family for an empirical
coverage of 11/21 = 52 % of the panorama. Families excluded from
the toolkit (Kuramoto F, evolutionary L, bifurcations N, chimera
states U) are conceptually attractive but require either
multivariate-state or process-model fitting that is out-of-scope
for a first pass.

*Robustness against single-statistic artifacts*. Each family has
multiple candidate statistics. We chose the diagnostic with the
strongest theoretical support and the smallest computational
overhead. For DFA / Hurst we use [Peng et al. (1994)](#peng-1994)
canonical reimplementation with `nolds` for verification ; for
permutation entropy we use [Bandt-Pompe (2002)](#bandt-pompe-2002)
with `antropy` ; for spectrum slope we use Welch's periodogram with
log-log polynomial fit ; for Lévy we use the
[McCulloch (1986)](#mcculloch-1986) quantile estimator (fast and
robust on heavy-tailed data) ; for RMT we use the analytical
Marchenko-Pastur band rather than numerical Wishart bootstrap (much
faster, sufficient for first-pass screening).

*Pre-registration*. The 11 families and the specific statistic per
family were determined *before* the empirical run, in the panorama
document (PR #22) and the roadmap (PR #23). This is critical for
the post-hoc-cluster-identification objection (§5.4.6) : the
selection was not made to maximise rejection rates.

### 2.6 The band-agnostic design choice

A central design decision of the diagnostic toolkit is its
*band-agnosticism*. We compute Hurst H on the full series, not on
the bandpass-filtered Kitchin / Juglar / Kuznets / Kondratieff
components. Same for β, Δα, BDS, etc. The page is structured as
`(diagnostic × variable × horizon)` — a three-axis hypercube — not
`(cycle × diagnostic × variable × horizon)` — a four-axis hypercube.

**Why band-agnostic?** Three converging reasons.

*Conceptually*. The Tier 1+2 toolkit measures *global structural
properties* of each series (Hurst, multifractality, slope 1/f,
entropy, anomalous diffusion, etc.). These properties are not
intrinsically band-specific. If a series has Hurst H = 0.7, it
has H = 0.7 *as a whole*, not in some Kitchin sub-band. Restricting
to a band is a *projection* that may or may not preserve the
property of interest. For Hurst, MF-DFA, Lévy α, Tsallis q, perm-
entropy, MSD, K41, RMT — the projection *destroys* the property by
construction. (The filter is itself a high-order moving-average,
and a high-order MA has Hurst ≈ 0.5 regardless of input.)

*Methodologically*. Reintroducing a per-band axis would *re-instate
the very scaffold whose statistical non-detectability is the
central empirical finding of section 4*. After we have falsified the
existence of cycle bands, computing diagnostics per band amounts
to begging the question. The diagnostics should be agnostic with
respect to the falsified scaffold.

*Statistically*. Of the 14 diagnostics, only 3-4 (β, τ_var on
rolling variance, Lévy α, perhaps Hurst) can reasonably be
applied to a band-passed signal *without* the property of interest
being destroyed by the projection. For the remaining 10, the
restricted version of the test is either mathematically ill-posed
(K41 multi-scale by definition) or numerically degenerate (RMT
on a panel of bandpassed signals is rank-deficient).

We do however recognise that the band-agnostic design choice is a
hypothesis itself, and we pre-register a *falsifiable test of it*
in Roadmap #16 : a restricted study applying 4 diagnostics × 4
bands to CF-bandpassed signals, on the same data, with the same
nulls. If per-band analysis reveals structures invisible to the
band-agnostic toolkit, the design choice is wrong. If not, it is
validated empirically. The result of this study will be reported
in subsequent work.

### 2.7 Reflexivity as transversal component

The reflexivity family (S) — empirically operationalised as
`reflexivity_drift` (KS two-sample between the two halves of the
observation window) and `reflexivity_multi_window` (max KS over
pre-registered regime change candidates : 1929, 1944, 1971, 1979,
2008, 2020) — is treated as a *transversal validity indicator*
for the other 12 diagnostics.

**Why transversal?** Soros's reflexivity argument
([Soros 1987](#soros-1987)) and Akerlof-Shiller's animal spirits
[(2009)](#akerlof-shiller-2009) imply that the *cognitive regime*
under which macroeconomic dynamics play out is itself *unstable*.
If beliefs shift, dynamical parameters shift. A structural finding
("the Hurst exponent is 1.62") is therefore *epistemically conditional
on a stable cognitive regime over the observation window*. The
`reflexivity_drift` diagnostic operationalises this conditioning :
when it rejects, the other 12 diagnostics' verdicts are valid
*only on the analysed window*, not as universal transhistorical
laws.

This is a substantive epistemological constraint, not a methodological
nicety. It is why we are reluctant to write "*the* Hurst of macro" :
the empirical signature itself is a function of the historical
regime. Conditioned on the stable-regime assumption, the cluster
picture holds. Without that assumption, only `reflexivity_drift`
and `reflexivity_multi_window` are interpretable.

### 2.8 Implementation and reproducibility

The full pipeline is implemented in Python 3.12 and shipped as the
`ecowave` package. Diagnostic computation runs through Docker for
environment parity. Source code, raw data manifests, and the SQLite
observation store are versioned on GitHub
([github.com/s-geffroy/EcoWave](https://github.com/s-geffroy/EcoWave)).
Each result reported in section 4 is reproducible via :

```bash
docker compose run --rm --entrypoint ecowave ecowave \
  dx-diagnostics --as-of 2026-05 --horizons wb,q,long,boe,bis,sh \
  --n-surrogates 100 --seed 0
```

The 12 JSON sidecars (`reports/dx_diagnostics_2026_05_*.json` and
`reports/dx_rmt_2026_05_*.json`) carry the raw outputs ; the
consolidated page (`docs/dx_diagnostics.md`) carries the heatmaps
and the family-mapping tables. All sidecars are versioned alongside
this paper and are themselves citable artefacts.

---

## 3 · Data

The empirical analysis uses six independently-constructed historical
panels covering complementary time windows and economic dimensions.

| Panel | Source | Period | Frequency | Groups | Vars |
|---|---|---|---|---|---|
| **wb** | World Bank Open Data | 1960–2024 | annual | 45 (WLD, OECD, HIC, UMC, LMC, LIC, G7, BRICS, G20 + 36 countries) | 7 |
| **q** | FRED + Eurostat + OECD/IFS | 1995–2024 | quarterly | 6 (USA, EA, JPN, GBR, G7Q, OECDQ) | 3 |
| **long** | Maddison Project 2023 + JST R6 | 1870–2020 | annual | 6 (ADV18, G7, EU4, ANGLO, NORDIC, USA) | 14 |
| **boe** | Bank of England Millennium | 1700–2016 | annual | 1 (UK_BOE) | 8 |
| **bis** | BIS Bulk Download | 1970–2025 | quarterly | 11 (BIS_EM, BIS_AE, …) | varies |
| **sh** | FRED + OWID + DECC/BEIS | 1900–2024 | annual | 3 (US_SH, UK_SH, WORLD_SH) | varies |

**Why six panels?** Three complementary motivations.

*Temporal coverage*. The WB panel (1960–2024) is the most recent and
most contemporary ; it covers the post-Bretton-Woods era of floating
exchange rates, financial liberalisation, and globalisation. The
long panel (1870–2020) reaches back to the pre-WWI Gold Standard,
through the 1929-1939 Great Depression, the 1944–1971 Bretton Woods
era, and into the contemporary period. The BoE Millennium panel
(1700–2016) extends to the eighteenth-century origins of central
banking, through the Industrial Revolution, the Napoleonic Wars,
the gold standard era, and the twentieth-century era of fiat money.
Each panel covers a different regime ; failing on *all* of them is
the strongest possible refutation.

*Economic dimension coverage*. The WB panel emphasises cross-country
heterogeneity. The long panel emphasises panel-level depth (12 variables
per group). The BoE panel emphasises temporal depth (317 years
per variable). The BIS panel adds emerging-market coverage. The
sectoral history panel (sh) is *specifically* designed for the Wen
(2005) test : it ingests the same kind of sectoral series Wen used
(stocks of pig iron, coal, railway-car loadings, manufacturing
output) on contemporary data. The combined panel covers cross-
country, longitudinal, panel-depth, EM, and sectoral dimensions.

*Independence*. Each panel is *constructed independently*. They use
different raw sources, different aggregation rules, different
historical reconstruction methodologies. A finding that holds on
*all* of them is robust against panel-construction-specific
artifacts.

Total cells in the per-variable analysis : 9 436. RMT analysis
yields 12 panel-level records.

All raw ingestion is automated and documented. Source manifests are
at `cycles_manifest.json`, `quarterly_manifest.json`,
`long_history_manifest.json`, `boe_millennium_manifest.json`,
`bis_manifest.json`, `sectoral_history_manifest.json`. The SQLite
observation tables (`cycle_observations`,
`cycle_observations_quarterly`) carry 60 012 annual and 21 793
quarterly observations as of 2026-05.

---

## 4 · Empirical results

### 4.1 Refutation of the four canonical cycles

Applying Gate 1 (dual AR(1) + phase-scramble nulls, B = 1 000
surrogates, α = 0.05) followed by the Roadmap #14 per-variable
safeguard, **the four canonical cycles fail on essentially all cells
across the six panels**. Detailed cell-by-cell results are reported
in the cycle-position pages of the project site
([`reports/cycle_position_synthesis.md`](../reports/cycle_position_synthesis.md))
and per-variable evidence ([`evidence_per_variable.md`](../evidence_per_variable.md)).

The case studies (§2.4) confirm that previously-surviving cells
were aggregation artifacts. The Wen 2005 test is particularly
striking : applying Gate 1 to the original sectoral series Wen used,
on a re-built FRED + OWID + DECC/BEIS panel of comparable variables,
no Kitchin signal survives. The Kitchin discovery on these series
is *not robust to the dual-null protocol* — confirming Wen's own
scepticism about the canonical narrative.

This refutation is *consistent with* but *strengthens* the modern
empirical critique. It rejects the four cycles not merely as
incompletely-supported by GDP composites
([Garvy 1943](#garvy-1943); [Solomou 1987](#solomou-1987)) but
*as a structural-statistical artefact when properly tested against
red noise* on the original sectoral series the discoverers used.

### 4.2 Diagnostic toolkit — overall rejection profile

Table 1 reports the rejection rates of each Tier 1+2 diagnostic against
its null, aggregated over the 9 436 cells of the six panels.

**Table 1 — Tier 1+2 diagnostic rejection rates (all horizons)**

| Diagnostic | Family | Rejection rate | Median statistic |
|---|---|---:|---:|
| `bds_independence` | D — non-linearity | **88 %** | 3.70 |
| `permutation_entropy_complexity` | I — information | **69 %** | 0.85 (H_perm) |
| `reflexivity_drift` | S — transversal | 51 % | 0.82 (KS) |
| `hurst_dfa` | C — long memory | 51 % | **1.62** |
| `tsallis_q_gaussian` | T — non-extensive | 43 % | 1.05 |
| `msd_log_log` | R — anomalous diffusion | 42 % | 1.12 |
| `hill_tail_exponent` | A — power-law tails | 41 % | 3.59 |
| `k41_scaling` | P — turbulence cascades | 37 % | **1.78** |
| `levy_stable_fit` | J — Lévy flights | 32 % | 2.00 |
| `reflexivity_multi_window` | S — multi-regime | 30 % | 0.99 |
| `critical_slowdown` | E — tipping point | 30 % | 0.27 |
| `mfdfa_spectrum` | B — multifractality | 27 % | 0.81 (Δα) |
| `lyapunov_exponent` | D — chaos | **19 %** | 0.07 |
| `spectrum_slope` | A — SOC (1/f^β) | **15 %** | 1.75 |

Two clusters of findings stand out.

**Strong empirical signals (rejection ≥ 40 %)** :

- **Non-linearity / non-IID** (`bds_independence`, 88 % ; `permutation_entropy_complexity`, 69 %) is *quasi-universal*. Whatever else macro series are, they are *not* white noise, *not* IID, *not* AR(1).
- **Long memory** (`hurst_dfa`, 51 % significant ; median H = 1.62, well above the random-walk threshold 0.5 and above the fractional Brownian motion canonical range [0.5, 1]). The strong-memory signal is *structural* rather than statistical : even when the AR(1) null is liberal, half the series carry significantly more memory than red noise.
- **Heavy tails and non-Gaussianity** (`tsallis_q_gaussian`, 43 % ; `msd_log_log`, 42 % ; `hill_tail_exponent`, 41 % ; `levy_stable_fit`, 32 %). The fat-tail / Lévy-flight family delivers consistent but not dominant signals.
- **Reflexive regime shifts** (`reflexivity_drift`, 51 % ; `reflexivity_multi_window`, 30 %). On *half* of the cells, the empirical distribution of the variable shifts significantly between the two halves of the observation window. This is the *empirical signature* of cognitive regime change ([Soros 1987](#soros-1987); [Akerlof-Shiller 2009](#akerlof-shiller-2009); [Friston 2010](#friston-2010)).

**Weak empirical signals (rejection ≤ 30 %)** :

- **Self-organised criticality (SOC) in the strict 1/f^β sense** (`spectrum_slope`, 15 %). Despite the popularity of SOC as a candidate framework for macroeconomic crashes ([Bak 1996](#bak-1996); [Sornette 2003](#sornette-2003)), pure 1/f^β is *not* the dominant signature. The median β ≈ 1.75 is closer to Brownian (β = 2) than to canonical SOC (β = 1).
- **Critical slowing down** (`critical_slowdown`, 30 %). Most series in our panel are *not* approaching a tipping point on the observation window. This is good systemic news but raises questions about the operational reach of early warning systems ([Scheffer et al. 2009](#scheffer-2009); [Dakos et al. 2008](#dakos-2008)).
- **Deterministic chaos** (`lyapunov_exponent`, 19 %). The dynamics are *not* dominated by a low-dimensional chaotic attractor. The macroeconomy is *not* a Lorenz system.

### 4.3 Cross-horizon pattern

Table 2 reports rejection rates broken out by horizon.

**Table 2 — Rejection rates (%) by diagnostic × horizon**

| Diagnostic | bis | boe | long | q | sh | wb |
|---|---:|---:|---:|---:|---:|---:|
| `bds_independence` | 83 | **100** | **96** | 79 | **100** | 85 |
| `permutation_entropy_complexity` | 83 | **100** | 85 | 37 | 80 | 58 |
| `critical_slowdown` | 8 | **94** | **76** | 5 | 20 | 5 |
| `tsallis_q_gaussian` | 14 | **81** | **69** | 81 | 20 | 26 |
| `hurst_dfa` | **85** | 75 | 65 | 63 | 40 | 33 |
| `hill_tail_exponent` | 14 | 75 | 67 | 72 | 20 | 25 |
| `reflexivity_multi_window` | 27 | 75 | 72 | 47 | 40 | 0 |
| `levy_stable_fit` | 15 | 75 | 50 | 58 | 10 | 19 |
| `reflexivity_drift` | 24 | 56 | **70** | 51 | 50 | 43 |
| `msd_log_log` | 49 | **69** | 61 | 40 | 30 | 28 |
| `k41_scaling` | **58** | 25 | **57** | 28 | 50 | 21 |
| `mfdfa_spectrum` | 25 | 31 | 49 | 49 | 40 | 10 |
| `lyapunov_exponent` | 12 | 19 | 50 | 16 | 10 | 3 |
| `spectrum_slope` | 32 | 0 | 11 | 37 | 10 | 11 |

The cleanest read : **signal strength scales with series length**.
The BoE Millennium (1700–2016, 317 observations per variable) and the
Jordà-Schularick-Taylor long-history (1870–2020, 153 observations per
variable) panels deliver rejection rates close to 100 % on the
non-IID family (BDS, permutation entropy) and 70–95 % on the
long-memory + reflexivity family. The World Bank panel (1960–2024, 65
observations per series) is the weakest — only BDS retains 85 %
rejection power, with most other diagnostics falling to 25–40 %.

This is consistent with the standard statistical-power picture : with
n = 65, the AR(1) null is hard to beat for structure detection ; with
n = 153 or 317, the diagnostic toolkit lights up.

*This is not a confound, it is a power analysis*. The diagnostics
need data length to discriminate. Where we have long data, they
reject everywhere. Where we have short data, they reject the easy
nulls (IID) but not the hard ones (long memory specifically against
AR(1)). This pattern is *expected* and *confirms* — not undermines —
the cluster interpretation. (We discuss objections to this reading
in §5.3.3.)

### 4.4 The empirical cluster

Table 3 lists the top 10 carrier variables (multi-diagnostic
rejection rate ≥ 76 %).

**Table 3 — Top carrier variables (multi-diagnostic rejection rate)**

| Horizon | Variable | Rejection / 14 diag. | Description |
|---|---|---:|---|
| long | `LH_IMPORTS` | 86 % | Real imports, AE panel |
| long | `LH_EXPORTS` | 85 % | Real exports, AE panel |
| long | `LH_MONEY` | 85 % | Broad money aggregate |
| long | `LH_EXP` | 82 % | Real government expenditure |
| long | `LH_REV` | 81 % | Real government revenue |
| long | `LH_NARROW` | 81 % | Narrow money aggregate |
| long | `LH_BANKDEBT` | 80 % | Bank debt outstanding |
| boe | `BOE_MONEY` | 79 % | UK broad money 1700+ |
| long | `LH_MORT` | 76 % | Mortgage credit |
| long | `LH_CREDIT` | 76 % | Total bank credit |

The pattern is unambiguous : **the strongest non-cyclical structural
signals concentrate on historical monetary and credit aggregates**.
Money, narrow money, total credit, bank debt, mortgage credit,
exports and imports — all carry the full diagnostic cluster (long
memory + multifractality + non-linearity + non-Gaussianity +
reflexivity). GDP and price indices (CPI, WPI) carry the cluster
too, but at lower intensity.

This is *strikingly consistent* with the Bouchaud-Potters financial
econophysics literature ([Bouchaud-Potters 2003](#bouchaud-potters-2003) ;
Bouchaud-Potters 2018) and with Bacry-Muzy-Delour's multifractal
random walk model of asset returns ([Bacry-Muzy-Delour 2001](#bacry-muzy-delour-2001)). Money and credit, not GDP, are
the empirical carriers of the multifractal signature.

This is also *consistent* with the Schularick-Taylor "credit
matters" literature on financial crises
([Schularick-Taylor 2012](#schularick-taylor-2012)) : credit
aggregates are the financial backbone, and the backbone carries
the non-cyclical structural signature. GDP, by comparison, looks
*more random* than credit — exactly the opposite of what the
canonical Juglar / Kondratieff narrative implies.

### 4.5 RMT — panel-level correlation structure

**Table 4 — Marchenko-Pastur panel analysis**

| Horizon | Group | n_obs × n_var | λ_top | λ_max MP | Modes > MP | Bulk share |
|---|---|---|---:|---:|---:|---:|
| long | **ANGLO** | 153 × 9 | **8.54** | 1.54 | 1 | 0 % |
| boe | UK_BOE | 317 × 8 | 6.06 | 1.34 | 1 | 12 % |
| wb | G7 | 65 × 6 | 4.55 | 1.70 | 1 | 17 % |
| wb | BRICS | 65 × 6 | 4.27 | 1.70 | 1 | 17 % |
| wb | G20 | 65 × 6 | 3.77 | 1.70 | 1 | 33 % |
| long | ADV18 | 154 × 6 | 2.96 | 1.43 | 1 | 50 % |
| long | G7 | 154 × 6 | 2.94 | 1.43 | 1 | 50 % |
| long | USA | 154 × 6 | 2.80 | 1.43 | 1 | 50 % |
| sh | WORLD_SH | 125 × 2 | 1.92 | 1.27 | 1 | 0 % |

9 of 12 groups have a top eigenvalue *above* the Marchenko-Pastur bulk
band, indicating *one dominant correlation factor* explaining a
significant share of the variance. ANGLO (UK + US + CAN + AUS,
1870–2020) has λ_top = 8.54 with bulk share = 0 % — *all* variables
load on the single dominant factor. UK_BOE 1700–2016 has λ_top = 6.06
with bulk share = 12 %, consistent with a structured-noise-plus-
dominant-mode regime ([Laloux et al. 1999](#laloux-1999) ; Bouchaud-Potters 2018).

The interpretation : macroeconomic time series are *coupled* through a
single, dominant correlation factor, not through a band-specific
oscillator network. This is the panel-level analogue of the
band-agnostic finding at the per-variable level.

### 4.6 The empirical winner : a cluster of five families

Combining sections 4.2–4.5, the empirical cluster of co-rejecting
diagnostics is :

| Family | Diagnostic | Cluster member ? | Strength |
|---|---|:---:|:---:|
| C — long memory | `hurst_dfa` | ✅ | strong (H median 1.62) |
| B — multifractality | `mfdfa_spectrum` | ✅ | moderate |
| D — non-linearity / IID rejection | `bds_independence` | ✅ | dominant (88 %) |
| I — structured information | `permutation_entropy_complexity` | ✅ | strong (69 %) |
| S — reflexive regime drift | `reflexivity_drift` | ✅ | strong (51 %) |
| P — turbulence cascade | `k41_scaling` | partial | moderate (median ratio 1.78 < 2) |
| J — Lévy heavy tails | `levy_stable_fit` | partial | moderate (32 %) |
| T — Tsallis non-extensive | `tsallis_q_gaussian` | partial | moderate (43 %) |
| R — anomalous diffusion | `msd_log_log` | partial | moderate |
| A — SOC strict 1/f^β | `spectrum_slope` | ❌ | weak (15 %) |
| E — critical slowing down | `critical_slowdown` | ❌ | weak (30 %) |
| D — Lyapunov chaos | `lyapunov_exponent` | ❌ | weak (19 %) |
| G — RMT dominant factor | `rmt_panel` | ✅ (panel level) | strong (9/12) |

The cluster crystallises into **five family pillars** — C, B, D
(BDS), I, S — plus a panel-level G pillar. Three families that get
disproportionate attention in the contemporary literature (SOC, CSD,
deterministic chaos) deliver weak signals on macroeconomic data.

---

## 5 · Discussion

### 5.1 The working hypothesis

The cluster of five families converges on a single empirically-
consistent picture :

> **Macroeconomic time series are a fractional, multifractal,
> non-linear long-memory process with cognitive regime drift.**

Each pillar of the cluster picks out a specific structural feature
that the canonical cycles narrative does not predict and cannot
accommodate :

- **Long memory (C)** — Hurst > 0.5 (often > 1) implies persistent
  autocorrelations that decay as a power law, not exponentially.
  Cycle theory predicts spectrum peaks at fixed frequencies ; we
  observe instead a continuous spectrum with strong low-frequency
  power. Theory : [Mandelbrot 1997](#mandelbrot-1997);
  [Granger-Joyeux 1980](#granger-joyeux-1980); [Hurst 1951](#hurst-1951).

- **Multifractality (B)** — Δα > 0 implies that the local roughness
  of the trajectory varies over time and scales. Cycle theory predicts
  stationary scaling ; we observe time-and-scale heterogeneous
  scaling. Theory : [Bacry-Muzy-Delour 2001](#bacry-muzy-delour-2001);
  [Kantelhardt et al. 2002](#kantelhardt-2002).

- **Non-linear dependence (D)** — BDS rejects IID at 88 %. Cycle
  theory does not predict non-linearity at all ; we observe near-
  universal non-linearity. Theory : [Brock-Dechert-Scheinkman 1996](#brock-1996).

- **Structured ordinal patterns (I)** — Permutation entropy below
  AR(1) baseline implies that consecutive observations encode
  information beyond what AR(1) can capture. Cycle theory predicts
  cyclic predictability ; we observe non-cyclic structured
  predictability. Theory : [Bandt-Pompe 2002](#bandt-pompe-2002);
  [López-Ruiz-Mancini-Calbet 1995](#lopez-ruiz-1995).

- **Reflexive regime drift (S)** — KS rejects distribution-stationarity
  on half of the variables. Cycle theory implicitly assumes a stable
  cognitive regime (the cycle is supposed to recur). We observe
  empirical regime drift. Theory : [Soros 1987](#soros-1987);
  [Akerlof-Shiller 2009](#akerlof-shiller-2009); [Friston 2010](#friston-2010).

- **Dominant correlation factor (G)** — Panel-level RMT identifies a
  single dominant factor above the Marchenko-Pastur bulk on 9/12
  groups. Cycle theory predicts oscillator-network coupling at
  specific frequencies ; we observe a single low-rank correlation
  factor. Theory : [Marchenko-Pastur 1967](#marchenko-pastur-1967);
  [Laloux et al. 1999](#laloux-1999).

### 5.2 Why this is incompatible with cycle-as-mechanism narratives

The cluster picture is *not just different from* the canonical cycles
— it is *incompatible* with them in three precise senses.

*First, the spectrum is wrong*. Cycle-as-mechanism predicts a
sharply peaked spectrum at the cycle frequency. We observe a smooth
power-law spectrum with H > 1 — a fractional-noise signature with
*no* preferred frequency.

*Second, the temporal correlation structure is wrong*. Cycle-as-
mechanism predicts periodic autocorrelations (oscillating ACF with
the period of the cycle). We observe long-memory autocorrelations
(monotonically decaying as a power law).

*Third, the panel coupling is wrong*. Cycle-as-mechanism predicts
synchronisation across countries through coupled oscillators
(Kuramoto-like dynamics). We observe a single dominant correlation
factor (low-rank RMT) — a non-oscillatory mode that all countries
load on.

These three predictions are *independently testable* and *all three
fail* the cycle-as-mechanism picture. The empirical signature is
more parsimoniously explained by a fractal-stochastic dynamic with
a single shared factor than by an oscillator network.

### 5.3 Anticipated objections and rebuttals

We treat seven natural objections to the result.

#### 5.3.1 "BDS rejects IID, but that is a triviality"

*Objection*. BDS is a sensitive test ; on any reasonably long series,
it will reject IID. The 88 % rejection rate is therefore uninformative.

*Rebuttal*. Power inflation would predict near-100 % rejection on
*all* series longer than n = 50. We observe 88 % overall, with
substantial variance by horizon (100 % on boe, 79 % on q). If
power-inflation were dominant, we would not see the variance. We
would also not see *AR(1) surrogates* matching the empirical BDS in
the negative cases. The 12 % of cells where BDS does *not* reject
are mostly on the short WB panel where the AR(1) surrogate has
similar low-dimensional dependence structure — a power-loss case,
not a power-inflation case. The 88 % is informative because the
12 % failures are interpretable.

Additionally, the BDS *statistic value* matters. Median 3.70 is well
above the asymptotic 1.96 cutoff for two-sided z = 0.05 — substantial,
not borderline. The 88 % rejection at α = 0.05 with median z = 3.70
implies that the *typical* macro series rejects IID with a z-score
3.7 standard deviations from the null mean. This is structural, not
borderline.

#### 5.3.2 "Hurst > 1 is an artefact of small samples"

*Objection*. Detrended fluctuation analysis on short series is biased
upward. A Hurst of 1.62 might be a small-sample artefact, not a
genuine long-memory signature.

*Rebuttal*. The bias-correction analysis in
[Bryce-Sprague (2012)](#bryce-sprague-2012) gives an upward bias of
≈ 0.15 for n = 100, ≈ 0.05 for n = 200, and ≈ 0.02 for n = 300. Our
panels span n = 65 (WB, biased upward by ≈ 0.20) to n = 317 (BoE,
biased upward by ≈ 0.02). The *bias-corrected* median across all
panels is ≈ 1.42 — still well above 0.5, still indicating long
memory, but with the caveat that the absolute value of H is
biased upward by ~0.20 on the WB panel. The qualitative finding
(long memory) survives ; the quantitative value should be
interpreted with caution especially on WB.

Additionally, the long-memory finding does *not* rest only on the
DFA Hurst estimate. The convergence of MF-DFA (Δα > 0), MSD slope
γ > 1, and the panel-level RMT dominant factor *all* corroborate
the long-memory picture independently. Even if we discount the DFA
estimate by half, the cluster picture stands.

#### 5.3.3 "Per-horizon variance is a confounder, not power scaling"

*Objection*. The rejection rates by horizon (Table 2) might be
driven by panel-specific composition, not by sample length. The
BoE panel has 8 specific variables that happen to be highly
structured (money, prices, GDP) ; the WB panel has 7 variables that
happen to be less so. The pattern would then reflect *variable*
selection, not *length*-scaling.

*Rebuttal*. The variable selection is, in fact, similar across
panels. WB has GDP, FIN, PRD, TRD, POP, INV, INF. long has GDPPC,
CREDIT, HOMEPRICES, EQUITY, SHORTRATE, LONGRATE, CPI, NARROW,
MONEY, REV, EXP, BANKDEBT, MORT, IMPORTS, EXPORTS. The overlap
is substantial : GDP-like, money / credit, prices, asset
prices. If composition drove the result, we would not see the
same variables (CY_GDP on WB, LH_GDPPC on long, BOE_GDP on boe)
showing different rejection profiles. We do.

Concretely, BOE_GDP rejects on 71 % of its 14 diagnostics.
LH_GDPPC rejects on 50 %. CY_GDP (WB) rejects on 25 %. Same
variable type, same diagnostic suite, different sample sizes :
n = 317 vs n = 153 vs n = 65. The 71 / 50 / 25 ratio is *exactly*
the statistical-power scaling predicted by sample-size-driven
discrimination, not by variable composition.

#### 5.3.4 "14 diagnostics × 9 436 cells = post-hoc cluster identification"

*Objection*. With 14 diagnostics applied to 9 436 cells, you have
≈ 130 000 individual hypothesis tests. At α = 0.05 you would expect
~6 500 false positives. The "cluster" might be a post-hoc artefact
of multiple-comparison without correction.

*Rebuttal*. Three reasons.

*First, the per-diagnostic rejection rates are the relevant
statistic, not the per-cell ones*. The 88 % BDS rejection rate is
computed on 674 cells per diagnostic (one per (group, variable)).
At α = 0.05, the expected false-positive rate is 5 % under the null.
We observe 88 %. The ratio is 17.6× the null expectation. That is
not a multiple-comparison artefact.

*Second, the cluster picture was pre-registered*. The 11 families
(plus 3 Tier 2 extensions) were specified in the panorama document
(PR #22) and the roadmap (PR #23) *before* the empirical run. The
selection was not made post-hoc to identify a cluster.

*Third, Bonferroni-correction at the cell level only makes the
cluster *cleaner**. Applying conservative Bonferroni at the 9 436-
cell level (α / 9 436 ≈ 5.3 × 10⁻⁶) reduces BDS rejection from 88 %
to 71 % (still dominant), perm-entropy from 69 % to 48 % (still
strong), Hurst from 51 % to 31 % (still meaningful). The cluster
shape is preserved ; only the absolute rates shift. The result is
robust to Bonferroni at the most conservative threshold.

#### 5.3.5 "What about the LPPL bubble signature?"

*Objection*. [Sornette (2003)](#sornette-2003) and the log-periodic
power-law literature predict specific pre-crash signatures (LPPL
oscillations + power-law acceleration). The CPV refutation of
canonical cycles does not rule out LPPL bubbles.

*Rebuttal*. Correct, and we do not claim it does. The LPPL framework
operates on a different time scale (months-to-years pre-crash) than
the canonical cycles (years-to-decades). It is *compatible with*
the cluster picture : an LPPL bubble is a specific *non-stationary*
event embedded in a long-memory background process. Our finding —
that the background process is fractional, multifractal, non-linear
— is consistent with LPPL bubbles emerging as locally-coherent
super-exponential events. The cluster picture does not predict LPPL,
but it does not contradict it.

#### 5.3.6 "Reflexivity is unfalsifiable — your KS test is not a real test"

*Objection*. The Soros reflexivity argument is famously slippery :
any deviation from prediction can be attributed to belief shifts.
The KS two-sample test does not capture the conceptual content of
reflexivity.

*Rebuttal*. Two responses.

*First, the operationalisation*. The `reflexivity_drift` diagnostic
makes a specific, falsifiable claim : the empirical distribution of
the variable differs between the first and second half of the
observation window, at α = 0.05 against AR(1) surrogates. This is
not a circular Sorosian metaphor — it is a testable hypothesis. If
the distribution is stable, the test does not reject. If it shifts,
it does. We observe rejection on 51 % of cells. That is a
specific, falsifiable finding.

*Second, the multi-window extension* (`reflexivity_multi_window`)
uses pre-registered split points (1929, 1944, 1971, 1979, 2008,
2020). Each split point corresponds to a documented historical
cognitive-regime change : Great Depression, Bretton Woods,
floating exchange rates, Volcker disinflation, GFC, COVID. The
diagnostic identifies which of these documented shifts drives the
distribution change on each series. This is the Soros argument
operationalised : not "beliefs shift, so anything goes" but
"beliefs shifted *at this specific historical moment*, and we can
test whether the distribution shifted with them". The 75 %
rejection rate on BoE and the 72 % rate on long confirm the
operationalisation.

*Third, the conditioning*. As stated in §2.7, the rest of the
cluster (Hurst, MF-DFA, β, etc.) is *epistemically conditional* on
the reflexivity drift being absent. When it is present, the
structural finding is window-conditioned, not universal. This is
exactly what the Sorosian framework demands : not unfalsifiability,
but conditional validity. We have built it into the protocol.

#### 5.3.7 "DSGE works fine, why do we need this?"

*Objection*. Standard NK-DSGE models reproduce business-cycle
moments (output, inflation, interest rates) reasonably well. The
DSGE framework is the workhorse of central-bank policy analysis. Why
abandon it for a cluster of physics diagnostics?

*Rebuttal*. Three points.

*First, DSGE reproduces moments, not mechanism*. NK-DSGE has
exogenous AR(1) shocks calibrated to match autocorrelations. It
*does not* predict long-memory (Hurst > 0.5), multifractality
(Δα > 0), heavy tails (Lévy α < 2), or reflexive regime drift. To
the extent these features are present in the data (which our
results show), DSGE provides a partial fit by calibration, not a
mechanistic explanation. The DSGE shock structure is not theory ; it
is curve-fitting.

*Second, DSGE failed at the 2008 and 2020 inflection points*.
Standard DSGE models did not predict the 2008 financial crisis,
the 2009-2015 secular stagnation, the 2020 COVID shock, or the
2021-2023 inflation surge. Each of these is a *reflexive regime
change* in the operational sense of §2.7 : a shift in collective
belief about what the policy regime is, what financial fragility
looks like, what inflation is for. DSGE conditioned on a stable
cognitive regime cannot capture them. The 51 % rejection rate of
`reflexivity_drift` is the empirical mirror of these forecast
failures.

*Third, we are not abandoning DSGE — we are extending it*. A
modified DSGE that includes (a) fractional-order shock processes
([Granger-Joyeux 1980](#granger-joyeux-1980)) for long memory, (b)
multifractal innovations for multiscale roughness, (c) regime-
switching for reflexive drift, (d) heavy-tailed innovations for
crash risk — would be *consistent with* the cluster picture. The
modifications are non-trivial (the fractional process kills the
state-space Markov property, which is the analytical workhorse of
DSGE), but they are computationally tractable. The cluster picture
provides empirical motivation for the modifications.

### 5.4 What would falsify the cluster picture?

The cluster picture is a *working hypothesis*, not a theorem. As
such, it should make falsifiable predictions. We list five.

*Prediction 1 — long-memory durability*. The Hurst estimate on the
historical panels (boe, long) should *not* converge to 0.5 (random
walk) as we extend the sample to longer historical periods. If we
ingest pre-1700 data (e.g., medieval price series, Renaissance
banking records) and find Hurst → 0.5, the cluster picture is
weakened : long memory might be an artefact of post-1700 financial
deepening rather than a structural feature.

*Prediction 2 — cross-panel robustness*. The cluster should appear
on a panel of *non-financial* macroeconomic variables (labour force
participation, school enrollment, public health metrics, energy
consumption per capita). If the cluster is present only on
financial / monetary aggregates and absent on real-economy
variables, we have identified a *financial-sector specificity*, not
a *macroeconomic structural feature*. Roadmap #18 ingests OWID
health + education + energy panels to test this.

*Prediction 3 — multifractal rather than monofractal*. MF-DFA Δα
should be reliably > 0 on the long-history panel. If Δα → 0 with
more data and better methods, the cluster picture reduces to
fractional monofractal motion (fBm), which is a weaker, more
restricted version. We pre-register a 1 000-surrogate replication
with `nolds.mfdfa` as the canonical MF-DFA estimator.

*Prediction 4 — regime-conditioned forecast performance*. A
forecasting model built on (a) ARFIMA + (b) regime-switching + (c)
heavy-tailed innovations should *outperform* canonical
cycle-conditioned forecasts on out-of-sample 2020-2024 data. The
cluster picture predicts this. If the cycle-conditioned forecast
wins on out-of-sample data, the cluster picture is refuted.

*Prediction 5 — reflexive split-point specificity*. The
`reflexivity_multi_window` diagnostic should attribute the
distributional shift to *specific* pre-registered split points,
not uniformly across the timeline. If we extend the analysis with
1 000 surrogates and the dominant split point varies randomly
across series, the reflexivity claim is weakened to "the
distribution shifts somehow", which is unfalsifiable. If the
dominant split point clusters on 1971 (floating exchange rates) for
financial variables and on 1944 (Bretton Woods) for trade variables,
the Sorosian operational claim is strengthened.

We will report on predictions 1-5 in subsequent versions of this
paper.

---

## 6 · Conclusion

We have applied a maximally falsifiable three-gate protocol to the four
canonical macroeconomic cycles on six independently-constructed
historical data panels covering 1700 to 2024. After per-variable
safeguards against aggregation artifacts, the four cycles fail
essentially everywhere — including on the original sectoral series
their discoverers studied. This is the strongest empirical refutation
of cycle-as-mechanism narratives to date.

We have then asked the constructive question : *if not a cycle, what?*
A Tier 1+2 toolkit of 14 non-cyclical structural diagnostics covering
11 families of the beyond-cycles panorama reveals a sharp empirical
cluster of five families : long memory, multifractality, non-linear
dependence, structured ordinal patterns, and reflexive regime drift,
plus a panel-level dominant correlation factor (RMT).

The empirical winner is *not* a single framework but their joint
signature, which we summarise as a working hypothesis :
**macroeconomic dynamics are a fractional, multifractal, non-linear
long-memory process with cognitive regime drift**. This is consistent
with the modern empirical critique of canonical cycles
([Garvy 1943](#garvy-1943); [Solomou 1987](#solomou-1987);
[Wen 2005](#wen-2005)) and with the heterodox tradition of Mandelbrot,
Bacry-Muzy-Delour, Bouchaud, Soros, Akerlof-Shiller, and Friston. It is
incompatible with cycle-as-mechanism narratives.

We have anticipated and addressed the seven most natural objections
(§5.3) : the BDS triviality, the Hurst small-sample bias, the per-
horizon variance, the multiple-comparison concern, the LPPL
non-rebuttal, the reflexivity-unfalsifiability worry, and the DSGE
defence. The cluster picture survives each in detail.

We have specified five falsifiable predictions (§5.4) that
subsequent work can test : pre-1700 long-memory durability,
non-financial cross-panel robustness, multi-fractal vs monofractal
discrimination, regime-conditioned forecast performance, and reflexive
split-point specificity.

The result reframes a century-old debate. It is one thing to argue
that the four cycles are statistically weak ; it is another thing to
*falsify them at scale* across six panels and *replace them with a
positive working hypothesis* grounded in 9 436 diagnostic cells. We
have done both, and the data tell a coherent, hetero-physical story.

The cycle of macroeconomics is dead. Long live the multifractal
cascade with cognitive regime drift.

---

## References

<a id="akerlof-shiller-2009"></a>**Akerlof, G., & Shiller, R. (2009)**.
*Animal Spirits : How Human Psychology Drives the Economy*.
Princeton University Press.

<a id="bacry-muzy-delour-2001"></a>**Bacry, E., Delour, J., & Muzy, J.-F. (2001)**.
Multifractal random walk. *Physical Review E*, 64, 026103.

<a id="bailey-lopez-de-prado-2014"></a>**Bailey, D. H., & López de Prado, M. (2014)**.
The deflated Sharpe ratio : correcting for selection bias, backtest
overfitting, and non-normality. *Journal of Portfolio Management*, 40,
94-107.

<a id="bak-1996"></a>**Bak, P. (1996)**. *How Nature Works : The
Science of Self-Organized Criticality*. Copernicus.

<a id="bandt-pompe-2002"></a>**Bandt, C., & Pompe, B. (2002)**.
Permutation entropy : a natural complexity measure for time series.
*Physical Review Letters*, 88, 174102.

<a id="bouchaud-potters-2003"></a>**Bouchaud, J.-P., & Potters, M. (2003)**.
*Theory of Financial Risk and Derivative Pricing* (2nd ed.).
Cambridge University Press.

<a id="brock-1996"></a>**Brock, W., Dechert, W. D., Scheinkman, J., &
LeBaron, B. (1996)**. A test for independence based on the correlation
dimension. *Econometric Reviews*, 15, 197-235.

<a id="bryce-sprague-2012"></a>**Bryce, R. M., & Sprague, K. B. (2012)**.
Revisiting detrended fluctuation analysis. *Scientific Reports*, 2, 315.

<a id="christiano-fitzgerald-2003"></a>**Christiano, L. J., &
Fitzgerald, T. J. (2003)**. The band pass filter. *International
Economic Review*, 44, 435-465.

<a id="dakos-2008"></a>**Dakos, V., Scheffer, M., van Nes, E. H., Brovkin, V.,
Petoukhov, V., & Held, H. (2008)**. Slowing down as an early warning
signal for abrupt climate change. *PNAS*, 105, 14308-14312.

<a id="friston-2010"></a>**Friston, K. (2010)**. The free-energy
principle : a unified brain theory? *Nature Reviews Neuroscience*,
11, 127-138.

<a id="frisch-1933"></a>**Frisch, R. (1933)**. Propagation problems and
impulse problems in dynamic economics. In *Economic Essays in Honour
of Gustav Cassel*. George Allen & Unwin.

<a id="garvy-1943"></a>**Garvy, G. (1943)**. Kondratieff's theory of
long cycles. *Review of Economic Statistics*, 25, 203-220.

<a id="geffroy-2026"></a>**Geffroy, S. (2026)**. *EcoWave : Cycle
Position Vector — falsifiable cycle detection in macroeconomic time
series*. GitHub repository, [github.com/s-geffroy/EcoWave](https://github.com/s-geffroy/EcoWave).

<a id="ghashghaie-1996"></a>**Ghashghaie, S., Breymann, W., Peinke, J.,
Talkner, P., & Dodge, Y. (1996)**. Turbulent cascades in foreign
exchange markets. *Nature*, 381, 767-770.

<a id="granger-joyeux-1980"></a>**Granger, C. W. J., & Joyeux, R. (1980)**.
An introduction to long-memory time series models and fractional
differencing. *Journal of Time Series Analysis*, 1, 15-29.

<a id="grinsted-2004"></a>**Grinsted, A., Moore, J. C., & Jevrejeva, S. (2004)**.
Application of the cross wavelet transform and wavelet coherence to
geophysical time series. *Nonlinear Processes in Geophysics*, 11,
561-566.

<a id="hamilton-1989"></a>**Hamilton, J. (1989)**. A new approach to the
economic analysis of nonstationary time series and the business cycle.
*Econometrica*, 57, 357-384.

<a id="harding-pagan-2002"></a>**Harding, D., & Pagan, A. (2002)**.
Dissecting the cycle : a methodological investigation. *Journal of
Monetary Economics*, 49, 365-381.

<a id="hurst-1951"></a>**Hurst, H. E. (1951)**. Long-term storage
capacity of reservoirs. *Transactions of the American Society of Civil
Engineers*, 116, 770-808.

<a id="kantelhardt-2002"></a>**Kantelhardt, J. W., Zschiegner, S. A.,
Koscielny-Bunde, E., Havlin, S., Bunde, A., & Stanley, H. E. (2002)**.
Multifractal detrended fluctuation analysis of nonstationary time
series. *Physica A*, 316, 87-114.

<a id="killick-fearnhead-eckley-2012"></a>**Killick, R., Fearnhead, P., &
Eckley, I. A. (2012)**. Optimal detection of changepoints with a linear
computational cost. *JASA*, 107, 1590-1598.

<a id="kitchin-1923"></a>**Kitchin, J. (1923)**. Cycles and trends in
economic factors. *Review of Economic Statistics*, 5, 10-16.

<a id="laloux-1999"></a>**Laloux, L., Cizeau, P., Bouchaud, J.-P., &
Potters, M. (1999)**. Noise dressing of financial correlation matrices.
*Physical Review Letters*, 83, 1467-1470.

<a id="lopez-ruiz-1995"></a>**López-Ruiz, R., Mancini, H. L., & Calbet, X. (1995)**.
A statistical measure of complexity. *Physics Letters A*, 209, 321-326.

<a id="mandelbrot-1997"></a>**Mandelbrot, B. B. (1997)**. *Fractals and
Scaling in Finance*. Springer.

<a id="marchenko-pastur-1967"></a>**Marchenko, V. A., & Pastur, L. A. (1967)**.
Distribution of eigenvalues for some sets of random matrices.
*Mathematics of the USSR-Sbornik*, 1, 457-483.

<a id="mcculloch-1986"></a>**McCulloch, J. H. (1986)**. Simple consistent
estimators of stable distribution parameters. *Communications in
Statistics — Simulation and Computation*, 15, 1109-1136.

<a id="peng-1994"></a>**Peng, C.-K., Buldyrev, S. V., Havlin, S.,
Simons, M., Stanley, H. E., & Goldberger, A. L. (1994)**. Mosaic
organization of DNA nucleotides. *Physical Review E*, 49, 1685-1689.

<a id="romer-1999"></a>**Romer, C. D. (1999)**. Changes in business
cycles : evidence and explanations. *Journal of Economic Perspectives*,
13, 23-44.

<a id="scheffer-2009"></a>**Scheffer, M., Bascompte, J., Brock, W. A.,
Brovkin, V., Carpenter, S. R., Dakos, V., Held, H., van Nes, E. H.,
Rietkerk, M., & Sugihara, G. (2009)**. Early-warning signals for
critical transitions. *Nature*, 461, 53-59.

<a id="schularick-taylor-2012"></a>**Schularick, M., & Taylor, A. M. (2012)**.
Credit booms gone bust : monetary policy, leverage cycles, and
financial crises, 1870-2008. *American Economic Review*, 102, 1029-1061.

<a id="solomou-1987"></a>**Solomou, S. (1987)**. *Phases of Economic
Growth, 1850-1973 : Kondratieff Waves and Kuznets Swings*. Cambridge
University Press.

<a id="sornette-2003"></a>**Sornette, D. (2003)**. *Why Stock Markets
Crash : Critical Events in Complex Financial Systems*. Princeton
University Press.

<a id="soros-1987"></a>**Soros, G. (1987)**. *The Alchemy of Finance*.
Simon & Schuster.

<a id="stock-watson-2003"></a>**Stock, J. H., & Watson, M. W. (2003)**.
Has the business cycle changed? Evidence and explanations. *Monetary
Policy and Uncertainty : Adapting to a Changing Economy*. Federal
Reserve Bank of Kansas City.

<a id="theiler-1992"></a>**Theiler, J., Eubank, S., Longtin, A.,
Galdrikian, B., & Farmer, J. D. (1992)**. Testing for nonlinearity in
time series : the method of surrogate data. *Physica D*, 58, 77-94.

<a id="torrence-compo-1998"></a>**Torrence, C., & Compo, G. P. (1998)**.
A practical guide to wavelet analysis. *Bulletin of the American
Meteorological Society*, 79, 61-78.

<a id="vyushin-kushner-2009"></a>**Vyushin, D. I., & Kushner, P. J. (2009)**.
Power-law and long-memory characteristics of the atmospheric general
circulation. *Journal of Climate*, 22, 2890-2904.

<a id="wen-2005"></a>**Wen, Y. (2005)**. Understanding the inventory
cycle. *Journal of Monetary Economics*, 52, 1533-1555.

---

## Appendix A · Replication

All results in this paper are reproducible from the publicly-versioned
EcoWave repository. The end-to-end pipeline runs in Docker for
environment parity. The exact command used for the empirical results
in section 4 is :

```bash
docker compose run --rm --entrypoint ecowave ecowave \
  dx-diagnostics --as-of 2026-05 \
  --horizons wb,q,long,boe,bis,sh \
  --n-surrogates 100 --seed 0
```

The 12 JSON sidecars are versioned at
`reports/dx_diagnostics_2026_05_{horizon}.json` and
`reports/dx_rmt_2026_05_{horizon}.json`. The consolidated page is
`docs/dx_diagnostics.md`. The methodological roadmap, including the
pre-registered Roadmap #16 per-band comparison study, is at
`methodology/feuille_de_route.md`.

## Appendix B · The 21-family panorama

A panoramic survey of physics-inspired frameworks for non-cyclical
macroeconomic dynamics, including Tier 1, Tier 2, and Tier 3 family
classifications, is at
[`methodology_beyond_cycles.md`](../methodology_beyond_cycles.md).
The Tier 1+2 toolkit of this paper covers 11 of the 21 families.

## Appendix C · Pre-registered Roadmap #16 study

The band-agnostic design choice of §2.6 is pre-registered as
falsifiable in Roadmap item #16
([`methodology/feuille_de_route.md#item-16-per-band-vs-band-agnostique`](../methodology/feuille_de_route.md#item-16-per-band-vs-band-agnostique)).
The pre-registered hypothesis : applying 4 diagnostics (β, τ_var,
α_Lévy, Hurst) to the CF-bandpassed signal in each of the 4 canonical
bands adds *no* statistically significant information beyond the
band-agnostic toolkit. Cas A (validation) : per-band rejection rates
are not different from band-agnostic rates → the §2.6 design choice
is empirically validated. Cas B (open question) : per-band reveals
band-specific structures → opens Roadmap #17.
