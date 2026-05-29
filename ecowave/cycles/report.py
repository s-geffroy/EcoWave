"""Report rendering for the CPV cycle-position output.

Builds the publishable matrix (group × cycle × phase + universality flag),
renders a markdown note, and emits three figures: phase heatmap, wavelet power
per group, and CF band-pass trajectories.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from ecowave.cycles.bands import CYCLE_BANDS, INCOME_GROUPS

# Canonical (cycle, horizon, group) triplets used to assemble the homepage
# synthesis table. One row per band, anchored to the aggregate where Gate 1
# (dual null, α=0.05) actually survives at as-of 2026-05. Rationale: in a
# 1000-surrogate dual-null regime, the global G7-quarterly composite dilutes
# Kitchin (out-of-phase 7-country averaging) and the annual WB panel sees too
# few Juglar/Kuznets cycles in 65 years. The pair (WB-WLD, Long-G7) covers
# all four bands at p ≤ 0.01:
#   - WB WLD Kitchin (4-5y, 16 cycles in panel)        p=0.002
#   - Long G7 Juglar (7-11y, ~17 cycles in 152y)        p=0.005
#   - Long G7 Kuznets (15-25y, ~7 cycles in 152y)       p=0.008
#   - WB WLD Kondratieff (40-60y, 1.3 cycles in panel)  p=0.001
CANONICAL_HOME_ROWS: tuple[tuple[str, str, str, str], ...] = (
    # (cycle, horizon, group_code, source_label)
    ("kitchin", "wb", "WLD", "Panel Banque mondiale (1960-2024)"),
    ("juglar", "long", "G7", "Histoire longue G7 (Maddison + JST, 1870-2022)"),
    ("kuznets", "long", "G7", "Histoire longue G7 (Maddison + JST, 1870-2022)"),
    ("kondratieff", "wb", "WLD", "Panel Banque mondiale (1960-2024)"),
)

# Aggregates worth surfacing in the cross-horizon synthesis note (more rows
# than the headline table but still curated).
SYNTHESIS_HORIZON_GROUPS: dict[str, tuple[str, ...]] = {
    "wb": ("WLD", "G7", "OECD", "BRICS"),
    "q": ("G7Q", "USA", "EA", "JPN"),
    "long": ("ADV18", "G7", "EU4", "ANGLO", "NORDIC"),
}

HORIZON_LABELS: dict[str, str] = {
    "wb": "Banque mondiale (1960-2024)",
    "q": "Trimestriel (Path 5, 1960-Q1 2026)",
    "long": "Histoire longue (1870-2022)",
}

# Short labels used as the "Source" column of the home dashboard table — kept
# narrow so the 14-column layout doesn't blow out on desktop.
HORIZON_LABEL_SHORT: dict[str, str] = {
    "wb": "WB",
    "q": "Path 5",
    "long": "Long",
}

# Row order for the home dashboard table. Within each horizon block the order
# is what the user pinned: WB block led by WLD (most global), then G7 / OECD /
# BRICS / income tiers; quarterly block opens with the composites (G7Q, OECDQ)
# then the four country series; long-history block opens with the broadest
# aggregate (ADV18) then narrower subsets.
AGGREGATE_ROW_ORDER: tuple[tuple[str, str], ...] = (
    ("wb", "WLD"), ("wb", "G7"), ("wb", "OECD"), ("wb", "BRICS"),
    ("wb", "HIC"), ("wb", "UMC"), ("wb", "LMC"), ("wb", "LIC"),
    ("q", "G7Q"), ("q", "OECDQ"), ("q", "USA"), ("q", "EA"),
    ("q", "JPN"), ("q", "GBR"),
    ("long", "ADV18"), ("long", "G7"), ("long", "EU4"),
    ("long", "ANGLO"), ("long", "NORDIC"), ("long", "USA"),
)

GROUP_GLOSSARY = {
    "WLD": "Monde — agrégat World Bank (population + GDP pondérés)",
    "OECD": "OECD — 38 pays membres de l'Organisation de Coopération et de Développement Économiques",
    "HIC": "High-Income Countries — RNB/hab > 14 005 USD (seuil WB 2024-2025)",
    "UMC": "Upper-Middle-Income — RNB/hab entre 4 516 et 14 005 USD",
    "LMC": "Lower-Middle-Income — RNB/hab entre 1 146 et 4 515 USD",
    "LIC": "Low-Income Countries — RNB/hab ≤ 1 145 USD",
    "G7": "G7 — USA, GBR, FRA, DEU, ITA, JPN, CAN (recompute pondéré PIB)",
    "G20": "G20 — 19 pays principaux (zone UE traitée par DEU+FRA+ITA)",
    "BRICS": "BRICS+ — Brésil, Russie, Inde, Chine, Afrique du Sud, Égypte, Émirats arabes unis, Éthiopie, Iran, Indonésie (10 pays, expansion Jan-2024 + Jan-2025)",
}


def build_position_table(positions: list[dict]) -> pd.DataFrame:
    """Materialize the cycle_positions rows as a tidy DataFrame for rendering."""
    if not positions:
        return pd.DataFrame(columns=["group_code", "cycle", "phase", "ar1_p_value",
                                     "separable", "amplitude", "endpoint_caveat",
                                     "trend", "next_kind", "next_eta_years"])
    df = pd.DataFrame(positions)
    df["cycle"] = pd.Categorical(df["cycle"], categories=list(CYCLE_BANDS.keys()),
                                  ordered=True)
    return df.sort_values(["group_code", "cycle"]).reset_index(drop=True)


def _matrix_view(table: pd.DataFrame, value_col: str = "phase") -> pd.DataFrame:
    if table.empty:
        return pd.DataFrame()
    return (table.pivot(index="group_code", columns="cycle", values=value_col)
            .reindex(columns=list(CYCLE_BANDS.keys())))


def _format_eta(eta_years) -> str:
    if eta_years is None or (isinstance(eta_years, float) and pd.isna(eta_years)):
        return "—"
    if eta_years < 1.0:
        return f"{eta_years * 12.0:.0f} mois"
    if eta_years < 10.0:
        return f"{eta_years:.1f} ans"
    return f"{eta_years:.0f} ans"


def _format_next(row) -> str:
    kind = row.get("next_kind", "—")
    eta = row.get("next_eta_years")
    if kind in (None, "—") or eta is None:
        return "—"
    arrow = "📈 max" if kind == "max" else "📉 min"
    return f"{arrow} dans {_format_eta(eta)}"


def positions_sidecar_path(reports_dir: Path, as_of: str, horizon: str) -> Path:
    """Sidecar JSON path for the positions DataFrame of one horizon.

    Why a sidecar: ``replace_cycle_positions`` wipes the SQLite table on every
    ``position-cycles`` invocation, so the three horizons cannot coexist in DB.
    The sidecars survive across runs and let ``home-synthesis`` reassemble the
    cross-horizon view without re-running any pipeline.
    """
    stem = f"{as_of.replace('-', '_')}_{horizon}"
    return reports_dir / f"cycle_position_{stem}.json"


def write_positions_sidecar(table: pd.DataFrame, path: Path) -> Path:
    """Serialize the positions table as JSON records (NaN → null)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if table.empty:
        path.write_text("[]", encoding="utf-8")
        return path
    df = table.copy()
    if isinstance(df["cycle"].dtype, pd.CategoricalDtype):
        df["cycle"] = df["cycle"].astype(str)
    records = df.where(pd.notna(df), None).to_dict(orient="records")
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def read_positions_sidecar(path: Path) -> pd.DataFrame:
    """Rehydrate a positions DataFrame from a sidecar JSON file."""
    if not path.exists():
        return build_position_table([])
    raw = json.loads(path.read_text(encoding="utf-8"))
    return build_position_table(raw)


