# HK Investment Research System

This repository is based on yoyo-evolve, but the current local working system has been extended into a Hong Kong stock and ETF research loop.

The investment system is not an auto-trading bot. It produces recommendation research, structured calls, posterior evaluation, and iterative rule updates. The user makes all final trading decisions.

## Current Purpose

Use yoyo as a local HK investment assistant that can:

- scan a broad market radar for sector and theme strength,
- rank a larger trade universe with deterministic technical scores,
- produce Chinese morning, midday, and close-session research reports,
- emit machine-readable recommendation JSON,
- evaluate previous calls against later snapshots,
- learn from repeated errors through memory and rule updates.

## Daily Scripts

Run from PowerShell via Git Bash:

```powershell
& "C:\Program Files\Git\bin\bash.exe" -lc 'cd /d/Code/yoyo && bash scripts/investment_morning.sh'
& "C:\Program Files\Git\bin\bash.exe" -lc 'cd /d/Code/yoyo && bash scripts/investment_midday.sh'
& "C:\Program Files\Git\bin\bash.exe" -lc 'cd /d/Code/yoyo && bash scripts/investment_close.sh'
```

Session behavior:

- `morning`: pre-market or early-session planning; no long-term memory or journal updates.
- `midday`: intraday confirmation check; no long-term memory or journal updates.
- `close`: official daily review; may update investment memory and journal.
- `historical`: bootstrap replay mode used by `scripts/bootstrap_investment_iterations.sh`.

Local model configuration lives in `.env` and is intentionally ignored by git. Use `.env.example` as the template.

## Inputs

- `config/market_radar.toml` — broad radar used to detect sector/theme strength.
- `config/trade_universe.toml` — symbols the system is allowed to dynamically rank and recommend.
- `config/watchlist.toml` — smaller user-focus list; no longer the only source of recommendations.
- `config/investment_profile.toml` — risk, cost, selection, and ranking thresholds.
- `config/portfolio.toml` — currently recommendation-only mode; no real holdings are assumed.
- `memory/active_investment_learnings.md` — active investment lessons.
- `memory/investment_rules.md` — stable investment rules.
- `memory/investment_error_patterns.md` — repeated error patterns.

## Runtime Pipeline

One investment session performs this pipeline:

1. Load `.env` defaults without overriding explicitly supplied environment variables.
2. Determine `SESSION` and output stem.
3. Fetch the trade universe snapshot into `data/snapshots/`.
4. Fetch the market radar snapshot into `data/snapshots/`.
5. Rank the trade universe with `scripts/rank_investment_universe.py`.
6. Run posterior evaluation with `scripts/evaluate_investment_calls.py`.
7. Ask yoyo-invest to write market assessment markdown.
8. Ask yoyo-invest to write a focused daily plan.
9. Ask yoyo-invest to write the recommendation report in Chinese.
10. Ask yoyo-invest to convert the report into structured calls JSON.
11. Ask yoyo-invest to write a reflection; only close/historical sessions may update long-term memory.

## Outputs

- `research/daily/YYYY-MM-DD-SESSION-market-assessment.md`
- `research/daily/YYYY-MM-DD-SESSION-plan.md`
- `research/daily/YYYY-MM-DD-SESSION-report.md`
- `research/daily/YYYY-MM-DD-SESSION-reflection.md`
- `research/calls/YYYY-MM-DD-SESSION-calls.json`
- `research/rankings/YYYY-MM-DD-SESSION-ranking.json`
- `research/evaluations/latest.md`
- `research/evaluations/latest.json`

Historical bootstrap outputs may omit the session suffix for compatibility with the original 30-day replay baseline.

## Iterative Optimization

The current optimization loop is implemented at the rule and evaluation level:

- `evaluate_investment_calls.py` compares prior calls to later snapshots.
- It separates sessions (`morning`, `midday`, `close`, `historical`).
- It classifies repeated problems such as `theme_error`, `symbol_selection_error`, `timing_unclear`, `overconfidence`, `bullish_misread`, and `defensive_misread`.
- Calls include `selection_source_theme` and `selection_reason` so the system can distinguish theme errors from same-theme symbol-selection errors.
- Close and historical reflections may update investment memory and rules.

The system does not yet fully auto-tune ranking weights. Ranking parameters live in `config/investment_profile.toml` and are currently deterministic defaults.

## Current Limitations

- It is research assistance, not financial advice or automated execution.
- It depends on the configured Tencent quote endpoints and local model service.
- The trade universe is broad but still manually configured; it is not full-market discovery.
- Ranking is deterministic but simple: trend, momentum, range position, volume confirmation, and risk penalties.
- Transaction costs are approximated through configurable gates, not broker-specific execution simulation.

## Important Orientation For New AI Sessions

If asked what this repository is for, answer that the upstream project is a self-evolving coding agent CLI, while the current local working system extends it into an HK stock/ETF investment research and posterior-optimization loop. For investment tasks, prefer this document and the investment scripts/configs over the original upstream project description.
