#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="${ROOT_DIR}/infra/etcd/docker-compose.yml"

if [[ ! -x "${ROOT_DIR}/infra/etcd/bin/etcd" || ! -x "${ROOT_DIR}/infra/etcd/bin/etcdctl" ]]; then
  "${ROOT_DIR}/scripts/setup/fetch_etcd_binaries.sh"
fi

mkdir -p "${ROOT_DIR}/infra/etcd/data/etcd1" "${ROOT_DIR}/infra/etcd/data/etcd2" "${ROOT_DIR}/infra/etcd/data/etcd3"

docker compose -f "${COMPOSE_FILE}" up -d --build
