# 2026-01-22 港股市场评估（historical replay）

> 研究模式：recommendation_only。本文只生成候选与研究优先级，不假设存在真实持仓。  
> 关键限制：本次 `as_of_date` 为 `2026-01-22`，但快照内行情字段显示 `quote_trade_date=2026-04-29`；根据稳定规则，非日期对齐行情只能作为条件审计与雷达观察，不能直接升级为交易建议。

## 1. 市场雷达事实

### 1.1 市场状态

**事实：**
- `market_summary.risk_state` = `risk_on`。
- 雷达股票平均 1 日涨幅：`avg_stock_move_1d=1.606%`。
- ETF 平均 1 日涨幅：`avg_etf_move_1d=1.7%`。
- 雷达领涨：`3690.HK` +3.55%、`9988.HK` +3.24%、`0388.HK` +2.99%。
- 雷达落后：`1093.HK` -0.59%、`0006.HK` -0.38%、`1177.HK` -0.36%。
- `failures=[]`，数据抓取层没有报告失败。

**解释：**
- 表面上是偏 `risk_on` 的反弹日，互联网平台与金融交易所出现较强 1 日动量。
- 但 `risk_on` 不能覆盖三项硬约束：`actionable_candidates=[]`、非日期对齐行情、多个高分标的存在 `symbol_risk_veto`。因此本轮结论上限是 `watch_only` / veto audit。

## 2. 主题强弱排序

### 2.1 雷达/交易宇宙内的主题强度

**事实：**

| 排名 | theme | 平均分 | 主题领先标的 | 领先分数 | 主题状态 |
|---:|---|---:|---|---:|---|
| 1 | `utilities-defensive` | 75.47 | `0002.HK` | 76.08 | 领先者达观察门槛，但被风险否决 |
| 2 | `telecom-dividend` | 75.00 | `0941.HK` | 81.98 | 领先者达观察门槛，但被风险否决 |
| 3 | `financials-bank` | 71.01 | `0005.HK` | 71.01 | 达观察门槛，但被风险否决 |
| 4 | `energy` | 69.67 | `0857.HK` | 84.42 | 分数最强之一，但被风险否决 |
| 5 | `financials-exchange` | 67.30 | `0388.HK` | 67.30 | 动量与放量突出，但被风险否决 |
| 6 | `financials-insurance` | 58.00 | `1299.HK` | 58.00 | 观察级别，低于行动分数 |
| 7 | `hong-kong-broad-market` | 56.60 | `2800.HK` | 56.60 | ETF 观察级别，低于行动分数且被风险否决 |
| 8 | `hang-seng-tech` | 43.52 | `3067.HK` | 44.39 | 低于观察门槛 |
| 9 | `internet-platform` | 32.34 | `9618.HK` | 72.27 | 主题均值弱，内部严重分化 |
| 10 | `consumer-discretionary` | 27.02 | `2020.HK` | 55.36 | 主题均值弱，领先者仍低于行动分数 |
| 11 | `consumer-tech` | 0.00 | `1810.HK` | 0.00 | 下行结构 |
| 12 | `healthcare-biotech` | 0.00 | `2269.HK` | 0.00 | 下行结构 |
| 13 | `healthcare-pharma` | 0.00 | `1177.HK` | 0.00 | 下行结构 |

**解释：**
- 防御、公用事业、电信高息、能源、金融类在模型分数上领先，但主要领先者不是可行动机会，因为都受到 `symbol_risk_veto` 或 `diagnostic_only=true` 限制。
- 科技与互联网表面有日内反弹，但主题 ETF 与多数平台股未形成足够趋势确认，且历史评估提示互联网选股存在反复 selected-vs-best miss。

## 3. ETF 确认

**事实：**
- `2800.HK`：收盘 26.24，1 日 +1.74%，高于 `ma20=25.8446` 与略高于 `ma60=26.1507`，`range_pos_60=0.4981`，`volume_ratio_20=1.1216`，分数 56.60。
- `3033.HK`：收盘 4.81，1 日 +1.78%，高于 `ma20=4.7717`，低于 `ma60=4.9835`，`range_pos_60=0.2131`，`volume_ratio_20=0.6564`，分数 42.65。
- `3067.HK`：收盘 10.31，1 日 +1.58%，高于 `ma20=10.2455`，低于 `ma60=10.6875`，`range_pos_60=0.2039`，`volume_ratio_20=1.0774`，分数 44.39。
- `hang-seng-tech` 主题平均分 43.52，低于 `min_watch_score=45`。
- `actionable_candidates=[]`。

