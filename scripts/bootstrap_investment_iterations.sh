#!/bin/bash
# scripts/bootstrap_investment_iterations.sh — replay prior market days to warm up investment learnings.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DAYS="${DAYS:-30}"
MODEL="${MODEL:-claude-opus-4-6}"
TIMEOUT="${TIMEOUT:-900}"

cd "$ROOT_DIR"

python3 "$ROOT_DIR/scripts/backfill_investment_snapshots.py" --days "$DAYS"

mapfile -t SNAPSHOT_DATES < <(python3 - <<'PY'
import os
import pathlib

paths = sorted(pathlib.Path('data/snapshots').glob('*.json'))
days = int(os.environ.get('DAYS', '30'))
for path in paths[-days:]:
    print(path.stem)
PY
)

for run_date in "${SNAPSHOT_DATES[@]}"; do
    echo "=== Bootstrap replay: $run_date ==="
    DATE="$run_date" \
    MODEL="$MODEL" \
    TIMEOUT="$TIMEOUT" \
    SNAPSHOT_FILE="$ROOT_DIR/data/snapshots/$run_date.json" \
    bash "$ROOT_DIR/scripts/evolve_investment.sh"
done

echo "Bootstrap replay complete for ${#SNAPSHOT_DATES[@]} dates."
