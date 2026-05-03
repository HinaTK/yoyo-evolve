# 2026-01-09 市场评估（historical replay）

> 角色：`yoyo-invest`  
> 市场：港股 / ETF  
> 模式：recommendation_only  
> 时间窗口：14-90 天 swing  
> 重要数据质量提示：本轮输入的 `as_of_date` 为 `2026-01-09`，但行情字段 `quote_trade_date` / `quote_trade_time` 显示为 `2026-04-29`。按稳定规则，历史回放日期与报价日期不一致时，所有升级只能视为低置信度条件审计项；即使 `actionable_candidates` 非空，也不能当作实时可执行信号。

---

## 一、市场雷达事实

### 1. 市场状态

**事实**

- `market_summary.risk_state`: `risk_on`
- 股票平均单日涨幅：`avg_stock_move_1d = 1.606%`
- ETF 平均单日涨幅：`avg_etf_move_1d = 1.7%`
- 雷达领涨：
  - `3690.HK`：+3.55%，`internet-platform`
  - `9988.HK`：+3.24%，`internet-platform`
  - `0388.HK`：+2.99%，`financials-exchange`，且 `volume-expansion`
- 雷达落后：
  - `1093.HK`：-0.59%，`healthcare-pharma`，`downtrend`
  - `0006.HK`：-0.38%，但仍为 `uptrend`
  - `1177.HK`：-0.36%，`healthcare-pharma`，`downtrend`

**解释**

- 表面市场处于风险偏好改善阶段，涨幅扩散到 ETF、金融、能源、电讯与部分互联网平台。
- 但由于报价日期与回放日期不一致，本轮不能把 `risk_on` 当作 2026-01-09 当日的实时确认，只能作为排序与主题审计输入。

---

## 二、按主题强弱排序

### 1. 强势 / 高分主题

**事实**

| 主题 | 平均分 | 主题领头 | 领头分数 | 交易宇宙覆盖 |
|---|---:|---|---:|---|
| `utilities-defensive` | 75.47 | `0002.HK` | 76.08 | 有：`0002.HK`, `0006.HK` |
| `telecom-dividend` | 75.00 | `0941.HK` | 81.98 | 有：`0941.HK`, `0728.HK` |
| `financials-bank` | 71.01 | `0005.HK` | 71.01 | 有：`0005.HK` |
| `energy` | 69.67 | `0857.HK` | 84.42 | 有：`0857.HK`, `0883.HK`, `0386.HK` |
| `financials-exchange` | 67.30 | `0388.HK` | 67.30 | 有：`0388.HK` |

**解释**

- 防守、公用事业、电讯、能源、金融银行是雷达中最强的主题群。
- 这些主题均已在交易宇宙中覆盖，不属于外部机会；但覆盖不等于可行动，仍需通过 `actionable_candidates`、风险 veto、成交量与日期一致性检查。

### 2. 中性 / 观察主题

**事实**

| 主题 | 平均分 | 主题领头 | 领头分数 | 状态 |
|---|---:|---|---:|---|
| `financials-insurance` | 58.00 | `1299.HK` | 58.00 | 达 watch 分但低于 action 分 |
| `hong-kong-broad-market` | 56.60 | `2800.HK` | 56.60 | ETF 观察，低于 action 分 |
| `hang-seng-tech` | 43.52 | `3067.HK` | 44.39 | 低于 watch 门槛 |
| `consumer-discretionary` | 27.02 | `2020.HK` | 55.36 | 主题平均弱，个别股相对较好 |

**解释**

- `2800.HK` 能作为港股大盘温度计，但评分不足且有历史低 pass_rate，不能升级。
- `hang-seng-tech` ETF 未达到 watch 门槛，且 `3033.HK` / `3067.HK` 都有低 pass_rate 与选择错误记录，因此只能观察。
- 可选消费内部有分化，`2020.HK` 比同主题更强，但低成交量与风险 veto 阻止升级。

### 3. 弱势 / 回避升级主题

**事实**