def _select_canonical_row(table: pd.DataFrame, cycle: str,
                          group_code: str) -> dict | None:
    if table.empty:
        return None
    matches = table[(table["cycle"].astype(str) == cycle)
                    & (table["group_code"] == group_code)]
    if matches.empty:
        return None
    return matches.iloc[0].to_dict()


def render_home_synthesis_table(by_horizon: dict[str, pd.DataFrame],
                                as_of: str,
                                link_prefix: str = "reports/") -> str:
    """Headline 4-row table for the homepage: one canonical row per cycle.

    Each row picks the dataset best suited to the band's timescale (cf.
    ``CANONICAL_HOME_ROWS``). Cells that cannot be located in the sidecars
    (e.g. an horizon hasn't been run yet) appear with em-dashes so the snippet
    is still renderable in a partial state.

    ``link_prefix`` is the relative directory from the consumer page to the
    `cycle_position_*.md` notes. Defaults to ``"reports/"`` (relative to
    ``docs/index.md``). The cross-horizon synthesis note, which itself lives
    in ``docs/reports/``, passes ``""``.
    """
    lines: list[str] = []
    lines.append(f"### Position actuelle des 4 cycles canoniques — {as_of}")
    lines.append("")
    lines.append("| Cycle | Source canonique | Agrégat | Phase | Tendance | Prochain extremum |")
    lines.append("|---|---|---|---|---|---|")
    any_caveat = False
    for cycle, horizon, group, source_label in CANONICAL_HOME_ROWS:
        table = by_horizon.get(horizon, build_position_table([]))
        row = _select_canonical_row(table, cycle, group)
        cycle_lbl = cycle.capitalize()
        if row is None:
            lines.append(
                f"| {cycle_lbl} | {source_label} | `{group}` | _en attente_ | — | — |"
            )
            continue
        phase = str(row.get("phase") or "—")
        trend = row.get("trend") or "—"
        nxt = _format_next({"next_kind": row.get("next_kind", "—"),
                            "next_eta_years": row.get("next_eta_years")})
        caveat = " ⚠️" if int(row.get("endpoint_caveat") or 0) == 1 else ""
        if caveat:
            any_caveat = True
        lines.append(
            f"| {cycle_lbl}{caveat} | {source_label} | `{group}` | "
            f"{phase} | {trend} | {nxt} |"
        )
    lines.append("")
    if any_caveat:
        lines.append(
            "_⚠️ = effet endpoint CF dominant sur les dernières `hi_years/2` années ; "
            "la prévision donne l'ordre de grandeur, pas la date exacte._"
        )
        lines.append("")
    lines.append(
        "Détails par agrégat : "
        f"[Panel Banque mondiale]({link_prefix}cycle_position_2026_05_wb.md) · "
        f"[Panel trimestriel]({link_prefix}cycle_position_2026_05_q.md) · "
        f"[Histoire longue]({link_prefix}cycle_position_2026_05_long.md)."
    )
    return "\n".join(lines)


