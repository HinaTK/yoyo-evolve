# HK + A-Share Investment Research System

This repository is based on yoyo-evolve, but the current local working system has been extended into a Hong Kong and mainland A-share stock/ETF research loop.

The investment system is not an auto-trading bot. It produces recommendation research, structured calls, posterior evaluation, and iterative rule updates. The user makes all final trading decisions.

## Current Purpose

Use yoyo as a local HK and A-share investment assistant that can:

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

- `config/market_radar.toml` — broad HK and mainland A-share radar used to detect sector/theme strength.
- `config/trade_universe.toml` — HK and mainland A-share symbols the system is allowed to dynamically rank and recommend.
- `config/watchlist.toml` — smaller user-focus list; no longer the only source of recommendations.
- `config/focus_industries.toml` — stable user preference layer for the four priority industries: technology, new energy, brokerage, and healthcare.
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
6. Generate the dynamic four-industry focus pool with `scripts/generate_investment_focus_pool.py`.
7. Run posterior evaluation with `scripts/evaluate_investment_calls.py`.
8. Ask yoyo-invest to write market assessment markdown.
9. Ask yoyo-invest to write a focused daily plan.
10. Ask yoyo-invest to write the recommendation report in Chinese.
11. Ask yoyo-invest to convert the report into structured calls JSON.
12. Ask yoyo-invest to write a reflection; only close/historical sessions may update long-term memory.

## Outputs

- `research/daily/YYYY-MM-DD-SESSION-market-assessment.md`
- `research/daily/YYYY-MM-DD-SESSION-plan.md`
- `research/daily/YYYY-MM-DD-SESSION-report.md`
- `research/daily/YYYY-MM-DD-SESSION-reflection.md`
- `research/calls/YYYY-MM-DD-SESSION-calls.json`
- `research/rankings/YYYY-MM-DD-SESSION-ranking.json`
- `research/focus/YYYY-MM-DD-SESSION-focus.json`
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

Level 5 MVP adds a research-only parameter optimization loop:

- `config/active_strategy.toml` stores the active research ranking weights and safety invariants.
- `config/optimization.toml` defines the whitelisted parameter grid, backtest gates, promotion sessions, layered candidate counts, and no-auto-trading invariants.
- `scripts/build_snapshot_registry.py` builds `data/snapshots/registry.json` for reproducible historical inputs.
- `scripts/backtest_investment_strategy.py` recomputes historical ranking candidates and evaluates cost-adjusted forward performance.
- `scripts/optimize_investment_params.py` compares champion/challenger parameter sets and can automatically promote a research strategy only when configured gates pass.

The Level 5 loop is still research-only: it must not enable automatic trading, reduce cost/edge gates, mutate historical snapshots, or use future snapshots beyond the current as-of date.

Level 6 MVP adds an automatic research-code improvement loop while staying research-only:

- `scripts/plan_investment_system_improvements.py` reads the latest posterior evaluation, backtest, optimization result, and investment error patterns, then writes up to three evidence-based `session_plan/investment_task_*.md` tasks.
- `scripts/evolve_investment_system.sh` builds the snapshot registry, evaluates calls, runs backtest/optimization, generates the improvement plan, and writes `research/experiments/system_changes/latest_system_evolution.*`.
- By default, Level 6 only plans and reports. Set `INVESTMENT_SYSTEM_AUTO_IMPLEMENT=true` to let yoyo attempt each generated task with prompts constrained to research system code, tests, docs, and safety-preserving changes.
- `scripts/evaluate_investment_system_change.py` is the fail-closed evaluator for code changes. It rejects automatic-trading enablement, research-only mode disablement, risk gate reductions, historical snapshot edits, future/as-of leakage-guard removals, evaluation logic removals, and execution-related vocabulary.
- After optional implementation, the loop runs the safety evaluator and Python Level 5/6 unittest coverage; if the evaluator fails, the script fails and does not automatically revert.

Level 6 stabilization adds conservative guardrails before this loop can promote an active research strategy:

