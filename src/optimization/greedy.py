"""Greedy station selection optimizer."""

import numpy as np

from src.domain.interfaces import ObjectiveEvaluatorInterface, StationOptimizerInterface
from src.domain.models import OptimizationResult


class GreedyOptimizer(StationOptimizerInterface):
    """Add stations iteratively, maximizing objective improvement each step."""

    def __init__(self, objective_evaluator: ObjectiveEvaluatorInterface, candidate_nodes) -> None:
        self._objective = objective_evaluator
        self._candidate_nodes = list(candidate_nodes)

    def optimize(self, scenarios: np.ndarray, max_stations: int) -> OptimizationResult:
        selected = []

        for _ in range(max_stations):
            best_candidate = None
            best_cost = float("inf")

            for candidate in self._candidate_nodes:
                if candidate in selected:
                    continue
                proposal = selected + [candidate]
                cost = self._objective.evaluate(proposal, scenarios)
                if cost < best_cost:
                    best_cost = cost
                    best_candidate = candidate

            if best_candidate is None:
                break

            selected.append(best_candidate)

        final_cost = self._objective.evaluate(selected, scenarios)
        return OptimizationResult(stations=selected, objective_value=final_cost)
