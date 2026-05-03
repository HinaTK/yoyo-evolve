# 2026-01-20 港股市场评估

> 会话：historical  
> 角色：yoyo-invest  
> 模式：recommendation_only  
> 适用周期：14-90 天 swing 观察  
> 重要数据约束：本轮输入的 `as_of_date` 为 `2026-01-20`，但行情字段 `quote_trade_date` / `as_of` 显示为 `2026-04-29`。按稳定规则，本报告只把排名与行情作为诊断材料，所有推荐上限为 `watch_only` / 审计观察，不作即时升级。

## 1. 结论摘要

### 事实

- 市场雷达给出的 `risk_state` 为 `risk_on`。
- 股票平均单日涨幅 `avg_stock_move_1d` 为 `1.606%`，ETF 平均单日涨幅 `avg_etf_move_1d` 为 `1.7%`。
- 雷达领涨：`3690.HK` +3.55%、`9988.HK` +3.24%、`0388.HK` +2.99%。
- 雷达落后：`1093.HK` -0.59%、`0006.HK` -0.38%、`1177.HK` -0.36%。
- 确定性排名的 `actionable_candidates` 为空。
- 诊断候选前三为 `0857.HK`、`0941.HK`、`0002.HK`，但三者均有 `symbol_risk_veto`，且均为 `diagnostic_only=true`、`qualified_for_action=false`。
- 主动策略仍为 `l5_mvp_conservative_v1`，参数优化未更新 active strategy。

### 解读

- 表面上是选择性 `risk_on`：指数与多数板块上涨，能源、电讯、公共事业、防御金融仍处强势，互联网平台有反弹但分化明显。
- 由于 `actionable_candidates=[]`、顶层诊断候选被 `symbol_risk_veto` 阻断、且历史回放日期与行情日期不一致，本轮不能把任何标的升级为 `buy_candidate`、`accumulate` 或 `hold`。
- 今天的主要任务不是下结论买入，而是做三件事：确认日期对齐数据、审计被 veto 的强势主题、比较同主题替代标的是否真的具备独立相对强度。

## 2. 市场雷达：按板块 / 主题强度排序

### 事实：主题排名

| 排名 | 主题 | 平均分 | 主题领头 | 领头分数 | 领头是否合格 | 代表成员 |
|---:|---|---:|---|---:|---|---|
| 1 | `utilities-defensive` | 75.47 | `0002.HK` | 76.08 | true | `0002.HK`, `0006.HK` |
| 2 | `telecom-dividend` | 75.00 | `0941.HK` | 81.98 | true | `0941.HK`, `0728.HK` |
| 3 | `financials-bank` | 71.01 | `0005.HK` | 71.01 | true | `0005.HK` |
| 4 | `energy` | 69.67 | `0857.HK` | 84.42 | true | `0857.HK`, `0883.HK`, `0386.HK` |
| 5 | `financials-exchange` | 67.30 | `0388.HK` | 67.30 | true | `0388.HK` |
| 6 | `financials-insurance` | 58.00 | `1299.HK` | 58.00 | true | `1299.HK` |
| 7 | `hong-kong-broad-market` | 56.60 | `2800.HK` | 56.60 | true | `2800.HK` |
| 8 | `hang-seng-tech` | 43.52 | `3067.HK` | 44.39 | false | `3067.HK`, `3033.HK` |
| 9 | `internet-platform` | 32.34 | `9618.HK` | 72.27 | true | `9618.HK`, `9988.HK`, `3690.HK`, `0700.HK`, `1024.HK` |
| 10 | `consumer-discretionary` | 27.02 | `2020.HK` | 55.36 | false | `2020.HK`, `2331.HK`, `9992.HK`, `6862.HK` |
| 11 | `consumer-tech` | 0.00 | `1810.HK` | 0.00 | false | `1810.HK` |
| 12 | `healthcare-biotech` | 0.00 | `2269.HK` | 0.00 | false | `2269.HK` |
| 13 | `healthcare-pharma` | 0.00 | `1177.HK` | 0.00 | false | `1177.HK`, `1093.HK` |

### 解读：雷达结构

