# 2026-01-26 港股市场评估（historical replay）

> 生成时间参考：2026-01-26 09:45  
> 模式：historical / recommendation_only  
> 适用周期：14-90 天 swing 观察  
> 重要限制：本次输入的 `as_of_date` 为 `2026-01-26`，但行情字段 `quote_trade_date` 为 `2026-04-30`，属于非日期对齐快照。依据稳定规则，本报告只能用于条件审计、主题相对强弱复盘与研究问题生成，不能作为同日交易升级依据。

## 1. 市场雷达事实

### 1.1 市场状态

**事实：**

- `market_summary.risk_state` = `neutral`。
- 雷达内平均个股单日变动 `avg_stock_move_1d` = -0.308%。
- 雷达内 ETF 平均单日变动 `avg_etf_move_1d` = -0.553%。
- 领先个股：`1299.HK` +2.41%、`0883.HK` +1.29%、`0388.HK` +1.10%。
- 落后个股：`9988.HK` -1.99%、`1024.HK` -1.79%、`3690.HK` -1.32%。
- `actionable_candidates` 为空。
- 排名前三的 `diagnostic_candidates` 分别为 `0883.HK`、`0857.HK`、`0941.HK`，但均为 `diagnostic_only=true` 且 `qualified_for_action=false`。

**解读：**

- 市场不是全面风险偏好扩张，而是中性环境下的防御、能源、部分金融相对占优。
- ETF 层面的广泛确认不足，尤其科技 ETF 偏弱，不能支持对互联网平台或恒生科技方向做主动升级。
- 因 `actionable_candidates=[]`，本轮没有确定性层面可升级的交易候选；所有候选最多只能列为 `watch_only` / 审计观察。

## 2. 主题强弱：先看雷达，再映射到交易宇宙

### 2.1 雷达主题强弱排序（事实）

按确定性排名的 `theme_summary`：

| 排名 | 主题 | 平均分 | 主题领先标的 | 领先分数 | 是否合格 |
|---:|---|---:|---|---:|---|
| 1 | `utilities-defensive` | 54.38 | `0002.HK` | 54.49 | false |
| 2 | `financials-exchange` | 52.49 | `0388.HK` | 52.49 | false |
| 3 | `financials-bank` | 51.02 | `0005.HK` | 51.02 | false |
| 4 | `telecom-dividend` | 46.26 | `0941.HK` | 55.11 | false |
| 5 | `energy` | 44.40 | `0883.HK` | 56.90 | false |
| 6 | `financials-insurance` | 43.78 | `1299.HK` | 43.78 | false |
| 7 | `hong-kong-broad-market` | 31.25 | `2800.HK` | 31.25 | false |
| 8 | `internet-platform` | 14.91 | `9618.HK` | 50.86 | false |
| 9 | `consumer-discretionary` | 14.65 | `2020.HK` | 46.78 | false |
| 10 | `hang-seng-tech` | 9.82 | `3033.HK` | 19.65 | false |
| 11 | `consumer-tech` | 0.00 | `1810.HK` | 0.00 | false |
| 12 | `healthcare-biotech` | 0.00 | `2269.HK` | 0.00 | false |
| 13 | `healthcare-pharma` | 0.00 | `1177.HK` | 0.00 | false |

**解读：**

- 强势集中在公用事业、防御收益、金融交易所/银行、电讯股息、能源。
- 弱势集中在恒生科技、互联网平台、消费科技和医疗医药。
- 虽然多个防御和资源类标的技术趋势良好，但全部主题的 `leader_qualified=false`，说明强弱只能作为观察线索，不能直接变成交易建议。

## 3. 交易宇宙内的主题可行动性

### 3.1 `utilities-defensive`：雷达最强，但不可升级

**事实：**

- 交易宇宙有 `0002.HK` 与 `0006.HK`。
- `0002.HK`：score 54.49，`regime_flags=["uptrend"]`，价格 75.8，高于 ma20 74.73 与 ma60 74.0388，`range_pos_60` 0.9284。
- `0006.HK`：score 54.26，`regime_flags=["uptrend"]`，价格 64.9，高于 ma20 63.8175 与 ma60 62.5067，`range_pos_60` 0.9271。
- 两者共同缺陷：`low_volume_ratio_20_below_0_6`，且均有 `symbol_risk_veto`。
- `0002.HK` 是主题分数领先者。

**解读：**

- 该主题是当前雷达最强的防御表达，最佳当前表达为 `0002.HK`，但只适合作为审计观察。
- 因 `symbol_risk_veto` 与低量能，不能用防御主题强度替代行动门槛。
- 状态：`watch_only`。

