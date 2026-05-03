# 2025-12-18 港股市场评估

> 会话：historical  
> 模式：recommendation_only  
> 时间窗口：14-90 天 swing  
> 风险配置：balanced，单一标的上限 10%，主题上限 30%，不使用杠杆/反向 ETF/低流动性标的  
> 数据注意：本轮输入的 `as_of_date` 是 `2025-12-18`，但行情字段 `quote_trade_date` / `as_of` 显示为 `2026-04-28`。根据稳定规则，日期不一致时，所有结论只能作为低置信度观察或条件观察，不能升级为立即行动建议。

## 1. 市场雷达：事实与主题强弱

### 1.1 市场状态事实

- `market_summary.risk_state`: `risk_off`
- 雷达股票平均 1 日涨跌：-0.946%
- 雷达 ETF 平均 1 日涨跌：-1.847%
- 当日领涨：
  - `0883.HK` CNOOC：+1.90%，`uptrend`
  - `0857.HK` PetroChina：+1.83%，`uptrend`
  - `2269.HK` WuXi Biologics：+1.26%，但仍为 `downtrend` 且 `volume-expansion`
- 当日落后：
  - `1093.HK` CSPC Pharma：-4.54%，`downtrend`
  - `1810.HK` Xiaomi：-3.79%，`downtrend`
  - `1024.HK` Kuaishou：-3.12%，`downtrend`

### 1.2 按主题强度排序的事实

确定性排名显示，当前强势主题集中在防御、股息与能源：

| 主题 | 平均分 | 主题领先标的 | 领先分数 | 解释状态 |
|---|---:|---|---:|---|
| `utilities-defensive` | 72.44 | `0006.HK` | 75.51 | 强，但主题领先标的有 `symbol_risk_veto` |
| `telecom-dividend` | 67.53 | `0941.HK` | 76.46 | 强，但主题领先标的有 `symbol_risk_veto` |
| `energy` | 56.81 | `0857.HK` | 81.90 | 价格动量最强，但主题领先标的有 `symbol_risk_veto` |
| `financials-bank` | 55.08 | `0005.HK` | 55.08 | 趋势尚可，但成交量低于门槛 |
| `financials-exchange` | 47.16 | `0388.HK` | 47.16 | 可观察，但未达行动分数 |
| `internet-platform` | 16.40 | `9618.HK` | 63.25 | 主题整体弱，仅 `9618.HK` 相对突出 |
| `consumer-discretionary` | 15.05 | `2020.HK` | 39.75 | 弱，不达观察门槛 |
| `hong-kong-broad-market` | 0.00 | `2800.HK` | 0 | 弱，指数 ETF 不确认 |
| `hang-seng-tech` | 0.00 | `3033.HK` | 0 | 弱，科技 ETF 不确认 |
| `consumer-tech` | 0.00 | `1810.HK` | 0 | 弱 |
| `financials-insurance` | 0.00 | `1299.HK` | 0 | 弱 |
| `healthcare-biotech` | 0.00 | `2269.HK` | 0 | 单日反弹但趋势未修复 |
| `healthcare-pharma` | 0.00 | `1177.HK` | 0 | 弱 |

### 1.3 解释

当前不是广泛风险偏好恢复，而是典型的 `risk_off` 下的分化：能源、通信股息、公用事业等防御/现金流主题相对强，恒生科技、互联网平台、消费科技和医药整体偏弱。雷达的强弱结构支持“防御优先观察”，不支持追逐高 beta 科技反弹。

## 2. 哪些雷达主题在交易池内可表达

本轮雷达强主题均在 trade universe 内有代表，因此不存在“强雷达主题未进入交易池”的外部机会缺口。需要做的是：在交易池内部比较同主题标的，并确认是否有资格从观察升级为行动。

### 2.1 `energy`：强主题，但主题领先标的被风险否决

事实：

