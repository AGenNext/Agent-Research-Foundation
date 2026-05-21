from pydantic import BaseModel
from typing import List, Dict, Optional


class BenchmarkTask(BaseModel):
    id: str
    domain: str
    title: str
    prompt: str
    expected: Dict
    sla_seconds: int = 5
    policy: Dict = {}


class AgentResult(BaseModel):
    task_id: str
    output: str
    latency_seconds: float
    tokens_input: int = 0
    tokens_output: int = 0
    estimated_cost_usd: float = 0.0


class EvaluationResult(BaseModel):
    task_id: str
    success: bool
    efficacy_score: float
    policy_adherence_score: float
    latency_seconds: float
    estimated_cost_usd: float
    reliability_pass: bool
    violations: List[str] = []
