# 2026-01-23 港股市场评估

> 会话：historical  
> 角色：yoyo-invest  
> 输出性质：历史回放研究记录；recommendation_only；非真实持仓管理。  
> 关键约束：`actionable_candidates=[]`，且行情字段出现 `as_of_date=2026-01-23` 与 `quote_trade_date=2026-04-29` 不一致，因此本报告只作条件审计与观察，不作直接升级。

## 1. 市场雷达事实

### 1.1 市场状态

**事实**

- `market_summary.risk_state` 为 `risk_on`。
- 雷达内股票平均单日涨幅 `avg_stock_move_1d=1.606%`。
- ETF 平均单日涨幅 `avg_etf_move_1d=1.7%`。
- 领涨个股：
  - `3690.HK`：+3.55%，theme=`internet-platform`，`regime_flags=["range"]`。
  - `9988.HK`：+3.24%，theme=`internet-platform`，`regime_flags=["range"]`。
  - `0388.HK`：+2.99%，theme=`financials-exchange`，`regime_flags=["range", "volume-expansion"]`。
- 落后个股：
  - `1093.HK`：-0.59%，theme=`healthcare-pharma`，`regime_flags=["downtrend"]`。
  - `0006.HK`：-0.38%，theme=`utilities-defensive`，但仍为 `uptrend`。
  - `1177.HK`：-0.36%，theme=`healthcare-pharma`，`regime_flags=["downtrend"]`。

**解释**

- 表面上是偏 `risk_on` 的普涨日，指数 ETF 与多数主题均为正收益。
- 但历史回放输入存在日期不对齐：`as_of_date=2026-01-23`，而行情字段显示 `quote_trade_date=2026-04-29`。根据稳定规则，`risk_on` 不能覆盖非日期对齐、`actionable_candidates=[]` 或 `symbol_risk_veto`。因此本日只能定性为“风险偏好改善的审计样本”，不能定性为可执行买入日。

## 2. 雷达主题强弱排序

### 2.1 强势主题

**事实**

按 deterministic ranking 的 `theme_summary`：

| 排名 | theme | avg_score | leader | leader_score | leader_qualified |
|---:|---|---:|---|---:|---|
| 1 | `utilities-defensive` | 75.47 | `0002.HK` | 76.08 | true |
| 2 | `telecom-dividend` | 75.00 | `0941.HK` | 81.98 | true |
| 3 | `financials-bank` | 71.01 | `0005.HK` | 71.01 | true |
| 4 | `energy` | 69.67 | `0857.HK` | 84.42 | true |
| 5 | `financials-exchange` | 67.30 | `0388.HK` | 67.30 | true |
| 6 | `financials-insurance` | 58.00 | `1299.HK` | 58.00 | true |
| 7 | `hong-kong-broad-market` | 56.60 | `2800.HK` | 56.60 | true |

**解释**

- 雷达最强并非互联网平台，而是防御、公用事业、电信红利、能源和金融类。
- `energy` 内部 leader `0857.HK` 分数最高，但它被 `symbol_risk_veto` 阻断。
- `telecom-dividend` 的 `0941.HK` 技术分数强，但同样被 `symbol_risk_veto` 阻断。
- `utilities-defensive` 的 `0002.HK` 分数稳定，但也被 `symbol_risk_veto` 阻断。

### 2.2 中性或偏弱主题

**事实**

| theme | avg_score | leader | leader_score | 主要状态 |
|---|---:|---|---:|---|
| `hang-seng-tech` | 43.52 | `3067.HK` | 44.39 | 未达 `min_watch_score=45` |
| `internet-platform` | 32.34 | `9618.HK` | 72.27 | 主题均值弱，内部高度分化 |
| `consumer-discretionary` | 27.02 | `2020.HK` | 55.36 | 主题均值弱，leader 低量能惩罚 |
| `consumer-tech` | 0.00 | `1810.HK` | 0 | downtrend |
| `healthcare-biotech` | 0.00 | `2269.HK` | 0 | downtrend |
| `healthcare-pharma` | 0.00 | `1177.HK` | 0 | downtrend |

**解释**

