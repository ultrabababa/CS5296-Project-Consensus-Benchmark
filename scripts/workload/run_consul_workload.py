#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import random
import urllib.request
import sys
import time
from pathlib import Path

import consul

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from analysis.metrics import summarize_latencies

ENDPOINTS = [("127.0.0.1", 18501), ("127.0.0.1", 18502), ("127.0.0.1", 18503)]


def execute_op(clients: list[tuple[str, int]], is_write: bool, key: str, value: str) -> bool:
    all_ok = True
    for host, port in clients:
        try:
            url = f"http://{host}:{port}/v1/kv/{key}"
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy_handler)
            
            if is_write:
                req = urllib.request.Request(url, data=value.encode("utf-8"), method="PUT")
                with opener.open(req, timeout=2.0) as f:
                    if f.read() != b"true":
                        all_ok = False
            else:
                req = urllib.request.Request(url, method="GET")
                with opener.open(req, timeout=2.0) as f:
                    if f.status != 200:
                        all_ok = False
        except Exception:
            all_ok = False
    return all_ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Consul workload (80%% write / 20%% read)")
    parser.add_argument("--ops", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--prefix", type=str, default="bench")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--redundant-copies", type=int, default=1)
    args = parser.parse_args()

    os.environ["NO_PROXY"] = "*"
    random.seed(args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    copies = max(1, min(args.redundant_copies, len(ENDPOINTS)))
    selected = ENDPOINTS[:copies]
    clients = selected

    latencies_ms: list[float] = []
    ops_trace: list[dict[str, float | bool | str]] = []
    failed_ops = 0
    existing_keys: list[str] = []
    started = time.perf_counter()

    for i in range(args.ops):
        is_write = random.random() < 0.8 or not existing_keys
        key = f"{args.prefix}-k-{i}" if is_write else random.choice(existing_keys)
        value = f"v-{i}"
        op_name = "write" if is_write else "read"

        submit = time.perf_counter()
        ok = execute_op(clients, is_write=is_write, key=key, value=value)
        end = time.perf_counter()

        if is_write and ok:
            existing_keys.append(key)
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
