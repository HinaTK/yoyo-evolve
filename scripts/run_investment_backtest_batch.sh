#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    if command -v python >/dev/null 2>&1; then
        PYTHON_BIN="python"
    fi
fi

BATCH_INDEX="${BATCH_INDEX:-${1:-}}"
PLAN_FILE="${PLAN_FILE:-research/experiments/historical_batches/plan.json}"
FORCE_REPLAY="${FORCE_REPLAY:-false}"

if [ -z "$BATCH_INDEX" ]; then
    echo "Usage: BATCH_INDEX=1 bash scripts/run_investment_backtest_batch.sh" >&2
    exit 2
fi

cd "$ROOT_DIR"

python_path() {
    if command -v cygpath >/dev/null 2>&1; then
        cygpath -w "$1"
    else
        printf '%s\n' "$1"
    fi
}

PLAN_FILE_PY="$(python_path "$PLAN_FILE")"

if [ ! -f "$PLAN_FILE" ]; then
    "$PYTHON_BIN" scripts/plan_investment_backtest_batches.py --output "$PLAN_FILE"
fi

mapfile -t BATCH_DATES < <("$PYTHON_BIN" - <<PY
import json, pathlib
plan = json.loads(pathlib.Path(r'''$PLAN_FILE_PY''').read_text(encoding='utf-8'))
batch_index = int(r'''$BATCH_INDEX''')
for batch in plan.get('batches', []):
    if int(batch.get('batch_index')) == batch_index:
        for day in batch.get('dates', []):
            print(day)
        break
PY
)

if [ "${#BATCH_DATES[@]}" -eq 0 ]; then
    echo "No dates found for batch $BATCH_INDEX in $PLAN_FILE" >&2
    exit 1
fi

echo "Running historical investment batch $BATCH_INDEX (${#BATCH_DATES[@]} dates)."
LAST_BATCH_DATE=""
for run_date in "${BATCH_DATES[@]}"; do
    run_date="${run_date//$'\r'/}"
    LAST_BATCH_DATE="$run_date"
    snapshot_file="$ROOT_DIR/data/snapshots/$run_date.json"
    if [ ! -f "$snapshot_file" ]; then
        echo "Missing snapshot: $snapshot_file. Run scripts/backfill_investment_snapshots.py first." >&2
        exit 1
    fi
    calls_file="$ROOT_DIR/research/calls/$run_date-calls.json"
    if [ "$FORCE_REPLAY" != "true" ] && [ -f "$calls_file" ]; then
        echo "Skip $run_date: calls already exist. Set FORCE_REPLAY=true to rerun."
        continue
    fi
    echo "=== Historical replay: $run_date ==="
    DATE="$run_date" \
        SESSION="historical" \
        SNAPSHOT_FILE="$snapshot_file" \
        PYTHON_BIN="$PYTHON_BIN" \
        bash scripts/evolve_investment.sh
done

"$PYTHON_BIN" scripts/build_snapshot_registry.py --snapshot-dir data/snapshots --output data/snapshots/registry.json
"$PYTHON_BIN" scripts/evaluate_investment_calls.py --summary-md research/evaluations/latest.md --summary-json research/evaluations/latest.json --records-json research/evaluations/latest_records.json
"$PYTHON_BIN" scripts/build_symbol_risk_memory.py --latest-json research/evaluations/latest.json --records-json research/evaluations/latest_records.json --output research/experiments/symbol_risk_memory.json --as-of-date "$LAST_BATCH_DATE"
BACKTEST_LAYER_ARGS=$($PYTHON_BIN - <<'PY'
import pathlib, shlex, tomllib
path = pathlib.Path('config') / 'optimization.toml'
opt = tomllib.load(open(path, 'rb')) if path.exists() else {}
args = [
    '--actionable-top-n', str(opt.get('actionable_top_n', opt.get('top_n', 1))),
    '--diagnostic-top-n', str(opt.get('diagnostic_top_n', opt.get('top_n', 3))),
    '--horizon-days', str(opt.get('horizon_days', 3)),
    '--round-trip-bps', str(opt.get('round_trip_bps', 35)),
    '--minimum-edge-bps', str(opt.get('minimum_edge_bps', 100)),
    '--benchmark-symbol', str(opt.get('benchmark_symbol', '2800.HK')),
    '--min-watch-score', str(opt.get('min_watch_score', 45)),
    '--min-action-score', str(opt.get('min_action_score', 65)),
    '--candidate-policy', str(opt.get('candidate_policy', 'strict')),
    '--min-samples', str(opt.get('min_samples', 12)),
    '--max-adverse-limit-pct', str(opt.get('max_adverse_limit_pct', -8.0)),
    '--max-market-range-for-action', str(opt.get('max_market_range_for_action', 0.70)),
]
symbol_risk_mode = str(opt.get('symbol_risk_mode', 'full'))
args.extend(['--symbol-risk-mode', symbol_risk_mode])
if symbol_risk_mode == 'point_in_time':
    args.extend(['--symbol-risk-records-json', str(opt.get('symbol_risk_records', 'research/evaluations/latest_records.json'))])
elif pathlib.Path(str(opt.get('symbol_risk_memory', 'research/experiments/symbol_risk_memory.json'))).exists():
    args.extend(['--symbol-risk-json', str(opt.get('symbol_risk_memory', 'research/experiments/symbol_risk_memory.json'))])
print(' '.join(shlex.quote(arg) for arg in args))
PY
)
"$PYTHON_BIN" scripts/backtest_investment_strategy.py --registry data/snapshots/registry.json --strategy-config config/active_strategy.toml --output-dir research/experiments --as-of-date "$LAST_BATCH_DATE" $BACKTEST_LAYER_ARGS
"$PYTHON_BIN" scripts/optimize_investment_params.py --config config/optimization.toml --as-of-date "$LAST_BATCH_DATE" --session historical

echo "Batch $BATCH_INDEX complete."
