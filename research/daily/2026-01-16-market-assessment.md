# 2026-01-16 港股市场评估（historical replay）

> 研究主体：`yoyo-invest`  
> 组合模式：recommendation_only  
> 适用周期：14-90 天 swing 观察  
> 输出文件：`research/daily/2026-01-16-market-assessment.md`

## 0. 数据与规则边界

### 事实

- 本轮输入的 `as_of_date` 为 `2026-01-16`。
- 快照 `generated_at` 为 `2026-04-29T15:29:27Z`。
- 多数行情字段的 `quote_trade_date` 为 `2026-04-29`，与 `as_of_date` 不一致。
- 确定性排序层显示：`actionable_candidates` 为空。
- `diagnostic_candidates` 前三名为 `0857.HK`、`0941.HK`、`0002.HK`，但三者均有 `symbol_risk_veto`，且 `qualified_for_action=false`。
- 成本门槛：往返成本估计 35bps，最低 swing edge 要求 100bps，并要求预期 edge 明显高于成本。

### 解读

- 因 `as_of_date` 与 `quote_trade_date` 不一致，本报告把行情与排序结果视为历史回放中的诊断材料，而不是可直接执行的当日交易信号。
- 因 `actionable_candidates=[]`，本轮没有任何标的可升级为 `buy_candidate`、`accumulate` 或 `hold`。所有候选只能作为 `watch_only` 或条件观察。
- 本报告重点是：识别强主题、比较主题内可用表达、列出缺失证据与后续触发条件。

---

## 1. 市场雷达：按主题强弱排序

### 事实

市场摘要显示：

- `risk_state`: `risk_on`
- 平均个股单日涨幅：`avg_stock_move_1d=1.606%`
- 平均 ETF 单日涨幅：`avg_etf_move_1d=1.7%`
- 当日领涨雷达：`3690.HK` +3.55%、`9988.HK` +3.24%、`0388.HK` +2.99%
- 当日落后雷达：`1093.HK` -0.59%、`0006.HK` -0.38%、`1177.HK` -0.36%

确定性主题评分排序：

| 排名 | theme | avg_score | 主题龙头 | leader_score | 主题状态 |
|---:|---|---:|---|---:|---|
| 1 | utilities-defensive | 75.47 | `0002.HK` | 76.08 | 强，但龙头被风险否决 |
| 2 | telecom-dividend | 75.00 | `0941.HK` | 81.98 | 强，但龙头被风险否决 |
| 3 | financials-bank | 71.01 | `0005.HK` | 71.01 | 强，但个股被风险否决 |
| 4 | energy | 69.67 | `0857.HK` | 84.42 | 强，但龙头被风险否决 |
| 5 | financials-exchange | 67.30 | `0388.HK` | 67.30 | 较强，但被风险否决 |
| 6 | financials-insurance | 58.00 | `1299.HK` | 58.00 | 观察级别 |
| 7 | hong-kong-broad-market | 56.60 | `2800.HK` | 56.60 | 观察级别 |
| 8 | hang-seng-tech | 43.52 | `3067.HK` | 44.39 | 未达 watch 门槛 |
| 9 | internet-platform | 32.34 | `9618.HK` | 72.27 | 主题分化，单一龙头强但被否决 |
| 10 | consumer-discretionary | 27.02 | `2020.HK` | 55.36 | 主题整体弱 |
| 11 | consumer-tech | 0.00 | `1810.HK` | 0.00 | 弱 |
| 12 | healthcare-biotech | 0.00 | `2269.HK` | 0.00 | 弱 |
| 13 | healthcare-pharma | 0.00 | `1177.HK` | 0.00 | 弱 |

### 解读

- 雷达呈现选择性 `risk_on`，但强势集中在防御、公用、电信、能源和部分金融，而不是高 beta 科技主题。
- 主题强度最高的几组并不等于可交易，因为主要候选被 `symbol_risk_veto` 阻断。
- 科技与互联网平台出现单日反弹，但 ETF 确认不足：`3033.HK`、`3067.HK` 均低于 watch 分数线，且仍未收复 `ma60`。
- 医药、消费科技和部分消费服务仍处于明显弱势，不适合逆势升级。

