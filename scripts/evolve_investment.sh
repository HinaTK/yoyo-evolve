#!/bin/bash
# scripts/evolve_investment.sh — autonomous investment research loop for HK and A-share stocks/ETFs.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -f "$ROOT_DIR/.env" ]; then
    while IFS='=' read -r key value; do
        key="${key#$'\xef\xbb\xbf'}"
        key="${key%$'\r'}"
        value="${value%$'\r'}"
        case "$key" in
            ''|'#'*) continue ;;
        esac
        case "$key" in
            *[!A-Za-z0-9_]*) continue ;;
        esac
        if [ -z "${!key+x}" ]; then
            export "$key=$value"
        fi
    done < "$ROOT_DIR/.env"
fi

DATE="${DATE:-$(date +%Y-%m-%d)}"
SESSION_TIME="${SESSION_TIME:-$(date +%H:%M)}"
SESSION="${SESSION:-close}"
MODEL="${MODEL:-claude-opus-4-6}"
PROVIDER="${PROVIDER:-anthropic}"
BASE_URL="${BASE_URL:-}"
TIMEOUT="${TIMEOUT:-900}"
YOYO_SKIP_PROJECT_CONTEXT="${YOYO_SKIP_PROJECT_CONTEXT:-true}"
PROMPT_PAUSE_SECONDS="${PROMPT_PAUSE_SECONDS:-0}"
PROMPT_PROVIDER_RETRIES="${PROMPT_PROVIDER_RETRIES:-3}"
PROVIDER_RETRY_SECONDS="${PROVIDER_RETRY_SECONDS:-120}"
SKIP_EXISTING_OUTPUTS="${SKIP_EXISTING_OUTPUTS:-true}"
INVESTMENT_LIGHT_CONTEXT="${INVESTMENT_LIGHT_CONTEXT:-true}"
FORCE_SNAPSHOT="${FORCE_SNAPSHOT:-false}"
ENABLE_SHADOW_LOGGING="${ENABLE_SHADOW_LOGGING:-true}"
if [ -z "${SNAPSHOT_FILE:-}" ]; then
    if [ "$SESSION" = "morning" ] || [ "$SESSION" = "midday" ]; then
        SNAPSHOT_FILE="$ROOT_DIR/data/snapshots/$DATE-$SESSION.json"
    else
        SNAPSHOT_FILE="$ROOT_DIR/data/snapshots/$DATE.json"
    fi
fi
WATCHLIST_CONFIG="${WATCHLIST_CONFIG:-$ROOT_DIR/config/watchlist.toml}"
TRADE_UNIVERSE_CONFIG="${TRADE_UNIVERSE_CONFIG:-$ROOT_DIR/config/trade_universe.toml}"
RADAR_CONFIG="${RADAR_CONFIG:-$ROOT_DIR/config/market_radar.toml}"
if [ -z "${RADAR_SNAPSHOT_FILE:-}" ]; then
    if [ "$SESSION" = "historical" ]; then
        RADAR_SNAPSHOT_FILE="$SNAPSHOT_FILE"
    elif [ "$SESSION" = "morning" ] || [ "$SESSION" = "midday" ]; then
        RADAR_SNAPSHOT_FILE="$ROOT_DIR/data/snapshots/$DATE-$SESSION-radar.json"
    else
        RADAR_SNAPSHOT_FILE="$ROOT_DIR/data/snapshots/$DATE-radar.json"
    fi
fi
YOYO_BIN="${YOYO_BIN:-$ROOT_DIR/target/debug/yoyo}"
if [ -z "${YOYO_BIN:-}" ] || [ "$YOYO_BIN" = "$ROOT_DIR/target/debug/yoyo" ]; then
    if [ -f "$ROOT_DIR/target/debug/yoyo.exe" ]; then
        YOYO_BIN="$ROOT_DIR/target/debug/yoyo.exe"
    fi
fi
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    if command -v python >/dev/null 2>&1; then
        PYTHON_BIN="python"
    fi
fi

cd "$ROOT_DIR"
export DATE
export SESSION
export SNAPSHOT_FILE
export RADAR_SNAPSHOT_FILE
export YOYO_SKIP_PROJECT_CONTEXT

python_path() {
    if command -v cygpath >/dev/null 2>&1; then
        cygpath -w "$1"
    else
        printf '%s\n' "$1"
    fi
}

case "$SESSION" in
    morning|midday|close|historical) ;;
    *)
        echo "Invalid SESSION '$SESSION'. Use morning, midday, close, or historical." >&2
        exit 2
        ;;
esac

if [ "$SESSION" = "historical" ]; then
    OUTPUT_STEM="$DATE"
    ALLOW_MEMORY_UPDATES="true"
else
    OUTPUT_STEM="$DATE-$SESSION"
    if [ "$SESSION" = "close" ]; then
        ALLOW_MEMORY_UPDATES="true"
    else
        ALLOW_MEMORY_UPDATES="false"
    fi