- `0857.HK`：score 81.90，`uptrend`，价格高于 MA20/MA60，MA20 高于 MA60，`volume_ratio_20` 1.2254，`range_pos_60` 1.0769。
- `0883.HK`：score 72.45，`uptrend`，价格高于 MA20/MA60，MA20 高于 MA60，但 `volume_ratio_20` 0.8064，且不是主题分数领先者。
- `0386.HK`：score 16.09，未达观察门槛，`range_pos_60` 0.0932，弱于同主题。
- `0857.HK` 有 `symbol_risk_veto`：历史平均回报 -12.408%，记录中有 -8% 以上不利回撤与 symbol selection error。
- `0883.HK` 没有 `symbol_risk_veto`，但被 `not_theme_score_leader` 限制，且不满足主题领先规则。

解释：

能源是当前最清晰的动量主题之一，但确定性层的最强表达 `0857.HK` 被历史风险否决，不能升级。`0883.HK` 是更干净的替代观察标的，但它不是模型主题领先者，成交量确认也不强，因此只能作为“替代表达观察”，不能越过 `actionable_candidates` 为空这一硬门槛。

当前最佳表达：`0883.HK` 用于观察能源主题持续性；`0857.HK` 用于解释主题强度，但不作为行动候选。

状态：`watch_only`

### 2.2 `telecom-dividend`：防御强，但领先标的被风险否决

事实：

- `0941.HK`：score 76.46，`uptrend`，价格高于 MA20/MA60，MA20 高于 MA60，`volume_ratio_20` 1.0334，`range_pos_60` 1.0362。
- `0728.HK`：score 58.59，`range`，价格高于 MA20/MA60，`volume_ratio_20` 1.3878，但 MA20 仍低于 MA60，且不是主题领先者。
- `0941.HK` 有 `symbol_risk_veto`：pass_rate=0.167，平均回报 -0.413%，记录包含 symbol_selection_error。

解释：

通信股息主题符合 `risk_off` 环境下的防御偏好，但主表达 `0941.HK` 被历史表现否决。`0728.HK` 量能更活跃，但趋势质量弱于 `0941.HK`，且同主题非领先。这个主题可观察，不可立即升级。

当前最佳表达：`0728.HK` 作为更干净但趋势较弱的替代观察；`0941.HK` 作为主题强度参考，不作为行动候选。

状态：`watch_only`

### 2.3 `utilities-defensive`：主题分数最高，但行动门槛仍未通过

事实：

- `0006.HK`：score 75.51，`uptrend`，价格高于 MA20/MA60，MA20 高于 MA60，`volume_ratio_20` 1.0304，`range_pos_60` 1.0092。
- `0002.HK`：score 69.37，`uptrend`，价格高于 MA20/MA60，MA20 高于 MA60，但 `volume_ratio_20` 0.645，且不是主题领先者。
- `0006.HK` 有 `symbol_risk_veto`：pass_rate=0，平均回报 -5.185%，记录中有 -8% 以上不利回撤与 symbol_selection_error。

解释：

公用事业是当前最强的防御主题之一，但最强标的 `0006.HK` 被历史风险否决。`0002.HK` 是较干净的替代表达，但成交量不足且不是主题领先者。主题方向可继续跟踪，但没有可升级的交易候选。

当前最佳表达：`0002.HK` 用于替代观察，等待量能改善；`0006.HK` 只保留为主题温度计。

状态：`watch_only`

### 2.4 `financials-bank` / `financials-exchange`：可观察，但证据不足

事实：

- `0005.HK`：score 55.08，`uptrend`，价格高于 MA20/MA60，MA20 高于 MA60，`range_pos_60` 0.8645；但 `volume_ratio_20` 0.507，触发 `low_volume_ratio_20_below_0_6`。
- `0388.HK`：score 47.16，`range`，价格略高于 MA20/MA60，`range_pos_60` 0.4559，`volume_ratio_20` 0.872。

解释：

金融内部不是统一强势。`0005.HK` 趋势好但量能不足，`0388.HK` 更像区间修复而非趋势突破。二者都未达到行动分数，适合放入观察清单而不是交易候选。

