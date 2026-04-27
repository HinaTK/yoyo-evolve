#!/bin/bash
# scripts/evolve_investment.sh — autonomous investment research loop for hk stocks and ETFs.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -f "$ROOT_DIR/.env" ]; then
    while IFS='=' read -r key value; do
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
FORCE_SNAPSHOT="${FORCE_SNAPSHOT:-false}"
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

mkdir -p "$ROOT_DIR/data/snapshots" "$ROOT_DIR/research/daily" "$ROOT_DIR/research/theses" "$ROOT_DIR/research/calls" "$ROOT_DIR/research/evaluations" "$ROOT_DIR/research/rankings"

if [ -f "$ROOT_DIR/scripts/yoyo_context.sh" ]; then
    # shellcheck disable=SC1091
    source "$ROOT_DIR/scripts/yoyo_context.sh"
else
    YOYO_CONTEXT=""
fi

if [ "$FORCE_SNAPSHOT" = "true" ] || [ ! -f "$SNAPSHOT_FILE" ]; then
    "$PYTHON_BIN" "$ROOT_DIR/scripts/fetch_investment_data.py" --date "$DATE" --watchlist "$TRADE_UNIVERSE_CONFIG" --output-file "$SNAPSHOT_FILE"
fi

if [ "$RADAR_SNAPSHOT_FILE" != "$SNAPSHOT_FILE" ] && { [ "$FORCE_SNAPSHOT" = "true" ] || [ ! -f "$RADAR_SNAPSHOT_FILE" ]; }; then
    "$PYTHON_BIN" "$ROOT_DIR/scripts/fetch_investment_data.py" --date "$DATE" --watchlist "$RADAR_CONFIG" --output-file "$RADAR_SNAPSHOT_FILE"
fi

RANK_ARGS=$($PYTHON_BIN - <<'PY'
import pathlib, shlex, tomllib
profile = tomllib.load(open(pathlib.Path('config') / 'investment_profile.toml', 'rb'))
ranking = profile.get('ranking', {})
costs = profile.get('costs', {})
args = []
for name, value in [
    ('--max-candidates', ranking.get('max_candidates', 8)),
    ('--min-watch-score', ranking.get('min_watch_score', 45)),
    ('--min-action-score', ranking.get('min_action_score', 65)),
    ('--round-trip-bps', costs.get('estimated_round_trip_bps', 35)),
    ('--minimum-edge-bps', costs.get('minimum_edge_bps', 100)),
]:
    args.extend([name, str(value)])
print(' '.join(shlex.quote(arg) for arg in args))
PY
)
"$PYTHON_BIN" "$ROOT_DIR/scripts/rank_investment_universe.py" --snapshot "$SNAPSHOT_FILE" --output "$RANKING_FILE" $RANK_ARGS

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
import os, pathlib
path = pathlib.Path(os.environ['SNAPSHOT_FILE_PY'])
if not path.exists():
    latest = sorted(path.parent.glob('*.json'))[-1]
    path = latest
print(path.read_text(encoding='utf-8'))
PY
)

RADAR_SNAPSHOT=$($PYTHON_BIN - <<'PY'
import os, pathlib
path = pathlib.Path(os.environ['RADAR_SNAPSHOT_FILE_PY'])
if not path.exists():
    latest = sorted(path.parent.glob('*.json'))[-1]
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
        return
    fi

    if [ -n "$TIMEOUT_CMD" ]; then
        "$TIMEOUT_CMD" "$TIMEOUT" "$YOYO_BIN" "${provider_args[@]}" --skills ./skills < "$prompt_file" 2>&1 | tee "$log_file"
    else
        "$YOYO_BIN" "${provider_args[@]}" --skills ./skills < "$prompt_file" 2>&1 | tee "$log_file"
    fi
}

ASSESSMENT_REL="research/daily/$OUTPUT_STEM-market-assessment.md"
PLAN_REL="research/daily/$OUTPUT_STEM-plan.md"
REPORT_REL="research/daily/$OUTPUT_STEM-report.md"
CALLS_REL="research/calls/$OUTPUT_STEM-calls.json"
REFLECTION_REL="research/daily/$OUTPUT_STEM-reflection.md"
EVALUATION_REL="research/evaluations/latest.md"
JOURNAL_REL="journals/investment_journal.md"

