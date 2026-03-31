"""Schemas for pathfinding inputs and outputs."""

from __future__ import annotations

from enum import StrEnum

import numpy as np
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    field_validator,
    model_validator,
)


class AlgorithmChoice(StrEnum):
    """Supported pathfinding algorithms exposed by the API."""

    BFS = "bfs"
    DIJKSTRA = "dijkstra"
    ASTAR = "astar"


class Coordinate(BaseModel):
    """A zero-based coordinate on the grid."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    row: StrictInt = Field(ge=0, description="Zero-based row index.")
    col: StrictInt = Field(ge=0, description="Zero-based column index.")

    def as_tuple(self) -> tuple[int, int]:
        """Return the coordinate as a tuple for algorithm implementations."""

        return self.row, self.col


class ServiceInfoResponse(BaseModel):
    """Metadata returned by the service root endpoint."""

    model_config = ConfigDict(extra="forbid")

    name: str
    version: str
    status: str


class GridProblem(BaseModel):
    """Validated grid/start/end payload shared across pathfinding use cases."""

    model_config = ConfigDict(extra="forbid")

    grid: list[list[StrictInt]]
    start: Coordinate
    end: Coordinate

    @field_validator("grid")
    @classmethod
    def validate_grid(cls, grid: list[list[StrictInt]]) -> list[list[StrictInt]]:
        """Ensure the grid is non-empty, rectangular, and contains valid costs."""

        if not grid:
            raise ValueError("Grid must contain at least one row.")

        row_lengths = {len(row) for row in grid}
        if not row_lengths or 0 in row_lengths:
            raise ValueError("Grid rows must contain at least one column.")
        if len(row_lengths) != 1:
            raise ValueError("Grid must be rectangular.")

        for row in grid:
            for cell in row:
                if cell < 0:
                    raise ValueError("Grid values must be 0 or positive integers.")

        return grid

    @model_validator(mode="after")
    def validate_coordinates(self) -> GridProblem:
        """Ensure coordinates are within bounds and point to traversable cells."""

        max_row = len(self.grid)
        max_col = len(self.grid[0])

        for name, coordinate in (("start", self.start), ("end", self.end)):
            if coordinate.row >= max_row or coordinate.col >= max_col:
                raise ValueError(
                    f"{name.capitalize()} coordinate must be within the grid bounds."
                )
            if self.grid[coordinate.row][coordinate.col] == 0:
                raise ValueError(
                    f"{name.capitalize()} coordinate cannot reference a blocked cell."
                )

        return self

    @property
    def shape(self) -> tuple[int, int]:
        """Return the validated grid dimensions."""

        return len(self.grid), len(self.grid[0])

    def to_numpy(self) -> np.ndarray:
        """Convert the validated grid to a NumPy array for algorithm processing."""

        return np.asarray(self.grid, dtype=np.int64)


class PathRequest(GridProblem):
    """Validated input payload for grid-based pathfinding requests."""

    algorithm: AlgorithmChoice


class PathResponse(BaseModel):
    """Structured pathfinding result returned by the API."""

    model_config = ConfigDict(extra="forbid")

    algorithm: AlgorithmChoice
    path: list[Coordinate] = Field(default_factory=list)
    path_found: bool
    total_cost: int | None = Field(
        default=None,
        ge=0,
        description="Total traversal cost for the returned path, if any.",
    )
    path_length: int = Field(ge=0)
    visited_nodes: int = Field(ge=0)
    runtime_ms: float = Field(ge=0)
