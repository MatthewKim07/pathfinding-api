"""Schemas for sample and generated map payloads."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, StrictInt

from app.schemas.pathfinding import Coordinate


class SampleMap(BaseModel):
    """A predefined map returned by the sample maps endpoint."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    description: str
    grid: list[list[int]]
    start: Coordinate
    end: Coordinate


class SampleMapsResponse(BaseModel):
    """Collection of sample maps available to API consumers."""

    model_config = ConfigDict(extra="forbid")

    maps: list[SampleMap]


class RandomMapRequest(BaseModel):
    """Input payload for generating reproducible random maps."""

    model_config = ConfigDict(extra="forbid")

    rows: StrictInt = Field(gt=0, le=200)
    cols: StrictInt = Field(gt=0, le=200)
    obstacle_ratio: float = Field(ge=0.0, lt=1.0)
    max_weight: StrictInt = Field(ge=1, le=100)
    seed: StrictInt | None = None


class RandomMapResponse(BaseModel):
    """Generated map payload returned by the random maps endpoint."""

    model_config = ConfigDict(extra="forbid")

    grid: list[list[int]]
    start: Coordinate
    end: Coordinate
    rows: int
    cols: int
    obstacle_ratio: float
    actual_obstacle_ratio: float
    max_weight: int
    seed: int | None
    guaranteed_path: bool
