# 2026-01-13 港股市场评估

> 身份：`yoyo-invest`  
> 模式：historical replay / recommendation_only  
> 交易窗口：14-90 天 swing  
> 约束：不使用杠杆、不使用反向 ETF、单一标的不超过 10%、主题敞口不超过 30%  
> 结论先行：本轮只做 `watch_only` 与条件观察，不给出 `buy_candidate`、`accumulate` 或 `hold` 升级。

## 0. 数据完整性与使用边界

### 事实

- 本次输入的 `as_of_date` 为 `2026-01-13`。
- 快照内多数行情字段的 `quote_trade_date` 为 `2026-04-29`，与 `as_of_date` 不一致。
- 确定性排名的 `actionable_candidates` 为空。
- 排名前三的 `diagnostic_candidates` 为：
  - `0857.HK`，score `84.42`，但有 `symbol_risk_veto`。
  - `0941.HK`，score `81.98`，但有 `symbol_risk_veto`。
  - `0002.HK`，score `76.08`，但有 `symbol_risk_veto`。
- 稳定规则明确：`actionable_candidates=[]` 时，不得把 `diagnostic_candidates` 升级为行动建议；若 replay 日期与 quote 日期不一致，只能视为低置信条件观察或 `watch_only`。

### 解读

- 今天的报告应当作为“市场雷达与候选审计”，不是实盘入场清单。
- 即使部分主题和个股分数较高，也只能用于定义后续观察条件；不能从诊断层下探挖掘替代标的作为行动建议。
- 本轮核心风险不是“没有强主题”，而是“强主题的确定性行动层未通过”。

## 1. 市场雷达：先按板块/主题强弱排序

### 事实：整体状态

- `market_summary.risk_state` 为 `risk_on`。
- 雷达内股票平均单日涨幅为 `1.606%`。
- 雷达内 ETF 平均单日涨幅为 `1.7%`。
- 当日雷达领涨：
  - `3690.HK` 美团：`+3.55%`
  - `9988.HK` 阿里巴巴-W：`+3.24%`
  - `0388.HK` 香港交易所：`+2.99%`，并带有 `volume-expansion`
- 当日雷达落后：
  - `1093.HK` 石药集团：`-0.59%`
  - `0006.HK` 电能实业：`-0.38%`
  - `1177.HK` 中国生物制药：`-0.36%`

### 事实：主题强弱，按确定性排名的 `theme_summary`

| 排名 | theme | avg_score | leader | leader_score | 观察 |
|---:|---|---:|---|---:|---|
| 1 | `utilities-defensive` | 75.47 | `0002.HK` | 76.08 | 防御公用事业分数最高 |
| 2 | `telecom-dividend` | 75.00 | `0941.HK` | 81.98 | 电信红利强，且量能扩张 |
| 3 | `financials-bank` | 71.01 | `0005.HK` | 71.01 | 银行维持上行结构 |
| 4 | `energy` | 69.67 | `0857.HK` | 84.42 | 能源内部最强，但风险 veto 明显 |
| 5 | `financials-exchange` | 67.30 | `0388.HK` | 67.30 | 港交所单日强且放量 |
| 6 | `financials-insurance` | 58.00 | `1299.HK` | 58.00 | 中等偏观察 |
| 7 | `hong-kong-broad-market` | 56.60 | `2800.HK` | 56.60 | 大盘 ETF 反弹但未到行动层 |
| 8 | `hang-seng-tech` | 43.52 | `3067.HK` | 44.39 | 科技 ETF 未达到 watch 门槛 |
| 9 | `internet-platform` | 32.34 | `9618.HK` | 72.27 | 主题平均弱，但内部有个别强标的 |
| 10 | `consumer-discretionary` | 27.02 | `2020.HK` | 55.36 | 分化，整体不强 |
| 11 | `consumer-tech` | 0.00 | `1810.HK` | 0.00 | 下行结构 |
| 12 | `healthcare-biotech` | 0.00 | `2269.HK` | 0.00 | 下行结构 |
| 13 | `healthcare-pharma` | 0.00 | `1177.HK` | 0.00 | 下行结构 |

