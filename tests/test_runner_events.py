from pathlib import Path

from agent_research.core.runner import BenchmarkRunner


def test_runner_creates_trace_events(tmp_path):
    benchmark_dir = tmp_path / 'benchmarks'
    benchmark_dir.mkdir()

    benchmark = benchmark_dir / 'task.yaml'

    benchmark.write_text(
        '''
id: test_task
domain: testing
title: Test task
prompt: hello world
expected:
  must_include:
    - hello
'''
    )

    traces = tmp_path / 'traces'
    artifacts = tmp_path / 'artifacts'

    runner = BenchmarkRunner(
        trace_dir=str(traces),
        artifact_dir=str(artifacts),
    )

    evaluations = runner.run_benchmark(str(benchmark_dir))

    assert len(evaluations) == 1

    trace_file = Path(traces) / 'test_task.jsonl'

    assert trace_file.exists()

    content = trace_file.read_text()

    assert 'task_started' in content
    assert 'agent_started' in content
    assert 'grader_completed' in content
    assert 'task_completed' in content
