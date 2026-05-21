from statistics import median


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
