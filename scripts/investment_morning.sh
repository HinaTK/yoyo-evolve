#!/bin/bash
# Run the morning investment planning pass.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

SESSION="morning" bash "$ROOT_DIR/scripts/evolve_investment.sh"
