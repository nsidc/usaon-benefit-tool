#!/usr/bin/env bash
set -euo pipefail

gunicorn \
    "usaon_benefit_tool:create_app()" \
    --log-level="info" \
    --access-logfile=- \
    --bind="0.0.0.0:5000" \
    --workers="${NUM_WORKERS:-5}" \
    --certfile="/run/secrets/site.crt" --keyfile="/run/secrets/site.key"
