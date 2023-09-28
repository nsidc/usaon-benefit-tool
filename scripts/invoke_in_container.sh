#!/usr/bin/env bash
set -euo pipefail

args="$@"

# TODO: Do we need this?  --user="${UID}" \
#       Or this for wrapping the command?   bash --login -c \
docker-compose run --rm \
    usaon-vta-survey \
    invoke $args

cd / 1>/dev/null
