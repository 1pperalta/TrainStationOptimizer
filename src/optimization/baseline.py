"""Random baseline optimizer for comparison."""

from typing import Optional

import numpy as np

from src.domain.interfaces import ObjectiveEvaluatorInterface, StationOptimizerInterface
from src.domain.models import OptimizationResult


class RandomBaselineOptimizer(StationOptimizerInterface):
    """Sample random station sets and keep the best observed."""

    def __init__(
        self,
        objective_evaluator: ObjectiveEvaluatorInterface,
        candidate_nodes,
        trials: int = 100,
        seed: Optional[int] = None,
    ) -> None:
        self._objective = objective_evaluator
        self._candidate_nodes = list(candidate_nodes)
        self._trials = trials
        self._rng = np.random.default_rng(seed)

    def optimize(self, scenarios: np.ndarray, max_stations: int) -> OptimizationResult:
        best_stations = None
        best_cost = float("inf")

        for _ in range(self._trials):
            indices = self._rng.choice(len(self._candidate_nodes), size=max_stations, replace=False)
            stations = [self._candidate_nodes[i] for i in indices]
            cost = self._objective.evaluate(stations, scenarios)
            if cost < best_cost:
                best_cost = cost
                best_stations = stations

        return OptimizationResult(stations=best_stations, objective_value=best_cost)