---

## 2. 市场状态与风险姿态

### 事实

- `2800.HK` 单日 +1.74%，收盘 26.24，高于 `ma20=25.8446` 和 `ma60=26.1507`，`range_pos_60=0.4981`，`volume_ratio_20=1.1216`。
- `3033.HK` 单日 +1.78%，收盘 4.81，高于 `ma20=4.7717`，但低于 `ma60=4.9835`，`volume_ratio_20=0.6564`。
- `3067.HK` 单日 +1.58%，收盘 10.31，高于 `ma20=10.2455`，但低于 `ma60=10.6875`，`volume_ratio_20=1.0774`。
- 低波动/防御类主题如 `utilities-defensive`、`telecom-dividend` 的主题得分领先。
- 强趋势个股中，多数高分标的带有 `symbol_risk_veto`。

### 解读

- 指数层面不是全面风险厌恶，`risk_state` 给出 `risk_on`，但可交易质量不足。
- `2800.HK` 对大市有一定确认，但分数 56.60 仅为观察级别，且历史后验显示低 pass_rate 与近期 broad-index ETF bullish failures，因此不能升级。
- 恒生科技 ETF 的反弹仍偏弱：价格仅收复 `ma20`，未收复 `ma60`，尤其 `3033.HK` 量能偏低；这不足以支持互联网平台单名升级。
- 当前风险姿态应为：保守观察，避免追涨，等待 date-aligned 行情、ETF 确认、量能与主题内相对强弱共同改善。

---

## 3. ETF 确认

### 事实

| ETF | theme | close | 1d | ma20 | ma60 | volume_ratio_20 | score | 结论 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `2800.HK` | hong-kong-broad-market | 26.24 | +1.74% | 25.8446 | 26.1507 | 1.1216 | 56.60 | 大市观察级确认 |
| `3033.HK` | hang-seng-tech | 4.81 | +1.78% | 4.7717 | 4.9835 | 0.6564 | 42.65 | 未达 watch 门槛 |
| `3067.HK` | hang-seng-tech | 10.31 | +1.58% | 10.2455 | 10.6875 | 1.0774 | 44.39 | 未达 watch 门槛 |

### 解读

- `2800.HK` 是当前大市确认的最佳 ETF 表达，但只支持 `watch_only`，不能支持买入升级。
- `3033.HK` 与 `3067.HK` 对科技主题的确认不足，尤其都低于 `ma60`，主题 score 也低于 45 的 watch 门槛。
- 在 ETF 确认不足的情况下，不应把 `9988.HK`、`3690.HK`、`0700.HK`、`1024.HK` 的单日反弹解读为可交易趋势反转。

---

## 4. 强雷达主题在交易宇宙内的可执行性

> 规则：只有 `actionable_candidates` 可进入升级考虑。本轮 `actionable_candidates=[]`，因此以下全部为主题观察与条件，不是交易建议。

### 4.1 `utilities-defensive`

### 事实

交易宇宙内可用标的：`0002.HK`、`0006.HK`。

| symbol | score | close | 1d | ma20 | ma60 | range_pos_60 | volume_ratio_20 | 状态 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `0002.HK` | 76.08 | 75.85 | +0.46% | 74.5825 | 73.9937 | 0.9407 | 1.2769 | 主题龙头，`symbol_risk_veto` |
| `0006.HK` | 74.86 | 65.00 | -0.38% | 63.6225 | 62.4233 | 0.9524 | 1.3544 | 非主题龙头，`symbol_risk_veto` |

### 解读

- 最佳当前表达是 `0002.HK`，因为它是主题得分龙头且价格结构强于均线。
- 但 `0002.HK` 后验样本显示 pass_rate=0.000、avg_return_pct=-2.133，触发 `symbol_risk_veto`，只能观察。
- `0006.HK` 分数接近，但不是主题龙头且同样被风险否决，不应替代升级。
- 结论：`watch_only`，观察防御类强势能否延续，不做行动升级。

