"""Pre-registered cycle bands + group code mapping. Frozen by design.

The frequency ranges are taken from the canonical literature
(Korotayev & Tsirel 2010; Diebolt & Doliger 2008) and locked in code rather than
in a config file: any change requires methodology review (Gate 1 of CPV).

Group codes mix official World Bank aggregates (WLD, OED, HIC, UMC, LMC, LIC)
with project-recomputed lists (G7, G20, BRICS). The WB aggregates are preferred
when present because they implement the same GDP-weighted methodology applied
by the World Bank itself; for G7/G20/BRICS we recompute (GDP-weighted) since
no official WB aggregate exists.
"""
from __future__ import annotations

from types import MappingProxyType

CYCLE_BANDS = MappingProxyType({
    "kitchin":     {"lo_years": 3,  "hi_years": 5,  "morlet_periods": (3, 5)},
    "juglar":      {"lo_years": 7,  "hi_years": 11, "morlet_periods": (7, 11)},
    "kuznets":     {"lo_years": 15, "hi_years": 25, "morlet_periods": (15, 25)},
    "kondratieff": {"lo_years": 40, "hi_years": 60, "morlet_periods": (40, 60)},
})

# Official World Bank aggregate codes for the 4 income classifications (2024-2025).
INCOME_GROUPS = ("HIC", "UMC", "LMC", "LIC")

# Group -> list of country codes. Singleton lists reuse the WB aggregate directly.
GROUPS = MappingProxyType({
    "WLD":   ["WLD"],
    "OECD":  ["OED"],
    "HIC":   ["HIC"],
    "UMC":   ["UMC"],
    "LMC":   ["LMC"],
    "LIC":   ["LIC"],
    "G7":    ["USA", "GBR", "FRA", "DEU", "ITA", "JPN", "CAN"],
    # BRICS+ as of January 2025: original 5 + Egypt, UAE, Ethiopia, Iran
    # (joined Jan 2024) + Indonesia (joined Jan 2025). Saudi Arabia was
    # invited but has not finalised membership; excluded.
    "BRICS": ["BRA", "RUS", "IND", "CHN", "ZAF",
              "EGY", "ARE", "ETH", "IRN", "IDN"],
    # G20 minus the EU bloc (avoid double-counting DEU/FRA/ITA already in
    # the country list). 19 countries.
    "G20": [
        "ARG", "AUS", "BRA", "CAN", "CHN", "FRA", "DEU", "IND", "IDN", "ITA",
        "JPN", "KOR", "MEX", "RUS", "SAU", "ZAF", "TUR", "GBR", "USA",
    ],
})

# Gate-2 / Gate-3 thresholds. Pre-registered.
MIN_METHOD_AGREEMENT = 3       # ≥ 3 of 4 methods must agree (Gate 2)
MIN_GROUP_CONCORDANCE = 4      # ≥ 4 of 5 income groups must concord (Gate 3)
N_INCOME_GROUPS = len(INCOME_GROUPS) + 1  # +1 for WLD as the reference
