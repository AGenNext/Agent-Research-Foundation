import json
from pathlib import Path
from uuid import uuid4

import yaml

from agent_research.core.schemas import (
    BenchmarkTask,
    BenchmarkSummary,
    FinalVerdict,
)
from agent_research.core.metrics import (
    clear_score,
    cost_per_success,
    p95,
    pass_at_k,
    reliability_metrics,
    sla_compliance,
)
from agent_research.core.artifacts import ArtifactStore
from agent_research.core.events import EvaluationEvent, EventType
from agent_research.core.oracles import OracleFactory
from agent_research.core.run_context import RunContext
from agent_research.core.traces import TraceCollector
from agent_research.agents.factory import create_agent
from agent_research.verticals.ai_agent_eval.graders import RuleBasedGrader


class BenchmarkRunner:
    def __init__(
        self,
        agent_name: str = "echo",
        trace_dir: str = "traces",
        artifact_dir: str = "artifacts",
    ):
        self.agent = create_agent(agent_name)
        self.grader = RuleBasedGrader()
        self.traces = TraceCollector(trace_dir)
        self.artifacts = ArtifactStore(artifact_dir)
        self.context = RunContext(agent_team_id=agent_name)

    def emit(self, task_id: str, event: EvaluationEvent):
        self.traces.append(task_id, event)

    def load_task(self, path: str) -> BenchmarkTask:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return BenchmarkTask(**data)

    def load_tasks_from_directory(self, directory: str):
        files = Path(directory).glob("*.yaml")
        return [self.load_task(str(file)) for file in files]

    def evaluate_with_oracle(self, task: BenchmarkTask, result, attempt_id: str):
        oracle = OracleFactory.create(task.oracle)

        try:
            if task.oracle.get("type") == "execution":
                return oracle.evaluate(
                    task=task,
                    patch_text=result.output,
                    emit_event=self.emit,
                    run_id=self.context.run_id,
                    task_id=task.id,
                )

            return oracle.evaluate(task, result)

        except Exception as exc:
            self.emit(
                task.id,
                EvaluationEvent(
                    event_type=EventType.ERROR,
                    run_id=self.context.run_id,
                    task_id=task.id,
                    attempt_id=attempt_id,
                    metadata={
                        "phase": "oracle_evaluation",
                        "error": str(exc),
                    },
                ),
            )

            return FinalVerdict(
                task_id=task.id,
                passed=False,
                score=0.0,
                reason="oracle error",
                details={"error": str(exc)},
            )

    def run_task(self, task: BenchmarkTask, run_index: int = 1):
        attempt_id = str(uuid4())

        self.emit(
            task.id,
            EvaluationEvent(
                event_type=EventType.TASK_STARTED,
                run_id=self.context.run_id,
                task_id=task.id,
                attempt_id=attempt_id,
                metadata={"run_index": run_index},
            ),
        )

        prompt_ref = self.artifacts.write_text(task.prompt)

        self.emit(
            task.id,
            EvaluationEvent(
                event_type=EventType.AGENT_STARTED,
                run_id=self.context.run_id,
                task_id=task.id,
                attempt_id=attempt_id,
                agent_id=self.agent.name,
                input_ref=prompt_ref,
            ),
        )

        result = self.agent.run(task)
        result.run_index = run_index

        output_ref = self.artifacts.write_text(result.output)

        self.emit(
            task.id,
            EvaluationEvent(
                event_type=EventType.AGENT_COMPLETED,
                run_id=self.context.run_id,
                task_id=task.id,
                attempt_id=attempt_id,
                agent_id=self.agent.name,
                output_ref=output_ref,
                latency_ms=result.latency_seconds * 1000,
                cost_usd=result.estimated_cost_usd,
                tokens_input=result.tokens_input,
                tokens_output=result.tokens_output,
            ),
        )

        self.emit(
            task.id,
            EvaluationEvent(
                event_type=EventType.GRADER_STARTED,
                run_id=self.context.run_id,
                task_id=task.id,
                attempt_id=attempt_id,
            ),
        )

        evaluation = self.grader.grade(task, result)
        evaluation.domain = task.domain
        evaluation.run_index = run_index
        evaluation.input_ref = prompt_ref
        evaluation.output_ref = output_ref

        grader_ref = self.artifacts.write_json(evaluation.model_dump())
        evaluation.grader_ref = grader_ref

        self.emit(
            task.id,
            EvaluationEvent(
                event_type=EventType.GRADER_COMPLETED,
                run_id=self.context.run_id,
                task_id=task.id,
                attempt_id=attempt_id,
                value_ref=grader_ref,
                score=evaluation.efficacy_score,
                passed=evaluation.success,
            ),
        )

        verdict = self.evaluate_with_oracle(task, result, attempt_id)

        verdict_ref = self.artifacts.write_json(verdict.model_dump())
        evaluation.final_verdict_ref = verdict_ref
        evaluation.success = verdict.passed
        evaluation.efficacy_score = verdict.score
        evaluation.reliability_pass = verdict.passed

        self.emit(
            task.id,
            EvaluationEvent(
                event_type=EventType.TASK_COMPLETED,
                run_id=self.context.run_id,
                task_id=task.id,
                attempt_id=attempt_id,
                value_ref=verdict_ref,
                score=verdict.score,
                passed=verdict.passed,
                metadata={"reason": verdict.reason},
            ),
        )

        return result, evaluation

    def run_benchmark(self, benchmark_dir: str, repeats: int = 1):
        tasks = self.load_tasks_from_directory(benchmark_dir)

        evaluations = []

        self.emit(
            "benchmark",
            EvaluationEvent(
                event_type=EventType.RUN_STARTED,
                run_id=self.context.run_id,
                metadata={
                    "benchmark_dir": benchmark_dir,
                    "repeats": repeats,
                },
            ),
        )

        for task in tasks:
            for run_idx in range(repeats):
                _, evaluation = self.run_task(task, run_idx + 1)
                evaluations.append(evaluation)

        self.emit(
            "benchmark",
            EvaluationEvent(
                event_type=EventType.RUN_COMPLETED,
                run_id=self.context.run_id,
                metadata={"total_evaluations": len(evaluations)},
            ),
        )

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

        task_successes: dict[str, list[bool]] = {}
        for e in evaluations:
            task_successes.setdefault(e.task_id, []).append(e.success)
        reliability = reliability_metrics(task_successes)

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
            pass_at_3=reliability["pass_at_3"],
            pass_at_5=reliability["pass_at_5"],
            pass_at_8=reliability["pass_at_8"],
            success_variance=reliability["success_variance"],
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
