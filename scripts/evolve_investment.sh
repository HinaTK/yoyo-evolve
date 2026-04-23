#!/bin/bash
# scripts/evolve_investment.sh — autonomous investment research loop for hk stocks and ETFs.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATE=$(date +%Y-%m-%d)
SESSION_TIME=$(date +%H:%M)
MODEL="${MODEL:-claude-opus-4-6}"
TIMEOUT="${TIMEOUT:-900}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-$ROOT_DIR/data/snapshots/$DATE.json}"
YOYO_BIN="${YOYO_BIN:-$ROOT_DIR/target/debug/yoyo}"

cd "$ROOT_DIR"
export DATE

mkdir -p "$ROOT_DIR/data/snapshots" "$ROOT_DIR/research/daily" "$ROOT_DIR/research/theses"

if [ -f "$ROOT_DIR/scripts/yoyo_context.sh" ]; then
    # shellcheck disable=SC1091
    source "$ROOT_DIR/scripts/yoyo_context.sh"
else
    YOYO_CONTEXT=""
fi

if [ ! -f "$SNAPSHOT_FILE" ]; then
    python3 "$ROOT_DIR/scripts/fetch_investment_data.py" --date "$DATE"
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

PROFILE=$(python3 - <<'PY'
import pathlib, tomllib, json
root = pathlib.Path.cwd()
with open(root / 'config' / 'investment_profile.toml', 'rb') as f:
    print(json.dumps(tomllib.load(f), indent=2))
PY
)

PORTFOLIO=$(python3 - <<'PY'
import pathlib, tomllib, json
root = pathlib.Path.cwd()
with open(root / 'config' / 'portfolio.toml', 'rb') as f:
    print(json.dumps(tomllib.load(f), indent=2))
PY
)

WATCHLIST=$(python3 - <<'PY'
import pathlib, tomllib, json
root = pathlib.Path.cwd()
with open(root / 'config' / 'watchlist.toml', 'rb') as f:
    print(json.dumps(tomllib.load(f), indent=2))
PY
)

SNAPSHOT=$(python3 - <<'PY'
import os, pathlib
path = pathlib.Path(os.environ['SNAPSHOT_FILE'])
if not path.exists():
    latest = sorted(path.parent.glob('*.json'))[-1]
    path = latest
print(path.read_text(encoding='utf-8'))
PY
)

RULES=$(cat "$ROOT_DIR/memory/investment_rules.md")
ERRORS=$(cat "$ROOT_DIR/memory/investment_error_patterns.md")

run_prompt() {
    local prompt_file="$1"
    local log_file="$2"
    if [ -n "$TIMEOUT_CMD" ]; then
        "$TIMEOUT_CMD" "$TIMEOUT" "$YOYO_BIN" --model "$MODEL" --skills ./skills < "$prompt_file" 2>&1 | tee "$log_file"
    else
        "$YOYO_BIN" --model "$MODEL" --skills ./skills < "$prompt_file" 2>&1 | tee "$log_file"
    fi
}

ASSESSMENT_FILE="$ROOT_DIR/research/daily/$DATE-market-assessment.md"
PLAN_FILE="$ROOT_DIR/research/daily/$DATE-plan.md"
REPORT_FILE="$ROOT_DIR/research/daily/$DATE-report.md"
REFLECTION_FILE="$ROOT_DIR/research/daily/$DATE-reflection.md"
JOURNAL_FILE="$ROOT_DIR/journals/investment_journal.md"

ASSESS_PROMPT=$(mktemp)
cat > "$ASSESS_PROMPT" <<EOF
You are yoyo-invest. Today is $DATE $SESSION_TIME.

$YOYO_CONTEXT

Use the investment-loop skill.

Your job: write a market assessment to $ASSESSMENT_FILE.

Inputs:
- Investment profile:
$PROFILE
- Portfolio:
$PORTFOLIO
- Watchlist:
$WATCHLIST
- Market snapshot:
$SNAPSHOT
- Stable rules:
$RULES
- Error patterns:
$ERRORS

