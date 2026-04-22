from __future__ import annotations

import json
from pathlib import Path

from analysis.metrics import sensitivity_score


def aggregate_scenario(dir_path: Path) -> dict[str, object]:
    runs = sorted(dir_path.glob("run_*.json"))
    if not runs:
        raise ValueError(f"no run_*.json files in {dir_path}")

    throughputs = []
    p99s = []
    failure_rates = []
    latencies: list[float] = []

    for run in runs:
        data = json.loads(run.read_text(encoding="utf-8"))
        summary = data["summary"]
        throughputs.append(float(summary["throughput_ops_per_sec"]))
        p99s.append(float(summary["p99_ms"]))
        failure_rates.append(float(summary["failure_rate"]))
        latencies.extend([float(v) for v in data["latencies_ms"]])

    n = len(runs)
    return {
        "runs": n,
        "mean_throughput_ops_per_sec": sum(throughputs) / n,
        "mean_p99_ms": sum(p99s) / n,
        "mean_failure_rate": sum(failure_rates) / n,
        "latencies_ms": latencies,
    }


def compare_baseline_fault(baseline_dir: Path, fault_dir: Path) -> dict[str, float]:
    b = aggregate_scenario(baseline_dir)
    f = aggregate_scenario(fault_dir)

    baseline_throughput = float(b["mean_throughput_ops_per_sec"])
    fault_throughput = float(f["mean_throughput_ops_per_sec"])
    throughput_degradation = (
        (baseline_throughput - fault_throughput) / baseline_throughput if baseline_throughput else 0.0
    )

    baseline_p99 = float(b["mean_p99_ms"])
    fault_p99 = float(f["mean_p99_ms"])

    return {
        "baseline_mean_throughput_ops_per_sec": baseline_throughput,
        "fault_mean_throughput_ops_per_sec": fault_throughput,
        "throughput_degradation_ratio": throughput_degradation,
        "baseline_mean_p99_ms": baseline_p99,
        "fault_mean_p99_ms": fault_p99,
        "baseline_mean_failure_rate": float(b["mean_failure_rate"]),
        "fault_mean_failure_rate": float(f["mean_failure_rate"]),
        "sensitivity_score": sensitivity_score(
            [float(v) for v in b["latencies_ms"]],
            [float(v) for v in f["latencies_ms"]],
        ),
    }