ASSESSMENT_FILE="$ROOT_DIR/$ASSESSMENT_REL"
PLAN_FILE="$ROOT_DIR/$PLAN_REL"
REPORT_FILE="$ROOT_DIR/$REPORT_REL"
CALLS_FILE="$ROOT_DIR/$CALLS_REL"
REFLECTION_FILE="$ROOT_DIR/$REFLECTION_REL"
EVALUATION_FILE="$ROOT_DIR/$EVALUATION_REL"
JOURNAL_FILE="$ROOT_DIR/$JOURNAL_REL"

"$PYTHON_BIN" "$ROOT_DIR/scripts/evaluate_investment_calls.py" \
    --calls-dir "$ROOT_DIR/research/calls" \
    --snapshot-dir "$ROOT_DIR/data/snapshots" \
    --summary-md "$EVALUATION_FILE" \
    --summary-json "$ROOT_DIR/research/evaluations/latest.json"

EVALUATION_SUMMARY=$(cat "$EVALUATION_FILE")

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

Output requirements:
- Write the markdown report in Simplified Chinese.
- Keep facts separate from interpretations.
- First summarize market radar results by sector/theme strength, then explain which radar themes are actionable inside the trade universe.
- Cover market regime, theme strength, ETF confirmation, standout names, and risk posture.
- If a radar theme is strong but not represented in the trade universe, say it is an external opportunity to consider adding later, not an immediate recommendation.
- If a radar theme is represented in the trade universe, compare the available symbols and identify the best current expression of that theme.
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

Plan requirements:
- Write the markdown plan in Simplified Chinese.
- Treat missing real holdings as recommendation-only mode: rank candidates for possible action, not as live portfolio management.
- Start with a "市场雷达结论" section: strongest themes, weakest themes, and any opportunity not covered by the current trade universe.
- Pick at most 5 candidates from the configured trade universe, not only the focused watchlist.
- For each strong theme, compare same-theme symbols in the trade universe and explain why the selected symbol is currently better than its peers.
- For each candidate, state why it deserves attention today.
- For each candidate, list missing evidence required before any upgrade to accumulate/buy.
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

Report requirements:
- Write the markdown report in Simplified Chinese.
- For every symbol, show the code in both forms when useful: 3033.HK and HKEX:3033; clearly state whether it is a stock or ETF and include the configured Chinese/common name.
- If portfolio mode is recommendation_only, explicitly say this is candidate recommendation mode, not real-position management; do not treat 100% cash as a portfolio decision.
- Provide a top section called "今日结论" with three buckets: "可重点观察", "触发后才考虑", and "暂时回避/低优先级".
- Include a "市场雷达" section before top candidates. Name the strongest/weakest radar themes, and clearly separate "雷达发现" from "当前交易池内建议".
- Do not recommend radar-only symbols as trades unless they are also present in the configured trade universe; instead list them under "可考虑加入交易池".
- For dynamic symbol selection, include a "为什么选它而不是同主题其他标的" paragraph for each top candidate.
- Use the deterministic ranking as the starting point. You may override it only if you explicitly explain the evidence-based reason.
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

Output requirements:
- Write valid JSON only.
- Keep JSON keys and enum values in English exactly as specified.
- Write human-readable values such as rationale, evidence, risks, and invalidation in Simplified Chinese.
- Recommendations should normally come from top_candidates in the deterministic ranking. If you include a lower-ranked symbol, explain why in selection_reason.
- Do not use actionable states unless the ranking score and cost gate support enough expected edge.
- Use this exact schema:
  {
    "date": "$DATE",
    "session": "$SESSION",
    "generated_at": "ISO-8601 UTC timestamp",
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

run_prompt "$ASSESS_PROMPT" "$(mktemp)"
run_prompt "$PLAN_PROMPT" "$(mktemp)"
run_prompt "$REPORT_PROMPT" "$(mktemp)"
run_prompt "$CALLS_PROMPT" "$(mktemp)"
run_prompt "$REFLECT_PROMPT" "$(mktemp)"

rm -f "$ASSESS_PROMPT" "$PLAN_PROMPT" "$REPORT_PROMPT" "$CALLS_PROMPT" "$REFLECT_PROMPT"

echo "=== Investment loop complete ==="
echo "Assessment: $ASSESSMENT_FILE"
echo "Plan:       $PLAN_FILE"
echo "Report:     $REPORT_FILE"
echo "Calls:      $CALLS_FILE"
echo "Reflection: $REFLECTION_FILE"
