# Juglar (7–11 years)

The classical "business cycle". Identified by Clément Juglar (1862) on French
banking and trade data, popularised by Schumpeter (1939) as the cycle of
fixed investment expenditure and credit.

## What CPV measures

The CPV pipeline runs the four votant methods (D, E, F, G) on the Juglar
band [7, 11] years. This band is the headline of the crisis-pilot mode:
Model F (CF band-pass + Hilbert) on the Juglar band is the primary CPV
output and its instantaneous phase classifies the endpoint as
expansion / peak / contraction / trough.

On annual WB data the 7–11 year band is fully resolvable; on monthly
pilot panels (5–7 year crisis windows) Model F **typically falls back**
because two complete Juglar cycles do not fit the window. Models D, E,
G still produce phases in that case.

## Driver indicators

- `NE.GDI.TOTL.ZS` (gross capital formation, % GDP) — Juglar is the
  investment cycle by definition.
- `SL.UEM.TOTL.ZS` (unemployment).
- `NE.TRD.GNFS.ZS` (trade % GDP).
- `FS.AST.PRVT.GD.ZS` (domestic credit / GDP) — Juglar credit cycle.

## References

- Juglar, C. (1862). *Des crises commerciales et de leur retour périodique
  en France, en Angleterre et aux États-Unis*.
- Schumpeter, J. A. (1939). *Business cycles*. McGraw-Hill.
- Harding, D., & Pagan, A. (2002). *Dissecting the cycle: a methodological
  investigation*. Journal of Monetary Economics, 49(2), 365–381.
- Hamilton, J. D. (1989). *A new approach to the economic analysis of
  nonstationary time series and the business cycle*. Econometrica, 57(2),
  357–384.

## See also

- [CPV protocol](../methodology/multi_cycle_decomposition.md)
- [Current report](../reports/cycle_position_2026_05.md)