### 解读：主题层级

- 第一梯队是防御/红利/资源与金融类：`utilities-defensive`、`telecom-dividend`、`energy`、`financials-bank`、`financials-exchange`。
- 第二梯队是宽基港股与保险：`2800.HK`、`1299.HK` 有反弹和中等分数，但不满足行动门槛。
- 科技和互联网平台表现分裂：单日领涨来自 `3690.HK`、`9988.HK`，但主题平均分低，且恒生科技 ETF 未确认。
- 医药、消费科技和部分可选消费仍是弱势观察区，不适合逆势升级。

## 2. 市场制度与风险姿态

### 事实

- 风险状态为 `risk_on`。
- 多数主要板块单日上涨，且 ETF 平均涨幅为正。
- 但确定性排名没有任何 `actionable_candidates`。
- 多个高分标的被 `symbol_risk_veto` 阻断。
- 参数优化摘要未更新 active strategy，原因包括样本、改善、胜率、风险等门槛未同时满足。

### 解读

- 这是“风险偏好回暖但研究系统不允许升级”的环境。
- 策略上应避免被单日上涨吸引，尤其不能把 `risk_on` 直接等同于可买。
- 当前最合适的姿态是：观察强主题是否能获得日期一致的价格、成交量和均线确认；在确认前维持 `watch_only`。

## 3. ETF 确认

### 事实

| ETF | theme | close | 1d | ma20 | ma60 | range_pos_60 | volume_ratio_20 | score | 状态 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `2800.HK` | `hong-kong-broad-market` | 26.24 | +1.74% | 25.8446 | 26.1507 | 0.4981 | 1.1216 | 56.60 | `watch_only` |
| `3033.HK` | `hang-seng-tech` | 4.81 | +1.78% | 4.7717 | 4.9835 | 0.2131 | 0.6564 | 42.65 | below watch |
| `3067.HK` | `hang-seng-tech` | 10.31 | +1.58% | 10.2455 | 10.6875 | 0.2039 | 1.0774 | 44.39 | below watch |

### 解读

- `2800.HK` 提供了宽基市场反弹确认：价格高于 ma20 和 ma60，量能超过 20 日均量，分数达到 watch 门槛，但未达到 action 门槛，且有低 pass_rate 与近期误判记录。
- `3033.HK` 和 `3067.HK` 均低于 ma60，且分数低于 watch 门槛；它们不能确认科技成长主题进入可行动阶段。
- 按规则，互联网平台单股若要升级，需要 ETF 或宽基确认。今天宽基有一定确认，但科技 ETF 不够，且 `actionable_candidates=[]`，因此科技/互联网不能升级。

## 4. 雷达强主题在交易 universe 内的可行动性

> 说明：雷达中的强主题均已在 trade universe 中有对应标的；本轮没有“雷达强但 trade universe 未覆盖”的外部机会。若后续出现未覆盖强主题，应先标记为“以后可考虑加入 universe 的外部机会”，不能作为当日即时建议。

### 4.1 `utilities-defensive`

#### 事实

- 可选标的：`0002.HK`、`0006.HK`。
- `0002.HK`：score `76.08`，主题 leader，`uptrend`，价格高于 ma20/ma60，`volume_ratio_20=1.2769`，但 `symbol_risk_veto=true`，`qualified_for_action=false`。
- `0006.HK`：score `74.86`，同主题非 leader，`uptrend`，但 `not_theme_score_leader` 且 `symbol_risk_veto=true`，`qualified_for_watch=false`。

#### 解读

- 当前主题最佳表达是 `0002.HK`，但只能作为诊断观察，不可升级。
- `0006.HK` 不应作为替代，因为它不是主题 leader，且同样存在 veto。
- 行动条件：需要日期一致的行情确认、`0002.HK` 的风险 veto 解除或后续评估改善，并且出现在 `actionable_candidates`。

### 4.2 `telecom-dividend`

#### 事实

