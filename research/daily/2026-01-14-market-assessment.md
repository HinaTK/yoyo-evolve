# 2026-01-14 港股市场评估

> 角色：`yoyo-invest`  
> 模式：历史回放 / recommendation_only  
> 适用周期：14-90 天 swing 观察  
> 数据说明：本次输入的 `as_of_date` 为 `2026-01-14`，但快照内多个 `quote_trade_date` 为 `2026-04-29`。按稳定规则，日期不一致时，本报告只把信号作为诊断与条件观察，不做直接升级。

## 1. 市场雷达事实

### 1.1 市场状态

**事实：**

- `market_summary.risk_state` = `risk_on`。
- 雷达内股票平均 1 日涨幅：`avg_stock_move_1d` = 1.606%。
- 雷达内 ETF 平均 1 日涨幅：`avg_etf_move_1d` = 1.7%。
- 领涨个股：`3690.HK` +3.55%、`9988.HK` +3.24%、`0388.HK` +2.99%。
- 落后个股：`1093.HK` -0.59%、`0006.HK` -0.38%、`1177.HK` -0.36%。

**解读：**

市场短线呈现风险偏好回升，但并非全面趋势确认。上涨集中在互联网平台反弹、交易所/金融、能源、通信和防御股的局部强势中。由于数据日期存在冲突，当前只能确认“雷达层面出现风险偏好信号”，不能把它视为可执行买入信号。

## 2. 按板块 / 主题强弱排序

### 2.1 强势主题

**事实：**

| 主题 | 代表符号 | 主题均分 / 关键信号 | 雷达观察 |
|---|---:|---:|---|
| `utilities-defensive` | `0002.HK`, `0006.HK` | avg_score 75.47 | 两只均处于 `uptrend`，价格高于 ma20 / ma60，区间位置高 |
| `telecom-dividend` | `0941.HK`, `0728.HK` | avg_score 75.00 | `0941.HK` 为强趋势并放量，`0728.HK` 也放量 |
| `financials-bank` | `0005.HK` | score 71.01 | `0005.HK` 处于 `uptrend`，价格高于均线 |
| `energy` | `0857.HK`, `0883.HK`, `0386.HK` | avg_score 69.67 | `0857.HK` 与 `0883.HK` 强趋势，`0386.HK` 放量反弹但仍低于 ma60 |
| `financials-exchange` | `0388.HK` | score 67.30 | `0388.HK` +2.99%，`volume-expansion`，价格高于 ma20 / ma60 |

**解读：**

强势主题主要偏向高股息、防御、能源和金融交易活跃度，而不是成长科技主线。风险偏好虽然回升，但资金更愿意拥抱已确认趋势或高现金流属性的品种。

### 2.2 中性 / 观察主题

**事实：**

| 主题 | 代表符号 | 主题均分 / 关键信号 | 雷达观察 |
|---|---:|---:|---|
| `financials-insurance` | `1299.HK` | score 58.00 | 接近 ma20 / ma60，放量，区间位置中位 |
| `hong-kong-broad-market` | `2800.HK` | score 56.60 | +1.74%，价格略高于 ma20 / ma60，成交确认 |
| `consumer-discretionary` | `2020.HK`, `9992.HK`, `2331.HK`, `6862.HK` | avg_score 27.02 | 只有 `2020.HK` 结构相对较好，其余多为反弹或弱势 |
| `hang-seng-tech` | `3033.HK`, `3067.HK` | avg_score 43.52 | 两只 ETF 均低于 watch 分数线，仍未收复 ma60 |

**解读：**

`2800.HK` 能确认大盘短线修复，但分数不足以进入行动层。恒生科技 ETF 虽上涨，但仍属于低位反弹，尚未给出足够 ETF 确认。消费可选内部差异大，暂不构成清晰主题机会。

### 2.3 弱势主题

**事实：**

