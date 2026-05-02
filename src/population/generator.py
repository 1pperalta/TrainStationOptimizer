"""Population scenario generation based on a Poisson process."""

from typing import Optional

import numpy as np

from src.domain.interfaces import PopulationGeneratorInterface
from src.domain.models import GridSpec


class PopulationGenerator(PopulationGeneratorInterface):
    """Generate stochastic population scenarios for the full grid."""

    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = np.random.default_rng(seed)

    @staticmethod
    def _lambda_ij(i: int, j: int, years_ahead: int) -> float:
        """Deterministic mean used by the Poisson model.

        This mirrors the idea in the starter notebook: expected population depends
        on location and forecast horizon.
        """

        base = 60.0 + 3.0 * i + 2.0 * j
        growth = 1.0 + 0.015 * years_ahead
        return max(1.0, base * growth)

    def generate(self, grid: GridSpec, years_ahead: int, num_scenarios: int) -> np.ndarray:
        scenarios = np.zeros((num_scenarios, grid.rows, grid.cols), dtype=np.int32)

        for k in range(num_scenarios):
            for i in range(grid.rows):
                for j in range(grid.cols):
                    lam = self._lambda_ij(i, j, years_ahead)
                    scenarios[k, i, j] = self._rng.poisson(lam)

        return scenarios