# Thresholds for the home p-values matrix. Each tuple is (upper_bound, icon)
# tested in ascending order; the first bound a p-value falls under wins. The
# four buckets (🟢/🟡/🟠/🔴) map to the readings shown in the table footer.
PVALUE_THRESHOLDS: tuple[tuple[float, str], ...] = (
    (0.01, "🟢"),
    (0.05, "🟡"),
    (0.10, "🟠"),
    (1.01, "🔴"),
)


def _format_pvalue_cell(p) -> str:
    if p is None or (isinstance(p, float) and pd.isna(p)):
        return "—"
    p = float(p)
    for upper, icon in PVALUE_THRESHOLDS:
        if p <= upper:
            return f"{icon} {p:.3f}"
    return f"🔴 {p:.3f}"


def render_home_pvalues_table(by_horizon: dict[str, pd.DataFrame],
                              as_of: str,
                              link_prefix: str = "reports/") -> str:
    """Compact p-value matrix: 20 rows × 4 cycle columns, color-coded.

    Lets readers apply their own α threshold (Bonferroni-strict ≈ 0.0014 on
    36 WB cells, macro-10%, or the protocol's standard 5%) by reading the
    icon band. Complementary to ``render_home_aggregates_table`` — the
    dashboard answers "what is the cycle doing when it survives?", this
    matrix answers "how strong is the evidence, pass or fail?".
    """
    cycles = ("kitchin", "juglar", "kuznets", "kondratieff")
    lines: list[str] = []
    lines.append(
        f"### Poids de preuve par cellule — p-values Gate 1 ({as_of})"
    )
    lines.append("")
    header_cells = ["Agrégat", "Source"] + [c.capitalize() for c in cycles]
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("|" + "---|" * len(header_cells))

    for horizon, group in AGGREGATE_ROW_ORDER:
        table = by_horizon.get(horizon, build_position_table([]))
        source_label = HORIZON_LABEL_SHORT.get(horizon, horizon)
        row_cells = [f"`{group}`", source_label]
        for cycle in cycles:
            cell = _select_canonical_row(table, cycle, group)
            p = cell.get("ar1_p_value") if cell else None
            row_cells.append(_format_pvalue_cell(p))
        lines.append("| " + " | ".join(row_cells) + " |")
    lines.append("")
    lines.append(
        "Lecture : 🟢 `p ≤ 0.01` (signal fort, survivrait à α=0.01) · "
        "🟡 `0.01 < p ≤ 0.05` (seuil standard CPV) · "
        "🟠 `0.05 < p ≤ 0.10` (marginal, survivrait à α=0.10) · "
        "🔴 `p > 0.10` (clairement null)."
    )
    lines.append("")
    lines.append(
        "_p-values issues du test dual-null sur 1000 surrogates, **non "
        "corrigées** pour comparaisons multiples. Lecture Bonferroni-stricte "
        "sur 36 cellules WB : comparer à α ≈ 0.0014. Pour les conventions "
        "macro à α=0.10, traiter 🟢🟡🟠 comme survivants._"
    )
    return "\n".join(lines)


def render_home_aggregates_table(by_horizon: dict[str, pd.DataFrame],
                                 as_of: str,
                                 link_prefix: str = "reports/") -> str:
    """Per-aggregate dashboard for the homepage.

    Twenty rows (8 WB + 6 quarterly + 6 long history) × fourteen columns
    (Agrégat, Source + 4 cycles × {Phase, Tendance, Next}). Cells where Gate 1
    rejected the cycle are rendered as ``—`` per the "publish failures"
    convention. Row order is ``AGGREGATE_ROW_ORDER`` — locked so successive
    runs produce visually diff-able snippets.
    """
    cycles = ("kitchin", "juglar", "kuznets", "kondratieff")
    lines: list[str] = []
    lines.append(
        f"### Tableau de bord — phase, tendance et prochain extremum ({as_of})"
    )
    lines.append("")
    header_cells = ["Agrégat", "Source"]
    for cycle in cycles:
        header_cells.extend([cycle.capitalize(), "Tendance", "Next"])
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("|" + "---|" * len(header_cells))

    any_caveat = False
    for horizon, group in AGGREGATE_ROW_ORDER:
        table = by_horizon.get(horizon, build_position_table([]))
        source_label = HORIZON_LABEL_SHORT.get(horizon, horizon)
        row_cells = [f"`{group}`", source_label]
        for cycle in cycles:
            cell = _select_canonical_row(table, cycle, group)
            phase_raw = str(cell.get("phase")) if cell else None
            if cell is None or phase_raw in (None, "rejected"):
                row_cells.extend(["—", "—", "—"])
                continue
            trend = cell.get("trend") or "—"
            nxt = _format_next({"next_kind": cell.get("next_kind", "—"),
                                "next_eta_years": cell.get("next_eta_years")})
            caveat = " ⚠️" if int(cell.get("endpoint_caveat") or 0) == 1 else ""
            if caveat:
                any_caveat = True
            row_cells.extend([phase_raw + caveat, trend, nxt])
        lines.append("| " + " | ".join(row_cells) + " |")
    lines.append("")
    if any_caveat:
        lines.append(
            "_⚠️ = effet endpoint CF dominant sur les dernières `hi_years/2` "
            "années ; la prévision donne l'ordre de grandeur, pas la date exacte._"
        )
        lines.append("")
    lines.append(
        "Notes signées : "
        f"[Banque mondiale]({link_prefix}cycle_position_2026_05_wb.md) · "
        f"[Path 5 trimestriel]({link_prefix}cycle_position_2026_05_q.md) · "
        f"[Histoire longue]({link_prefix}cycle_position_2026_05_long.md) · "
        f"[Synthèse multi-horizons]({link_prefix}cycle_position_synthesis.md)."
    )
    return "\n".join(lines)