| 主题 | 代表符号 | 雷达观察 |
|---|---:|---|
| `internet-platform` | `0700.HK`, `9988.HK`, `3690.HK`, `1024.HK`, `9618.HK` | 主题均分 32.34，只有 `9618.HK` 为主题 leader 且处于 `uptrend`；`0700.HK`、`1024.HK` 仍是 `downtrend` |
| `consumer-tech` | `1810.HK` | `downtrend`，低于 ma20 / ma60，range_pos_60 仅 0.0306 |
| `healthcare-biotech` | `2269.HK` | `downtrend`，低于 ma20 / ma60 |
| `healthcare-pharma` | `1177.HK`, `1093.HK` | 两者均为 `downtrend`，且当日为负收益 |

**解读：**

互联网平台出现单日反弹，但内部结构不一致。`9988.HK` 与 `3690.HK` 当日涨幅强，不过确定性不足；`9618.HK` 是当前互联网主题内结构最好的表达，但风险层阻止升级。医药与小米仍是弱势，不适合把反弹当成趋势反转。

## 3. ETF 确认

**事实：**

- `2800.HK`：收 26.24，+1.74%，ma20 25.8446，ma60 26.1507，`range`，score 56.60，`qualified_for_action=false`。
- `3033.HK`：收 4.81，+1.78%，ma20 4.7717，ma60 4.9835，score 42.65，低于 watch 分数线。
- `3067.HK`：收 10.31，+1.58%，ma20 10.2455，ma60 10.6875，score 44.39，低于 watch 分数线。
- `actionable_candidates` 为空。

**解读：**

ETF 层面支持“市场有反弹”，但不支持“可以升级”。`2800.HK` 略高于 ma60，但历史低 pass_rate 与近期 broad-index ETF bullish failures 要求更严格的 breadth、volume、均线确认。`3033.HK` / `3067.HK` 仍未收复 ma60，且分数低于 watch 门槛，不能作为科技单名升级依据。

## 4. 交易宇宙内的主题可行动性

### 4.1 关键约束

**事实：**

- `actionable_candidates` = []。
- top `diagnostic_candidates` 为 `0857.HK`、`0941.HK`、`0002.HK`。
- 三者均有 `symbol_risk_veto`，且 `qualified_for_action=false`。
- 稳定规则要求：`actionable_candidates` 为空时，不升级 `diagnostic_candidates`；诊断候选只用于观察和解释。

**解读：**

今天没有 deterministic layer 可升级候选。所有主题表达只能是 `watch_only` 或条件观察，不应从低排名或非 veto peer 中“挖”替代品。

### 4.2 强势主题在交易宇宙中的最佳表达

#### `energy`

**事实：**

| 符号 | 分数 | 状态 | 关键证据 | 风险层 |
|---|---:|---|---|---|
| `0857.HK` | 84.42 | 主题 leader | uptrend，价格高于 ma20 / ma60，volume_ratio_20 1.2356 | `symbol_risk_veto=true`，pass_rate 0.152，avg_return -4.514% |
| `0883.HK` | 73.93 | 同主题第二 | uptrend，价格高于 ma20 / ma60 | 非主题 leader，`symbol_risk_veto=true` |
| `0386.HK` | 50.67 | 同主题第三 | volume_ratio_20 2.2023，放量 | 非主题 leader，低于 ma60，未进入行动名单 |

**解读：**

`energy` 是雷达强主题，但交易宇宙内没有可行动表达。`0857.HK` 是结构最强表达，但被风险 veto；`0386.HK` 虽无 veto 且放量，但不是 theme leader、低于 ma60、也不在 `actionable_candidates`。因此能源主题只做 peer-relative 审核，不做替代升级。

#### `telecom-dividend`

**事实：**

| 符号 | 分数 | 状态 | 关键证据 | 风险层 |
|---|---:|---|---|---|
| `0941.HK` | 81.98 | 主题 leader | uptrend + `volume-expansion`，range_pos_60 1.1119 | `symbol_risk_veto=true`，pass_rate 0.033 |
| `0728.HK` | 68.01 | 同主题第二 | 放量，价格高于 ma20 / ma60 | 非主题 leader，`symbol_risk_veto=true` |

**解读：**

通信高股息是很强的雷达主题，但 `0941.HK` 与 `0728.HK` 均被风险层阻断。当前最佳表达是 `0941.HK`，但只能观察其是否继续放量并守住 ma20；不能升级。

#### `utilities-defensive`

**事实：**

