# Pathfinding & Route Optimization API 🚀

A FastAPI backend for grid-based pathfinding with BFS, Dijkstra, and A* implemented from scratch, plus reproducible map generation and benchmark reporting.

## ✨ Highlights

- BFS, Dijkstra, and A* implemented manually with `deque` and `heapq`
- Layered backend structure: API routes, services, algorithms, schemas, and data
- Pandas-based benchmarking with CSV export and summary comparisons
- Seeded random map generation for reproducible experiments
- Strong automated coverage across algorithms, services, and API endpoints

## 🔍 Overview

This project started as an algorithms exercise, but it is built like a backend application rather than a standalone script. The goal is to show solid Python fundamentals, careful API design, clean separation of responsibilities, and measurable algorithm behavior on realistic grid scenarios.

It supports custom pathfinding requests, predefined and generated maps, and comparative benchmarking across multiple algorithms. Everything runs locally with no external services.

## ⚙️ What It Does

### 🧠 Pathfinding

- `bfs` for shortest path by step count
- `dijkstra` for minimum-cost weighted paths
- `astar` for minimum-cost paths guided by Manhattan distance

Each run returns:

- `path`
- `path_found`
- `total_cost`
- `path_length`
- `visited_nodes`
- `runtime_ms`

### 🗺️ Maps

- predefined sample maps via `GET /maps/sample`
- seeded random map generation via `POST /maps/random`
- configurable `rows`, `cols`, `obstacle_ratio`, and `max_weight`
- guaranteed path from `(0, 0)` to `(rows - 1, cols - 1)` for generated maps

### 📊 Benchmarking

- benchmark multiple maps in one request
- benchmark multiple algorithms in the same run
- repeat runs for more stable measurements
- persist raw results to CSV
- return summaries and human-readable highlights

### 🔁 Reproducibility

Benchmarking is deterministic relative to its inputs. Results can be reproduced by:

- reusing the sample maps
- generating maps with a fixed `seed`
- supplying your own fixed benchmark maps

## 🧰 Tech Stack

- Python 3.12+
- FastAPI
- Pydantic
- NumPy
- Pandas
- Uvicorn
- Pytest

## 🏗️ Architecture

The project uses a simple layered structure:

- `app/api/` for HTTP routes and response models
- `app/services/` for orchestration and application logic
- `app/algorithms/` for BFS, Dijkstra, A*, and shared traversal helpers
- `app/schemas/` for request and response validation
- `app/data/` for sample maps and benchmark CSV output

```text
API routes -> services -> algorithms
           -> schemas
           -> data
```

This keeps routes thin and makes the algorithm and benchmarking logic easier to test independently.

## 🗂️ Project Structure

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

## 🧱 Grid Model

- `0` means blocked
- positive integers represent traversal cost
- movement is 4-directional only
- `start` and `end` must be in bounds and on traversable cells

Example grid:

```json
[
  [1, 1, 1, 0],
  [2, 0, 3, 1],
  [1, 1, 1, 1]
]
```

## 🧠 Algorithms

### BFS

Best when every move should count equally. It finds the fewest-step path, not the cheapest weighted path.

### Dijkstra

Best when cell weights matter. It guarantees the minimum total traversal cost.

### A*

Also cost-optimal on this grid model, but uses Manhattan distance to guide the search toward the goal and reduce unnecessary exploration.

## 🚀 Setup

### 1. Create and activate a virtual environment

```bash
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

## 🧪 Testing

Run the full suite:

```bash
.venv/bin/python -m pytest
```

The current suite covers:

- algorithm correctness
- invalid input handling
- map generation
- service-layer behavior
- API responses and validation
- benchmark execution and CSV persistence

## 📡 API Endpoints

### `GET /`

Returns basic service metadata.

```json
{
  "name": "Pathfinding & Route Optimization API",
  "version": "0.1.0",
  "status": "ok"
}
```

### `POST /path`

Runs one algorithm on one grid.

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

Returns predefined sample maps for experimentation.

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

Each run is also exported to CSV under `app/data/benchmark_results/`.

### `GET /benchmark/sample`

Returns the most recently saved benchmark result, if one exists.

## 📈 Benchmarking Notes

Each benchmark record includes:

- algorithm
- map name
- map size
- success/failure
- path length
- total cost
- visited nodes
- runtime in milliseconds

The response is intentionally split into:

- `records` for raw per-run data
- `summaries` for algorithm-level averages
- `highlights` for quick human-readable comparisons

That makes the endpoint useful both for programmatic analysis and for quick inspection.

## 💡 Example Interpretation

The benchmark output makes it easy to spot tradeoffs:

- BFS may return shorter step counts but worse weighted costs
- Dijkstra gives the cheapest path on weighted maps
- A* can match Dijkstra’s optimal cost while exploring more selectively

Those differences are visible in both the raw records and the summary highlights.

## 🔭 Future Work

- richer benchmark analysis in notebooks
- additional heuristics and search strategies
- larger scenario sets for performance profiling
- path and search visualization