fi
RANKING_FILE="$ROOT_DIR/research/rankings/$OUTPUT_STEM-ranking.json"
RANKING_REL="research/rankings/$OUTPUT_STEM-ranking.json"
ACTIVE_STRATEGY_FILE="$ROOT_DIR/config/active_strategy.toml"
OPTIMIZATION_CONFIG="$ROOT_DIR/config/optimization.toml"
SYMBOL_RISK_FILE="$ROOT_DIR/research/experiments/symbol_risk_memory.json"
export RANKING_FILE
WATCHLIST_CONFIG_PY="$(python_path "$WATCHLIST_CONFIG")"
TRADE_UNIVERSE_CONFIG_PY="$(python_path "$TRADE_UNIVERSE_CONFIG")"
RADAR_CONFIG_PY="$(python_path "$RADAR_CONFIG")"
SNAPSHOT_FILE_PY="$(python_path "$SNAPSHOT_FILE")"
RADAR_SNAPSHOT_FILE_PY="$(python_path "$RADAR_SNAPSHOT_FILE")"
RANKING_FILE_PY="$(python_path "$RANKING_FILE")"
export SNAPSHOT_FILE_PY
export RADAR_SNAPSHOT_FILE_PY
export RANKING_FILE_PY

case "$SESSION" in
    morning)
        SESSION_GUIDANCE="This is a pre-market or early-session planning pass. Focus on watchlist priorities, trigger conditions, position sizing constraints, and what evidence would permit action today. Do not update long-term memory or the journal."
        ;;
    midday)
        SESSION_GUIDANCE="This is an intraday check. Focus on whether morning triggers are being confirmed or invalidated. Avoid strong conclusions unless the snapshot provides clear evidence. Do not update long-term memory or the journal."
        ;;
    close)
        SESSION_GUIDANCE="This is the official close-session daily review. Produce the durable recommendation set and update long-term memory only when posterior evidence shows repeated patterns."
        ;;
    historical)
        SESSION_GUIDANCE="This is a historical bootstrap replay. Produce durable baseline outputs and update long-term memory only when posterior evidence shows repeated patterns."
        ;;
esac

mkdir -p "$ROOT_DIR/data/snapshots" "$ROOT_DIR/research/daily" "$ROOT_DIR/research/theses" "$ROOT_DIR/research/calls" "$ROOT_DIR/research/evaluations" "$ROOT_DIR/research/rankings" "$ROOT_DIR/research/experiments" "$ROOT_DIR/research/risk" "$ROOT_DIR/research/shadow"

if [ -f "$ROOT_DIR/scripts/yoyo_context.sh" ]; then
    # shellcheck disable=SC1091
    source "$ROOT_DIR/scripts/yoyo_context.sh"
else
    YOYO_CONTEXT=""
fi

if [ "$SESSION" = "historical" ] && [ "$INVESTMENT_LIGHT_CONTEXT" = "true" ]; then
    YOYO_CONTEXT="Historical investment replay mode. Use the explicit investment profile, rules, memory, evaluation, snapshot, and ranking inputs below; do not rely on generic repository identity context."
fi

if [ "$FORCE_SNAPSHOT" = "true" ] || [ ! -f "$SNAPSHOT_FILE" ]; then
    "$PYTHON_BIN" "$ROOT_DIR/scripts/fetch_investment_data.py" --date "$DATE" --watchlist "$TRADE_UNIVERSE_CONFIG" --output-file "$SNAPSHOT_FILE"
fi

if [ "$RADAR_SNAPSHOT_FILE" != "$SNAPSHOT_FILE" ] && { [ "$FORCE_SNAPSHOT" = "true" ] || [ ! -f "$RADAR_SNAPSHOT_FILE" ]; }; then
    "$PYTHON_BIN" "$ROOT_DIR/scripts/fetch_investment_data.py" --date "$DATE" --watchlist "$RADAR_CONFIG" --output-file "$RADAR_SNAPSHOT_FILE"
fi

"$PYTHON_BIN" "$ROOT_DIR/scripts/build_snapshot_registry.py" \
    --snapshot-dir "$ROOT_DIR/data/snapshots" \
    --output "$ROOT_DIR/data/snapshots/registry.json"

if [ -f "$OPTIMIZATION_CONFIG" ]; then
    "$PYTHON_BIN" "$ROOT_DIR/scripts/optimize_investment_params.py" --config "$OPTIMIZATION_CONFIG" --as-of-date "$DATE" --session "$SESSION"
fi

if [ -f "$ROOT_DIR/research/evaluations/latest.json" ]; then
    "$PYTHON_BIN" "$ROOT_DIR/scripts/build_symbol_risk_memory.py" \
        --latest-json "$ROOT_DIR/research/evaluations/latest.json" \
        --output "$SYMBOL_RISK_FILE" \
        --as-of-date "$DATE" || true
fi

