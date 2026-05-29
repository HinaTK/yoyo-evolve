# Investment Rules

## Stable Rules
- When evidence is thin or conflicting, downgrade to `watch_only`.
- Every actionable recommendation must include a clear invalidation condition.
- Prefer theme confirmation through ETFs before upgrading a single-stock thesis.
- Do not treat posterior evaluation as current-session confirmation.
- `risk_on` regime cannot override `actionable_candidates=[]`, non-date-aligned quotes, or `symbol_risk_veto`; these conditions cap recommendations at `watch_only` / audit.
- Treat `qualified_for_watch=true` as radar-only; do not upgrade unless `qualified_for_action=true` or the symbol appears in `actionable_candidates`.
- If `actionable_candidates` is empty and top diagnostic candidates are vetoed, treat the cycle as veto audit plus peer-relative review; do not mine lower-ranked peers for action substitutes.
- A same-theme substitute for a vetoed leader is not actionable unless it independently clears the action list and shows fresh peer-relative strength versus both the vetoed leader and the recent best peer.
- When a symbol has repeated selected-vs-best misses, future same-theme upgrades must name the recent best peer and show fresh relative-strength improvement versus that peer, not only versus the vetoed or current leader.
- Historical replay rankings generated from non-date-aligned quotes are conditional audit items, not direct upgrades.
- Do not promote parameter challengers unless samples, improvement, win_rate, adverse-risk, and sample_quality gates all pass.
- Broad-market ETF 只能作为 confirmation，不是默认防守替代；若其近期 T+3/T+5 多次失效，必须重新通过 date-aligned edge gate 后才能升级。
- 被 veto 的高分主题 leader 必须维持 audit-only，直到日期对齐重跑后同时通过 `actionable_candidates`、risk gates，并证明相对近期 actual best peer 的 peer-relative strength。

- Dynamic ranking from non-date-aligned quotes may identify audit priorities only; it cannot supply triggers, ETF confirmation, or peer-relative strength for same-day action.
- `focus_industries.toml` expresses stable user preference; `research/focus/*-focus.json` only changes daily attention and must not delete or auto-add durable trade-universe symbols without explicit confirmation.
- Track four-industry mistakes separately: industry priority errors are not the same as same-theme symbol-selection errors.
- Proxy-only nontechnical evidence is watch/audit-only; action requires point-in-time manual/formal evidence with real sources, known event risk, and still must pass cost and risk gates.

## Updating This File
- Only add a rule after repeated evidence across multiple review windows.
- Keep rules short, testable, and operational.
