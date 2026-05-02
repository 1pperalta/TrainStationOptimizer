"""Local search refinement using one-for-one station swaps."""

import numpy as np

from src.domain.interfaces import ObjectiveEvaluatorInterface, StationOptimizerInterface
from src.domain.models import Coordinate, OptimizationResult


class LocalSearchOptimizer(StationOptimizerInterface):
    """Improve an initial solution via improving swaps until local optimum."""

    def __init__(
        self,
        objective_evaluator: ObjectiveEvaluatorInterface,
        candidate_nodes,
        initial_stations,
    ) -> None:
        self._objective = objective_evaluator
        self._candidate_nodes = list(candidate_nodes)
        self._initial_stations = list(initial_stations)

    def optimize(self, scenarios: np.ndarray, max_stations: int) -> OptimizationResult:
        current = self._initial_stations[:max_stations]
        best_cost = self._objective.evaluate(current, scenarios)

        improved = True
        while improved:
            improved = False
            selected_set = set(current)
            non_selected = [c for c in self._candidate_nodes if c not in selected_set]

            for out_station in list(current):
                for in_station in non_selected:
                    proposal = [s for s in current if s != out_station] + [in_station]
                    proposal_cost = self._objective.evaluate(proposal, scenarios)
                    if proposal_cost < best_cost:
                        current = proposal
                        best_cost = proposal_cost
                        improved = True
                        break
                if improved:
                    break

        return OptimizationResult(stations=current, objective_value=best_cost)
