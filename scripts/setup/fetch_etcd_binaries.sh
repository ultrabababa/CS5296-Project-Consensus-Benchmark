#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET_DIR="${ROOT_DIR}/infra/etcd/bin"
VERSION="v3.5.14"
TARBALL="etcd-${VERSION}-linux-amd64.tar.gz"
URL="https://github.com/etcd-io/etcd/releases/download/${VERSION}/${TARBALL}"
TMP_DIR="${ROOT_DIR}/.tmp"

mkdir -p "${TMP_DIR}" "${TARGET_DIR}"

echo "Downloading ${URL}"
curl -L "${URL}" -o "${TMP_DIR}/${TARBALL}"

tar -xzf "${TMP_DIR}/${TARBALL}" -C "${TMP_DIR}"
cp "${TMP_DIR}/etcd-${VERSION}-linux-amd64/etcd" "${TARGET_DIR}/etcd"
cp "${TMP_DIR}/etcd-${VERSION}-linux-amd64/etcdctl" "${TARGET_DIR}/etcdctl"

chmod +x "${TARGET_DIR}/etcd" "${TARGET_DIR}/etcdctl"

echo "etcd binaries ready at ${TARGET_DIR}"
