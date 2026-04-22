#!/usr/bin/env bash
set -euo pipefail

PRE_SLEEP="${PRE_SLEEP:-2}"
sleep "${PRE_SLEEP}"
TARGET="${1:-zk3}"
LOSS_PCT="${2:-8}"
PRE_SLEEP="${PRE_SLEEP:-2}"
sleep "${PRE_SLEEP}"
DURATION_SECS="${3:-8}"

docker exec "${TARGET}" tc qdisc replace dev eth0 root netem loss "${LOSS_PCT}%"
sleep "${DURATION_SECS}"
docker exec "${TARGET}" tc qdisc del dev eth0 root || true