- 强势集中在高股息 / 防御 / 资源：`utilities-defensive`、`telecom-dividend`、`financials-bank`、`energy` 分数领先。
- 交易所与保险也有修复迹象：`0388.HK` 放量上涨，`1299.HK` 站在 MA20 附近但仍未完全站稳 MA60。
- 科技与互联网不是全面强势：`internet-platform` 平均分低，主要被 `0700.HK`、`1024.HK` 的下行趋势拖累；`hang-seng-tech` ETF 分数低于观察门槛。
- 医药与生物科技仍处弱势，多个成员处 `downtrend`，不适合在本轮作为主动多头方向。

## 3. 交易宇宙内：哪些雷达主题可以落地

> 规则：只有 `actionable_candidates` 是确定性层面可考虑升级的名单。本轮 `actionable_candidates=[]`，因此所有主题均不能升级，只能形成观察队列。

### 3.1 `energy`

#### 事实

| 标的 | 分数 | 状态 | 关键事实 | 阻断因素 |
|---|---:|---|---|---|
| `0857.HK` | 84.42 | `diagnostic_only` | `uptrend`；价格高于 MA20/MA60；`volume_ratio_20=1.2356`；`range_pos_60=1.1084` | `symbol_risk_veto`；pass_rate=0.091 over 33；avg_return=-1.658% |
| `0883.HK` | 73.93 | `diagnostic_only` | `uptrend`；价格高于 MA20/MA60；`range_pos_60=0.8462` | 非主题分数领头；`symbol_risk_veto`；avg_return=-8.404% |
| `0386.HK` | 50.67 | `diagnostic_only` | `volume_ratio_20=2.2023`；放量；价格高于 MA20 | 非主题分数领头；未进入 `actionable_candidates`；MA60 仍高于现价 |

#### 解读

- 最强表达是 `0857.HK`，但它被 `symbol_risk_veto` 明确阻断，不能升级。
- `0386.HK` 虽然没有风险 veto 且放量明显，但它不是主题领头，分数只达观察区间，并且未进入 `actionable_candidates`。按规则，不能因为领头被 veto 就向下挖替代标的。
- `energy` 今天适合做 veto 审计与同主题相对强度跟踪，不适合形成即时推荐。

### 3.2 `telecom-dividend`

#### 事实

| 标的 | 分数 | 状态 | 关键事实 | 阻断因素 |
|---|---:|---|---|---|
| `0941.HK` | 81.98 | `diagnostic_only` | `uptrend` + `volume-expansion`；价格高于 MA20/MA60；`volume_ratio_20=1.5041` | `symbol_risk_veto`；pass_rate=0.000 over 30；近期有 adverse breach |
| `0728.HK` | 68.01 | `diagnostic_only` | `range` + `volume-expansion`；`volume_ratio_20=1.677`；价格高于 MA20 | 非主题分数领头；`symbol_risk_veto`；MA20 低于 MA60 |

#### 解读

- 最强表达是 `0941.HK`，趋势、量能和区间位置都强，但历史风险统计极差，必须保留为观察。
- `0728.HK` 有更强短线量能，但不是主题 leader，且同样有 veto，不能替代升级。
- 该主题可作为防御收益风格的强弱温度计，但不能给出买入候选。

### 3.3 `utilities-defensive`

#### 事实

| 标的 | 分数 | 状态 | 关键事实 | 阻断因素 |
|---|---:|---|---|---|
| `0002.HK` | 76.08 | `diagnostic_only` | `uptrend`；价格高于 MA20/MA60；`volume_ratio_20=1.2769` | `symbol_risk_veto`；pass_rate=0.000 over 3 |
| `0006.HK` | 74.86 | `diagnostic_only` | `uptrend`；价格高于 MA20/MA60；`volume_ratio_20=1.3544` | 非主题分数领头；`symbol_risk_veto`；当日 -0.38% |

#### 解读

- `0002.HK` 是该主题最佳表达，但样本少且 pass_rate 为 0，被 veto 阻断。
- `0006.HK` 分数接近，但不是 leader 且同样被 veto；不能替代。
- 公用事业强度偏“拥挤防御”，适合观察是否出现滞涨或回撤，而不是追高。

### 3.4 金融：`financials-bank`、`financials-exchange`、`financials-insurance`

#### 事实

