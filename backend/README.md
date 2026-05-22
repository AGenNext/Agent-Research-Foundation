# CLEARBench Backend

Minimal FastAPI backend for CLEARBench demo and future agent evaluation APIs.

## Run locally

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /` → service metadata
- `GET /health` → health check
- `GET /api/demo` → demo CLEARBench data

## Planned expansion

- live evaluation runs
- Docker execution oracles
- artifact persistence
- benchmark APIs
- websocket streaming
- run history
