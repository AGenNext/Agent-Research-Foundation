from pathlib import Path

import typer

from agent_research.core.runner import BenchmarkRunner

app = typer.Typer()
clear_app = typer.Typer()

app.add_typer(clear_app, name="clear")


@clear_app.command("run")
def run_benchmark(task_path: str, output: str = "outputs"):
    runner = BenchmarkRunner()

    task = runner.load_task(task_path)

    _, evaluation = runner.run_task(task)

    runner.save_result(output, evaluation)

    typer.echo(f"Completed task: {evaluation.task_id}")
    typer.echo(f"Success: {evaluation.success}")
    typer.echo(f"Efficacy: {evaluation.efficacy_score}")
    typer.echo(f"Cost: ${evaluation.estimated_cost_usd}")


@clear_app.command("report")
def generate_report(output: str = "outputs"):
    path = Path(output)

    files = list(path.glob("*.json"))

    typer.echo(f"Found {len(files)} evaluation artifacts")

    for file in files:
        typer.echo(file.name)


if __name__ == "__main__":
    app()