| 主题 | 最佳表达 | 分数 | 关键事实 | 阻断因素 |
|---|---|---:|---|---|
| `financials-bank` | `0005.HK` | 71.01 | `uptrend`；价格高于 MA20/MA60；`range_pos_60=0.8805` | `symbol_risk_veto`；pass_rate=0.000 over 6；量能不足 `volume_ratio_20=0.7907` |
| `financials-exchange` | `0388.HK` | 67.30 | 单日 +2.99%；`volume_ratio_20=1.5564`；`range` + `volume-expansion` | `symbol_risk_veto`；pass_rate=0.000 over 4 |
| `financials-insurance` | `1299.HK` | 58.00 | 单日 +2.16%；`volume_ratio_20=1.2945`；接近 MA20/MA60 | 分数低于行动阈值；`symbol_risk_veto`；仍未明确站上 MA60 |

#### 解读

- 金融内部，`0388.HK` 的短线动量最显眼，量能也更强；`0005.HK` 趋势更稳但动量较弱；`1299.HK` 是修复观察而非趋势确认。
- 三者都不能升级：`0388.HK` 与 `0005.HK` 达到或接近行动分数但被 veto，`1299.HK` 分数不足且也被 veto。
- 若后续日期对齐数据确认金融继续放量，优先审计 `0388.HK` 是否从单日放量转为多日成交确认。

### 3.5 `hong-kong-broad-market`

#### 事实

| 标的 | 分数 | 关键事实 | 阻断因素 |
|---|---:|---|---|
| `2800.HK` | 56.60 | 单日 +1.74%；价格略高于 MA20 与 MA60；`volume_ratio_20=1.1216`；`range` | 分数低于行动阈值；`symbol_risk_veto`；pass_rate=0.074 over 94；近期 `hold` / `buy_candidate` 多次失误 |

#### 解读

- `2800.HK` 只能作为市场确认工具，不是本轮候选。
- 广义港股反弹需要更多宽度、量能与均线确认；当前不能用 `risk_on` 覆盖过往广义 ETF 多头失败。

### 3.6 `hang-seng-tech`

#### 事实

| 标的 | 分数 | 关键事实 | 阻断因素 |
|---|---:|---|---|
| `3067.HK` | 44.39 | 单日 +1.58%；价格高于 MA20；`volume_ratio_20=1.0774` | 低于观察门槛；MA60 未收复；`symbol_risk_veto` |
| `3033.HK` | 42.65 | 单日 +1.78%；价格高于 MA20 | 低于观察门槛；非主题 leader；MA60 未收复；`symbol_risk_veto` |

#### 解读

- 恒生科技 ETF 没有足够确认：分数低、仍在 MA60 下方或未修复到可靠上行结构。
- 尽管单日反弹与市场 `risk_on` 一致，但稳定规则要求在弱量、未收复 MA60、低通过率背景下保持 `watch_only`。

### 3.7 `internet-platform`

#### 事实

| 标的 | 分数 | 关键事实 | 阻断因素 |
|---|---:|---|---|
| `9618.HK` | 72.27 | 主题 leader；`uptrend`；价格高于 MA20/MA60；`range_pos_60=0.7952` | `symbol_risk_veto`；pass_rate=0.000 over 2；量能偏弱 `volume_ratio_20=0.7545` |
| `9988.HK` | 44.75 | 单日 +3.24%；价格高于 MA20 | 低于观察门槛；非主题 leader；MA60 未收复；`symbol_risk_veto`；近期多次 misfire |
| `3690.HK` | 44.67 | 单日 +3.55%；成交接近确认 `volume_ratio_20=1.0194` | 低于观察门槛；价格低于 MA20/MA60；非主题 leader |
| `0700.HK` | 0.00 | 单日 +1.14% | `downtrend`；价格低于 MA20/MA60；低区间位置；`symbol_risk_veto` |
| `1024.HK` | 0.00 | 单日 +2.93% | `downtrend`；价格低于 MA20/MA60；低区间位置；`symbol_risk_veto` |

#### 解读

- 主题内最佳当前表达是 `9618.HK`，但它并非可行动标的：它被 veto，且量能没有达到更强确认。
- `9988.HK` 与 `3690.HK` 单日领涨，但都没有通过排名与均线门槛。尤其 `9988.HK` 有近期选择错误和低 pass_rate，不能因日涨幅追入。
- 互联网平台需要先确认谁是“近期 best peer”，再看是否有超过 100bps 的新相对强度改善；本轮没有足够证据。

### 3.8 消费、科技硬件、医药

