#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

"${ROOT_DIR}/scripts/pipeline/run_etcd_full.sh"
"${ROOT_DIR}/scripts/pipeline/run_zookeeper_full.sh"
"${ROOT_DIR}/scripts/pipeline/run_consul_full.sh"

python3 "${ROOT_DIR}/analysis/multi_system_radar.py" \
  --results-root "${ROOT_DIR}/results" \
  --systems etcd zookeeper consul \
  --out-png "${ROOT_DIR}/results/figures/all_systems_fig2_radar.png" \
  --out-csv "${ROOT_DIR}/results/figures/all_systems_fig2_radar.csv"

echo "All systems complete. See results/{etcd,zookeeper,consul} and results/figures/all_systems_fig2_radar.png"
