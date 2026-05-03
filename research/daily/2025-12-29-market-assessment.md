# 2025-12-29 港股市场评估

> 会话：historical  
> 研究员：yoyo-invest  
> 时间：2025-12-29 09:45  
> 模式：recommendation_only  
> 结论先行：今日没有确定性可升级标的；`actionable_candidates` 为空，所有候选只能作为观察队列或条件触发，不作为即时推荐。

## 1. 数据与使用边界

### 事实

- 市场雷达 `as_of_date` 为 `2025-12-29`。
- 快照 `generated_at` 为 `2026-04-29T01:46:01Z`。
- 多数行情字段的 `quote_trade_date` / `as_of` 显示为 `2026-04-29`，与本次历史回放日期不一致。
- 市场摘要给出的 `risk_state` 为 `neutral`。
- 确定性排序层：
  - `actionable_candidates`: 空。
  - `diagnostic_candidates`: `0006.HK`、`0002.HK`、`0857.HK`。
- 策略安全约束明确：`research_only: true`、`automatic_trading_enabled: false`。

### 解读

由于 `as_of_date` 与行情日期存在冲突，本报告把价格、均线、成交量与排序结果视为历史回放中的诊断材料，而不是严格的当日实盘确认。稳定规则要求：当回放日期与报价日期不一致时，推荐上限应降至低置信条件观察或 `watch_only`。再加上 `actionable_candidates` 为空，今天不应把任何 `diagnostic_candidates` 升级为 `buy_candidate`、`accumulate` 或 `hold`。

## 2. 市场雷达：按主题/板块强弱排序

### 事实：主题强度排名

| 排名 | 主题 | 平均分 | 主题领先标的 | 领先分数 | 交易宇宙覆盖 | 状态 |
|---:|---|---:|---|---:|---|---|
| 1 | `utilities-defensive` | 58.64 | `0006.HK` | 58.66 | 有 | 诊断强、不可行动 |
| 2 | `financials-bank` | 53.68 | `0005.HK` | 53.68 | 有 | 观察 |
| 3 | `telecom-dividend` | 48.50 | `0941.HK` | 57.70 | 有 | 观察但被风险历史压制 |
| 4 | `energy` | 44.10 | `0857.HK` | 57.99 | 有 | 诊断强、不可行动 |
| 5 | `financials-exchange` | 35.29 | `0388.HK` | 35.29 | 有 | 弱观察 |
| 6 | `hong-kong-broad-market` | 31.59 | `2800.HK` | 31.59 | 有 | 弱确认 |
| 7 | `internet-platform` | 17.52 | `9618.HK` | 52.43 | 有 | 分化，主题整体弱 |
| 8 | `consumer-discretionary` | 12.95 | `2020.HK` | 48.55 | 有 | 分化，主题整体弱 |
| 9 | `hang-seng-tech` | 0.00 | `3033.HK` | 0.00 | 有 | ETF 未确认 |
| 10 | `consumer-tech` | 0.00 | `1810.HK` | 0.00 | 有 | 弱 |
| 11 | `financials-insurance` | 0.00 | `1299.HK` | 0.00 | 有 | 弱 |
| 12 | `healthcare-biotech` | 0.00 | `2269.HK` | 0.00 | 有 | 弱 |
| 13 | `healthcare-pharma` | 0.00 | `1177.HK` | 0.00 | 有 | 弱 |

### 解读

今天的雷达不是典型风险偏好扩散行情。强度集中在防御、公用事业、高息/资源和部分金融，科技、互联网平台、医药与恒生科技 ETF 没有形成可靠确认。市场摘要虽为 `neutral`，但排序结构更像“防御与现金流资产相对强，成长风险资产未修复”。

## 3. 哪些雷达主题在交易宇宙内可执行？

### 总结

所有雷达主题都在交易宇宙中有代表标的，因此不存在“强主题未被交易宇宙覆盖、只能作为外部机会后续加入”的情况。但“有覆盖”不等于“可行动”：今天确定性层没有任何 `actionable_candidates`，所以所有主题只能进入观察与触发条件设计。

## 4. 主题内部比较与最佳表达

### 4.1 `utilities-defensive`：最强主题，但只能观察

#### 事实

- 主题平均分：58.64，为全市场雷达最高。
- 交易宇宙成员：`0006.HK`、`0002.HK`。
- `0006.HK`：
  - score 58.66，主题第 1。
  - `latest_close` 65.55，高于 `ma20` 63.6225 与 `ma60` 62.4233。
  - `ma20_above_ma60`，`regime_flags` 为 `uptrend`。
  - `range_pos_60` 1.0571，已处于 60 日区间高位上方。
  - `volume_ratio_20` 0.0889，低于 0.6。
  - 存在 `symbol_risk_veto`：历史样本 pass_rate=0.000，avg_return_pct=-7.380。
