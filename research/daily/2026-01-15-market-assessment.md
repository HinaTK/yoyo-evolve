# 2026-01-15 港股市场评估

> 模式：historical replay / recommendation_only  
> 适用周期：14-90 天 swing 观察  
> 重要约束：`actionable_candidates` 为空，因此本轮没有任何确定性层面可升级为 `buy_candidate`、`accumulate` 或 `hold` 的标的；所有标的最多为 `watch_only` 或条件观察。另：输入的 `as_of_date=2026-01-15`，但行情字段 `quote_trade_date=2026-04-29`，存在日期不一致，进一步降低行动置信度。

## 1. 事实层：市场雷达结果

### 1.1 市场状态

- `market_summary.risk_state`: `risk_on`
- 雷达股票平均单日涨幅：`avg_stock_move_1d=1.606%`
- 雷达 ETF 平均单日涨幅：`avg_etf_move_1d=1.7%`
- 雷达领涨：
  - `3690.HK`：+3.55%，theme=`internet-platform`
  - `9988.HK`：+3.24%，theme=`internet-platform`
  - `0388.HK`：+2.99%，theme=`financials-exchange`，且 `volume-expansion`
- 雷达落后：
  - `1093.HK`：-0.59%，theme=`healthcare-pharma`，`downtrend`
  - `0006.HK`：-0.38%，theme=`utilities-defensive`，但仍为 `uptrend`
  - `1177.HK`：-0.36%，theme=`healthcare-pharma`，`downtrend`

### 1.2 按主题强度排序（来自 deterministic ranking）

| 排名 | theme | avg_score | leader | leader_score | 事实摘要 |
|---:|---|---:|---|---:|---|
| 1 | `utilities-defensive` | 75.47 | `0002.HK` | 76.08 | 两个成员均偏强，`0002.HK`、`0006.HK` 都在 MA20/MA60 上方 |
| 2 | `telecom-dividend` | 75.00 | `0941.HK` | 81.98 | `0941.HK` 强趋势并放量，`0728.HK` 亦放量但非主题 leader |
| 3 | `financials-bank` | 71.01 | `0005.HK` | 71.01 | 单一成员，价格在 MA20/MA60 上方 |
| 4 | `energy` | 69.67 | `0857.HK` | 84.42 | `0857.HK` 分数最高，`0883.HK` 也强，`0386.HK` 放量但非 leader |
| 5 | `financials-exchange` | 67.30 | `0388.HK` | 67.30 | 单日强势并放量，分数过 action 门槛但被风险 veto |
| 6 | `financials-insurance` | 58.00 | `1299.HK` | 58.00 | 中等分数，仅 watch 阈值以上 |
| 7 | `hong-kong-broad-market` | 56.60 | `2800.HK` | 56.60 | ETF 上涨且成交确认，但低于 action 分数 |
| 8 | `hang-seng-tech` | 43.52 | `3067.HK` | 44.39 | 低于 watch 阈值；ETF 仍低于 MA60 |
| 9 | `internet-platform` | 32.34 | `9618.HK` | 72.27 | 主题均值弱，但内部有分化，`9618.HK` 强于同组 |
| 10 | `consumer-discretionary` | 27.02 | `2020.HK` | 55.36 | 主题均值弱；`2020.HK` 分数中等但量能不足 |
| 11 | `consumer-tech` | 0.00 | `1810.HK` | 0.00 | 下行趋势，接近 60 日区间低位 |
| 12 | `healthcare-biotech` | 0.00 | `2269.HK` | 0.00 | 下行趋势 |
| 13 | `healthcare-pharma` | 0.00 | `1177.HK` | 0.00 | `1177.HK`、`1093.HK` 均为下行结构 |

## 2. 解释层：市场结构判断

- 表面上是 `risk_on`：多数雷达标的上涨，ETF 平均涨幅约 1.7%，互联网、金融交易所、能源、电信与防御公用事业均有局部强势。
- 但这不是干净的全面进攻信号：
  1. `actionable_candidates=[]`，确定性交易层没有给出可升级标的。
  2. top diagnostic candidates `0857.HK`、`0941.HK`、`0002.HK` 均因 `symbol_risk_veto` 被挡下。
  3. 科技 ETF `3033.HK`、`3067.HK` 仍低于 MA60，且分数低于 watch 阈值，不能为互联网或科技单名提供足够 ETF 确认。
  4. replay 日期与 quote 日期不一致，所有行情触发只能视作审计线索，不可视作日期对齐的实时确认。

