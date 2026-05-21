from pydantic import BaseModel
from typing import List, Dict


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
    run_index: int = 1


class EvaluationResult(BaseModel):
    task_id: str
    domain: str
    success: bool
    efficacy_score: float
    policy_adherence_score: float
    latency_seconds: float
    estimated_cost_usd: float
    reliability_pass: bool
    run_index: int = 1
    violations: List[str] = []


class BenchmarkSummary(BaseModel):
    total_runs: int
    total_tasks: int
    success_rate: float
    mean_efficacy: float
    mean_policy_adherence: float
    total_cost_usd: float
    cost_per_success_usd: float
    mean_latency_seconds: float
    p95_latency_seconds: float
    sla_compliance_rate: float
    pass_at_k: float
    clear_score: float
