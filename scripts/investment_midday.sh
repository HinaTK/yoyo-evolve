#!/bin/bash
# Run the midday intraday investment check.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

SESSION="midday" bash "$ROOT_DIR/scripts/evolve_investment.sh"
