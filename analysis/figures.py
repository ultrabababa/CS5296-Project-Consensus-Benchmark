#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from analysis.figure_data import ecdf_points, load_latencies_from_runs, radar_rows
from analysis.multi_scenario import load_sensitivity_by_scenario
from analysis.stabl_metric import area_under_ecdf


MULTI_RADAR_LEGEND_ANCHOR = (1.52, 1.20)
MULTI_RADAR_LABEL_PAD = 14


def radar_scenarios() -> list[str]:
    return [
        "leader_kill",
        "delay_120ms",
        "loss_8pct",
        "partition",
        "majority_crash",
        "majority_partition",
    ]




def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * p
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return ordered[lo]
    frac = pos - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def compute_ecdf_x_limit(baseline: list[float], altered: list[float]) -> float:
    values = sorted(float(v) for v in [*baseline, *altered])
    if not values:
        return 1.0
    q1 = _percentile(values, 0.25)
    q3 = _percentile(values, 0.75)
    iqr = max(0.0, q3 - q1)
    whisker = q3 + 3.0 * iqr
    upper = min(max(values), whisker)
    if upper <= 0:
        return 1.0
    return upper * 1.05


def compute_radar_rmax(scores: dict[str, dict[str, float]], scenarios: list[str]) -> float:
    max_v = 0.0
    for system_scores in scores.values():
        for s in scenarios:
            max_v = max(max_v, float(system_scores.get(s, 0.0)))
    if max_v <= 0:
        return 1.0
    return math.ceil(max_v * 1.2 * 10.0) / 10.0


def compute_log_radar_rmax(scores: dict[str, dict[str, float]], scenarios: list[str]) -> float:
    max_log_v = 0.0
    for system_scores in scores.values():
        for s in scenarios:
            raw = float(system_scores.get(s, 0.0))
            log_v = math.log10(1.0 + max(0.0, raw))
            max_log_v = max(max_log_v, log_v)
    if max_log_v <= 0:
        return 1.0
    return math.ceil(max_log_v * 1.1 * 10.0) / 10.0


def fig1_ecdf_with_sensitivity(baseline_dir: Path, altered_dir: Path, out_png: Path, out_csv: Path) -> float:
    baseline = load_latencies_from_runs(baseline_dir)
    altered = load_latencies_from_runs(altered_dir)
    if not baseline or not altered:
        raise ValueError("baseline and altered must both contain latency samples")

    bx, by = ecdf_points(baseline)
    ax, ay = ecdf_points(altered)

    union_x = sorted(set(bx + ax))
    b_yi = np.interp(union_x, bx, by, left=0.0, right=1.0)
    a_yi = np.interp(union_x, ax, ay, left=0.0, right=1.0)

    sensitivity = abs(area_under_ecdf(baseline) - area_under_ecdf(altered))

    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(bx, by, label="baseline", color="#1f77b4", linewidth=2)
    plt.plot(ax, ay, label="altered", color="#9ec1e6", linewidth=2)
    plt.fill_between(union_x, b_yi, a_yi, color="#e6b3b3", alpha=0.7, label="sensitivity")
    plt.xlabel("Latency (ms)")
    plt.ylabel("Proportion")
    plt.ylim(0, 1.05)
    plt.xlim(0.0, compute_ecdf_x_limit(baseline, altered))
    plt.title(f"eCDF Sensitivity (score={sensitivity:.2f})")
    plt.legend(loc="upper center", ncol=3)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["x_ms", "baseline_ecdf", "altered_ecdf", "abs_gap"])
        for x, b, a in zip(union_x, b_yi, a_yi):
            w.writerow([x, b, a, abs(a - b)])

    return sensitivity


