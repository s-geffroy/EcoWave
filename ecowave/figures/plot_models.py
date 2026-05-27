from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless container
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

def plot_model_windows(curves: pd.DataFrame, output_path: Path, models: dict) -> Path:
    """Plot the mean cross-curve stress with each model's candidate phase windows."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    model_items = list(models.items())
    mean_stress = (curves.groupby("month")["stress_precrisis"].mean().sort_index())
    months = list(mean_stress.index)
    pos = {m: i for i, m in enumerate(months)}

    fig, axes = plt.subplots(len(model_items), 1, figsize=(11, 8), sharex=True)
    for ax, (code, model) in zip(axes, model_items):
        ax.plot(range(len(months)), mean_stress.values, color="black", linewidth=1.4)
        ax.axhline(75, color="grey", linestyle="--", linewidth=0.8)
        for i, (label, start, end) in enumerate(model["candidate_phases"]):
            x0 = pos.get(start, 0)
            x1 = pos.get(end, len(months) - 1)
            ax.axvspan(x0, x1, alpha=0.15, color=f"C{i}")
        ax.set_title(f"Model {code}: {model['name']}", fontsize=10, loc="left")
        ax.set_ylim(0, 105)
        ax.set_ylabel("mean stress")
        ax.grid(True, alpha=0.2)

    step = max(1, len(months) // 12)
    axes[-1].set_xticks(range(0, len(months), step))
    axes[-1].set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")
    fig.suptitle("EcoWave — candidate Elliott windows vs mean cross-curve stress", y=0.995)
    fig.tight_layout()
    fig.savefig(output_path, dpi=120)
    plt.close(fig)
    return output_path
