import os
import time

from agent_research.agents.base import BaseAgent
from agent_research.core.schemas import BenchmarkTask, AgentResult


class OpenAIAgent(BaseAgent):
    name = "openai"

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

    def run(self, task: BenchmarkTask) -> AgentResult:
        start = time.time()

        output = (
            "OpenAI adapter scaffold response. Replace with real API integration."
        )

        latency = time.time() - start

        return AgentResult(
            task_id=task.id,
            output=output,
            latency_seconds=latency,
            tokens_input=500,
            tokens_output=120,
            estimated_cost_usd=0.01,
        )
