#!/bin/bash
# Run the close-session investment review and memory update pass.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

SESSION="close" bash "$ROOT_DIR/scripts/evolve_investment.sh"
