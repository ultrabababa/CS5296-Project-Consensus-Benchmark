#!/usr/bin/env bash
set -euo pipefail

PRE_SLEEP="${PRE_SLEEP:-2}"
sleep "${PRE_SLEEP}"
DURATION_SECS="${1:-10}"

# isolate etcd1 by dropping peer and client ports
docker exec etcd1 iptables -I INPUT 1 -p tcp --dport 2379 -j DROP
docker exec etcd1 iptables -I OUTPUT 1 -p tcp --sport 2379 -j DROP
docker exec etcd1 iptables -I INPUT 1 -p tcp --dport 2380 -j DROP
docker exec etcd1 iptables -I OUTPUT 1 -p tcp --sport 2380 -j DROP

sleep "${DURATION_SECS}"

docker exec etcd1 iptables -D INPUT -p tcp --dport 2379 -j DROP || true
docker exec etcd1 iptables -D OUTPUT -p tcp --sport 2379 -j DROP || true
docker exec etcd1 iptables -D INPUT -p tcp --dport 2380 -j DROP || true
docker exec etcd1 iptables -D OUTPUT -p tcp --sport 2380 -j DROP || true
