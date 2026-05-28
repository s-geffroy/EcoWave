# Kitchin (3–5 years)

The shortest of the four canonical cycles. Identified by Joseph Kitchin in
1923 from US clearings and wholesale-price data, it captures the rhythm of
business inventories and short-term price corrections.

## What CPV measures

The CPV pipeline runs the four votant methods (D, E, F, G) on the Kitchin
band [3, 5] years. On annual World Bank data the **lower edge (3 y) is below
the Nyquist limit** (annual sampling resolves cycles ≥ 2 y in theory, but
practically ≥ 4 y for noisy macro series). The protocol therefore
pre-registers Kitchin reporting on the 4–5 y upper edge only on annual data.

Quarterly upsample (cubic spline) is documented as a sensitivity variant,
never the default — see `methodology/cycle_validation_rules.md` for the
anti-HARKing rule.

## Driver indicators (`cycles_manifest.json`)

- `NY.GDP.MKTP.KD.ZG` (real GDP growth) — primary driver.
- `FP.CPI.TOTL.ZG` (CPI inflation) — inventory / price cycle proxy.

## References

- Kitchin, J. (1923). *Cycles and trends in economic factors*. The Review of
  Economics and Statistics, 5(1), 10–16.
- Diebolt, C., & Doliger, C. (2008). *Economic cycles under test: A spectral
  analysis*. Cliometrica.
- Korotayev, A. V., & Tsirel, S. V. (2010). *A spectral analysis of world GDP
  dynamics: Kondratieff waves, Kuznets swings, Juglar and Kitchin cycles in
  global economic development*. Structure and Dynamics, 4(1).

## See also

- [CPV protocol](../methodology/multi_cycle_decomposition.md)
- [Current report](../reports/cycle_position_2026_05.md)
