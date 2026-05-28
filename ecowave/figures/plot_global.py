from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless container
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

WEIGHTING_STYLE = {
    "equal": {"label": "equal weights (0.20 each)", "linestyle": "-", "color": "#0b3d91"},
    "pca": {"label": "PCA loadings (PC1)", "linestyle": "--", "color": "#cc5500"},
    "favar": {"label": "FAVAR predictive R²", "linestyle": ":", "color": "#117733"},
}


def plot_global_indices(global_indices: pd.DataFrame, output_path: Path, pilot: str,
                        ref: str = "precrisis") -> Path:
    """Composite intensity (3 weightings) + diffusion histogram."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sub = global_indices[global_indices["ref"] == ref].sort_values("month")
    if sub.empty:
        return output_path
    months = sorted(sub["month"].unique())

    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=(11, 6.5), sharex=True,
        gridspec_kw={"height_ratios": [3, 1]},
    )

    for weighting, style in WEIGHTING_STYLE.items():
        wsub = sub[sub["weighting"] == weighting].set_index("month").sort_index()
        if wsub.empty:
            continue
        ax_top.plot(
            range(len(months)),
            [wsub.loc[m, "intensity_ma3"] if m in wsub.index else float("nan")
             for m in months],
            linestyle=style["linestyle"], color=style["color"], linewidth=1.6,
            label=f"I_intensity ({style['label']})",
        )

    ax_top.axhline(75, color="grey", linestyle="--", linewidth=0.8,
                    label="high-stress threshold (75)")
    ax_top.set_ylabel("I_intensity (MA3, 0-100)")
    ax_top.set_ylim(0, 105)
    ax_top.set_title(f"CPV — composite intensity, pilot {pilot} (ref={ref})")
    ax_top.grid(True, alpha=0.25)

    diff = sub[sub["weighting"] == "equal"].set_index("month")["diffusion"]
    ax_bot.bar(range(len(months)), [diff.get(m, 0) for m in months],
               color="#888888", width=0.85)
    ax_bot.axhline(3, color="#cc5500", linestyle="--", linewidth=0.8,
                    label="diffusion confirmation (≥3)")
    ax_bot.set_ylim(0, 5.5)
    ax_bot.set_ylabel("I_diffusion (count >80)")
    ax_bot.set_yticks([0, 1, 2, 3, 4, 5])
    ax_bot.grid(True, alpha=0.25)
    ax_bot.legend(loc="upper left", fontsize=8)

    step = max(1, len(months) // 12)
    ax_bot.set_xticks(range(0, len(months), step))
    ax_bot.set_xticklabels([months[i] for i in range(0, len(months), step)],
                            rotation=45, ha="right")
    ax_top.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=120)
    plt.close(fig)
    return output_path
