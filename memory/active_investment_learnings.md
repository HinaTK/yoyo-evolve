# Active Investment Learnings

This file stores the currently active investment learnings that should influence the next research cycle.

## Current Focus
- 在 historical replay 中，若 `as_of_date` 与 quote 日期不一致，即使市场为 `risk_on` 也只能做 `watch_only` / audit。
- `actionable_candidates=[]` 是硬停机信号：不得从 `diagnostic_candidates` 或低排名 peer 中挖替代行动标的。
- 当 top diagnostic candidates 全部被 `symbol_risk_veto` 阻断时，下一周期优先做 veto audit 与 peer-relative review，而不是升级同主题替代品。
- 同主题替代品只有在独立进入 `actionable_candidates`、通过 cost/edge/risk gates，并相对 veto leader 与近期 best peer 显示 fresh relative strength 后，才可考虑升级。
- 对互联网平台主题，任何升级前必须检查近期 selected-vs-best 记录；若 `0700.HK` 或 `9988.HK` 持续落后 `9618.HK`、`3690.HK`、`1024.HK` 等 best peer，默认 `watch_only`。
- 参数优化未通过 samples、improvement、win_rate、sample_quality 等 gate 时，不因单日高分或 `risk_on` 调整 active strategy。
- `2800.HK` 近期多次 T+3 / T+5 失效；不得把 broad-market ETF 当作 veto 后的安全 fallback，升级前必须有日期对齐的 ETF confirmation 与正向 edge。

- 高分主题 leader 若被 `symbol_risk_veto` 阻断，不得因分数或单日 risk-on 重启；下一次升级必须同时证明相对近期 actual best peer 的 fresh relative strength。

- 历史回放中的 dynamic ranking 若使用非日期对齐 quote，只能用来发现审计对象；不得把其 theme leader、trend_score 或 volume signal 当作当日触发条件。

## How To Update
- Prefer concise, operational learnings.
- Promote a learning here only after posterior evaluation suggests it matters.