### 3.2 `financials-exchange`：`0388.HK` 强势但仍被风险门槛限制

**事实：**

- 交易宇宙有 `0388.HK`。
- `0388.HK`：score 52.49，单日 +1.10%，价格 424.4，高于 ma20 407.59 与 ma60 406.6493，`range_pos_60` 0.7598，`regime_flags=["uptrend"]`。
- 主要限制：`low_volume_ratio_20_below_0_6`、`symbol_risk_veto`，`qualified_for_action=false`。

**解读：**

- `0388.HK` 是金融交易所主题的唯一且最佳表达，趋势结构优于大盘 ETF 与科技 ETF。
- 但风险层未放行，不能升级为 `buy_candidate`。
- 状态：`watch_only`。

### 3.3 `financials-bank`：`0005.HK` 趋势延续，但不是行动候选

**事实：**

- 交易宇宙有 `0005.HK`。
- `0005.HK`：score 51.02，价格 140.2，高于 ma20 138.235 与 ma60 133.3526，`range_pos_60` 0.8486，`regime_flags=["uptrend"]`。
- 限制：`low_volume_ratio_20_below_0_6`、`symbol_risk_veto`，`qualified_for_action=false`。

**解读：**

- `0005.HK` 是银行主题的最佳表达，但缺少可交易放量与历史风险放行。
- 状态：`watch_only`。

### 3.4 `telecom-dividend`：`0941.HK` 相对最强，但风险否决明确

**事实：**

- 交易宇宙有 `0941.HK`、`0728.HK`。
- `0941.HK`：score 55.11，主题排名第 1，价格 85.2，高于 ma20 81.92 与 ma60 79.9358，`range_pos_60` 0.9686，`regime_flags=["uptrend"]`。
- `0728.HK`：score 37.41，低于 watch 门槛，且不是主题领先者。
- `0941.HK` 的 `symbol_risk` 显示 `action_veto=true`，原因包括 pass_rate=0.000 over 30 evaluated calls、平均回报略负、存在 adverse breach 与 symbol_selection_error。

**解读：**

- 若只看技术趋势，`0941.HK` 是电讯股息主题最强表达。
- 但后验风险否决非常清楚；不能因为高 trend_score 或防御属性而升级。
- 状态：`watch_only` / veto audit。

### 3.5 `energy`：雷达领先但被 veto 与量能共同限制

**事实：**

- 交易宇宙有 `0883.HK`、`0857.HK`、`0386.HK`。
- `0883.HK`：score 56.90，全市场排名第 1，单日 +1.29%，价格 29.76，高于 ma20 27.274 与 ma60 26.7913，`range_pos_60` 0.8984，`regime_flags=["uptrend"]`。
- `0857.HK`：score 55.82，趋势分 99.70，但不是主题领先者，`range_pos_60` 0.9901。
- `0386.HK`：score 20.48，低于 watch 门槛，且不是主题领先者。
- `0883.HK` 与 `0857.HK` 均被 `symbol_risk_veto`，且均有 `low_volume_ratio_20_below_0_6`。

**解读：**

- 能源是最值得审计的强主题之一；最佳当前表达是 `0883.HK`，次优观察是 `0857.HK`。
- 但排名前两名都被后验风险否决，不能向下挖掘 `0386.HK` 作为替代交易，因为规则要求：当 `actionable_candidates=[]` 且 leader 被 veto 时，不得挖掘低排名同主题替代品。
- 状态：`watch_only` / peer-relative review。

### 3.6 `financials-insurance`：`1299.HK` 单日最强，但分数未达 watch

**事实：**

- 交易宇宙有 `1299.HK`。
- `1299.HK`：单日 +2.41%，是雷达单日最大涨幅；score 43.78，低于 `min_watch_score` 45。
- 价格 87.0，高于 ma20 84.8925 与 ma60 85.1267，`range_pos_60` 0.6595，`regime_flags=["range"]`。
- 限制：`below_watch_score`、`low_volume_ratio_20_below_0_6`、`symbol_risk_veto`。

**解读：**

- `1299.HK` 的日内/单日弹性突出，但确定性排名未确认足够质量。
- 只能观察是否从区间转为稳定上行，不能因单日领涨升级。
- 状态：`watch_only`。

### 3.7 `hong-kong-broad-market`：`2800.HK` 未提供广泛确认

**事实：**