- `0002.HK`：
  - score 58.63，主题第 2。
  - `latest_close` 76.10，高于 `ma20` 74.5825 与 `ma60` 73.9937。
  - `regime_flags` 为 `uptrend`。
  - `range_pos_60` 1.0025。
  - `volume_ratio_20` 0.1383，低于 0.6。
  - 无 `symbol_risk_veto`，但不是主题分数领先者，且同样成交确认不足。

#### 解读

最佳主题表达不是自动选择 `0006.HK`。虽然 `0006.HK` 是分数领先者，但被 `symbol_risk_veto` 阻断；稳定规则也要求：被 veto 的主题领导者不能机械替换成同主题更干净的标的，替代者必须独立满足趋势、成交量、相对强度和风险门槛。`0002.HK` 风险历史更干净，但成交量确认不足，且没有证明相对 `0006.HK` 的新鲜领先优势。

- 当前最佳表达：`0002.HK` 作为“更干净的观察表达”。
- 当前推荐状态：`watch_only`。
- 升级条件：`0002.HK` 需要继续站稳 `ma20`/`ma60`，并且 `volume_ratio_20` 明显改善，同时相对 `0006.HK` 走强。
- 失效条件：跌回 `ma20` 下方，或防御主题平均分回落并失去主题领先地位。

### 4.2 `financials-bank`：`0005.HK` 趋势稳定但成交不足

#### 事实

- 主题平均分：53.68。
- 交易宇宙成员：`0005.HK`。
- `0005.HK`：
  - score 53.68。
  - `latest_close` 140.90，高于 `ma20` 137.425 与 `ma60` 133.1856。
  - `ma20_above_ma60`，`regime_flags` 为 `uptrend`。
  - `range_pos_60` 0.8765，处于 60 日区间高位区域。
  - `volume_ratio_20` 0.0101，显著不足。
  - 无 `symbol_risk_veto`。

#### 解读

`0005.HK` 是金融银行主题的唯一且最佳表达。趋势结构完整，但交易确认极弱，且不是 `actionable_candidates`。在中性市场里，这类高位慢趋势资产适合做观察基准，而不是追高。

- 当前最佳表达：`0005.HK`。
- 当前推荐状态：`watch_only`。
- 升级条件：放量维持在 `ma20`/`ma60` 上方，并且金融板块扩散到 `0388.HK` 或 `1299.HK`。
- 失效条件：跌破 `ma20`，或高位滞涨伴随主题排名下滑。

### 4.3 `telecom-dividend`：趋势强，但领导者被风险历史阻断

#### 事实

- 主题平均分：48.50。
- 交易宇宙成员：`0941.HK`、`0728.HK`。
- `0941.HK`：
  - score 57.70，主题第 1。
  - `latest_close` 84.85，高于 `ma20` 81.55 与 `ma60` 79.82。
  - `regime_flags` 为 `uptrend`。
  - `range_pos_60` 1.028。
  - `volume_ratio_20` 0.0073，极低。
  - 存在 `symbol_risk_veto`：pass_rate=0.062，avg_return_pct=-1.458。
- `0728.HK`：
  - score 39.30，低于 watch 门槛。
  - `latest_close` 5.20，高于 `ma20` 4.9625 与 `ma60` 5.0065。
  - `regime_flags` 为 `range`。
  - `volume_ratio_20` 0.0079，极低。

#### 解读

`0941.HK` 是趋势上最强的表达，但风险历史与成交确认均不支持升级。`0728.HK` 更弱，不能作为替代行动标的。

- 当前最佳表达：`0941.HK` 仅作主题观察锚。
- 当前推荐状态：`watch_only`。
- 升级条件：`0941.HK` 需要解除成交不足问题，并显示相对 `0728.HK` 的持续强势；同时风险 veto 需要由后续评估改善。
- 失效条件：跌破 `ma20`，或高息主题从前三强主题中掉出。

### 4.4 `energy`：资源主题有趋势，但首选标的被 veto

#### 事实

- 主题平均分：44.10。
- 交易宇宙成员：`0857.HK`、`0883.HK`、`0386.HK`。
- `0857.HK`：
  - score 57.99，主题第 1。
  - `latest_close` 11.72，高于 `ma20` 10.853 与 `ma60` 10.2045。
  - `regime_flags` 为 `uptrend`。
  - `range_pos_60` 1.0175。
  - `volume_ratio_20` 0.0222。
  - 存在 `symbol_risk_veto`：pass_rate=0.059，avg_return_pct=-15.332。
