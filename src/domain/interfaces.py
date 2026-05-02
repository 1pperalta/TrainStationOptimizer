"""Abstract interfaces to enforce dependency inversion."""

from abc import ABC, abstractmethod
from typing import Sequence, Tuple

import numpy as np

from src.domain.models import Coordinate, GridSpec, OptimizationResult


class PopulationGeneratorInterface(ABC):
    """Contract for stochastic population scenario generation."""

    @abstractmethod
    def generate(self, grid: GridSpec, years_ahead: int, num_scenarios: int) -> np.ndarray:
        """Return array with shape (num_scenarios, rows, cols)."""


class ObjectiveEvaluatorInterface(ABC):
    """Contract for station-set objective evaluation."""

    @abstractmethod
    def evaluate(self, stations: Sequence[Coordinate], scenarios: np.ndarray) -> float:
        """Return expected weighted walking cost."""


class StationOptimizerInterface(ABC):
    """Contract for any station optimization strategy."""

    @abstractmethod
    def optimize(self, scenarios: np.ndarray, max_stations: int) -> OptimizationResult:
        """Return best stations and objective value."""
