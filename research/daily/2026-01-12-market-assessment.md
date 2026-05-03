# 2026-01-12 港股市场评估

> 角色：`yoyo-invest`  
> 模式：historical replay / recommendation_only  
> 适用周期：14-90 天 swing 观察  
> 结论先行：今日只输出 `watch_only` 与条件触发清单，不升级为 `buy_candidate`、`hold` 或 `accumulate`。

## 0. 数据完整性与使用边界

### 事实

- 回放日期为 `as_of_date=2026-01-12`。
- 快照中的行情字段显示 `quote_trade_date=2026-04-29`、`quote_trade_time=2026/04/29 16:08:xx`。
- 确定性排名层的 `actionable_candidates` 为空。
- 排名层的 `diagnostic_candidates` 为：`0857.HK`、`0941.HK`、`0002.HK`，但三者均有 `symbol_risk_veto`，且 `qualified_for_action=false`。
- 稳定规则要求：当 replay `as_of_date` 与 quote dates 不一致时，降级为低置信条件观察或 `watch_only`；当 `actionable_candidates` 为空时，不得升级 `diagnostic_candidates`。

### 解读

本报告只能作为历史回放基线与研究雷达，不构成当前可执行交易清单。即使若干主题和个股在诊断层显示较强趋势，日期错配、空行动清单、以及多个高分标的的风险否决共同阻止升级。今日的正确姿态是保存观察框架、列出触发条件，并避免把诊断分数误读为交易信号。

---

## 1. 市场雷达：按主题强弱排序

### 事实：市场状态

- `market_summary.risk_state` 为 `risk_on`。
- 雷达股票平均单日涨幅：`avg_stock_move_1d=1.606%`。
- 雷达 ETF 平均单日涨幅：`avg_etf_move_1d=1.7%`。
- 单日领涨：
  - `3690.HK` 美团：`+3.55%`，theme=`internet-platform`。
  - `9988.HK` 阿里巴巴：`+3.24%`，theme=`internet-platform`。
  - `0388.HK` 港交所：`+2.99%`，theme=`financials-exchange`，并有 `volume-expansion`。
- 单日落后：
  - `1093.HK` 石药集团：`-0.59%`，theme=`healthcare-pharma`。
  - `0006.HK` 电能实业：`-0.38%`，theme=`utilities-defensive`。
  - `1177.HK` 中国生物制药：`-0.36%`，theme=`healthcare-pharma`。

### 事实：主题排名层

| 强弱层级 | 主题 | 平均分 / 代表分 | 代表标的 | 雷达事实 |
|---|---:|---:|---|---|
| 第一梯队 | `utilities-defensive` | avg_score `75.47` | `0002.HK` | `0002.HK`、`0006.HK` 均处于高位趋势区间，但 `0006.HK` 当日微跌 |
| 第一梯队 | `telecom-dividend` | avg_score `75.00` | `0941.HK` | `0941.HK` 为 `uptrend` 且 `volume-expansion`，`0728.HK` 也放量 |
| 第一梯队 | `financials-bank` | score `71.01` | `0005.HK` | `0005.HK` 高位上行，价格在 MA20、MA60 上方 |
| 第一梯队 | `energy` | avg_score `69.67` | `0857.HK` | `0857.HK`、`0883.HK` 趋势强，`0386.HK` 放量但仍在区间内 |
| 第二梯队 | `financials-exchange` | score `67.30` | `0388.HK` | 单日强势且放量，但仍标记为 `range` |
| 第二梯队 | `financials-insurance` | score `58.00` | `1299.HK` | 接近均线，区间中部 |
| 第二梯队 | `hong-kong-broad-market` | score `56.60` | `2800.HK` | 广义市场 ETF 单日上涨，价格略高于 MA20、MA60，区间位置中性 |
| 弱确认 | `hang-seng-tech` | avg_score `43.52` | `3067.HK` | 科技 ETF 反弹但低于观察阈值，仍未收复 MA60 |
| 分化 | `internet-platform` | avg_score `32.34` | `9618.HK` | 主题内部明显分化：`9618.HK` 上行，`0700.HK`、`1024.HK` 仍为下行趋势 |
| 弱势 | `consumer-discretionary` | avg_score `27.02` | `2020.HK` | `2020.HK` 较稳，但主题内部广泛低分或低量 |
| 弱势 | `consumer-tech` | avg_score `0.00` | `1810.HK` | `1810.HK` 下行趋势，价格低于 MA20、MA60 |
| 弱势 | `healthcare-biotech` / `healthcare-pharma` | avg_score `0.00` | `2269.HK` / `1177.HK` | 医药、生物科技普遍下行或低分 |

