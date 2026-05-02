# Train Station Planning Project Context

## Project Goal

Design a train route/station plan for a city represented as an `R x C` grid. Each grid vertex `(i, j)` has a stochastic future population. The goal is to choose at most `N` train stations so that, even under random population changes, the average user walking cost is minimized.

The current notebook sets:

- `R = 20`
- `C = 20`
- `N = 6`

## Source Files

- `projectinstructions.txt`: Spanish assignment description.
- `información_base_modelo_de_prescriptiva.ipynb`: starter notebook with stochastic population functions and a population heatmap.

## Population Model From Notebook

The notebook defines two functions:

```python
def pr(i, j, t, n):
    # Probability that node (i, j) has population n after t years.
    # Uses a Poisson distribution.

def gen(i, j, t):
    # Generates one sampled population value for node (i, j) after t years.
```

The population is modeled with a Poisson distribution whose mean depends on grid position and time `t`.

Important detail from the assignment: for every fixed `(i, j, t)`, the probabilities over all possible population values `n` sum to 1. Probabilities are not normalized across grid positions.

## Travel Behavior

People travel randomly from an origin node `(i, j)` to a destination node `(a, b)`.

Destination probabilities are proportional to destination population. Example:

```text
destination populations = [1200, 1200, 2400]
destination probabilities = [0.25, 0.25, 0.50]
```

For each trip:

1. A user walks from origin to the nearest train station.
2. The user rides the train.
3. The user walks from the station nearest the destination to the destination.

Train travel cost can be ignored. The relevant cost is only the walking distance before and after riding the train.

## Core Modeling Insight

Because train travel cost is negligible, the main optimization problem is station placement, not the exact train route order.

Once stations are chosen, they can be connected afterward as:

- a cycle, or
- a linear route.

The optimization should first decide where the `N` stations go.

## Recommended Distance Metric

Use Manhattan distance on the grid:

```text
dist((i, j), (a, b)) = abs(i - a) + abs(j - b)
```

This matches walking through grid edges.

## Optimization Interpretation

This is similar to a stochastic `p-median` / facility-location problem.

Let:

- `S` be the selected station set.
- `pop_scenario[k]` be one sampled population map.
- `d(node, S)` be the distance from a node to its nearest selected station.

A practical objective is:

```text
minimize average over scenarios of:
    sum over grid nodes population(node) * d(node, S)
```

If origins and destinations are both proportional to population, the full trip walking cost is approximately:

```text
2 * sum population(node) * distance_to_nearest_station(node)
```

So minimizing the one-sided weighted distance also minimizes the total expected walking cost.

## Suggested Implementation Plan

1. Generate many population scenarios for a target year `t` using `gen(i, j, t)`.
2. Flatten the grid into a list of candidate nodes.
3. Build a Manhattan distance matrix between every grid node and every possible station node.
4. Optimize station placement with at most `N` stations.
5. Compute the expected/average walking cost over all population scenarios.
6. Visualize:
   - population heatmap,
   - selected station locations,
   - optional train route connecting stations.

## Possible Solution Methods

### Simple Heuristic

Use greedy station selection:

1. Start with no stations.
2. Add the station that gives the largest reduction in weighted walking cost.
3. Repeat until `N` stations are selected.

This is easy to implement and explain.

### Better Heuristic

Use local search after greedy initialization:

1. Start from greedy stations.
2. Try swapping one selected station with one unselected candidate.
3. Keep swaps that improve cost.
4. Stop when no improving swap exists.

### Exact Optimization

Formulate as a mixed-integer optimization model:

- Binary variable `x_s = 1` if station candidate `s` is selected.
- Binary assignment variable `y_{v,s} = 1` if node `v` is assigned to station `s`.
- Constraint: `sum_s x_s <= N`.
- Constraint: each node assigned to exactly one station.
- Constraint: `y_{v,s} <= x_s`.
- Objective: minimize weighted distance over all nodes and scenarios.

This can be solved with packages like `scipy.optimize.milp`, `pulp`, or `ortools`.

## Expected Notebook Deliverable

The notebook should likely include:

1. Problem explanation.
2. Population generation.
3. Distance/cost model.
4. Optimization method.
5. Results for a chosen `t`, such as `t = 20`.
6. Visualizations and interpretation.

## Notes For Future Work

- The existing notebook currently only generates and plots population scenarios.
- The station selection optimization still needs to be implemented.
- Since `R*C = 400` and `N = 6`, exhaustive search is not practical.
- Greedy plus local search is a good balance between simplicity and quality.
- If the assignment expects a formal prescriptive analytics model, include the MILP formulation even if the implementation uses a heuristic.
