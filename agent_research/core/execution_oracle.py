from agent_research.core.events import EvaluationEvent, EventType
from agent_research.core.schemas import BenchmarkTask, FinalVerdict
from agent_research.execution.docker_runner import DockerSandboxRunner
from agent_research.execution.workspace import PatchApplier, RepoWorkspace


class ExecutionOracle:
    def __init__(self):
        self.workspace_manager = RepoWorkspace()
        self.patch_applier = PatchApplier()
        self.runner = DockerSandboxRunner()

    def evaluate(
        self,
        task: BenchmarkTask,
        patch_text: str,
        emit_event,
        run_id: str,
        task_id: str,
    ) -> FinalVerdict:
        workspace = self.workspace_manager.prepare(
            repo=task.repo,
            task_id=task.id,
            base_commit=task.base_commit,
        )

        emit_event(
            task.id,
            EvaluationEvent(
                event_type=EventType.TOOL_CALLED,
                run_id=run_id,
                task_id=task_id,
                metadata={
                    "tool": "patch_apply",
                    "workspace": str(workspace),
                },
            ),
        )

        patch_result = self.patch_applier.apply_patch(
            workspace=str(workspace),
            patch_text=patch_text,
        )

        emit_event(
            task.id,
            EvaluationEvent(
                event_type=EventType.TOOL_COMPLETED,
                run_id=run_id,
                task_id=task_id,
                passed=patch_result.returncode == 0,
                metadata={
                    "tool": "patch_apply",
                    "stdout": patch_result.stdout[-2000:],
                    "stderr": patch_result.stderr[-2000:],
                },
            ),
        )

        if patch_result.returncode != 0:
            return FinalVerdict(
                task_id=task.id,
                passed=False,
                score=0.0,
                reason="patch apply failed",
                details={
                    "stderr": patch_result.stderr,
                },
            )

        emit_event(
            task.id,
            EvaluationEvent(
                event_type=EventType.TOOL_CALLED,
                run_id=run_id,
                task_id=task_id,
                metadata={
                    "tool": "docker_test_execution",
                    "command": task.test_command,
                },
            ),
        )

        execution_result = self.runner.run_command(
            command=task.test_command,
            workspace=str(workspace),
            image=task.docker_image,
        )

        passed = execution_result.returncode == 0

        emit_event(
            task.id,
            EvaluationEvent(
                event_type=EventType.TOOL_COMPLETED,
                run_id=run_id,
                task_id=task_id,
                passed=passed,
                metadata={
                    "tool": "docker_test_execution",
                    "stdout": execution_result.stdout[-4000:],
                    "stderr": execution_result.stderr[-4000:],
                    "returncode": execution_result.returncode,
                },
            ),
        )

        return FinalVerdict(
            task_id=task.id,
            passed=passed,
            score=1.0 if passed else 0.0,
            reason="tests passed" if passed else "tests failed",
            details={
                "stdout": execution_result.stdout[-4000:],
                "stderr": execution_result.stderr[-4000:],
                "returncode": execution_result.returncode,
            },
        )