- Backtests support `candidate_policy = "relaxed"`, which falls back to each snapshot's top candidates only when strict `min_watch_score` samples are thin; fallback records are marked `below_watch_score` and summaries expose `strict_sample_count`, `relaxed_sample_count`, and `sample_quality`.
- Optimizer promotion remains fail-closed: `relaxed_fallback` runs can generate reports and improvement tasks but cannot update `config/active_strategy.toml`.
- Adverse-move reporting now includes average max adverse return and adverse breach rate, with promotion gated by `max_adverse_breach_rate` as well as the single worst adverse limit.
- The planner now distinguishes relaxed fallback sample-quality issues from generic low sample counts and can generate adverse breach-rate protection tasks.
- Historical expansion should be staged. Use `scripts/plan_investment_backtest_batches.py` to divide the latest 90 available close snapshots into 9 batches, then run exactly one confirmed batch with `scripts/run_investment_backtest_batch.sh` before reviewing the updated records, symbol risk memory, backtest, and optimization outputs.
- `evaluate_investment_calls.py` now writes complete per-call evaluation records to `research/evaluations/latest_records.json`; symbol risk memory should prefer those records when available and mark summary-only risk memory as `as_of_limited=true`.

Level 6 second-round stabilization tightens candidate quality and selection evidence:

- Ranking output now marks each item with `qualification_flags`, `disqualifiers`, `qualified_for_watch`, and `diagnostic_only` so weak liquidity, downtrend, low-range, and below-moving-average setups cannot be mistaken for promotable candidates.
- Backtests evaluate qualified watch candidates first; strict mode excludes disqualified rows, while relaxed diagnostics separately report `qualified_sample_count` and `diagnostic_sample_count`.
- Posterior evaluation records same-theme peer opportunity cost through selected-vs-best and selected-vs-median bps, and treats missed same-theme leaders as clearer `symbol_selection_error` evidence.
- The Level 6 planner can now propose targeted tasks when same-theme best peers are repeatedly missed or diagnostic fallback samples remain too prominent.

Level 6 third-round stabilization separates action eligibility from diagnostics and adds symbol-level risk memory:

- Ranking now emits `actionable_candidates` and `diagnostic_candidates`. Only `actionable_candidates` can be considered for upgrades; diagnostic rows are for observation, watch-only context, and explanation.
- `top_candidates` remains for compatibility, but it is composed from actionable rows plus diagnostic fill, with diagnostic rows marked through `diagnostic_only` and qualification flags.
- `qualified_for_action` requires `qualified_for_watch`, `score >= min_action_score`, theme leadership, and no symbol risk veto.
- `scripts/build_symbol_risk_memory.py` creates `research/experiments/symbol_risk_memory.json` from latest evaluation summaries. If only aggregate summary fields are available, metadata marks `as_of_limited=true` instead of claiming full as-of training.
- Backtests and optimization distinguish `actionable_top_n` from `diagnostic_top_n`; promotion uses the conservative actionable sample layer and the higher `min_samples` gate.

Level 6 kernel hardening adds traceable run lineage and deterministic draft calls:

- Ranking rows now include per-candidate `expected_edge_bps`, `net_expected_edge_bps`, `cost_gate_passed`, `edge_method`, and `evidence_window`. Action qualification requires the edge/cost gate to pass; validator rejects actionable final calls without those fields.
- Nontechnical evidence can be loaded from manual/formal point-in-time files configured under `config/nontechnical_evidence.toml` `[curated_sources]`; proxy-only evidence remains watch/audit-only and cannot override cost, market-risk, or symbol-risk gates.
- `scripts/generate_investment_draft_calls.py` creates deterministic draft policy JSON from ranking layers. LLM report/calls stages may explain or downgrade these drafts, but should not upgrade beyond the deterministic draft state.
- `scripts/create_investment_run_manifest.py` writes `research/runs/<date>-<session>/manifest.json` with as-of metadata, model/provider, and sha256/size/existence metadata for key inputs and outputs. The investment loop writes the manifest before LLM stages and refreshes it after final outputs exist.

