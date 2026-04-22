#!/usr/bin/env bash
set -euo pipefail

PRE_SLEEP="${PRE_SLEEP:-2}"
DOWN_SECS="${DOWN_SECS:-8}"
POST_SLEEP="${POST_SLEEP:-3}"

sleep "${PRE_SLEEP}"
docker stop consul1
sleep "${DOWN_SECS}"
docker start consul1
sleep "${POST_SLEEP}"
