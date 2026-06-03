# Kitchin (3–5 ans)

!!! success "Verdict V3 (juin 2026) — Kitchin vivant sur crédit BIS EM ; BoE déclassé"

    Source : `papers/cycles_refuted/sections/{01_introduction,05_results}.tex`.

    **La concentration la plus nette du papier**. Sur le panel **BIS quarterly** (93 cellules Kitchin testables), **25 cellules passent Gate 1 unadjusted**, soit **5.3× l'excès sur null** — la plus grosse concentration positive du papier. La signature est sans ambiguïté :

    - Agrégats crédit BIS marchés émergents (credit-to-GDP gap, credit-to-GDP ratio, total credit, household credit, business credit, real residential property prices) sur **Corée, Chine, Mexique, Afrique du Sud, Turquie, Russie, Indonésie** — *p*<sub>1</sub> ≈ floor surrogate 0.003.
    - Chômage économies avancées (G7Q, OECDQ, GBR, JPN) à *p*<sub>1</sub> ≈ 0.01.

    Sur **WB annuel** : 5 / 50 cellules (excès 2×) sur agrégats financiers et commerciaux EM (BRICS inflation *p*<sub>1</sub> = 0.008 ; BRICS financial flows *p*<sub>1</sub> = 0.014 ; LIC investment *p*<sub>1</sub> = 0.024 ; LMC trade *p*<sub>1</sub> = 0.040 ; WLD trade *p*<sub>1</sub> = 0.048).

    Sur le **panel sectoriel** (test Wen 2005) : 3 / 26 cellules (US wheat *p*<sub>1</sub> = 0.040, US WPI *p*<sub>1</sub> = 0.015, world coal *p*<sub>1</sub> = 0.020).

    !!! warning "BoE Kitchin déclassé comme artefact band-edge (R4)"

        Sur **BoE Millennium**, le pass-rate Kitchin unadjusted est 7.7 % (5 / 65 séries testables). Le **test R4 de sensibilité band-edge** révèle une instabilité asymétrique à une perturbation d'1 an : resserrer la borne basse de `[3,5]` à `[4,5]` effondre le pass-rate à **0.0 %** ; élargir la borne haute à `[3,6]` le double à 16.9 %. Signature d'un **artefact de bande**, pas d'un cycle substantif. La cellule BoE Kitchin est **exclue** du support à la vindication Kitchin. La cellule BIS quarterly sur les agrégats crédit EM reste le verdict load-bearing Kitchin.

    **Lecture V3** : vindication substantive de [Kitchin (1923)](../bibliographie.md#kitchin-1923) et de l'hypothèse d'inventaire/credit [Wen (2005)](../bibliographie.md#wen-2005) sur les agrégats EM ; lecture universaliste rejetée BH-FDR.

> **Résumé historique.** Le plus court des quatre cycles canoniques.
> [Kitchin (1923)](../bibliographie.md#kitchin-1923) l'identifie sur les
> données de compensation bancaire et de prix de gros aux États-Unis ; il
> capture le rythme des stocks d'entreprises et des corrections de prix
> de court terme. Sur données annuelles WB, la borne basse (3 ans) est
> sous le seuil de Nyquist pratique ; CPV publie Kitchin uniquement sur
> la borne haute 4–5 ans.

## Diagramme de phase polaire — panel Banque mondiale 2026

<figure markdown>
  ![Diagramme polaire Kitchin — panel WB mai 2026](../figures/cycle_phase_polar_kitchin_2026_05_wb.png){ width="90%" }
  <figcaption>
    <strong>Figure 1.</strong> Diagramme polaire de la bande Kitchin
    (3-5 ans), panel Banque mondiale mai 2026. Chaque point représente
    un agrégat positionné par sa phase de Hilbert <em>φ</em> (angle) et
    son amplitude (rayon). Les quatre quadrants correspondent aux
    étiquettes canoniques expansion / peak / contraction / trough. Les
    cellules échouant à la Porte 1 (null AR(1) + scramble) ne sont pas
    tracées ; sur ce run, presque toutes les cellules Kitchin sont
    rejetées, conséquence attendue du plafond de Nyquist annuel.
  </figcaption>
</figure>

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

### Chemin trimestriel natif (Roadmap #9 — implémenté)

L'option `position-cycles --horizon quarterly` active un second chemin
d'ingestion fondé sur des séries trimestrielles natives (FRED `GDPC1`,
Eurostat `namq_10_gdp`, OECD QNA `B1_GE/VOBARSA`). À
`samples_per_year = 4`, le filtre CF couvre la bande complète 3-5 ans
(12-20 échantillons par période) — bien au-dessus du seuil de Nyquist
pratique. Le rapport `cycle_position_<as_of>_q.md` publie alors des
phases concrètes pour Kitchin, là où le chemin annuel WB continue à
publier `rejected` (valeur diagnostique conservée). Voir
[Feuille de route #9](../methodology/feuille_de_route.md).

## Indicateurs moteurs (`cycles_manifest.json`)

- `NY.GDP.MKTP.KD.ZG` (croissance du PIB réel) — moteur principal.
- `FP.CPI.TOTL.ZG` (inflation IPC) — proxy du cycle stocks / prix.

## Caveats

- **Nyquist annuel** : Kitchin 3 ans non publié sur le panel WB.
- **Mode pilote** : sur les fenêtres de pilote (5–7 ans), Kitchin peut
  produire 1–2 cycles complets, ce qui est statistiquement borderline.
  La méthode F y est souvent rejetée tandis que G (Bry-Boschan) date
  encore des retournements.
- **Extension trimestrielle** : implémentée (feuille de route #9). Activable
  via `position-cycles --horizon quarterly` — FRED GDPC1 + Eurostat `namq_10_gdp`
  + OECD QNA sur USA / EA / JPN / GBR / G7Q / OECDQ, permettant le filtre CF
  sur la bande complète 3–5 ans.

## Références

- [Kitchin (1923)](../bibliographie.md#kitchin-1923)
- [Diebolt & Doliger (2008)](../bibliographie.md#diebolt-doliger-2008)
- [Korotayev & Tsirel (2010)](../bibliographie.md#korotayev-tsirel-2010)
- [Harding & Pagan (2002)](../bibliographie.md#harding-pagan-2002)

## Voir aussi

- [Protocole CPV](../methodology/protocole_cpv.md)
- [Résultats panel Banque mondiale 2026-05](../reports/panel_banque_mondiale_2026.md)
