#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

"${ROOT_DIR}/scripts/zookeeper/cluster/up.sh"
sleep 10
"${ROOT_DIR}/scripts/zookeeper/cluster/health.sh"

"${ROOT_DIR}/scripts/zookeeper/workload/run_baseline.sh"
"${ROOT_DIR}/scripts/zookeeper/fault/run_fault_experiments.sh"

for scenario in leader_kill delay_120ms loss_8pct partition majority_crash majority_partition; do
  python3 "${ROOT_DIR}/analysis/report.py" \
    --baseline "${ROOT_DIR}/results/zookeeper/baseline" \
    --fault "${ROOT_DIR}/results/zookeeper/fault/${scenario}" \
    --out "${ROOT_DIR}/results/zookeeper/report_${scenario}.json"
done

python3 "${ROOT_DIR}/analysis/figures.py" \
  --results-root "${ROOT_DIR}/results" \
  --system zookeeper \
  --fig-dir "${ROOT_DIR}/results/figures"

echo "Done. ZooKeeper reports at results/zookeeper/report_*.json and figures at results/figures/."
