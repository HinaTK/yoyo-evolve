#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    if command -v python >/dev/null 2>&1; then
        PYTHON_BIN="python"
    fi
fi

YOYO_BIN="${YOYO_BIN:-$ROOT_DIR/target/debug/yoyo}"
if [ "$YOYO_BIN" = "$ROOT_DIR/target/debug/yoyo" ] && [ -f "$ROOT_DIR/target/debug/yoyo.exe" ]; then
    YOYO_BIN="$ROOT_DIR/target/debug/yoyo.exe"
fi

DATE="${DATE:-$(date +%Y-%m-%d)}"
SESSION="${SESSION:-close}"
MODEL="${MODEL:-claude-opus-4-6}"
PROVIDER="${PROVIDER:-anthropic}"
BASE_URL="${BASE_URL:-}"
TIMEOUT="${TIMEOUT:-1200}"
AUTO_IMPLEMENT="${INVESTMENT_SYSTEM_AUTO_IMPLEMENT:-false}"
OUTPUT_DIR="$ROOT_DIR/research/experiments/system_changes"
PLAN_JSON="$OUTPUT_DIR/latest_improvement_plan.json"
CHANGE_JSON="$OUTPUT_DIR/latest_change_evaluation.json"
SYSTEM_JSON="$OUTPUT_DIR/latest_system_evolution.json"
SYSTEM_MD="$OUTPUT_DIR/latest_system_evolution.md"

cd "$ROOT_DIR"
mkdir -p "$OUTPUT_DIR" "session_plan" "research/evaluations" "research/experiments" "data/snapshots"

timeout_cmd=""
if command -v timeout >/dev/null 2>&1; then
    timeout_cmd="timeout"
elif command -v gtimeout >/dev/null 2>&1; then
    timeout_cmd="gtimeout"
fi

has_investment_changes() {
    git status --short -- scripts config memory research INVESTMENT_SYSTEM.md tests data/snapshots | grep -q .
}

run_yoyo_task() {
    local task_file="$1"
    local prompt_file log_file
    prompt_file="$(mktemp)"
    log_file="$OUTPUT_DIR/$(basename "$task_file" .md)-implementation.log"
    cat > "$prompt_file" <<EOF
You are implementing one bounded HK investment research-system improvement task.

Task file:
$(cat "$task_file")

Hard constraints:
- Modify only investment research system code, tests, docs, config, or prompts needed for this task.
- Do not add automatic trading, execution venue integrations, trade placement, or execution hooks.
- Do not set recommendation_only=false, research_only=false, or automatic_trading=true.
- Do not reduce cost gates, edge gates, position limits, theme exposure limits, or future/as-of leakage safeguards.
- Do not modify historical files under data/snapshots.
- Run relevant validation and report what passed.
EOF

    local provider_args=(--provider "$PROVIDER" --model "$MODEL")
    if [ -n "$BASE_URL" ]; then
        provider_args+=(--base-url "$BASE_URL")
    fi
    if [ -n "$timeout_cmd" ]; then
        "$timeout_cmd" "$TIMEOUT" "$YOYO_BIN" "${provider_args[@]}" --skills ./skills < "$prompt_file" 2>&1 | tee "$log_file"
    else
        "$YOYO_BIN" "${provider_args[@]}" --skills ./skills < "$prompt_file" 2>&1 | tee "$log_file"
    fi
}

echo "Building snapshot registry..."
"$PYTHON_BIN" scripts/build_snapshot_registry.py --snapshot-dir data/snapshots --output data/snapshots/registry.json

echo "Evaluating investment calls..."
"$PYTHON_BIN" scripts/evaluate_investment_calls.py --summary-md research/evaluations/latest.md --summary-json research/evaluations/latest.json --records-json research/evaluations/latest_records.json

echo "Attributing investment outcomes..."
"$PYTHON_BIN" scripts/attribute_investment_outcomes.py --records-json research/evaluations/latest_records.json --output-json research/evaluations/latest_attribution.json --output-md research/evaluations/latest_attribution.md

echo "Building symbol risk memory..."
if [ -f research/evaluations/latest.json ]; then
    "$PYTHON_BIN" scripts/build_symbol_risk_memory.py --latest-json research/evaluations/latest.json --output research/experiments/symbol_risk_memory.json --as-of-date "$DATE" || true
else
    echo "No latest evaluation JSON; skipping symbol risk memory."
fi

echo "Running backtest..."
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
"$PYTHON_BIN" scripts/backtest_investment_strategy.py --registry data/snapshots/registry.json --strategy-config config/active_strategy.toml --output-dir research/experiments --as-of-date "$DATE" $BACKTEST_LAYER_ARGS

