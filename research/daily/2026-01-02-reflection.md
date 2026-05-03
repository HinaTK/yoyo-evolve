# 2026-01-02 投资复盘反思

> 会话：`historical`  
> 模式：`recommendation_only`  
> 写入时间：2026-01-02 13:09  
> 关键限制：`as_of_date=2026-01-02`，但行情字段来自 `quote_trade_date=2026-04-29`。因此今天的所有结论只能作为历史回放诊断和下一轮观察清单，不能当作日期对齐的实时交易确认。

## 1. 今天我实际应该相信什么

表面上，市场状态是 `risk_on`：股票平均 1 日涨幅约 `+1.271%`，ETF 平均约 `+1.07%`；`3690.HK`、`9992.HK`、`9988.HK` 等高 beta/消费互联网个股领涨。但这个 risk-on 不够干净：

- broad ETF `2800.HK` 仍在 MA60 下方附近，`volume_ratio_20=0.5493`，未达到成交确认门槛；
- tech ETF `3033.HK`、`3067.HK` 都只刚站上 MA20，仍低于 MA60；
- 很多单名虽然反弹，但成交不足，且后验低通过率或 `symbol_risk_veto` 仍然存在；
- 排名输出中 `actionable_candidates=[]`，这是今天最硬的约束。

所以今天最稳健的结论不是“risk-on 可以买”，而是：**市场有反弹迹象，但证据只能支持 `watch_only`，不能支持 `buy_candidate` / `accumulate` / `hold`。**

## 2. 信心最弱的地方

我今天信心最弱的地方有四个：

1. **日期错位**：`as_of_date` 与 `quote_trade_date` 不一致，这是最大不确定性。任何基于 2026-04-29 行情字段对 2026-01-02 做出的解释，都可能只是回放系统的诊断投影，而不是当日可执行证据。
2. **risk-on 的质量**：平均涨幅为正，但 ETF 成交和 MA60 确认不足。这个 risk-on 可能是选择性反弹，而不是可持续的趋势修复。
3. **动态选股的可执行性**：`0728.HK` 是唯一 `qualified_for_watch=true` 且无 disqualifier 的前排标的，但它仍是 `diagnostic_only=true`、`below_action_score`，不能被误读为行动信号。
4. **leader 与 peer 的切换**：`0857.HK`、`0941.HK`、`0006.HK` 等传统 leader 被 `symbol_risk_veto` 或低成交拦住，转向 `0883.HK`、`0728.HK`、`0002.HK` 这类 peer 时，最容易把“更干净”误读成“足够买”。

## 3. 仍然缺失的证据

下一轮要把这些缺口补齐，否则继续维持 `watch_only`：

- **日期对齐证据**：需要与 `2026-01-02` 对齐的 OHLCV、MA20/MA60、成交比和主题排名，而不是 2026-04-29 的报价字段。
- **ETF 确认**：`2800.HK` 需要明确重回并站稳 MA60；`3033.HK` / `3067.HK` 需要 MA60 reclaim，而不是只站上 MA20。
- **成交确认**：多数候选的 `volume_ratio_20` 仍低于 `0.6`。即使 `0883.HK`、`0857.HK`、`0941.HK` 接近门槛，也还没有足够确认。
- **peer-relative confirmation**：若避开 veto leader 选择同主题 peer，需要证明 peer 相对 leader 的近期强度改善，而不是只因为 leader 被否决。
- **成本/edge 证据**：35 bps 往返成本与 100 bps 最低 edge 门槛仍未被明确覆盖。

## 4. 今日建议的可能失败模式

1. **timing error**：risk-on 反弹可能在 T+3/T+5 内回落，尤其是 ETF 未站稳 MA60、成交不足时。即使中期方向修复，短线追高也容易错。
2. **symbol-selection error**：动态排名可能把主题 leader 或 cleaner peer 选错。`0857.HK`、`0941.HK` 有历史风险，`0883.HK`、`0728.HK` 虽更干净，但如果没有证明相对 leader 的新强度，替代选择仍可能落后。
3. **risk-control error**：把 `qualified_for_watch=true` 或高 `trend_score` 误读成行动信号，会绕过 `actionable_candidates=[]`、成交门槛、`symbol_risk_veto` 和成本门槛。

## 5. 动态选股错误分类

今天的候选明显来自动态 symbol selection，因此要预先标记可能错误类型：

- `0728.HK`：主要风险是 **timing error** 与 **risk-control error**。它是 `telecom-dividend` 的当前排名 leader，`qualified_for_watch=true`，但仍低于 action score；若被升级，就是把观察资格误当成行动资格。
- `0857.HK`：主要风险是 **symbol-selection error** 与 **risk-control error**。它趋势强、主题 leader，但 `symbol_risk_veto=true` 且 `volume_ratio_20=0.5414`，历史平均回报差，不能因为强趋势而升级。
- `0941.HK`：主要风险是 **symbol-selection error**。它不是当前主题 score leader，且有低 pass_rate、负 avg_return、历史 selection error；继续选它需要新的相对强度证据。
- `0883.HK`、`0005.HK`、`0002.HK`、`9618.HK`：主要风险是 **risk-control error**。它们可能看起来比 veto leader 干净，但成交、行动分数或 peer-relative 证据不足，仍只能观察。

## 6. 下一周期优先级调整

1. **先修日期对齐，再谈动作**：下一轮优先使用 `as_of_date` 对齐的快照字段验证，而不是让 `quote_trade_date` 的数据驱动结论。
2. **把 `0728.HK` 放在观察首位，而不是买入首位**：它是今天少数满足 watch 条件的标的，但下一步必须看是否突破 action score、保持成交确认，并继续领先 `0941.HK`。
3. **能源只做 peer audit**：`0857.HK` 仍是趋势 leader 但被 veto；`0883.HK` 需要证明相对 `0857.HK` 的持续强度且成交过门槛，才可能从观察升级。
4. **tech/internet 继续 ETF-first**：`3033.HK`、`3067.HK` 未收复 MA60 前，不升级 `9618.HK`、`9988.HK`、`3690.HK` 等单名反弹。
5. **把“观察资格”和“行动资格”分开写**：`qualified_for_watch=true` 只能进入雷达；只有 `qualified_for_action=true` 或 `actionable_candidates` 非空，才允许讨论行动。

## 7. 今天的最终自我评分

纪律：合格。没有因为 `risk_on` 和若干高分趋势股而升级。  
证据质量：偏弱。日期错位让所有信号都只能诊断使用。  
下一步：不要寻找“能买的名字”，先寻找“缺失证据是否补齐”。今天最好的交易，是不把观察清单伪装成交易清单。