- 科技 ETF 有单日反弹，但 `3033.HK` 与 `3067.HK` 都低于观察分数阈值，不能作为科技主题确认。
- 互联网平台单日领涨，但主题均分低，且 `0700.HK`、`1024.HK`、`1810.HK` 等多只仍在 downtrend 或低位区间，说明更像修复反弹而非全主题趋势确认。
- 医药主题继续是明确弱势，不适合逆势挖掘。

## 3. 贸易宇宙内的主题可执行性

### 3.1 总结结论

**事实**

- `actionable_candidates=[]`。
- `diagnostic_candidates` 只有：`0857.HK`、`0941.HK`、`0002.HK`。
- 三个 diagnostic candidates 均为 `diagnostic_only=true`、`qualified_for_action=false`，且 disqualifier 包含 `symbol_risk_veto`。
- 稳定规则要求：`actionable_candidates` 是唯一可进入升级考虑的确定性层；`diagnostic_candidates` 只能用于观察和解释。

**解释**

- 今日没有任何 trade universe 内标的可升级为 `buy_candidate`、`accumulate` 或 `hold`。
- 本轮正确动作是 `watch_only` + veto audit + peer-relative review，而不是从较低排名标的中寻找替代买点。

## 4. ETF 确认

### 4.1 宽基 ETF：`2800.HK`

**事实**

- `2800.HK` 最新收盘 26.24，单日 +1.74%。
- `ma20=25.8446`，`ma60=26.1507`；价格高于 MA20 和 MA60。
- `range_pos_60=0.4981`，处于 60 日区间中部。
- `volume_ratio_20=1.1216`，量能温和确认。
- ranking score=56.60，`qualified_for_watch=true`，但 `qualified_for_action=false`，`diagnostic_only=true`。
- `symbol_risk_veto=true`，原因包括 `pass_rate=0.069 over 101 evaluated calls`，以及近期 `2026-04-20`、`2026-04-21` 的误判。

**解释**

- `2800.HK` 可作为宽基情绪修复观察标的，但不能作为行动确认。
- 宽基 ETF 当前仅支持“市场风险偏好改善”的解释，不支持突破成本门槛后的交易升级。

### 4.2 恒生科技 ETF：`3033.HK` / `3067.HK`

**事实**

- `3033.HK`：收盘 4.81，单日 +1.78%，score=42.65，低于 `min_watch_score=45`。
- `3067.HK`：收盘 10.31，单日 +1.58%，score=44.39，低于 `min_watch_score=45`。
- 两者均为 `diagnostic_only=true`、`qualified_for_action=false`，并被 `symbol_risk_veto` 阻断。
- `3033.HK` 与 `3067.HK` 价格仍低于 MA60，主题 `hang-seng-tech` 平均分仅 43.52。

**解释**

- 恒生科技 ETF 反弹不足以确认科技主题可交易。
- 若后续要升级互联网平台或科技成长股，至少需要 ETF 先重新站稳 MA60、分数超过 watch/action 门槛，并出现日期对齐的 T+3/T+5 edge 证据。

## 5. 代表性主题与可用表达比较

### 5.1 `energy`

**事实**

可用标的：`0857.HK`、`0883.HK`、`0386.HK`。

| symbol | score | 状态 | 关键事实 | 约束 |
|---|---:|---|---|---|
| `0857.HK` | 84.42 | theme leader | 价格高于 MA20/MA60，MA20 高于 MA60，`volume_ratio_20=1.2356`，`range_pos_60=1.1084` | `symbol_risk_veto`，`qualified_for_action=false` |
| `0883.HK` | 73.93 | 同主题第 2 | uptrend，价格高于 MA20/MA60 | 非主题 leader，`symbol_risk_veto` |
| `0386.HK` | 50.67 | 同主题第 3 | `volume_ratio_20=2.2023`，`volume-expansion` | 非主题 leader，价格仍低于 MA60 |

**解释**

- 最好的当前主题表达是 `0857.HK`，但仅限审计观察。
- `0386.HK` 没有 `symbol_risk_veto`，但它不是主题 leader，且 `actionable_candidates=[]`。根据规则，不能把它作为被 veto leader 的替代行动标的。

### 5.2 `telecom-dividend`

**事实**

可用标的：`0941.HK`、`0728.HK`。

