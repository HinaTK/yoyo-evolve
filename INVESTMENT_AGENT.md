# Investment Agent

This repository now includes an investment research loop that can run alongside the original coding-agent evolution workflow without modifying the protected core pipeline.

## What It Does

- Tracks a configured Hong Kong stock and ETF watchlist
- Fetches a daily market snapshot from Yahoo Finance
- Runs a four-step autonomous loop:
  - market assessment
  - daily plan
  - recommendation report
  - reflection
- Writes outputs under `research/daily/`
- Uses stable memory files under `memory/` to reduce drift

## Files

- `config/investment_profile.toml`
- `config/watchlist.toml`
- `config/portfolio.toml`
- `scripts/fetch_investment_data.py`
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

If you already have a snapshot file, the loop reuses it. Otherwise it fetches one for the current date.

## Guardrails

- The investment loop uses a fixed analysis order: market, theme, ETF, symbol, risk, action.
- Recommendations must carry evidence, risks, invalidation, horizon, and confidence.
- When evidence is weak, the expected fallback is `watch_only`.
- The loop writes memory and journal artifacts instead of modifying the protected self-evolution pipeline.
