"""Application entrypoint to run the full optimization pipeline."""

from src.config import ExperimentConfig
from src.cost.distance import DistanceCalculator
from src.cost.objective import ObjectiveEvaluator
from src.domain.models import ExperimentResult, GridSpec
from src.optimization.baseline import RandomBaselineOptimizer
from src.optimization.greedy import GreedyOptimizer
from src.optimization.local_search import LocalSearchOptimizer
from src.population.generator import PopulationGenerator


def run_experiment(config: ExperimentConfig) -> ExperimentResult:
    """Run scenario generation, optimization, and comparison end-to-end."""

    grid = GridSpec(rows=config.rows, cols=config.cols)

    generator = PopulationGenerator(seed=config.seed)
    scenarios = generator.generate(
        grid=grid,
        years_ahead=config.years_ahead,
        num_scenarios=config.num_scenarios,
    )

    distance = DistanceCalculator(grid)
    objective = ObjectiveEvaluator(distance)

    baseline_optimizer = RandomBaselineOptimizer(
        objective_evaluator=objective,
        candidate_nodes=distance.nodes,
        trials=100,
        seed=config.seed,
    )
    baseline = baseline_optimizer.optimize(scenarios, config.max_stations)

    greedy_optimizer = GreedyOptimizer(
        objective_evaluator=objective,
        candidate_nodes=distance.nodes,
    )
    greedy = greedy_optimizer.optimize(scenarios, config.max_stations)

    local_search_optimizer = LocalSearchOptimizer(
        objective_evaluator=objective,
        candidate_nodes=distance.nodes,
        initial_stations=greedy.stations,
    )
    local_search = local_search_optimizer.optimize(scenarios, config.max_stations)

    return ExperimentResult(
        baseline=baseline,
        greedy=greedy,
        local_search=local_search,
        scenario_count=config.num_scenarios,
        stations_limit=config.max_stations,
    )


if __name__ == "__main__":
    cfg = ExperimentConfig()
    result = run_experiment(cfg)

    print("=== Train Station Optimization Results ===")
    print(f"Scenarios: {result.scenario_count}")
    print(f"Max stations: {result.stations_limit}")
    print()
    print(f"Baseline cost: {result.baseline.objective_value:.2f}")
    print(f"Greedy cost:   {result.greedy.objective_value:.2f}")
    print(f"Local cost:    {result.local_search.objective_value:.2f}")
    print()
    print(f"Baseline stations: {result.baseline.stations}")
    print(f"Greedy stations:   {result.greedy.stations}")
    print(f"Local stations:    {result.local_search.stations}")
