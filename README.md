# Pathfinding & Route Optimization API

A FastAPI backend for exploring grid-based pathfinding on weighted and unweighted maps. The project implements BFS, Dijkstra, and A* from scratch, exposes them through a clean API, and includes a benchmarking system for comparing runtime, search effort, and success rates across scenarios.

## Overview

This project is built as a backend portfolio piece rather than a single-file algorithm demo. It focuses on:

- correct algorithm implementations
- strict request validation
- thin API routes with a service layer
- reproducible map generation
- benchmark reporting with pandas and CSV export
- comprehensive automated tests

The API is fully local and does not depend on external services.

## Features

### Pathfinding

- `bfs`: shortest path by number of steps on unweighted grids
- `dijkstra`: minimum-cost path on weighted grids
- `astar`: minimum-cost path using a Manhattan-distance heuristic

All algorithms support:

- 4-directional movement
- blocked cells (`0`)
- positive traversal costs
- path reconstruction
- visited-node counts
- runtime measurement in milliseconds

### Maps

- predefined sample maps via `GET /maps/sample`
- seeded random map generation via `POST /maps/random`
- configurable `rows`, `cols`, `obstacle_ratio`, and `max_weight`
- guaranteed path from the returned `start` `(0, 0)` to the returned `end` `(rows - 1, cols - 1)` for generated maps

### Benchmarking

- benchmark multiple maps in one request
- benchmark multiple algorithms in one run
- repeat runs for more stable measurements
- collect raw records into a pandas DataFrame
- export CSV output under `app/data/benchmark_results/`
- return aggregated summaries and readable highlights

## Tech Stack

- Python 3.12+
- FastAPI
- Pydantic
- NumPy
- Pandas
- Uvicorn
- Pytest

## Architecture

The codebase follows a layered structure:

- `app/api/`: FastAPI routes and HTTP concerns
- `app/services/`: orchestration for pathfinding, maps, and benchmarking
- `app/algorithms/`: BFS, Dijkstra, A*, and shared traversal helpers
- `app/schemas/`: request and response models
- `app/data/`: sample maps and benchmark CSV output

Routes stay thin. Algorithm selection, benchmarking, and map generation live outside the API layer, which keeps the code easier to test and extend.

## Project Structure

```text
pathfinding-api/
├── app/
│   ├── algorithms/
│   ├── api/
│   ├── core/
│   ├── data/
│   ├── schemas/
│   └── services/
├── notebooks/
├── tests/
├── README.md
└── requirements.txt
```

## Grid Model

- `0` = blocked cell
- positive integers = traversal cost
- movement is limited to up, down, left, and right
- `start` and `end` must be within bounds and cannot reference blocked cells

Example:

```json
[
  [1, 1, 1, 0],
  [2, 0, 3, 1],
  [1, 1, 1, 1]
]
```

## Algorithms

### BFS

Breadth-first search minimizes the number of steps. It is the right choice for unweighted movement where each move should be treated equally.

- queue-based traversal with `collections.deque`
- deterministic neighbor order
- returns the cost of the chosen path for reporting, but does not optimize by weight

### Dijkstra

Dijkstra minimizes total traversal cost on weighted grids.

- priority queue via `heapq`
- weighted shortest-path guarantee
- ignores stale heap entries after a node has been finalized

### A*

A* also minimizes total traversal cost, but uses a Manhattan-distance heuristic to guide the search.

- priority queue via `heapq`
- `f = g + h`
- Manhattan heuristic aligned with 4-directional movement
- same optimal-cost guarantee as Dijkstra on this grid model

## Setup

### 1. Create and activate a virtual environment

