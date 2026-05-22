import subprocess
from pathlib import Path


class DockerSandboxRunner:
    def run_command(
        self,
        command: str,
        workspace: str,
        image: str = "python:3.11-slim",
        timeout_seconds: int = 60,
    ):
        workspace_path = Path(workspace).resolve()

        cmd = [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
            "-v",
            f"{workspace_path}:/workspace",
            "-w",
            "/workspace",
            image,
            "sh",
            "-lc",
            command,
        ]

        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )

    def run_python(self, script_path: str, workspace: str = "."):
        script = Path(script_path).name
        return self.run_command(f"python {script}", workspace=workspace)