当前最佳表达：偏趋势选择 `0005.HK`，偏市场活跃度/成交敏感选择 `0388.HK`；但二者均为观察。

状态：`watch_only`

### 2.5 `internet-platform`：主题弱，仅 `9618.HK` 相对强

事实：

- `9618.HK`：score 63.25，低于行动门槛 65；`uptrend`，价格高于 MA20/MA60，MA20 高于 MA60，`range_pos_60` 0.7237，但 `volume_ratio_20` 0.9333。
- `0700.HK`、`9988.HK`、`1024.HK`：均为 `downtrend`，且 `0700.HK`、`9988.HK` 有低 pass rate / selection error 等风险记录。
- 恒生科技 ETF `3033.HK`、`3067.HK` 均为 `downtrend`，分数为 0。

解释：

互联网平台主题没有 ETF 确认，且大多数核心标的处于下行趋势。`9618.HK` 是当前同主题内相对最好的表达，但它低于行动分数，也缺少 ETF 背书。根据“互联网单股需要 ETF 确认”和“空 actionable_candidates 不升级”的规则，不能给出买入候选。

当前最佳表达：`9618.HK` 作为相对强弱观察标的。

状态：`watch_only`

### 2.6 弱主题：暂不作为今日主线

事实：

- `hong-kong-broad-market`：`2800.HK` score 0，`downtrend`，价格低于 MA20/MA60。
- `hang-seng-tech`：`3033.HK`、`3067.HK` score 0，均为 `downtrend`，价格低于 MA20/MA60。
- `consumer-tech`：`1810.HK` score 0，`downtrend`，单日 -3.79%。
- `consumer-discretionary`：主题均分 15.05，领先 `2020.HK` 也只有 39.75。
- `healthcare-biotech`：`2269.HK` 单日上涨且放量，但仍处 `downtrend`。
- `healthcare-pharma`：`1177.HK`、`1093.HK` 均弱。

解释：

这些主题缺少趋势、ETF 或同主题广度确认。若有反弹，也更像短线波动而非 14-90 天 swing 的可执行优势。

状态：`watch_only`

## 3. ETF 确认

### 3.1 事实

- `2800.HK`：latest_close 25.98，低于 MA20 25.993 与 MA60 26.36，`downtrend`，score 0。
- `3033.HK`：latest_close 4.726，低于 MA20 4.7682 与 MA60 4.9981，`downtrend`，score 0。
- `3067.HK`：latest_close 10.15，低于 MA20 10.238 与 MA60 10.7185，`downtrend`，score 0。

### 3.2 解释

宽基与科技 ETF 均不确认风险偏好修复。尤其是科技 ETF 仍在 MA20/MA60 下方，意味着不能用单个互联网平台或消费科技标的的局部相对强势来升级整体科技/互联网主题。ETF 层的结论是：风险资产反弹证据不足，防御/股息/能源相对强，但不宜扩大到广泛风险偏好判断。

## 4. 今日候选与推荐状态

### 4.1 确定性层结论

- `actionable_candidates`: 空
- `diagnostic_candidates`: `0857.HK`、`0941.HK`、`0006.HK`
- 由于 `actionable_candidates` 为空，所有诊断候选只能用于解释和观察，不能升级为 `buy_candidate`、`accumulate` 或 `hold`。

### 4.2 高优先级观察清单

| 优先级 | 标的 | 主题 | 当前状态 | 主要理由 | 不能升级的原因 |
|---:|---|---|---|---|---|
| 1 | `0883.HK` | `energy` | `watch_only` | 能源强势、`uptrend`、无 `symbol_risk_veto` | 非主题分数领先，量能未明显扩张，`actionable_candidates` 为空 |
| 2 | `0728.HK` | `telecom-dividend` | `watch_only` | 通信股息强，量能较好 | 非主题领先，MA20 未高于 MA60，`actionable_candidates` 为空 |
| 3 | `0002.HK` | `utilities-defensive` | `watch_only` | 防御主题强，趋势结构较稳 | 非主题领先，量能偏弱，`actionable_candidates` 为空 |
| 4 | `9618.HK` | `internet-platform` | `watch_only` | 同主题内相对最强，仍为 `uptrend` | 分数低于 65，科技 ETF 不确认 |
| 5 | `0388.HK` | `financials-exchange` | `watch_only` | 分数过观察线，区间中性 | 未达行动门槛，趋势不够强 |

