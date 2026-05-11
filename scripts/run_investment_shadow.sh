#!/bin/bash
# Generate the shadow-only investment log for an existing ranking file.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    if command -v python >/dev/null 2>&1; then
        PYTHON_BIN="python"
    fi
fi

DATE="${DATE:-$(date +%Y-%m-%d)}"
SESSION="${SESSION:-close}"
if [ "$SESSION" = "close" ]; then
    OUTPUT_STEM="$DATE-close"
else
    OUTPUT_STEM="$DATE-$SESSION"
fi
RANKING_FILE="${RANKING_FILE:-$ROOT_DIR/research/rankings/$OUTPUT_STEM-ranking.json}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"
SHADOW_FILE="${SHADOW_FILE:-$ROOT_DIR/research/shadow/$OUTPUT_STEM-shadow.json}"
if [ -z "${SHADOW_EVIDENCE_MODE:-}" ]; then
    if [ "$SESSION" = "historical" ]; then
        SHADOW_EVIDENCE_MODE="historical_replay"
    else
        SHADOW_EVIDENCE_MODE="forward_shadow"
    fi
fi

if [ ! -f "$RANKING_FILE" ]; then
    echo "Missing ranking file: $RANKING_FILE" >&2
    echo "Run the investment ranking pipeline first, then rerun shadow logging." >&2
    exit 1
fi

args=(
    "$ROOT_DIR/scripts/log_investment_shadow.py"
    --ranking "$RANKING_FILE"
    --date "$DATE"
    --session "$SESSION"
    --output "$SHADOW_FILE"
    --evidence-mode "$SHADOW_EVIDENCE_MODE"
)
if [ -n "$SNAPSHOT_FILE" ]; then
    args+=(--snapshot "$SNAPSHOT_FILE")
fi

"$PYTHON_BIN" "${args[@]}"