### 解读：主题强度

今日雷达显示的是“选择性 risk_on”，不是全面普涨趋势确认。高分集中在防御公用事业、电信分红、银行、能源与交易所金融；科技互联网虽然单日有反弹，但 ETF 确认不足，内部个股趋势分化明显。医药、生物科技、消费科技仍处于弱势区，不应因单日小反弹提前抄底。

---

## 2. ETF 确认

### 事实

| ETF | 主题 | 最新收盘 | 1日涨跌 | MA20 | MA60 | range_pos_60 | volume_ratio_20 | 排名分 | 状态 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `2800.HK` | `hong-kong-broad-market` | `26.24` | `+1.74%` | `25.8446` | `26.1507` | `0.4981` | `1.1216` | `56.60` | `qualified_for_watch=true`，但 `symbol_risk_veto` |
| `3033.HK` | `hang-seng-tech` | `4.81` | `+1.78%` | `4.7717` | `4.9835` | `0.2131` | `0.6564` | `42.65` | 低于 watch 分数，MA60 未收复 |
| `3067.HK` | `hang-seng-tech` | `10.31` | `+1.58%` | `10.2455` | `10.6875` | `0.2039` | `1.0774` | `44.39` | 低于 watch 分数，MA60 未收复 |

### 解读

- `2800.HK` 给出了广义市场温和确认：价格站上 MA20 与 MA60，成交量略高于 20 日均量，但分数仅为观察级，且历史后验显示广义指数 ETF 近期 bullish calls 失败较多，因此不能升级。
- `3033.HK`、`3067.HK` 的科技 ETF 确认不足：虽然单日上涨，但仍低于 MA60，且排名分低于 `min_watch_score=45`。这意味着互联网平台个股的反弹缺少 ETF 层面的足够背书。
- 由于投资规则偏好“先用 ETF 确认主题，再升级单股”，科技与互联网主题今日最多只能作为观察对象。

---

## 3. 雷达主题在交易池中的可执行性

### 事实

本次雷达中的主题均在 trade universe 中有对应标的；没有“雷达强但交易池未覆盖”的外部机会。因此不存在需要标记为“未来可考虑加入交易池但今日不推荐”的外部主题。

### 可执行性原则

- 只有 `actionable_candidates` 可以进入升级考虑。
- 今日 `actionable_candidates=[]`。
- 因此所有主题，无论雷达强弱，最终推荐状态均不得高于 `watch_only`。
- `diagnostic_candidates` 只能用于解释强弱、设定观察条件、提出研究问题。

### 各主题最佳表达与结论

#### `utilities-defensive`

**事实**

- 主题平均分 `75.47`，为排名最高主题。
- `0002.HK`：score `76.08`，theme leader，`uptrend`，价格高于 MA20 与 MA60，`volume_ratio_20=1.2769`，但有 `symbol_risk_veto`，`qualified_for_action=false`。
- `0006.HK`：score `74.86`，同主题非 leader，`qualified_for_watch=false`，有 `not_theme_score_leader` 与 `symbol_risk_veto`。

**解读**

