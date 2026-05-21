from pathlib import Path

import typer

from agent_research.core.report import MarkdownReportGenerator
from agent_research.core.runner import BenchmarkRunner

app = typer.Typer()
clear_app = typer.Typer()

app.add_typer(clear_app, name="clear")


@clear_app.command("run")
def run_benchmark(
    benchmark_dir: str,
    output: str = "outputs",
    repeats: int = 1,
):
    runner = BenchmarkRunner()

    evaluations = runner.run_benchmark(benchmark_dir, repeats=repeats)

    for evaluation in evaluations:
        runner.save_result(output, evaluation)

    summary = runner.build_summary(evaluations)

    reporter = MarkdownReportGenerator()
    reporter.generate(summary, output)

    typer.echo("CLEARBench execution complete")
    typer.echo(f"Tasks: {summary.total_tasks}")
    typer.echo(f"Runs: {summary.total_runs}")
    typer.echo(f"Success Rate: {summary.success_rate:.2f}")
    typer.echo(f"CLEAR Score: {summary.clear_score:.2f}")


@clear_app.command("report")
def generate_report(output: str = "outputs"):
    path = Path(output)

    files = list(path.glob("*.json"))

    typer.echo(f"Found {len(files)} evaluation artifacts")

    report_path = path / "report.md"

    if report_path.exists():
        typer.echo(f"Markdown report: {report_path}")

    for file in files:
        typer.echo(file.name)


if __name__ == "__main__":
    app()
