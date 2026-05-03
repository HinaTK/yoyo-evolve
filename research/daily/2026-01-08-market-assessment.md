# 2026-01-08 港股市场评估（historical replay）

> 研究主体：`yoyo-invest`  
> 时间：2026-01-08 18:37  
> 模式：recommendation_only / historical bootstrap replay  
> 结论先行：本轮雷达显示 `risk_on`，但输入存在 `as_of_date=2026-01-08` 与行情字段 `quote_trade_date=2026-04-29` 不一致的问题。因此，即使 deterministic ranking 给出非空 `actionable_candidates`，也只能作为条件化审计线索，不能视为当日直接可执行信号。

## 1. 事实层：市场雷达结果

### 1.1 市场状态

- `market_summary.risk_state`: `risk_on`
- 雷达样本平均表现：
  - 股票平均 1 日涨幅：`avg_stock_move_1d=1.606%`
  - ETF 平均 1 日涨幅：`avg_etf_move_1d=1.7%`
- 当日雷达领涨：
  1. `3690.HK`：+3.55%，`internet-platform`
  2. `9988.HK`：+3.24%，`internet-platform`
  3. `0388.HK`：+2.99%，`financials-exchange`，且有 `volume-expansion`
- 当日雷达落后：
  1. `1093.HK`：-0.59%，`healthcare-pharma`，`downtrend`
  2. `0006.HK`：-0.38%，但仍为 `uptrend`
  3. `1177.HK`：-0.36%，`downtrend`

### 1.2 主题强度排序（基于 deterministic trade universe ranking）

| 排名 | theme | 平均分 | 主题领头 | 领头分数 | 领头是否通过主题资格 |
|---:|---|---:|---|---:|---|
| 1 | `utilities-defensive` | 75.47 | `0002.HK` | 76.08 | true |
| 2 | `telecom-dividend` | 75.00 | `0941.HK` | 81.98 | true |
| 3 | `financials-bank` | 71.01 | `0005.HK` | 71.01 | true |
| 4 | `energy` | 69.67 | `0857.HK` | 84.42 | true |
| 5 | `financials-exchange` | 67.30 | `0388.HK` | 67.30 | true |
| 6 | `financials-insurance` | 58.00 | `1299.HK` | 58.00 | true |
| 7 | `hong-kong-broad-market` | 56.60 | `2800.HK` | 56.60 | true |
| 8 | `hang-seng-tech` | 43.52 | `3067.HK` | 44.39 | false |
| 9 | `internet-platform` | 32.34 | `9618.HK` | 72.27 | true |
| 10 | `consumer-discretionary` | 27.02 | `2020.HK` | 55.36 | false |
| 11 | `consumer-tech` | 0.00 | `1810.HK` | 0.00 | false |
| 12 | `healthcare-biotech` | 0.00 | `2269.HK` | 0.00 | false |
| 13 | `healthcare-pharma` | 0.00 | `1177.HK` | 0.00 | false |

## 2. 解释层：市场结构与主题判断

### 2.1 风险偏好

解释上，雷达呈现选择性 `risk_on`：指数与 ETF 当日反弹，股票平均涨幅为正，金融、能源、电讯、公用事业等高现金流或防御收益类主题保持较高排序。与此同时，科技与互联网内部并不一致：`3690.HK`、`9988.HK` 单日反弹较强，但 `0700.HK`、`1024.HK`、`1810.HK` 仍处于 `downtrend` 或低位区间，恒生科技 ETF 仍低于行动门槛。

### 2.2 ETF 确认

事实：

- `2800.HK`：收盘 26.24，高于 `ma20=25.8446` 与 `ma60=26.1507`，`range_pos_60=0.4981`，`volume_ratio_20=1.1216`，评分 56.60，低于行动门槛 65。
- `3033.HK`：收盘 4.81，高于 `ma20=4.7717` 但低于 `ma60=4.9835`，评分 42.65，低于观察门槛 45。
- `3067.HK`：收盘 10.31，高于 `ma20=10.2455` 但低于 `ma60=10.6875`，评分 44.39，低于观察门槛 45。

