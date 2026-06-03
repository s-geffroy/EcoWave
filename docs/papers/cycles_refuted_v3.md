# Cycles Refuted V3 — résumé portail

> **Working paper.** *Cycles Refuted: a falsifiable single-protocol
> assessment of the four canonical macroeconomic cycles across five
> independent panels, 1700–2024.* Geffroy S., juin 2026. Source LaTeX
> sous `papers/cycles_refuted/` ; PDF construit par
> `docker compose run --rm cycles-refuted make pdf`. Cible *Physica A*
> / *Journal of Economic Behavior & Organization*.

!!! success "Verdict V3 en une phrase"

    Trois cycles canoniques **vindiqués** sur exactement les variables que leur théorie d'origine nomme ; Kondratieff **recasté** comme chronologie de dette de guerre Reinhart-Rogoff ; lecture **universaliste sinusoïdale-sur-tout rejetée** par BH-FDR sur grille jointe.

## Pourquoi une V3

La V3 est la réponse complète aux **10 recommandations** d'un rapport de
referee TSE qui a poussé le papier à durcir simultanément (a) le null,
(b) la lecture interprétative et (c) le vocabulaire de pré-engagement.
Le détail intégral est dans le `CHANGELOG.md` du projet (entrée
2026-06-03). Les quatre changements majeurs :

1. **Dual null Gate 1** : AR(1) bootstrap (primaire) + ARFIMA(0, *d̂*<sub>GPH</sub>, 0)
   (robustesse long-memory). 97–100 % des cellules JST/BoE ont
   *|d̂|* > 0.1, ce qui rend l'AR(1) seul mis-spécifié sur les niveaux
   bruts. La lecture load-bearing sur cellules long-memory est la
   lecture ARFIMA-conditional.
2. **Per-cell long-memory & stationarity diagnostics** : ADF, KPSS,
   GPH *d̂*, DFA Hurst. Médiane *H*<sub>DFA</sub> = 1.76 sur JST R6,
   1.64 sur BoE Millennium.
3. **R4 band-edge sensitivity** (± 1 an pour Kitchin/Juglar,
   ± 2 ans pour Kuznets/Kondratieff). Conduit au **déclassement de
   la cellule BoE Kitchin** comme artefact de bande (pass-rate 7.7 %
   sur [3,5] → 0.0 % sous resserrement [4,5]).
4. **Recast Kondratieff** : la seule positive (UK dette) est lue
   comme chronologie de dette de guerre Reinhart-Rogoff (Napoléon
   ~1815, Crimée, WWI, WWII), pas comme vindication de la long-wave
   endogène. Toutes les autres séries UK Kondratieff-éligibles
   échouent les deux nulls. Le rolling-window R5 localise la
   puissance maximale post-1815 et post-1945 (windows que la lecture
   R-R anticipe).

Auxiliairement :

- **R5 rolling-window Gate 1** à 50-80y windows pour cartographier la
  présence temporelle.
- Vocabulaire **« threshold transparency »** au lieu de
  « pre-registration » (les bornes sont figées en Git public ; OSF /
  AEA n'est pas revendiqué — engagement prospectif pour la
  réplication out-of-sample post-2024).
- **LH_XRUSD flag « théorique faux positif »** : passe Juglar sur
  11 / 18 pays JST (61 %), exclu de la claim « investissement-et-chômage »
  car le mécanisme Juglar ne prédit pas le taux de change bilatéral USD.
- **Benjamini-Hochberg FDR** au seuil 0.05 sur grille jointe :
  *p\** = 3.4 × 10⁻⁵ vs. floor 1/(*B*+1) ≈ 10⁻³ aux surrogate counts
  actuels — aucune cellule individuelle n'y survit ; la lecture
  universaliste sinusoïdale-sur-tout est rejetée.

## Verdict V3 en chiffres

Source de vérité : `papers/cycles_refuted/sections/{00_abstract,01_introduction,05_results,07_conclusion}.tex`.

### Vue d'ensemble

| Bloc | Pass / testable | Excès | Lecture V3 |
|---|---|---|---|
| Total Gate 1 unadjusted | **166 / 1 456** | **2.3×** | concentrations variable-spécifiques |
| Lecture universaliste (BH-FDR) | **0** | n/a | floor > p* — **rejetée** |

### Juglar (7-11 ans) — vindiqué

| Source | Pass / testable | Excès | Notes |
|---|---|---|---|
| JST R6 (1870–2020, 18 économies avancées) | **67 / 605** | **2.2×** | LH_INV 39 % (CH/CA *p*<sub>1</sub> = 0.001) ; LH_UNRATE 33 % ; LH_BUSCREDIT 33 % |
| Quarterly (1995–2024) | 12 / 55 | 4.3× | G7Q / OECDQ / GBR / JPN chômage |
| BoE Millennium UK chômage | 1 cellule | dual null | *p*<sub>AR(1)</sub> = 0.004 · *p*<sub>ARFIMA</sub> = 0.002 à *d̂* = 0.49 |

