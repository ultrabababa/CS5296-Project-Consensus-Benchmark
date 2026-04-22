#!/usr/bin/env bash
set -euo pipefail

PRE_SLEEP="${PRE_SLEEP:-2}"
sleep "${PRE_SLEEP}"
TARGET="${1:-consul3}"
PRE_SLEEP="${PRE_SLEEP:-2}"
sleep "${PRE_SLEEP}"
DURATION_SECS="${2:-8}"

docker exec "${TARGET}" iptables -I INPUT 1 -p tcp --dport 8500 -j DROP
docker exec "${TARGET}" iptables -I OUTPUT 1 -p tcp --sport 8500 -j DROP
docker exec "${TARGET}" iptables -I INPUT 1 -p tcp --dport 8300 -j DROP
docker exec "${TARGET}" iptables -I OUTPUT 1 -p tcp --sport 8300 -j DROP
docker exec "${TARGET}" iptables -I INPUT 1 -p tcp --dport 8301 -j DROP
docker exec "${TARGET}" iptables -I OUTPUT 1 -p tcp --sport 8301 -j DROP

sleep "${DURATION_SECS}"

docker exec "${TARGET}" iptables -D INPUT -p tcp --dport 8500 -j DROP || true
docker exec "${TARGET}" iptables -D OUTPUT -p tcp --sport 8500 -j DROP || true
docker exec "${TARGET}" iptables -D INPUT -p tcp --dport 8300 -j DROP || true
docker exec "${TARGET}" iptables -D OUTPUT -p tcp --sport 8300 -j DROP || true
docker exec "${TARGET}" iptables -D INPUT -p tcp --dport 8301 -j DROP || true
docker exec "${TARGET}" iptables -D OUTPUT -p tcp --sport 8301 -j DROP || true
