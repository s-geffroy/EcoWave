"""Bank of England — A Millennium of Macroeconomic Data for the UK.

Roadmap #13 Phase 1 (2026-05). Source: BoE Working Paper 845 (Thomas &
Dimsdale, 2017), v3.1 data through 2016. License: UK Open Government
Licence v3.0 (open, attribution required). Ingested via the long-format
CSV mirror on `datahub.io/economic-history/millennium-macroeconomic-data-uk`
(the official BoE xlsx requires a browser User-Agent due to Cloudflare).

Coverage: UK 1700-2016 = 316 years (some series back to 1086/1209/1694
but pre-1700 is benchmark-interpolated and not continuous). This is the
single best dataset for testing the **Kondratieff cycle** statistically —
~5-8 K-waves fit in the 1700-2016 window, vs ~1.3 on the World Bank
panel and ~3 on Maddison/JST.

Single aggregate group: ``UK_BOE``. Variables are prefixed ``BOE_``
(BOE_GDP, BOE_CPI, BOE_STIR, BOE_YIELD, etc.) — defined in
``boe_millennium_manifest.json``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import typer

from ecowave.db import upsert_cycle_observation


# Hard-coded for now — single aggregate (UK). Could be extended to regional
# splits (England-only via the `composite-estimate-of-english-...` series)
# but the BoE dataset is UK-centric.
BOE_GROUPS: dict[str, tuple[str, ...]] = {
    "UK_BOE": ("GBR",),
}


@dataclass(frozen=True)
class BoeMillenniumDataset:
    """Path container for the BoE long-format annual CSV."""
    csv_path: Path

    @classmethod
    def default(cls, data_raw_dir: Path) -> "BoeMillenniumDataset":
        return cls(csv_path=data_raw_dir / "boe" / "annual.csv")

    def assert_exists(self) -> None:
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"BoE Millennium CSV not found at {self.csv_path}.\n"
                "Run inside the container:\n"
                "  mkdir -p data_raw/boe && curl -sL "
                "https://datahub.io/economic-history/millennium-macroeconomic-data-uk/_r/-/data/annual.csv "
                "-o data_raw/boe/annual.csv"
            )


def load_boe_long_format(path: Path) -> pd.DataFrame:
    """Return the BoE annual long-format DataFrame.

    Columns: ``year``, ``variable_id``, ``variable``, ``section``, ``unit``,
    ``value``. We coerce ``year`` to int and ``value`` to float (NaN-safe).
    """
    df = pd.read_csv(path)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["year", "variable_id"])
    df["year"] = df["year"].astype(int)
    return df


def build_boe_panel(group_code: str, variable_specs: list[dict],
                    dataset: BoeMillenniumDataset, *,
                    start_year: int = 1700,
                    persist: dict | None = None) -> pd.DataFrame:
    """Build a wide-format (year × variable_code) panel for one group.

    ``variable_specs`` is the manifest's ``variable_codes`` list — each
    item has ``variable_code`` (our internal slug) + ``boe_id`` (the source
    slug from the BoE CSV) + ``start_year`` (variable-specific lower bound
    that complements the manifest-level ``start_year``).

    Persists into ``cycle_observations`` so the per-variable evidence
    analysis (``evidence-per-variable``) can read it back without
    re-ingesting from the CSV.
    """
    if group_code not in BOE_GROUPS:
        raise ValueError(f"Unknown BoE group {group_code!r}; "
                          f"expected one of {sorted(BOE_GROUPS)}.")

    dataset.assert_exists()
    long_df = load_boe_long_format(dataset.csv_path)

    wide_cols: dict[str, pd.Series] = {}
    for spec in variable_specs:
        cpv_code = spec["variable_code"]
        boe_id = spec["boe_id"]
        var_start = max(start_year, int(spec.get("start_year") or start_year))
        sub = long_df[(long_df["variable_id"] == boe_id)
                       & (long_df["year"] >= var_start)]
        if sub.empty:
            continue
        # Defensive deduplication: BoE CSV has one row per (year, variable)
        # but a few rebased series ship duplicates.
        series = (sub.sort_values("year")
                     .drop_duplicates(subset=["year"], keep="last")
                     .set_index("year")["value"])
        wide_cols[cpv_code] = series

    if not wide_cols:
        return pd.DataFrame()

    panel = pd.DataFrame(wide_cols)
    panel.index.name = "year"
    panel = panel.sort_index()

    if persist is not None and "con" in persist:
        con = persist["con"]
        for cpv_code, ser in wide_cols.items():
            for year, val in ser.items():
                if pd.notna(val):
                    upsert_cycle_observation(
                        con, group_code, cpv_code, int(year),
                        float(val), source_id=None,
                    )
        con.commit()

    return panel


def load_boe_manifest(path: Path) -> dict:
    """Parse the BoE Millennium manifest into a plain dict."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