- 交易宇宙有 `2800.HK`。
- `2800.HK`：score 31.25，低于 watch 门槛；单日 -0.46%；价格 26.12，略高于 ma20 25.9058，接近 ma60 26.1361 下方；`regime_flags=["range"]`。
- `symbol_risk` 显示 pass_rate=0.065 over 107 evaluated calls，并有近期 misfire。

**解读：**

- 大盘 ETF 没有给出强确认，无法支持全面风险偏好升级。
- 它也不能作为被 veto 主题的 fallback。
- 状态：`watch_only`。

### 3.8 `internet-platform`：主题弱，最佳表达不是传统关注股

**事实：**

- 交易宇宙有 `0700.HK`、`9988.HK`、`3690.HK`、`1024.HK`、`9618.HK`。
- 主题平均分 14.91，整体偏弱。
- `9618.HK` 是主题内分数领先者：score 50.86，价格 117.5，高于 ma20 115.8882 与 ma60 108.0392，`regime_flags=["uptrend"]`。
- `0700.HK`：score 0，`downtrend`，价格低于 ma20 与 ma60，`range_pos_60` -0.0013。
- `9988.HK`：score 12.64，单日 -1.99%，为落后股之一；虽略高于 ma20，但低于 ma60。
- `3690.HK`：score 11.04，价格低于 ma20 与 ma60。
- `1024.HK`：score 0，`downtrend`。
- `9618.HK` 也有 `symbol_risk_veto` 与 `low_volume_ratio_20_below_0_6`。

**解读：**

- 若必须表达互联网平台主题，当前最佳相对表达是 `9618.HK`，不是 `0700.HK` 或 `9988.HK`。
- 但该主题整体弱，且后验记录显示互联网平台存在重复 selected-vs-best 错误；不能把 `9618.HK` 的相对领先直接升级为交易。
- `0700.HK`、`9988.HK` 只能作为相对强弱追踪对象，尤其要验证是否重新跑赢 `9618.HK`、`3690.HK`、`1024.HK` 等近期 best peer。
- 状态：`watch_only`。

### 3.9 `consumer-discretionary`：`2020.HK` 是最佳表达，但主题确认不足

**事实：**

- 交易宇宙有 `2020.HK`、`2331.HK`、`9992.HK`、`6862.HK`。
- `2020.HK`：score 46.78，是主题领先者，价格 82.9，高于 ma20 82.4725 与 ma60 81.03，`regime_flags=["uptrend"]`。
- `2331.HK`：score 11.81，价格低于 ma20 与 ma60。
- `9992.HK`：score 0，虽高于 ma20，但低于 ma60 且 `range_pos_60` 0.107。
- `6862.HK`：score 0，`downtrend`。
- `2020.HK` 有 `symbol_risk_veto` 与低量能限制。

**解读：**

- `2020.HK` 是可选消费主题内的最佳当前表达，但主题平均分仅 14.65。
- 由于主题本身弱、leader 被 veto，不能行动化。
- 状态：`watch_only`。

### 3.10 `hang-seng-tech` 与 `consumer-tech`：ETF 与核心科技均未确认

**事实：**

- `3033.HK`：score 19.65，单日 -0.62%，价格 4.78 基本贴近 ma20 4.7782，但低于 ma60 4.9698，`regime_flags=["range"]`。
- `3067.HK`：score 0，`downtrend`，价格低于 ma20 与 ma60。
- `1810.HK`：score 0，`downtrend`，价格低于 ma20 与 ma60，`range_pos_60` -0.0223。

**解读：**

- 科技 ETF 没有提供主题确认，因此不支持单一科技股升级。
- `1810.HK` 当前不具备 swing 多头结构。
- 状态：`watch_only`，偏弱观察。

### 3.11 医疗医药：当前不具备行动条件

**事实：**

- `2269.HK`、`1177.HK`、`1093.HK` 均为 score 0。
- 三者均低于 ma20 与 ma60，并带有 `downtrend`。
- `1177.HK` 与 `1093.HK` 还有 `symbol_risk_veto`。

**解读：**

- 医疗医药方向当前不是可操作强主题。
- 状态：`watch_only` / avoid new action。

## 4. ETF 确认

**事实：**

- `2800.HK`：score 31.25，`range`，单日 -0.46%，低于 watch 门槛。
- `3033.HK`：score 19.65，`range`，单日 -0.62%，低于 watch 门槛。
- `3067.HK`：score 0，`downtrend`，单日 -0.58%。
- 三只 ETF 均有 `low_volume_ratio_20_below_0_6`。

**解读：**

- 大盘与科技 ETF 均未确认风险偏好扩张。
- 根据“优先用 ETF 做主题确认”的规则，本轮不能用单一个股强势替代 ETF 确认。
- 防御、公用事业、能源、金融个股的相对强势更像局部轮动，不是全市场广谱买入信号。

