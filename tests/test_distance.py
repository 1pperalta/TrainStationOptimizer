import numpy as np

from src.cost.distance import DistanceCalculator
from src.domain.models import GridSpec


def test_nearest_station_distance_basic() -> None:
    grid = GridSpec(rows=3, cols=3)
    calc = DistanceCalculator(grid)

    distances = calc.nearest_station_distance([(0, 0)])
    assert distances.shape == (9,)
    assert distances[0] == 0


def test_nearest_station_distance_multiple() -> None:
    grid = GridSpec(rows=3, cols=3)
    calc = DistanceCalculator(grid)

    distances = calc.nearest_station_distance([(0, 0), (2, 2)])
    assert int(distances.max()) <= 2
