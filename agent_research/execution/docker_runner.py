import subprocess


class DockerSandboxRunner:
    def run_python(self, script_path: str):
        cmd = [
            "docker",
            "run",
            "--rm",
            "python:3.11-slim",
            "python",
            script_path,
        ]

        return subprocess.run(cmd, capture_output=True, text=True)