解释：

- 宽基 ETF `2800.HK` 有一定风险偏好修复，但仅为观察级，不足以支持广泛升级。
- 科技 ETF `3033.HK`、`3067.HK` 均未重新站上 `ma60`，且评分未达 `min_watch_score=45`；这不支持将互联网或消费科技单名升级为行动候选。
- 稳定规则要求优先使用 ETF 做主题确认；本轮科技 ETF 确认不足，因此科技/互联网反弹更应视为低置信度反弹，而不是确定性趋势恢复。

## 3. 雷达主题在交易宇宙中的可行动性

> 规则约束：`actionable_candidates` 是唯一可升级考虑层；`diagnostic_candidates` 只能用于观察与解释。由于本轮行情日期不对齐，所有升级都进一步降级为“条件化审计项”。

### 3.1 `financials-bank`：最佳表达为 `0005.HK`

事实：

- `0005.HK` 是唯一 `actionable_candidates` 成员。
- 评分：71.01，高于 `min_action_score=65`。
- 趋势：`trend_score=96.41`。
- 动量：`momentum_score=48.05`，并不强。
- 价格：收盘 141.0，高于 `ma20=137.425` 与 `ma60=133.1856`。
- 均线结构：`ma20_above_ma60`。
- `range_pos_60=0.8805`，位置偏高但仍被模型标记为 constructive。
- `volume_ratio_20=0.7907`，没有放量确认。
- `symbol_risk.action_veto=false`。

解释：

`0005.HK` 是本轮交易宇宙中唯一通过 deterministic action layer 的标的，也是 `financials-bank` 的唯一可用表达。其优势来自趋势结构清晰、价格高于 20/60 日均线、风险 veto 未触发。弱点是动量一般、成交量没有明显确认，且因历史回放日期错配，不能直接升级为实盘 `buy_candidate`。

建议状态：`watch_only`，条件化 `buy_candidate` 审计项。

触发条件：若后续获得日期对齐行情，且 `0005.HK` 继续维持高于 `ma20` 与 `ma60`，同时 `volume_ratio_20` 回到 1.0 以上，才可重新评估是否升级为 `buy_candidate`。

失效条件：跌破 `ma20` 或金融银行主题排名明显转弱；若价格高位回落且 `range_pos_60` 从高位快速下行，也应取消行动观察。

时间窗口：14-90 天 swing。

信心：低到中；主要受日期错配与成交量不足约束。

### 3.2 `energy`：主题强，但领头 `0857.HK` 被风险 veto 阻断

事实：

- 主题平均分 69.67，排名第 4。
- 主题领头 `0857.HK`：评分 84.42，`uptrend`，`volume_ratio_20=1.2356`，但 `symbol_risk_veto=true`。
- veto 原因包括：`avg_return_pct=-11.390 over 31 evaluated calls`、不利阈值突破、重复 `symbol_selection_error`。
- 同主题 `0883.HK`：评分 73.93，但不是主题领头，且 `symbol_risk_veto=true`。
- 同主题 `0386.HK`：评分 50.67，无 action veto，但不是主题领头，且低于行动门槛。

解释：

能源主题雷达很强，但不能直接行动。稳定规则明确：主题领头被 `symbol_risk_veto` 阻断时，不能机械替换为同主题更“干净”的标的；替代标的必须独立通过趋势、成交量、相对强度与风险门槛，并证明相对 veto leader 的新近优势。本轮 `0386.HK` 虽无 veto，但未进入 `actionable_candidates`，不能升级。

建议状态：`watch_only`。

最佳当前表达：无可行动表达；观察队列可放 `0857.HK`、`0883.HK`、`0386.HK`，但仅用于比较主题延续与 peer-relative 改善。

