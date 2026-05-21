from agent_research.core.metrics import (
    cost_normalized_accuracy,
    cost_per_success,
    pass_at_k,
)


def test_cost_normalized_accuracy():
    assert cost_normalized_accuracy(0.8, 0.4) == 200.0


def test_cost_per_success():
    assert cost_per_success(10.0, 5) == 2.0


def test_pass_at_k():
    assert pass_at_k([True, False, True]) == 2 / 3