RANK_ARGS=$($PYTHON_BIN - <<'PY'
import pathlib, shlex, tomllib
profile = tomllib.load(open(pathlib.Path('config') / 'investment_profile.toml', 'rb'))
opt_path = pathlib.Path('config') / 'optimization.toml'
opt = tomllib.load(open(opt_path, 'rb')) if opt_path.exists() else {}
active_path = pathlib.Path('config') / 'active_strategy.toml'
active = tomllib.load(open(active_path, 'rb')) if active_path.exists() else {}
ranking = profile.get('ranking', {})
costs = profile.get('costs', {})
active_gate = active.get('cost_gate', {})
opt_safety = opt.get('safety_invariants', {})
active_safety = active.get('safety_invariants', {})
round_trip_bps = costs.get('estimated_round_trip_bps', 35)
minimum_edge_bps = costs.get('minimum_edge_bps', 100)
if active_safety.get('forbid_cost_gate_reduction', True) and opt_safety.get('forbid_cost_gate_reduction', True):
    round_trip_bps = max(float(round_trip_bps), float(active_gate.get('estimated_round_trip_bps', round_trip_bps)), float(opt.get('round_trip_bps', round_trip_bps)))
if active_safety.get('forbid_edge_gate_reduction', True) and opt_safety.get('forbid_edge_gate_reduction', True):
    minimum_edge_bps = max(float(minimum_edge_bps), float(active_gate.get('minimum_edge_bps', minimum_edge_bps)), float(opt.get('minimum_edge_bps', minimum_edge_bps)))
args = []
for name, value in [
    ('--max-candidates', ranking.get('max_candidates', 8)),
    ('--actionable-top-n', opt.get('actionable_top_n', ranking.get('actionable_top_n', 1))),
    ('--diagnostic-top-n', opt.get('diagnostic_top_n', opt.get('top_n', ranking.get('diagnostic_top_n', 3)))),
    ('--min-watch-score', ranking.get('min_watch_score', 45)),
    ('--min-action-score', ranking.get('min_action_score', 65)),
    ('--round-trip-bps', round_trip_bps),
    ('--minimum-edge-bps', minimum_edge_bps),
]:
    args.extend([name, str(value)])
print(' '.join(shlex.quote(arg) for arg in args))
PY
)
HORIZON_ARGS=$($PYTHON_BIN - <<'PY'
import pathlib, shlex, tomllib
profile = tomllib.load(open(pathlib.Path('config') / 'investment_profile.toml', 'rb'))
agent = profile.get('agent', {})
args = [
    '--horizon-days-min', str(agent.get('time_window_days_min', 14)),
    '--horizon-days-max', str(agent.get('time_window_days_max', 90)),
]
print(' '.join(shlex.quote(arg) for arg in args))
PY
)
SYMBOL_RISK_ARG=()
if [ -f "$SYMBOL_RISK_FILE" ]; then
    SYMBOL_RISK_ARG=(--symbol-risk-json "$SYMBOL_RISK_FILE")
fi
"$PYTHON_BIN" "$ROOT_DIR/scripts/rank_investment_universe.py" --snapshot "$SNAPSHOT_FILE" --output "$RANKING_FILE" --strategy-config "$ACTIVE_STRATEGY_FILE" "${SYMBOL_RISK_ARG[@]}" $RANK_ARGS

if [ "$ENABLE_SHADOW_LOGGING" = "true" ]; then
    SHADOW_FILE="$ROOT_DIR/research/shadow/$OUTPUT_STEM-shadow.json"
    if [ -z "${SHADOW_EVIDENCE_MODE:-}" ]; then
        if [ "$SESSION" = "historical" ]; then
            SHADOW_EVIDENCE_MODE="historical_replay"
        else
            SHADOW_EVIDENCE_MODE="forward_shadow"
        fi
    fi
    "$PYTHON_BIN" "$ROOT_DIR/scripts/log_investment_shadow.py" \
        --ranking "$RANKING_FILE" \
        --snapshot "$SNAPSHOT_FILE" \
        --date "$DATE" \
        --session "$SESSION" \
        --output "$SHADOW_FILE" \
        --evidence-mode "$SHADOW_EVIDENCE_MODE"
fi

if [ ! -f "$YOYO_BIN" ]; then
    echo "→ Building yoyo binary..."
    cargo build --quiet
fi

TIMEOUT_CMD="timeout"
if ! command -v timeout &>/dev/null; then
    if command -v gtimeout &>/dev/null; then
        TIMEOUT_CMD="gtimeout"
    else
        TIMEOUT_CMD=""
    fi
fi

PROFILE=$($PYTHON_BIN - <<'PY'
import pathlib, tomllib, json
root = pathlib.Path.cwd()
with open(root / 'config' / 'investment_profile.toml', 'rb') as f:
    print(json.dumps(tomllib.load(f), indent=2))
PY
)

PORTFOLIO=$($PYTHON_BIN - <<'PY'
import pathlib, tomllib, json
root = pathlib.Path.cwd()
with open(root / 'config' / 'portfolio.toml', 'rb') as f:
    print(json.dumps(tomllib.load(f), indent=2))
PY
)

WATCHLIST=$($PYTHON_BIN - <<PY
import pathlib, tomllib, json
with open(pathlib.Path(r'''$WATCHLIST_CONFIG_PY'''), 'rb') as f:
    print(json.dumps(tomllib.load(f), indent=2))
PY
)

TRADE_UNIVERSE=$($PYTHON_BIN - <<PY
import pathlib, tomllib, json
with open(pathlib.Path(r'''$TRADE_UNIVERSE_CONFIG_PY'''), 'rb') as f:
    print(json.dumps(tomllib.load(f), indent=2))
PY
)

RADAR_LIST=$($PYTHON_BIN - <<PY
import pathlib, tomllib, json
with open(pathlib.Path(r'''$RADAR_CONFIG_PY'''), 'rb') as f:
    print(json.dumps(tomllib.load(f), indent=2))
PY
)

