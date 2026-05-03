# 2026-01-20 投资复盘反思（historical）

## 结论摘要

今天的回放输入显示市场表层为 `risk_on`：股票平均 1 日涨幅约 1.606%，ETF 平均 1 日涨幅约 1.7%，领涨集中在 `3690.HK`、`9988.HK`、`0388.HK`。但这不是可直接升级的交易环境，因为两个硬约束同时存在：

1. `actionable_candidates=[]`，没有任何候选进入行动列表。
2. `as_of_date=2026-01-20`，但快照内 quote 日期为 2026-04-29，存在明显非日期对齐问题。

因此今天所有高分动态候选都只能作为诊断队列和观察清单，不能升级为 `buy_candidate`、`hold` 或 `accumulate`。核心建议状态应为 `watch_only` / audit。

## 今日动态选择与推荐状态

动态排名前三为：

- `0857.HK`：score=84.42，`energy` 主题第一，趋势与量能均较强，但被 `symbol_risk_veto` 阻断；历史 33 次评估 pass_rate=0.091，avg_return=-1.658%，且包含 adverse breach 与 `symbol_selection_error`。
- `0941.HK`：score=81.98，`telecom-dividend` 主题第一，量能扩张，但被 `symbol_risk_veto` 阻断；30 次评估 pass_rate=0.000，avg_return=-0.510%。
- `0002.HK`：score=76.08，`utilities-defensive` 主题第一，但同样被 `symbol_risk_veto` 阻断；样本较少但 pass_rate=0.000。

推荐状态：上述三者均为 `watch_only`，不是行动建议。今天的有效工作不是寻找替代下单标的，而是做 veto audit 与 peer-relative review。

## 信心最弱的位置

信心最弱的是“高趋势分数是否能转化为可交易优势”。原因：

- `0857.HK`、`0941.HK`、`0002.HK` 的技术分数高，但均被 `symbol_risk_veto` 拦截。
- `risk_on` 不能覆盖 `actionable_candidates=[]`、非日期对齐报价、低 pass_rate、以及历史 selected-vs-best 问题。
- 后验评估总体较弱：688 次评估中 pass 仅 57 次，fail 211 次，说明当前选择与时点系统仍需保守。
- 参数优化没有升级 active strategy；样本、改善、胜率、样本质量等 promotion gate 未通过。

## 仍然缺失的证据

下一步若要从 `watch_only` 升级，需要补足：

1. 日期对齐证据：必须有 `2026-01-20` 对应的价格、成交量、MA20/MA60、区间位置，而不是 2026-04-29 报价。
2. 行动列表确认：至少有候选进入 `actionable_candidates`，且 `qualified_for_action=true`。
3. 风险 veto 解除或替代标的独立通过：若 leader 被 `symbol_risk_veto`，替代 peer 不能只因为 `symbol_risk_veto=false` 就升级，必须独立进入 action list。
4. peer-relative 证据：若替代同主题 peer，需要证明相对 veto leader 和近期 best peer 的新强度，而不是只看当前分数。
5. ETF/广谱确认：特别是互联网、科技、宽基类标的，需要 broad-market 与 ETF 的量价、均线、广度共同确认。
6. 成本/边际证据：预期 swing edge 必须同时超过 35bps round-trip cost 与 100bps minimum_edge_bps。

## 可能失败模式

1. **risk-control error**：把 `risk_on` 市况和高 score 当作足够证据，忽略 `actionable_candidates=[]`、`symbol_risk_veto` 与非日期对齐报价。
2. **symbol-selection error**：在 `0857.HK`、`0941.HK`、`0002.HK` 被 veto 后，从同主题低排名 peer 中机械寻找替代，而没有证明其相对 veto leader 与近期 best peer 的改善。
3. **timing error**：在反弹日追入高位趋势股，尤其 `range_pos_60` 已接近或超过高位的标的，后续 T+3/T+5 可能回吐。

## 动态选择错误分类

今天的推荐来自 dynamic symbol selection。若未来出错，优先分类如下：

- `0857.HK`：主要风险为 `risk-control error` 与 `symbol-selection error`。分数强但历史 veto 强，若强行升级属于风险闸门失效。
- `0941.HK`：主要风险为 `risk-control error`。趋势、量能与高股息防御叙事可能诱发过度信任，但 pass_rate=0.000 是硬约束。
- `0002.HK`：主要风险为 `timing error` 与 `risk-control error`。样本少、pass_rate=0.000，且防御股在 risk-on 日可能不是最佳表达。
- 互联网主题：近期 `0700.HK`、`9988.HK` 多次错过 same-theme best peer，若再升级而不比较 `9618.HK`、`3690.HK`、`1024.HK` 的相对强弱，应归为 `symbol-selection error`。

## 下一周期优先级调整

1. 第一优先级：修复/验证日期对齐，所有 replay 排名必须标注报价日期差异；未对齐时只允许 audit。
2. 第二优先级：把 `actionable_candidates=[]` 作为硬停机信号，禁止从 diagnostic list 挖替代交易。
3. 第三优先级：对被 veto 的主题 leader 做 peer-relative 审核，但只记录观察条件，不升级。
4. 第四优先级：互联网主题必须增加 selected-vs-best 检查；若近期 best peer 不是当前 leader，必须说明为何相对强度已经改善。
5. 第五优先级：保留 `l5_mvp_conservative_v1`，不因单日 risk_on 或高分候选调整策略参数。

## 今日可执行研究清单

- `0857.HK`、`0941.HK`、`0002.HK`：维持 `watch_only`，观察是否能在日期对齐数据中继续保持趋势、量能和相对强度，并等待 veto 风险改善。
- `0386.HK`、`3690.HK`、`2331.HK` 等 `symbol_risk_veto=false` 的低排名 peer：仅作 audit，不是替代行动标的；需先进入 `actionable_candidates` 并证明相对 leader / best peer 改善。
- `2800.HK`、`3033.HK`、`3067.HK`：因历史低 pass_rate 与近期 misfire，只能观察 ETF 确认是否恢复，不能作为单日风险偏好升级依据。
