#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from analysis.metrics import summarize_latencies

ENDPOINTS = ["http://etcd1:2379", "http://etcd2:2379", "http://etcd3:2379"]


def run_etcdctl(endpoint: str, args: list[str]) -> subprocess.CompletedProcess[str]:
    cmd = [
        "docker",
        "exec",
        "etcd1",
        "etcdctl",
        f"--endpoints={endpoint}",
        "--dial-timeout=1s",
        "--command-timeout=1s",
        *args,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def execute_op(args: list[str], redundant_copies: int) -> bool:
    copies = max(1, min(redundant_copies, len(ENDPOINTS)))
    selected = ENDPOINTS[:copies]

    all_ok = True
    for endpoint in selected:
        res = run_etcdctl(endpoint, args)
        if res.returncode != 0:
            all_ok = False
    return all_ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Run etcd workload (80%% write / 20%% read)")
    parser.add_argument("--ops", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--prefix", type=str, default="bench")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--redundant-copies", type=int, default=1)
    args = parser.parse_args()

    random.seed(args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    latencies_ms: list[float] = []
    ops_trace: list[dict[str, float | bool | str]] = []
    failed_ops = 0

    existing_keys: list[str] = []
    started = time.perf_counter()

    for i in range(args.ops):
        is_write = random.random() < 0.8 or not existing_keys

        if is_write:
            key = f"{args.prefix}-k-{i}"
            value = f"v-{i}"
            op_name = "write"
            submit = time.perf_counter()
            ok = execute_op(["put", key, value], args.redundant_copies)
            end = time.perf_counter()
            if ok:
                existing_keys.append(key)
            else:
                failed_ops += 1
        else:
            key = random.choice(existing_keys)
            op_name = "read"
            submit = time.perf_counter()
            ok = execute_op(["get", key], args.redundant_copies)
            end = time.perf_counter()
            if not ok:
                failed_ops += 1

        latency_ms = (end - submit) * 1000.0
        ops_trace.append(
            {
                "submit_time": submit - started,
                "end_time": end - started,
                "success": ok,
                "op": op_name,
            }
        )

        if ok:
            latencies_ms.append(latency_ms)

    duration = time.perf_counter() - started
    summary = summarize_latencies(
        latencies_ms=latencies_ms,
        duration_sec=duration,
        total_ops=args.ops,
        failed_ops=failed_ops,
    )
    summary["mode"] = "80_write_20_read"
    summary["redundant_copies"] = args.redundant_copies

    with args.out.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "summary": summary,
                "latencies_ms": latencies_ms,
                "ops_trace": ops_trace,
            },
            f,
            indent=2,
        )

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
