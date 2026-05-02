import numpy as np

from src.cost.distance import DistanceCalculator
from src.cost.objective import ObjectiveEvaluator
from src.domain.models import GridSpec


def test_objective_non_negative() -> None:
    grid = GridSpec(rows=2, cols=2)
    distance = DistanceCalculator(grid)
    objective = ObjectiveEvaluator(distance)

    scenarios = np.array([[[10, 20], [30, 40]]], dtype=np.int32)
    value = objective.evaluate(stations=[(0, 0)], scenarios=scenarios)

    assert value >= 0
