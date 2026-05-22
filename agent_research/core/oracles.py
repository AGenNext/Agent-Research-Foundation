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


class OracleFactory:
    @staticmethod
    def create(config: dict):
        oracle_type = config.get("type", "rule_based")

        if oracle_type == "rule_based":
            return RuleBasedOracle()

        raise ValueError(f"Unsupported oracle type: {oracle_type}")
