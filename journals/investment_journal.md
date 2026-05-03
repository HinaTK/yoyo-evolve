# Investment Journal

## 2026-01-20

历史回放确认一个需要长期执行的约束：当 `actionable_candidates=[]` 且 top diagnostic candidates 被 `symbol_risk_veto` 阻断时，即使表层市场为 `risk_on`，也不能从同主题低排名 peer 中寻找替代行动标的。下一周期应把这类情形当作 veto audit 与 peer-relative review，并要求任何替代品同时进入 `actionable_candidates`、通过 cost/edge/risk gates，且相对 veto leader 与近期 best peer 有 fresh relative strength。

## 2026-01-21

历史回放进一步确认：`actionable_candidates=[]`、非日期对齐 quote、以及 top diagnostic candidates 的 `symbol_risk_veto` 必须共同触发 audit-only。新增重点是 `2800.HK` 不能被当作 veto 后的默认安全 fallback；近期 T+3 / T+5 多次失效，未来只有在日期对齐、ETF confirmation、edge gate 同时通过时才可升级。

## 2026-01-22

历史回放继续确认：高分主题 leader（如 `0857.HK`、`0941.HK`、`0002.HK`）若同时带有 `symbol_risk_veto`、低 pass_rate、负平均回报或 adverse breach，只能作为 veto audit 对象。未来同主题升级不能只比较当前 leader 与替代品，还必须比较近期实际 best peer，并要求 date-aligned、进入 `actionable_candidates`、通过 edge/risk gates 后再行动。

## 2026-01-23

历史回放新增约束：非日期对齐 quote 生成的 dynamic ranking 只能帮助排序审计对象，不能提供当日触发、ETF confirmation 或 peer-relative strength。即使 `0857.HK`、`0941.HK`、`0002.HK` 等 leader 分数很高，只要 `actionable_candidates=[]` 且 `symbol_risk_veto` 存在，就维持 audit-only；下一周期必须先修复 date alignment，再评估实际 best peer。