| 主题 | 平均分 | 代表符号 | 主要问题 |
|---|---:|---|---|
| `internet-platform` | 32.34 | `9618.HK`, `9988.HK`, `3690.HK`, `0700.HK`, `1024.HK` | 主题平均弱，选择错误频繁 |
| `consumer-tech` | 0.00 | `1810.HK` | `downtrend`，低区间位置 |
| `healthcare-biotech` | 0.00 | `2269.HK` | `downtrend`，价格低于均线 |
| `healthcare-pharma` | 0.00 | `1177.HK`, `1093.HK` | `downtrend`，低区间位置 |

**解释**

- 互联网平台当天涨幅看起来突出，但确定性排名显示该主题平均分仅 32.34，且近期 selected-vs-best 错误密集。单日反弹不能替代 ETF、均线与同主题相对强度确认。
- 医药与小米相关主题处于技术弱势，当前不应从反弹角度提前升级。

---

## 三、ETF 确认

**事实**

- `2800.HK`：收盘 26.24，+1.74%，高于 `ma20=25.8446` 与 `ma60=26.1507`，`volume_ratio_20=1.1216`，评分 56.60，低于 action 分。
- `3033.HK`：收盘 4.81，+1.78%，高于 `ma20=4.7717`，但低于 `ma60=4.9835`，`volume_ratio_20=0.6564`，评分 42.65，低于 watch 分。
- `3067.HK`：收盘 10.31，+1.58%，高于 `ma20=10.2455`，但低于 `ma60=10.6875`，`volume_ratio_20=1.0774`，评分 44.39，低于 watch 分。

**解释**

- 大盘 ETF `2800.HK` 有温和确认，但不足以给出行动升级；后验摘要显示其 pass_rate 仅 0.086，且近期有多次 bullish misfire。
- 恒生科技 ETF 未收复 MA60，且评分低于 watch 门槛，因此不能支撑互联网平台或科技股升级。
- ETF 层面结论：风险偏好可以记录为改善，但 ETF 证据不足以支持高置信度进攻性配置。

---

## 四、交易宇宙内主题表达与可行动性

### 1. `financials-bank`：最佳表达为 `0005.HK`

**事实**

- `0005.HK` 是本轮唯一 `actionable_candidates` 成员。
- 分数：71.01，高于 `min_action_score=65`
- 趋势分：96.41
- 动量分：48.05
- 收盘：141.0
- `ma20=137.425`，`ma60=133.1856`
- `range_pos_60=0.8805`
- `volume_ratio_20=0.7907`
- `regime_flags`: `uptrend`
- `symbol_risk_veto=false`
- 但后验摘要中 `0005.HK` 样本数为 2，平均回报 -8.917%，pass_rate 0.0；样本很少但不支持过度自信。

**解释**

- 在确定性层面，`0005.HK` 是唯一有资格进入升级审查的标的。
- 但由于回放日期与报价日期不一致，本轮不能直接给 `buy_candidate`；更合适的状态是：**条件型 `watch_only` / 审计候选**。
- 若后续能取得日期一致的 2026-01-09 数据，并确认价格仍在 MA20、MA60 上方，且成交量不低于近期均值，才可重新评估是否升级。

**当前状态**：`watch_only`（条件审计项，非即时买入）

**触发条件**

- 日期一致数据确认 `0005.HK` 仍高于 MA20 与 MA60；
- `volume_ratio_20` 改善至约 1.0 或以上；
- 金融银行主题继续领先，且大盘 ETF 未转弱；
- 预期 swing edge 明显超过 35 bps 交易成本与 100 bps 最低边际门槛。

**失效条件**

- 跌回 MA20 下方并放量；或
- `2800.HK` 重新跌破 MA60，金融主题跟随转弱；或
- 后续同日期验证显示本轮信号来自日期错配而非真实 2026-01-09 强势。

---

### 2. `energy`：雷达强，但交易宇宙内无可行动表达

**事实**

- 主题平均分：69.67。
- `0857.HK`：分数 84.42，主题领头，但 `symbol_risk_veto=true`，原因包括低 pass_rate、负平均回报、近期 adverse breach、selection error。
- `0883.HK`：分数 73.93，但非主题领头，且 `symbol_risk_veto=true`。
- `0386.HK`：分数 50.67，无 risk veto，但低于 action 分，且不是主题领头。

