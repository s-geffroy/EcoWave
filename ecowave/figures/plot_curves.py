from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless container
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

CURVE_LABELS = {
    "E": "E — Economic / financial",
    "D": "D — Diplomatic / institutional",
    "S": "S — Social",
    "L": "L — Logistics / energy",
    "I": "I — Information",
}
CURVE_ORDER = ["E", "D", "S", "L", "I"]


def plot_curve_stress(curves: pd.DataFrame, output_path: Path) -> Path:
    """Plot pre-crisis stress (0-100) per curve over the panel window."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pivot = curves.pivot(index="month", columns="curve", values="stress_precrisis").sort_index()

    window = f"{pivot.index.min()}..{pivot.index.max()}" if len(pivot.index) else ""
    fig, ax = plt.subplots(figsize=(11, 5))
    for curve in CURVE_ORDER:
        if curve in pivot.columns and pivot[curve].notna().any():
            ax.plot(pivot.index, pivot[curve], marker="o", markersize=3,
                    linewidth=1.6, label=CURVE_LABELS[curve])
    ax.axhline(75, color="grey", linestyle="--", linewidth=0.8, label="high-stress threshold (75)")
    ax.set_title(f"EcoWave — curve stress (pre-crisis percentile), {window}")
    ax.set_xlabel("month")
    ax.set_ylabel("stress percentile (0-100)")
    ax.set_ylim(0, 105)
    _thin_xticks(ax, pivot.index)
    ax.legend(loc="upper left", fontsize=8, ncol=2)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=120)
    plt.close(fig)
    return output_path


def _thin_xticks(ax, months) -> None:
    months = list(months)
    step = max(1, len(months) // 12)
    ax.set_xticks(range(0, len(months), step))
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")
