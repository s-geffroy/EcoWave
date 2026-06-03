# Kondratieff (40–60 ans)

!!! warning "Verdict V3 (juin 2026) — Kondratieff *recasté*, pas vindiqué comme long-wave endogène"

    Source : `papers/cycles_refuted/sections/{01_introduction,05_results,07_conclusion}.tex`.

    **Le résultat le plus délicat du papier.** Seul **BoE Millennium 1700–2016** admet un test Kondratieff (les autres panels sont window-bound : WB max *N* = 65, JST max *N* = 151, Quarterly encore plus court ; [Torrence & Compo 1998](../bibliographie.md#torrence-compo-1998) requièrent ≥ 2.5 périodes complètes pour Gate 1, soit ≥ 100–150 ans et ≥ 240 obs. annuelles sur 40-60y).

    **Sur les 16 séries UK long-enough du BoE Millennium, seules deux séries de dette UK passent Gate 1** :

    | Cellule | *p*<sub>AR(1)</sub> | *p*<sub>ARFIMA</sub> | *d̂*<sub>GPH</sub> |
    |---|---|---|---|
    | UK dette publique (public-sector debt) | 0.002 | **0.022** | +0.436 |
    | UK dette centrale brute (central-gov gross) | 0.032 | **0.048** | +0.468 |

    **Toutes les autres séries UK Kondratieff-éligibles** (PIB réel, CPI, prix de gros, salaires réels, Bank Rate, actions, population) échouent Gate 1 sur les deux nulls, avec *p*<sub>1</sub> ∈ [0.10, 0.99].

    !!! info "Recast Reinhart-Rogoff : chronologie de dette de guerre"

        À l'inspection, la série UK debt/GDP 1700-2016 est **dominée par quatre chocs fiscaux exogènes** : pic de financement des guerres napoléoniennes (~1815), guerre de Crimée, deux guerres mondiales — séparés par des phases d'amortissement. Ce pattern est plus proche de la lecture **public-debt cycle** de [Reinhart & Rogoff (2009)](../bibliographie.md#reinhart-rogoff-2009) — où la période émerge de l'espacement des grandes guerres — que de la **long-wave endogène** de [Kondratieff (1925)](../bibliographie.md#kondratieff-1925) ou de [Schumpeter (1939)](../bibliographie.md#schumpeter-1939) (innovation, crédit, prix agricoles).

        Le null **ARFIMA(0, *d̂*, 0)** est crucial : *d̂*<sub>GPH</sub> est proche du clipping bound long-memory sur les deux séries de dette, donc l'AR(1) seul est mis-spécifié. La survie au null ARFIMA convertit ce qui aurait pu être un signal AR(1)-only en un finding **two-independent-nulls** robuste à la mémoire longue.

        Le **rolling-window R5** (Gate 1 sur fenêtres glissantes 80y, step 40y, 284 fenêtres) donne un pass-rate Kondratieff de 14.1 % (40 / 284), modestement élevé au-dessus du nominal 5 %, **compatible avec une présence intermittente** plutôt qu'une cyclicité stationnaire sur 1700-2016. La heat-map localise la puissance maximale **post-1815** (amortissement napoléonien) et **post-1945** (build-up WWII) — windows que la lecture R-R anticipe.

    **Ce que V3 ne revendique pas** : une vindication de la long-wave endogène de Kondratieff sur les variables macro qu'il aurait reconnues (PIB réel, CPI, salaires, actions, population — toutes échouent les deux nulls sur BoE). « Kondratieff » est conservé comme **nom de bande** (40–60y) par convention, **pas comme support à la théorie substantive**.

    **Ce qui falsifierait ou élargirait le verdict** : une réplication cross-country avec des séries de dette longues hors-UK (Toutain France [Toutain 1997](../bibliographie.md#toutain1997), Allemagne, Pays-Bas) trancherait entre signature multi-pays de financement-guerre vs. artefact spécifique à l'empire britannique (priorité d'extension V4).

> **Résumé historique.** L'onde longue. [Kondratieff (1925)](../bibliographie.md#kondratieff-1925)
> l'identifie à partir de séries de niveau de prix et de taux d'intérêt ;
> elle est ensuite associée à des clusters d'innovation techno-économique
> ([Schumpeter, 1939](../bibliographie.md#schumpeter-1939) ;
> [Mensch, 1979](../bibliographie.md#mensch-1979)) et à des super-cycles de
> prix de matières premières. **V3 ré-encadre** le résultat sur BoE
> comme chronologie de dette de guerre Reinhart-Rogoff plutôt que comme
> vindication de la long-wave endogène ; les autres panels sont
> window-bound.

## Diagramme de phase polaire — panel d'histoire longue (1870-2022)

<figure markdown>
  ![Diagramme polaire Kondratieff — panel long-history mai 2026](../figures/cycle_phase_polar_kondratieff_2026_05_long.png){ width="90%" }
  <figcaption>
    <strong>Figure 1.</strong> Diagramme polaire de la bande Kondratieff
    (40-60 ans), panel d'histoire longue (Maddison + JST, 1870-2022).
    Seuls ADV18 et EU4 passent la Porte 1 ; tous deux émergent avec
    <em>φ</em> ≈ 0 (cellule <code>disputed</code> au pic du cycle K5),
    amplitude ~0.85 — soit environ la moitié des pics K3 (~1.55 vers
    1920) et K4 (~1.28 vers 1973). Analyse complète :
    <a href="../reports/kondratieff_adv18_eu4_2026.md">Kondratieff K5 — ADV18 / EU4</a>.
  </figcaption>
</figure>

## Ce que mesure CPV

Le pipeline applique les quatre méthodes votantes (D, E, F, G) sur la
bande Kondratieff $[40, 60]$ années. C'est **la bande où le caveat
small-N est le plus aigu** : les séries Banque mondiale démarrent en
1960, fournissant environ 65 ans de données — soit grossièrement
1.0–1.5 K-wave d'historique. Sur le panel d'histoire longue (1870-2022,
153 années), $\geq 2.5$ K-waves sont disponibles, ce qui permet à la
Porte 1 de rejeter le null sur ADV18 et EU4.

Le null AR(1) + scramble (Porte 1) **rejette fréquemment la séparabilité
de Kondratieff** sur le panel WB, pour plusieurs agrégats de revenu.
**C'est honnête, pas un échec** : des échantillons courts ne peuvent pas
distinguer de façon fiable une oscillation multi-décennale unique d'un
bruit auto-corrélé. Le protocole CPV publie `separable = 0` plutôt que
de fabriquer une phase.

Les caveats d'endpoint sont sévères : le filtre CF est instable sur les
$\lfloor 60 / 2 \rfloor = 30$ dernières années pour Kondratieff. Le
rapport courant signale ce drapeau explicitement.

## Indicateurs moteurs

- `NY.GDP.PCAP.KD` (PIB réel par habitant, log-différence) — proxy de
  productivité onde-longue.
- `FS.AST.PRVT.GD.ZS` (crédit domestique / PIB) — super-cycle de crédit
  Reinhart-Rogoff.
- (Histoire longue) `LH_GDP` (Maddison) + `LH_CREDIT` (JST) sur 153 ans.

## Caveats

- **Small-N WB** : 65 ans $\approx 1.0$–$1.5$ K-wave → Porte 1
  systématiquement rejetée pour la plupart des agrégats WB.
- **Endpoint CF sévère** : 30 dernières années instables sur la bande
  haute. `endpoint_caveat = 1` systématique sur les cellules
  Kondratieff.
- **Disputed au pic** : sur ADV18 et EU4 en mai 2026,
  $\varphi \approx 0$ (pic) ; trois méthodes votent peak / expansion /
  contraction sans consensus à 3/4, d'où `phase = disputed`. Voir
  [K5 ADV18/EU4](../reports/kondratieff_adv18_eu4_2026.md).
- **Recouvrement avec le cycle financier** : la K-wave et le cycle
  financier Borio-Drehmann (~15–20 ans) coexistent ; la décomposition
  CF sépare les deux mais la séparation est imparfaite sur les fenêtres
  courtes.

## Références

- [Kondratieff (1925)](../bibliographie.md#kondratieff-1925)
- [Schumpeter (1939)](../bibliographie.md#schumpeter-1939)
- [Mensch (1979)](../bibliographie.md#mensch-1979)
- [Modelski (1987)](../bibliographie.md#modelski-1987)
- [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010)
- [Reinhart & Rogoff (2009)](../bibliographie.md#reinhart-rogoff-2009)
- [Gordon (2016)](../bibliographie.md#gordon-2016)
- [Summers (2014)](../bibliographie.md#summers-2014)
- [Perez (2002)](../bibliographie.md#perez-2002)

## Voir aussi

- [Protocole CPV](../methodology/protocole_cpv.md)
- [Analyse K5 ADV18/EU4](../reports/kondratieff_adv18_eu4_2026.md)
- [Résultats panel d'histoire longue 2026-05](../reports/histoire_longue_2026.md)
