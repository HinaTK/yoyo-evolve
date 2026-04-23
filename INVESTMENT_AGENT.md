# Investment Agent

This repository now includes an investment research loop that can run alongside the original coding-agent evolution workflow without modifying the protected core pipeline.

## What It Does

- Tracks a configured Hong Kong stock and ETF watchlist
- Fetches a daily market snapshot from Tencent's public Hong Kong market endpoints
- Runs a four-step autonomous loop:
  - market assessment
  - daily plan
  - recommendation report
  - reflection
- Stores structured call records for each cycle under `research/calls/`
- Runs posterior evaluation across historical calls and later snapshots under `research/evaluations/`
- Feeds evaluation learnings back into investment memory files
- Writes outputs under `research/daily/`
- Uses stable memory files under `memory/` to reduce drift

## Files

- `config/investment_profile.toml`
- `config/watchlist.toml`
- `config/portfolio.toml`
- `scripts/fetch_investment_data.py`
- `scripts/backfill_investment_snapshots.py`
- `scripts/evaluate_investment_calls.py`
- `scripts/bootstrap_investment_iterations.sh`
- `scripts/evolve_investment.sh`
- `skills/investment-loop/SKILL.md`
- `memory/investment_rules.md`
- `memory/investment_error_patterns.md`

## Run It

Build `yoyo` first, then run:

```bash
cargo build
bash scripts/evolve_investment.sh
```

To bootstrap the system with roughly one month of prior market days and let it replay 30 autonomous iterations:

```bash
cargo build
bash scripts/bootstrap_investment_iterations.sh
```

If you already have a snapshot file, the loop reuses it. Otherwise it fetches one for the current date.
Before each new cycle, it evaluates prior structured calls against later snapshots and injects the summary into the next prompt.

## Research Artifacts

- Tracked and committed by workflow:
  - `research/daily/`
  - `research/calls/`
  - `research/evaluations/`
  - `journals/investment_journal.md`
  - investment memory files under `memory/`
- Ignored as runtime cache:
  - `data/snapshots/`

## Guardrails

- The investment loop uses a fixed analysis order: market, theme, ETF, symbol, risk, action.
- Recommendations must carry evidence, risks, invalidation, horizon, and confidence.
- When evidence is weak, the expected fallback is `watch_only`.
- The loop persists machine-readable calls, posterior evaluations, memory, and journal artifacts instead of modifying the protected self-evolution pipeline.
