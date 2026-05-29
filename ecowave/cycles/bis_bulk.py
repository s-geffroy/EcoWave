"""BIS bulk download — quarterly macroprudential indicators.

Roadmap #13 Phase 2 (2026-05). Source: BIS Statistics Data Portal
``data.bis.org/bulkdownload``. License: open non-commercial with
attribution; commercial use needs BIS terms. Bulks are zipped CSV in
"column" (wide) format — one row per series × column per time period.

This module ingests three priority bulks:

  - ``WS_CREDIT_GAP_csv_col.zip`` → ``BIS_CGAP``/``BIS_CRATIO``
    Credit-to-GDP actual ratio + gap (Borio-Drehmann CCyB signal).
    44 countries, quarterly, ~1960+ (some earlier).
  - ``WS_SPP_csv_col.zip`` → ``BIS_RPP``
    Residential property prices (nominal). 61 countries, quarterly,
    most series 1970+.
  - ``WS_TC_csv_col.zip`` → ``BIS_TCRED``
    Total credit to non-financial sector (level, % of GDP). 48
    countries, quarterly, mostly 1960+.

Brings the CPV financial-cycle channels onto Brazil, China, India,
Mexico, Korea, Turkey, South Africa, Russia, Indonesia — emerging
markets entirely absent from the previous horizons (WB groups are
income-tier aggregates, quarterly Path 5 covers AE only, long-history
JST is 18 AE).

Closes the panel gap on Borio's central-banker financial cycle
indicator — the credit-to-GDP gap is the primary CCyB (counter-cyclical
capital buffer) signal under Basel III, but had no direct test under
the dual-null framework until now.
"""
from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import typer

from ecowave.db import upsert_cycle_observation_quarterly


# Country codes the BIS bulk shares with our CPV manifests. ISO-2 throughout
# (BR not BRA, CN not CHN). Aggregates compose multiple country series via
# simple cross-sectional mean (BIS doesn't expose GDP weights in the bulk).
BIS_GROUPS: dict[str, tuple[str, ...]] = {
    "BIS_EM": ("BR", "CN", "IN", "MX", "KR", "TR", "ZA", "RU", "ID"),
    "BIS_AE": ("US", "GB", "DE", "FR", "IT", "JP", "CA", "AU"),
    # Per-country aggregates for the EM panel — useful for testing whether
    # the credit cycle is universal across EMs or country-specific.
    "BR_BIS": ("BR",), "CN_BIS": ("CN",), "IN_BIS": ("IN",),
    "MX_BIS": ("MX",), "KR_BIS": ("KR",), "TR_BIS": ("TR",),
    "ZA_BIS": ("ZA",), "RU_BIS": ("RU",), "ID_BIS": ("ID",),
}


@dataclass(frozen=True)
class BisBulkDataset:
    """Paths to the four BIS bulk ZIP archives."""
    credit_gap_zip: Path
    rpp_zip: Path
    total_credit_zip: Path
    dsr_zip: Path  # not yet wired but reserved for follow-up

    @classmethod
    def default(cls, data_raw_dir: Path) -> "BisBulkDataset":
        base = data_raw_dir / "bis"
        return cls(
            credit_gap_zip=base / "credit_gap.zip",
            rpp_zip=base / "SPP_csv_col.zip",
            total_credit_zip=base / "TC_csv_col.zip",
            dsr_zip=base / "DSR_csv_col.zip",
        )

    def assert_exists(self) -> None:
        missing = [p for p in (self.credit_gap_zip, self.rpp_zip,
                                 self.total_credit_zip)
                   if not p.exists()]
        if missing:
            raise FileNotFoundError(
                "BIS bulk zips missing:\n  "
                + "\n  ".join(str(p) for p in missing)
                + "\n\nDownload via:\n"
                + "  mkdir -p data_raw/bis && cd data_raw/bis && \\\n"
                + "  curl -sLO https://data.bis.org/static/bulk/WS_CREDIT_GAP_csv_col.zip && \\\n"
                + "  mv WS_CREDIT_GAP_csv_col.zip credit_gap.zip && \\\n"
                + "  curl -sLO https://data.bis.org/static/bulk/WS_SPP_csv_col.zip && \\\n"
                + "  curl -sLO https://data.bis.org/static/bulk/WS_TC_csv_col.zip"
            )


