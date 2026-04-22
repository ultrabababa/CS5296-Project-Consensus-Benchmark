from __future__ import annotations

import json
from pathlib import Path


def ecdf_points(latencies_ms: list[float]) -> tuple[list[float], list[float]]:
    values = sorted(float(v) for v in latencies_ms)
    if not values:
        return [], []
    n = len(values)
    ys = [(i + 1) / n for i in range(n)]
    return values, ys


def load_latencies_from_runs(run_dir: Path) -> list[float]:
    runs = sorted(run_dir.glob("run_*.json"))
    all_values: list[float] = []
    for run in runs:
        data = json.loads(run.read_text(encoding="utf-8"))
        all_values.extend(float(v) for v in data.get("latencies_ms", []))
    return all_values


def radar_rows(
    score_table: dict[str, dict[str, float]], systems: list[str], scenarios: list[str]
) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for system in systems:
        row: dict[str, float | str] = {"system": system}
        for scenario in scenarios:
            row[scenario] = float(score_table.get(system, {}).get(scenario, 0.0))
        rows.append(row)
    return rows