失效条件：能源主题领头继续触发风险 veto，或油气股出现放量冲高回落。

### 3.3 `telecom-dividend`：强趋势但历史风险阻断

事实：

- 主题平均分 75.00，排名第 2。
- `0941.HK`：评分 81.98，`uptrend` + `volume-expansion`，但 `symbol_risk_veto=true`。
- veto 原因包括低 pass_rate、负平均回报、重复 `symbol_selection_error`。
- `0728.HK`：评分 68.01，`volume-expansion`，但不是主题领头，且 `symbol_risk_veto=true`。

解释：

电讯股从技术面看强，但 posterior risk 明确阻断。该主题适合作为风险偏好与高股息资金流监测，不适合作为今日行动推荐。

建议状态：`watch_only`。

最佳当前表达：无可行动表达；若后续需要重启该主题，应先验证 `0941.HK` 与 `0728.HK` 的相对强弱是否改善，并等待 veto 风险解除或出现独立确认。

### 3.4 `utilities-defensive`：分数高但不应追高

事实：

- 主题平均分 75.47，排名第 1。
- `0002.HK`：评分 76.08，`uptrend`，但 `symbol_risk_veto=true`。
- `0006.HK`：评分 74.86，`uptrend`，非主题领头，`symbol_risk_veto=true`。
- 两者 `range_pos_60` 均较高：`0002.HK=0.9407`，`0006.HK=0.9524`。

解释：

公用事业主题强度最高，但更多体现为防御资金或收益型偏好的拥挤表现。两个可用表达均受风险 veto 阻断，高位追入的安全边际不足。

建议状态：`watch_only`。

### 3.5 `financials-exchange`：`0388.HK` 强单日表现，但风险 veto 阻断

事实：

- `0388.HK`：评分 67.30，超过行动分数门槛。
- 单日涨幅 2.99%，`volume_ratio_20=1.5564`，有 `volume-expansion`。
- `symbol_risk_veto=true`，原因含 `pass_rate=0.000 over 2 evaluated calls`。
- 不在 `actionable_candidates`。

解释：

`0388.HK` 是雷达中较醒目的放量金融 beta 表达，但 deterministic layer 将其归为 diagnostic，而非 actionable。由于 action layer 未通过，不能升级；只可作为市场交易活跃度改善的观察信号。

建议状态：`watch_only`。

### 3.6 `financials-insurance`：`1299.HK` 观察级

事实：

- `1299.HK`：评分 58.00，低于行动门槛。
- 收盘 84.95，接近 `ma20=84.9275`，略低于 `ma60=85.1517`。
- `volume_ratio_20=1.2945`。
- 无 `symbol_risk_veto`。

解释：

`1299.HK` 有一定修复迹象，但尚未有效站稳 `ma60`，只能作为保险主题观察，不是行动候选。

建议状态：`watch_only`。

### 3.7 `hong-kong-broad-market`：`2800.HK` 有修复但历史风险不允许升级

事实：

- `2800.HK`：评分 56.60，低于行动门槛。
- 高于 `ma20` 与 `ma60`，`volume_ratio_20=1.1216`。
- `symbol_risk_veto=true`，包含低 pass_rate 与近期 misfire。

解释：

宽基 ETF 反弹对整体情绪有帮助，但 posterior evidence 显示宽基 bullish calls 近期多次失败。稳定规则要求宽基 ETF 需要 breadth、volume、moving-average 三重确认才可升级。本轮信息不足。

建议状态：`watch_only`。

### 3.8 `hang-seng-tech` 与 `internet-platform`：反弹强，但 ETF 与历史选择错误均限制升级

事实：