- 可选标的：`0941.HK`、`0728.HK`。
- `0941.HK`：score `81.98`，主题 leader，`uptrend` + `volume-expansion`，价格高于 ma20/ma60，`volume_ratio_20=1.5041`，但 `symbol_risk_veto=true`。
- `0728.HK`：score `68.01`，同主题非 leader，`range` + `volume-expansion`，但 `not_theme_score_leader` 且 `symbol_risk_veto=true`。

#### 解读

- 主题层面很强，最佳表达是 `0941.HK`。
- 但 `0941.HK` 过去样本 pass_rate 极低，系统 veto 明确阻断升级。
- `0728.HK` 不能因 `0941.HK` 被 veto 而自动替代；它需要独立趋势、量能、相对强度和风险门槛全部通过，并进入 `actionable_candidates`。

### 4.3 `energy`

#### 事实

- 可选标的：`0857.HK`、`0883.HK`、`0386.HK`。
- `0857.HK`：score `84.42`，全市场排名第一，主题 leader，`uptrend`，价格高于 ma20/ma60，`volume_ratio_20=1.2356`，但 `symbol_risk_veto=true`。
- `0883.HK`：score `73.93`，同主题非 leader，`uptrend`，但 `not_theme_score_leader` 与 `symbol_risk_veto=true`。
- `0386.HK`：score `50.67`，`volume-expansion`，`symbol_risk_veto=false`，但主题 rank 第三，`not_theme_score_leader`，且低于 action 分数。

#### 解读

- 主题最佳表达是 `0857.HK`，但 veto 阻断。
- `0386.HK` 虽然没有 veto、放量明显，但它不是主题最强表达，趋势分数较低，且没有进入 `actionable_candidates`；不能作为替代行动标的。
- 能源主题今天应列为“高优先级审计主题”，不是买入主题。

### 4.4 `financials-bank`

#### 事实

- 可选标的：`0005.HK`。
- `0005.HK`：score `71.01`，`uptrend`，价格高于 ma20/ma60，但 `volume_ratio_20=0.7907`，且 `symbol_risk_veto=true`。

#### 解读

- `0005.HK` 是该主题唯一表达，也是最佳表达。
- 结构偏强但量能不足以强化入场，且风险 veto 明确。
- 维持 `watch_only`，等待量能和风险记录改善。

### 4.5 `financials-exchange`

#### 事实

- 可选标的：`0388.HK`。
- `0388.HK`：score `67.30`，`range` + `volume-expansion`，价格高于 ma20/ma60，`pct_change_1d=2.99%`，`volume_ratio_20=1.5564`，但 `symbol_risk_veto=true`。

#### 解读

- `0388.HK` 是金融交易所主题的最佳表达，也是当日最值得观察的金融弹性标的。
- 它的放量突破倾向比银行和保险更清晰，但系统 veto 仍然阻断行动升级。
- 后续应重点确认是否能连续站稳 ma20/ma60 上方并改善历史表现记录。

### 4.6 `financials-insurance`

#### 事实

- 可选标的：`1299.HK`。
- `1299.HK`：score `58.00`，价格接近 ma20/ma60，`volume_ratio_20=1.2945`，但低于 action score，且 `symbol_risk_veto=true`。

#### 解读

- `1299.HK` 只能作为中等优先级观察，当前不是主线。
- 若金融风险偏好继续改善，它可作为“金融扩散确认”观察，而不是今日入场候选。

### 4.7 `hong-kong-broad-market`

#### 事实

- 可选标的：`2800.HK`。
- `2800.HK`：score `56.60`，价格高于 ma20/ma60，`volume_ratio_20=1.1216`，`range`，但低于 action score，且 `symbol_risk_veto=true`。
- posterior summary 显示 `2800.HK` 样本多但 pass_rate 低，并有近期 bullish misfire。

#### 解读

- `2800.HK` 有宽基反弹观察价值，但不能升级为 `hold` 或 `buy_candidate`。
- 由于近期宽基 ETF 看多误判较多，必须等待 breadth、成交量和均线确认同步改善。

### 4.8 `hang-seng-tech`

#### 事实