最佳表达是 `0002.HK`，但它只是诊断层观察标的，不是行动标的。若后续要重评，需要看到日期对齐数据中继续维持 MA20/MA60 上方、相对 `0006.HK` 保持强势，并解除或绕过后验风险否决。今日结论：`watch_only`。

#### `telecom-dividend`

**事实**

- 主题平均分 `75.00`。
- `0941.HK`：score `81.98`，theme leader，`uptrend` + `volume-expansion`，`range_pos_60=1.1119`，`volume_ratio_20=1.5041`，但有 `symbol_risk_veto`，`qualified_for_action=false`。
- `0728.HK`：score `68.01`，同主题非 leader，放量，`qualified_for_watch=false`，有 `not_theme_score_leader` 与 `symbol_risk_veto`。

**解读**

最佳表达是 `0941.HK`，趋势和成交量都强，但风险否决与行动清单为空阻止升级。`0728.HK` 不能仅因放量作为替代，因为它不是主题 leader，且没有独立通过行动门槛。今日结论：`watch_only`。

#### `energy`

**事实**

- 主题平均分 `69.67`。
- `0857.HK`：score `84.42`，全市场最高分，theme leader，`uptrend`，价格高于 MA20 与 MA60，`volume_ratio_20=1.2356`，但有 `symbol_risk_veto`，`qualified_for_action=false`。
- `0883.HK`：score `73.93`，同主题非 leader，`uptrend`，但有 `not_theme_score_leader` 与 `symbol_risk_veto`。
- `0386.HK`：score `50.67`，放量 `volume_ratio_20=2.2023`，但主题内排名第三，MA60 未收复，`qualified_for_action=false`。

**解读**

最佳趋势表达是 `0857.HK`，但后验风险否决非常强，不能升级。`0386.HK` 虽然没有 `symbol_risk_veto`，但它不是主题 leader，且趋势质量不足；稳定规则要求同主题替代必须独立满足趋势、成交量、相对强度和风险门槛，今日不满足。今日结论：`watch_only`，重点观察能源内部是否从 `0857.HK` 切换到更干净且更强的 peer。

#### `financials-bank`

**事实**

- `0005.HK`：score `71.01`，theme leader，`uptrend`，价格高于 MA20 与 MA60，但 `volume_ratio_20=0.7907`，有 `symbol_risk_veto`，`qualified_for_action=false`。

**解读**

`0005.HK` 是银行主题唯一表达，但后验风险与成交量不够强。今日只保留观察，不升级。

#### `financials-exchange`

**事实**

- `0388.HK`：score `67.30`，`pct_change_1d=+2.99%`，`volume_ratio_20=1.5564`，`regime_flags=["range", "volume-expansion"]`，有 `symbol_risk_veto`，`qualified_for_action=false`。

**解读**

`0388.HK` 是今日较值得关注的非防御性金融标的：单日放量强于多数金融股。但它仍被标记为 `range`，且行动层为空。若未来连续站稳 MA60 上方并维持放量，才可能重新进入条件候选。今日结论：`watch_only`。

#### `hong-kong-broad-market`

**事实**

- `2800.HK`：score `56.60`，高于 watch 阈值但低于 action 阈值；价格高于 MA20 与 MA60，`volume_ratio_20=1.1216`，但有 `symbol_risk_veto`。
- 后验摘要显示 `2800.HK` 样本 `81`，pass_rate `0.086`，近期有多次 bullish misfire。

**解读**

`2800.HK` 可以作为市场温度计，但不能作为买入候选。若要升级 broad-market ETF，需要宽度、成交量和均线确认同时改善，并且必须有非错配日期证据。今日结论：`watch_only`。

#### `hang-seng-tech`

**事实**

- `3067.HK`：score `44.39`，theme leader，但低于 watch 阈值，MA60 未收复，有 `symbol_risk_veto`。
- `3033.HK`：score `42.65`，同主题非 leader，低于 watch 阈值，MA60 未收复，有 `symbol_risk_veto`。

**解读**