- `hang-seng-tech` 平均分 43.52，低于观察门槛。
- `3033.HK`、`3067.HK` 均低于 `ma60`，且均有 `symbol_risk_veto`。
- `internet-platform` 平均分 32.34，内部高度分化。
- `9618.HK` 分数 72.27，是互联网主题领头，但 `symbol_risk_veto=true`。
- `9988.HK` 单日 +3.24%，但评分 44.75，低于观察门槛，且 `symbol_risk_veto=true`。
- `0700.HK`、`1024.HK` 仍为 `downtrend`，评分为 0。

解释：

互联网平台当日反弹很显眼，但这更像选择性修复，而不是主题级确认。ETF 未站上 `ma60`，主题内部高低切换频繁，且近期 posterior selection errors 集中在互联网平台。按照现有规则，不能将单名反弹升级为 `buy_candidate`。

建议状态：`watch_only`。

最佳当前表达：无可行动表达。若必须观察，`9618.HK` 是当前模型分数最高者，但因 veto 只能作为 peer-relative 对照；`9988.HK` 与 `3690.HK` 需证明相对 `9618.HK` 的新近强度后才有讨论价值。

### 3.9 消费、医药、生物科技：整体不具备行动条件

事实：

- `consumer-discretionary` 平均分 27.02；`2020.HK` 为主题领头但仅 55.36，且低成交量与 veto 阻断。
- `consumer-tech` 的 `1810.HK` 评分 0，`downtrend`，低位区间。
- `healthcare-biotech`、`healthcare-pharma` 主题平均分为 0，多数标的处于 `downtrend`。

解释：

这些主题不适合今天承担主动风险。若出现短线反弹，也更可能是技术性修复而非可审计 swing setup。

建议状态：`watch_only`。

## 4. 今日候选与风险姿态

### 4.1 今日唯一条件化审计候选

| symbol | theme | deterministic state | 本报告状态 | 主要原因 |
|---|---|---|---|---|
| `0005.HK` | `financials-bank` | `actionable_candidates` | `watch_only` / 条件化 `buy_candidate` 审计项 | 唯一 action layer 通过；但行情日期错配，且成交量不足 |

### 4.2 不升级的主要原因

1. `as_of_date=2026-01-08` 与 `quote_trade_date=2026-04-29` 不一致，稳定规则要求降低行动置信度。
2. 多个高分主题领头被 `symbol_risk_veto` 阻断，包括 `0857.HK`、`0941.HK`、`0002.HK`。
3. 科技 ETF `3033.HK`、`3067.HK` 未重新站上 `ma60`，且低于观察门槛。
4. 互联网平台存在反弹，但 posterior selection errors 密集，不能用单日强势替代主题确认。
5. 组合模式是 recommendation_only，不应假设真实持仓；本报告只生成候选与触发条件。

### 4.3 风险控制框架

- 单一标的最大建议仓位上限：10%，但今日不直接给出实盘建仓建议。
- 主题最大暴露上限：30%。
- 不使用杠杆、不使用反向 ETF、不使用低流动性标的。
- 交易成本门槛：round trip 35 bps，最低 edge 100 bps，且预期 swing edge 需显著超过成本；当前除 `0005.HK` 外无 action layer 标的，`0005.HK` 也因日期错配只能观察。

## 5. 今日高优先级研究问题

1. `0005.HK` 的日期对齐行情是否仍维持在 `ma20` 与 `ma60` 之上，并且 `volume_ratio_20` 是否改善到 1.0 以上？
2. `2800.HK` 是否能提供宽基确认：成交量、市场宽度、以及价格相对 `ma60` 是否同步改善？
3. `3033.HK` 与 `3067.HK` 是否能重新站上 `ma60`，从而为互联网平台或消费科技单名提供 ETF 确认？
4. 被 veto 的强主题领头（`0857.HK`、`0941.HK`、`0002.HK`）是否只是历史选择错误导致的风险阻断，还是当前仍存在 peer-relative 弱化？
5. `financials-exchange` 中 `0388.HK` 的放量是否能持续，并改善其低 pass_rate 风险，还是仅为单日 headline/情绪驱动反弹？