**Théorique faux positif** : LH_XRUSD passe sur 11 / 18 (61 %), exclu de la claim car le mécanisme Juglar ne prédit pas le taux de change bilatéral USD.

### Kuznets (15-25 ans) — vindiqué

| Source | Pass / testable | Excès | Notes |
|---|---|---|---|
| JST R6 | **51 / 529** | **1.9×** | LH_HPI 46 % (6/13) ; LH_POP 39 % ; LH_CREDIT 41 % ; LH_MORT 5 ; LH_DEBTGDP & LH_CA 4 |
| BoE | UK debt / GDP (*p*<sub>1</sub> = 0.006) | — | + BoE real-effective / nominal-effective exchange rate passent dual null |

### Kitchin (3-5 ans) — vindiqué ; BoE déclassé R4

| Source | Pass / testable | Excès | Notes |
|---|---|---|---|
| BIS quarterly EM credit | **25 / 93** | **5.3×** | KR/CN/MX/ZA/TR/RU/ID, *p*<sub>1</sub> ≈ floor 0.003 |
| WB annuel | 5 / 50 | 2× | BRICS inflation, BRICS financial flows, LIC investment, LMC trade, WLD trade |
| Sectoral (test Wen 2005) | 3 / 26 | — | US wheat, US WPI, world coal |
| BoE Millennium | déclassé | — | pass-rate 7.7 % [3,5] → **0 % sous [4,5]** (R4 band-edge artefact) |

### Kondratieff (40-60 ans) — recasté Reinhart-Rogoff

Seul BoE Millennium admet un test (autres panels short-window). Sur
les 16 séries UK long-enough :

| Cellule | *p*<sub>AR(1)</sub> | *p*<sub>ARFIMA</sub> | *d̂*<sub>GPH</sub> | Lecture |
|---|---|---|---|---|
| UK public-sector debt | 0.002 | 0.022 | +0.436 | ♻️ chronologie R-R |
| UK central-gov gross debt | 0.032 | 0.048 | +0.468 | ♻️ chronologie R-R |
| UK real GDP, CPI, real wages, share prices, population… | > 0.10 | > 0.10 | — | échec |

**Lecture V3** : la chronologie est dominée par les pics de financement
des grandes guerres (Napoléon ~1815, Crimée, WWI, WWII) puis
amortissement. Pas un mécanisme endogène à la Kondratieff. La R5
rolling-window pass-rate de 14.1 % (40 / 284 fenêtres 80y) est
modestement élevée au-dessus du 5 % nominal, cohérent avec présence
intermittente plutôt que cyclicité stationnaire. La puissance maximale
est localisée post-1815 et post-1945, windows que la lecture R-R
anticipe.

## Pour aller plus loin

- **Méthode** :
  [Gate 1 dual null AR(1) + ARFIMA](../methodology/arfima_dual_null.md) ·
  [Diagnostics par cellule (ADF/KPSS/GPH/DFA)](../methodology/long_memory_diagnostics.md) ·
  [Band-edge sensitivity R4](../methodology/band_sensitivity.md) ·
  [Rolling-window R5](../methodology/rolling_window_gates.md) ·
  [Trois portes V3](../methodology/trois_portes.md).
- **Verdict par panel** :
  [synthèse multi-horizons](../reports/cycle_position_synthesis.md) ·
  [BoE](../reports/cycle_position_2026_05_boe.md) ·
  [BIS](../reports/cycle_position_2026_05_bis.md) ·
  [WB](../reports/cycle_position_2026_05_wb.md) ·
  [Quarterly](../reports/cycle_position_2026_05_q.md) ·
  [Long history](../reports/cycle_position_2026_05_long.md) ·
  [Sectoral](../reports/cycle_position_2026_05_sh.md).
- **Évidence par variable** :
  [evidence_per_variable.md](../evidence_per_variable.md).
- **Pages cycles** :
  [Kitchin](../cycles/kitchin.md) ·
  [Juglar](../cycles/juglar.md) ·
  [Kuznets](../cycles/kuznets.md) ·
  [Kondratieff](../cycles/kondratieff.md).
- **Companion paper en préparation** (cluster CBDIS + benchmark
  PASS 78 %) : [forecast_benchmark.md](../forecast_benchmark.md).
- **Archive V1** :
  [cpv_main_paper.md](cpv_main_paper.md) (dramaturgie réfutation-first,
  thèse pré-V3 — conservée pour historicité).

## Citation

```bibtex
@unpublished{geffroy_cycles_refuted_v3,
  author       = {Geffroy, Sylvain},
  title        = {{Cycles Refuted: a falsifiable single-protocol
                   assessment of the four canonical macroeconomic
                   cycles across five independent panels, 1700–2024}},
  note         = {Working paper, version V3 (TSE referee response),
                  June 2026},
  url          = {https://github.com/s-geffroy/EcoWave/tree/main/papers/cycles_refuted}
}
```
