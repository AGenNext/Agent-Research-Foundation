import json
from pathlib import Path

import yaml

from agent_research.core.schemas import BenchmarkTask
from agent_research.agents.echo_agent import EchoAgent
from agent_research.verticals.ai_agent_eval.graders import RuleBasedGrader


class BenchmarkRunner:
    def __init__(self):
        self.agent = EchoAgent()
        self.grader = RuleBasedGrader()

    def load_task(self, path: str) -> BenchmarkTask:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return BenchmarkTask(**data)

    def run_task(self, task: BenchmarkTask):
        result = self.agent.run(task)
        evaluation = self.grader.grade(task, result)
        return result, evaluation

    def save_result(self, output_dir: str, evaluation):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        output_path = Path(output_dir) / f"{evaluation.task_id}.json"

        with open(output_path, "w") as f:
            json.dump(evaluation.model_dump(), f, indent=2)
