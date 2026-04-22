#!/usr/bin/env bash
set -euo pipefail

for node in consul1 consul2 consul3; do
  docker exec "${node}" consul members >/dev/null
done