| symbol | score | 状态 | 关键事实 | 约束 |
|---|---:|---|---|---|
| `0941.HK` | 81.98 | theme leader | uptrend，`volume-expansion`，价格高于 MA20/MA60，`range_pos_60=1.1119` | `symbol_risk_veto`，`qualified_for_action=false` |
| `0728.HK` | 68.01 | 同主题第 2 | `volume-expansion`，单日 +1.93% | 非主题 leader，`symbol_risk_veto` |

**解释**

- 最好的当前主题表达是 `0941.HK`，但只能观察。
- `0728.HK` 量能强，但不是 leader，且同样被风险记录约束；不能替代升级。

### 5.3 `utilities-defensive`

**事实**

可用标的：`0002.HK`、`0006.HK`。

| symbol | score | 状态 | 关键事实 | 约束 |
|---|---:|---|---|---|
| `0002.HK` | 76.08 | theme leader | uptrend，价格高于 MA20/MA60，`volume_ratio_20=1.2769` | `symbol_risk_veto`，`qualified_for_action=false` |
| `0006.HK` | 74.86 | 同主题第 2 | uptrend，价格高于 MA20/MA60 | 非 theme leader，`symbol_risk_veto` |

**解释**

- 最好的当前表达是 `0002.HK`，但只适合 watch/audit。
- 防御主题分数高，说明资金对稳定现金流仍有偏好；但 posterior 记录对该类标的的通过率很弱，不能升级。

### 5.4 金融主题：`0005.HK`、`0388.HK`、`1299.HK`

**事实**

| theme | symbol | score | 关键事实 | 约束 |
|---|---|---:|---|---|
| `financials-bank` | `0005.HK` | 71.01 | uptrend，价格高于 MA20/MA60 | `symbol_risk_veto` |
| `financials-exchange` | `0388.HK` | 67.30 | 单日 +2.99%，`volume-expansion`，价格高于 MA20/MA60 | `symbol_risk_veto` |
| `financials-insurance` | `1299.HK` | 58.00 | 单日 +2.16%，价格接近 MA20/MA60 | `symbol_risk_veto`，低于 action score |

**解释**

- `0388.HK` 是金融内部最有短线动量的名字，因有量能扩张和单日强度。
- 但金融主题没有 actionable candidate；因此只能列为观察对象。

### 5.5 `internet-platform`

**事实**

可用标的：`0700.HK`、`9988.HK`、`3690.HK`、`1024.HK`、`9618.HK`。

| symbol | score | 关键事实 | 约束 |
|---|---:|---|---|
| `9618.HK` | 72.27 | 主题 leader，uptrend，价格高于 MA20/MA60 | `symbol_risk_veto`，样本少且有 selection error |
| `9988.HK` | 44.75 | 单日 +3.24%，高于 MA20 | 低于 watch score，非 theme leader，`symbol_risk_veto` |
| `3690.HK` | 44.67 | 雷达单日领涨 +3.55%，量能接近确认 | 低于 watch score，价格低于 MA20/MA60，非 theme leader |
| `0700.HK` | 0 | 单日 +1.14% | downtrend，低 range_pos，`symbol_risk_veto` |
| `1024.HK` | 0 | 单日 +2.93% | downtrend，低 range_pos，`symbol_risk_veto` |

**解释**

- 单日最亮眼是 `3690.HK` 与 `9988.HK`，但确定性排名内最好的表达是 `9618.HK`。
- 由于互联网平台主题均值只有 32.34，且近期 posterior selection errors 显示 `0700.HK`、`9988.HK` 多次错过实际最佳同业，今天不能从单日涨幅直接升级。
- 若未来重启该主题，需要明确比较 `9618.HK`、`3690.HK`、`1024.HK` 与 `9988.HK` 的新近相对强度，而不是默认选择大市值平台股。

### 5.6 消费、科技硬件、医药

**事实**

- `consumer-discretionary`：leader `2020.HK` score=55.36，但 `volume_ratio_20=0.5795`，低于量能要求，并有 `symbol_risk_veto`。
- `consumer-tech`：`1810.HK` score=0，downtrend，价格低于 MA20/MA60，`range_pos_60=0.0306`。
- `healthcare-biotech`：`2269.HK` score=0，downtrend，价格低于 MA20/MA60。
- `healthcare-pharma`：`1177.HK`、`1093.HK` score=0，均为 downtrend。

**解释**

