#!/usr/bin/env bash
set -euo pipefail

PRE_SLEEP="${PRE_SLEEP:-2}"
DOWN_SECS="${DOWN_SECS:-10}"
POST_SLEEP="${POST_SLEEP:-3}"

sleep "${PRE_SLEEP}"
docker stop zk2
docker stop zk3
sleep "${DOWN_SECS}"
docker start zk2
docker start zk3
sleep "${POST_SLEEP}"
