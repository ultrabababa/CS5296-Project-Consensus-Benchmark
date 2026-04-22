#!/usr/bin/env bash
set -euo pipefail

PRE_SLEEP="${PRE_SLEEP:-2}"
sleep "${PRE_SLEEP}"
DURATION_SECS="${1:-10}"

for target in zk1 zk2; do
  docker exec "${target}" iptables -I INPUT 1 -p tcp --dport 2181 -j DROP
  docker exec "${target}" iptables -I OUTPUT 1 -p tcp --sport 2181 -j DROP
  docker exec "${target}" iptables -I INPUT 1 -p tcp --dport 2888 -j DROP
  docker exec "${target}" iptables -I OUTPUT 1 -p tcp --sport 2888 -j DROP
  docker exec "${target}" iptables -I INPUT 1 -p tcp --dport 3888 -j DROP
  docker exec "${target}" iptables -I OUTPUT 1 -p tcp --sport 3888 -j DROP
done

sleep "${DURATION_SECS}"

for target in zk1 zk2; do
  docker exec "${target}" iptables -D INPUT -p tcp --dport 2181 -j DROP || true
  docker exec "${target}" iptables -D OUTPUT -p tcp --sport 2181 -j DROP || true
  docker exec "${target}" iptables -D INPUT -p tcp --dport 2888 -j DROP || true
  docker exec "${target}" iptables -D OUTPUT -p tcp --sport 2888 -j DROP || true
  docker exec "${target}" iptables -D INPUT -p tcp --dport 3888 -j DROP || true
  docker exec "${target}" iptables -D OUTPUT -p tcp --sport 3888 -j DROP || true
done
