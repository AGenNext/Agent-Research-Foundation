from pathlib import Path
import json


class RegressionGate:
    def compare(self, baseline_dir: str, candidate_dir: str):
        baseline = self._load_scores(baseline_dir)
        candidate = self._load_scores(candidate_dir)

        return {
            "baseline_success_rate": baseline["success_rate"],
            "candidate_success_rate": candidate["success_rate"],
            "delta": candidate["success_rate"] - baseline["success_rate"],
        }

    def _load_scores(self, path: str):
        files = list(Path(path).glob("*.json"))

        successes = 0

        for file in files:
            with open(file, "r") as f:
                data = json.load(f)
                successes += int(data.get("success", False))

        return {
            "success_rate": successes / max(len(files), 1),
        }
