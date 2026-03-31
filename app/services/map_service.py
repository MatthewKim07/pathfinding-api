"""Service-layer logic for sample and generated maps."""

from __future__ import annotations

import numpy as np

from app.data.sample_maps import SAMPLE_MAPS
from app.schemas import (
    Coordinate,
    RandomMapRequest,
    RandomMapResponse,
    SampleMap,
    SampleMapsResponse,
)


def list_sample_maps() -> SampleMapsResponse:
    """Return the predefined sample maps exposed by the API."""

    return SampleMapsResponse(maps=[SampleMap(**sample) for sample in SAMPLE_MAPS])


def generate_random_map(request: RandomMapRequest) -> RandomMapResponse:
    """Generate a reproducible weighted grid with a guaranteed start-to-end path."""

    rng = np.random.default_rng(request.seed)
    start = Coordinate(row=0, col=0)
    end = Coordinate(row=request.rows - 1, col=request.cols - 1)
    grid = rng.integers(
        low=1,
        high=request.max_weight + 1,
        size=(request.rows, request.cols),
        dtype=np.int64,
    )
    obstacle_mask = rng.random((request.rows, request.cols)) < request.obstacle_ratio

    for row, col in _build_guaranteed_path(request.rows, request.cols, rng):
        obstacle_mask[row, col] = False
        grid[row, col] = rng.integers(1, request.max_weight + 1)

    obstacle_mask[start.row, start.col] = False
    obstacle_mask[end.row, end.col] = False
    grid[obstacle_mask] = 0

    actual_obstacle_ratio = float(np.count_nonzero(grid == 0) / grid.size)
    return RandomMapResponse(
        grid=grid.tolist(),
        start=start,
        end=end,
        rows=request.rows,
        cols=request.cols,
        obstacle_ratio=request.obstacle_ratio,
        actual_obstacle_ratio=actual_obstacle_ratio,
        max_weight=request.max_weight,
        seed=request.seed,
        guaranteed_path=True,
    )


def _build_guaranteed_path(
    rows: int, cols: int, rng: np.random.Generator
) -> list[tuple[int, int]]:
    """Carve a monotonic path from the top-left to the bottom-right corner."""

    row = 0
    col = 0
    path = [(row, col)]

    while row < rows - 1 or col < cols - 1:
        can_move_down = row < rows - 1
        can_move_right = col < cols - 1

        if can_move_down and can_move_right:
            if rng.random() < 0.5:
                row += 1
            else:
                col += 1
        elif can_move_down:
            row += 1
        else:
            col += 1

        path.append((row, col))

    return path
