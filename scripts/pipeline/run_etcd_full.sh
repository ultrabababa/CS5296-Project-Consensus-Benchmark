#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

"${ROOT_DIR}/scripts/cluster/up.sh"
sleep 8
"${ROOT_DIR}/scripts/cluster/health.sh"

"${ROOT_DIR}/scripts/workload/run_baseline.sh"
"${ROOT_DIR}/scripts/fault/run_fault_experiments.sh"

python3 "${ROOT_DIR}/analysis/report.py" \
  --baseline "${ROOT_DIR}/results/etcd/baseline" \
  --fault "${ROOT_DIR}/results/etcd/fault/leader_kill" \
  --out "${ROOT_DIR}/results/etcd/report_leader_kill.json"

python3 "${ROOT_DIR}/analysis/report.py" \
  --baseline "${ROOT_DIR}/results/etcd/baseline" \
  --fault "${ROOT_DIR}/results/etcd/fault/delay_120ms" \
  --out "${ROOT_DIR}/results/etcd/report_delay_120ms.json"

python3 "${ROOT_DIR}/analysis/report.py" \
  --baseline "${ROOT_DIR}/results/etcd/baseline" \
  --fault "${ROOT_DIR}/results/etcd/fault/loss_8pct" \
  --out "${ROOT_DIR}/results/etcd/report_loss_8pct.json"

python3 "${ROOT_DIR}/analysis/report.py" \
  --baseline "${ROOT_DIR}/results/etcd/baseline" \
  --fault "${ROOT_DIR}/results/etcd/fault/partition" \
  --out "${ROOT_DIR}/results/etcd/report_partition.json"

python3 "${ROOT_DIR}/analysis/report.py" \
  --baseline "${ROOT_DIR}/results/etcd/baseline" \
  --fault "${ROOT_DIR}/results/etcd/fault/majority_crash" \
  --out "${ROOT_DIR}/results/etcd/report_majority_crash.json"

python3 "${ROOT_DIR}/analysis/report.py" \
  --baseline "${ROOT_DIR}/results/etcd/baseline" \
  --fault "${ROOT_DIR}/results/etcd/fault/majority_partition" \
  --out "${ROOT_DIR}/results/etcd/report_majority_partition.json"

python3 "${ROOT_DIR}/analysis/figures.py" \
  --results-root "${ROOT_DIR}/results" \
  --system etcd \
  --fig-dir "${ROOT_DIR}/results/figures"

echo "Done. Reports at results/etcd/report_*.json and figures at results/figures/"