### 4.2 `telecom-dividend`

### 事实

交易宇宙内可用标的：`0941.HK`、`0728.HK`。

| symbol | score | close | 1d | ma20 | ma60 | range_pos_60 | volume_ratio_20 | 状态 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `0941.HK` | 81.98 | 85.45 | +0.95% | 81.55 | 79.82 | 1.1119 | 1.5041 | 主题龙头，`symbol_risk_veto` |
| `0728.HK` | 68.01 | 5.27 | +1.93% | 4.9625 | 5.0065 | 0.7656 | 1.6770 | 非主题龙头，`symbol_risk_veto` |

### 解读

- 最佳当前表达是 `0941.HK`，趋势、量能和主题排名都强。
- 但 `0941.HK` 有 `symbol_risk_veto`：pass_rate=0.033，历史记录含 adverse breach 与 selection error。
- `0728.HK` 虽有量能扩张，但不是主题龙头，也被风险否决；不能作为自动替代。
- 结论：`watch_only`。该主题是高优先级观察主题，但不是可执行主题。

### 4.3 `energy`

### 事实

交易宇宙内可用标的：`0857.HK`、`0883.HK`、`0386.HK`。

| symbol | score | close | 1d | ma20 | ma60 | range_pos_60 | volume_ratio_20 | 状态 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `0857.HK` | 84.42 | 11.98 | +2.66% | 10.853 | 10.2045 | 1.1084 | 1.2356 | 主题龙头，`symbol_risk_veto` |
| `0883.HK` | 73.93 | 29.38 | +1.38% | 27.258 | 26.6937 | 0.8462 | 0.9994 | 非主题龙头，`symbol_risk_veto` |
| `0386.HK` | 50.67 | 4.70 | +2.40% | 4.5865 | 4.9833 | 0.1864 | 2.2023 | 非主题龙头，无 veto 但未进 action list |

### 解读

- 最佳当前表达按排序是 `0857.HK`，趋势与动量最强。
- 但 `0857.HK` 被 `symbol_risk_veto` 阻断，且后验显示 pass_rate=0.121、avg_return_pct 为负，并有 adverse breach 与 selection error。
- `0386.HK` 虽无 `symbol_risk_veto` 且量能扩张明显，但分数仅 50.67、低于行动门槛、不是主题龙头，且低于 `ma60`；根据规则，不能在龙头被 veto 后从低位同主题标的中挖替代品。
- 结论：`watch_only`。能源主题强，但当前无可执行表达。

### 4.4 金融主题：`financials-bank`、`financials-exchange`、`financials-insurance`

### 事实

| theme | 可用表达 | score | close | 1d | volume_ratio_20 | 状态 |
|---|---|---:|---:|---:|---:|---|
| `financials-bank` | `0005.HK` | 71.01 | 141.00 | +0.28% | 0.7907 | `symbol_risk_veto` |
| `financials-exchange` | `0388.HK` | 67.30 | 419.80 | +2.99% | 1.5564 | `symbol_risk_veto` |
| `financials-insurance` | `1299.HK` | 58.00 | 84.95 | +2.16% | 1.2945 | `symbol_risk_veto` |

### 解读

- `0388.HK` 是金融内部最突出的短线弹性表达，因为单日涨幅 +2.99%，且 `volume-expansion`。
- `0005.HK` 趋势稳定但量能不足，后验风险否决明确。
- `1299.HK` 刚贴近 `ma20`，仍低于 `ma60`，只适合观察。
- 金融主题在雷达中有强势信号，但三个表达均被风险层限制，不能升级。

### 4.5 `hong-kong-broad-market`

### 事实

- 交易宇宙内可用表达：`2800.HK`。
- `2800.HK` score=56.60，close=26.24，1d=+1.74%，高于 `ma20` 与 `ma60`，`volume_ratio_20=1.1216`。
- 后验摘要显示 `2800.HK` pass_rate 约 0.078-0.080，且近期有多次 `hold` / `buy_candidate` misfire。

### 解读

