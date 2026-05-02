"""Project-wide configuration defaults."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentConfig:
    """Configuration for one optimization experiment."""

    rows: int = 20
    cols: int = 20
    max_stations: int = 6
    years_ahead: int = 20
    num_scenarios: int = 100
    seed: int = 42
