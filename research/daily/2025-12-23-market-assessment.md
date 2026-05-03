# 2025-12-23 港股市场评估

> 会话：historical  
> 角色：yoyo-invest  
> 输出用途：recommendation_only，不代表真实持仓管理。  
> 重要数据提示：本次快照 `as_of_date` 为 `2025-12-23`，但行情字段 `quote_trade_date` 为 `2026-04-28`。按稳定规则，日期不一致时，本报告只把排名和行情视为诊断材料，不把任何标的升级为即时行动建议。

## 1. 市场雷达：先看事实

### 1.1 市场状态事实

- `market_summary.risk_state`: `risk_off`
- 平均单日表现：
  - 股票：`avg_stock_move_1d = -0.946%`
  - ETF：`avg_etf_move_1d = -1.847%`
- 雷达涨幅领先：
  1. `0883.HK` CNOOC / 中国海洋石油：`+1.90%`，`uptrend`
  2. `0857.HK` PetroChina / 中国石油股份：`+1.83%`，`uptrend`
  3. `2269.HK` WuXi Biologics / 药明生物：`+1.26%`，但仍为 `downtrend` 且 `volume-expansion`
- 雷达跌幅落后：
  1. `1093.HK` CSPC Pharma / 石药集团：`-4.54%`，`downtrend`
  2. `1810.HK` Xiaomi / 小米集团-W：`-3.79%`，`downtrend`
  3. `1024.HK` Kuaishou / 快手-W：`-3.12%`，`downtrend`

### 1.2 按主题强弱排序的事实

确定性排名给出的主题强度：

| 排名 | 主题 | 平均分 | 主题领先标的 | 领先分数 | 领先标的是否通过主题资格 |
|---:|---|---:|---|---:|---|
| 1 | `utilities-defensive` | 72.44 | `0006.HK` | 75.51 | true |
| 2 | `telecom-dividend` | 67.53 | `0941.HK` | 76.46 | true |
| 3 | `energy` | 56.81 | `0857.HK` | 81.90 | true |
| 4 | `financials-bank` | 55.08 | `0005.HK` | 55.08 | false |
| 5 | `financials-exchange` | 47.16 | `0388.HK` | 47.16 | true |
| 6 | `internet-platform` | 16.40 | `9618.HK` | 63.25 | true |
| 7 | `consumer-discretionary` | 15.05 | `2020.HK` | 39.75 | false |
| 8 | `hong-kong-broad-market` | 0.00 | `2800.HK` | 0 | false |
| 9 | `hang-seng-tech` | 0.00 | `3033.HK` | 0 | false |
| 10 | `consumer-tech` | 0.00 | `1810.HK` | 0 | false |
| 11 | `financials-insurance` | 0.00 | `1299.HK` | 0 | false |
| 12 | `healthcare-biotech` | 0.00 | `2269.HK` | 0 | false |
| 13 | `healthcare-pharma` | 0.00 | `1177.HK` | 0 | false |

## 2. 市场雷达：解释

### 2.1 市场风格

事实显示今天不是广泛风险偏好扩张，而是防御、股息、电讯、公用事业、能源相对占优。互联网平台、恒生科技、消费科技、医药大多处在弱势或下跌结构中。

我的解释：这更像是 `risk_off` 中的防御轮动，而不是可以追逐成长股反弹的环境。小章鱼今天不要逞强。没有 ETF 确认、没有行动候选、还有日期错配，就不能把诊断强度误当成交易信号。

### 2.2 ETF 确认

事实：

- `2800.HK`：收 `25.98`，低于 `ma20=25.993` 与 `ma60=26.36`，`regime_flags=["downtrend"]`，评分 `0`。
- `3033.HK`：收 `4.726`，低于 `ma20=4.7682` 与 `ma60=4.9981`，`regime_flags=["downtrend"]`，评分 `0`。
- `3067.HK`：收 `10.15`，低于 `ma20=10.238` 与 `ma60=10.7185`，`regime_flags=["downtrend"]`，评分 `0`。

解释：宽基港股和恒生科技 ETF 都没有给出确认。即使部分单名股票有强势，ETF 层面不支持把风险资产整体升级。特别是 `internet-platform` 和 `hang-seng-tech`，缺少 ETF 确认，不能升级为 `buy_candidate`。

