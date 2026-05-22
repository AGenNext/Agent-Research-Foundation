from pathlib import Path

import typer

from agent_research.dashboard import DashboardExporter
from agent_research.core.regression import RegressionGate
from agent_research.core.report import MarkdownReportGenerator
from agent_research.core.runner import BenchmarkRunner
from agent_research.core.summary import SummaryWriter

app = typer.Typer()
clear_app = typer.Typer()

app.add_typer(clear_app, name="clear")


@clear_app.command("run")
def run_benchmark(
    benchmark_dir: str,
    output: str = "outputs",
    repeats: int = 1,
    agent: str = "echo",
):
    runner = BenchmarkRunner(agent_name=agent)

    evaluations = runner.run_benchmark(benchmark_dir, repeats=repeats)

    for evaluation in evaluations:
        runner.save_result(output, evaluation)

    summary = runner.build_summary(evaluations)

    reporter = MarkdownReportGenerator()
    reporter.generate(summary, output)

    dashboard = DashboardExporter()
    dashboard.export_summary(summary, output)

    summary_writer = SummaryWriter()
    summary_writer.write(
        output,
        {
            "run_id": runner.context.run_id,
            "agent_team_id": runner.context.agent_team_id,
            "benchmark_dir": benchmark_dir,
            "repeats": repeats,
            "summary": summary.model_dump(),
            "evaluations": [e.model_dump() for e in evaluations],
        },
    )

    typer.echo("CLEARBench execution complete")
    typer.echo(f"Run ID: {runner.context.run_id}")
    typer.echo(f"Agent: {agent}")
    typer.echo(f"Tasks: {summary.total_tasks}")
    typer.echo(f"Runs: {summary.total_runs}")
    typer.echo(f"Success Rate: {summary.success_rate:.2f}")
    typer.echo(f"CLEAR Score: {summary.clear_score:.2f}")


@clear_app.command("compare")
def compare_runs(baseline: str, candidate: str):
    gate = RegressionGate()

    result = gate.compare(baseline, candidate)

    typer.echo("Comparison complete")
    typer.echo(f"Baseline Success Rate: {result['baseline_success_rate']:.2f}")
    typer.echo(f"Candidate Success Rate: {result['candidate_success_rate']:.2f}")
    typer.echo(f"Delta: {result['delta']:.2f}")


@clear_app.command("gate")
def gate_run(
    baseline: str,
    candidate: str,
    min_delta: float = 0.0,
):
    gate = RegressionGate()

    result = gate.compare(baseline, candidate)

    passed = result["delta"] >= min_delta

    typer.echo(f"Gate Passed: {passed}")

    if not passed:
        raise typer.Exit(code=1)


@clear_app.command("report")
def generate_report(output: str = "outputs"):
    path = Path(output)

    files = list(path.glob("*.json"))

    typer.echo(f"Found {len(files)} evaluation artifacts")

    report_path = path / "report.md"

    if report_path.exists():
        typer.echo(f"Markdown report: {report_path}")

    dashboard_path = path / "dashboard.json"

    if dashboard_path.exists():
        typer.echo(f"Dashboard export: {dashboard_path}")

    summary_path = path / "summary.json"

    if summary_path.exists():
        typer.echo(f"Summary artifact: {summary_path}")

    for file in files:
        typer.echo(file.name)


if __name__ == "__main__":
    app()
