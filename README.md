# Train Station Optimization

This project solves train-station placement on a grid city under uncertain population.

## Objective

- City is an `R x C` grid.
- Population is stochastic at each node.
- Walking cost is counted as:
  - origin -> nearest station
  - nearest station -> destination
- Train ride cost is ignored.
- Goal: choose at most `N` stations minimizing expected walking cost.

## Units and Interpretation

- Distance metric: Manhattan distance on the grid.
- Cost unit: weighted grid-steps (not meters by default).
- If one cell equals `k` meters, convert by multiplying distance/cost by `k`.

## Project Structure

- `src/config.py`: experiment parameters (`R, C, N, t, num_scenarios, seed`).
- `src/population/generator.py`: Poisson-based scenario generation.
- `src/cost/distance.py`: Manhattan distance engine.
- `src/cost/objective.py`: expected walking-cost objective.
- `src/optimization/baseline.py`: random baseline.
- `src/optimization/greedy.py`: greedy station construction.
- `src/optimization/local_search.py`: swap-based local improvement.
- `src/app/run_experiment.py`: end-to-end run.
- `src/visualization/plots.py`: heatmap + station overlay.
- `tests/`: core sanity tests.

## Coding Rules

- Keep functions focused and short.
- Use clear English names and `snake_case` in Python.
- No emojis or redundant comments in code/docs.
- Separate concerns: generation, cost, optimization, visualization.
- Prefer interface-based dependencies for extensibility.
- Keep runs reproducible with fixed seeds.

## Workflow

1. Set parameters in `src/config.py`.
2. Run scenario generation and optimization pipeline.
3. Compare baseline vs greedy vs local search.
4. Validate stability with multiple seeds.
5. Visualize and interpret results.

## Setup (uv)

```bash
uv sync --dev
```

## Run

```bash
uv run python -m src.app.run_experiment
```

## Test

```bash
uv run python -m pytest -q
```
