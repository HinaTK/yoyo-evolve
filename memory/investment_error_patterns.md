# Investment Error Patterns

## Patterns To Track
- Treating a selective `risk_on` day as enough to override `actionable_candidates=[]`, non-date-aligned quotes, or `symbol_risk_veto`.
- Upgrading `diagnostic_candidates` despite `diagnostic_only=true` or `qualified_for_action=false`.
- Treating `qualified_for_watch=true` as an actionable signal while `diagnostic_only=true` or `qualified_for_action=false`.
- Selecting the model's theme leader without checking whether it has recently underperformed same-theme alternatives.
- Re-selecting a theme score leader after repeated selected-vs-best misses without proving fresh peer-relative improvement.
- Treating a clean-looking same-theme peer as actionable merely because the ranked leader was blocked by `symbol_risk_veto`.
- Mining lower-ranked peers for substitutes when `actionable_candidates=[]` instead of treating the cycle as audit-only.
- Reframing repeated selected-vs-best misses as only a theme problem instead of requiring proof versus the actual recent best peer.
- Promoting or changing strategy parameters when challenger evidence fails samples, improvement, win_rate, or sample_quality gates.
- 在个股或主题 leader 被 veto 后，把 `2800.HK` 当作低风险默认 fallback，而未检查其近期 T+3/T+5 失效记录。
- 仅因 trend_score 强就重新启用被 veto 的高分主题 leader，而未检查 low pass_rate、负平均回报、adverse breach 与近期 actual best peer。

- 把非日期对齐 dynamic ranking 中的 theme leader、trend_score 或 volume-expansion 误当作当日入场触发，而不是 audit priority。
- 把四大行业动态焦点池误当作硬性买入名单，或在焦点池外推荐失败后没有归因 `focus_priority_ignored`。
- 把行业优先级错误和同主题个股选择错误混为一谈，导致自迭代无法调整行业评分权重。

## Updating This File
- Add errors that recur at least twice.
- Rewrite patterns as prevention rules when they become clear.
