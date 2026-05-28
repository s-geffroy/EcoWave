# Juglar (7–11 ans)

> **Résumé.** Le « cycle des affaires » classique.
> [Juglar (1862)](../bibliographie.md#juglar-1862) l'identifie sur les
> données bancaires et commerciales françaises ;
> [Schumpeter (1939)](../bibliographie.md#schumpeter-1939) le popularise
> comme cycle d'investissement fixe et de crédit. C'est la bande sur
> laquelle CPV produit ses verdicts les plus solides en mai 2026, avec
> une divergence économique observée entre USA/ANGLO (expansion) et
> NORDIC (contraction profonde).

## Diagramme de phase polaire — panel Banque mondiale 2026

![Diagramme polaire Juglar — panel WB mai 2026](../figures/cycle_phase_polar_juglar_2026_05_wb.png){ width="90%" }

## Diagramme de phase polaire — panel d'histoire longue (1870-2022)

![Diagramme polaire Juglar — panel long-history mai 2026](../figures/cycle_phase_polar_juglar_2026_05_long.png){ width="90%" }

Sur le panel long-history (153 années, 18 économies avancées), USA et
ANGLO se positionnent dans le quadrant expansion (φ ≈ −1.5 rad, amplitude
~0.3) ; NORDIC est isolé dans le quadrant contraction profonde
(φ ≈ −2.6 rad, amplitude ~0.4). L'analyse économique détaillée :
[Juglar US/ANGLO vs NORDIC 2022-2026](../reports/juglar_us_anglo_nordic_2026.md).

## Ce que mesure CPV

Le pipeline applique les quatre méthodes votantes (D, E, F, G) sur la
bande Juglar $[7, 11]$ années. Cette bande est la **tête de file** du
mode crisis-pilot : la méthode F (CF band-pass + Hilbert) sur la bande
Juglar est la sortie CPV principale, et sa phase instantanée classe
l'endpoint en expansion / peak / contraction / trough.

Sur le panel WB annuel, la bande 7–11 ans est complètement résolue ; sur
les panels mensuels pilotes (fenêtres de crise de 5–7 ans), la méthode F
**retombe typiquement** parce que deux cycles Juglar complets ne tiennent
pas dans la fenêtre. Les méthodes D, E, G produisent encore des phases
dans ce cas.

## Indicateurs moteurs

- `NE.GDI.TOTL.ZS` (formation brute de capital fixe, % PIB) — Juglar
  est par définition le cycle d'investissement.
- `SL.UEM.TOTL.ZS` (taux de chômage).
- `NE.TRD.GNFS.ZS` (commerce extérieur, % PIB).
- `FS.AST.PRVT.GD.ZS` (crédit domestique / PIB) — cycle de crédit
  Juglar.

## Caveats

- **Fenêtre pilote** : sur 5–7 ans, méthode F instable ; consensus 2/4
  fréquent → `disputed`.
- **Endpoint CF** : les 5–6 dernières années sont marquées
  `endpoint_caveat = 1`.

## Références

- [Juglar (1862)](../bibliographie.md#juglar-1862)
- [Schumpeter (1939)](../bibliographie.md#schumpeter-1939)
- [Harding & Pagan (2002)](../bibliographie.md#harding-pagan-2002)
- [Hamilton (1989)](../bibliographie.md#hamilton-1989)
- [Stock & Watson (2005)](../bibliographie.md#stock-watson-2005)

## Voir aussi

- [Protocole CPV](../methodology/protocole_cpv.md)
- [Analyse approfondie Juglar US/ANGLO vs NORDIC](../reports/juglar_us_anglo_nordic_2026.md)
- [Résultats panel Banque mondiale 2026-05](../reports/panel_banque_mondiale_2026.md)
