# Deployment

## Frontend

Frontend lives in `ui/`.

### GitHub Pages

1. Enable GitHub Actions in repository settings.
2. Enable Pages → Source = GitHub Actions.
3. Push to `main`.

Expected URL:

```text
https://agennext.github.io/Agent-Research/
```

## Backend

Backend lives in `backend/`.

### Local

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Docker

```bash
docker compose up
```

### Render

Uses `render.yaml`.

### Railway

Uses `railway.json`.
