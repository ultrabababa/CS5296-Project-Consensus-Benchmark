#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_DIR="${ROOT_DIR}/results/etcd/baseline"
mkdir -p "${OUT_DIR}"
rm -f "${OUT_DIR}"/run_*.json

python3 "${ROOT_DIR}/scripts/workload/run_etcd_workload.py" --ops 300 --seed 42 --prefix baseline --out "${OUT_DIR}/run_1.json"
python3 "${ROOT_DIR}/scripts/workload/run_etcd_workload.py" --ops 300 --seed 43 --prefix baseline --out "${OUT_DIR}/run_2.json"
python3 "${ROOT_DIR}/scripts/workload/run_etcd_workload.py" --ops 300 --seed 44 --prefix baseline --out "${OUT_DIR}/run_3.json"
