from pathlib import Path
from agent_research.core.schemas import BenchmarkSummary


class MarkdownReportGenerator:
    def generate(self, summary: BenchmarkSummary, output_dir: str):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        report = f'''# CLEARBench Report

## Summary

- Total Tasks: {summary.total_tasks}
- Total Runs: {summary.total_runs}
- Success Rate: {summary.success_rate:.2f}
- Mean Efficacy: {summary.mean_efficacy:.2f}
- Mean Policy Adherence: {summary.mean_policy_adherence:.2f}
- Total Cost (USD): {summary.total_cost_usd:.4f}
- Cost Per Success (USD): {summary.cost_per_success_usd:.4f}
- Mean Latency (s): {summary.mean_latency_seconds:.4f}
- P95 Latency (s): {summary.p95_latency_seconds:.4f}
- SLA Compliance: {summary.sla_compliance_rate:.2f}
- Mean Success (pass@k): {summary.pass_at_k:.2f}
- pass@3 / pass@5 / pass@8: {summary.pass_at_3:.2f} / {summary.pass_at_5:.2f} / {summary.pass_at_8:.2f}
- Success Variance: {summary.success_variance:.4f}
- CLEAR Score: {summary.clear_score:.2f}
'''

        output_path = Path(output_dir) / 'report.md'

        with open(output_path, 'w') as f:
            f.write(report)
