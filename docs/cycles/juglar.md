# Juglar (7–11 ans)

!!! success "Verdict V3 (juin 2026) — Juglar empiriquement vivant"

    Source : `papers/cycles_refuted/sections/{01_introduction,05_results}.tex`.

    - **JST R6 (1870–2020, 18 économies avancées)** : **67 / 605 cellules** passent Gate 1 unadjusted, soit **2.2× l'excès sur null**. Concentration :
        - `LH_INV` (investissement-PIB) : **39 % des pays** (7 / 18). Plus petites *p*<sub>1</sub> sur Suisse et Canada (*p*<sub>1</sub> = 0.001).
        - `LH_UNRATE` : **33 %** (6 / 18). `LH_BUSCREDIT` : **33 %** (5 / 15). `LH_RCONS`, `LH_HPI`, `LH_RGDP_BARRO`, `LH_DEBTGDP` : 4 chacune.
    - **Quarterly (1995–2024)** : **12 / 55 cellules** (4.3× excès) — G7Q / OECDQ / GBR / JPN chômage, US et EA long-term yields, ZA / MX / KR crédit.
    - **BoE Millennium UK chômage** survit aux **deux nulls** : *p*<sub>AR(1)</sub> = 0.004, *p*<sub>ARFIMA</sub> = 0.002 à *d̂* = 0.49 ; idem real USD-GBP exchange rate (*p*<sub>AR(1)</sub> = 0.006, *p*<sub>ARFIMA</sub> = 0.002 à *d̂* = 0.428).
    - **Théorique faux positif `LH_XRUSD`** : passe sur 11 / 18 (61 %, plus grosse concentration single-variable Juglar) mais le mécanisme substantif Juglar n'attribue pas de rôle direct au taux de change bilatéral USD ; cellule **retenue pour transparence, exclue** de la claim « investissement-et-chômage ».

    **Lecture V3** : la vindication substantive de [Juglar (1862)](../bibliographie.md#juglar-1862) et de [Schumpeter (1939)](../bibliographie.md#schumpeter-1939) sur l'investissement-credit channels est tenue ; la lecture universaliste (un Juglar sur toutes les variables macro) reste rejetée par BH-FDR sur la grille jointe.

> **Résumé historique.** Le « cycle des affaires » classique.
> [Juglar (1862)](../bibliographie.md#juglar-1862) l'identifie sur les
> données bancaires et commerciales françaises ;
> [Schumpeter (1939)](../bibliographie.md#schumpeter-1939) le popularise
> comme cycle d'investissement fixe et de crédit. C'est la bande sur
> laquelle CPV produit ses verdicts les plus solides en juin 2026 (V3),
> avec une divergence économique observée entre USA/ANGLO (expansion) et
> NORDIC (contraction profonde).

## Diagramme de phase polaire — panel Banque mondiale 2026

<figure markdown>
  ![Diagramme polaire Juglar — panel WB mai 2026](../figures/cycle_phase_polar_juglar_2026_05_wb.png){ width="90%" }
  <figcaption>
    <strong>Figure 1.</strong> Diagramme polaire de la bande Juglar
    (7-11 ans), panel Banque mondiale mai 2026. UMC et WLD ressortent
    en contraction profonde (quadrant gauche), seuls agrégats à passer
    les portes 1 et 2 sur ce run.
  </figcaption>
</figure>

## Diagramme de phase polaire — panel d'histoire longue (1870-2022)

<figure markdown>
  ![Diagramme polaire Juglar — panel long-history mai 2026](../figures/cycle_phase_polar_juglar_2026_05_long.png){ width="90%" }
  <figcaption>
    <strong>Figure 2.</strong> Diagramme polaire de la bande Juglar
    sur le panel d'histoire longue (Maddison + JST, 1870-2022, 18
    économies avancées). USA et ANGLO se positionnent dans le quadrant
    expansion (<em>φ</em> ≈ −1.5 rad, amplitude ~0.3) ; NORDIC est
    isolé dans le quadrant contraction profonde (<em>φ</em> ≈ −2.6 rad,
    amplitude ~0.4), avec un décalage d'environ 1.6 années de phase par
    rapport à USA — analyse économique :
    <a href="../reports/juglar_us_anglo_nordic_2026.md">Juglar US/ANGLO vs NORDIC 2022-2026</a>.
  </figcaption>
</figure>

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