- 消费和医药不是今天的优先方向。
- `1810.HK` 即使成交活跃，也仍是下跌趋势中的反弹观察，不应提前布局。

## 6. 外部机会与贸易宇宙覆盖

**事实**

- 本次 radar universe 中的强主题大多已在 trade universe 中有代表：`energy`、`telecom-dividend`、`utilities-defensive`、金融、宽基、科技 ETF 均已覆盖。
- 未发现“雷达强、但 trade universe 完全未覆盖”的主要主题。

**解释**

- 暂无必须新增的外部机会。
- 后续若要扩展 universe，优先不是新增同类替代标的，而是改善同主题 peer-relative selection：例如能源内不要只看 `0857.HK` 分数，还要验证它是否持续跑赢 `0883.HK`、`0386.HK`；互联网平台内必须验证 actual best peer。

## 7. 风险姿态

**事实**

- 投资 profile 为 balanced，单一持仓上限 10%，主题上限 30%，不允许杠杆、不允许反向 ETF、不允许低流动性。
- 交易成本假设：round-trip 35 bps，最低 edge 100 bps，且需要 edge 明显超过成本。
- `actionable_candidates=[]`。
- top diagnostic candidates：`0857.HK`、`0941.HK`、`0002.HK` 均被 `symbol_risk_veto` 阻断。
- 参数优化未更新 active strategy；原因包含 samples、improvement、win_rate、sample_quality 未通过。

**解释**

- 今日风险姿态应为保守观察：`watch_only`。
- 不能因为 `risk_on`、高分 leader、或单日涨幅强就降低成本门槛、edge 门槛或风险 veto。
- 后验评估提示当前最大风险不是看错当天方向，而是 symbol selection error 与过早升级 diagnostic signal。

## 8. 今日建议状态

**结论：全部维持 `watch_only`。**

| symbol/theme | 状态 | 原因 | 失效/升级条件 |
|---|---|---|---|
| `0857.HK` / `energy` | `watch_only` | 分数最高且能源主题强，但 `symbol_risk_veto`，非可行动层 | 只有进入 `actionable_candidates`、解除 veto，并显示相对 `0883.HK`/`0386.HK` 的新近优势，才可重新评估 |
| `0941.HK` / `telecom-dividend` | `watch_only` | 技术趋势与量能强，但 `symbol_risk_veto` | 需要日期对齐的 T+3/T+5 edge 与非 veto 状态 |
| `0002.HK` / `utilities-defensive` | `watch_only` | 主题稳健、分数高，但 posterior pass_rate 弱且 veto | 需要后验样本改善，不可凭防御属性直接升级 |
| `0388.HK` / `financials-exchange` | `watch_only` | 单日强、放量，但 `symbol_risk_veto` 且非 actionable | 需要连续相对强度与进入 action list |
| `3033.HK` / `3067.HK` | `watch_only` | 科技 ETF 反弹但未达 watch score，且低于 MA60 | 需站稳 MA60、分数超过阈值，并通过 edge/risk gate |
| `0700.HK` / `9988.HK` / `3690.HK` / `9618.HK` | `watch_only` | 互联网平台单日反弹但主题均值弱、选择错误历史明显 | 必须证明 actual best peer 的新近相对强度，而非默认买入反弹领涨股 |

## 9. 今日高优先级研究问题

1. `energy` 主题中，`0857.HK` 的高分是否只是区间高位延伸？与 `0883.HK`、`0386.HK` 在未来 T+3/T+5 的相对强度是否能证明它仍是最佳表达？
2. `telecom-dividend` 与 `utilities-defensive` 的强势是否代表防御现金流偏好，而非真正 `risk_on`？若是，是否应降低对高 beta 互联网反弹的解释权重？
3. `3033.HK` / `3067.HK` 何时能重新站上 MA60，并形成可验证的恒生科技 ETF 确认？没有 ETF 确认前，是否继续禁止单股科技升级？
4. `internet-platform` 的 actual best peer 近期在 `9618.HK`、`3690.HK`、`1024.HK`、`9988.HK` 间切换；下一轮如何量化 fresh relative strength，避免再次选择 `0700.HK` 或 `9988.HK` 的滞后反弹？
5. 本日非日期对齐行情导致只能审计：需要补齐哪一份 date-aligned snapshot，才能把 2026-01-23 的判断从 audit 转为可评估信号？
