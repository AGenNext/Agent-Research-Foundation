from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CLEARBench Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sample_data = {
    "agentNodes": [
        {
            "id": "planner",
            "label": "Planner Agent",
            "score": 0.86,
            "trustScore": 0.82,
            "status": "passed"
        },
        {
            "id": "coder",
            "label": "Coder Agent",
            "score": 0.52,
            "trustScore": 0.61,
            "status": "warning"
        }
    ],
    "executionLogs": [
        {
            "id": "log-1",
            "type": "agent",
            "message": "Planner created implementation plan",
            "score": 0.86
        }
    ]
}

@app.get("/")
def root():
    return {
        "name": "CLEARBench Backend",
        "status": "ok",
        "version": "0.1.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/demo")
def demo_data():
    return sample_data