科技 ETF 反弹仍不足以支持单股互联网升级。最佳表达只是相对的 `3067.HK`，但分数不足且 MA60 未收复。今日结论：`watch_only`，不追反弹。

#### `internet-platform`

**事实**

- 主题均分 `32.34`，但内部分化大。
- `9618.HK`：score `72.27`，theme leader，`uptrend`，价格高于 MA20 与 MA60，但 `volume_ratio_20=0.7545`，有 `symbol_risk_veto`，`qualified_for_action=false`。
- `9988.HK`：score `44.75`，单日 `+3.24%`，但低于 watch 阈值，MA60 未收复，同主题非 leader，有 `symbol_risk_veto`。
- `3690.HK`：score `44.67`，单日 `+3.55%`，成交量确认，但价格低于 MA20 与 MA60，且非 theme leader。
- `0700.HK`、`1024.HK`：score `0`，均为 `downtrend`，低位反弹属性明显。
- 后验选择错误中，`0700.HK` 与 `9988.HK` 多次错过同主题最佳 peer，近期 best peer 经常为 `9618.HK`、`9988.HK`、`3690.HK` 或 `1024.HK`，说明主题内部选择风险很高。

**解读**

最佳当前表达是 `9618.HK`，但它不具备行动资格。`9988.HK` 与 `3690.HK` 的单日涨幅属于反弹雷达，不是趋势确认；科技 ETF 也未确认。今日结论：互联网平台全组 `watch_only`，重点研究 peer-relative strength，而不是追涨领涨单日标的。

#### `consumer-discretionary`

**事实**

- `2020.HK`：score `55.36`，theme leader，价格高于 MA20 与 MA60，但 `volume_ratio_20=0.5795`，低于成交量门槛，且有 `symbol_risk_veto`。
- `2331.HK`、`9992.HK`、`6862.HK` 均低分或趋势不稳。

**解读**

最佳表达是 `2020.HK`，但成交量不足直接阻止升级。稳定规则明确：高趋势分和 theme leader 身份不能覆盖弱 `volume_ratio_20`。今日结论：`watch_only`。

#### `consumer-tech`、`healthcare-biotech`、`healthcare-pharma`

**事实**

- `1810.HK`、`2269.HK`、`1177.HK`、`1093.HK` 均为低分或 `downtrend`。
- `1810.HK` score `0`，价格低于 MA20 与 MA60，`range_pos_60=0.0306`。
- `1177.HK` 与 `1093.HK` 均 score `0`，医药主题弱势。

**解读**

这些主题今日没有可交易强度。若未来出现反弹，应先检查是否只是低位技术反抽；在没有 MA20/MA60 修复和 ETF/行业确认前，不做升级。

---

## 4. 今日 standout names：观察而非行动

### 观察清单

| 标的 | 主题 | 观察理由 | 阻止升级的原因 | 今日状态 |
|---|---|---|---|---|
| `0857.HK` | `energy` | 全市场最高 score `84.42`，趋势和量能合格 | `symbol_risk_veto`；`actionable_candidates` 为空；日期错配 | `watch_only` |
| `0941.HK` | `telecom-dividend` | score `81.98`，`uptrend` + `volume-expansion` | `symbol_risk_veto`；历史 pass_rate 很低；行动清单为空 | `watch_only` |
| `0002.HK` | `utilities-defensive` | score `76.08`，防御主题 leader | `symbol_risk_veto`；样本虽少但 pass_rate 为 `0.0`；行动清单为空 | `watch_only` |
| `0388.HK` | `financials-exchange` | 单日 `+2.99%` 且放量，金融弹性较好 | `range` 状态；`symbol_risk_veto`；行动清单为空 | `watch_only` |
| `9618.HK` | `internet-platform` | 互联网主题中唯一趋势较完整的 leader | `symbol_risk_veto`；成交量不足强确认；科技 ETF 未确认 | `watch_only` |

### 解读

