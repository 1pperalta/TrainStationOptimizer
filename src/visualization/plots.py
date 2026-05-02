"""Visualization helpers for population and station plans."""

from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np


def plot_average_population_with_stations(
    scenarios: np.ndarray,
    stations: Sequence[tuple[int, int]],
    title: str = "Average Population and Selected Stations",
) -> None:
    """Plot mean population heatmap and overlay selected station coordinates."""

    avg_population = scenarios.mean(axis=0)

    plt.figure(figsize=(8, 7))
    plt.imshow(avg_population, cmap="YlOrRd", origin="lower")
    if stations:
        ys = [s[0] for s in stations]
        xs = [s[1] for s in stations]
        plt.scatter(xs, ys, c="blue", s=90, marker="s", label="Stations")
        plt.legend()
    plt.colorbar(label="Average population")
    plt.title(title)
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.tight_layout()
    plt.show()