结论：本轮应定义为“选择性 risk_on + 高 veto 压力 + 无可行动候选”。研究重点应放在主题审计、peer-relative 对比和触发条件，而不是生成买入建议。

## 3. ETF 确认

### 3.1 `2800.HK` / 港股宽基

**事实：**
- 最新收盘 26.24，+1.74%。
- 价格高于 MA20=25.8446，也略高于 MA60=26.1507。
- `volume_ratio_20=1.1216`，成交确认尚可。
- ranking score=56.60，低于 `min_action_score=65`。
- `symbol_risk_veto=true`，历史 pass_rate 低，且近期存在 `2800.HK` bullish misfire。

**解释：**
- 宽基有修复迹象，但不足以升级。过去 broad-index ETF bullish failures 要求 breadth、volume、moving-average 三重确认；目前只看到局部价格和量能确认，且 deterministic action list 为空。
- 最佳状态：`watch_only`，用于判断整体风险偏好是否延续。

### 3.2 `3033.HK` / `3067.HK` 恒生科技 ETF

**事实：**
- `3033.HK`：4.81，+1.78%，高于 MA20=4.7717，但低于 MA60=4.9835，`volume_ratio_20=0.6564`，score=42.65。
- `3067.HK`：10.31，+1.58%，高于 MA20=10.2455，但低于 MA60=10.6875，`volume_ratio_20=1.0774`，score=44.39。
- 两者均低于 `min_watch_score=45`，且均有 `symbol_risk_veto`。

**解释：**
- 科技 ETF 反弹不足以确认互联网平台或消费科技的 swing 升级。尤其在 MA60 未收复、分数低于 watch 门槛的情况下，不能用单日上涨解释为趋势反转。
- `3067.HK` 是当前 hang-seng-tech 中相对更好的表达，但仍只能列为观察，不是交易候选。

## 4. 雷达主题在 trade universe 内的可行动性

本轮 radar 主题均已在 trade universe 中有代表标的，因此没有“强雷达但未纳入交易池”的外部机会需要立即标注为新增。下面只讨论 trade universe 内的最佳表达与限制。

### 4.1 `energy`

**可选标的：** `0857.HK`、`0883.HK`、`0386.HK`

**事实对比：**
- `0857.HK`：score=84.42，主题 leader，+2.66%，MA20/MA60 多头排列，`volume_ratio_20=1.2356`，但 `symbol_risk_veto=true`。
- `0883.HK`：score=73.93，趋势强，+1.38%，但非主题 leader，`symbol_risk_veto=true`。
- `0386.HK`：score=50.67，+2.40%，`volume_ratio_20=2.2023`，`symbol_risk_veto=false`，但低于 action 分数，且非主题 leader，`qualified_for_watch=false`。

**解释：**
- 主题本身很强，最佳当前表达按模型是 `0857.HK`，但它被风险 veto 阻断。
- 不能因为 `0386.HK` 没有 veto 就替代升级；规则要求同主题替代必须独立进入 action list，并证明相对 veto leader 的新强度。本轮不满足。
- 状态：`watch_only`。研究重点是比较 `0386.HK` 是否能持续跑赢 `0857.HK` 和 `0883.HK`，而不是直接交易。

### 4.2 `telecom-dividend`

**可选标的：** `0941.HK`、`0728.HK`

**事实对比：**
- `0941.HK`：score=81.98，主题 leader，`uptrend` + `volume-expansion`，但 `symbol_risk_veto=true`。
- `0728.HK`：score=68.01，放量，价格高于 MA20/MA60，但非主题 leader，且 `symbol_risk_veto=true`。

**解释：**
- 电信股是雷达强主题之一，但两只可选标的都被 posterior risk gate 限制。
- `0941.HK` 是最强表达，但不能升级；`0728.HK` 也不能作为替代。
- 状态：`watch_only`，关注是否出现连续日期对齐的放量突破以及风险 veto 是否在后续复核中缓解。