这些名字定义了“今天应该看哪里”，但不定义“今天应该买什么”。最高分标的都被后验风险或行动层拦截，说明研究重点应转向：哪些强主题有持续性、哪些 leader 的历史选择错误可以被修复、哪些同主题 peer 能在后续提供更干净的相对强度证据。

---

## 5. 风险姿态

### 事实

- 投资组合模式为 `recommendation_only`，无真实持仓。
- 风险配置为 balanced，单一标的上限 `10%`，主题上限 `30%`，不允许杠杆，不允许反向 ETF，不允许低流动性。
- 成本门槛：估算双边交易成本 `35 bps`，最低 edge `100 bps`，要求 edge 明显超过成本。
- 今日没有任何 `qualified_for_action=true` 的候选进入 `actionable_candidates`。

### 解读

今日不应配置风险预算。即使市场表面为 `risk_on`，这更像“选择性修复 + 防御/高股息/能源偏强”的结构，而不是全市场可追风险。日期错配进一步降低信号可信度。所有交易想法都应停留在条件观察层：等待日期对齐、行动清单非空、ETF 确认、以及后验风险门槛改善。

---

## 6. 今日推荐状态

| 类型 | 状态 | 说明 |
|---|---|---|
| 市场整体 | `watch_only` | `risk_on` 但证据不满足行动层，且数据日期错配 |
| 防御公用事业 | `watch_only` | 强主题，但 `0002.HK`、`0006.HK` 均受风险门槛限制 |
| 电信分红 | `watch_only` | `0941.HK` 趋势最强，但 `symbol_risk_veto` 阻止升级 |
| 能源 | `watch_only` | `0857.HK` 分数最高但风险否决；替代 peer 不独立满足行动条件 |
| 金融 | `watch_only` | `0388.HK` 放量可观察，`0005.HK` 稳但不行动 |
| 广义市场 ETF | `watch_only` | `2800.HK` 仅为市场温度计，后验失败较多 |
| 科技 / 互联网 | `watch_only` | ETF 未确认，MA60 未修复，个股内部分化和选择错误风险高 |
| 医药 / 生物科技 / 消费科技 | `watch_only` | 弱趋势，不抄底 |

### 条件触发框架

仅当以下条件同时改善时，才允许下一轮重新评估是否从 `watch_only` 升级：

1. 使用日期对齐行情，解决 `as_of_date` 与 `quote_trade_date` 不一致问题。
2. `actionable_candidates` 非空，且候选 `qualified_for_action=true`。
3. 候选标的无 `symbol_risk_veto`，或有明确、可审计的新证据解释风险状态改善。
4. 对单股主题，相关 ETF 或广义市场确认改善；科技互联网尤其需要 `3033.HK` / `3067.HK` 收复 MA60 并放量。
5. 同主题替代标的必须证明相对被 veto leader 或近期 best peer 的新相对强度，而不是只依赖“风险记录更干净”。

---

## 7. 今日高优先级研究问题

1. `0857.HK` 的能源强势是否只是高位延伸，还是 `0883.HK`、`0386.HK` 能给出可持续的同主题确认？若 `0857.HK` 被 veto，哪个 peer 能在日期对齐数据中真正跑赢它？
2. `0941.HK` 的放量突破是否有基本面或资金流支撑，还是高股息拥挤交易？需要比较 `0941.HK` 与 `0728.HK` 的相对强弱和回撤风险。
3. `0388.HK` 的放量上涨是否预示金融交易活跃度改善？是否能连续站稳 MA20/MA60 上方并维持 `volume_ratio_20>1.2`？
4. `3033.HK` 与 `3067.HK` 何时能收复 MA60？在此之前，`9988.HK`、`3690.HK`、`9618.HK` 的反弹是否都只能视为单股噪音？
5. 为什么高分主题 leader 普遍被 `symbol_risk_veto` 拦截？需要复核后验错误中是方向错误、时点错误，还是 selected-vs-best 选择错误，以决定后续是调整主题选择还是标的选择规则。