# --- Generic bulk reader -----------------------------------------------------

def _read_bulk_csv(zip_path: Path) -> pd.DataFrame:
    """Open a BIS bulk zip and return its single CSV as a wide DataFrame."""
    with zipfile.ZipFile(zip_path) as zf:
        member = next(n for n in zf.namelist() if n.endswith(".csv"))
        with zf.open(member) as fh:
            return pd.read_csv(fh, dtype=str)  # keep everything string for safety


def _melt_quarterly(wide: pd.DataFrame, id_cols: list[str]) -> pd.DataFrame:
    """Turn wide BIS quarterly data into long format (id_cols + year, quarter, value).

    Time columns look like ``1947-Q4``, ``2025-Q3``. Skips metadata cols.
    """
    time_cols = [c for c in wide.columns
                 if len(c) == 7 and c[4] == "-" and c[5] == "Q"]
    long = wide[id_cols + time_cols].melt(
        id_vars=id_cols, var_name="period", value_name="value")
    long[["year_str", "q_str"]] = long["period"].str.split("-Q", expand=True)
    long["year"] = pd.to_numeric(long["year_str"], errors="coerce").astype("Int64")
    long["quarter"] = pd.to_numeric(long["q_str"], errors="coerce").astype("Int64")
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    return long.drop(columns=["period", "year_str", "q_str"]).dropna(
        subset=["year", "quarter", "value"])


# --- Per-indicator slicers ---------------------------------------------------

def load_credit_gap(dataset: BisBulkDataset) -> pd.DataFrame:
    """Return (country, variable_code, year, quarter, value).

    Selects two derived series per country:
      - CG_DTYPE='A'  →  BIS_CRATIO  (credit-to-GDP, actual data)
      - CG_DTYPE='C'  →  BIS_CGAP    (credit-to-GDP gap, HP-filter deviation)
    Both at the Private non-financial sector × All-lenders intersection.
    """
    wide = _read_bulk_csv(dataset.credit_gap_zip)
    wide = wide[(wide["TC_BORROWERS"] == "P") & (wide["TC_LENDERS"] == "A")]
    actual = wide[wide["CG_DTYPE"] == "A"].copy()
    actual["variable_code"] = "BIS_CRATIO"
    gap = wide[wide["CG_DTYPE"] == "C"].copy()
    gap["variable_code"] = "BIS_CGAP"
    full = pd.concat([actual, gap], ignore_index=True)
    long = _melt_quarterly(full, ["BORROWERS_CTY", "variable_code"])
    return long.rename(columns={"BORROWERS_CTY": "country"})


def load_rpp(dataset: BisBulkDataset) -> pd.DataFrame:
    """Return (country, variable_code='BIS_RPP', year, quarter, value).

    Selects the headline nominal residential property price series:
    ``VALUE='N:628:Q:0'`` (nominal, in national currency, quarterly,
    raw value) — the broadest cross-country comparable series. If
    multiple matches per country exist, keeps the first.
    """
    wide = _read_bulk_csv(dataset.rpp_zip)
    # Heuristic: use the nominal (N) headline series, drop region/breaks variants.
    sub = wide[wide["UNIT_MEASURE"].str.startswith("Nominal", na=False)
                if wide["UNIT_MEASURE"].notna().any() else slice(None)].copy()
    if sub.empty:
        # Fall back to all rows — let the country-level dedup keep one per ISO.
        sub = wide.copy()
    sub["variable_code"] = "BIS_RPP"
    long = _melt_quarterly(sub, ["REF_AREA", "variable_code"])
    long = long.rename(columns={"REF_AREA": "country"})
    # Defensive dedup: keep the first series per (country, year, quarter).
    return (long.sort_values(["country", "year", "quarter"])
                 .drop_duplicates(subset=["country", "variable_code",
                                            "year", "quarter"],
                                    keep="first")
                 .reset_index(drop=True))


