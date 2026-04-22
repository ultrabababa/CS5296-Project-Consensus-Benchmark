from __future__ import annotations

from pathlib import Path

from analysis.ops_timeseries import aggregate_dir_series


def _empty_series() -> dict[str, list[float]]:
    return {"times": [], "mean_tps": [], "std_tps": []}


def build_ops_series(
    results_root: Path,
    system: str,
    scenarios: list[str],
    window_size: float = 5.0,
    step_size: float = 1.0,
) -> dict[str, dict[str, list[float]]]:
    base_dir = results_root / system / "baseline"
    out: dict[str, dict[str, list[float]]] = {}

    out["baseline"] = aggregate_dir_series(
        base_dir,
        window_size=window_size,
        step_size=step_size,
        time_key="end_time",
        success_only=True,
    )

    for scenario in scenarios:
        scenario_dir = results_root / system / "fault" / scenario
        if not scenario_dir.exists():
            out[scenario] = _empty_series()
            continue
        try:
            out[scenario] = aggregate_dir_series(
                scenario_dir,
                window_size=window_size,
                step_size=step_size,
                time_key="end_time",
                success_only=True,
            )
        except ValueError:
            out[scenario] = _empty_series()

    return out