**解释**

- 能源主题看起来强，但领头 `0857.HK` 被风险 veto 阻断。
- `0386.HK` 虽然风险历史更干净，但它没有出现在 `actionable_candidates`，也没有证明相对 `0857.HK` 的新鲜强势，因此不能作为替代升级。

**当前状态**：`watch_only`

**最佳当前表达**：无可行动表达；观察顺序为 `0857.HK` 主题强度、`0386.HK` 是否出现独立放量与相对强势。

---

### 3. `telecom-dividend`：主题强，但领头被 veto

**事实**

- 主题平均分：75.00。
- `0941.HK`：分数 81.98，`uptrend` + `volume-expansion`，但 `symbol_risk_veto=true`。
- `0728.HK`：分数 68.01，高于 action 分，但不是主题领头，`qualified_for_watch=false`，且 `symbol_risk_veto=true`。

**解释**

- 电讯股的技术形态强，但后验风险明显，不能把防守趋势直接转化为买入建议。
- 同主题替代 `0728.HK` 同样被 veto，且不是主题领头，因此不具备替代资格。

**当前状态**：`watch_only`

---

### 4. `utilities-defensive`：防守主题强，但风险历史阻断

**事实**

- 主题平均分：75.47，为最高主题。
- `0002.HK`：分数 76.08，主题领头，`uptrend`，但 `symbol_risk_veto=true`。
- `0006.HK`：分数 74.86，非主题领头，`uptrend`，但 `symbol_risk_veto=true`，且 `qualified_for_watch=false`。

**解释**

- 公用事业强势可能反映防守资金偏好，但两只主要表达都被后验风险阻断。
- 因为 `0006.HK` 不是主题领头且也被 veto，不能作为替代。

**当前状态**：`watch_only`

---

### 5. `financials-exchange`：`0388.HK` 动量强，但风险 veto

**事实**

- `0388.HK`：分数 67.30，高于 action 分。
- 单日涨幅：+2.99%。
- `volume_ratio_20=1.5564`，`volume-expansion`。
- 价格高于 MA20 与 MA60。
- `symbol_risk_veto=true`，原因是 pass_rate 0.0 over 4 evaluated calls。

**解释**

- `0388.HK` 是本轮最值得继续研究的金融 Beta / 交易活跃度表达之一。
- 但它只在 `diagnostic_candidates` / 排名层出现，没有进入 `actionable_candidates`，且有 veto；所以只能观察，不能升级。

**当前状态**：`watch_only`

---

### 6. `internet-platform`：短线反弹强，但不具备升级条件

**事实**

- 雷达领涨中有 `3690.HK` 与 `9988.HK`。
- 主题领头按排名为 `9618.HK`，分数 72.27，`uptrend`，但 `symbol_risk_veto=true`。
- `9988.HK`：分数 44.75，低于 watch 分；虽单日 +3.24%，但仍低于 MA60。
- `3690.HK`：分数 44.67，低于 watch 分，且价格低于 MA20 与 MA60。
- `0700.HK`、`1024.HK`：均为 `downtrend`，分数 0。
- 恒生科技 ETF `3033.HK` / `3067.HK` 未收复 MA60，评分低于 watch 门槛。
- 后验记录显示该主题 selected-vs-best 错误密集，近期 best peer 多次在 `9618.HK`、`9988.HK`、`1024.HK`、`3690.HK` 间切换。

**解释**

- 互联网平台是短线反弹最显眼的板块，但 ETF 未确认、主题平均分弱、同主题选择错误频繁。
- 当前不能追涨，也不能机械选择单日领涨股。

**当前状态**：`watch_only`

**最佳当前表达**：无可行动表达；若必须观察，优先跟踪 `9618.HK` 是否能在无 veto 或 veto解除条件下继续领先，同时比较 `9988.HK`、`3690.HK` 是否出现相对强度改善。

---

