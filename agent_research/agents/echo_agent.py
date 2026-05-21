import time
from agent_research.core.schemas import BenchmarkTask, AgentResult


class EchoAgent:
    name = "echo"

    def run(self, task: BenchmarkTask) -> AgentResult:
        start = time.time()

        output = (
            "We cannot approve the refund because the request exceeds the "
            "30-day policy window. We are happy to assist with alternatives."
        )

        latency = time.time() - start

        return AgentResult(
            task_id=task.id,
            output=output,
            latency_seconds=latency,
            tokens_input=300,
            tokens_output=60,
            estimated_cost_usd=0.002,
        )