| 符号 | 分数 | 状态 | 关键证据 | 风险层 |
|---|---:|---|---|---|
| `0002.HK` | 76.08 | 主题 leader | uptrend，价格高于 ma20 / ma60，volume_ratio_20 1.2769 | `symbol_risk_veto=true`，pass_rate 0.000 |
| `0006.HK` | 74.86 | 同主题第二 | uptrend，价格高于 ma20 / ma60，volume_ratio_20 1.3544 | 非主题 leader，`symbol_risk_veto=true` |

**解读：**

防御公用事业是排序最高的主题，但两个可交易代表均被风险层否决。`0002.HK` 是最佳表达，但只适合作为防御资金偏好的温度计。

#### `financials-bank` / `financials-exchange` / `financials-insurance`

**事实：**

| 主题 | 最佳表达 | 分数 | 状态 | 风险层 |
|---|---:|---:|---|---|
| `financials-bank` | `0005.HK` | 71.01 | uptrend，价格高于 ma20 / ma60 | `symbol_risk_veto=true` |
| `financials-exchange` | `0388.HK` | 67.30 | +2.99%，`volume-expansion`，价格高于 ma20 / ma60 | `symbol_risk_veto=true` |
| `financials-insurance` | `1299.HK` | 58.00 | 放量，接近 ma20 / ma60 | `symbol_risk_veto=true` |

**解读：**

金融链条里，`0388.HK` 的当日动量最突出，`0005.HK` 的趋势更稳，`1299.HK` 仍偏中性。但三者均不能升级。`0388.HK` 值得重点跟踪是否有连续放量和成交活跃度扩散。

#### `internet-platform`

**事实：**

| 符号 | 分数 | 状态 | 关键证据 | 风险层 |
|---|---:|---|---|---|
| `9618.HK` | 72.27 | 主题 leader | uptrend，价格高于 ma20 / ma60 | `symbol_risk_veto=true`，pass_rate 0.000 |
| `9988.HK` | 44.75 | 同主题第二 | +3.24%，价格高于 ma20 但低于 ma60 | 低于 watch 分数，`symbol_risk_veto=true` |
| `3690.HK` | 44.67 | 同主题第三 | +3.55%，volume_ratio_20 1.0194 | 低于 watch 分数，价格低于 ma20 / ma60 |
| `0700.HK` | 0 | 同主题第四 | `downtrend`，低于 ma20 / ma60 | `symbol_risk_veto=true` |
| `1024.HK` | 0 | 同主题第五 | `downtrend`，低于 ma20 / ma60 | `symbol_risk_veto=true` |

**解读：**

互联网平台是“单日强、结构弱”的典型反弹。`9618.HK` 是当前最佳表达，但被风险 veto；`9988.HK` 与 `3690.HK` 的反弹尚未修复 ma60 或 action gate。结合近期 selected-vs-best 错误，今天不能从 `0700.HK` / `9988.HK` 的反弹中升级买点。

#### `hong-kong-broad-market` 与 `hang-seng-tech`

**事实：**

| 主题 | 最佳表达 | 分数 | 关键证据 | 行动状态 |
|---|---:|---:|---|---|
| `hong-kong-broad-market` | `2800.HK` | 56.60 | +1.74%，略高于 ma20 / ma60 | watch-only 诊断 |
| `hang-seng-tech` | `3067.HK` | 44.39 | +1.58%，高于 ma20、低于 ma60 | 低于 watch 分数 |
| `hang-seng-tech` | `3033.HK` | 42.65 | +1.78%，高于 ma20、低于 ma60 | 低于 watch 分数 |

**解读：**

大盘 ETF 只支持“修复观察”，科技 ETF 不支持单名科技升级。若要后续考虑科技方向，第一条件是 `3033.HK` / `3067.HK` 收复 ma60 并伴随更稳定成交确认。

## 5. 外部机会与交易宇宙覆盖

**事实：**

本次市场雷达中的主要强主题均已在 trade universe 中有代表：`utilities-defensive`、`telecom-dividend`、`energy`、`financials-bank`、`financials-exchange`、`financials-insurance`、`hong-kong-broad-market`、`hang-seng-tech`、`internet-platform`、`consumer-discretionary`、`healthcare-biotech`、`healthcare-pharma`。

**解读：**

