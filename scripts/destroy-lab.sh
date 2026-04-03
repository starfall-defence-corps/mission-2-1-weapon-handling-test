#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DOCKER_DIR="$ROOT_DIR/.docker"

echo ""
echo "=============================================="
echo "  Decommissioning WHT range and fleet..."
echo "=============================================="
echo ""

if [ -f "$DOCKER_DIR/docker-compose.yml" ]; then
    docker compose -f "$DOCKER_DIR/docker-compose.yml" down -v 2>&1 | while read -r line; do
        echo "    $line"
    done
fi

rm -rf "$DOCKER_DIR/ssh-keys"
rm -rf "$ROOT_DIR/workspace/.ssh"
rm -rf "$ROOT_DIR/venv"

echo ""
echo "  WHT range and fleet decommissioned."
echo ""
