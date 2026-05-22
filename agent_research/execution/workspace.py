import subprocess
from pathlib import Path


class RepoWorkspace:
    def __init__(self, root: str = "workspaces"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def prepare(self, repo: str, task_id: str, base_commit: str | None = None) -> Path:
        workspace = self.root / task_id

        if workspace.exists():
            subprocess.run(["rm", "-rf", str(workspace)], check=True)

        subprocess.run(["git", "clone", repo, str(workspace)], check=True)

        if base_commit:
            subprocess.run(["git", "checkout", base_commit], cwd=workspace, check=True)

        return workspace


class PatchApplier:
    def apply_patch(self, workspace: str, patch_text: str):
        workspace_path = Path(workspace)
        patch_path = workspace_path / "agent.patch"
        patch_path.write_text(patch_text)

        return subprocess.run(
            ["git", "apply", str(patch_path)],
            cwd=workspace_path,
            capture_output=True,
            text=True,
        )
