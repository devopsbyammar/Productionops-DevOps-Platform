
#!/usr/bin/env bash

set -euo pipefail

HEALTH_URL="${1:-http://127.0.0.1:5001/health}"

echo "Checking ProductionOps application..."
echo "Health URL: ${HEALTH_URL}"

if curl --fail --silent --show-error \
    --max-time 5 \
    "${HEALTH_URL}"; then
    echo
    echo "Health check PASSED"
else
    echo
    echo "Health check FAILED"
    exit 1
fi
