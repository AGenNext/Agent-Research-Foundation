from agent_research.core.metrics import (
    cost_normalized_accuracy,
    cost_per_success,
    pass_at_k,
    pass_at_k_estimate,
    pass_at_k_by_task,
    reliability_metrics,
    success_variance,
)


def test_cost_normalized_accuracy():
    assert cost_normalized_accuracy(0.8, 0.4) == 200.0


def test_cost_per_success():
    assert cost_per_success(10.0, 5) == 2.0


def test_pass_at_k():
    assert pass_at_k([True, False, True]) == 2 / 3


def test_pass_at_k_estimate_basic():
    # All k samples fail only if every drawn sample is from the failures.
    # n=4, c=1, k=2  ->  1 - C(3,2)/C(4,2) = 1 - 3/6 = 0.5
    assert pass_at_k_estimate(4, 1, 2) == 0.5


def test_pass_at_k_estimate_edges():
    assert pass_at_k_estimate(4, 0, 2) == 0.0          # no successes
    assert pass_at_k_estimate(3, 3, 2) == 1.0          # all succeed
    assert pass_at_k_estimate(2, 1, 5) == 1.0          # k clamped to n; n-c<k
    assert pass_at_k_estimate(0, 0, 1) == 0.0          # no runs


def test_pass_at_k_by_task():
    tasks = {"a": [True, False, False, False], "b": [True, True, True, True]}
    # task a: pass@2 = 0.5 ; task b: pass@2 = 1.0 ; mean = 0.75
    assert pass_at_k_by_task(tasks, 2) == 0.75


def test_success_variance():
    assert success_variance([True, True, True, True]) == 0.0
    assert success_variance([True, False]) == 0.25


def test_reliability_metrics_keys():
    tasks = {"a": [True, False, True], "b": [False, False, False]}
    m = reliability_metrics(tasks)
    assert set(m) == {"pass_at_3", "pass_at_5", "pass_at_8", "success_variance"}
    # task b never succeeds -> its pass@k is 0; mean is pulled below task a's.
    assert 0.0 <= m["pass_at_3"] <= 1.0
