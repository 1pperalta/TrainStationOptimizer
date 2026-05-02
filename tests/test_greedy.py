from src.cost.distance import DistanceCalculator
from src.cost.objective import ObjectiveEvaluator
from src.domain.models import GridSpec
from src.optimization.greedy import GreedyOptimizer
from src.population.generator import PopulationGenerator


def test_greedy_returns_requested_station_count() -> None:
    grid = GridSpec(rows=4, cols=4)
    generator = PopulationGenerator(seed=1)
    scenarios = generator.generate(grid=grid, years_ahead=5, num_scenarios=5)

    distance = DistanceCalculator(grid)
    objective = ObjectiveEvaluator(distance)
    optimizer = GreedyOptimizer(objective_evaluator=objective, candidate_nodes=distance.nodes)

    result = optimizer.optimize(scenarios=scenarios, max_stations=3)

    assert len(result.stations) == 3