## 3. 雷达主题在交易池内的可行动性

关键约束：

- `actionable_candidates` 为空。
- 按规则，只有 `actionable_candidates` 有资格进入升级考虑。
- `diagnostic_candidates` 只能用于观察和解释，不能升级。
- 前三名诊断候选 `0857.HK`、`0941.HK`、`0006.HK` 全部被 `symbol_risk_veto` 阻断。

结论：今天没有即时可行动标的。所有主题最多进入观察队列。

### 3.1 `utilities-defensive`：雷达最强，交易池有代表，但不能行动

事实：交易池内代表为 `0006.HK` 与 `0002.HK`。

- `0006.HK`：
  - score `75.51`
  - `uptrend`
  - 收 `65.25`，高于 `ma20=63.41` 与 `ma60=62.3317`
  - `volume_ratio_20=1.0304`
  - 主题排名第 1
  - 但有 `symbol_risk_veto`：pass_rate `0.000` over 11 evaluated calls，avg_return_pct `-7.524%`
- `0002.HK`：
  - score `69.37`
  - `uptrend`
  - 收 `75.5`，高于 `ma20=74.4525` 与 `ma60=73.9485`
  - `volume_ratio_20=0.645`
  - 主题排名第 2
  - disqualifier: `not_theme_score_leader`

解释：公用事业防御主题是雷达上最强的主题之一。若只看趋势，`0006.HK` 是当前最强表达；但风险否决非常硬，不能行动。`0002.HK` 更干净一些，没有 `symbol_risk_veto`，但不是主题分数领先者，成交确认也一般，且 `actionable_candidates` 为空，所以也不能替代升级。

当前状态：`watch_only`。

观察条件：若后续日期一致的数据中，`0002.HK` 或 `0006.HK` 继续高于 ma20/ma60，且量能保持或改善，同时风险否决解除或出现更干净的同主题候选，才重新评估。

失效条件：主题跌破 ma20 或防御主题平均分明显回落，说明防御轮动失效。

### 3.2 `telecom-dividend`：强势明确，但领先标的被风险否决

事实：交易池内代表为 `0941.HK` 与 `0728.HK`。

- `0941.HK`：
  - score `76.46`
  - `uptrend`
  - 收 `84.65`，高于 `ma20=81.1925` 与 `ma60=79.7225`
  - `volume_ratio_20=1.0334`
  - range_pos_60 `1.0362`
  - 主题排名第 1
  - 但有 `symbol_risk_veto`：pass_rate `0.071` over 14 evaluated calls，avg_return_pct `-1.413%`
- `0728.HK`：
  - score `58.59`
  - `range`
  - 收 `5.17`，高于 `ma20=4.948` 与 `ma60=5.007`
  - `volume_ratio_20=1.3878`
  - 主题排名第 2
  - disqualifier: `not_theme_score_leader`

解释：电讯股息主题强，且 `0941.HK` 趋势结构漂亮；但它被历史风险否决阻断。`0728.HK` 的量能更强，但趋势分和主题排名弱于 `0941.HK`，不能仅因领先者被否决就机械替代。按规则，替代同主题标的必须独立满足趋势、量能、相对强度和风险门槛；今天它还不够。

当前状态：`watch_only`。

观察条件：优先看 `0728.HK` 是否能从 `range` 进入 `uptrend`，并保持 `volume_ratio_20 > 1.0`；同时观察 `0941.HK` 是否继续强势但不追。

失效条件：`0941.HK` 跌回 ma20 下方，或 `0728.HK` 跌破 ma60，说明主题强度退潮。

### 3.3 `energy`：雷达领涨主题，但最佳表达被风险否决，次优表达可观察

事实：交易池内代表为 `0857.HK`、`0883.HK`、`0386.HK`。

- `0857.HK`：
  - score `81.90`
  - `uptrend`
  - 收 `11.67`，高于 `ma20=10.8135` 与 `ma60=10.1555`
  - `volume_ratio_20=1.2254`
  - 主题排名第 1
  - 但有 `symbol_risk_veto`：pass_rate `0.067` over 15 evaluated calls，avg_return_pct `-15.736%`
