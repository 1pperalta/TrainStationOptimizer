"""Distance utilities for grid-based walking cost."""

from typing import List, Sequence

import numpy as np

from src.domain.models import Coordinate, GridSpec


class DistanceCalculator:
    """Precompute and query Manhattan distances over the full grid."""

    def __init__(self, grid: GridSpec) -> None:
        self.grid = grid
        self.nodes: List[Coordinate] = [
            (i, j) for i in range(self.grid.rows) for j in range(self.grid.cols)
        ]
        self._node_to_idx = {node: idx for idx, node in enumerate(self.nodes)}
        self._distance_matrix = self._build_distance_matrix()

    def _build_distance_matrix(self) -> np.ndarray:
        n = len(self.nodes)
        matrix = np.zeros((n, n), dtype=np.int16)
        for a, (i1, j1) in enumerate(self.nodes):
            for b, (i2, j2) in enumerate(self.nodes):
                matrix[a, b] = abs(i1 - i2) + abs(j1 - j2)
        return matrix

    def nearest_station_distance(self, stations: Sequence[Coordinate]) -> np.ndarray:
        """Return vector with nearest-station distance for each grid node."""

        if not stations:
            raise ValueError("stations must not be empty")

        station_indices = [self._node_to_idx[s] for s in stations]
        distances_to_selected = self._distance_matrix[:, station_indices]
        return distances_to_selected.min(axis=1)
