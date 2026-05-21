import json
from pathlib import Path
from datetime import datetime


class TraceCollector:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def append(self, task_id: str, payload: dict):
        payload["timestamp"] = datetime.utcnow().isoformat()

        trace_file = self.output_dir / f"{task_id}.jsonl"

        with open(trace_file, "a") as f:
            f.write(json.dumps(payload) + "\n")