- `0883.HK`：
  - score `72.45`
  - `uptrend`
  - 收 `28.98`，高于 `ma20=27.27` 与 `ma60=26.5997`
  - `pct_change_1d=+1.90%`
  - `volume_ratio_20=0.8064`
  - 主题排名第 2
  - disqualifier: `not_theme_score_leader`
  - 无 `symbol_risk_veto`
- `0386.HK`：
  - score `16.09`
  - `range`
  - 收 `4.59`，仅略高于 `ma20=4.581`，低于 `ma60=4.9945`
  - disqualifiers 包括 `range_pos_60_below_0_12` 与 `not_theme_score_leader`

解释：能源是今天最显眼的相对强势板块，`0857.HK` 是模型分数上的最佳表达，但历史风险表现太差，不能升级。`0883.HK` 是更干净的观察对象：趋势强、当日领涨、没有风险否决；问题是量能未确认且不是主题分数领先者。因此 `0883.HK` 是“后续研究优先级高”的同主题替代候选，但不是今天的即时推荐。

当前状态：`watch_only`，重点观察 `0883.HK`。

观察条件：若日期一致数据中 `0883.HK` 继续高于 ma20/ma60，且 `volume_ratio_20` 回到或超过 `1.0`，同时能源主题继续领先，可重新评估是否具备条件性 `buy_candidate`。

失效条件：`0883.HK` 跌破 ma20，或能源主题由领涨转为普跌。

### 3.4 `financials-bank` 与 `financials-exchange`：有结构但不够强

事实：

- `0005.HK`：score `55.08`，`uptrend`，高于 ma20/ma60，但 `volume_ratio_20=0.507`，disqualifier: `low_volume_ratio_20_below_0_6`。
- `0388.HK`：score `47.16`，`range`，高于 ma20，略高于 ma60，但有 `symbol_risk_veto`，pass_rate `0.000` over 2 evaluated calls。

解释：金融类不是今天最强主线。`0005.HK` 趋势还可以，但量能太弱；`0388.HK` 处于区间且有风险否决。它们适合观察，不适合行动。

当前状态：`watch_only`。

### 3.5 `internet-platform`：交易池覆盖充分，但缺少 ETF 和多数成分确认

事实：交易池内有 `0700.HK`、`9988.HK`、`3690.HK`、`1024.HK`、`9618.HK`。

- `9618.HK` 是主题分数领先者，score `63.25`，`uptrend`，但低于 action score，且有 `symbol_risk_veto`。
- `0700.HK`、`9988.HK`、`1024.HK` 均为 `downtrend`，评分 `0`。
- `3690.HK` 为 `range`，score `18.73`，低于 watch score。
- 恒生科技 ETF `3033.HK` 与 `3067.HK` 均为 `downtrend`，评分 `0`。

解释：互联网平台不是今天的行动主题。`9618.HK` 相对最好，但没有达到行动分数且被风险否决。ETF 不确认，主流大型平台股也没有恢复均线结构。根据历史错误模式，不能在这种结构下升级互联网或科技反弹。

当前状态：`watch_only`。

### 3.6 `consumer-discretionary`、`consumer-tech`、`healthcare`：弱势或反弹证据不足

事实：

- `consumer-discretionary` 平均分 `15.05`，领先者 `2020.HK` 仅 `39.75`，低于 watch score。
- `1810.HK` 当日 `-3.79%`，`downtrend`，评分 `0`。
- `2269.HK` 当日 `+1.26%` 且放量，但仍低于 ma20/ma60，`downtrend`，评分 `0`。
- `1093.HK` 当日 `-4.54%`，为雷达最大跌幅。

解释：这些主题里有个别反弹或放量点，但结构没有转强。尤其 `2269.HK` 的放量上涨只能作为“可能有事件驱动”的观察点，不能视为趋势确认。

当前状态：`watch_only`。

## 4. 今日突出标的清单

### 4.1 仅观察，不升级