## 5. 突出标的与最佳主题表达

| 主题 | 交易宇宙内最佳表达 | 事实依据 | 当前状态 |
|---|---|---|---|
| `energy` | `0883.HK` | score 56.90，全市场最高；uptrend；价在 ma20/ma60 上方 | `watch_only` / veto audit |
| `telecom-dividend` | `0941.HK` | score 55.11；uptrend；主题 leader | `watch_only` / veto audit |
| `utilities-defensive` | `0002.HK` | score 54.49；uptrend；主题 leader | `watch_only` |
| `financials-exchange` | `0388.HK` | score 52.49；uptrend；单日 +1.10% | `watch_only` |
| `financials-bank` | `0005.HK` | score 51.02；uptrend；价在 ma20/ma60 上方 | `watch_only` |
| `internet-platform` | `9618.HK` | 主题内 score 50.86，明显强于 `0700.HK`、`9988.HK` | `watch_only` |
| `consumer-discretionary` | `2020.HK` | 主题内 score 46.78，唯一略高于 watch 门槛 | `watch_only` |
| `hang-seng-tech` | `3033.HK` | 主题内领先，但 score 19.65 且 ETF 未确认 | `watch_only` |

**结论：**

- 今天没有 `buy_candidate`。
- 最重要的观察对象不是“买入清单”，而是 veto 后的主题强弱审计：`0883.HK`、`0941.HK`、`0002.HK`、`0388.HK`、`0005.HK`。
- 若后续日期对齐数据出现，必须重新验证：量能、ETF 确认、是否进入 `actionable_candidates`、以及是否解除 `symbol_risk_veto`。

## 6. 风险姿态

**事实：**

- 组合模式为 `recommendation_only`，无真实持仓。
- 风险配置为 balanced，单一仓位上限 10%，主题上限 30%，不允许杠杆、不允许反向 ETF、不允许低流动性。
- 交易成本假设：往返 35 bps；最小边际收益要求 100 bps；需要预期 swing edge 明显超过交易成本。
- 本轮 `actionable_candidates=[]`。
- 主要高分候选普遍存在 `low_volume_ratio_20_below_0_6` 与/或 `symbol_risk_veto`。

**解读：**

- 风险姿态应保持防守性审计，而非主动进攻。
- 非日期对齐行情不能提供当日触发价或同日行动确认。
- 即使个别标的趋势分较高，也不能覆盖低量能、后验风险否决与空行动列表。

## 7. 今日 recommendation state

### 总体状态：`watch_only`

**理由：**

1. `actionable_candidates` 为空，确定性行动层没有可升级对象。
2. 行情数据与 `as_of_date` 非日期对齐，不能提供同日交易确认。
3. 高分 diagnostic candidates 均为 `diagnostic_only=true` 且 `qualified_for_action=false`。
4. 排名前列标的普遍受到 `symbol_risk_veto` 与低量能限制。
5. ETF 层面没有确认大盘或科技风险偏好扩张。

**失效条件 / 重新评估条件：**

- 若后续日期对齐快照显示某标的进入 `actionable_candidates`；
- 且价格继续维持在 ma20 与 ma60 上方；
- 且量能不再触发 `low_volume_ratio_20_below_0_6`；
- 且 `symbol_risk_veto` 不再存在或有明确的新鲜相对强弱证据；
- 且预期 14-90 天 swing edge 明确超过 100 bps 与 35 bps 成本门槛；
- 才能重新讨论从 `watch_only` 升级为 `buy_candidate`。

## 8. 今天的高优先级研究问题

1. `0883.HK` 与 `0857.HK` 的能源强势是否有真实日期对齐的放量确认，还是仅由非日期对齐快照造成的审计噪音？
2. 防御主题中 `0002.HK` 与 `0006.HK` 的高 `range_pos_60` 是否代表趋势延续，还是接近短期拥挤区，需要等待回撤后再评估？
3. `0941.HK` 的趋势结构很强，但后验 pass_rate 极低：过去失败主要是入场时点错误、主题拥挤，还是标的选择本身不适合 swing？
4. 互联网平台中 `9618.HK` 当前明显强于 `0700.HK` 与 `9988.HK`：这种相对强势是否持续，并能否在日期对齐数据中战胜近期 best peer？
5. ETF 确认不足时，是否应将所有单股强势统一降级为“主题审计”，直到 `2800.HK` 或 `3033.HK` 出现可验证的 T+3/T+5 edge？
