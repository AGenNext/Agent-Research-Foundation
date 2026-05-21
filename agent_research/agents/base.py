from abc import ABC, abstractmethod
from agent_research.core.schemas import BenchmarkTask, AgentResult


class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    def run(self, task: BenchmarkTask) -> AgentResult:
        raise NotImplementedError
