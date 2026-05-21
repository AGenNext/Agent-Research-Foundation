from statistics import median


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
    if not results:
        return 0.0
    return sum(results) / len(results)


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