### 4.3 `utilities-defensive`

**可选标的：** `0002.HK`、`0006.HK`

**事实对比：**
- `0002.HK`：score=76.08，主题 leader，价格高于 MA20/MA60，`volume_ratio_20=1.2769`，但 `symbol_risk_veto=true`。
- `0006.HK`：score=74.86，趋势强但单日 -0.38%，非主题 leader，`symbol_risk_veto=true`。

**解释：**
- 防御公用事业分数最高，但强势更偏“稳健趋势/防御拥挤”，不等同于 swing 买点。
- 两者都被 veto，且 `0006.HK` 非 leader，不能替代 `0002.HK`。
- 状态：`watch_only`，不追高。

### 4.4 `financials-bank` / `financials-exchange` / `financials-insurance`

**可选标的：** `0005.HK`、`0388.HK`、`1299.HK`

**事实对比：**
- `0005.HK`：score=71.01，价格高于 MA20/MA60，`uptrend`，但 `symbol_risk_veto=true`。
- `0388.HK`：score=67.30，+2.99%，`volume_ratio_20=1.5564`，`volume-expansion`，但 `symbol_risk_veto=true`。
- `1299.HK`：score=58.00，+2.16%，接近 MA60，低于 action 分数，`symbol_risk_veto=true`。

**解释：**
- 金融内部最有短线弹性的观察对象是 `0388.HK`，因其单日涨幅和量能最好；最稳趋势表达是 `0005.HK`。
- 但三者均不能升级。`0388.HK` 尤其适合作为“成交放大是否延续”的观察样本。
- 状态：全部 `watch_only`。

### 4.5 `hong-kong-broad-market`

**可选标的：** `2800.HK`

**事实与解释：**
- `2800.HK` 是唯一宽基表达；有价格和量能修复，但 score=56.60、低于 action 门槛，且被 `symbol_risk_veto` 限制。
- 状态：`watch_only`。它更适合作为广度确认工具，而非本轮交易对象。

### 4.6 `internet-platform`

**可选标的：** `0700.HK`、`9988.HK`、`3690.HK`、`1024.HK`、`9618.HK`

**事实对比：**
- `9618.HK`：score=72.27，主题 leader，`uptrend`，价格高于 MA20/MA60，但 `volume_ratio_20=0.7545`，且 `symbol_risk_veto=true`。
- `9988.HK`：+3.24%，但 score=44.75，低于 watch 分数，非 leader，且 `symbol_risk_veto=true`。
- `3690.HK`：雷达单日 leader，+3.55%，但 score=44.67，低于 watch 分数，价格低于 MA20/MA60，非 leader。
- `0700.HK`：score=0，`downtrend`，低位，且 `symbol_risk_veto=true`。
- `1024.HK`：score=0，`downtrend`，低位，且 `symbol_risk_veto=true`。

**解释：**
- 互联网平台出现单日反弹，但主题均值只有 32.34，ETF 确认不足，且近期 selected-vs-best 错误集中在该组。
- 当前最佳结构表达是 `9618.HK`，不是单日涨幅最大的 `3690.HK` 或 `9988.HK`；但 `9618.HK` 仍被风险 veto，且没有进入 action list。
- 状态：全部 `watch_only`。任何升级前必须证明：科技 ETF 收复 MA60、`9618.HK` 或替代 peer 连续跑赢同组、且不再被 action layer 排除。

### 4.7 `consumer-discretionary`

**可选标的：** `2020.HK`、`2331.HK`、`9992.HK`、`6862.HK`

**事实对比：**
- `2020.HK`：score=55.36，主题 leader，价格高于 MA20/MA60，但 `volume_ratio_20=0.5795` 低于量能门槛，且 `symbol_risk_veto=true`。
- `2331.HK`：score=33.54，低于 watch。
- `9992.HK`：score=19.18，低于 watch，且 60 日区间位置偏低。
- `6862.HK`：score=0，`downtrend`。

**解释：**
- 可选表达中 `2020.HK` 相对最好，但量能不足和 veto 使其不具备行动资格。
- 状态：`watch_only`；除非 `2020.HK` 重新放量并进入 action list，否则不升级。

### 4.8 `consumer-tech`、`healthcare-biotech`、`healthcare-pharma`

