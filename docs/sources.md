# Sources de données

> **Résumé.** Toutes les séries ci-dessous sont ingérées automatiquement avec
> provenance complète : chaque payload brut est stocké sous
> `data_raw/<fournisseur>/` et enregistré dans SQLite (`sources`, `raw_files`
> avec SHA-256). Cette page est générée à partir de `sources_manifest.json`
> — la **source unique de vérité**.

## Variables ingérées

| Variable | Courbe | Jeu de données | Fournisseur | Identifiant | Confiance | Note de licence |
|---|---|---|---|---|---|---|
| E1 | E | CBOE Volatility Index : VIX | FRED | `VIXCLS` | A | vérifier avant redistribution |
| E2 | E | TED Spread (arrêté en 2022 ; historique 2007-2012 disponible) | FRED | `TEDRATE` | A | vérifier avant redistribution |
| E3 | E | NASDAQ Composite Index (proxy de drawdown actions large) | FRED | `NASDAQCOM` | A | vérifier avant redistribution |
| E4 | E | Croissance du PIB réel trimestriel — composite US + zone euro | FRED | `GDPC1 + CLVMNACSCAB1GQEA19` | B | US (GDPC1) + Zone euro (CLVMNACSCAB1GQEA19) ; chacun normalisé sur son historique |
| E5 | E | Taux de chômage — composite US + zone euro (mensuel) | FRED | `UNRATE + LRHUTTTTEZM156S` | B | US (UNRATE) + Zone euro (LRHUTTTTEZM156S) |
| E6 | E | Inflation YoY déviation de 2 % — composite US + zone euro (mensuel) | FRED | `CPIAUCSL + CP0000EZ19M086NEST` | B | US (CPIAUCSL) + Zone euro HICP (CP0000EZ19M086NEST) ; cible 2 % |
| D1 | D | Composite Indicator of Systemic Stress (zone euro, quotidien) | ECB | `CISS/D.U2.Z0Z.4F.EC.SS_CIN.IDX` | A | ECB Data Portal ; vérifier avant redistribution |
| D2 | D | Spreads souverains 10 ans périphérie euro vs Allemagne — panier IT/ES/PT (mensuel) | FRED | `IRLTLT01ITM156N−IRLTLT01DEM156N + IRLTLT01ESM156N−IRLTLT01DEM156N + IRLTLT01PTM156N−IRLTLT01DEM156N` | B | Taux long OECD via FRED ; panier périphérique vs Allemagne |
| S1 | S | Taux de chômage des jeunes, 15-24 ans, zone euro (mensuel) | FRED | `LRHU24TTEZM156S` | B | OECD/Eurostat via FRED ; active la courbe sociale (S) |
| L1 | L | Prix du pétrole brut Brent — Europe (quotidien) | FRED | `DCOILBRENTEU` | A | vérifier avant redistribution |
| D3 | D | Intensité d'intervention publique (compte mensuel d'événements institutionnels D) | EVENTS_DERIVED | `—` | C | Dérivé de events_master.csv ; pas de baseline pré-crise → statut partiel |
| L2 | L | Importations mondiales de biens et services, volume (Banque mondiale, WLD, annuel) | WORLD_BANK | `NE.IMP.GNFS.KD` | B | World Bank Open Data (CC BY 4.0) ; volume annuel de commerce mondial, contraction YoY = stress |
| I1 | I | Volume médiatique de crise — Economic Policy Uncertainty, US + Europe (mensuel) | FRED | `USEPUINDXM + EUEPUINDXM` | C | Baker-Bloom-Davis EPU via FRED (comptage d'articles) ; proxy I1 sans GDELT |

## Variables non-automatisables en V1

| Variable | Raison |
|---|---|
| S2 | Protestations anti-austérité : pas de source mensuelle ouverte pour 2010-2012 (l'ONU ne suit pas les protestations ; ACLED ne couvre l'Europe qu'à partir de ~2020). Curation manuelle uniquement. |
| I2 | Tonalité / négativité médiatique : nécessite des données de sentiment (par ex. GDELT tone) ; pas de substitut ONU/Banque mondiale |

## Variables du panel d'histoire longue

| Variable | Source | Identifiant | Couverture |
|---|---|---|---|
| LH_GDP | Maddison Project Database 2023 | `gdppc` | 1820-2022, 169 pays |
| LH_CREDIT | Jordà-Schularick-Taylor R6 | `tloans` | 1870-2020, 18 pays |
| LH_HPI | Jordà-Schularick-Taylor R6 | `hpnom / cpi → réel` | 1870-2020, 18 pays |
| LH_EQUITY | Jordà-Schularick-Taylor R6 | `eq_capgain` | 1870-2020, 18 pays |
| LH_YIELD | Jordà-Schularick-Taylor R6 | `ltrate` | 1870-2020, 18 pays |
| LH_CPI | Jordà-Schularick-Taylor R6 | `cpi` | 1870-2020, 18 pays |

## Variables du panel CPV principal (Banque mondiale)

| Code | Série WB | Cible cyclique |
|---|---|---|
| CY_GDP | `NY.GDP.MKTP.KD.ZG` | Toutes bandes (croissance PIB réel) |
| CY_INV | `NE.GDI.TOTL.ZS` | Juglar (investissement fixe) |
| CY_INF | `FP.CPI.TOTL.ZG` | Kitchin / Juglar (inflation IPC) |
| CY_UEM | `SL.UEM.TOTL.ZS` | Juglar (chômage) |
| CY_TRD | `NE.TRD.GNFS.ZS` | Juglar / Kuznets (commerce % PIB) |
| CY_POP | `SP.URB.TOTL.IN.ZS` | Kuznets (urbanisation) |
| CY_FIN | `FS.AST.PRVT.GD.ZS` | Juglar / Kondratieff (crédit domestique) |
| CY_PRD | `NY.GDP.PCAP.KD` | Kondratieff (PIB par habitant) |

## Fournisseurs & citations

- **ECB** — Banque centrale européenne — ECB Data Portal,
  <https://data.ecb.europa.eu>. CISS : Hollo, Kremer & Lo Duca (2012),
  ECB Working Paper 1426.
- **EVENTS_DERIVED** — Événements curés par EcoWave
  (`events/events_master.csv`) — curation manuelle, sources à vérifier
  par ligne.
- **FRED** — Federal Reserve Bank of St. Louis — FRED® (Federal Reserve
  Economic Data), <https://fred.stlouisfed.org>.
  Conditions : <https://fred.stlouisfed.org/legal/>.
- **WORLD_BANK** — Banque mondiale — *World Development Indicators* /
  World Bank Open Data, <https://data.worldbank.org>. Licence : CC BY 4.0.
- **MADDISON_PROJECT** — Bolt, J., & van Zanden, J. L. (2024). Maddison
  Project Database 2023, <https://www.rug.nl/ggdc/historicaldevelopment/maddison/>.
- **MACROHISTORY** — Jordà-Schularick-Taylor Macrohistory Database
  (Release 6), <https://www.macrohistory.net/database/>.

## Sources amont (créditées au-delà de l'hôte API)

- **Economic Policy Uncertainty (I1)** — Baker, S. R., Bloom, N., & Davis,
  S. J. (2016), *Measuring Economic Policy Uncertainty*, *Quarterly
  Journal of Economics* 131(4). Séries `USEPUINDXM`, `EUEPUINDXM` via FRED.
- **Taux des emprunts d'État long terme (D2)** — OECD Main Economic
  Indicators, via FRED (`IRLTLT01{IT,ES,PT,DE}M156N`).
- **HICP zone euro (E6) et PIB réel (E4)** — Eurostat, via FRED
  (`CP0000EZ19M086NEST`, `CLVMNACSCAB1GQEA19`).
- **CBOE Volatility Index (E1)** — Cboe Global Markets, via FRED
  (`VIXCLS`).

!!! warning "Redistribution"
    Les payloads bruts d'API ne sont **pas** redistribués sur ce site.
    Vérifiez la licence de chaque fournisseur avant toute redistribution
    de données brutes. Les panels mensuels agrégés sont des statistiques
    dérivées.
