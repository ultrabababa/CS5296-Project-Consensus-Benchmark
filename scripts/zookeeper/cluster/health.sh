#!/usr/bin/env bash
set -euo pipefail

for node in zk1 zk2 zk3; do
  docker exec "${node}" sh -lc "echo ruok | nc 127.0.0.1 2181 | grep imok"
done
