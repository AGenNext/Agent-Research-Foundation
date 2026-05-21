import os
import time

from agent_research.agents.base import BaseAgent
from agent_research.core.schemas import BenchmarkTask, AgentResult


class AnthropicAgent(BaseAgent):
    name = "anthropic"

    def __init__(self, model: str = "claude-3-5-sonnet"):
        self.model = model
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def run(self, task: BenchmarkTask) -> AgentResult:
        start = time.time()

        output = (
            "Anthropic adapter scaffold response. Replace with real API integration."
        )

        latency = time.time() - start

        return AgentResult(
            task_id=task.id,
            output=output,
            latency_seconds=latency,
            tokens_input=420,
            tokens_output=90,
            estimated_cost_usd=0.009,
        )