- `0883.HK`：
  - score 52.94，主题第 2。
  - `latest_close` 29.16，高于 `ma20` 27.258 与 `ma60` 26.6937。
  - `regime_flags` 为 `uptrend`。
  - `range_pos_60` 0.8159。
  - `volume_ratio_20` 0.0197。
  - 无 `symbol_risk_veto`，但不是主题分数领先者。
- `0386.HK`：
  - score 21.38。
  - `latest_close` 4.66，高于 `ma20` 4.5865，但低于 `ma60` 4.9833。
  - `regime_flags` 为 `range`。

#### 解读

能源主题内，`0857.HK` 趋势最强但被风险 veto 阻断。`0883.HK` 是更干净的同主题观察替代，但稳定规则要求替代者必须独立证明趋势、成交量、相对强度与风险门槛；当前最大短板仍是成交确认严重不足。

- 当前最佳表达：`0883.HK` 作为更干净的观察表达；`0857.HK` 只作为被 veto 的强趋势参照。
- 当前推荐状态：`watch_only`。
- 升级条件：`0883.HK` 放量上行，并在同主题中相对 `0857.HK` 改善；若油气主题继续进入前三，同时 `volume_ratio_20` 修复，才可重新评估。
- 失效条件：跌破 `ma20`，或能源主题平均分继续低于 watch 门槛。

### 4.5 `internet-platform` 与 `hang-seng-tech`：不确认风险偏好

#### 事实

- `internet-platform` 平均分 17.52，主题整体弱。
- 交易宇宙成员：`0700.HK`、`9988.HK`、`3690.HK`、`1024.HK`、`9618.HK`。
- `9618.HK` 为主题内分数最高，score 52.43，`regime_flags` 为 `uptrend`，但存在 `symbol_risk_veto`，且 `volume_ratio_20` 0.0191。
- `9988.HK` 单日涨幅 1.58%，为市场雷达涨幅领先者之一，但 score 21.40，低于 watch 门槛，且低于 `ma60` 138.9633。
- `0700.HK` score 0，`regime_flags` 为 `downtrend`，`range_pos_60` 0.0148。
- `hang-seng-tech` ETF：
  - `3033.HK` score 0，`regime_flags` 为 `downtrend`，低于 `ma20` 与 `ma60`。
  - `3067.HK` score 0，`regime_flags` 为 `downtrend`，低于 `ma20` 与 `ma60`。

#### 解读

互联网平台中个别股票有反弹，例如 `9988.HK` 与 `9618.HK`，但 ETF 确认缺失，主题平均分弱，恒生科技 ETF 仍处下行状态。稳定规则要求：低通过率与成长/科技类标的不能在缺少广义市场和 ETF 确认时升级。今天不应把单日反弹解读成 swing 多头信号。

- 当前最佳表达：无行动表达；若必须观察，优先观察 `9618.HK` 的相对强度与 `3033.HK` / `3067.HK` 是否修复。
- 当前推荐状态：`watch_only`。
- 升级条件：`3033.HK` 或 `3067.HK` 重回 `ma20` 并接近/收复 `ma60`，同时互联网平台内部出现多标的同步放量，而非单名反弹。
- 失效条件：`3033.HK` / `3067.HK` 继续低于 `ma20`/`ma60`，或 `0700.HK`、`9988.HK` 反弹无量回落。

### 4.6 `consumer-discretionary`：个别标的可观察，主题整体不强

#### 事实

- 主题平均分：12.95。
- 交易宇宙成员：`2020.HK`、`2331.HK`、`9992.HK`、`6862.HK`。
- `2020.HK`：score 48.55，主题第 1，高于 watch 门槛但低于 action 门槛；高于 `ma20` 与 `ma60`，`regime_flags` 为 `uptrend`，`volume_ratio_20` 0.0197。
- `2331.HK`：单日 -0.50%，score 3.25。
- `9992.HK`、`6862.HK`：均为 `downtrend`，score 0。

#### 解读

`2020.HK` 是消费可选里唯一有观察价值的表达，但主题整体弱，且成交确认不足。由于不是 `actionable_candidates`，只能作为后续主题扩散观察项。

- 当前最佳表达：`2020.HK`。
- 当前推荐状态：`watch_only`。
- 升级条件：`2020.HK` 放量突破并带动 `2331.HK` 或其他同主题成员改善。
- 失效条件：跌回 `ma20` 下方，或消费可选主题继续由弱势成员拖累。

## 5. ETF 确认

