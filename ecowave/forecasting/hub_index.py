"""Hub index rendering — Roadmap #22 Phase 6.

The hub home page (`docs/index.md`) displays the *current* consolidated
forecast benchmark verdict. To keep it in sync with the actual JSON
sidecars without a manual edit each time the benchmark is re-run, this
module reads the consolidated summary and updates the "Verdict en une
page" block of `docs/index.md` in place.

Mechanism. The home page contains two HTML-comment markers:

    <!-- BEGIN: AUTO-VERDICT -->
    ...content automatically replaced...
    <!-- END: AUTO-VERDICT -->

Calling :func:`render_hub_index` reads the sidecars via
``consolidate_benchmark_sidecars`` and rewrites the block between the
markers with up-to-date numbers (pass rate, n variables, leaderboard).
The rest of `docs/index.md` is untouched.

The block is kept short — a one-line headline + a 3-row leaderboard
table — so it stays above the fold on the rendered Material page.

The matching CLI command is ``ecowave render-hub-index`` (see
:mod:`ecowave.cli`).
"""
from __future__ import annotations

import re
from pathlib import Path

from ecowave.forecasting.consolidated_report import (
    ConsolidatedSummary,
    consolidate_benchmark_sidecars,
)


AUTO_VERDICT_BEGIN_MARKER = "<!-- BEGIN: AUTO-VERDICT -->"
AUTO_VERDICT_END_MARKER = "<!-- END: AUTO-VERDICT -->"


def render_verdict_block(summary: ConsolidatedSummary) -> str:
    """Return the markdown content that goes between the auto markers."""
    aggregate_label = "PASS" if summary.passes else "FAIL"
    emoji = "✅" if summary.passes else "❌"
    pass_rate_pct = int(round(summary.aggregate_pass_rate * 100))
    leaderboard = summary.leaderboard()
    total_wins = sum(count for _, count in leaderboard)

    leaderboard_lines = [
        "| Modèle cluster | Wins | Part |",
        "|---|---|---|",
    ]
    for model_name, count in leaderboard:
        share_pct = int(round(100 * count / total_wins)) if total_wins > 0 else 0
        # Match the human-readable labels used in V1.
        display = {
            "msm": "MSM (Calvet-Fisher)",
            "har": "HAR (Corsi 2009)",
            "arfima_rs": "ARFIMA + regime-switching",
        }.get(model_name, model_name)
        leaderboard_lines.append(f"| {display} | {count} | {share_pct} % |")

    return (
        f"{emoji} **Verdict consolidé** : {aggregate_label} — pass rate "
        f"{pass_rate_pct} % sur {summary.total_passing} / "
        f"{summary.total_variables} variables (6 panels, "
        f"as_of = {summary.as_of}).\n\n" + "\n".join(leaderboard_lines)
    )


def render_hub_index(
    index_path: Path,
    summary: ConsolidatedSummary,
) -> None:
    """Rewrite the AUTO-VERDICT block of ``index_path`` in place.

    If the markers are absent, raises ``ValueError`` rather than
    silently appending — this keeps the change explicit.
    """
    original_text = index_path.read_text(encoding="utf-8")
    if AUTO_VERDICT_BEGIN_MARKER not in original_text:
        raise ValueError(
            f"{index_path} does not contain {AUTO_VERDICT_BEGIN_MARKER!r}"
        )
    if AUTO_VERDICT_END_MARKER not in original_text:
        raise ValueError(
            f"{index_path} does not contain {AUTO_VERDICT_END_MARKER!r}"
        )

    new_block = render_verdict_block(summary)
    replacement = f"{AUTO_VERDICT_BEGIN_MARKER}\n\n{new_block}\n\n{AUTO_VERDICT_END_MARKER}"

    pattern = re.compile(
        re.escape(AUTO_VERDICT_BEGIN_MARKER) + r".*?" + re.escape(AUTO_VERDICT_END_MARKER),
        flags=re.DOTALL,
    )
    new_text = pattern.sub(replacement, original_text)
    index_path.write_text(new_text, encoding="utf-8")


def render_hub_index_from_reports(
    reports_dir: Path,
    index_path: Path,
    as_of: str,
    panel_codes: tuple[str, ...] = ("wb", "q", "long", "boe", "bis", "sh"),
    beat_threshold: float = 0.5,
) -> ConsolidatedSummary:
    """Convenience wrapper : consolidate then render."""
    summary = consolidate_benchmark_sidecars(
        reports_dir=reports_dir,
        as_of=as_of,
        panel_codes=panel_codes,
        beat_threshold=beat_threshold,
    )
    render_hub_index(index_path, summary)
    return summary
