#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

"${ROOT_DIR}/scripts/consul/cluster/up.sh"
sleep 10
"${ROOT_DIR}/scripts/consul/cluster/health.sh"

"${ROOT_DIR}/scripts/consul/workload/run_baseline.sh"
"${ROOT_DIR}/scripts/consul/fault/run_fault_experiments.sh"

for scenario in leader_kill delay_120ms loss_8pct partition majority_crash majority_partition; do
  python3 "${ROOT_DIR}/analysis/report.py" \
    --baseline "${ROOT_DIR}/results/consul/baseline" \
    --fault "${ROOT_DIR}/results/consul/fault/${scenario}" \
    --out "${ROOT_DIR}/results/consul/report_${scenario}.json"
done

python3 "${ROOT_DIR}/analysis/figures.py" \
  --results-root "${ROOT_DIR}/results" \
  --system consul \
  --fig-dir "${ROOT_DIR}/results/figures"

echo "Done. Consul reports at results/consul/report_*.json and figures at results/figures/."