## 5. 风险姿态

### 5.1 事实

- 市场状态为 `risk_off`。
- ETF 平均 1 日跌幅大于股票平均跌幅。
- 宽基 ETF 与科技 ETF 均处于 `downtrend`。
- 确定性排名没有任何 `actionable_candidates`。
- 多个高分主题领先标的存在 `symbol_risk_veto`。
- 当前历史回放数据存在 `as_of_date` 与行情日期不一致。

### 5.2 解释

今日风险姿态应保持保守：不追涨高分诊断候选，不把防御主题强势直接转化为买入建议，也不在科技 ETF 未修复前升级互联网平台单股。更合适的工作是建立条件触发清单，等待日期对齐、ETF 确认、量能确认和同主题替代表达确认。

## 6. 条件触发与失效条件

以下不是立即交易建议，只是后续观察条件。

### `0883.HK` 能源替代表达

- 触发条件：继续保持 MA20/MA60 上方，`volume_ratio_20` 回到 1.0 以上，且能源主题不只由 `0857.HK` 单独带动。
- 失效条件：跌回 MA20 下方，或能源主题内部只剩单一标的强势，或油气主题领涨消失。
- 时间窗口：14-45 天观察。
- 信心：低到中，原因是主题强但确定性层未给出行动候选。

### `0728.HK` 通信股息替代表达

- 触发条件：MA20 上穿或明显修复至 MA60 上方，成交量继续高于 20 日均量，且 `0941.HK` 的风险否决不再迫使主题只能靠低质量领先标的表达。
- 失效条件：跌破 MA20，或通信股息主题相对强度消失。
- 时间窗口：14-60 天观察。
- 信心：低。

### `0002.HK` 公用事业替代表达

- 触发条件：量能改善至接近或高于 20 日均量，同时保持 MA20/MA60 上方。
- 失效条件：跌破 MA20，或防御主题轮动结束。
- 时间窗口：14-60 天观察。
- 信心：低。

### `9618.HK` 互联网平台相对强者

- 触发条件：分数升至 65 以上，同时 `3033.HK` / `3067.HK` 至少重新站上 MA20，并最好出现 MA60 修复迹象。
- 失效条件：跌破 MA20，或同主题更强标的出现且 `9618.HK` 相对强度下降。
- 时间窗口：14-45 天观察。
- 信心：低，因 ETF 不确认。

## 7. 今日结论

今日没有可升级的确定性交易候选。市场雷达显示防御、通信股息和能源相对强，但这些主题的模型领先标的要么被 `symbol_risk_veto` 否决，要么替代表达缺少独立的趋势、量能、相对强度和风险门槛确认。科技、互联网和宽基 ETF 均未确认，不能用单股局部强势提前下注。

因此，本轮推荐状态为：整体 `watch_only`。今天的任务不是买入，而是确认哪些强主题能从“防御性相对强”进化为“可执行 swing 边际”。

## 8. 今日高优先级研究问题

1. `0883.HK` 是否能在后续交易日以更强量能确认能源主题，而不是继续落后于被风险否决的 `0857.HK`？
2. `0728.HK` 能否完成 MA20/MA60 趋势修复，并成为比 `0941.HK` 更干净的通信股息表达？
3. `0002.HK` 的量能是否能改善到足以替代被风险否决的 `0006.HK`？
4. `3033.HK` / `3067.HK` 是否能重新站上 MA20，从而为 `9618.HK` 这类互联网平台相对强者提供 ETF 确认？
5. 当前历史回放的日期错配是否会影响排名有效性？是否能取得与 `2025-12-18` 对齐的行情快照来复核今日判断？
