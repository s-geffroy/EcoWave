### Poids de preuve par cellule — p-values Gate 1 (2026-05)

| Agrégat | Source | Kitchin | Juglar | Kuznets | Kondratieff |
|---|---|---|---|---|---|
| `WLD` | WB | 🟢 0.002 | 🔴 0.444 | 🟠 0.054 | 🟢 0.001 |
| `G7` | WB | 🟡 0.029 | 🔴 0.267 | 🔴 0.714 | 🟠 0.055 |
| `OECD` | WB | 🟢 0.010 | 🔴 0.498 | 🔴 0.577 | 🟢 0.001 |
| `BRICS` | WB | 🟢 0.001 | 🔴 0.150 | 🔴 0.463 | 🔴 0.999 |
| `HIC` | WB | 🟢 0.010 | 🔴 0.589 | 🔴 0.351 | 🟢 0.001 |
| `UMC` | WB | 🟢 0.001 | 🟡 0.041 | 🔴 0.214 | 🔴 0.380 |
| `LMC` | WB | 🟡 0.014 | 🔴 0.540 | 🔴 0.746 | 🟠 0.063 |
| `LIC` | WB | 🟡 0.025 | 🔴 0.850 | 🔴 0.299 | 🔴 0.506 |
| `G7Q` | Path 5 | 🔴 0.106 | 🔴 0.531 | 🔴 0.120 | 🔴 0.608 |
| `OECDQ` | Path 5 | 🔴 0.106 | 🔴 0.531 | 🔴 0.120 | 🔴 0.608 |
| `USA` | Path 5 | 🔴 0.185 | 🔴 0.421 | 🟢 0.001 | 🔴 0.496 |
| `EA` | Path 5 | 🔴 0.388 | 🔴 0.252 | 🔴 0.428 | 🔴 0.957 |
| `JPN` | Path 5 | 🟢 0.001 | 🔴 0.528 | 🟡 0.041 | 🔴 0.804 |
| `GBR` | Path 5 | 🔴 0.297 | 🟡 0.025 | 🟢 0.004 | 🔴 0.430 |
| `ADV18` | Long | 🔴 0.860 | 🟢 0.001 | 🟢 0.001 | 🔴 0.684 |
| `G7` | Long | 🔴 0.706 | 🟡 0.041 | 🟢 0.001 | 🔴 0.130 |
| `EU4` | Long | 🔴 0.238 | 🔴 0.596 | 🟢 0.001 | 🟢 0.001 |
| `ANGLO` | Long | 🔴 0.994 | 🔴 0.953 | 🔴 0.408 | 🔴 0.758 |
| `NORDIC` | Long | 🟢 0.003 | 🟢 0.009 | 🔴 0.363 | 🔴 0.247 |
| `USA` | Long | 🔴 0.566 | 🟡 0.015 | 🔴 0.888 | 🔴 0.996 |
| `UK_BOE` | BoE | 🔴 0.126 | 🔴 0.856 | 🟡 0.024 | 🔴 0.892 |
| `BIS_EM` | BIS | 🟢 0.001 | 🟠 0.094 | 🟢 0.001 | 🔴 0.965 |
| `BIS_AE` | BIS | 🔴 0.757 | 🔴 0.360 | 🔴 0.188 | 🔴 0.979 |
| `BR_BIS` | BIS | 🔴 0.679 | 🔴 0.680 | 🔴 0.474 | 🔴 0.997 |
| `CN_BIS` | BIS | 🟡 0.044 | 🔴 0.878 | 🔴 0.337 | 🟡 0.025 |
| `IN_BIS` | BIS | 🔴 0.171 | 🔴 0.173 | 🟢 0.001 | 🔴 1.000 |
| `MX_BIS` | BIS | 🟡 0.015 | 🟠 0.092 | 🔴 0.414 | 🔴 0.739 |
| `KR_BIS` | BIS | 🟢 0.001 | 🔴 0.126 | 🟢 0.007 | 🔴 0.825 |
| `TR_BIS` | BIS | 🟢 0.001 | 🔴 0.706 | 🔴 0.447 | 🔴 1.000 |
| `ZA_BIS` | BIS | 🔴 0.223 | 🟢 0.005 | 🟢 0.001 | 🔴 0.457 |
| `RU_BIS` | BIS | 🔴 0.199 | 🟢 0.006 | 🔴 0.658 | 🔴 0.994 |
| `ID_BIS` | BIS | 🟢 0.007 | 🟡 0.021 | 🔴 0.313 | 🔴 0.541 |

Lecture : 🟢 `p ≤ 0.01` (signal fort, survivrait à α=0.01) · 🟡 `0.01 < p ≤ 0.05` (seuil standard CPV) · 🟠 `0.05 < p ≤ 0.10` (marginal, survivrait à α=0.10) · 🔴 `p > 0.10` (clairement null).

_p-values issues du test dual-null sur 1000 surrogates, **non corrigées** pour comparaisons multiples. Lecture Bonferroni-stricte sur 36 cellules WB : comparer à α ≈ 0.0014. Pour les conventions macro à α=0.10, traiter 🟢🟡🟠 comme survivants._
