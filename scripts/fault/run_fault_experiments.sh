#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ROUNDS="${ROUNDS:-3}"

run_scenario() {
  local scenario="$1"
  local out_dir="${ROOT_DIR}/results/etcd/fault/${scenario}"
  mkdir -p "${out_dir}"
  rm -f "${out_dir}"/run_*.json

  # Ensure workload overlaps with fault injection window.
  fault_pid=""

  for i in $(seq 1 "${ROUNDS}"); do
    case "${scenario}" in
      leader_kill)
        PRE_SLEEP=1 DOWN_SECS=8 POST_SLEEP=1 "${ROOT_DIR}/scripts/fault/kill_leader.sh" &
        fault_pid="$!"
        ;;
      delay_120ms)
        "${ROOT_DIR}/scripts/fault/net_delay.sh" etcd3 120 20 8 &
        fault_pid="$!"
        ;;
      loss_8pct)
        "${ROOT_DIR}/scripts/fault/net_loss.sh" etcd3 8 8 &
        fault_pid="$!"
        ;;
      partition)
        "${ROOT_DIR}/scripts/fault/partition_one_node.sh" etcd3 8 &
        fault_pid="$!"
        ;;
      majority_crash)
        PRE_SLEEP=1 DOWN_SECS=10 POST_SLEEP=1 "${ROOT_DIR}/scripts/fault/majority_crash.sh" &
        fault_pid="$!"
        ;;
      majority_partition)
        "${ROOT_DIR}/scripts/fault/majority_partition.sh" 10 &
        fault_pid="$!"
        ;;
      *)
        echo "Unknown scenario: ${scenario}" >&2
        exit 1
        ;;
    esac

    python3 "${ROOT_DIR}/scripts/workload/run_etcd_workload.py" \
      --ops 300 \
      --seed "$((1000 + i))" \
      --prefix "fault-${scenario}" \
      --redundant-copies 1 \
      --out "${out_dir}/run_${i}.json"

    if [[ -n "${fault_pid}" ]]; then
      wait "${fault_pid}" || true
      fault_pid=""
    fi
  done
}

run_scenario leader_kill
run_scenario delay_120ms
run_scenario loss_8pct
run_scenario partition
run_scenario majority_crash
run_scenario majority_partition