def fig2_radar(scores: dict[str, dict[str, float]], out_png: Path, out_csv: Path) -> None:
    systems = sorted(scores.keys())
    scenarios = radar_scenarios()

    rows = radar_rows(scores, systems=systems, scenarios=scenarios)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["system", *scenarios])
        w.writeheader()
        for row in rows:
            w.writerow(row)

    n = len(scenarios)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
    rmax = compute_radar_rmax(scores, scenarios)
    for system in systems:
        vals = [float(scores[system].get(s, 0.0)) for s in scenarios]
        vals += vals[:1]
        ax.plot(angles, vals, linewidth=2, label=system)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(scenarios, fontsize=10)
    ax.tick_params(axis="x", pad=MULTI_RADAR_LABEL_PAD)
    ax.set_ylim(0.0, rmax)
    ax.set_title("Sensitivity by Failure Scenario")
    ax.grid(True)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.15))
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def fig2_radar_multi(scores: dict[str, dict[str, float]], out_png: Path, out_csv: Path) -> None:
    systems = sorted(scores.keys())
    scenarios = radar_scenarios()

    rows = radar_rows(scores, systems=systems, scenarios=scenarios)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["system", *scenarios])
        w.writeheader()
        for row in rows:
            w.writerow(row)

    n = len(scenarios)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
    rmax = compute_log_radar_rmax(scores, scenarios)
    
    # 1. 模仿右图：使用不同的线型、加粗线条，去掉圆点 marker
    linestyles = ['--', '-.', ':', '-']
    for i, system in enumerate(systems):
        vals = [math.log10(1.0 + max(0.0, float(scores[system].get(s, 0.0)))) for s in scenarios]
        vals += vals[:1]
        ax.plot(angles, vals, linewidth=2.5, label=system, linestyle=linestyles[i % len(linestyles)])

    ax.set_xticks(angles[:-1])
    # 2. 增大外围标签字号，并设置 pad 推远距离，防止重叠
    ax.set_xticklabels(scenarios, fontsize=12)
    ax.tick_params(axis="x", pad=30) 

    ax.set_ylim(0.0, rmax)
    ticks = np.linspace(0.0, rmax, 5)
    ax.set_yticks(ticks)
    # 弱化内部网格的刻度数字，避免喧宾夺主
    ax.set_yticklabels([f"{(10**t)-1:.0f}" for t in ticks], fontsize=9, color="gray")

    # 3. 调整标题，增加 pad 使其上移
    ax.set_title("Sensitivity by Failure Scenario (log scale)", pad=40, fontsize=15, fontweight="bold")
    
    # 弱化极坐标外圈的黑色粗线（可选，让它更像右图的清爽风格）
    ax.spines['polar'].set_color('silver')
    ax.grid(True)

    # 4. 调整图例：带边框，增大字号，位置调整到右上角
    ax.legend(
        loc="upper right", 
        bbox_to_anchor=(1.35, 1.15), 
        fontsize=12, 
        frameon=True, 
        borderpad=0.8
    )
    
    out_png.parent.mkdir(parents=True, exist_ok=True)
    
    # 5. 关键：使用 bbox_inches="tight" 确保外部图例和撑开的标签不会被裁切
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close()



def main() -> int:
    parser = argparse.ArgumentParser(description="Generate figure-ready outputs")
    parser.add_argument("--results-root", type=Path, required=True)
    parser.add_argument("--system", type=str, default="etcd")
    parser.add_argument("--fig-dir", type=Path, required=True)
    args = parser.parse_args()

    baseline = args.results_root / args.system / "baseline"
    fault_root = args.results_root / args.system / "fault"

    fig1_png = args.fig_dir / f"{args.system}_fig1_ecdf_leader_kill.png"
    fig1_csv = args.fig_dir / f"{args.system}_fig1_ecdf_leader_kill.csv"
    sensitivity = fig1_ecdf_with_sensitivity(
        baseline_dir=baseline,
        altered_dir=fault_root / "leader_kill",
        out_png=fig1_png,
        out_csv=fig1_csv,
    )

    scenario_scores = load_sensitivity_by_scenario(
        args.results_root / args.system,
        scenarios={
            "leader_kill": "report_leader_kill.json",
            "delay_120ms": "report_delay_120ms.json",
            "loss_8pct": "report_loss_8pct.json",
            "partition": "report_partition.json",
            "majority_crash": "report_majority_crash.json",
            "majority_partition": "report_majority_partition.json",
        },
    )
    score_table = {args.system: scenario_scores}

    fig2_png = args.fig_dir / f"{args.system}_fig2_radar.png"
    fig2_csv = args.fig_dir / f"{args.system}_fig2_radar.csv"
    fig2_radar(score_table, fig2_png, fig2_csv)

    summary = {
        "fig1_sensitivity": sensitivity,
        "fig1_png": str(fig1_png),
        "fig2_png": str(fig2_png),
        "radar_scores": scenario_scores,
    }
    summary_path = args.fig_dir / f"{args.system}_figures_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
