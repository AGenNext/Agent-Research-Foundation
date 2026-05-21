import json
from pathlib import Path
from uuid import uuid4


class ArtifactStore:
    def __init__(self, root: str = "artifacts"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write_text(self, content: str, suffix: str = ".txt") -> str:
        artifact_id = str(uuid4())
        path = self.root / f"{artifact_id}{suffix}"

        with open(path, "w") as f:
            f.write(content)

        return str(path)

    def write_json(self, payload: dict) -> str:
        artifact_id = str(uuid4())
        path = self.root / f"{artifact_id}.json"

        with open(path, "w") as f:
            json.dump(payload, f, indent=2)

        return str(path)