echo "Running optimization..."
"$PYTHON_BIN" scripts/optimize_investment_params.py --config config/optimization.toml --as-of-date "$DATE" --session "$SESSION"

echo "Planning system improvements..."
"$PYTHON_BIN" scripts/plan_investment_system_improvements.py --plan-dir session_plan --output "$PLAN_JSON"

implemented=false
if [ "$AUTO_IMPLEMENT" = "true" ]; then
    if [ ! -f "$YOYO_BIN" ]; then
        echo "Building yoyo binary..."
        cargo build --quiet
    fi
    shopt -s nullglob
    for task_file in session_plan/investment_task_*.md; do
        implemented=true
        run_yoyo_task "$task_file"
    done
    shopt -u nullglob
else
    echo "INVESTMENT_SYSTEM_AUTO_IMPLEMENT is not true; generated tasks only."
fi

change_exit=0
if has_investment_changes; then
    echo "Evaluating investment system change invariants..."
    "$PYTHON_BIN" scripts/evaluate_investment_system_change.py --output-dir "$OUTPUT_DIR" || change_exit=$?
else
    echo "No investment system changes detected; writing pass evaluation."
    "$PYTHON_BIN" scripts/evaluate_investment_system_change.py --output-dir "$OUTPUT_DIR" >/dev/null
fi

tests_exit=0
"$PYTHON_BIN" -m unittest tests/test_investment_level5_level6.py || tests_exit=$?

export L6_AUTO_IMPLEMENT="$AUTO_IMPLEMENT"
export L6_IMPLEMENTED="$implemented"
export L6_TESTS_EXIT="$tests_exit"
export L6_CHANGE_EXIT="$change_exit"
"$PYTHON_BIN" - <<'PY'
import datetime as dt, json, os, pathlib
out = pathlib.Path("research/experiments/system_changes")
plan_path = out / "latest_improvement_plan.json"
change_path = out / "latest_change_evaluation.json"
system_json = out / "latest_system_evolution.json"
system_md = out / "latest_system_evolution.md"
out.mkdir(parents=True, exist_ok=True)
plan = json.loads(plan_path.read_text(encoding='utf-8')) if plan_path.exists() else {'tasks': []}
change = json.loads(change_path.read_text(encoding='utf-8')) if change_path.exists() else {'passed': False, 'findings': []}
result = {
  'generated_at': dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
  'auto_implement_requested': os.environ.get('L6_AUTO_IMPLEMENT') == 'true',
  'implemented': os.environ.get('L6_IMPLEMENTED') == 'true',
  'task_count': len(plan.get('tasks', [])),
  'tasks': plan.get('tasks', []),
  'change_evaluation_passed': bool(change.get('passed')),
  'change_finding_count': len(change.get('findings', [])),
  'changed_paths': change.get('changed_paths', []),
  'change_findings': change.get('findings', []),
  'python_unittest_exit': int(os.environ.get('L6_TESTS_EXIT', '1')),
  'change_evaluator_exit': int(os.environ.get('L6_CHANGE_EXIT', '1')),
}
system_json.write_text(json.dumps(result, indent=2), encoding='utf-8')
lines = ['# Investment System Evolution', '', f"Generated: `{result['generated_at']}`", f"Auto implementation requested: `{result['auto_implement_requested']}`", f"Implemented: `{result['implemented']}`", f"Change evaluation passed: `{result['change_evaluation_passed']}`", f"Python unittest exit: `{result['python_unittest_exit']}`", '', '## Planned Tasks']
if result['tasks']:
    lines.extend(f"- `{task['id']}` {task['title']}" for task in result['tasks'])
else:
    lines.append('- No improvement tasks generated.')
lines.extend(['', '## Change Findings'])
if change.get('findings'):
    lines.extend(f"- `{item.get('rule')}` `{item.get('path') or 'global'}`: {item.get('message')}" for item in change.get('findings', []))
else:
    lines.append('- No invariant violations detected.')
lines.extend(['', '## Changed Paths'])
if result['changed_paths']:
    lines.extend(f"- `{path}`" for path in result['changed_paths'])
else:
    lines.append('- No changed paths detected.')
system_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')
PY

if [ "$change_exit" -ne 0 ]; then
    echo "Investment system change evaluator failed; not reverting automatically." >&2
    exit "$change_exit"
fi
if [ "$tests_exit" -ne 0 ]; then
    exit "$tests_exit"
fi

echo "Wrote $SYSTEM_MD and $SYSTEM_JSON"
