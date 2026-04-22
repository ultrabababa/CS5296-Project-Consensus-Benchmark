from __future__ import annotations

from bisect import bisect_right
import json
import math
from pathlib import Path


def load_ops_events(run_json: dict[str, object]) -> list[dict[str, float | bool | str]]:
    out: list[dict[str, float | bool | str]] = []
    for row in run_json.get("ops_trace", []):
        if not isinstance(row, dict):
            continue
        submit = float(row.get("submit_time", -1.0))
        end = float(row.get("end_time", -1.0))
        if submit < 0 or end < 0:
            continue
        out.append(
            {
                "submit_time": submit,
                "end_time": end,
                "success": bool(row.get("success", False)),
                "op": str(row.get("op", "")),
            }
        )
    return out


def sliding_tps(
    events: list[dict[str, float | bool | str]],
    window_size: float,
    step_size: float,
    time_key: str = "end_time",
    success_only: bool = True,
) -> tuple[list[float], list[float]]:
    if window_size <= 0 or step_size <= 0:
        raise ValueError("window_size and step_size must be positive")
    if not events:
        return [], []

    all_times = sorted(float(e[time_key]) for e in events if float(e.get(time_key, -1.0)) >= 0)
    if not all_times:
        return [], []

    count_times = all_times
    if success_only:
        count_times = sorted(
            float(e[time_key])
            for e in events
            if bool(e.get("success", False)) and float(e.get(time_key, -1.0)) >= 0
        )
        if not count_times:
            return [], []

    max_t = all_times[-1]
    if max_t < window_size:
        return [], []

    out_t: list[float] = []
    out_v: list[float] = []
    t = window_size
    while t <= max_t + 1e-9:
        left = t - window_size
        left_idx = bisect_right(count_times, left)
        right_idx = bisect_right(count_times, t)
        count = right_idx - left_idx
        out_t.append(round(t, 6))
        out_v.append(count / window_size)
        t += step_size
    return out_t, out_v


def aggregate_dir_series(
    run_dir: Path,
    window_size: float,
    step_size: float,
    time_key: str = "end_time",
    success_only: bool = True,
) -> dict[str, list[float]]:
    runs = sorted(run_dir.glob("run_*.json"))
    if not runs:
        raise ValueError(f"no run_*.json in {run_dir}")

    series: list[tuple[list[float], list[float]]] = []
    for run in runs:
        payload = json.loads(run.read_text(encoding="utf-8"))
        events = load_ops_events(payload)
        t, v = sliding_tps(
            events,
            window_size=window_size,
            step_size=step_size,
            time_key=time_key,
            success_only=success_only,
        )
        if t and v:
            series.append((t, v))

    if not series:
        return {"times": [], "mean_tps": [], "std_tps": []}

    common_times = series[0][0]
    for t, _ in series[1:]:
        common_times = [x for x in common_times if x in set(t)]
    common_times = sorted(common_times)
    if not common_times:
        return {"times": [], "mean_tps": [], "std_tps": []}

    mean_tps: list[float] = []
    std_tps: list[float] = []
    for t in common_times:
        vals = []
        for ts, vs in series:
            idx = ts.index(t)
            vals.append(vs[idx])
        m = sum(vals) / len(vals)
        var = sum((x - m) ** 2 for x in vals) / len(vals)
        mean_tps.append(m)
        std_tps.append(math.sqrt(var))

    return {"times": common_times, "mean_tps": mean_tps, "std_tps": std_tps}