### 事实

- `2800.HK`：
  - score 31.59，低于 watch 门槛。
  - `latest_close` 25.94，高于 `ma20` 25.8446，但低于 `ma60` 26.1507。
  - `regime_flags` 为 `range`。
  - `volume_ratio_20` 0.0036。
  - 存在 `symbol_risk_veto`，pass_rate=0.119。
- `3033.HK`：
  - score 0。
  - 低于 `ma20` 4.7717 与 `ma60` 4.9835。
  - `regime_flags` 为 `downtrend`。
- `3067.HK`：
  - score 0。
  - 低于 `ma20` 10.2455 与 `ma60` 10.6875。
  - `regime_flags` 为 `downtrend`。

### 解读

ETF 层没有支持进攻性风险偏好。`2800.HK` 只能说明大市处于区间而非明确上行；`3033.HK` 与 `3067.HK` 均未确认恒生科技反弹。按照“优先用 ETF 确认主题”的规则，科技、互联网平台、消费成长类单名反弹都不能升级。

## 6. 今日突出标的与状态

| 标的 | 主题 | 事实亮点 | 主要阻断 | 状态 |
|---|---|---|---|---|
| `0002.HK` | `utilities-defensive` | 上升趋势、无 risk veto | 非主题 leader、成交不足 | `watch_only` |
| `0005.HK` | `financials-bank` | 上升趋势、无 risk veto | 成交不足、非 actionable | `watch_only` |
| `0883.HK` | `energy` | 上升趋势、无 risk veto | 非主题 leader、成交不足 | `watch_only` |
| `2020.HK` | `consumer-discretionary` | 主题内最强、上升趋势 | 主题弱、成交不足 | `watch_only` |
| `9618.HK` | `internet-platform` | 主题内分数最高、上升趋势 | risk veto、ETF 不确认 | `watch_only` |

## 7. 风险姿态

### 事实

- 市场 `risk_state` 为 `neutral`。
- `actionable_candidates` 为空。
- 顶部诊断候选普遍存在 `low_volume_ratio_20_below_0_6`。
- 多个分数领先标的存在 `symbol_risk_veto`：`0006.HK`、`0857.HK`、`0941.HK`、`9618.HK` 等。
- 主要 ETF 未形成清晰多头确认：`2800.HK` 未收复 `ma60`，`3033.HK` / `3067.HK` 仍在 `downtrend`。

### 解读

今天应采取保守观察姿态。最强的是防御与高息现金流资产，而不是宽基或科技 Beta；成交量指标又普遍不足，说明价格结构强于资金确认。对 swing 周期而言，当前更适合建立“下一步触发清单”，不适合在历史回放数据日期不一致且无 actionable 输出时主动升级。

## 8. 今日结论

### 推荐状态

- 总体市场：`watch_only`
- 可升级标的：无
- 重点观察主题：`utilities-defensive`、`financials-bank`、`energy`
- 暂不追逐主题：`hang-seng-tech`、`internet-platform`、`consumer-tech`、`healthcare-pharma`、`healthcare-biotech`

### 条件触发框架

1. 若 `2800.HK` 收复并站稳 `ma60`，且成交量明显改善，才重新评估宽基多头。
2. 若 `3033.HK` / `3067.HK` 从 `downtrend` 修复至至少站回 `ma20`，才重新评估科技与互联网平台单名。
3. 若 `0002.HK` 相对 `0006.HK` 持续走强并放量，可作为 `utilities-defensive` 的更干净候选重新进入候选池。
4. 若 `0883.HK` 相对 `0857.HK` 改善并放量，可作为能源主题的替代观察表达。
5. 若 `0005.HK` 继续沿 `ma20` 上行且金融主题扩散，可提高研究优先级，但仍需等待 deterministic 层产生 `actionable_candidates`。

## 9. 今日高优先级研究问题

1. `0002.HK` 是否已经开始相对 `0006.HK` 走强，还是只是同主题内跟随？需要比较近 3/5/10 日相对收益与成交量。
2. `0883.HK` 是否能成为能源主题中替代 `0857.HK` 的更干净表达？重点看相对强弱、成交确认和回撤质量。
3. `2800.HK` 距离重新站上 `ma60` 还需要多少幅度与成交配合？宽基是否足以支持非防御主题升级？
4. `3033.HK` 与 `3067.HK` 是否仍处于无效反弹？如果科技 ETF 不修复，`9988.HK` / `9618.HK` 的单名反弹应继续降级处理。
5. 今日成交量普遍偏低是数据源/回放时间问题，还是实际市场确认不足？需要用日期对齐的历史成交数据复核。
