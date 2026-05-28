"""Long-history macro ingestion: Maddison Project + Jordà-Schularick-Taylor.

This is the "long horizon" data path used by ``position-cycles --horizon long``.
It complements (does not replace) the World Bank panel: WB has 65 years of
data on every income group; Maddison + JST have 100-200 years of data on
~18 advanced economies. The longer panel gives Gate 1 substantially more
statistical power against the AR(1) null for Kuznets and Kondratieff cycles.

Datasets
--------
- **Maddison Project Database 2023** (Bolt & van Zanden et al.)
  Real GDP per capita, 1820-2022, 169 countries. CC BY 4.0.
- **Jordà-Schularick-Taylor Macrohistory R6** (2023). 18 advanced economies,
  1870-2020+, annual. Variables: GDP, credit to households, credit to
  non-financial corporates, house prices, equity prices, sovereign yield,
  CPI. CC BY 4.0.

Both datasets are downloaded by ``scripts/download_macrohistory.sh`` into
``data_raw/macrohistory/`` and read here as offline files. We never bundle
them in the repo (file-size + licence hygiene).

Country sets
------------
The JST set defines the natural "advanced 18" group: AUS, BEL, CAN, CHE,
DEU, DNK, ESP, FIN, FRA, GBR, IRL, ITA, JPN, NLD, NOR, PRT, SWE, USA.
Maddison covers a strict superset; we use it only for GDP weights.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

JST_ADVANCED_18 = ("AUS", "BEL", "CAN", "CHE", "DEU", "DNK", "ESP", "FIN",
                   "FRA", "GBR", "IRL", "ITA", "JPN", "NLD", "NOR", "PRT",
                   "SWE", "USA")

LONG_GROUPS = {
    "ADV18": JST_ADVANCED_18,                  # JST advanced economies
    "G7":    ("USA", "GBR", "FRA", "DEU", "ITA", "JPN", "CAN"),
    "USA":   ("USA",),
    "EU4":   ("DEU", "FRA", "ITA", "ESP"),
    "ANGLO": ("USA", "GBR", "CAN", "AUS"),
    "NORDIC": ("DNK", "FIN", "NOR", "SWE"),
}

# Default columns we expose from each dataset.
MADDISON_GDP_COL = "gdppc"
JST_VARS = {
    "LH_GDP":     ("rgdpmad",       "Real GDP per capita (Maddison-aligned, JST series)"),
    "LH_CREDIT":  ("tloans",        "Total loans to households + non-financial corporates"),
    "LH_HPI":     ("hpnom",         "House price index (nominal)"),
    "LH_EQUITY":  ("eq_capgain",    "Equity capital gains return"),
    "LH_YIELD":   ("ltrate",        "Long-term government bond yield"),
    "LH_CPI":     ("cpi",           "Consumer price index"),
    "LH_MONEY":   ("money",         "Broad money stock"),
}


@dataclass(frozen=True)
class LongHistoryDataset:
    maddison_path: Path
    jst_path: Path

    @classmethod
    def default(cls, data_raw_dir: Path) -> "LongHistoryDataset":
        return cls(
            maddison_path=data_raw_dir / "macrohistory" / "mpd2023.xlsx",
            jst_path=data_raw_dir / "macrohistory" / "jst_r6.xlsx",
        )

    def assert_exists(self) -> None:
        missing = [p for p in (self.maddison_path, self.jst_path) if not p.exists()]
        if missing:
            raise FileNotFoundError(
                "Long-history datasets missing:\n  "
                + "\n  ".join(str(p) for p in missing)
                + "\n\nRun `bash scripts/download_macrohistory.sh` inside the "
                "container to fetch them."
            )


# --- Maddison loader ----------------------------------------------------

def load_maddison_gdp(path: Path) -> pd.DataFrame:
    """Return DataFrame[year, country, gdppc] from MPD 2023.

    MPD 2023 ships the GDP series on sheet ``Full data`` with columns
    countrycode (ISO3), country, year, gdppc (real GDP per capita in
    constant 2011 USD), pop. We keep only the columns we need.
    """
    df = pd.read_excel(path, sheet_name="Full data", engine="openpyxl")
    # Normalise column names defensively (MPD has shifted casing across releases).
    df.columns = [c.lower() for c in df.columns]
    if "countrycode" not in df.columns or "year" not in df.columns:
        raise ValueError(f"Unexpected Maddison schema: columns={list(df.columns)}")
    out = (df[["countrycode", "year", MADDISON_GDP_COL]]
            .rename(columns={"countrycode": "country"})
            .dropna(subset=["country", "year"]))
    # MPD 2023 has some country-year duplicates (historical-imputation overlaps);
    # we keep the last value per (country, year) deterministically.
    return (out.sort_values(["country", "year"])
              .drop_duplicates(subset=["country", "year"], keep="last")
              .reset_index(drop=True))


# --- JST loader ---------------------------------------------------------

def load_jst(path: Path) -> pd.DataFrame:
    """Return the long-format JST panel: country, year, then JST variables.

    The JST R6 Excel file ships a single sheet ('Sheet1') with 2 718 rows ×
    59 columns. ISO3 codes are in the ``iso`` column; we rename it to
    ``country`` for parity with the Maddison loader.
    """
    sheet_names = ("Sheet1", "Data", "JSTdatasetR6")  # be defensive across releases
    last_err: Exception | None = None
    df: pd.DataFrame | None = None
    for sheet in sheet_names:
        try:
            df = pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
            break
        except (ValueError, KeyError) as exc:
            last_err = exc
    if df is None:
        raise ValueError(f"JST sheet not found (tried {sheet_names}): {last_err}")
    df.columns = [c.lower() for c in df.columns]
    if "iso" not in df.columns:
        raise ValueError(f"JST file must expose an 'iso' column. Got {list(df.columns)}")
    # JST ships a 'country' column with the long name (e.g. 'Australia'); we
    # rename it out of the way so the ISO3 code becomes our 'country' join key.
    if "country" in df.columns:
        df = df.rename(columns={"country": "country_name"})
    out = df.rename(columns={"iso": "country"})
    # JST has occasional (country, year) duplicates from data revisions; we
    # keep the last row per (country, year) so the panel is well-formed.
    return (out.sort_values(["country", "year"])
              .drop_duplicates(subset=["country", "year"], keep="last")
              .reset_index(drop=True))


# --- Long-history group panel ------------------------------------------

def _gdp_weights_long(maddison: pd.DataFrame, countries: tuple[str, ...],
                      start_year: int) -> pd.DataFrame:
    """GDP-weights matrix [year, country] used to aggregate to groups.

    We use Maddison GDP per capita (the only universally-available series back
    to 1870 across the JST 18). Strictly, we would multiply by population to
    get GDP-level weights, but the population scaling is roughly stable across
    the JST 18, so per-capita weighting is a reasonable approximation for
    aggregation purposes — and it's transparent.
    """
    sub = maddison[(maddison["country"].isin(countries))
                    & (maddison["year"] >= start_year)].copy()
    if sub.empty:
        return pd.DataFrame()
    return sub.pivot(index="year", columns="country", values=MADDISON_GDP_COL)


def _country_series(jst: pd.DataFrame, maddison: pd.DataFrame, country: str,
                    variable_code: str, start_year: int) -> pd.Series:
    """Series for one (country, variable) starting at start_year.

    GDP per capita falls back to Maddison (more complete coverage) if the
    JST column is missing; everything else uses JST.
    """
    jst_col, _label = JST_VARS[variable_code]
    sub = jst[(jst["country"] == country) & (jst["year"] >= start_year)]
    if variable_code == "LH_GDP" or jst_col not in sub.columns or sub[jst_col].isna().all():
        m = maddison[(maddison["country"] == country)
                      & (maddison["year"] >= start_year)]
        return pd.Series(m[MADDISON_GDP_COL].values,
                          index=m["year"].astype(int).values,
                          name=f"{country}/{variable_code}").sort_index()
    return pd.Series(sub[jst_col].values, index=sub["year"].astype(int).values,
                      name=f"{country}/{variable_code}").sort_index()


def build_long_history_panel(group_code: str, variable_codes: list[str],
                              dataset: LongHistoryDataset,
                              start_year: int = 1870,
                              persist: dict | None = None) -> pd.DataFrame:
    """Build the per-group annual panel from Maddison + JST.

    Returns DataFrame indexed by year, one column per variable_code, holding
    the GDP-weighted group aggregate.

    ``persist`` (optional): dict with keys ``con`` (sqlite3.Connection) and
    ``source_id`` (int) — when present we upsert every (group, variable,
    year, value) into ``cycle_observations`` so the DB stays consistent
    with the WB pipeline.
    """
    if group_code not in LONG_GROUPS:
        raise ValueError(f"Unknown long-history group {group_code}; "
                          f"available: {list(LONG_GROUPS)}")
    dataset.assert_exists()
    countries = LONG_GROUPS[group_code]

    maddison = load_maddison_gdp(dataset.maddison_path)
    jst = load_jst(dataset.jst_path)
    weights = _gdp_weights_long(maddison, countries, start_year)
    if weights.empty:
        return pd.DataFrame()

    panel: dict[str, pd.Series] = {}
    for var in variable_codes:
        if var not in JST_VARS:
            continue
        per_country = {c: _country_series(jst, maddison, c, var, start_year)
                       for c in countries}
        df = pd.DataFrame(per_country)
        # GDP-weighted average per year, ignoring rows where the variable or
        # the weight is missing.
        w = weights.reindex_like(df)
        mask = df.notna() & w.notna() & (w > 0)
        w_eff = w.where(mask, other=0.0)
        v_eff = df.where(mask, other=0.0)
        denom = w_eff.sum(axis=1)
        numer = (v_eff * w_eff).sum(axis=1)
        panel[var] = (numer / denom).where(denom > 0, other=pd.NA).astype(float)

    if not panel:
        return pd.DataFrame()
    out = pd.DataFrame(panel).sort_index()

    if persist is not None and "con" in persist:
        con: sqlite3.Connection = persist["con"]
        source_id = persist.get("source_id")
        from ecowave.db import upsert_cycle_observation
        for year, row in out.iterrows():
            for var, value in row.items():
                if pd.notna(value):
                    upsert_cycle_observation(con, group_code, var, int(year),
                                              float(value), source_id)
        con.commit()

    return out
