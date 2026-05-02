"""Objective function: expected weighted walking distance."""

from typing import Sequence

import numpy as np

from src.cost.distance import DistanceCalculator
from src.domain.interfaces import ObjectiveEvaluatorInterface
from src.domain.models import Coordinate


class ObjectiveEvaluator(ObjectiveEvaluatorInterface):
    """Evaluate expected cost of a station set under stochastic scenarios."""

    def __init__(self, distance_calculator: DistanceCalculator) -> None:
        self._distance = distance_calculator

    def evaluate(self, stations: Sequence[Coordinate], scenarios: np.ndarray) -> float:
        if scenarios.ndim != 3:
            raise ValueError("scenarios must have shape (num_scenarios, rows, cols)")

        nearest_dist = self._distance.nearest_station_distance(stations)
        flat_dist = nearest_dist.astype(np.float64)

        costs = []
        for scenario in scenarios:
            pop = scenario.reshape(-1).astype(np.float64)
            one_side_cost = float(np.dot(pop, flat_dist))
            full_trip_cost = 2.0 * one_side_cost
            costs.append(full_trip_cost)

        return float(np.mean(costs))
