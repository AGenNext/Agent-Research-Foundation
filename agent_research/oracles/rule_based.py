from agent_research.core.schemas import BenchmarkTask, AgentResult, FinalVerdict
from agent_research.oracles.base import BaseOracle


class RuleBasedOracle(BaseOracle):
    def evaluate(self, task: BenchmarkTask, result: AgentResult):
        expected = task.expected.get("must_include", [])

        missing = []

        for item in expected:
            if item.lower() not in result.output.lower():
                missing.append(item)

        passed = len(missing) == 0

        return FinalVerdict(
            task_id=task.id,
            passed=passed,
            score=1.0 if passed else 0.0,
            reason="passed" if passed else "missing required outputs",
            details={"missing": missing},
        )
