# 2025-12-15 投资复盘反思（historical）

本次是 historical bootstrap replay，名义 `as_of_date` 是 `2025-12-15`，但输入中的 `quote_trade_date` / `quote_trade_time` 指向 `2026-04-28`。所以我不能把价格字段当成真实 2025-12-15 当日确认，只能把它作为回放系统生成的结构化信号来使用。今天最重要的动作不是扩大进攻，而是在 `risk_off` 背景下把“看起来强”的标的拆成：可行动、仅诊断、观察、回避。

## 今日结论回看

市场总状态是 `risk_off`：股票平均 1 日跌幅约 -0.946%，ETF 平均 1 日跌幅约 -1.847%，`2800.HK`、`3033.HK`、`3067.HK` 都处于 `downtrend`，且主要科技/互联网权重仍缺少 ETF 层面的确认。这种环境下，任何单一强势股都需要更高的证据门槛。

唯一进入 `actionable_candidates` 的是 `0006.HK`。它的优点清楚：

- `score=75.51`，超过 action threshold；
- 价格在 MA20 和 MA60 之上，且 MA20 > MA60；
- `volume_ratio_20=1.0304`，没有成交萎缩问题；
- 属于 `utilities-defensive`，主题在 `risk_off` 环境中相对合拍；
- 没有 `symbol_risk_veto`。

但我仍然应该把它写成低 beta 防守型 `buy_candidate`，而不是高置信追涨。原因是 `range_pos_60=1.0092`，已经接近或略高于 60 日区间上沿，短线风险不是趋势破坏，而是“防守拥挤后的回撤”。它的无效条件应保持具体：跌回 MA20（63.41）且成交不能维持，或防守主题相对强度消失，就降回 `watch_only`。

`0941.HK` 和 `0857.HK` 都是今天最容易犯错的地方。它们分数高、趋势形态好，但都被 `symbol_risk_veto` 拦住：`0941.HK` 的 pass_rate 为 0/3，`0857.HK` 的 pass_rate 为 0/4 且平均回报明显为负，还包含 repeated `symbol_selection_error`。这说明动态排名分数和历史后验风险发生冲突时，不能用当日强势覆盖后验纪律。今天把它们放在 `diagnostic_candidates`，不升级为行动，是正确的风险控制。

`0883.HK` 是能源主题里的替代观察对象。它没有 `symbol_risk_veto`，趋势也不错，但它不是主题分数 leader，且 `volume_ratio_20=0.8064` 不算强确认。因此它只能是 `watch_only` / peer-relative diagnostic，不能因为 `0857.HK` 被 veto 就自动替换成买入对象。

`9618.HK` 是互联网平台里少数仍保持 `uptrend` 的单名，但主题平均分只有 16.4，ETF 和核心互联网权重 `0700.HK`、`9988.HK`、`1024.HK` 都弱。这里最重要的纪律是：单名强不能代替主题确认，尤其在此前互联网平台已经多次出现 `symbol_selection_error` 和低 pass-rate 的背景下。

## 信心最弱的地方

1. **时间一致性最弱。** `as_of_date=2025-12-15`，但行情字段来自 `2026-04-28`，所以所有结论必须被视为回放结构判断，而不是当日真实市场判断。
2. **`0006.HK` 的入场时点最弱。** 它是唯一可行动标的，但 `range_pos_60` 已在高位，可能正确方向是防守优先，错误点却是追在短线拥挤位置。
3. **能源主题替代选择最弱。** `0857.HK` 被 veto 后，`0883.HK` 看起来更干净，但还没有足够成交、leader 地位或独立风险证据来支持升级。
4. **互联网平台单名强度最弱。** `9618.HK` 的个股形态较好，但主题和 ETF 背景太弱，容易再次发生“选中看起来最强的单名，却输给主题或 ETF 方向”的错误。

## 仍然缺失的证据

- 真实 2025-12-15 的成交、价格与均线快照，而不是 replay 中带有未来 quote timestamp 的字段。
- `0006.HK` 是否在随后 3-5 个交易日继续保持相对强度，尤其是否守住 MA20 且成交不缩。
- 防守主题是否有广泛确认：`0006.HK` 与 `0002.HK` 是否同步强，还是只有一个高位防守拥挤标的。
- 能源主题中 `0883.HK` 相对 `0857.HK` 的持续超额表现证据，而不是单日替代想象。
- 科技 ETF `3033.HK` / `3067.HK` 和 broad ETF `2800.HK` 的 breadth、volume、MA60 修复证据。

## 可能的失败模式

1. **timing error：** `0006.HK` 趋势仍好，但短期因为已接近 60 日高位而回撤，导致 `buy_candidate` 的 T+3/T+5 体验不佳。
2. **risk-control error：** 如果我忽视 `risk_off` 和 ETF 下行，把 `0006.HK` 以外的高分标的也升级，就会把诊断候选误当成行动候选。
3. **symbol-selection error：** 能源和互联网平台都存在动态选择陷阱：`0857.HK` 是模型 leader 但被 veto；`9618.HK` 是弱主题里的相对强单名。未来错误很可能不是“主题完全错”，而是“在主题内部选错或过早升级”。

## 动态选择错误分类

- `0006.HK`：动态筛选出的唯一 actionable symbol。主要未来风险是 **timing error**，其次是防守拥挤导致的 **risk-control error**。
- `0857.HK`：动态主题 leader，但被 `symbol_risk_veto` 拦截。若未来仍升级，错误类型应归为 **symbol-selection error** 与 **risk-control error**。
- `0941.HK`：动态高分候选但被低 pass-rate veto。若未来无新增确认就升级，错误类型偏 **risk-control error**。
- `0883.HK`：可能被当作 `0857.HK` 的替代。若仅因 leader 被 veto 就买入，错误类型是 **symbol-selection error**。
- `9618.HK`：弱主题中的相对强单名。若无 ETF/主题确认就升级，错误类型是 **theme error** + **symbol-selection error**。

## 下一周期优先级

1. **先验证 `0006.HK`，不要扩大战线。** 下一轮先看它是否守住 MA20、成交是否维持、是否继续强于 `0002.HK` 和 broad market。
2. **把 `0941.HK` 留在观察池，等待 veto 修复证据。** 它的形态好，但 pass-rate 证据不足以支持行动。
3. **能源主题先做 peer-relative 检查。** 比较 `0857.HK`、`0883.HK`、`0386.HK` 的相对强度和成交确认；只有 `0883.HK` 独立通过趋势、成交、相对强度和风险门槛，才考虑升级。
4. **科技/互联网继续 ETF-first。** `9618.HK` 不应在 `3033.HK`、`3067.HK`、`2800.HK` 仍弱时升级。
5. **继续让 `symbol_risk_veto` 真正生效。** 高分但低 pass-rate 的标的只能做诊断，不能因为形态漂亮而绕过后验风险。

## 记忆更新判断

本次 posterior evidence 继续显示重复模式：`symbol_selection_error=88`，并且近期仍有互联网平台 selected-vs-best underperformance；`0857.HK`、`0941.HK` 的高分但 veto 也再次提醒我，动态 leader 和可行动标的不是同一件事。不过这些模式已经被当前 memory 中的 peer-relative confirmation、`symbol_risk_veto` 和 ETF-first 规则覆盖。今天不新增长期规则，只在 journal 记录本次 baseline：在 `risk_off` 中，只允许 `0006.HK` 作为低 beta 条件候选，其余高分标的保持诊断或观察。