- `2800.HK` 是大市确认工具，不是本轮行动候选。
- 大市并不弱，但后验规则要求 breadth、volume、moving-average confirmation 同时改善后，才可重新升级 broad-index ETF。
- 当前只可用于确认风险偏好，不可单独作为买入建议。

### 4.6 `hang-seng-tech` 与 `internet-platform`

### 事实

恒生科技 ETF：

- `3067.HK` score=44.39，低于 watch 门槛 45；收盘低于 `ma60`。
- `3033.HK` score=42.65，低于 watch 门槛；收盘低于 `ma60`，`volume_ratio_20=0.6564`。

互联网平台内排序：

| symbol | score | close | 1d | ma20 | ma60 | range_pos_60 | 状态 |
|---|---:|---:|---:|---:|---:|---:|---|
| `9618.HK` | 72.27 | 117.50 | +1.91% | 115.5027 | 107.9074 | 0.7952 | 主题龙头，`symbol_risk_veto` |
| `9988.HK` | 44.75 | 130.60 | +3.24% | 127.52 | 138.9633 | 0.2200 | 低于 watch，`symbol_risk_veto` |
| `3690.HK` | 44.67 | 83.15 | +3.55% | 84.8 | 84.3275 | 0.3589 | 低于 watch，价格低于双均线 |
| `0700.HK` | 0.00 | 479.20 | +1.14% | 498.1 | 526.9 | 0.0364 | downtrend，`symbol_risk_veto` |
| `1024.HK` | 0.00 | 43.52 | +2.93% | 45.25 | 58.3908 | 0.0305 | downtrend，`symbol_risk_veto` |

### 解读

- 最佳当前表达按排序是 `9618.HK`，不是 `9988.HK` 或 `0700.HK`。
- 但 `9618.HK` 也被 `symbol_risk_veto` 阻断，且 ETF 层 `3033.HK` / `3067.HK` 未确认。
- `3690.HK` 是雷达单日涨幅第一，但价格仍低于 `ma20` 和 `ma60`，分数低于 watch 门槛；不能因为单日强势而升级。
- 后验选择错误显示，`0700.HK` 与 `9988.HK` 多次错过同主题 best peer，近期 best peer 在不同窗口包括 `9618.HK`、`9988.HK`、`3690.HK`、`1024.HK`。因此互联网平台必须先证明 fresh peer-relative improvement。
- 结论：整个科技/互联网主题维持 `watch_only`，且短线 timing confidence 低。

### 4.7 消费、医药与消费科技

### 事实

- `consumer-discretionary` 主题平均分 27.02，主题龙头 `2020.HK` score=55.36，但有 `low_volume_ratio_20_below_0_6` 与 `symbol_risk_veto`。
- `1810.HK` score=0，`downtrend`，低于 `ma20` 与 `ma60`。
- `2269.HK` score=0，`downtrend`，低于 `ma20` 与 `ma60`。
- `1177.HK` 与 `1093.HK` score=0，均为 `downtrend`，且均低于关键均线。

### 解读

- 消费、医药、消费科技都不是本轮主攻方向。
- 即使个别标的单日反弹，也缺乏趋势、量能和主题确认。
- 这些板块仅适合记录潜在超跌反弹风险，不适合做 `avoid` 或 `buy_candidate` 的强判断。

---

## 5. 今日可升级候选与观察候选

### 事实

- `actionable_candidates`: 空。
- `diagnostic_candidates`: `0857.HK`、`0941.HK`、`0002.HK`。
- 三个 diagnostic 标的都满足 watch 分数和趋势条件，但均被 `symbol_risk_veto` 阻断。

### 解读

- 今日没有可升级候选。
- diagnostic 标的用于说明市场强势集中在哪里，而不是交易清单。
- 在 `actionable_candidates=[]` 且 top diagnostic 均被 veto 的情况下，本轮应被定义为“风险否决审计 + 主题相对强弱观察”，不是选股行动日。

