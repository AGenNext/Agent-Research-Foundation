from abc import ABC, abstractmethod

from agent_research.core.schemas import BenchmarkTask, AgentResult, FinalVerdict


class BaseOracle(ABC):
    @abstractmethod
    def evaluate(
        self,
        task: BenchmarkTask,
        result: AgentResult,
    ) -> FinalVerdict:
        raise NotImplementedError