- 可选标的：`3033.HK`、`3067.HK`。
- `3067.HK`：score `44.39`，主题 leader，但低于 watch score，低于 ma60，且 `symbol_risk_veto=true`。
- `3033.HK`：score `42.65`，同主题非 leader，低于 watch score，低于 ma60，且 `symbol_risk_veto=true`。

#### 解读

- 恒生科技 ETF 目前没有提供足够确认。
- 即使互联网平台个股出现反弹，也不能在 ETF 确认不足时升级科技敞口。
- 该主题维持低置信 `watch_only`。

### 4.9 `internet-platform`

#### 事实

- 可选标的：`0700.HK`、`9988.HK`、`3690.HK`、`1024.HK`、`9618.HK`。
- `9618.HK`：score `72.27`，主题 leader，`uptrend`，价格高于 ma20/ma60，但 `volume_ratio_20=0.7545`，且 `symbol_risk_veto=true`。
- `9988.HK`：score `44.75`，当日 `+3.24%`，高于 ma20 但低于 ma60，低于 watch score，且 `symbol_risk_veto=true`。
- `3690.HK`：score `44.67`，当日 `+3.55%`，但价格低于 ma20/ma60，低于 watch score。
- `0700.HK`：score `0`，`downtrend`，低位区间，价格低于 ma20/ma60，`symbol_risk_veto=true`。
- `1024.HK`：score `0`，`downtrend`，价格低于 ma20/ma60，`symbol_risk_veto=true`。
- posterior selection errors 显示互联网平台存在多次 selected-vs-best miss，近期 best peer 曾在 `9618.HK`、`9988.HK`、`3690.HK`、`1024.HK` 之间切换。

#### 解读

- 当前主题最佳量化表达是 `9618.HK`，但不能升级，因为它被 veto，且成交量确认偏弱。
- `3690.HK` 和 `9988.HK` 的单日强势更像反弹雷达信号，不是完整 swing 入场信号。
- 在科技 ETF 未确认、互联网平台选股历史误差较多的条件下，整个主题维持 `watch_only`。

### 4.10 `consumer-discretionary`

#### 事实

- 可选标的：`2020.HK`、`2331.HK`、`9992.HK`、`6862.HK`。
- `2020.HK`：score `55.36`，主题 leader，`uptrend`，但 `volume_ratio_20=0.5795` 低于流动/量能门槛，且 `symbol_risk_veto=true`。
- `2331.HK`：score `33.54`，价格低于 ma20/ma60。
- `9992.HK`：score `19.18`，价格高于 ma20 但低于 ma60，range_pos_60 偏低。
- `6862.HK`：score `0`，`downtrend`。

#### 解读

- 主题最佳表达是 `2020.HK`，但量能不足且 veto 阻断。
- 该主题分化大，不适合今日作为优先方向。

### 4.11 `consumer-tech`

#### 事实

- 可选标的：`1810.HK`。
- `1810.HK`：score `0`，`downtrend`，价格低于 ma20/ma60，range_pos_60 `0.0306`，`symbol_risk_veto=true`。

#### 解读

- `1810.HK` 当前不是可行动标的。
- 由于历史上对该低 pass-rate 标的有多次误判，本轮只能观察，不做反弹预判。

### 4.12 `healthcare-biotech` 与 `healthcare-pharma`

#### 事实

- `2269.HK`：score `0`，`downtrend`，低于 ma20/ma60。
- `1177.HK`：score `0`，`downtrend`，低于 ma20/ma60，`symbol_risk_veto=true`。
- `1093.HK`：score `0`，`downtrend`，低于 ma20/ma60，`symbol_risk_veto=true`。

#### 解读

- 医药相关主题是当前雷达中的明确弱势区。
- 不做 `avoid`，因为规则要求对反弹风险进行宽基/ETF检查；当前报告目的不是做空或规避建议，而是候选生成。
- 维持低优先级观察。

## 5. 今日突出标的与处理方式

### 只用于观察的高优先级清单