SNAPSHOT=$($PYTHON_BIN - <<'PY'
import os, pathlib, sys
path = pathlib.Path(os.environ['SNAPSHOT_FILE_PY'])
if not path.exists():
    if os.environ.get('ALLOW_LATEST_SNAPSHOT_FALLBACK') != 'true':
        raise SystemExit(f"Missing required snapshot file: {path}")
    candidates = sorted(
        item for item in path.parent.glob('*.json')
        if item.name != 'registry.json' and not item.stem.endswith('-radar')
    )
    if not candidates:
        raise SystemExit(f"Missing required snapshot file and no fallback snapshots found: {path}")
    latest = candidates[-1]
    print(f"WARNING: using latest snapshot fallback for missing {path}: {latest}", file=sys.stderr)
    path = latest
print(path.read_text(encoding='utf-8'))
PY
)

RADAR_SNAPSHOT=$($PYTHON_BIN - <<'PY'
import os, pathlib, sys
path = pathlib.Path(os.environ['RADAR_SNAPSHOT_FILE_PY'])
if not path.exists():
    if os.environ.get('ALLOW_LATEST_SNAPSHOT_FALLBACK') != 'true':
        raise SystemExit(f"Missing required radar snapshot file: {path}")
    candidates = sorted(item for item in path.parent.glob('*-radar.json'))
    if not candidates:
        raise SystemExit(f"Missing required radar snapshot file and no fallback snapshots found: {path}")
    latest = candidates[-1]
    print(f"WARNING: using latest radar snapshot fallback for missing {path}: {latest}", file=sys.stderr)
    path = latest
print(path.read_text(encoding='utf-8'))
PY
)

RANKING=$($PYTHON_BIN - <<'PY'
import os, pathlib
path = pathlib.Path(os.environ['RANKING_FILE_PY'])
print(path.read_text(encoding='utf-8'))
PY
)

RULES=$(cat "$ROOT_DIR/memory/investment_rules.md")
ERRORS=$(cat "$ROOT_DIR/memory/investment_error_patterns.md")
ACTIVE_LEARNINGS=$(cat "$ROOT_DIR/memory/active_investment_learnings.md")

run_prompt() {
    local prompt_file="$1"
    local log_file="$2"
    local provider_args=(--provider "$PROVIDER" --model "$MODEL")
    if [ -n "$BASE_URL" ]; then
        provider_args+=(--base-url "$BASE_URL")
    fi
    local exe_path="$YOYO_BIN"
    local prompt_path="$prompt_file"
    if command -v cygpath >/dev/null 2>&1; then
        exe_path="$(cygpath -w "$YOYO_BIN")"
        prompt_path="$(cygpath -w "$prompt_file")"
    fi

    local attempt=1
    local max_attempts="$PROMPT_PROVIDER_RETRIES"
    while true; do
        local status=0
        set +e
        if [[ "$YOYO_BIN" == *.exe ]] && command -v powershell.exe >/dev/null 2>&1; then
            local ps_cmd
            ps_cmd="Get-Content -Raw '$prompt_path' | & '$exe_path'"
            for arg in "${provider_args[@]}"; do
                ps_cmd+=" '$arg'"
            done
            ps_cmd+=" --skills ./skills"
            if [ -n "$TIMEOUT_CMD" ]; then
                "$TIMEOUT_CMD" "$TIMEOUT" powershell.exe -NoProfile -Command "$ps_cmd" 2>&1 | tee "$log_file"
            else
                powershell.exe -NoProfile -Command "$ps_cmd" 2>&1 | tee "$log_file"
            fi
            status=${PIPESTATUS[0]}
        else
            if [ -n "$TIMEOUT_CMD" ]; then
                "$TIMEOUT_CMD" "$TIMEOUT" "$YOYO_BIN" "${provider_args[@]}" --skills ./skills < "$prompt_file" 2>&1 | tee "$log_file"
            else
                "$YOYO_BIN" "${provider_args[@]}" --skills ./skills < "$prompt_file" 2>&1 | tee "$log_file"
            fi
            status=${PIPESTATUS[0]}
        fi
        set -e

        if grep -Eiq '(^|[[:space:]])error: (Auth error|No API key found)|HTTP 401|Invalid API key|OPENAI_API_KEY is not set|ANTHROPIC_API_KEY is not set|API_KEY is not set' "$log_file"; then
            echo "Fatal provider error detected. See log: $log_file" >&2
            return 1
        fi

        if [ "$status" -eq 0 ]; then
            return 0
        fi

        if grep -Eiq 'Stream ended|Rate limited|Too Many Requests|HTTP 429|HTTP 503|Service Unavailable|auth_unavailable' "$log_file" && [ "$attempt" -lt "$max_attempts" ]; then
            local wait_seconds=15
            if grep -Eiq 'Rate limited|Too Many Requests|HTTP 429|HTTP 503|Service Unavailable|auth_unavailable' "$log_file"; then
                wait_seconds="$PROVIDER_RETRY_SECONDS"
            fi
            attempt=$((attempt + 1))
            echo "Transient provider error detected; retrying prompt attempt $attempt/$max_attempts after ${wait_seconds}s." >&2
            sleep "$wait_seconds"
            continue
        fi

        return "$status"
    done
}

require_output_file() {
    local path="$1"
    local label="$2"
    if [ ! -s "$path" ]; then
        echo "Expected $label output missing or empty: $path" >&2
        return 1
    fi
}

require_json_file() {
    local path="$1"
    require_output_file "$path" "JSON"
    "$PYTHON_BIN" - "$path" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
json.loads(path.read_text(encoding='utf-8'))
PY
}

