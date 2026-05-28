# Kitchin (3–5 ans)

> **Résumé.** Le plus court des quatre cycles canoniques.
> [Kitchin (1923)](../bibliographie.md#kitchin-1923) l'identifie sur les
> données de compensation bancaire et de prix de gros aux États-Unis ; il
> capture le rythme des stocks d'entreprises et des corrections de prix
> de court terme. Sur données annuelles WB, la borne basse (3 ans) est
> sous le seuil de Nyquist pratique ; CPV publie Kitchin uniquement sur
> la borne haute 4–5 ans.

## Diagramme de phase polaire — panel Banque mondiale 2026

![Diagramme polaire Kitchin — panel WB mai 2026](../figures/cycle_phase_polar_kitchin_2026_05_wb.png){ width="90%" }

Chaque point représente un agrégat positionné par sa phase $\varphi$
(angle) et son amplitude (rayon). Les cellules échouant à la Porte 1
(rejet par bruit AR(1) + scramble) ne sont pas tracées. Sur le run mai
2026, la quasi-totalité des cellules Kitchin sont `rejected` à
fréquence annuelle, d'où la rareté des points : c'est la conséquence
attendue du plafond de Nyquist annuel.

## Ce que mesure CPV

Le pipeline applique les quatre méthodes votantes (D, E, F, G) sur la
bande Kitchin $[3, 5]$ années. Sur données annuelles WB, la **borne basse
(3 ans) est sous le seuil de Nyquist** (l'échantillonnage annuel résout
en théorie les cycles $\geq 2$ ans, mais pratiquement $\geq 4$ ans pour
des séries macro bruitées). Le protocole pré-enregistre donc Kitchin
uniquement sur la borne haute 4–5 ans en annuel.

L'upsample trimestriel (spline cubique) est documenté comme variante de
sensibilité, jamais le défaut — voir
[Trois portes](../methodology/trois_portes.md) pour la règle anti-HARKing.

## Indicateurs moteurs (`cycles_manifest.json`)

- `NY.GDP.MKTP.KD.ZG` (croissance du PIB réel) — moteur principal.
- `FP.CPI.TOTL.ZG` (inflation IPC) — proxy du cycle stocks / prix.

## Caveats

- **Nyquist annuel** : Kitchin 3 ans non publié sur le panel WB.
- **Mode pilote** : sur les fenêtres de pilote (5–7 ans), Kitchin peut
  produire 1–2 cycles complets, ce qui est statistiquement borderline.
  La méthode F y est souvent rejetée tandis que G (Bry-Boschan) date
  encore des retournements.
- **Extension trimestrielle** : prévue en feuille de route #9
  ([Feuille de route](../methodology/feuille_de_route.md)). FRED GDPC1
  trimestriel permettrait CF sur la bande complète 3–5 ans.

## Références

- [Kitchin (1923)](../bibliographie.md#kitchin-1923)
- [Diebolt & Doliger (2008)](../bibliographie.md#diebolt-doliger-2008)
- [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010)
- [Harding & Pagan (2002)](../bibliographie.md#harding-pagan-2002)

## Voir aussi

- [Protocole CPV](../methodology/protocole_cpv.md)
- [Résultats panel Banque mondiale 2026-05](../reports/panel_banque_mondiale_2026.md)