今天没有出现“雷达强但交易宇宙未覆盖”的明确外部主题。后续扩展交易宇宙的重点不是新增主题，而是为强主题寻找更干净、低 veto、流动性合格、且能战胜当前 leader 的替代表达。

## 6. 今日突出个股

### 6.1 只作观察的强势标的

- `0857.HK`：分数最高，趋势与成交均合格，但 `symbol_risk_veto` 阻止行动。
- `0941.HK`：强趋势 + 放量，但历史 pass_rate 极低，不能升级。
- `0002.HK`：防御主题 leader，但 posterior 风险记录差。
- `0388.HK`：当日涨幅与放量突出，是金融风险偏好观察窗口。
- `9618.HK`：互联网平台里结构最佳，但风险 veto 与历史选择错误要求谨慎。

### 6.2 明确不应升级的反弹标的

- `0700.HK`：仍为 `downtrend`，低于 ma20 / ma60，score 0。
- `1810.HK`：仍为 `downtrend`，range_pos_60 极低。
- `3033.HK` / `3067.HK`：仍低于 ma60，且未达到 watch 分数。
- `2269.HK`、`1177.HK`、`1093.HK`：医药方向仍弱，不能把低位反弹或小跌当作底部确认。

## 7. 风险姿态与建议状态

**事实：**

- 组合为 recommendation_only，未提供真实持仓。
- 风险偏好为 balanced。
- 单一持仓上限 10%，主题上限 30%，不允许杠杆、不允许反向 ETF、不允许低流动性。
- 成本门槛：往返成本 35 bps，最低 edge 100 bps，且需要明显超过成本。
- `actionable_candidates` 为空。

**解读：**

今日风险姿态应为：**风险偏好观察，但行动保守**。市场短线风险偏好回升，但 deterministic action layer 没有候选，加上数据日期不一致、顶部诊断候选全被 veto，所有方向维持 `watch_only`。不建议为了参与反弹而降低 cost gate 或 risk veto。

## 8. 今日候选结论

| 符号 / 主题 | 状态 | 理由 | 触发条件 | 失效条件 | 信心 |
|---|---|---|---|---|---|
| `0857.HK` / `energy` | `watch_only` | 主题最强表达，但 `symbol_risk_veto` 且不在 `actionable_candidates` | 后续进入 `actionable_candidates`，并保持高于 ma20 / ma60、成交确认、风险 veto 解除 | 跌回 ma20 下方或能源主题失去相对强度 | 低 |
| `0941.HK` / `telecom-dividend` | `watch_only` | 趋势与成交强，但 pass_rate 低且 veto | 连续放量站稳高位，并进入行动名单 | 跌破 ma20 或主题内相对强度转弱 | 低 |
| `0002.HK` / `utilities-defensive` | `watch_only` | 防御主题强，但历史样本 pass_rate 0 | 后续行动层确认且风险记录改善 | 跌破 ma20 或 defensive rotation 失效 | 低 |
| `0388.HK` / `financials-exchange` | `watch_only` | 放量强，但 veto 且只是诊断候选 | 连续放量并进入 `actionable_candidates` | 放量失败、跌回 ma20 / ma60 下方 | 低 |
| `2800.HK` / broad market | `watch_only` | ETF 修复但近期 broad-index bullish failures 未修复 | breadth、volume、ma20 / ma60 同步改善并进入行动层 | 跌回 ma60 下方或成交萎缩 | 低 |

## 9. 今日高优先级研究问题

1. `0857.HK` 的强势是否只是能源主题内的拥挤动量，还是有 `0883.HK` / `0386.HK` 的持续 peer confirmation？
2. `0941.HK` 与 `0728.HK` 的放量能否延续，还是高股息主题已接近短线拥挤区？
3. `0388.HK` 的放量上涨是否能带动 `0005.HK`、`1299.HK` 等金融链条扩散，还是单日交易所弹性？
4. `3033.HK` / `3067.HK` 能否重新收复 ma60，并用成交确认科技 ETF 的趋势修复？
5. 在互联网平台内，`9618.HK` 是否能持续跑赢 `9988.HK`、`3690.HK`、`0700.HK`，从而修复近期 selected-vs-best 错误？