| symbol | 推荐状态 | 理由 | 触发升级条件 | 失效条件 |
|---|---|---|---|---|
| `0857.HK` | `watch_only` | 能源主题强，趋势与动量高，但 `symbol_risk_veto` | 重新进入 `actionable_candidates`，解除或绕过风险否决，并显示相对 `0883.HK`、`0386.HK` 的持续强势 | 跌回 `ma20` 下方或能源主题量价扩散失败 |
| `0941.HK` | `watch_only` | 电信股息主题强，量能扩张，但 `symbol_risk_veto` | 重新进入 `actionable_candidates`，同时保持高于 `ma20`/`ma60` 与成交确认 | 跌破 `ma20` 或 `0728.HK` 明显相对跑赢但主题未扩散 |
| `0002.HK` | `watch_only` | 公用防御主题强，价格结构好，但 `symbol_risk_veto` | 进入 `actionable_candidates`，并证明优于 `0006.HK` 的 peer-relative strength | 跌破 `ma20` 或防御主题整体回落 |
| `2800.HK` | `watch_only` | 大市 ETF 提供背景确认，但后验 broad-index ETF 失败较多 | breadth、volume、moving-average confirmation 同步改善，并进入 action list | 跌回 `ma60` 下方且成交放大 |
| `3033.HK` / `3067.HK` | `watch_only` | 科技 ETF 反弹但未收复 `ma60`，score 低于 watch 门槛 | 收复 `ma60`，score 升至 watch/action 门槛，且量能持续 | 再次跌破 `ma20` 或互联网平台龙头相对强弱恶化 |

---

## 6. 风险控制

### 事实

- 组合模式为 recommendation_only，没有真实持仓。
- 风险规则限制：单一仓位上限 10%，主题暴露上限 30%，不允许杠杆，不允许反向 ETF，不允许低流动性。
- 后验评估中，整体 pass 数量较低：652 次评估中 pass=59，fail=196，mixed=105，informational=292。
- 近期错误集中在 `symbol_selection_error`、`timing_unclear`、`theme_error`。

### 解读

- 当前最主要风险不是“看不出强主题”，而是“强主题没有干净的可执行表达”。
- 不能用高分 diagnostic 候选绕过 `symbol_risk_veto`。
- 不能因为某个同主题低位标的没有 veto，就把它替代成行动候选；它必须独立进入 `actionable_candidates`，并证明相对 veto leader 与近期 best peer 的 fresh relative strength。
- 因 date mismatch，本轮任何结论都应降低执行置信度。

---

## 7. 今日结论

### 事实结论

- 市场雷达为选择性 `risk_on`。
- 强主题主要为：`utilities-defensive`、`telecom-dividend`、`financials-bank`、`energy`、`financials-exchange`。
- `hang-seng-tech` ETF 确认不足，`internet-platform` 主题内部分化严重。
- 确定性交易层没有可行动候选：`actionable_candidates=[]`。

### 投资解读

- 今日不做升级推荐。
- 最值得跟踪的主题是能源、电信股息、公用防御和部分金融，但都需要等待风险否决解除、date-aligned 确认和 action list 入选。
- 科技与互联网平台仍需 ETF 与同主题相对强弱确认；当前反弹不应追。
- 整体推荐状态：`watch_only`。

---

## 8. 今日高优先级研究问题

1. `0857.HK`、`0941.HK`、`0002.HK` 的 `symbol_risk_veto` 是否来自可修正的择时问题，还是持续的选股质量问题？需要拆分 T+3/T+5 与 T+10/T+20 表现。
2. 能源主题中，`0386.HK` 虽无 veto 且量能扩张，但为何未进入 `actionable_candidates`？它是否能在后续证明相对 `0857.HK` 和 `0883.HK` 的 fresh relative strength？
3. `2800.HK` 是否真的完成大市确认？需要补充 breadth、成交、成分股扩散和是否稳在 `ma60` 之上。
4. `3033.HK` / `3067.HK` 若收复 `ma60`，互联网平台最佳表达应优先比较 `9618.HK`、`9988.HK`、`3690.HK`，还是仍需排除所有有 selection-error 历史的标的？
5. 金融主题中 `0388.HK` 的量能扩张是否可持续，还是仅为单日 headline/流动性驱动？需要后续 3-5 个交易日跟踪。
