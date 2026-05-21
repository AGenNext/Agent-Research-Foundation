import json
from pathlib import Path


class DashboardExporter:
    def export_summary(self, summary, output_dir: str):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        with open(Path(output_dir) / 'dashboard.json', 'w') as f:
            json.dump(summary.model_dump(), f, indent=2)
