# Kondratieff (40–60 years)

The long wave. Identified by Nikolai Kondratieff in 1925 from price-level and
interest-rate series; later linked to clusters of techno-economic innovation
(Schumpeter, Mensch) and to commodity-price super-cycles.

## What CPV measures

The CPV pipeline runs the four votant methods (D, E, F, G) on the Kondratieff
band [40, 60] years. This is **the band where the small-N caveat is most
acute**: World Bank series start in 1960, providing about 65 years of data —
roughly 1.0–1.5 K-waves of history.

The AR(1) null (Gate 1) frequently rejects Kondratieff separability for
several income groups. **This is honest, not a failure**: short samples
cannot reliably distinguish a single multi-decade swing from red noise.
The CPV protocol publishes `separable = 0` rather than fabricating a phase.

Endpoint caveats are severe: the CF filter is unreliable on the last
`hi_years / 2` = 30 years for Kondratieff. The current report flags this
explicitly.

## Driver indicators

- `NY.GDP.PCAP.KD` (real GDP per capita, log-difference) — long-wave
  productivity proxy.
- `FS.AST.PRVT.GD.ZS` (domestic credit / GDP) — Reinhart-Rogoff credit
  super-cycle.

## References

- Kondratieff, N. D. (1925). *The major economic cycles* (English translation:
  *The long waves in economic life*, Review of Economic Statistics, 1935).
- Schumpeter, J. A. (1939). *Business cycles*.
- Mensch, G. (1979). *Stalemate in technology: Innovations overcome the
  depression*.
- Modelski, G. (1996). *Leading sectors and world powers*.
- Korotayev, A. V., & Tsirel, S. V. (2010). *A spectral analysis of world
  GDP dynamics*.
- Reinhart, C. M., & Rogoff, K. S. (2009). *This time is different: Eight
  centuries of financial folly*.

## See also

- [CPV protocol](../methodology/multi_cycle_decomposition.md)
- [Current report](../reports/cycle_position_2026_05_wb.md)
