"""Predefined sample maps exposed by the API."""

from __future__ import annotations

SAMPLE_MAPS = [
    {
        "id": "weighted_corridor",
        "name": "Weighted Corridor",
        "description": "A simple weighted map with a low-cost corridor and blocked cells.",
        "grid": [
            [1, 4, 0, 1],
            [1, 1, 1, 1],
            [0, 3, 0, 1],
            [1, 1, 1, 1],
        ],
        "start": {"row": 0, "col": 0},
        "end": {"row": 3, "col": 3},
    },
    {
        "id": "detour_weights",
        "name": "Detour Weights",
        "description": "A map where the cheapest weighted path is longer than the shortest-step path.",
        "grid": [
            [1, 9, 1],
            [1, 9, 1],
            [1, 1, 1],
        ],
        "start": {"row": 0, "col": 0},
        "end": {"row": 0, "col": 2},
    },
    {
        "id": "open_field",
        "name": "Open Field",
        "description": "A small open grid useful for comparing search behavior across algorithms.",
        "grid": [
            [1, 1, 1, 1],
            [1, 2, 2, 1],
            [1, 1, 1, 1],
        ],
        "start": {"row": 0, "col": 0},
        "end": {"row": 2, "col": 3},
    },
]