```bash
cd /Users/matthewkim/Documents/GitHub/pathfinding-api
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

### 4. Open the docs

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## Testing

Run the full suite:

```bash
.venv/bin/python -m pytest
```

The current suite includes 48 tests covering:

- algorithm correctness
- invalid input handling
- API behavior
- map generation
- benchmarking workflows

## API Endpoints

### `GET /`

Basic service metadata.

Example response:

```json
{
  "name": "Pathfinding & Route Optimization API",
  "version": "0.1.0",
  "status": "ok"
}
```

### `POST /path`

Runs one pathfinding algorithm on one grid.

Example request:

```json
{
  "grid": [
    [1, 9, 1],
    [1, 9, 1],
    [1, 1, 1]
  ],
  "start": { "row": 0, "col": 0 },
  "end": { "row": 0, "col": 2 },
  "algorithm": "astar"
}
```

Example response:

```json
{
  "algorithm": "astar",
  "path": [
    { "row": 0, "col": 0 },
    { "row": 1, "col": 0 },
    { "row": 2, "col": 0 },
    { "row": 2, "col": 1 },
    { "row": 2, "col": 2 },
    { "row": 1, "col": 2 },
    { "row": 0, "col": 2 }
  ],
  "path_found": true,
  "total_cost": 6,
  "path_length": 6,
  "visited_nodes": 7,
  "runtime_ms": 0.085
}
```

### `GET /maps/sample`

Returns predefined sample maps.

Example response:

```json
{
  "maps": [
    {
      "id": "weighted_corridor",
      "name": "Weighted Corridor",
      "description": "A simple weighted map with a low-cost corridor and blocked cells.",
      "grid": [[1, 4, 0, 1], [1, 1, 1, 1], [0, 3, 0, 1], [1, 1, 1, 1]],
      "start": { "row": 0, "col": 0 },
      "end": { "row": 3, "col": 3 }
    }
  ]
}
```

### `POST /maps/random`

Generates a reproducible weighted map.

Example request:

```json
{
  "rows": 4,
  "cols": 6,
  "obstacle_ratio": 0.25,
  "max_weight": 7,
  "seed": 8
}
```

Example response:

```json
{
  "grid": [
    [7, 0, 2, 7, 2, 3],
    [1, 1, 3, 0, 1, 3],
    [0, 0, 3, 4, 2, 6],
    [4, 0, 0, 2, 0, 4]
  ],
  "start": { "row": 0, "col": 0 },
  "end": { "row": 3, "col": 5 },
  "rows": 4,
  "cols": 6,
  "obstacle_ratio": 0.25,
  "actual_obstacle_ratio": 0.2916666666666667,
  "max_weight": 7,
  "seed": 8,
  "guaranteed_path": true
}
```

### `POST /benchmark`

Runs benchmark comparisons across multiple maps and algorithms.

Example request:

```json
{
  "maps": [
    {
      "name": "detour",
      "grid": [
        [1, 9, 1],
        [1, 9, 1],
        [1, 1, 1]
      ],
      "start": { "row": 0, "col": 0 },
      "end": { "row": 0, "col": 2 }
    },
    {
      "name": "blocked",
      "grid": [
        [1, 0],
        [0, 1]
      ],
      "start": { "row": 0, "col": 0 },
      "end": { "row": 1, "col": 1 }
    }
  ],
  "algorithms": ["bfs", "dijkstra", "astar"],
  "repeat_runs": 1
}
```

Example response excerpt:

```json
{
  "total_runs": 6,
  "summaries": [
    {
      "algorithm": "astar",
      "runs": 2,
      "avg_runtime_ms": 0.013,
      "avg_visited_nodes": 4.0,
      "success_rate": 50.0,
      "avg_path_length": 6.0
    },
    {
      "algorithm": "bfs",
      "runs": 2,
      "avg_runtime_ms": 0.026,
      "avg_visited_nodes": 2.5,
      "success_rate": 50.0,
      "avg_path_length": 2.0
    }
  ],
  "highlights": [
    "Fastest average runtime: astar at 0.013 ms.",
    "Fewest average visited nodes: bfs at 2.5.",
    "Highest success rate: astar at 50.0%."
  ]
}
```

Each benchmark run is also saved to CSV under `app/data/benchmark_results/`.

### `GET /benchmark/sample`

Returns the most recently saved benchmark result, if one exists.

## Benchmarking Notes

Benchmark runs collect:

- algorithm
- map size
- path success
- path length
- total cost
- visited nodes
- runtime in milliseconds

The response is designed to be readable, not just machine-friendly:

- `records` contains the raw per-run data
- `summaries` aggregates metrics per algorithm
- `highlights` surfaces quick comparisons for humans

Because the benchmark service itself is deterministic relative to its inputs, results are reproducible when you use:

- sample maps
- custom fixed maps
- seeded generated maps

## Example Interpretation

Typical patterns you can observe from the benchmark output:

- BFS can appear efficient on step count but return higher path costs on weighted maps.
- Dijkstra guarantees optimal weighted cost but may visit more nodes.
- A* can match Dijkstra’s optimal cost while reducing average runtime or search effort on goal-directed maps.

## Future Work

Potential next steps:

- richer benchmark reporting and notebook analysis
- larger scenario sets for performance profiling
- visualization of paths and explored nodes
- additional heuristics or map-generation strategies
