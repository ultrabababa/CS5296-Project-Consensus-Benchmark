#!/usr/bin/env bash
set -euo pipefail

PRE_SLEEP="${PRE_SLEEP:-2}"
sleep "${PRE_SLEEP}"
DURATION_SECS="${1:-10}"

for target in consul1 consul2; do
  docker exec "${target}" iptables -I INPUT 1 -p tcp --dport 8500 -j DROP
  docker exec "${target}" iptables -I OUTPUT 1 -p tcp --sport 8500 -j DROP
  docker exec "${target}" iptables -I INPUT 1 -p tcp --dport 8300 -j DROP
  docker exec "${target}" iptables -I OUTPUT 1 -p tcp --sport 8300 -j DROP
  docker exec "${target}" iptables -I INPUT 1 -p tcp --dport 8301 -j DROP
  docker exec "${target}" iptables -I OUTPUT 1 -p tcp --sport 8301 -j DROP
done

sleep "${DURATION_SECS}"

for target in consul1 consul2; do
  docker exec "${target}" iptables -D INPUT -p tcp --dport 8500 -j DROP || true
  docker exec "${target}" iptables -D OUTPUT -p tcp --sport 8500 -j DROP || true
  docker exec "${target}" iptables -D INPUT -p tcp --dport 8300 -j DROP || true
  docker exec "${target}" iptables -D OUTPUT -p tcp --sport 8300 -j DROP || true
  docker exec "${target}" iptables -D INPUT -p tcp --dport 8301 -j DROP || true
  docker exec "${target}" iptables -D OUTPUT -p tcp --sport 8301 -j DROP || true
done