**解释：**
- 大盘 ETF `2800.HK` 给出温和广谱确认，但只是观察级别，不足以触发行动。
- 恒生科技 ETF 反弹尚未越过 60 日均线，主题分数也未达观察门槛；不能用个别互联网股 1 日上涨替代 ETF 确认。
- 由于历史评估中 `2800.HK`、`3033.HK`、`3067.HK` 均有低 pass_rate 或近期 misfire，ETF 只能作为确认线索，不能作为自动 fallback。

## 4. 雷达主题在交易宇宙中的可表达性

所有雷达主题本轮均在 trade universe 中有代表标的；因此没有需要标注为“外部机会、以后考虑加入”的强雷达主题。问题不在可交易覆盖，而在行动门槛未通过。

### 4.1 `energy`

**事实：**
- `0857.HK`：score 84.42，`uptrend`，高于 ma20/ma60，`volume_ratio_20=1.2356`，是 energy 主题 leader，但 `symbol_risk_veto=true`，`qualified_for_action=false`。
- `0883.HK`：score 73.93，`uptrend`，但同主题非 leader，且 `symbol_risk_veto=true`。
- `0386.HK`：score 50.67，`range` + `volume-expansion`，没有 `symbol_risk_veto`，但同主题非 leader，低于行动分数，`qualified_for_action=false`。

**解释：**
- 当前 energy 最佳表达从模型分数看是 `0857.HK`，但只能做 veto audit。
- 不能因为 `0386.HK` 风险否决较少，就把它作为 `0857.HK` 的行动替代；规则要求同主题替代必须独立进入行动列表并证明相对强度，本轮没有满足。

### 4.2 `telecom-dividend`

**事实：**
- `0941.HK`：score 81.98，`uptrend` + `volume-expansion`，`range_pos_60=1.1119`，主题 leader，但 `symbol_risk_veto=true`。
- `0728.HK`：score 68.01，`range` + `volume-expansion`，同主题非 leader，`symbol_risk_veto=true`。

**解释：**
- 最佳表达是 `0941.HK`，但只适合观察其是否继续放量、是否出现可验证回撤后再上行。
- 因两个可选标的均被 veto，电信高息主题不能升级为交易建议。

### 4.3 `utilities-defensive`

**事实：**
- `0002.HK`：score 76.08，`uptrend`，主题 leader，`symbol_risk_veto=true`。
- `0006.HK`：score 74.86，`uptrend`，同主题非 leader，`symbol_risk_veto=true`。

**解释：**
- 最佳表达是 `0002.HK`，但只可列入观察。
- 该主题强度偏高，但在 `risk_on` 日防御股强势可能代表资金偏保守或高息/稳定现金流偏好，不能直接解读为进攻性行情全面确认。

### 4.4 `financials-bank` 与 `financials-exchange`

**事实：**
- `0005.HK`：score 71.01，`uptrend`，但 `symbol_risk_veto=true`。
- `0388.HK`：score 67.30，1 日 +2.99%，`volume_ratio_20=1.5564`，`range` + `volume-expansion`，但 `symbol_risk_veto=true`。

**解释：**
- 银行主题当前只有 `0005.HK`，交易所主题当前只有 `0388.HK`，分别是各自主题的唯一表达。
- `0388.HK` 是本轮更值得研究的“动量观察对象”，因为放量与涨幅突出；但它仍不能越过行动层，因为 deterministic layer 没有给出 actionable candidate。

### 4.5 `hong-kong-broad-market`

**事实：**
- `2800.HK`：score 56.60，`range`，高于 ma20/ma60，`qualified_for_watch=true`，但 `symbol_risk_veto=true`，`qualified_for_action=false`。

**解释：**
- `2800.HK` 是广谱市场温度计，而不是本轮行动标的。
- 近期 `2800.HK` 评估中出现 T+3/T+5 misfire，本轮需要等待 date-aligned 的 T+3/T+5 edge 确认后再考虑提高权重。

