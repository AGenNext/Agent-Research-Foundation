from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class BenchmarkTask(BaseModel):
    id: str
    domain: str
    title: str
    prompt: str

    expected: Dict[str, Any] = {}
    inputs: Dict[str, Any] = {}
    policy: Dict[str, Any] = {}

    grader: Dict[str, Any] = {"type": "rule_based"}
    oracle: Dict[str, Any] = {"type": "rule_based"}

    sla_seconds: int = 5
    repeats: int = 1

    repo: Optional[str] = None
    base_commit: Optional[str] = None
    docker_image: str = "python:3.11-slim"
    workspace: str = "."
    test_command: Optional[str] = None

    allowed_tools: List[str] = []
    metadata: Dict[str, Any] = {}


class AgentResult(BaseModel):
    task_id: str
    output: str
    latency_seconds: float
    tokens_input: int = 0
    tokens_output: int = 0
    estimated_cost_usd: float = 0.0
    run_index: int = 1


class FinalVerdict(BaseModel):
    task_id: str
    passed: bool
    score: float
    reason: str
    details: Dict[str, Any] = {}


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
    input_ref: Optional[str] = None
    output_ref: Optional[str] = None
    grader_ref: Optional[str] = None
    final_verdict_ref: Optional[str] = None
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
