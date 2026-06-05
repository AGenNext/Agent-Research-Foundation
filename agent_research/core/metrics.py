from math import comb
from statistics import median, pvariance


DEFAULT_CLEAR_WEIGHTS = {
    "cost": 0.20,
    "latency": 0.20,
    "efficacy": 0.25,
    "assurance": 0.20,
    "reliability": 0.15,
}


def cost_normalized_accuracy(efficacy: float, cost: float) -> float:
    if cost <= 0:
        return efficacy * 100
    return (efficacy / cost) * 100


def cost_per_success(total_cost: float, successful_tasks: int) -> float:
    if successful_tasks == 0:
        return total_cost
    return total_cost / successful_tasks


def sla_compliance(latencies: list[float], sla_seconds: float) -> float:
    if not latencies:
        return 0.0
    passed = [x for x in latencies if x <= sla_seconds]
    return len(passed) / len(latencies)


def pass_at_k(results: list[bool]) -> float:
    """Mean success rate over a flat list of runs.

    NOTE: this is the simple repeated-run success rate, not the unbiased
    "at least one of k succeeds" estimator. Use ``pass_at_k_estimate`` /
    ``pass_at_k_by_task`` for true pass@k.
    """
    if not results:
        return 0.0
    return sum(results) / len(results)


def pass_at_k_estimate(n: int, c: int, k: int) -> float:
    """Unbiased estimator of pass@k for a single task.

    Probability that at least one of ``k`` samples drawn (without replacement)
    from ``n`` total runs — of which ``c`` succeeded — is a success. This is the
    estimator from Chen et al. (HumanEval, 2021):

        pass@k = 1 - C(n - c, k) / C(n, k)

    ``k`` is clamped to ``n`` when fewer than ``k`` runs are available.
    """
    if n <= 0 or k <= 0 or c <= 0:
        return 0.0
    k = min(k, n)
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


def pass_at_k_by_task(task_successes: dict[str, list[bool]], k: int) -> float:
    """Mean unbiased pass@k across tasks, each with its own repeated runs."""
    if not task_successes:
        return 0.0
    estimates = [
        pass_at_k_estimate(len(results), sum(bool(r) for r in results), k)
        for results in task_successes.values()
    ]
    return sum(estimates) / len(estimates)


def success_variance(results: list[bool]) -> float:
    """Population variance of run successes (1.0/0.0), a stability signal."""
    if not results:
        return 0.0
    return pvariance([1.0 if r else 0.0 for r in results])


def reliability_metrics(
    task_successes: dict[str, list[bool]],
    ks: tuple[int, ...] = (3, 5, 8),
) -> dict[str, float]:
    """True pass@k for each k plus overall success variance.

    Returns keys ``pass_at_{k}`` for each requested ``k`` and
    ``success_variance`` over all runs (flattened across tasks).
    """
    flat = [r for results in task_successes.values() for r in results]
    metrics = {f"pass_at_{k}": pass_at_k_by_task(task_successes, k) for k in ks}
    metrics["success_variance"] = success_variance(flat)
    return metrics


def p50(values: list[float]) -> float:
    if not values:
        return 0.0
    return median(values)


def p95(values: list[float]) -> float:
    if not values:
        return 0.0

    ordered = sorted(values)
    idx = int(len(ordered) * 0.95) - 1
    idx = max(idx, 0)

    return ordered[idx]


def clear_score(
    cost_score: float,
    latency_score: float,
    efficacy_score: float,
    assurance_score: float,
    reliability_score: float,
    weights: dict | None = None,
) -> float:
    weights = weights or DEFAULT_CLEAR_WEIGHTS

    return (
        weights["cost"] * cost_score
        + weights["latency"] * latency_score
        + weights["efficacy"] * efficacy_score
        + weights["assurance"] * assurance_score
        + weights["reliability"] * reliability_score
    )
