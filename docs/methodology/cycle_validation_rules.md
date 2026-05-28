# Cycle validation rules — CPV protocol

A phase published for any (group, cycle, month) cell must satisfy **all** of
the following falsifiability gates:

## Gate 1 — Existence

The band's CF-filtered power must exceed the 95th percentile of band-power
under AR(1) red noise with the same mean / variance / persistence as the
input. Formally: `ar1_bootstrap_null(series, lo_years, hi_years).p_value < 0.05`.
A cell that fails this gate is published with `phase = rejected`,
`separable = 0`, `ar1_p_value = p`.

Source: Torrence & Compo (1998); Grinsted et al. (2004).

## Gate 2 — Method consensus

At least 3 of the 4 votant models must agree on the phase label:

- **F** — CF Juglar band-pass + Hilbert phase
- **G** — Bry-Boschan / Harding-Pagan turning-point dating
- **E** — Markov-switching AR(1) regimes (Hamilton 1989)
- **D** — PELT change-point detection (Killick 2012)

If fewer than 3 agree, the cell is published as `phase = disputed`. Disagreement
is published explicitly in the per-method votes table (`cycle_consensus`),
never resolved by picking a "friendly" method.

## Gate 3 — Cross-group universality

For each cycle and as-of month, the cycle is qualified `universal` only if
≥ 4 of the 5 income groups (WLD + HIC + UMC + LMC + LIC) share the same modal
phase. This transposes the EcoWave C6 transferability criterion from the
temporal to the income-stratification dimension.

Universal cycles can be reported as global state of the world economy;
non-universal cycles are reported as `regional / idiosyncratic` and must
specify which groups concur.

## Other constraints

- **Endpoint caveat**: any cell whose last data point is within `hi_years / 2`
  of the panel endpoint is flagged `endpoint_caveat = 1`. The phase claim is
  still published but readers are explicitly warned that the CF filter is
  unreliable at the boundary.
- **Frequency adequacy**: WB data is annual. Kitchin (3–5 years) is borderline;
  the lower edge (3 y) is below the Nyquist limit for annual sampling. The
  protocol pre-registers Kitchin reporting on the 4–5 y upper edge only;
  quarterly upsample (spline) is a sensitivity variant, never the default.
- **Small-N Kondratieff**: WB series start in 1960 (~65 y of data ≈ 1.0–1.5
  K-waves). Gate 1 frequently rejects Kondratieff for income groups with
  shorter or noisier history; this is published as `separable = 0`, not
  reinterpreted as evidence of a hidden phase.
- **No cherry-picking of band**: cycle bands are frozen in
  `ecowave/cycles/bands.py` and never tuned per group.

## Verdict scale

- **A** — Gate 1 ✓, Gate 2 ✓ (4/4 agree), Gate 3 ✓ (universal). Phase published as
  the modal label.
- **B** — Gate 1 ✓, Gate 2 ✓ (3/4 agree), Gate 3 ✓. Phase published, with the
  dissenting model noted in `notes`.
- **C** — Gate 1 ✓, Gate 2 ✗ (`disputed`) OR Gate 3 ✗ (`regional`). Cell reported
  but the verdict is qualified.
- **D** — Gate 1 ✗ (`rejected`). Cycle does not exist at this frequency for this
  group. Honest failure, not a hidden phase.
