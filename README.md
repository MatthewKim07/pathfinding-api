# Pathfinding & Route Optimization API

A Python backend project for exploring grid-based pathfinding algorithms and route optimization. The API is built with FastAPI and is structured to grow incrementally through algorithm implementations, benchmarking, and testing.

## Current Status

Milestone 1 is complete:

- Project structure scaffolded
- FastAPI application initialized
- Root health/info endpoint added

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the API root and [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

## Test

```bash
pytest
```