Level 6 risk review hardening adds a second deterministic policy layer between draft calls and final LLM calls:

- `scripts/generate_investment_risk_review.py` reads deterministic draft calls, ranking rows, `config/investment_profile.toml`, and optional symbol risk memory, then writes `research/risk/<date>-<session>-risk-review.json`.
- Each verdict records `risk_decision`, `final_state_cap`, `max_position_pct`, `risk_tags`, `reasons`, and `required_confirmations` for a symbol.
- Symbol risk memory vetoes and deterministic `avoid` drafts force `avoid`; `watch_only` drafts remain capped at `watch_only`.
- Draft `buy_candidate` rows can pass only when action qualification, cost gate, volume confirmation, and trend checks all pass; otherwise the review downgrades to `watch_only` or vetoes severe disqualifiers.
- `scripts/validate_investment_calls.py` accepts `--risk-review` and rejects any non-diagnostic final call without a matching risk verdict or above that verdict's `final_state_cap`.
- `scripts/evolve_investment.sh` generates the risk review after the draft policy, records it in the run manifest, includes it in the calls prompt, and passes it to final validation.

Level 6 readiness gates define what the current research metrics are allowed to support:

- `scripts/check_investment_readiness.py` reads the latest backtest, optimization result, and `config/investment_profile.toml`, then writes `research/readiness/latest_readiness.json` and `.md`.
- `shadow_logging` is the minimum observation stage: at least 60 production samples, positive average net return, sufficient sample quality, and zero adverse-breach rate.
- `paper_trading` is stricter: at least 70 production samples, win rate at least 0.50, average net return at least 0.15%, median return non-negative, average alpha at least 0.50%, max adverse no worse than -6%, zero adverse-breach rate, and no severe mature-month imbalance.
- `small_live_observation` is not automatic execution. It requires at least 100 samples, win rate at least 0.56, average net return at least 0.30%, median return at least 0.10%, max adverse no worse than -4%, and at least 20 forward paper-trading days before any tiny, manually confirmed, recommendation-only real-money observation is considered.

Layer 3/4 hardening attributes posterior outcomes back to the deterministic and LLM layers, then feeds repeated causes into bounded improvement planning:

- `scripts/attribute_investment_outcomes.py` joins `research/evaluations/latest_records.json` with final calls, draft policy calls, risk reviews, and ranking rows when those artifacts exist.
- Attribution records tag evidence-supported causes such as `ranking_selection_error`, `same_theme_best_missed`, `cost_gate_too_loose`, `cost_gate_too_strict`, `risk_veto_missed`, `risk_veto_saved_loss`, `risk_veto_too_strict`, `symbol_risk_memory_too_harsh`, `focus_industry_error`, `focus_priority_ignored`, and `llm_final_deviation`.
- The attribution layer is fail-soft: missing historical draft, risk, or ranking artifacts do not block attribution from posterior records.
- `scripts/evolve_investment_system.sh` runs attribution after posterior evaluation and before planning, writing `research/evaluations/latest_attribution.json` and `research/evaluations/latest_attribution.md`.
- `scripts/plan_investment_system_improvements.py` reads latest attribution by default and can generate focused tasks when the same attribution tag repeats, with validation commands that stay research-only.

## Current Limitations

- It is research assistance, not financial advice or automated execution.
- It depends on the configured Tencent quote endpoints and local model service.
- The trade universe is broad but still manually configured; it is not full-market discovery.
- Ranking is deterministic but simple: trend, momentum, range position, volume confirmation, and risk penalties.
- Transaction costs are approximated through configurable gates, not broker-specific execution simulation.

## Important Orientation For New AI Sessions

If asked what this repository is for, answer that the upstream project is a self-evolving coding agent CLI, while the current local working system extends it into an HK and mainland A-share stock/ETF investment research and posterior-optimization loop. For investment tasks, prefer this document and the investment scripts/configs over the original upstream project description.