#### 事实

- `consumer-discretionary` 主题均值 27.02；最佳 `2020.HK` 分数 55.36，但 `qualified_for_watch=false`，且有低量能阻断 `low_volume_ratio_20_below_0_6` 与 `symbol_risk_veto`。
- `consumer-tech` 中 `1810.HK` 分数 0，`downtrend`，价格低于 MA20/MA60，`range_pos_60=0.0306`。
- `healthcare-biotech` 的 `2269.HK` 分数 0，`downtrend`，价格低于 MA20/MA60。
- `healthcare-pharma` 中 `1177.HK` 与 `1093.HK` 分数均为 0，均处 `downtrend`。

#### 解读

- 这些主题目前不是多头优先方向。
- 医药与小米等低位反弹风险存在，但没有趋势确认；不适合做 `avoid` 集群，也不适合做反弹买入。

## 4. ETF 确认

### 事实

| ETF | 主题 | 分数 | 单日涨幅 | MA 状态 | 量能 | 状态 |
|---|---|---:|---:|---|---:|---|
| `2800.HK` | `hong-kong-broad-market` | 56.60 | +1.74% | 价格略高于 MA20/MA60 | `volume_ratio_20=1.1216` | `diagnostic_only`，veto |
| `3033.HK` | `hang-seng-tech` | 42.65 | +1.78% | 高于 MA20，低于 MA60 | `volume_ratio_20=0.6564` | `diagnostic_only`，veto |
| `3067.HK` | `hang-seng-tech` | 44.39 | +1.58% | 高于 MA20，低于 MA60 | `volume_ratio_20=1.0774` | `diagnostic_only`，veto |

### 解读

- 宽基 ETF `2800.HK` 有一定修复，但历史失败率与近期 misfire 要求更严格确认。
- 科技 ETF 只显示从低位反弹，不显示可升级趋势；MA60 未收复是关键缺口。
- 由于 ETF 确认不足，不能把单个互联网或科技股反弹升级为行动候选。

## 5. 突出标的观察清单

> 以下不是推荐买入；全部为 `watch_only` / 审计观察。

### `0857.HK`：能源趋势最强，但被风险 veto

- 事实：分数 84.42，`uptrend`，价格高于 MA20/MA60，`volume_ratio_20=1.2356`，`range_pos_60=1.1084`。
- 解读：趋势与动量最强，但位置偏高，且历史表现低通过率、负平均收益、存在 adverse breach。不得升级。
- 观察触发：若后续进入 `actionable_candidates`，且 `symbol_risk_veto` 解除，同时同主题相对强度继续领先 `0883.HK` 与 `0386.HK`，再重新评估。
- 失效条件：跌回 MA20 下方，或相对 `0386.HK` / `0883.HK` 明显转弱，或量能低于确认门槛。

### `0941.HK`：电讯股息趋势强，但历史 pass_rate 阻断

- 事实：分数 81.98，`uptrend` + `volume-expansion`，价格高于 MA20/MA60，`volume_ratio_20=1.5041`。
- 解读：结构强，但 pass_rate=0.000 over 30 是硬阻断。不能因防御趋势强就忽略 posterior 风险。
- 观察触发：需要日期对齐后继续放量，并进入 `actionable_candidates`，且 risk veto 解除。
- 失效条件：跌破 MA20，或量能扩张消失，或 `0728.HK` 明显成为更强 peer。

### `0002.HK`：公用事业 leader，但样本与 veto 限制

- 事实：分数 76.08，`uptrend`，价格高于 MA20/MA60，`volume_ratio_20=1.2769`。
- 解读：防御主题 leader，但样本少且 pass_rate=0。只能观察，不能升级。
- 观察触发：保持 MA20/MA60 上方并进入 `actionable_candidates`，同时确认不是滞后防御轮动尾声。
- 失效条件：跌破 MA20，或 `0006.HK` 明显转强而 `0002.HK` 失去 leader 地位。

### `0388.HK`：金融交易所放量修复，短线值得审计

- 事实：单日 +2.99%，`volume_ratio_20=1.5564`，分数 67.30，价格高于 MA20/MA60，`range_pos_60=0.6766`。
- 解读：短线动量与量能较好，是金融里更值得观察的修复标的；但仍被 `symbol_risk_veto` 阻断。
- 观察触发：连续量能确认、维持 MA20/MA60 上方、解除 veto，并进入 `actionable_candidates`。
- 失效条件：放量后无 follow-through，或跌回 MA20 下方。