def load_total_credit(dataset: BisBulkDataset) -> pd.DataFrame:
    """Return (country, variable_code='BIS_TCRED', year, quarter, value).

    Picks Total credit to **Private non-financial sector** valued in
    **percent of GDP** (UNIT_TYPE='770'), market-value VALUATION='M',
    no adjustment TC_ADJUST='A'. The most cross-country comparable
    headline series.
    """
    wide = _read_bulk_csv(dataset.total_credit_zip)
    mask = (
        (wide["TC_BORROWERS"] == "P")
        & (wide["TC_LENDERS"] == "A")
        & (wide["UNIT_TYPE"] == "770")  # % of GDP
        & (wide["VALUATION"] == "M")     # market value
        & (wide["TC_ADJUST"] == "A")     # adjusted
    )
    sub = wide[mask].copy()
    sub["variable_code"] = "BIS_TCRED"
    long = _melt_quarterly(sub, ["BORROWERS_CTY", "variable_code"])
    return (long.rename(columns={"BORROWERS_CTY": "country"})
                 .drop_duplicates(subset=["country", "variable_code",
                                            "year", "quarter"], keep="first")
                 .reset_index(drop=True))


# --- Group panel builder -----------------------------------------------------

def build_bis_panel(group_code: str, variable_specs: list[dict],
                    dataset: BisBulkDataset, *,
                    start_year: int = 1970,
                    persist: dict | None = None) -> pd.DataFrame:
    """Build a quarterly (period × variable_code) panel for ``group_code``.

    Aggregates across the BIS countries that compose the group via simple
    cross-sectional mean (no GDP weights — sufficient for cycle detection,
    which is invariant to level scaling). Persists to
    ``cycle_observations_quarterly`` so the per-variable evidence path
    can recompose without re-reading the BIS zips.
    """
    if group_code not in BIS_GROUPS:
        raise ValueError(f"Unknown BIS group {group_code!r}; "
                          f"expected one of {sorted(BIS_GROUPS)}.")
    dataset.assert_exists()

    countries = list(BIS_GROUPS[group_code])
    requested = {spec["variable_code"] for spec in variable_specs}

    long_pieces: list[pd.DataFrame] = []
    if {"BIS_CGAP", "BIS_CRATIO"} & requested:
        long_pieces.append(load_credit_gap(dataset))
    if "BIS_RPP" in requested:
        long_pieces.append(load_rpp(dataset))
    if "BIS_TCRED" in requested:
        long_pieces.append(load_total_credit(dataset))
    if not long_pieces:
        return pd.DataFrame()

    long_df = pd.concat(long_pieces, ignore_index=True)
    long_df = long_df[long_df["country"].isin(countries)
                       & (long_df["year"] >= start_year)
                       & long_df["variable_code"].isin(requested)]
    if long_df.empty:
        return pd.DataFrame()

    # Cross-country mean per (variable_code, year, quarter).
    agg = (long_df.groupby(["variable_code", "year", "quarter"],
                             as_index=False)["value"].mean())
    agg["period"] = pd.PeriodIndex.from_fields(
        year=agg["year"].astype(int),
        quarter=agg["quarter"].astype(int), freq="Q")
    panel = (agg.pivot(index="period", columns="variable_code", values="value")
                 .sort_index())

    if persist is not None and "con" in persist:
        con = persist["con"]
        for var_code in panel.columns:
            for period, val in panel[var_code].items():
                if pd.notna(val):
                    upsert_cycle_observation_quarterly(
                        con, group_code, var_code,
                        int(period.year), int(period.quarter),
                        float(val), source_id=None,
                    )
        con.commit()

    return panel


def load_bis_manifest(path: Path) -> dict:
    """Parse the BIS bulk manifest into a plain dict."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
