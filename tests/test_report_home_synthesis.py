"""Home synthesis table + sidecar roundtrip + cross-horizon note rendering."""
from __future__ import annotations

import pandas as pd

from ecowave.cycles.report import (
    AGGREGATE_ROW_ORDER,
    CANONICAL_HOME_ROWS,
    build_position_table,
    positions_sidecar_path,
    read_positions_sidecar,
    render_cross_horizon_synthesis_md,
    render_home_aggregates_table,
    render_home_synthesis_table,
    write_positions_sidecar,
)


def _row(group_code: str, cycle: str, phase: str, *, trend: str = "—",
         next_kind: str | None = None, next_eta_years: float | None = None,
         endpoint_caveat: int = 0, separable: int = 1) -> dict:
    return {
        "group_code": group_code, "cycle": cycle, "phase": phase,
        "phi_rad": 0.1, "amplitude": 0.5, "ar1_p_value": 0.01,
        "separable": separable, "endpoint_caveat": endpoint_caveat,
        "trend": trend, "next_kind": next_kind,
        "next_eta_years": next_eta_years, "notes": "",
    }


def _three_horizon_fixtures() -> dict[str, pd.DataFrame]:
    wb = build_position_table([
        _row("WLD", "kitchin", "contraction", trend="falling",
             next_kind="min", next_eta_years=0.4, endpoint_caveat=1),
        _row("WLD", "kondratieff", "contraction", trend="rising",
             next_kind="max", next_eta_years=7.3, endpoint_caveat=1),
    ])
    q = build_position_table([])
    long = build_position_table([
        _row("G7", "juglar", "contraction", trend="falling",
             next_kind="max", next_eta_years=3.8, endpoint_caveat=1),
        _row("G7", "kuznets", "disputed", trend="rising",
             next_kind="max", next_eta_years=1.4, endpoint_caveat=1),
    ])
    return {"wb": wb, "q": q, "long": long}


def test_canonical_home_rows_cover_four_cycles():
    cycles = {cycle for cycle, *_ in CANONICAL_HOME_ROWS}
    assert cycles == {"kitchin", "juglar", "kuznets", "kondratieff"}


def test_home_synthesis_table_picks_canonical_rows_per_cycle():
    md = render_home_synthesis_table(_three_horizon_fixtures(), "2026-05")
    assert "Position actuelle des 4 cycles canoniques — 2026-05" in md
    # Kitchin + Kondratieff are anchored to the WB/WLD aggregate (Gate 1 survives
    # there at p ≤ 0.01); Juglar + Kuznets to the Long/G7 aggregate.
    assert "Kitchin ⚠️" in md and "`WLD`" in md
    assert "📉 min dans 5 mois" in md  # 0.4y → 5 mois
    assert "Juglar ⚠️" in md and "`G7`" in md
    assert "📈 max dans 3.8 ans" in md
    assert "Kuznets ⚠️" in md and "📈 max dans 1.4 ans" in md
    # Kondratieff WB WLD: max 7.3 ans (the post-WWII K-wave on the way up).
    assert "Kondratieff" in md and "📈 max dans 7.3 ans" in md
    # Endpoint caveat note appears because every WB/Long row triggered it.
    assert "effet endpoint CF" in md


def test_home_synthesis_handles_missing_horizon_gracefully():
    md = render_home_synthesis_table({}, "2026-05")
    assert "en attente" in md  # placeholder for unavailable sidecars


def test_sidecar_roundtrip_preserves_values(tmp_path):
    table = _three_horizon_fixtures()["wb"]
    sidecar = positions_sidecar_path(tmp_path, "2026-05", "wb")
    write_positions_sidecar(table, sidecar)
    assert sidecar.exists()
    rehydrated = read_positions_sidecar(sidecar)
    assert list(rehydrated["group_code"]) == list(table["group_code"])
    assert list(rehydrated["phase"]) == list(table["phase"])
    # Categorical cycle column survives serialization → string ordering preserved.
    assert list(map(str, rehydrated["cycle"])) == list(map(str, table["cycle"]))


def test_sidecar_handles_empty_table(tmp_path):
    sidecar = positions_sidecar_path(tmp_path, "2026-05", "q")
    write_positions_sidecar(build_position_table([]), sidecar)
    assert sidecar.read_text(encoding="utf-8") == "[]"
    assert read_positions_sidecar(sidecar).empty


def test_aggregate_row_order_covers_3_horizons():
    horizons = {h for h, _ in AGGREGATE_ROW_ORDER}
    assert horizons == {"wb", "q", "long"}
    assert len(AGGREGATE_ROW_ORDER) == 20  # 8 + 6 + 6
    # Canonical WB ordering pinned by the user.
    wb_order = [g for h, g in AGGREGATE_ROW_ORDER if h == "wb"]
    assert wb_order == ["WLD", "G7", "OECD", "BRICS",
                         "HIC", "UMC", "LMC", "LIC"]


def test_home_aggregates_table_renders_surviving_cells_and_emdashes():
    by_horizon = _three_horizon_fixtures()
    # Add a Long-G7 Juglar row that should appear in the dashboard.
    long = by_horizon["long"]
    by_horizon["long"] = build_position_table(
        long.to_dict(orient="records") + [
            _row("ANGLO", "juglar", "expansion", trend="rising",
                 next_kind="max", next_eta_years=1.5, endpoint_caveat=1),
        ]
    )
    md = render_home_aggregates_table(by_horizon, "2026-05")
    # Header has Agrégat + Source + 4 × 3 metric columns = 14.
    header = next(l for l in md.split("\n") if l.startswith("| Agrégat"))
    assert header.count("|") == 15  # 14 cols → 15 pipes including the outer ones
    # WB WLD: Kitchin + Kondratieff survive, Juglar + Kuznets are "—".
    wld_row = next(l for l in md.split("\n") if l.startswith("| `WLD` |"))
    assert "contraction ⚠️ | falling | 📉 min dans 5 mois" in wld_row
    assert "contraction ⚠️ | rising | 📈 max dans 7.3 ans" in wld_row
    # Long ANGLO Juglar survives.
    anglo_row = next(l for l in md.split("\n") if l.startswith("| `ANGLO` |"))
    assert "expansion ⚠️ | rising | 📈 max dans 1.5 ans" in anglo_row
    # WB UMC: no fixture data — every metric column should be em-dashes.
    umc_row = next(l for l in md.split("\n") if l.startswith("| `UMC` |"))
    assert umc_row.count("—") == 12  # 4 cycles × 3 metrics
    # Footer links use the default "reports/" prefix for home consumption.
    assert "[Banque mondiale](reports/cycle_position_2026_05_wb.md)" in md


def test_home_aggregates_table_link_prefix_override():
    md = render_home_aggregates_table({}, "2026-05", link_prefix="")
    assert "[Banque mondiale](cycle_position_2026_05_wb.md)" in md


def test_cross_horizon_synthesis_md_writes_signed_note(tmp_path):
    out = tmp_path / "synthesis.md"
    render_cross_horizon_synthesis_md(
        as_of="2026-05",
        by_horizon=_three_horizon_fixtures(),
        schema_version="0.5.0",
        out_path=out,
    )
    text = out.read_text(encoding="utf-8")
    assert "Synthèse multi-horizons — CPV 2026-05" in text
    assert "Schema EcoWave : `0.5.0`" in text
    # Each horizon's extended panel is rendered under its own header.
    assert "Banque mondiale (1960-2024)" in text
    assert "Trimestriel (Path 5" in text
    assert "Histoire longue (1870-2022)" in text