### `9618.HK`：互联网平台内部较强，但缺量且 veto

- 事实：分数 72.27，`uptrend`，价格高于 MA20/MA60，主题 leader；但 `volume_ratio_20=0.7545`，`symbol_risk_veto=true`。
- 解读：在互联网平台里相对强，但没有足够量能和风险通过；不能替代过去误选的 `0700.HK` / `9988.HK` 直接升级。
- 观察触发：需要新数据证明它持续优于近期 best peer，且进入 `actionable_candidates`。
- 失效条件：跌破 MA20，或同主题 best peer 转向 `9988.HK` / `3690.HK` 且领先幅度超过成本与边际要求。

## 6. 风险姿态

### 事实

- 投资档案为 balanced，单一持仓上限 10%，主题上限 30%，不允许杠杆、不允许反向 ETF、不允许低流动性。
- 交易成本假设为 round-trip 35bps，最低边际要求 100bps，且需明显超过交易成本。
- 本轮 `actionable_candidates=[]`。
- 多个高分诊断标的存在 `symbol_risk_veto`。
- posterior 总评中失败样本较多：`fail=211`，`pass=57`；近期 misfires 包括 `2800.HK`、`9988.HK`、科技 ETF 与互联网平台选择错误。

### 解读

- 今天风险姿态应为保守观察：不追强、不挖 lower-ranked 替代、不把 `risk_on` 当作交易许可。
- 重点风险是“强趋势但历史低通过率”的陷阱：`0857.HK`、`0941.HK`、`0002.HK` 都符合技术强势，但全部被风险层阻断。
- 第二个风险是“单日科技 / 互联网反弹误判”：`9988.HK`、`3690.HK` 领涨，但 ETF 与 MA60 确认不足。
- 第三个风险是日期错配：`as_of_date` 与行情日期不一致，任何行动信号都必须降级为审计材料。

## 7. 今日推荐状态

### 总体状态：`watch_only`

- 本轮无 `buy_candidate`。
- 本轮无 `accumulate`。
- 本轮无 `hold` 建议，因为没有真实持仓且推荐模式不假设用户持仓。
- 本轮无 `avoid` 集群，因为市场处 `risk_on`，且缺少日期对齐的下行确认；对弱势科技 / 医药只做观察。

### 观察队列

| 优先级 | 标的 | 主题 | 当前状态 | 观察目的 |
|---:|---|---|---|---|
| 1 | `0857.HK` | `energy` | `watch_only` | 审计强趋势 + veto 是否持续有效；比较 `0386.HK` 是否成为更干净 peer |
| 2 | `0941.HK` | `telecom-dividend` | `watch_only` | 审计防御高股息趋势是否有真实 follow-through |
| 3 | `0002.HK` | `utilities-defensive` | `watch_only` | 观察公用事业 leader 是否维持趋势且不拥挤回撤 |
| 4 | `0388.HK` | `financials-exchange` | `watch_only` | 观察放量修复是否延续 |
| 5 | `9618.HK` | `internet-platform` | `watch_only` | 观察互联网平台内部是否出现可验证 best peer |

## 8. 今天的高优先级研究问题

1. 日期对齐问题：能否取得真正 `2026-01-20` 的收盘价、MA20/MA60、成交量与 `range_pos_60`？若不能，本轮所有排名继续保持审计状态。
2. 能源主题中，`0386.HK` 虽然不是 leader 但无 `symbol_risk_veto`，后续是否能在日期对齐数据中持续跑赢 `0857.HK` 与 `0883.HK`，并独立进入 `actionable_candidates`？
3. 电讯与公用事业的高分是否只是防御拥挤交易？需要检查 `0941.HK`、`0002.HK`、`0006.HK` 在 T+3/T+5 的回撤与量能延续。
4. 金融内部是否由 `0388.HK` 领涨形成可持续风险偏好改善，还是单日放量后无 follow-through？
5. 互联网平台近期 best peer 到底是谁：`9618.HK`、`9988.HK`、`3690.HK` 之间是否存在连续超过 100bps 的相对强度改善，并且是否得到 `3033.HK` / `3067.HK` ETF 确认？
