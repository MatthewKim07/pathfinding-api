"""Schema validation tests for pathfinding payloads."""

from pydantic import ValidationError
import pytest

from app.schemas import AlgorithmChoice, Coordinate, PathRequest


def test_path_request_accepts_valid_grid_and_coordinates() -> None:
    """A valid payload should be accepted and convertible to NumPy."""

    payload = PathRequest(
        grid=[
            [1, 1, 1, 0],
            [2, 1, 3, 1],
            [1, 1, 1, 1],
        ],
        start=Coordinate(row=0, col=0),
        end=Coordinate(row=2, col=3),
        algorithm=AlgorithmChoice.DIJKSTRA,
    )

    assert payload.shape == (3, 4)
    assert payload.to_numpy().tolist() == [
        [1, 1, 1, 0],
        [2, 1, 3, 1],
        [1, 1, 1, 1],
    ]


def test_path_request_rejects_empty_grid() -> None:
    """The grid must contain at least one row."""

    with pytest.raises(ValidationError, match="Grid must contain at least one row"):
        PathRequest(
            grid=[],
            start=Coordinate(row=0, col=0),
            end=Coordinate(row=0, col=0),
            algorithm=AlgorithmChoice.BFS,
        )


def test_path_request_rejects_non_rectangular_grid() -> None:
    """All rows should have the same width."""

    with pytest.raises(ValidationError, match="Grid must be rectangular"):
        PathRequest(
            grid=[[1, 1], [1]],
            start=Coordinate(row=0, col=0),
            end=Coordinate(row=1, col=0),
            algorithm=AlgorithmChoice.BFS,
        )


def test_path_request_rejects_negative_costs() -> None:
    """Traversal costs must be non-negative."""

    with pytest.raises(
        ValidationError, match="Grid values must be 0 or positive integers"
    ):
        PathRequest(
            grid=[[1, -1], [1, 1]],
            start=Coordinate(row=0, col=0),
            end=Coordinate(row=1, col=1),
            algorithm=AlgorithmChoice.DIJKSTRA,
        )


def test_path_request_rejects_boolean_grid_values() -> None:
    """Boolean values should not be accepted as integer costs."""

    with pytest.raises(ValidationError, match="Input should be a valid integer"):
        PathRequest(
            grid=[[True, 1], [1, 1]],
            start=Coordinate(row=0, col=1),
            end=Coordinate(row=1, col=1),
            algorithm=AlgorithmChoice.ASTAR,
        )


def test_path_request_rejects_out_of_bounds_coordinates() -> None:
    """Coordinates must fall within the validated grid bounds."""

    with pytest.raises(
        ValidationError, match="End coordinate must be within the grid bounds"
    ):
        PathRequest(
            grid=[[1, 1], [1, 1]],
            start=Coordinate(row=0, col=0),
            end=Coordinate(row=3, col=1),
            algorithm=AlgorithmChoice.BFS,
        )


def test_path_request_rejects_blocked_start_coordinate() -> None:
    """Start and end coordinates must reference traversable cells."""

    with pytest.raises(
        ValidationError, match="Start coordinate cannot reference a blocked cell"
    ):
        PathRequest(
            grid=[[0, 1], [1, 1]],
            start=Coordinate(row=0, col=0),
            end=Coordinate(row=1, col=1),
            algorithm=AlgorithmChoice.BFS,
        )
