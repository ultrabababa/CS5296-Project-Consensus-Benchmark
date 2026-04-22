#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PRE_SLEEP="${PRE_SLEEP:-2}"
DOWN_SECS="${DOWN_SECS:-8}"
POST_SLEEP="${POST_SLEEP:-3}"

sleep "${PRE_SLEEP}"

LEADER="$(ROOT_DIR="${ROOT_DIR}" python3 - <<'PY'
import json
import os
import subprocess
import sys
from pathlib import Path

root = Path(os.environ["ROOT_DIR"]).resolve()
sys.path.insert(0, str(root))

from analysis.etcd_status import leader_container_name

cmd = [
    "docker",
    "exec",
    "etcd1",
    "etcdctl",
    "--endpoints=http://etcd1:2379,http://etcd2:2379,http://etcd3:2379",
    "endpoint",
    "status",
    "-w",
    "json",
]
res = subprocess.run(cmd, capture_output=True, text=True, check=True)
payload = json.loads(res.stdout)
print(leader_container_name(payload))
PY
)"

echo "Detected leader: ${LEADER}"
docker stop "${LEADER}"
sleep "${DOWN_SECS}"
docker start "${LEADER}"
sleep "${POST_SLEEP}"
