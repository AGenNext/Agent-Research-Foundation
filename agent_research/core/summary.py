import json
from pathlib import Path


class SummaryWriter:
    def write(self, output_dir: str, payload: dict):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        path = Path(output_dir) / 'summary.json'

        with open(path, 'w') as f:
            json.dump(payload, f, indent=2)

        return str(path)
