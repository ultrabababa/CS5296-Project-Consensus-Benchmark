from __future__ import annotations

import math


def area_under_ecdf(
    latencies_ms: list[float], lower_bound: float = 0.0, upper_bound: float | None = None
) -> float:
    if not latencies_ms:
        return 0.0
    values = sorted(float(v) for v in latencies_ms)
    if upper_bound is None:
        upper_bound = values[-1]
    if upper_bound < values[0]:
        return 0.0

    n = len(values)
    area = 0.0
    prev_x = min(lower_bound, values[0])
    prev_f = 0.0
    for i, x in enumerate(values, start=1):
        if x > upper_bound:
            break
        area += (x - prev_x) * prev_f
        prev_x = x
        prev_f = i / n

    if upper_bound > prev_x:
        area += (upper_bound - prev_x) * prev_f
    return area


def stabl_sensitivity_score(baseline_ms: list[float], altered_ms: list[float]) -> float:
    if not baseline_ms:
        return 0.0
    if not altered_ms:
        return math.inf

    lower = min(min(baseline_ms), min(altered_ms), 0.0)
    upper = max(max(baseline_ms), max(altered_ms))
    b_area = area_under_ecdf(baseline_ms, lower_bound=lower, upper_bound=upper)
    a_area = area_under_ecdf(altered_ms, lower_bound=lower, upper_bound=upper)
    return abs(b_area - a_area)
