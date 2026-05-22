from agent_research.core.oracles import CommandOracle
from agent_research.core.schemas import BenchmarkTask, AgentResult


def test_command_oracle_passes():
    oracle = CommandOracle()

    task = BenchmarkTask(
        id="cmd-pass",
        domain="testing",
        title="command test",
        prompt="noop",
        oracle={
            "type": "command",
            "command": "python -c \"print('ok')\"",
        },
    )

    result = AgentResult(
        task_id="cmd-pass",
        output="ok",
        latency_seconds=0.1,
    )

    verdict = oracle.evaluate(task, result)

    assert verdict.passed is True


def test_command_oracle_fails():
    oracle = CommandOracle()

    task = BenchmarkTask(
        id="cmd-fail",
        domain="testing",
        title="command fail",
        prompt="noop",
        oracle={
            "type": "command",
            "command": "python -c \"import sys; sys.exit(1)\"",
        },
    )

    result = AgentResult(
        task_id="cmd-fail",
        output="bad",
        latency_seconds=0.1,
    )

    verdict = oracle.evaluate(task, result)

    assert verdict.passed is False