| 标的 | 主题 | 观察理由 | 阻断原因 | 当前状态 |
|---|---|---|---|---|
| `0883.HK` | `energy` | 雷达涨幅第一，`uptrend`，无 `symbol_risk_veto` | 不是主题分数领先者，`volume_ratio_20=0.8064`，`actionable_candidates` 为空 | `watch_only` |
| `0728.HK` | `telecom-dividend` | 高于 ma20/ma60，量能强于 `0941.HK` | 不是主题分数领先者，仍为 `range` | `watch_only` |
| `0002.HK` | `utilities-defensive` | 防御主题强，趋势仍在 | 不是主题分数领先者，量能一般 | `watch_only` |
| `0005.HK` | `financials-bank` | 趋势保持在 ma20/ma60 上方 | `volume_ratio_20=0.507` 低于门槛 | `watch_only` |
| `2269.HK` | `healthcare-biotech` | 当日上涨且放量 | 仍为 `downtrend`，低于 ma20/ma60 | `watch_only` |

### 4.2 被风险否决但需继续跟踪的主题领先者

| 标的 | 主题 | 诊断分数 | 否决原因摘要 | 用途 |
|---|---|---:|---|---|
| `0857.HK` | `energy` | 81.90 | pass_rate `0.067`，avg_return_pct `-15.736%`，有 adverse breach | 只用于能源主题强度观察 |
| `0941.HK` | `telecom-dividend` | 76.46 | pass_rate `0.071`，avg_return_pct `-1.413%` | 只用于电讯股息主题强度观察 |
| `0006.HK` | `utilities-defensive` | 75.51 | pass_rate `0.000`，avg_return_pct `-7.524%`，有 adverse breach | 只用于公用事业主题强度观察 |

## 5. 风险姿态

事实：

- `risk_state` 为 `risk_off`。
- `actionable_candidates` 为空。
- 日期字段不一致：`as_of_date=2025-12-23`，但 `quote_trade_date=2026-04-28`。
- 宽基与科技 ETF 都处于 `downtrend`。
- 顶部诊断候选全部被 `symbol_risk_veto` 阻断。

解释：今天的正确风险姿态是保守观察。不能因为防御、能源、电讯看起来强，就忽略系统级风险约束。推荐模式下，今天应输出研究队列，而不是交易指令。

组合/建议层状态：

- 即时行动：无。
- 默认状态：`watch_only`。
- 单一标的最大仓位规则暂不触发，因为没有 `buy_candidate`。
- 主题暴露规则暂不触发，因为没有建议建仓。
- 若后续出现行动候选，也必须确认预期 swing edge 明确超过 35 bps 往返成本，并超过最低 100 bps edge 门槛。

## 6. 今日结论

### 事实结论

1. 市场处于 `risk_off`。
2. 最强主题是 `utilities-defensive`、`telecom-dividend`、`energy`。
3. ETF 确认不足：`2800.HK`、`3033.HK`、`3067.HK` 均为 `downtrend`。
4. `actionable_candidates` 为空。
5. 前三名诊断候选 `0857.HK`、`0941.HK`、`0006.HK` 都被 `symbol_risk_veto` 阻断。
6. 日期不一致降低所有行动信号可信度。

### 解释结论

今天不是买入日，是建立观察清单和验证主题持续性的日子。能源、防御、公用事业、电讯股息相对强，但最强表达被历史风险否决；更干净的替代表达还没有独立满足所有门槛。成长和科技缺少 ETF 确认，不应升级。

小章鱼今天要做的不是证明自己勇敢，而是证明自己守门。`watch_only` 是正确动作。

## 7. 今日高优先级研究问题

1. `0883.HK` 是否能在后续日期一致的数据中维持能源主题强度，并把 `volume_ratio_20` 提升到 `1.0` 以上？
2. `0728.HK` 是否能从 `range` 转为 `uptrend`，成为比被风险否决的 `0941.HK` 更干净的电讯股息表达？
3. `0002.HK` 是否能在公用事业主题内继续缩小与 `0006.HK` 的相对强度差距，并提供足够量能确认？
4. `2800.HK`、`3033.HK`、`3067.HK` 何时重新站上 ma20/ma60？没有 ETF 确认前，是否应继续冻结科技和互联网平台升级？
5. 当前快照日期错配是否来自历史回放数据管线问题？下一轮需要优先确认是否存在 date-aligned 行情，以免把未来报价误用于历史判断。
