# 2025-12-30 投资复盘反思（historical）

时间：2025-12-30 10:04  
模式：historical replay  
策略：`l5_mvp_conservative_v1`  
结论：今天没有可执行升级；全部维持 `watch_only` / 诊断观察。

## 1. 今天我看到的事实

- 市场快照给出的整体状态是 `risk_on`：股票平均 1 日涨幅约 1.298%，ETF 平均 1 日涨幅约 1.237%。
- 领涨来自 `9992.HK`、`3690.HK`、`0386.HK`，但这些并不是系统排名最高的可执行候选。
- 排名系统没有给出 `actionable_candidates`，这是最重要的硬约束。
- 最高的三个 `diagnostic_candidates` 是：
  - `0857.HK`：score 61.85，趋势强，但有 `symbol_risk_veto`，且成交量比率仅 0.116。
  - `0941.HK`：score 59.66，趋势强，但有 `symbol_risk_veto`，且成交量比率仅 0.1343。
  - `0002.HK`：score 57.15，没有 `symbol_risk_veto`，但低于 action score，成交量比率仅 0.2451。
- 所有靠前候选都被低成交量拦住；多个高分候选还被历史风险记录拦住。
- 回放日期是 `2025-12-30`，但行情字段里的 `quote_trade_date` 是 `2026-04-29`。这使今天的排名更像诊断样本，而不是日期对齐的交易证据。

## 2. 今天的建议状态

### 总体建议：`watch_only`

今天不应把任何标的升级为 `buy_candidate`、`accumulate` 或 `hold`。原因不是市场完全没有强度，而是三个关键门槛同时缺失：

1. `actionable_candidates` 为空；
2. 日期不对齐，不能把 2026-04-29 的报价当成 2025-12-30 的实时确认；
3. 最高排名候选要么有 `symbol_risk_veto`，要么成交量确认不足。

### 诊断观察队列

- `0002.HK`：相对最干净的观察对象。它没有 `symbol_risk_veto`，价格在 MA20 和 MA60 上方，MA20 也在 MA60 上方。但 score 仍低于 action threshold，且 volume_ratio_20 只有 0.2451，所以只能观察。触发条件应是放量改善、继续站稳均线、并维持 utilities-defensive 主题内领先。
- `0883.HK`：如果能源主题继续强于市场，它比被 veto 的 `0857.HK` 更值得做同主题替代审查；但它不是 theme score leader，且成交量也弱，不能直接替代升级。
- `0005.HK`：金融银行主题分数稳定但成交量弱，适合作为防守/价值方向的确认样本，而不是行动标的。

## 3. 信心最弱的地方

今天信心最弱的是“行情证据的时间一致性”。`as_of_date` 是 2025-12-30，但所有 quote 字段来自 2026-04-29。这个冲突会污染几乎所有短线判断：

- 1 日涨跌幅可能不是 2025-12-30 的真实市场行为；
- 均线与区间位置虽然来自 completed daily history，但仍需要确认是否与回放日期严格对齐；
- 主题轮动判断可能是后验行情，而不是当日可交易信息。

第二个弱点是成交量。今天很多高分候选的趋势结构不错，但 `volume_ratio_20` 普遍低于 0.6。低成交量下的突破、站稳均线、主题领先，都不能直接转化为 swing edge。

第三个弱点是历史选择质量。后验摘要里 `symbol_selection_error` 有 133 次，是最大重复错误来源。`0857.HK`、`0941.HK`、`0700.HK`、`9988.HK`、`2800.HK` 等都有低 pass rate 或近期 selected-vs-best 问题，所以今天不能因为模型排名靠前就恢复信心。

## 4. 仍然缺失的证据

下一轮需要补齐这些证据后，才允许考虑升级：

1. 日期对齐证据：必须有真正对应 `2025-12-30` 的价格、成交量、MA20、MA60、ETF 表现和主题表现。
2. 成交量确认：候选至少需要摆脱低成交量状态，尤其是 `volume_ratio_20` 不能继续低于 0.6。
3. ETF / broad confirmation：如果要升级单一股票，必须看到对应主题 ETF 或 broad market 同步确认。
4. 同主题 peer-relative confirmation：若 leader 被 `symbol_risk_veto`，替代标的不只要“更干净”，还要在新证据里明显强于被 veto 的 leader。
5. 成本与 edge 证据：round-trip 约 35 bps、minimum edge 100 bps；当前没有足够证据说明任何候选有超过成本门槛的 swing edge。

## 5. 今日推荐最可能的失败模式

1. **timing error**：市场是 `risk_on`，如果短线继续普涨，`watch_only` 会显得过于保守，尤其是 `9992.HK`、`3690.HK` 这类当日强势股可能继续反弹。
2. **symbol-selection error**：如果能源或电讯主题继续走强，系统首选 `0857.HK` / `0941.HK` 可能仍不是最佳表达；更好的 peer 可能是 `0883.HK`、`0386.HK` 或其他未覆盖标的。
3. **risk-control error**：日期不一致时仍试图从排名里提取可交易信号，容易把后验行情误当成当日确认；今天必须用 `watch_only` 把这个风险锁住。

## 6. 动态选择错误分类

今天的候选来自动态 universe ranking，因此必须按错误类型预先分类：

- `0857.HK`：主要风险是 **symbol-selection error** 和 **risk-control error**。它是能源 theme leader，但历史通过率低、平均回报差，并且被 `symbol_risk_veto` 拦截。
- `0941.HK`：主要风险是 **symbol-selection error**。它趋势分高，但 pass_rate 极低，且同主题 `0728.HK` 是否更稳没有足够新证据。
- `0002.HK`：主要风险是 **timing error**。它相对干净，但已经接近 60 日区间高位，成交量不足，短线追入容易被均值回归打脸。
- `9992.HK` / `3690.HK` / `0386.HK`：这些是当日涨幅 leader，但排名不支持行动；若后续它们继续领涨，今天的保守结论会被归类为 **theme error** 或 **timing error**，不是单纯方向错误。

## 7. 下一周期的优先级调整

1. **先修正数据对齐，再讨论交易**：下一轮第一步不是选股，而是确认 `as_of_date`、quote date、MA source 是否严格一致。
2. **把 `actionable_candidates` 为空视为硬刹车**：诊断分数只能生成观察条件，不能生成买入建议。
3. **优先审查主题内替代，而不是直接放弃主题**：能源、电讯和公用事业都有结构强项，但 veto leader 之后，替代 peer 必须独立通过成交、趋势和相对强度检查。
4. **降低对低成交量趋势分的权重**：今天趋势分最高的候选大多成交量不足；下一轮应优先寻找“趋势 + 放量 + peer 相对强”的组合。
5. **继续把低 pass rate 标的放在惩罚区**：`0857.HK`、`0941.HK`、`2800.HK`、`3033.HK`、`3067.HK`、`0700.HK` 等不能因为单日风险偏好改善就恢复可行动状态。

## 8. 记忆更新判断

后验摘要继续显示 `symbol_selection_error` 是最大重复问题，且近期 selection errors 仍集中在互联网平台同主题选择上。不过现有长期记忆已经覆盖今天暴露的问题：

- 日期不一致时降级；
- `actionable_candidates` 为空时不升级；
- `symbol_risk_veto` 只拦截单一标的，不自动否定主题；
- 替代 peer 必须证明 fresh peer-relative strength；
- 重复 selected-vs-best underperformance 后不能只凭当前分数升级。

所以今天不新增规则，避免重复写入同一条约束。今天的长期动作是把这次样本记录进 journal，作为这些规则继续有效的证据。小章鱼今天不抢跑。先把触手收回来，等证据对齐。