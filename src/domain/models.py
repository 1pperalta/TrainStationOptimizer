"""Domain models and shared type aliases."""

from dataclasses import dataclass
from typing import List, Sequence, Tuple

import numpy as np

Coordinate = Tuple[int, int]
ScenarioArray = np.ndarray


@dataclass(frozen=True)
class GridSpec:
    """Grid dimensions for the city model."""

    rows: int
    cols: int


@dataclass(frozen=True)
class OptimizationResult:
    """Optimization output with selected stations and objective value."""

    stations: Sequence[Coordinate]
    objective_value: float


@dataclass(frozen=True)
class ExperimentResult:
    """Aggregated results for baseline, greedy, and local search."""

    baseline: OptimizationResult
    greedy: OptimizationResult
    local_search: OptimizationResult
    scenario_count: int
    stations_limit: int
