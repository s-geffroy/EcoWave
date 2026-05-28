# Kondratieff (40–60 ans)

> **Résumé.** L'onde longue. [Kondratieff (1925)](../bibliographie.md#kondratieff-1925)
> l'identifie à partir de séries de niveau de prix et de taux d'intérêt ;
> elle est ensuite associée à des clusters d'innovation techno-économique
> ([Schumpeter, 1939](../bibliographie.md#schumpeter-1939) ;
> [Mensch, 1979](../bibliographie.md#mensch-1979)) et à des super-cycles de
> prix de matières premières. C'est la bande où le verrou du *small-N* est
> le plus aigu sur le panel WB ; le panel d'histoire longue
> (Maddison + JST, 1870-2022) permet de la trancher proprement.

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