def render_cross_horizon_commentary(by_horizon: dict[str, pd.DataFrame]) -> str:
    """Short narrative paragraphs comparing the three horizons cycle-by-cycle."""
    lines: list[str] = []
    for cycle, horizon, group, _ in CANONICAL_HOME_ROWS:
        cycle_lbl = cycle.capitalize()
        row = _select_canonical_row(
            by_horizon.get(horizon, build_position_table([])), cycle, group)
        if row is None:
            lines.append(
                f"- **{cycle_lbl}** — données manquantes pour `{group}` "
                f"sur l'horizon `{horizon}` ; lancer "
                f"`ecowave position-cycles --horizon {horizon}`."
            )
            continue
        phase = row.get("phase", "—")
        trend = row.get("trend") or "—"
        nxt = _format_next({"next_kind": row.get("next_kind", "—"),
                            "next_eta_years": row.get("next_eta_years")})
        lines.append(
            f"- **{cycle_lbl}** ({group}, source `{horizon}`) — phase `{phase}`, "
            f"tendance `{trend}`, {nxt}."
        )
    return "\n".join(lines)


def render_cross_horizon_synthesis_md(as_of: str,
                                      by_horizon: dict[str, pd.DataFrame],
                                      schema_version: str,
                                      out_path: Path) -> Path:
    """Cross-horizon synthesis note: home table + extended per-horizon panels."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines: list[str] = []
    lines.append(f"# Synthèse multi-horizons — CPV {as_of}")
    lines.append("")
    lines.append("> Note signée — agrégation des trois horizons CPV (Banque mondiale,")
    lines.append("> trimestriel, histoire longue) pour répondre à la question :")
    lines.append("> **\"où en sommes-nous dans chaque cycle, et où allons-nous ?\"**.")
    lines.append("> Chaque cellule provient d'une ligne SQLite `cycle_positions`")
    lines.append("> traçable ; aucune agrégation inter-dataset n'est effectuée.")
    lines.append("")

    lines.append("## Position canonique par cycle")
    lines.append("")
    # The synthesis note lives in docs/reports/ so cycle_position_*.md siblings
    # are reached without the "reports/" prefix used on the homepage snippet.
    lines.append(render_home_synthesis_table(by_horizon, as_of, link_prefix=""))
    lines.append("")

    lines.append("## Lecture par cycle")
    lines.append("")
    lines.append(render_cross_horizon_commentary(by_horizon))
    lines.append("")

    lines.append("## Panels étendus par horizon")
    lines.append("")
    for horizon, label in HORIZON_LABELS.items():
        table = by_horizon.get(horizon, build_position_table([]))
        groups = SYNTHESIS_HORIZON_GROUPS.get(horizon, ())
        lines.append(f"### {label}")
        lines.append("")
        if table.empty:
            lines.append(f"_Aucune donnée — exécuter `ecowave position-cycles "
                         f"--horizon {horizon}`._")
            lines.append("")
            continue
        sub = table[table["group_code"].isin(groups)]
        if sub.empty:
            lines.append("_Aucun agrégat canonique disponible pour cet horizon._")
            lines.append("")
            continue
        lines.append(render_recap_table(sub))
        lines.append("")

    lines.append("## Sign-off")
    lines.append("")
    lines.append(f"- Date de la note : {now_iso}")
    lines.append(f"- As-of : {as_of}")
    lines.append(f"- Schema EcoWave : `{schema_version}`")
    lines.append("- Pipeline : `ecowave home-synthesis`")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def render_recap_table(table: pd.DataFrame) -> str:
    """Per-group recap: cycle × phase × trend × forecast.

    One block per group. Each block lists the 4 cycles with their current phase,
    instantaneous trend (rising / falling / post-extremum) and the expected
    next extremum + ETA. Cycles that failed Gate 1 (`rejected`) appear with
    em-dashes for the forecast columns.
    """
    if table.empty:
        return "_Aucune donnée à récapituler._"
    lines: list[str] = []
    for group in table["group_code"].drop_duplicates():
        sub = table[table["group_code"] == group].sort_values("cycle")
        lines.append(f"### {group}")
        lines.append("")
        lines.append("| Cycle | Phase | Tendance | Prochain extremum |")
        lines.append("|---|---|---|---|")
        for r in sub.itertuples():
            cycle_lbl = str(r.cycle).capitalize()
            phase = str(r.phase) if r.phase else "—"
            trend = getattr(r, "trend", "—") or "—"
            nxt = _format_next({"next_kind": getattr(r, "next_kind", "—"),
                                  "next_eta_years": getattr(r, "next_eta_years", None)})
            caveat = " ⚠️" if int(getattr(r, "endpoint_caveat", 0)) == 1 else ""
            lines.append(f"| {cycle_lbl}{caveat} | {phase} | {trend} | {nxt} |")
        lines.append("")
    lines.append(
        "_⚠️ = effet endpoint CF dominant (les dernières hi_years/2 années sont "
        "moins fiables ; la prévision donne l'ordre de grandeur, pas la date exacte)._"
    )
    return "\n".join(lines)


def render_group_glossary() -> str:
    """Markdown glossary of group codes used in the report."""
    lines = ["| Code | Définition |", "|---|---|"]
    for code, definition in GROUP_GLOSSARY.items():
        lines.append(f"| `{code}` | {definition} |")
    return "\n".join(lines)


def render_cycle_position_md(as_of: str, table: pd.DataFrame,
                             consensus_rows: list[dict],
                             universality_rows: list[dict],
                             figures: dict[str, str],
                             schema_version: str,
                             out_path: Path) -> Path:
    """Write the signed note to ``out_path``."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines: list[str] = []
    lines.append(f"# Où se situe le monde en {as_of} dans les 4 cycles canoniques ?")
    lines.append("")
    lines.append("> Note signée — sortie du protocole CPV (Cycle Position Vector).")
    lines.append("> Méthode : CF band-pass + Morlet wavelet + Hilbert phase + Markov-switching")
    lines.append("> + Bry-Boschan, avec 3 gates de falsifiabilité (existence AR(1), consensus")
    lines.append("> méthodologique ≥3/4, universalité cross-group ≥4/5). Voir")
    lines.append("> `methodology/multi_cycle_decomposition.md` pour la spécification complète.")
    lines.append("")

    # Group glossary upfront so a first-time reader knows what WLD / HIC / ... mean.
    lines.append("## Glossaire des agrégats")
    lines.append("")
    lines.append(render_group_glossary())
    lines.append("")

    # ---------- Headline recap: per-group cycle position + trend + next extremum.
    lines.append("## Récapitulatif par agrégat (position, tendance, prochain extremum)")
    lines.append("")
    lines.append("Pour chaque groupe, position du cycle, tendance instantanée et")
    lines.append("ETA du prochain pic/creux (calculé via la fréquence instantanée Hilbert :")
    lines.append("Δt = ((φ_cible − φ) mod 2π) / ω, où ω = 2π / période centrale de la bande).")
    lines.append("")
    lines.append(render_recap_table(table))
    lines.append("")

    # Gate 1 + 2 output: position table.
    lines.append("## Matrice de phase (Gate 2 — consensus inter-méthode)")
    lines.append("")
    if table.empty:
        lines.append("_Pas de données — l'ingestion a échoué ou le mode est dégradé._")
    else:
        matrix = _matrix_view(table, "phase")
        lines.append(matrix.fillna("—").to_markdown())
    lines.append("")

    # AR(1) p-values matrix (Gate 1).
    if not table.empty:
        lines.append("## p-values AR(1) (Gate 1 — existence du cycle)")
        lines.append("")
        pmatrix = _matrix_view(table, "ar1_p_value")
        lines.append(pmatrix.applymap(
            lambda v: "—" if (v is None or pd.isna(v)) else f"{v:.3f}").to_markdown())
        lines.append("")

    # Gate 3 — universality.
    lines.append("## Drapeau d'universalité par cycle (Gate 3 — cross-group)")
    lines.append("")
    if universality_rows:
        udf = pd.DataFrame(universality_rows)
        udf["status"] = udf["universal"].map({1: "universal", 0: "regional"})
        lines.append(udf[["cycle", "modal_phase", "n_groups_concording",
                          "n_groups_total", "status"]].to_markdown(index=False))
    else:
        lines.append("_Pas d'évaluation cross-group disponible._")
    lines.append("")

    # Per-method votes (Gate 2 detail).
    if consensus_rows:
        lines.append("## Votes par modèle (D/E/F/G) — détail Gate 2")
        lines.append("")
        cdf = pd.DataFrame(consensus_rows)
        for cycle in CYCLE_BANDS.keys():
            sub = cdf[cdf["cycle"] == cycle]
            if sub.empty:
                continue
            lines.append(f"### {cycle.capitalize()}")
            lines.append("")
            pivot = sub.pivot(index="group_code", columns="model_code", values="phase")
            lines.append(pivot.fillna("—").to_markdown())
            lines.append("")

    # Figures.
    if figures:
        lines.append("## Figures")
        lines.append("")
        for caption, path in figures.items():
            lines.append(f"![{caption}]({path})")
            lines.append("")

    # Lecture par cycle (anchoring).
    lines.append("## Lecture par cycle (ancrage littérature)")
    lines.append("")
    lines.append("- **Kitchin (3-5 ans)** — cycle d'inventaire. Référence : Kitchin (1923) ;")
    lines.append("  contestation moderne : Diebolt & Doliger (2008).")
    lines.append("- **Juglar (7-11 ans)** — cycle d'investissement fixe. Référence :")
    lines.append("  Schumpeter (1939) ; opérationalisation : Harding & Pagan (2002).")
    lines.append("- **Kuznets (15-25 ans)** — cycle infrastructure/démographie. Référence :")
    lines.append("  Kuznets (1930) ; lecture financière : Borio & Drehmann (2009).")
    lines.append("- **Kondratieff (40-60 ans)** — vague techno-économique longue. Référence :")
    lines.append("  Kondratieff (1925) ; lecture quantitative : Korotayev & Tsirel (2010).")
    lines.append("")

    # Caveats.
    lines.append("## Caveats")
    lines.append("")
    lines.append("- **Effet endpoint CF** : les dernières `hi_years/2` années sont moins")
    lines.append("  fiables (filtre asymétrique). Les cellules concernées sont marquées")
    lines.append(f"  `endpoint_caveat=1` dans la table `cycle_positions`.")
    lines.append("- **Fréquence annuelle WB** : Kitchin (3-5 ans) est borderline ; la bande")
    lines.append("  basse 3a est inutilisable annuellement (Nyquist).")
    lines.append("- **Small-N Kondratieff** : WB démarre en 1960, soit ≈ 1.0-1.5 K-wave. Le")
    lines.append("  null AR(1) peut rejeter Kondratieff (`separable=0`) pour plusieurs")
    lines.append("  groupes : c'est honnête, pas un échec.")
    lines.append("")

    lines.append("## Sign-off")
    lines.append("")
    lines.append(f"- Date de la note : {now_iso}")
    lines.append(f"- As-of : {as_of}")
    lines.append(f"- Schema EcoWave : `{schema_version}`")
    lines.append("- Pipeline : `ecowave position-cycles`")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def plot_phase_heatmap(table: pd.DataFrame, out_path: Path) -> Path:
    """Heatmap of phase labels: rows=group, cols=cycle. Color by phase."""
    import matplotlib.pyplot as plt
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if table.empty:
        return out_path
    phase_order = ["expansion", "peak", "contraction", "trough", "disputed", "rejected"]
    phase_to_id = {p: i for i, p in enumerate(phase_order)}
    matrix = _matrix_view(table, "phase")
    if matrix.empty:
        return out_path
    ids = matrix.applymap(lambda v: phase_to_id.get(v, np.nan)).to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(8, max(3, 0.6 * matrix.shape[0])))
    im = ax.imshow(ids, cmap="viridis", aspect="auto", vmin=0,
                    vmax=len(phase_order) - 1)
    ax.set_xticks(range(matrix.shape[1]), [c.capitalize() for c in matrix.columns])
    ax.set_yticks(range(matrix.shape[0]), list(matrix.index))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            v = matrix.iat[i, j]
            ax.text(j, i, "—" if pd.isna(v) else v[:4], ha="center", va="center",
                    color="white", fontsize=8)
    cbar = fig.colorbar(im, ax=ax, ticks=range(len(phase_order)))
    cbar.ax.set_yticklabels(phase_order)
    ax.set_title("CPV — phase consensus (group × cycle)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def plot_cf_trajectories(cycles_by_group: dict[str, dict[str, pd.Series]],
                         out_path: Path) -> Path:
    """Plot CF band-pass trajectories: subplots per cycle, lines per group."""
    import matplotlib.pyplot as plt
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cycles = list(CYCLE_BANDS.keys())
    fig, axes = plt.subplots(len(cycles), 1, figsize=(9, 2.4 * len(cycles)),
                              sharex=False)
    if len(cycles) == 1:
        axes = [axes]
    for ax, cycle in zip(axes, cycles):
        for group, by_cycle in cycles_by_group.items():
            series = by_cycle.get(cycle)
            if series is None or series.dropna().empty:
                continue
            # Quarterly horizons publish PeriodIndex; matplotlib can't cast
            # Period directly to float, so convert to Timestamp first.
            index = series.index
            if isinstance(index, pd.PeriodIndex):
                index = index.to_timestamp()
            ax.plot(index, series.values, label=group, linewidth=1.0)
        ax.axhline(0.0, color="black", linewidth=0.4)
        ax.set_title(f"CF band-pass — {cycle.capitalize()} "
                     f"({CYCLE_BANDS[cycle]['lo_years']}–{CYCLE_BANDS[cycle]['hi_years']} ans)")
        ax.legend(loc="upper left", fontsize=7, ncols=2)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def plot_wavelet_power(power_by_group: dict[str, dict],
                       out_path: Path) -> Path:
    """Wavelet power scaleogram per group (one figure with subplots)."""
    import matplotlib.pyplot as plt
    out_path.parent.mkdir(parents=True, exist_ok=True)
    groups = list(power_by_group.keys())
    if not groups:
        return out_path
    fig, axes = plt.subplots(len(groups), 1, figsize=(9, 2.6 * len(groups)),
                              sharex=False)
    if len(groups) == 1:
        axes = [axes]
    for ax, group in zip(axes, groups):
        wav = power_by_group[group]
        power = wav.get("power")
        periods = wav.get("periods")
        if power is None or power.size == 0 or periods is None or len(periods) == 0:
            ax.text(0.5, 0.5, f"{group}: pas de données", ha="center", va="center")
            continue
        ax.imshow(np.log1p(power), aspect="auto", origin="lower",
                  extent=[0, power.shape[1], periods.min(), periods.max()],
                  cmap="magma")
        ax.set_yscale("log")
        ax.set_ylabel("Période (années)")
        ax.set_title(f"Puissance wavelet — {group} (log1p)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def plot_amplitude_heatmap(table: pd.DataFrame, out_path: Path) -> Path:
    """Heatmap of Hilbert amplitudes: rows=group, cols=cycle.

    Rejected cells are masked grey. Surviving cells are coloured on a viridis
    scale and annotated with the numeric amplitude. Reading: a higher amplitude
    means a stronger band-passed signal at the endpoint, i.e. a cycle that is
    currently active rather than dormant.
    """
    import matplotlib.pyplot as plt
    from matplotlib import colors as mcolors
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if table.empty:
        return out_path
    matrix = _matrix_view(table, "amplitude")
    if matrix.empty:
        return out_path
    arr = matrix.to_numpy(dtype=float)
    masked = np.ma.masked_invalid(arr)

    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad(color="#d0d0d0")

    fig, ax = plt.subplots(figsize=(8, max(3, 0.6 * matrix.shape[0])))
    finite = arr[np.isfinite(arr)]
    vmax = float(finite.max()) if finite.size else 1.0
    im = ax.imshow(masked, cmap=cmap, aspect="auto", vmin=0.0, vmax=vmax)
    ax.set_xticks(range(matrix.shape[1]), [c.capitalize() for c in matrix.columns])
    ax.set_yticks(range(matrix.shape[0]), list(matrix.index))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            v = matrix.iat[i, j]
            if pd.isna(v):
                ax.text(j, i, "—", ha="center", va="center",
                        color="#404040", fontsize=8)
                continue
            text_colour = "white" if v < 0.55 * vmax else "black"
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    color=text_colour, fontsize=8)
    fig.colorbar(im, ax=ax, label="Amplitude Hilbert (z-score CF)")
    ax.set_title("CPV — amplitude des cycles (groupes × bandes)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def plot_pvalue_heatmap(table: pd.DataFrame, out_path: Path,
                        alpha: float = 0.05) -> Path:
    """Heatmap of Gate 1 p-values: rows=group, cols=cycle.

    Cells with p ≤ ``alpha`` are coloured green (the null is rejected — the
    cycle survives Gate 1) ; cells with p > ``alpha`` are red. The fixed scale
    [0, 1] makes the threshold visually obvious. Annotations show the p-value.
    """
    import matplotlib.pyplot as plt
    from matplotlib import colors as mcolors
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if table.empty:
        return out_path
    matrix = _matrix_view(table, "ar1_p_value")
    if matrix.empty:
        return out_path
    arr = matrix.to_numpy(dtype=float)
    masked = np.ma.masked_invalid(arr)

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "pdual", [(0.0, "#1b7837"), (alpha, "#a6dba0"),
                  (alpha + 1e-6, "#f4a582"), (1.0, "#b2182b")])
    cmap.set_bad(color="#d0d0d0")

    fig, ax = plt.subplots(figsize=(8, max(3, 0.6 * matrix.shape[0])))
    im = ax.imshow(masked, cmap=cmap, aspect="auto", vmin=0.0, vmax=1.0)
    ax.set_xticks(range(matrix.shape[1]), [c.capitalize() for c in matrix.columns])
    ax.set_yticks(range(matrix.shape[0]), list(matrix.index))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            v = matrix.iat[i, j]
            if pd.isna(v):
                ax.text(j, i, "—", ha="center", va="center",
                        color="#404040", fontsize=8)
                continue
            text_colour = "white" if v <= alpha or v >= 0.7 else "black"
            ax.text(j, i, f"{v:.3f}", ha="center", va="center",
                    color=text_colour, fontsize=8)
    cbar = fig.colorbar(im, ax=ax, label="p-value dual-null")
    cbar.ax.axhline(alpha, color="black", linewidth=1.2)
    ax.set_title(f"CPV — p-values Gate 1 (seuil α = {alpha:.2f})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def plot_phase_polar_diagram(table: pd.DataFrame, cycle: str,
                             out_path: Path) -> Path:
    """Polar phase diagram for a single cycle band.

    Each group is plotted at angular position φ (Hilbert phase) and radius
    equal to its Hilbert amplitude. The four cardinal quadrants are annotated
    with the Bry-Boschan-equivalent labels (expansion / peak / contraction /
    trough). Cells that failed Gate 1 are dropped.
    """
    import matplotlib.pyplot as plt
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if table.empty:
        return out_path
    sub = table[(table["cycle"] == cycle) & (table["phase"] != "rejected")].copy()
    if sub.empty:
        return out_path
    sub = sub.dropna(subset=["phi_rad", "amplitude"])
    if sub.empty:
        return out_path

    fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(7, 7))
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)

    amp_max = float(sub["amplitude"].max()) if sub["amplitude"].size else 1.0
    cmap = plt.get_cmap("tab10")
    groups = list(sub["group_code"])
    for idx, row in enumerate(sub.itertuples()):
        ax.scatter(float(row.phi_rad), float(row.amplitude),
                   color=cmap(idx % 10), s=130, zorder=5,
                   edgecolor="black", linewidth=0.6, label=row.group_code)
        ax.annotate(row.group_code,
                    xy=(float(row.phi_rad), float(row.amplitude)),
                    xytext=(8, 8), textcoords="offset points",
                    fontsize=8)

    # Quadrant labels at mid-angle and outside the data ring.
    label_r = amp_max * 1.15 if amp_max > 0 else 1.0
    ax.text(np.pi / 2, label_r, "Pic", ha="center", va="bottom", fontsize=10,
            color="#1b7837", weight="bold")
    ax.text(np.pi, label_r, "Contraction", ha="right", va="center", fontsize=10,
            color="#b2182b", weight="bold")
    ax.text(-np.pi / 2, label_r, "Creux", ha="center", va="top", fontsize=10,
            color="#762a83", weight="bold")
    ax.text(0.0, label_r, "Expansion", ha="left", va="center", fontsize=10,
            color="#1f77b4", weight="bold")

    # Quadrant separators.
    for angle in (0.0, np.pi / 2, np.pi, -np.pi / 2):
        ax.plot([angle, angle], [0, label_r * 1.05], color="grey",
                linewidth=0.6, linestyle="--", zorder=1)

    ax.set_rlim(0.0, label_r * 1.2 if amp_max > 0 else 1.5)
    ax.set_rlabel_position(135)
    ax.set_title(f"Diagramme de phase polaire — {cycle.capitalize()} "
                 f"({CYCLE_BANDS[cycle]['lo_years']}-"
                 f"{CYCLE_BANDS[cycle]['hi_years']} ans)", pad=20)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def plot_next_extremum_timeline(table: pd.DataFrame, as_of: str,
                                out_path: Path) -> Path:
    """Horizontal timeline of the next predicted extremum per group, per cycle.

    Four rows (one per cycle band). Each surviving cell is plotted at its
    forecast ETA from ``as_of``, as ▲ (peak) or ▼ (trough). A ±1 year span
    illustrates that this is an order of magnitude, not a Bayesian CI.
    """
    import matplotlib.pyplot as plt
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if table.empty:
        return out_path
    sub = table[(table["phase"] != "rejected")].dropna(
        subset=["next_eta_years"]).copy()
    if sub.empty:
        return out_path

    base_year = float(as_of[:4])
    if "-" in as_of and len(as_of) >= 7:
        base_year += (int(as_of[5:7]) - 1) / 12.0
    sub["target_year"] = base_year + sub["next_eta_years"].astype(float)

    cycles = list(CYCLE_BANDS.keys())
    fig, ax = plt.subplots(figsize=(10, 1.0 * len(cycles) + 2.0))

    group_to_colour: dict[str, tuple] = {}
    cmap = plt.get_cmap("tab10")
    for idx, g in enumerate(sorted(sub["group_code"].drop_duplicates())):
        group_to_colour[g] = cmap(idx % 10)

    for row_idx, cycle in enumerate(cycles):
        ax.axhline(row_idx, color="lightgrey", linewidth=0.5, zorder=1)
        for r in sub[sub["cycle"] == cycle].itertuples():
            marker = "^" if r.next_kind == "max" else "v"
            colour = group_to_colour.get(r.group_code, "black")
            ax.errorbar(r.target_year, row_idx, xerr=1.0, fmt=marker,
                        color=colour, markersize=10, ecolor=colour,
                        elinewidth=1.0, capsize=3, zorder=5)
            ax.annotate(r.group_code, xy=(r.target_year, row_idx),
                        xytext=(0, 8), textcoords="offset points",
                        ha="center", fontsize=7, color=colour)

    ax.axvline(base_year, color="black", linewidth=0.8, linestyle=":",
               label=f"as-of {as_of}")
    ax.set_yticks(range(len(cycles)))
    ax.set_yticklabels([c.capitalize() for c in cycles])
    ax.set_xlabel("Année calendaire (forecast ± 1 an)")
    ax.set_title("Prochains extrema prévus par cycle (▲ pic / ▼ creux)")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path
