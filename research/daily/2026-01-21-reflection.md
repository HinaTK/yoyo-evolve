# 2026-01-21 投资复盘反思（historical）

## 结论摘要

本轮 historical replay 的核心结论是：尽管快照中的 `market_summary.risk_state` 为 `risk_on`，平均股票与 ETF 单日涨幅均为正，且能源、电信分红、公用事业、防御金融等主题在排名上靠前，但今天不应产生行动型推荐。原因有三点：

1. `actionable_candidates=[]`，这是硬停机信号。
2. 排名前三的 `0857.HK`、`0941.HK`、`0002.HK` 都是 `diagnostic_only=true` 且 `qualified_for_action=false`，并被 `symbol_risk_veto` 阻断。
3. 本次 snapshot 的 `as_of_date=2026-01-21`，但行情字段显示 quote 日期为 `2026-04-29`，属于非日期对齐输入，只能作为条件审计材料，不能当作当日交易确认。

因此，今天的建议状态应保持为 `watch_only` / audit，而不是 `buy_candidate`、`accumulate` 或任何行动升级。

## 事实与解释分离

### 事实

- 市场层面：`risk_on`，股票平均 1 日涨幅约 1.606%，ETF 平均 1 日涨幅约 1.7%。
- 领涨个股包括 `3690.HK`、`9988.HK`、`0388.HK`；但这些并不自动进入行动名单。
- 主题排名靠前：`utilities-defensive`、`telecom-dividend`、`financials-bank`、`energy`。
- 模型 top candidates：`0857.HK` 分数 84.42，`0941.HK` 分数 81.98，`0002.HK` 分数 76.08。
- 三个 top candidates 均满足 watch 层面的技术条件，但均被 `symbol_risk_veto` 阻断，且 `qualified_for_action=false`。
- 参数优化未更新 active strategy：samples、improvement、win_rate、sample_quality 等 gate 未通过。

### 解释

今天是一个“表层风险偏好改善、但系统级行动门槛未打开”的周期。最容易犯错的地方是把 `risk_on` 和高排名误读为买入许可。实际上，排名结果更适合用来做 veto audit：检查为什么高分标的长期后验表现差、为什么同主题 leader 被反复 veto、以及是否存在需要重新定义 peer-relative selection 的证据。

## 置信度最弱的地方

置信度最弱的是对 2026-01-21 当日真实市场状态的判断。输入中的 `as_of_date` 与 quote 日期不一致，导致技术指标、成交量确认和短期动量只能作为后验审计线索，不能确认 2026-01-21 当天的可执行状态。其次，`0002.HK` 的样本数只有 3，`9618.HK`、`0728.HK`、`1299.HK` 等部分标的样本也偏少；这些 veto 或 pass_rate 信息有方向价值，但不足以单独形成稳定的交易结论。

## 仍缺失的证据

- 与 `as_of_date=2026-01-21` 完全日期对齐的收盘价、成交量、MA20、MA60、range position。
- 同主题内的当日相对强弱矩阵，尤其是能源、电信、公用事业、互联网平台内 leader 与 best peer 的 T+3 / T+5 表现对比。
- ETF 层面的主题确认：例如 `2800.HK`、`3033.HK`、`3067.HK` 是否在同一日期给出一致确认，而不是后验 quote 混入。
- 被 `symbol_risk_veto` 标的的失败拆解：到底是方向错误、选股错误、时点错误，还是风险门槛过松。
- 参数 challenger 的高质量样本；当前 `relaxed_fallback` 且 avg_net_return_pct 为负，不能支持策略切换。

## 今日建议及失效条件

- 总体状态：`watch_only` / audit。
- 观察对象：`0857.HK`、`0941.HK`、`0002.HK` 仅用于 veto audit；`9618.HK`、`3690.HK`、`9988.HK`、`0700.HK` 仅用于互联网平台 peer-relative review；`2800.HK` 仅用于大盘 ETF confirmation audit。
- 不升级条件：只要 `actionable_candidates=[]`、`qualified_for_action=false`、`diagnostic_only=true`、`symbol_risk_veto` 或非日期对齐 quote 任一条件存在，就不得升级。
- 若未来要升级，必须看到日期对齐数据、进入 `actionable_candidates`、通过 cost/edge/risk gates，并给出相对近期 best peer 的 fresh relative strength。

## 可能失败模式

1. **风险控制错误**：把 `risk_on`、高分数、`qualified_for_watch=true` 当成行动信号，忽视 `actionable_candidates=[]` 与 `symbol_risk_veto`。
2. **选股错误**：在 `0857.HK`、`0941.HK`、`0002.HK` 被 veto 后，从同主题较低排名标的中挖替代品，而没有证明其相对 veto leader 与近期 best peer 的 fresh relative strength。
3. **时点错误**：使用非日期对齐 quote 解释历史当天走势，导致把后验动量误认为当时可见信号。

## 动态选股的未来错误分类

本轮使用了动态 symbol selection，但没有形成行动推荐。若未来错误发生，最可能分类为：

- `symbol-selection error`：尤其是互联网平台主题中，历史上 `0700.HK`、`9988.HK` 多次落后 `9618.HK`、`3690.HK`、`1024.HK` 等 best peer。
- `timing error`：若仅因当日反弹或量能扩张追入，而 T+3 / T+5 无法延续。
- `risk-control error`：若在 `symbol_risk_veto` 或 `actionable_candidates=[]` 下仍升级。

## 下一周期优先级调整

1. 第一优先级：修复日期对齐问题。所有 historical replay 的 ranking 与 snapshot 必须使用同一 `as_of_date` 的行情数据，否则只做 audit。
2. 第二优先级：建立 veto leader 与 recent best peer 对照表，尤其针对互联网平台、能源、电信、公用事业四个主题。
3. 第三优先级：对 `2800.HK` 做单独审计。近期 `hold` / `buy_candidate` 多次在 T+3 / T+5 失败，不能把大盘 ETF 当作低风险默认 fallback。
4. 第四优先级：参数优化继续保持 inactive；除非 samples、improvement、win_rate、sample_quality 同时改善，否则不切换 active strategy。
