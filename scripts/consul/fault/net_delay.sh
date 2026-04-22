#!/usr/bin/env bash
set -euo pipefail

PRE_SLEEP="${PRE_SLEEP:-2}"
sleep "${PRE_SLEEP}"
TARGET="${1:-consul3}"
DELAY_MS="${2:-120}"
JITTER_MS="${3:-20}"
PRE_SLEEP="${PRE_SLEEP:-2}"
sleep "${PRE_SLEEP}"
DURATION_SECS="${4:-8}"

docker exec "${TARGET}" tc qdisc replace dev eth0 root netem delay "${DELAY_MS}ms" "${JITTER_MS}ms" distribution normal
sleep "${DURATION_SECS}"
docker exec "${TARGET}" tc qdisc del dev eth0 root || true
