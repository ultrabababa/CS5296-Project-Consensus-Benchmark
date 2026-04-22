#!/usr/bin/env bash
set -euo pipefail

# Simple deterministic choice: stop etcd3 as follower candidate.
docker stop etcd3

sleep 5

docker start etcd3

sleep 5
