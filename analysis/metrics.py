from __future__ import annotations

import math

from analysis.stabl_metric import stabl_sensitivity_score


def _percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        raise ValueError("latency list cannot be empty")
    if q < 0 or q > 1:
        raise ValueError("percentile q must be in [0,1]")
    if len(sorted_values) == 1:
        return sorted_values[0]
    idx = q * (len(sorted_values) - 1)
    lo = math.floor(idx)
    hi = math.ceil(idx)
    if lo == hi:
        return sorted_values[lo]
    frac = idx - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def summarize_latencies(
    latencies_ms: list[float], duration_sec: float, total_ops: int, failed_ops: int
) -> dict[str, float | int]:
    if total_ops < 0 or failed_ops < 0 or failed_ops > total_ops:
        raise ValueError("invalid operation counts")
    if duration_sec <= 0:
        raise ValueError("duration_sec must be > 0")

    sorted_lats = sorted(latencies_ms)
    success_ops = total_ops - failed_ops

    if sorted_lats:
        p50 = _percentile(sorted_lats, 0.50)
        p95 = _percentile(sorted_lats, 0.95)
        p99 = _percentile(sorted_lats, 0.99)
    else:
        p50 = p95 = p99 = 0.0

    return {
        "total_ops": total_ops,
        "success_ops": success_ops,
        "failed_ops": failed_ops,
        "failure_rate": (failed_ops / total_ops) if total_ops else 0.0,
        "throughput_ops_per_sec": success_ops / duration_sec,
        "p50_ms": p50,
        "p95_ms": p95,
        "p99_ms": p99,
    }


def _ecdf(values: list[float], x: float) -> float:
    if not values:
        return 0.0
    count = 0
    for v in values:
        if v <= x:
            count += 1
    return count / len(values)


def sensitivity_score(baseline_ms: list[float], fault_ms: list[float], bins: int = 200) -> float:
    if bins <= 0:
        raise ValueError("bins must be > 0")
    return stabl_sensitivity_score(baseline_ms, fault_ms)