**可选标的：** `1810.HK`、`2269.HK`、`1177.HK`、`1093.HK`

**事实：**
- `1810.HK`：score=0，`downtrend`，低于 MA20/MA60，`range_pos_60=0.0306`。
- `2269.HK`：score=0，`downtrend`，低于 MA20/MA60。
- `1177.HK`：score=0，`downtrend`，`range_pos_60=-0.0144`。
- `1093.HK`：score=0，`downtrend`，`range_pos_60=0.0791`。

**解释：**
- 这些主题没有可用的多头 swing 结构。即使部分标的有单日反弹，也应视为下跌趋势中的波动，而不是确认。
- 状态：`watch_only`，不做 `avoid`，因为规则要求在低 pass-rate 或 rebound-prone 标的上避免无充分广度证据的防御性判断。

## 5. 风险姿态

- 本轮风险姿态：防守型观察，而非进攻型建仓。
- 主要风险：
  1. **日期不一致风险**：`as_of_date` 与 quote 日期冲突，所有行情只能作为 replay 审计输入。
  2. **模型行动层为空**：`actionable_candidates=[]`，阻断所有升级。
  3. **posterior veto 集中**：高分主题 leader 多数被 `symbol_risk_veto` 阻断。
  4. **科技 ETF 确认不足**：`3033.HK`、`3067.HK` 未收复 MA60，不能支持互联网平台升级。
  5. **peer-selection 风险**：互联网主题近期多次出现 selected-vs-best underperformance，不能只凭单名反弹或当前 leader 分数升级。

## 6. 今日结论与观察清单

### 6.1 推荐状态汇总

| symbol | theme | 当前状态 | 原因 |
|---|---|---|---|
| `0857.HK` | `energy` | `watch_only` | 分数最高但 `symbol_risk_veto`，且 action list 为空 |
| `0941.HK` | `telecom-dividend` | `watch_only` | 强趋势放量但 `symbol_risk_veto` |
| `0002.HK` | `utilities-defensive` | `watch_only` | 强趋势但 `symbol_risk_veto` |
| `0388.HK` | `financials-exchange` | `watch_only` | 放量强势但 `symbol_risk_veto` |
| `2800.HK` | `hong-kong-broad-market` | `watch_only` | 宽基修复但低于 action 分数，且近期 bullish failures |
| `3067.HK` / `3033.HK` | `hang-seng-tech` | `watch_only` | 未收复 MA60，低于 watch 分数 |
| `9618.HK` | `internet-platform` | `watch_only` | 同组最佳结构但 `symbol_risk_veto`，ETF 确认不足 |

### 6.2 不升级的明确条件

本轮没有 `buy_candidate`。只有在后续出现以下变化时，才可重新讨论升级：

1. `actionable_candidates` 不再为空，且候选标的 `qualified_for_action=true`。
2. replay 数据的 `as_of_date` 与行情日期对齐，或有独立日期对齐证据。
3. 对于互联网/科技相关标的，`3033.HK` 或 `3067.HK` 至少收复 MA60，并伴随成交确认。
4. 对被 veto 的主题 leader，风险 veto 解除；若选择同主题替代 peer，该 peer 必须进入 action list，并证明相对 veto leader 与近期 best peer 的新强度。

## 7. 今日高优先级研究问题

1. `actionable_candidates=[]` 的主因是历史风险 veto 过强，还是日期不一致导致的 ranking 审计降级？需要核对日期对齐后的候选列表。
2. 在 `energy` 中，`0386.HK` 的放量是否能连续 3-5 个交易日跑赢 `0857.HK` 与 `0883.HK`，从而成为非 veto 替代表达？
3. `internet-platform` 中，`9618.HK` 是否继续相对 `0700.HK`、`9988.HK`、`3690.HK` 保持强度？近期 best peer 是否已从 `9988.HK` / `1024.HK` 切回 `9618.HK`？
4. `0388.HK` 的 `volume-expansion` 是单日事件还是交易所主题的持续资金流入？是否能连续站稳 MA20/MA60 上方？
5. `2800.HK` 能否提供真正的宽基确认：成交量、MA60、市场广度是否同时改善，而不是再次形成 broad-index ETF bullish failure？