pause_after_prompt() {
    if [ "${PROMPT_PAUSE_SECONDS:-0}" -gt 0 ]; then
        sleep "$PROMPT_PAUSE_SECONDS"
    fi
}

should_skip_output() {
    local path="$1"
    [ "$SKIP_EXISTING_OUTPUTS" = "true" ] && [ "${FORCE_REPLAY:-false}" != "true" ] && [ -s "$path" ]
}

run_markdown_stage() {
    local prompt_file="$1"
    local output_file="$2"
    local label="$3"
    if should_skip_output "$output_file"; then
        echo "Skip $label: existing output found at $output_file"
    else
        run_prompt "$prompt_file" "$(mktemp)"
    fi
    require_output_file "$output_file" "$label"
    pause_after_prompt
}

run_json_stage() {
    local prompt_file="$1"
    local output_file="$2"
    if should_skip_output "$output_file"; then
        echo "Skip JSON: existing output found at $output_file"
    else
        run_prompt "$prompt_file" "$(mktemp)"
    fi
    require_json_file "$output_file"
    if [ "${CALLS_FILE:-}" = "$output_file" ]; then
        "$PYTHON_BIN" "$ROOT_DIR/scripts/validate_investment_calls.py" \
            --calls "$output_file" \
            --ranking "$RANKING_FILE" \
            --trade-universe "$TRADE_UNIVERSE_CONFIG" \
            --draft-calls "$DRAFT_CALLS_FILE" \
            --risk-review "$RISK_REVIEW_FILE"
    fi
    pause_after_prompt
}

ASSESSMENT_REL="research/daily/$OUTPUT_STEM-market-assessment.md"
PLAN_REL="research/daily/$OUTPUT_STEM-plan.md"
REPORT_REL="research/daily/$OUTPUT_STEM-report.md"
CALLS_REL="research/calls/$OUTPUT_STEM-calls.json"
DRAFT_CALLS_REL="research/calls/$OUTPUT_STEM-draft-policy.json"
RISK_REVIEW_REL="research/risk/$OUTPUT_STEM-risk-review.json"
REFLECTION_REL="research/daily/$OUTPUT_STEM-reflection.md"
EVALUATION_REL="research/evaluations/latest.md"
OPTIMIZATION_REL="research/experiments/latest_optimization.md"
RUN_MANIFEST_REL="research/runs/$OUTPUT_STEM/manifest.json"
JOURNAL_REL="journals/investment_journal.md"

ASSESSMENT_FILE="$ROOT_DIR/$ASSESSMENT_REL"
PLAN_FILE="$ROOT_DIR/$PLAN_REL"
REPORT_FILE="$ROOT_DIR/$REPORT_REL"
CALLS_FILE="$ROOT_DIR/$CALLS_REL"
DRAFT_CALLS_FILE="$ROOT_DIR/$DRAFT_CALLS_REL"
RISK_REVIEW_FILE="$ROOT_DIR/$RISK_REVIEW_REL"
REFLECTION_FILE="$ROOT_DIR/$REFLECTION_REL"
EVALUATION_FILE="$ROOT_DIR/$EVALUATION_REL"
OPTIMIZATION_FILE="$ROOT_DIR/$OPTIMIZATION_REL"
RUN_MANIFEST_FILE="$ROOT_DIR/$RUN_MANIFEST_REL"
JOURNAL_FILE="$ROOT_DIR/$JOURNAL_REL"

write_run_manifest() {
    "$PYTHON_BIN" "$ROOT_DIR/scripts/create_investment_run_manifest.py" \
        --date "$DATE" \
        --session "$SESSION" \
        --as-of-date "$DATE" \
        --as-of-session "$SESSION" \
        --model "$MODEL" \
        --provider "$PROVIDER" \
        --runs-root "$ROOT_DIR/research/runs" \
        --file investment_profile "$ROOT_DIR/config/investment_profile.toml" \
        --file active_strategy "$ACTIVE_STRATEGY_FILE" \
        --file optimization_config "$OPTIMIZATION_CONFIG" \
        --file trade_universe "$TRADE_UNIVERSE_CONFIG" \
        --file market_radar "$RADAR_CONFIG" \
        --file trade_snapshot "$SNAPSHOT_FILE" \
        --file radar_snapshot "$RADAR_SNAPSHOT_FILE" \
        --file ranking "$RANKING_FILE" \
        --file draft_calls "$DRAFT_CALLS_FILE" \
        --file risk_review "$RISK_REVIEW_FILE" \
        --file final_calls "$CALLS_FILE" \
        --file market_assessment "$ASSESSMENT_FILE" \
        --file daily_plan "$PLAN_FILE" \
        --file daily_report "$REPORT_FILE" \
        --file reflection "$REFLECTION_FILE" \
        --file evaluation "$ROOT_DIR/research/evaluations/latest.json"
}

write_run_manifest

"$PYTHON_BIN" "$ROOT_DIR/scripts/generate_investment_draft_calls.py" \
    --ranking "$RANKING_FILE" \
    --output "$DRAFT_CALLS_FILE" \
    --date "$DATE" \
    --session "$SESSION" \
    $HORIZON_ARGS \
    --include-diagnostics

write_run_manifest