| 标的 | 主题 | 为什么突出 | 为什么不能升级 | 今日状态 |
|---|---|---|---|---|
| `0857.HK` | `energy` | score 最高，趋势和动量强 | `symbol_risk_veto`，且 `actionable_candidates=[]` | `watch_only` |
| `0941.HK` | `telecom-dividend` | 上行趋势 + 放量，主题强 | `symbol_risk_veto`，历史 pass_rate 极低 | `watch_only` |
| `0002.HK` | `utilities-defensive` | 防御主题 leader，结构稳定 | `symbol_risk_veto` | `watch_only` |
| `0388.HK` | `financials-exchange` | 单日放量强，金融弹性突出 | `symbol_risk_veto` | `watch_only` |
| `2800.HK` | `hong-kong-broad-market` | 宽基 ETF 有反弹确认 | 低 pass_rate，近期误判，低于 action score | `watch_only` |

### 不应被单日涨幅误导的标的

- `3690.HK`：当日领涨，但价格仍低于 ma20/ma60，且低于 watch score。
- `9988.HK`：当日强，但低于 ma60，且近期 misfire 和 selection error 较多。
- `3033.HK`、`3067.HK`：科技 ETF 反弹但低于 ma60，分数未达 watch 门槛。
- `0700.HK`、`1810.HK`、`1024.HK`：仍处于 `downtrend` 或低位结构，不能因反弹预期升级。

## 6. 推荐状态与失效条件

### 总体推荐状态

- 市场：`watch_only`
- 主题：`watch_only`
- 个股/ETF：全部 `watch_only`

### 统一行动门槛

任何标的要从 `watch_only` 升级，至少需要同时满足：

1. 出现在 `actionable_candidates`，而不是仅出现在 `diagnostic_candidates`。
2. replay 的 `as_of_date` 与 quote 日期一致，或有独立日期对齐证据。
3. 若主题 leader 被 `symbol_risk_veto`，不能机械替代为同主题 peer；替代标的必须独立通过趋势、量能、相对强度和风险门槛。
4. 若是科技/互联网主题，需要 `3033.HK` 或 `3067.HK` 重新站上 ma60 并改善 watch/action 分数。
5. 对低 pass_rate 标的，需要宽基和 ETF 同步确认，且近期 selection error 改善。

### 失效条件

- 若 `2800.HK` 跌回 ma20/ma60 下方，宽基反弹假设失效。
- 若 `3033.HK`、`3067.HK` 继续低于 ma60，科技/互联网单股反弹不视为可交易主题确认。
- 若高分防御/红利/能源 leader 的 `symbol_risk_veto` 未解除，则不得升级这些主题的 leader。
- 若后续仍出现 `actionable_candidates=[]`，则继续禁止从诊断层挖掘替代行动标的。

## 7. 风险提示

- 数据日期错配风险：`as_of_date` 与 quote 日期不一致，降低所有结论的可交易性。
- 后验污染风险：posterior evaluation 只能用于降低信心和识别错误模式，不能作为当前行情确认。
- 主题替代风险：leader 被 veto 后，选择同主题低排名 peer 容易重复 selection error。
- 反弹追高风险：`risk_on` 日内上涨可能只是短期修复，特别是科技 ETF 未收复 ma60 的情况下。
- 成本门槛风险：估计往返成本为 35 bps，且最低 edge 要求为 100 bps；当前没有足够证据证明预期 swing edge 明显超过成本门槛。

## 8. 今天最高优先级研究问题

1. 日期对齐后，`0857.HK`、`0941.HK`、`0002.HK` 的高分结构是否仍然存在，还是由 2026-04-29 quote 造成 replay 偏差？
2. `2800.HK` 的宽基确认是否能持续：成交量、ma20/ma60、市场宽度是否同时改善？
3. `3033.HK` 与 `3067.HK` 是否能重新站上 ma60；若不能，互联网平台单股反弹是否应继续全部限制为 `watch_only`？
4. 在 `internet-platform` 内，近期 best peer 到底是 `9618.HK`、`9988.HK`、`3690.HK` 还是 `1024.HK`；是否有新的 peer-relative improvement 能降低 selection error？
5. 对 `symbol_risk_veto` 集中的高分主题，是否需要建立“veto 审计表”，区分真实不可碰标的与因历史样本过旧/日期错配导致的临时阻断？
