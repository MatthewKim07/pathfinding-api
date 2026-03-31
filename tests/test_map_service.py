"""Tests for sample and random map services."""

from app.schemas import AlgorithmChoice, Coordinate, PathRequest, RandomMapRequest
from app.services import generate_random_map, list_sample_maps, solve_path


def test_list_sample_maps_returns_named_maps_with_coordinates() -> None:
    """Sample maps should be available in a stable structured format."""

    response = list_sample_maps()

    assert len(response.maps) >= 3
    assert all(sample.id for sample in response.maps)
    assert all(sample.grid for sample in response.maps)


def test_generate_random_map_respects_shape_and_value_ranges() -> None:
    """Generated maps should match the requested dimensions and allowed values."""

    response = generate_random_map(
        RandomMapRequest(rows=5, cols=7, obstacle_ratio=0.3, max_weight=4, seed=7)
    )

    assert len(response.grid) == 5
    assert all(len(row) == 7 for row in response.grid)
    assert response.start == Coordinate(row=0, col=0)
    assert response.end == Coordinate(row=4, col=6)
    assert all(cell == 0 or 1 <= cell <= 4 for row in response.grid for cell in row)
    assert response.guaranteed_path is True


def test_generate_random_map_is_reproducible_with_a_seed() -> None:
    """Using the same seed should reproduce the same generated map."""

    request = RandomMapRequest(
        rows=6,
        cols=6,
        obstacle_ratio=0.35,
        max_weight=5,
        seed=123,
    )

    first = generate_random_map(request)
    second = generate_random_map(request)

    assert first.grid == second.grid
    assert first.start == second.start
    assert first.end == second.end
    assert first.actual_obstacle_ratio == second.actual_obstacle_ratio


def test_generate_random_map_guarantees_a_valid_path_between_start_and_end() -> None:
    """Generated maps should preserve at least one path from start to end."""

    generated = generate_random_map(
        RandomMapRequest(rows=8, cols=8, obstacle_ratio=0.45, max_weight=9, seed=99)
    )
    result = solve_path(
        PathRequest(
            grid=generated.grid,
            start=generated.start,
            end=generated.end,
            algorithm=AlgorithmChoice.BFS,
        )
    )

    assert result.path_found is True
    assert result.path[0] == generated.start.as_tuple()
    assert result.path[-1] == generated.end.as_tuple()
