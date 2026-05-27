from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_placeholder(panel: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure()
    plt.title("EcoWave placeholder")
    plt.xlabel("month")
    plt.ylabel("stress")
    plt.text(0.5, 0.5, "Real data ingestion required", ha="center", va="center")
    fig.savefig(output_path)
    plt.close(fig)