### 4.6 `hang-seng-tech` 与 `internet-platform`

**事实：**
- `3067.HK` score 44.39，`3033.HK` score 42.65，均低于观察门槛。
- `9618.HK` score 72.27，是 `internet-platform` 内部 leader，但 `symbol_risk_veto=true`，`qualified_for_action=false`。
- `9988.HK` +3.24%、`3690.HK` +3.55% 为日内领涨，但二者均非主题 leader，且分数分别为 44.75、44.67，低于观察门槛。
- `0700.HK`、`1024.HK` 处于 `downtrend`，分数为 0。

**解释：**
- 互联网平台是“日内强、结构弱、内部分化大”的主题。
- 当前最佳表达按模型是 `9618.HK`，但它仅可作为相对强度观察对象；不能因 `9988.HK` 与 `3690.HK` 领涨就追入，因为它们没有独立进入行动层。
- 历史 selection error 显示 `0700.HK` 与 `9988.HK` 多次跑输当期最佳同主题 peers；今后若要重新升级互联网主题，必须明确比较近期最佳 peer，如 `9618.HK`、`3690.HK`、`1024.HK`，而不是只看绝对反弹。

### 4.7 消费、医药与小米链

**事实：**
- `2020.HK` score 55.36，低于行动分数且 `symbol_risk_veto=true`。
- `2331.HK`、`9992.HK`、`6862.HK` 均未达观察条件或存在趋势/位置问题。
- `1810.HK` score 0，`downtrend`，低于 ma20/ma60。
- `2269.HK`、`1177.HK`、`1093.HK` 均为 `downtrend` 或分数为 0。

**解释：**
- 消费与医药目前更像反弹噪音或弱势修复，不是主线。
- `1810.HK` 与医药链应继续避免把低位反弹误判为趋势反转。

## 5. 行动层结论

**事实：**
- `actionable_candidates=[]`。
- top diagnostic candidates 为 `0857.HK`、`0941.HK`、`0002.HK`，三者均 `diagnostic_only=true` 且 `qualified_for_action=false`。
- 三个 top diagnostic candidates 均存在 `symbol_risk_veto`。
- 稳定规则要求：`qualified_for_watch=true` 只能作为雷达观察，不能升级；`risk_on` 不能覆盖空行动列表、非日期对齐行情或风险否决。

**解释：**
- 今日没有 deterministic layer 允许升级的标的。
- 本轮应执行 `watch_only`，重点做 veto audit、主题相对强度复核、以及 ETF 确认观察。

## 6. 风险姿态

**推荐状态：`watch_only`**

- 时间窗口：14-90 天 swing 观察窗口，但今天不建立买入候选。
- 仓位含义：recommendation_only，不涉及真实仓位管理。
- 风险上限：即使后续出现机会，也应遵守单一标的不超过 10%、单一主题不超过 30%、不使用杠杆、不使用反向 ETF。
- 成本门槛：预估双边成本 35 bps，行动前需要 swing edge 明显超过 100 bps 且至少为成本的 2 倍。
- 失效条件：若后续 date-aligned 数据仍显示 `actionable_candidates=[]`、ETF 未能确认、或候选继续带有 `symbol_risk_veto`，则维持 `watch_only`。

## 7. 今日高优先级研究问题

1. `0857.HK`、`0941.HK`、`0002.HK` 的 `symbol_risk_veto` 是否来自同一类错误：追高、主题误读、还是历史窗口内防御/高息风格切换误判？
2. `0388.HK` 的放量上涨是否能在 date-aligned 数据中持续，并且相对 `0005.HK`、`1299.HK` 形成金融主题内更优表达？
3. `2800.HK` 的温和突破是否能在 T+3/T+5 重新产生超过成本门槛的 edge，还是继续重复近期 broad-market ETF misfire？
4. `internet-platform` 内部，`9618.HK` 是否真的成为近期最佳表达，还是 `9988.HK`、`3690.HK` 的 1 日强势只是低位反弹？需要做 peer-relative 复核。
5. 恒生科技 ETF `3033.HK` / `3067.HK` 何时重新站上 ma60 并让 `hang-seng-tech` 主题分数回到 `min_watch_score=45` 以上？
