#!/bin/bash
# scripts/bootstrap_investment_iterations.sh — replay prior market days to warm up investment learnings.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DAYS="${DAYS:-30}"
MODEL="${MODEL:-gpt-5.5}"
FALLBACK_MODEL="${FALLBACK_MODEL:-gpt-5.4}"
TIMEOUT="${TIMEOUT:-900}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
FORCE_REPLAY="${FORCE_REPLAY:-false}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    if command -v python >/dev/null 2>&1; then
        PYTHON_BIN="python"
    fi
fi

cd "$ROOT_DIR"

"$PYTHON_BIN" "$ROOT_DIR/scripts/backfill_investment_snapshots.py" --days "$DAYS"

mapfile -t SNAPSHOT_DATES < <($PYTHON_BIN - <<'PY'
import os
import pathlib

paths = sorted(pathlib.Path('data/snapshots').glob('*.json'))
days = int(os.environ.get('DAYS', '30'))
for path in paths[-days:]:
    print(path.stem)
PY
)

done_count=0
total_count=${#SNAPSHOT_DATES[@]}

for run_date in "${SNAPSHOT_DATES[@]}"; do
    run_date="${run_date//$'\r'/}"
    done_count=$((done_count + 1))
    calls_file="$ROOT_DIR/research/calls/$run_date-calls.json"
    assessment_file="$ROOT_DIR/research/daily/$run_date-market-assessment.md"
    plan_file="$ROOT_DIR/research/daily/$run_date-plan.md"
    report_file="$ROOT_DIR/research/daily/$run_date-report.md"
    reflection_file="$ROOT_DIR/research/daily/$run_date-reflection.md"

    if [ "$FORCE_REPLAY" != "true" ] \
        && [ -f "$calls_file" ] \
        && [ -f "$assessment_file" ] \
        && [ -f "$plan_file" ] \
        && [ -f "$report_file" ] \
        && [ -f "$reflection_file" ]; then
        echo "=== Bootstrap replay [$done_count/$total_count]: $run_date (skip: outputs complete) ==="
        continue
    fi

    echo "=== Bootstrap replay [$done_count/$total_count]: $run_date (model: $MODEL) ==="
    if ! DATE="$run_date" \
        MODEL="$MODEL" \
        TIMEOUT="$TIMEOUT" \
        SNAPSHOT_FILE="$ROOT_DIR/data/snapshots/$run_date.json" \
        SESSION="historical" \
        PYTHON_BIN="$PYTHON_BIN" \
        PROVIDER="${PROVIDER:-custom}" \
        BASE_URL="${BASE_URL:-http://127.0.0.1:8310/v1}" \
        API_KEY="${API_KEY:-}" \
        OPENAI_API_KEY="${OPENAI_API_KEY:-}" \
        bash "$ROOT_DIR/scripts/evolve_investment.sh"; then
        if [ -n "$FALLBACK_MODEL" ] && [ "$FALLBACK_MODEL" != "$MODEL" ]; then
            echo "    primary model failed; retrying $run_date with fallback model: $FALLBACK_MODEL"
            DATE="$run_date" \
            MODEL="$FALLBACK_MODEL" \
            TIMEOUT="$TIMEOUT" \
            SNAPSHOT_FILE="$ROOT_DIR/data/snapshots/$run_date.json" \
            SESSION="historical" \
            PYTHON_BIN="$PYTHON_BIN" \
            PROVIDER="${PROVIDER:-custom}" \
            BASE_URL="${BASE_URL:-http://127.0.0.1:8310/v1}" \
            API_KEY="${API_KEY:-}" \
            OPENAI_API_KEY="${OPENAI_API_KEY:-}" \
            bash "$ROOT_DIR/scripts/evolve_investment.sh"
        else
            echo "    no fallback model configured; stopping bootstrap." >&2
            exit 1
        fi
    fi
done

echo "Bootstrap replay complete for ${#SNAPSHOT_DATES[@]} dates."