RISK_ARGS=()
if [ -f "$SYMBOL_RISK_FILE" ]; then
    RISK_ARGS=(--symbol-risk-json "$SYMBOL_RISK_FILE")
fi
mkdir -p "$(dirname "$RISK_REVIEW_FILE")"
"$PYTHON_BIN" "$ROOT_DIR/scripts/generate_investment_risk_review.py" \
    --draft-calls "$DRAFT_CALLS_FILE" \
    --ranking "$RANKING_FILE" \
    --investment-profile "$ROOT_DIR/config/investment_profile.toml" \
    "${RISK_ARGS[@]}" \
    --output "$RISK_REVIEW_FILE"

write_run_manifest

"$PYTHON_BIN" "$ROOT_DIR/scripts/validate_investment_calls.py" \
    --calls "$DRAFT_CALLS_FILE" \
    --ranking "$RANKING_FILE" \
    --trade-universe "$TRADE_UNIVERSE_CONFIG"

"$PYTHON_BIN" "$ROOT_DIR/scripts/evaluate_investment_calls.py" \
    --calls-dir "$ROOT_DIR/research/calls" \
    --snapshot-dir "$ROOT_DIR/data/snapshots" \
    --summary-md "$EVALUATION_FILE" \
    --summary-json "$ROOT_DIR/research/evaluations/latest.json" \
    --records-json "$ROOT_DIR/research/evaluations/latest_records.json" \
    --as-of-date "$DATE" \
    --as-of-session "$SESSION"

EVALUATION_SUMMARY=$(cat "$EVALUATION_FILE")
if [ -f "$OPTIMIZATION_FILE" ]; then
    OPTIMIZATION_SUMMARY=$(cat "$OPTIMIZATION_FILE")
else
    OPTIMIZATION_SUMMARY="No parameter optimization summary is available yet."
fi

ASSESS_PROMPT=$(mktemp)
cat > "$ASSESS_PROMPT" <<EOF
You are yoyo-invest. Today is $DATE $SESSION_TIME. Session: $SESSION.

$YOYO_CONTEXT

Use the investment-loop skill.

Session guidance: $SESSION_GUIDANCE

Language requirement: write all human-readable analysis in Simplified Chinese. Keep ticker symbols, JSON keys, enum values, and file paths exactly as specified.

Your job: write a market assessment to $ASSESSMENT_REL.

Inputs:
- Investment profile:
$PROFILE
- Portfolio:
$PORTFOLIO
- Watchlist:
$WATCHLIST
- Trade universe:
$TRADE_UNIVERSE
- Market radar universe:
$RADAR_LIST
- Market radar snapshot:
$RADAR_SNAPSHOT
- Trade candidate snapshot:
$SNAPSHOT
- Deterministic trade universe ranking:
$RANKING
- Stable rules:
$RULES
- Error patterns:
$ERRORS
- Active learnings:
$ACTIVE_LEARNINGS
- Posterior evaluation summary:
$EVALUATION_SUMMARY
- Parameter optimization summary:
$OPTIMIZATION_SUMMARY

Output requirements:
- Write the markdown report in Simplified Chinese.
- Keep facts separate from interpretations.
- First summarize market radar results by sector/theme strength, then explain which radar themes are actionable inside the trade universe.
- Cover market regime, theme strength, ETF confirmation, standout names, and risk posture.
- If a radar theme is strong but not represented in the trade universe, say it is an external opportunity to consider adding later, not an immediate recommendation.
- If a radar theme is represented in the trade universe, compare the available symbols and identify the best current expression of that theme.
- Treat actionable_candidates as the only deterministic layer eligible for upgrade consideration; use diagnostic_candidates only for observation and explanation.
- End with 3-5 high-priority research questions for today.
- Save only markdown to $ASSESSMENT_REL.
EOF

PLAN_PROMPT=$(mktemp)
cat > "$PLAN_PROMPT" <<EOF
You are yoyo-invest. Today is $DATE $SESSION_TIME. Session: $SESSION.

$YOYO_CONTEXT

Use the investment-loop skill.

Session guidance: $SESSION_GUIDANCE

Language requirement: write all human-readable analysis in Simplified Chinese. Keep ticker symbols, JSON keys, enum values, and file paths exactly as specified.

Your job: write a focused daily plan to $PLAN_REL.

Inputs:
- Market assessment:
$( [ -f "$ASSESSMENT_FILE" ] && cat "$ASSESSMENT_FILE" )
- Investment profile:
$PROFILE
- Portfolio:
$PORTFOLIO
- Trade universe:
$TRADE_UNIVERSE
- Market radar snapshot:
$RADAR_SNAPSHOT
- Trade universe snapshot:
$SNAPSHOT
- Deterministic trade universe ranking:
$RANKING
- Stable rules:
$RULES
- Active learnings:
$ACTIVE_LEARNINGS
- Posterior evaluation summary:
$EVALUATION_SUMMARY
- Parameter optimization summary:
$OPTIMIZATION_SUMMARY

