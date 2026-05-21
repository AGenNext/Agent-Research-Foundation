import json
from pathlib import Path

import yaml

from agent_research.core.schemas import (
    BenchmarkTask,
    BenchmarkSummary,
)
from agent_research.core.metrics import (
    clear_score,
    cost_per_success,
    p95,
    pass_at_k,
    sla_compliance,
)
from agent_research.core.traces import TraceCollector
from agent_research.agents.factory import create_agent
from agent_research.verticals.ai_agent_eval.graders import RuleBasedGrader


class BenchmarkRunner:
    def __init__(self, agent_name: str = "echo", trace_dir: str = "traces"):
        self.agent = create_agent(agent_name)
        self.grader = RuleBasedGrader()
        self.traces = TraceCollector(trace_dir)

    def load_task(self, path: str) -> BenchmarkTask:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return BenchmarkTask(**data)

    def load_tasks_from_directory(self, directory: str):
        files = Path(directory).glob("*.yaml")
        return [self.load_task(str(file)) for file in files]

    def run_task(self, task: BenchmarkTask, run_index: int = 1):
        result = self.agent.run(task)
        result.run_index = run_index

        self.traces.append(
            task.id,
            {
                "agent": self.agent.name,
                "run_index": run_index,
                "latency_seconds": result.latency_seconds,
                "tokens_input": result.tokens_input,
                "tokens_output": result.tokens_output,
                "estimated_cost_usd": result.estimated_cost_usd,
            },
        )

        evaluation = self.grader.grade(task, result)
        evaluation.domain = task.domain
        evaluation.run_index = run_index

        return result, evaluation

    def run_benchmark(self, benchmark_dir: str, repeats: int = 1):
        tasks = self.load_tasks_from_directory(benchmark_dir)

        evaluations = []

        for task in tasks:
            for run_idx in range(repeats):
                _, evaluation = self.run_task(task, run_idx + 1)
                evaluations.append(evaluation)

        return evaluations

    def build_summary(self, evaluations: list[dict]):
        total_runs = len(evaluations)
        total_tasks = len(set(e.task_id for e in evaluations))

        successes = [e.success for e in evaluations]
        latencies = [e.latency_seconds for e in evaluations]
        costs = [e.estimated_cost_usd for e in evaluations]
        efficacy_scores = [e.efficacy_score for e in evaluations]
        policy_scores = [e.policy_adherence_score for e in evaluations]

        success_rate = sum(successes) / max(total_runs, 1)
        total_cost = sum(costs)

        summary = BenchmarkSummary(
            total_runs=total_runs,
            total_tasks=total_tasks,
            success_rate=success_rate,
            mean_efficacy=sum(efficacy_scores) / max(len(efficacy_scores), 1),
            mean_policy_adherence=sum(policy_scores) / max(len(policy_scores), 1),
            total_cost_usd=total_cost,
            cost_per_success_usd=cost_per_success(total_cost, sum(successes)),
            mean_latency_seconds=sum(latencies) / max(len(latencies), 1),
            p95_latency_seconds=p95(latencies),
            sla_compliance_rate=sla_compliance(latencies, 3),
            pass_at_k=pass_at_k(successes),
            clear_score=clear_score(
                cost_score=max(0.0, 1.0 - total_cost),
                latency_score=max(0.0, 1.0 - (sum(latencies) / max(len(latencies), 1))),
                efficacy_score=sum(efficacy_scores) / max(len(efficacy_scores), 1),
                assurance_score=sum(policy_scores) / max(len(policy_scores), 1),
                reliability_score=pass_at_k(successes),
            ),
        )

        return summary

    def save_result(self, output_dir: str, evaluation):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        output_path = (
            Path(output_dir)
            / f"{evaluation.task_id}_run_{evaluation.run_index}.json"
        )

        with open(output_path, "w") as f:
            json.dump(evaluation.model_dump(), f, indent=2)