Output requirements:
- Keep facts separate from interpretations.
- Cover market regime, theme strength, ETF confirmation, standout names, and risk posture.
- End with 3-5 high-priority research questions for today.
- Save only markdown to $ASSESSMENT_FILE.
EOF

PLAN_PROMPT=$(mktemp)
cat > "$PLAN_PROMPT" <<EOF
You are yoyo-invest. Today is $DATE $SESSION_TIME.

$YOYO_CONTEXT

Use the investment-loop skill.

Your job: write a focused daily plan to $PLAN_FILE.

Inputs:
- Market assessment:
$( [ -f "$ASSESSMENT_FILE" ] && cat "$ASSESSMENT_FILE" )
- Investment profile:
$PROFILE
- Portfolio:
$PORTFOLIO
- Stable rules:
$RULES

Plan requirements:
- Pick at most 5 candidates from the configured watchlist.
- For each candidate, state why it deserves attention today.
- For each candidate, list missing evidence required before any upgrade to accumulate/buy.
- Include one section called "Disqualifiers" for cases that force watch_only or avoid.
- Save only markdown to $PLAN_FILE.
EOF

REPORT_PROMPT=$(mktemp)
cat > "$REPORT_PROMPT" <<EOF
You are yoyo-invest. Today is $DATE $SESSION_TIME.

$YOYO_CONTEXT

Use the investment-loop skill.

Your job: write the daily recommendation report to $REPORT_FILE.

Inputs:
- Market assessment:
$( [ -f "$ASSESSMENT_FILE" ] && cat "$ASSESSMENT_FILE" )
- Daily plan:
$( [ -f "$PLAN_FILE" ] && cat "$PLAN_FILE" )
- Market snapshot:
$SNAPSHOT
- Stable rules:
$RULES
- Error patterns:
$ERRORS

Report requirements:
- Provide sections for market regime, top candidates, avoids, and portfolio posture.
- Every recommendation must include: state, rationale, evidence, risks, invalidation, horizon, confidence.
- If evidence is weak, use watch_only.
- Do not invent catalysts that are absent from the snapshot.
- Save only markdown to $REPORT_FILE.
EOF

REFLECT_PROMPT=$(mktemp)
cat > "$REFLECT_PROMPT" <<EOF
You are yoyo-invest. Today is $DATE $SESSION_TIME.

$YOYO_CONTEXT

Use the investment-loop skill.

Your job:
1. Write a reflection to $REFLECTION_FILE.
2. Append a short dated entry to $JOURNAL_FILE.

Inputs:
- Market assessment:
$( [ -f "$ASSESSMENT_FILE" ] && cat "$ASSESSMENT_FILE" )
- Daily plan:
$( [ -f "$PLAN_FILE" ] && cat "$PLAN_FILE" )
- Daily report:
$( [ -f "$REPORT_FILE" ] && cat "$REPORT_FILE" )
- Stable rules:
$RULES
- Error patterns:
$ERRORS

Reflection requirements:
- Record where confidence is weakest.
- State what evidence is still missing.
- Name 1-3 likely failure modes for today's recommendations.
- Suggest concrete priority shifts for the next cycle.
- Do not update rules unless a repeated pattern is already evident.
EOF

export SNAPSHOT_FILE

run_prompt "$ASSESS_PROMPT" "$(mktemp)"
run_prompt "$PLAN_PROMPT" "$(mktemp)"
run_prompt "$REPORT_PROMPT" "$(mktemp)"
run_prompt "$REFLECT_PROMPT" "$(mktemp)"

rm -f "$ASSESS_PROMPT" "$PLAN_PROMPT" "$REPORT_PROMPT" "$REFLECT_PROMPT"

echo "=== Investment loop complete ==="
echo "Assessment: $ASSESSMENT_FILE"
echo "Plan:       $PLAN_FILE"
echo "Report:     $REPORT_FILE"
echo "Reflection: $REFLECTION_FILE"