Plan requirements:
- Write the markdown plan in Simplified Chinese.
- Treat missing real holdings as recommendation-only mode: rank candidates for possible action, not as live portfolio management.
- Start with a "市场雷达结论" section: strongest themes, weakest themes, and any opportunity not covered by the current trade universe.
- Pick at most 5 candidates from the configured trade universe, not only the focused watchlist.
- For each strong theme, compare same-theme symbols in the trade universe and explain why the selected symbol is currently better than its peers.
- For each candidate, state why it deserves attention today.
- For each candidate, list missing evidence required before any upgrade to accumulate/buy.
- Only actionable_candidates may be considered for upgrade; diagnostic_candidates are watch/avoid diagnostics only.
- Include a clear "今日优先级" section ranking candidates from strongest to weakest.
- Include one section called "Disqualifiers" for cases that force watch_only or avoid.
- Save only markdown to $PLAN_REL.
EOF

REPORT_PROMPT=$(mktemp)
cat > "$REPORT_PROMPT" <<EOF
You are yoyo-invest. Today is $DATE $SESSION_TIME. Session: $SESSION.

$YOYO_CONTEXT

Use the investment-loop skill.

Session guidance: $SESSION_GUIDANCE

Language requirement: write all human-readable analysis in Simplified Chinese. Keep ticker symbols, JSON keys, enum values, and file paths exactly as specified.

Your job: write the daily recommendation report to $REPORT_REL.

Inputs:
- Market assessment:
$( [ -f "$ASSESSMENT_FILE" ] && cat "$ASSESSMENT_FILE" )
- Daily plan:
$( [ -f "$PLAN_FILE" ] && cat "$PLAN_FILE" )
- Market snapshot:
$SNAPSHOT
- Trade universe:
$TRADE_UNIVERSE
- Market radar snapshot:
$RADAR_SNAPSHOT
- Deterministic trade universe ranking:
$RANKING
- Stable rules:
$RULES
- Error patterns:
$ERRORS
- Active learnings:
$ACTIVE_LEARNINGS
- Posterior evaluation summary:
$EVALUATION_SUMMARY
- Parameter optimization summary:
$OPTIMIZATION_SUMMARY

Report requirements:
- Write the markdown report in Simplified Chinese.
- For every symbol, show the code in both forms when useful: 3033.HK and HKEX:3033; clearly state whether it is a stock or ETF and include the configured Chinese/common name.
- If portfolio mode is recommendation_only, explicitly say this is candidate recommendation mode, not real-position management; do not treat 100% cash as a portfolio decision.
- Provide a top section called "今日结论" with three buckets: "可重点观察", "触发后才考虑", and "暂时回避/低优先级".
- Include a "市场雷达" section before top candidates. Name the strongest/weakest radar themes, and clearly separate "雷达发现" from "当前交易池内建议".
- Do not recommend radar-only symbols as trades unless they are also present in the configured trade universe; instead list them under "可考虑加入交易池".
- For dynamic symbol selection, include a "为什么选它而不是同主题其他标的" paragraph for each top candidate.
- Use the deterministic ranking as the starting point. You may override it only if you explicitly explain the evidence-based reason.
- Treat diagnostic_only=true or qualified_for_watch=false ranking rows as diagnostics only; do not upgrade them to actionable recommendations.
- Treat actionable_candidates as the only deterministic layer eligible for buy_candidate/accumulate/hold consideration; diagnostic_candidates can only explain watch_only/avoid context.
- Prefer is_theme_leader=true rows for each theme; do not upgrade same-theme non-leaders unless the report gives explicit evidence that overrides the deterministic theme rank.
- Do not upgrade to buy_candidate, hold, or accumulate unless the setup passes the cost gate in the ranking file.
- Provide sections for market regime, top candidates, avoids, and portfolio posture.
- Every recommendation must include: state, rationale, evidence, risks, invalidation, horizon, confidence.
- Use buy_candidate only when the current snapshot already supports an actionable candidate; otherwise use watch_only with exact trigger conditions.
- If evidence is weak, use watch_only.
- Do not invent catalysts that are absent from the snapshot.
- Save only markdown to $REPORT_REL.
EOF

CALLS_PROMPT=$(mktemp)
cat > "$CALLS_PROMPT" <<EOF
You are yoyo-invest. Today is $DATE $SESSION_TIME. Session: $SESSION.

$YOYO_CONTEXT

Use the investment-loop skill.

Session guidance: $SESSION_GUIDANCE

Language requirement: keep JSON keys and enum values in English exactly as specified, but write human-readable string values in Simplified Chinese where possible.

Your job: convert today's report into structured machine-readable recommendations and save them to $CALLS_REL.

Inputs:
- Daily report:
$( [ -f "$REPORT_FILE" ] && cat "$REPORT_FILE" )
- Watchlist:
$WATCHLIST
- Trade universe:
$TRADE_UNIVERSE
- Market radar snapshot:
$RADAR_SNAPSHOT
- Trade candidate snapshot:
$SNAPSHOT
- Deterministic trade universe ranking:
$RANKING
- Deterministic draft policy calls:
$( [ -f "$DRAFT_CALLS_FILE" ] && cat "$DRAFT_CALLS_FILE" )
- Deterministic risk review:
$( [ -f "$RISK_REVIEW_FILE" ] && cat "$RISK_REVIEW_FILE" )
- Parameter optimization summary:
$OPTIMIZATION_SUMMARY

