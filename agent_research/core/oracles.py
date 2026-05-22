import subprocess

from agent_research.core.schemas import BenchmarkTask, AgentResult, FinalVerdict


class RuleBasedOracle:
    def evaluate(self, task: BenchmarkTask, result: AgentResult) -> FinalVerdict:
        output = result.output.lower()
        must_include = task.expected.get("must_include", [])
        missing = [item for item in must_include if item.lower() not in output]
        score = 1.0 - (len(missing) / max(len(must_include), 1))
        passed = len(missing) == 0

        return FinalVerdict(
            task_id=task.id,
            passed=passed,
            score=score,
            reason="passed" if passed else "missing required output elements",
            details={"missing": missing},
        )


class CommandOracle:
    def evaluate(self, task: BenchmarkTask, result: AgentResult) -> FinalVerdict:
        command = task.oracle.get("command")
        timeout = task.oracle.get("timeout_seconds", 30)

        if not command:
            return FinalVerdict(
                task_id=task.id,
                passed=False,
                score=0.0,
                reason="missing oracle command",
                details={},
            )

        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        passed = completed.returncode == 0

        return FinalVerdict(
            task_id=task.id,
            passed=passed,
            score=1.0 if passed else 0.0,
            reason="command passed" if passed else "command failed",
            details={
                "command": command,
                "returncode": completed.returncode,
                "stdout": completed.stdout[-4000:],
                "stderr": completed.stderr[-4000:],
            },
        )


class OracleFactory:
    @staticmethod
    def create(config: dict):
        oracle_type = config.get("type", "rule_based")

        if oracle_type == "rule_based":
            return RuleBasedOracle()

        if oracle_type == "command":
            return CommandOracle()

        raise ValueError(f"Unsupported oracle type: {oracle_type}")