## 五、突出标的清单

### 可进入升级审查但未直接升级

| 符号 | 主题 | 状态 | 原因 |
|---|---|---|---|
| `0005.HK` | `financials-bank` | `watch_only` 条件审计项 | 唯一 `actionable_candidates`；但历史回放日期与报价日期不一致，且后验样本不支持高置信度 |

### 只作观察的高分诊断标的

| 符号 | 主题 | 分数 | 不升级原因 |
|---|---|---:|---|
| `0857.HK` | `energy` | 84.42 | `symbol_risk_veto`，历史负回报与 selection error |
| `0941.HK` | `telecom-dividend` | 81.98 | `symbol_risk_veto`，低 pass_rate |
| `0002.HK` | `utilities-defensive` | 76.08 | `symbol_risk_veto`，低 pass_rate 与 adverse breach |
| `0388.HK` | `financials-exchange` | 67.30 | `symbol_risk_veto`，未进入 `actionable_candidates` |

---

## 六、风险姿态

**事实**

- 组合模式为 recommendation_only，没有真实持仓。
- 单一标的上限：10%。
- 主题上限：30%。
- 不允许杠杆，不允许反向 ETF，不允许低流动性。
- 成本门槛：35 bps 往返成本，最低 edge 100 bps，并要求 edge 明显覆盖成本。
- 稳定规则要求：证据薄弱或冲突时降级为 `watch_only`。

**解释**

- 本轮最大风险不是流动性，而是信号日期错配与后验低 pass_rate。
- 因此今天的风险姿态应为：**低进攻、重观察、只保留条件触发**。
- 不应因 `risk_on` 或单日上涨而追逐互联网平台、恒生科技 ETF、能源或电讯高分诊断标的。

---

## 七、今日结论

**事实结论**

- 市场雷达显示 `risk_on`，但数据日期存在冲突。
- 强主题主要是 `utilities-defensive`、`telecom-dividend`、`financials-bank`、`energy`、`financials-exchange`。
- 交易宇宙中唯一进入 `actionable_candidates` 的标的是 `0005.HK`。
- 多数高分主题领头被 `symbol_risk_veto` 阻断。
- 恒生科技 ETF 未提供足够确认。

**投资解释**

- 今天不应给出直接买入建议。
- `0005.HK` 是唯一值得进行下一步日期对齐验证的候选，但当前状态仍应为 `watch_only`。
- 其他高分标的属于诊断队列，不是行动队列。

**推荐状态汇总**

| 符号 | 状态 | 时间窗口 | 置信度 |
|---|---|---|---|
| `0005.HK` | `watch_only`（条件审计项） | 14-90 天 | 低到中，受日期错配限制 |
| `0857.HK` | `watch_only` | 14-90 天 | 低 |
| `0941.HK` | `watch_only` | 14-90 天 | 低 |
| `0002.HK` | `watch_only` | 14-90 天 | 低 |
| `0388.HK` | `watch_only` | 14-90 天 | 低 |
| `3033.HK` / `3067.HK` | `watch_only` | 14-90 天 | 低 |

---

## 八、今日高优先级研究问题

1. 能否取得与 `2026-01-09` 对齐的 `0005.HK`、`2800.HK`、`0388.HK`、`0941.HK`、`0857.HK` 日线数据，以验证本轮排名是否被 `2026-04-29` 报价污染？
2. `0005.HK` 的银行主题强势是否有同日大盘 ETF、金融股内部广度、成交额扩张共同确认，还是只是单股趋势残留？
3. 能源主题中，`0386.HK` 是否出现相对 `0857.HK` 的新鲜 peer-relative strength，并且是否能在成交量和均线结构上独立达标？
4. `internet-platform` 主题是否能通过 `3033.HK` / `3067.HK` 收复 MA60 与放量来确认，而不是只依赖 `3690.HK`、`9988.HK` 的单日反弹？
5. 对被 `symbol_risk_veto` 阻断的高分防守股（`0941.HK`、`0002.HK`），历史失败主要来自方向错误、入场时点错误，还是 selected-vs-best 错误？