Output requirements:
- Write valid JSON only.
- Keep JSON keys and enum values in English exactly as specified.
- Write human-readable values such as rationale, evidence, risks, and invalidation in Simplified Chinese.
- Actionable recommendations should come only from actionable_candidates in the deterministic ranking. Diagnostic candidates may only become watch/avoid rows when the report discussed them.
- Start from the deterministic draft policy calls. You may explain or downgrade draft recommendations, but do not upgrade any row beyond the deterministic draft state.
- Apply the deterministic risk review as a hard second-layer cap: no final state may exceed final_state_cap, veto means avoid, and downgrade means watch_only unless the risk review says otherwise.
- Include risk review reasons and required_confirmations in each affected recommendation's risks, evidence, or invalidation text.
- Do not turn diagnostic_only=true or qualified_for_watch=false rows into actionable states; they may only appear as watch/avoid diagnostics when the report discussed them.
- Do not turn qualified_for_action=false rows into buy_candidate, accumulate, or hold.
- If is_theme_leader=false, keep the state non-actionable unless selection_reason explains why it is better than the deterministic same-theme leader.
- Do not use actionable states unless the ranking score and cost gate support enough expected edge.
- Use this exact schema:
  {
    "date": "$DATE",
    "session": "$SESSION",
    "generated_at": "ISO-8601 UTC timestamp",
    "strategy_version": "copy from deterministic ranking strategy_version",
    "strategy_weights": "copy from deterministic ranking strategy_weights object",
    "recommendations": [
        {
          "symbol": "0700.HK",
          "state": "watch_only|buy_candidate|accumulate|hold|trim|sell_candidate|avoid",
        "theme": "string",
        "kind": "stock|etf",
        "horizon_days_min": 14,
        "horizon_days_max": 90,
        "confidence": 0.0,
        "rationale": "short string",
        "evidence": ["fact 1", "fact 2"],
        "risks": ["risk 1", "risk 2"],
          "invalidation": "single string",
          "selection_source_theme": "theme that caused this symbol to be selected",
          "selection_reason": "why this symbol was selected over same-theme alternatives"
        }
      ]
    }
- Include only symbols that appear in today's report as actionable, watch, or avoid names.
- Include only configured trade universe symbols in recommendations. Do not include radar-only symbols in this JSON.
- Save only JSON to $CALLS_REL.
EOF

REFLECT_PROMPT=$(mktemp)
cat > "$REFLECT_PROMPT" <<EOF
You are yoyo-invest. Today is $DATE $SESSION_TIME. Session: $SESSION.

$YOYO_CONTEXT

Use the investment-loop skill.

Session guidance: $SESSION_GUIDANCE

Language requirement: write all human-readable reflection content, journal entries, and memory updates in Simplified Chinese. Keep ticker symbols, JSON keys, enum values, and file paths exactly as specified.

Your job:
1. Write a reflection to $REFLECTION_REL.
2. If memory updates are allowed, append a short dated entry to $JOURNAL_REL.

Inputs:
- Market assessment:
$( [ -f "$ASSESSMENT_FILE" ] && cat "$ASSESSMENT_FILE" )
- Daily plan:
$( [ -f "$PLAN_FILE" ] && cat "$PLAN_FILE" )
- Daily report:
$( [ -f "$REPORT_FILE" ] && cat "$REPORT_FILE" )
- Trade universe snapshot:
$SNAPSHOT
- Deterministic trade universe ranking:
$RANKING
- Stable rules:
$RULES
- Error patterns:
$ERRORS
- Active learnings:
$ACTIVE_LEARNINGS
- Posterior evaluation summary:
$EVALUATION_SUMMARY
- Parameter optimization summary:
$OPTIMIZATION_SUMMARY

Reflection requirements:
- Write the reflection in Simplified Chinese.
- Record where confidence is weakest.
- State what evidence is still missing.
- Name 1-3 likely failure modes for today's recommendations.
- If any recommendation came from dynamic symbol selection, classify likely future errors as theme error, symbol-selection error, timing error, or risk-control error.
- Suggest concrete priority shifts for the next cycle.
- Memory updates allowed: $ALLOW_MEMORY_UPDATES.
- If memory updates are allowed and posterior evaluation shows repeated patterns, update:
  - memory/active_investment_learnings.md
  - memory/investment_rules.md
  - memory/investment_error_patterns.md
  Keep changes concise and operational.
- When a selected symbol underperforms same-theme alternatives, update memory with a more precise selection rule rather than only downgrading the whole theme.
- If memory updates are not allowed, do not edit memory files and do not append to $JOURNAL_REL; keep this as an intraday working note only.
EOF

run_markdown_stage "$ASSESS_PROMPT" "$ASSESSMENT_FILE" "market assessment"
run_markdown_stage "$PLAN_PROMPT" "$PLAN_FILE" "daily plan"
run_markdown_stage "$REPORT_PROMPT" "$REPORT_FILE" "daily report"
run_json_stage "$CALLS_PROMPT" "$CALLS_FILE"
run_markdown_stage "$REFLECT_PROMPT" "$REFLECTION_FILE" "reflection"

write_run_manifest

rm -f "$ASSESS_PROMPT" "$PLAN_PROMPT" "$REPORT_PROMPT" "$CALLS_PROMPT" "$REFLECT_PROMPT"

echo "=== Investment loop complete ==="
echo "Assessment: $ASSESSMENT_FILE"
echo "Plan:       $PLAN_FILE"
echo "Report:     $REPORT_FILE"
echo "Calls:      $CALLS_FILE"
echo "Reflection: $REFLECTION_FILE"
