# Forecast benchmark — Roadmap #20

> **Run.** `as_of = 2026-05`, horizon data `long`.

## Verdict

✅ **PASS** — pass rate 100% (threshold 50%) on 5 variables with baseline comparator at horizon 12.

The empirical-cluster picture gains a constructive operational counterpart — at least one cluster model outperforms the random walk on out-of-sample CRPS at the decision horizon on the required 50 % of variables.

## Mean CRPS — decision horizon

At the decision horizon ``h = 12``. Cluster models that beat the random-walk baseline appear in **bold**.

| variable | rw | ar1 | arma11 | har | arfima_rs | msm | best |
|---|---|---|---|---|---|---|---|
| ADV18::LH_CPI | 672.4283 | 672.4283 | 669.1694 | **666.3171** | **672.4204** | **631.6137** | msm ✓ |
| ADV18::LH_CREDIT | 10083291.9978 | 10083291.9978 | 9924834.1540 | 101436637.6800 | **8979123.5886** | 14317034.3126 | arfima_rs ✓ |
| ADV18::LH_EQUITY | 12137661.7481 | 2356088.0786 | 2437032.6498 | **2505185.6540** | **30474.4765** | **17360.2844** | msm ✓ |
| ADV18::LH_GDP | 7784.4122 | 7784.4122 | 6813.8135 | **3993.2298** | 9009.3853 | **2249.9072** | msm ✓ |
| ADV18::LH_HPI | 71.3958 | 71.3958 | 70.7784 | 130.3667 | 72.1568 | **70.3810** | msm ✓ |

## Mean CRPS — h = 1

| variable | rw | ar1 | arma11 | har | arfima_rs | msm | best |
|---|---|---|---|---|---|---|---|
| ADV18::LH_CPI | 2.4535 | 2.4535 | 0.6381 | **0.8315** | 5.3990 | **0.9920** | har ✓ |
| ADV18::LH_CREDIT | 378578.6489 | 378578.6489 | 287481.3364 | **323595.7255** | 572856.5196 | 500205.1988 | har ✓ |
| ADV18::LH_EQUITY | 3495222.0196 | 2279564.6645 | 2590758.3305 | **2665498.3415** | **12015.9282** | **96.6076** | msm ✓ |
| ADV18::LH_GDP | 778.2239 | 778.2239 | 337.0418 | **106.2745** | 1712.4030 | **310.9117** | har ✓ |
| ADV18::LH_HPI | 4.2181 | 4.2181 | 4.9820 | **4.2120** | 11.5072 | **3.4606** | msm ✓ |


## Mean CRPS — h = 3

| variable | rw | ar1 | arma11 | har | arfima_rs | msm | best |
|---|---|---|---|---|---|---|---|
| ADV18::LH_CPI | 6.9622 | 6.9622 | 4.3968 | **2.9167** | 11.2181 | **2.1457** | msm ✓ |
| ADV18::LH_CREDIT | 1826207.0741 | 1826207.0741 | 1725059.1941 | 3744810.7071 | **1189899.1874** | 2337543.6897 | arfima_rs ✓ |
| ADV18::LH_EQUITY | 6311213.7982 | 2648981.6340 | 2564183.1521 | **2569577.5366** | **39171.8268** | **306.7176** | msm ✓ |
| ADV18::LH_GDP | 2168.4433 | 2168.4433 | 1645.8609 | **1171.5913** | 3731.3306 | **1092.7644** | msm ✓ |
| ADV18::LH_HPI | 16.7077 | 16.7077 | 15.0417 | 21.0876 | 32.2911 | **12.1576** | msm ✓ |


## Mean CRPS — h = 6

| variable | rw | ar1 | arma11 | har | arfima_rs | msm | best |
|---|---|---|---|---|---|---|---|
| ADV18::LH_CPI | 15.2474 | 15.2474 | 11.8823 | **6.7600** | 18.9931 | **6.1045** | msm ✓ |
| ADV18::LH_CREDIT | 3023166.4980 | 3023166.4980 | 2889374.6813 | 14954237.4879 | **2291622.2519** | 4544529.2776 | arfima_rs ✓ |
| ADV18::LH_EQUITY | 8896696.6267 | 2637537.6699 | 2398001.1453 | **2621815.1111** | **10355.5447** | **464.9916** | msm ✓ |
| ADV18::LH_GDP | 4086.4755 | 4086.4755 | 3167.5592 | **1981.3668** | 5775.7018 | **1461.5326** | msm ✓ |
| ADV18::LH_HPI | 50.3286 | 50.3286 | 45.2200 | **45.7830** | 70.2553 | **21.9589** | msm ✓ |


## Per-variable pass/fail

| variable | best cluster model | beats RW @ h = 12 |
|---|---|---|
| ADV18::LH_CPI | msm | ✓ |
| ADV18::LH_CREDIT | arfima_rs | ✓ |
| ADV18::LH_EQUITY | msm | ✓ |
| ADV18::LH_GDP | msm | ✓ |
| ADV18::LH_HPI | msm | ✓ |

## Method

Each variable's tail is held out as the test region. Inside the test region we place ``n_origins = 3`` evenly-spaced forecast origins, fit each model on the history up to the origin, and score the resulting probabilistic forecast against the realised value at each horizon. Scores are averaged across origins to yield the per-cell summary tables above. Probabilistic samples per forecast: ``100``. RNG seed: ``0``. CRPS is the proper scoring rule of Gneiting-Raftery 2007 ; lower is better.

Generated at 2026-06-01T16:21:25+00:00 by `ecowave forecast-benchmark`.
