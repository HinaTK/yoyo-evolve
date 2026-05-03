# Historical Replay Handoff

Purpose: this file is a resume note for a fresh agent session. It is not executable code and does not change the investment system behavior. Use it to continue the historical replay without loading the full prior chat context.

## Current Status

- Historical replay plan: `research/experiments/historical_batches/plan.json`
- Completed batches: 1, 2, 3
- Next batch to run: 4
- Batch 4 date range: `2026-01-26` to `2026-02-06`
- Do not start batch 5 unless explicitly confirmed by the user.

## Completed Batch Ranges

- Batch 1: `2025-12-10` to `2025-12-23`
- Batch 2: `2025-12-24` to `2026-01-09`
- Batch 3: `2026-01-12` to `2026-01-23`

Each completed replay date should have matching files under:

- `research/daily/`
- `research/calls/`
- `research/rankings/`

Batch-level outputs have been refreshed after each completed batch:

- `research/evaluations/latest.md`
- `research/evaluations/latest.json`
- `research/evaluations/latest_records.json`
- `research/experiments/symbol_risk_memory.json`
- `research/experiments/latest_backtest.json`
- `research/experiments/latest_optimization.json`

## Resume Command

From PowerShell:

```powershell
$env:BATCH_INDEX="4"
$env:PROMPT_PAUSE_SECONDS="300"
$env:PROMPT_PROVIDER_RETRIES="2"
$env:PROVIDER_RETRY_SECONDS="600"
$env:SKIP_EXISTING_OUTPUTS="true"
$env:INVESTMENT_LIGHT_CONTEXT="true"
& "C:\Program Files\Git\bin\bash.exe" "scripts/run_investment_backtest_batch.sh"
```

## Retry / Rate Limit Notes

- The local custom model endpoint is configured through `.env`; do not print or commit secrets.
- If `/chat/completions` returns `429 Too Many Requests`, pause and resume later.
- If the batch stops mid-date, rerun the same batch command. Existing `calls` files are skipped automatically.
- For partial dates, `scripts/evolve_investment.sh` can skip existing assessment/plan/report files when `SKIP_EXISTING_OUTPUTS=true`.
- `INVESTMENT_LIGHT_CONTEXT=true` reduces prompt size during historical replay.

## Important Guardrails

- This is research/recommendation-only work, not trading automation.
- Do not weaken risk gates, cost assumptions, symbol vetoes, or promotion gates just to improve backtest results.
- Keep `actionable_candidates`, `diagnostic_candidates`, `qualified_for_watch`, `qualified_for_action`, `diagnostic_only`, `theme_rank`, and `is_theme_leader` semantics intact.
- Treat non-date-aligned historical replay quotes as audit signals, not direct live-action triggers.
- Continue one batch at a time and report before starting the next batch.

## Latest Known Metrics After Batch 3

- Evaluation total: 754
- Verdicts: pass 57, fail 236, mixed 146, informational 315
- Main learning tags: `symbol_selection_error` 160, `theme_error` 98, `timing_unclear` 138
- Backtest as of: `2026-01-23`
- Backtest sample count: 67
- Average net return: -0.262%
- Win rate: 17.9%
- Average alpha: 0.088%
- Adverse breach rate: 0.0%
- Active strategy was not updated because promotion gates did not pass.
