# 2026-01-19 港股市场评估（historical）

> 模式：recommendation_only。本文只生成研究候选与条件触发，不假设真实持仓。  
> 重要数据质量提示：输入的 `as_of_date` 为 `2026-01-19`，但行情字段 `quote_trade_date` / `as_of` 显示为 `2026-04-29`。按稳定规则，本轮所有结论最多只能作为低置信度条件观察或 `watch_only`，不能视为日期对齐的直接交易信号。

## 1. 市场雷达：先看主题强弱

### 事实

- 市场雷达的 `risk_state` 为 `risk_on`。
- 雷达样本中，股票平均 1 日涨幅为 `1.606%`，ETF 平均 1 日涨幅为 `1.7%`。
- 当日雷达领涨：
  1. `3690.HK` 美团-W：`+3.55%`，theme=`internet-platform`，`range`。
  2. `9988.HK` 阿里巴巴-W：`+3.24%`，theme=`internet-platform`，`range`。
  3. `0388.HK` 香港交易所：`+2.99%`，theme=`financials-exchange`，`range` + `volume-expansion`。
- 当日雷达落后：
  1. `1093.HK` 石药集团：`-0.59%`，theme=`healthcare-pharma`，`downtrend`。
  2. `0006.HK` 电能实业：`-0.38%`，theme=`utilities-defensive`，但仍为 `uptrend`。
  3. `1177.HK` 中国生物制药：`-0.36%`，theme=`healthcare-pharma`，`downtrend`。
- 确定性主题排名显示：
  - `utilities-defensive` 平均分 `75.47`，leader=`0002.HK`。
  - `telecom-dividend` 平均分 `75.0`，leader=`0941.HK`。
  - `financials-bank` 平均分 `71.01`，leader=`0005.HK`。
  - `energy` 平均分 `69.67`，leader=`0857.HK`。
  - `financials-exchange` 平均分 `67.3`，leader=`0388.HK`。
  - `hong-kong-broad-market` 平均分 `56.6`，leader=`2800.HK`。
  - `hang-seng-tech` 平均分 `43.52`，未达到 `min_watch_score=45`。
  - `internet-platform` 平均分 `32.34`，但内部 leader=`9618.HK` 分数 `72.27`。
  - `consumer-tech`、`healthcare-biotech`、`healthcare-pharma` 当前分数为 `0.0`。

### 解读

- 表面风险偏好为 `risk_on`，但强势并非全面科技反弹，而更偏向防御高分红、公用事业、能源、银行/交易所等低波动或现金流主题。
- 互联网平台虽然出现单日领涨，但主题平均分低，分化明显；`3690.HK` 与 `9988.HK` 的单日反弹不能直接推导为整个互联网平台主题可交易。
- 医药主题整体仍弱，多个样本处于 `downtrend`，不适合作为今日优先研究的多头方向。

## 2. 雷达主题在 trade universe 内的可执行性

### 总体事实

- `actionable_candidates` 为空：`[]`。
- 因此，按规则，确定性层没有任何标的有资格从观察升级为 `buy_candidate`、`accumulate` 或 `hold`。
- `diagnostic_candidates` 仅包含观察队列：`0857.HK`、`0941.HK`、`0002.HK`。
- 这三个最高诊断候选均被 `symbol_risk_veto` 阻断，且 `qualified_for_action=false`。
- 雷达中出现的主要强主题均已在 trade universe 中有代表标的；本轮没有“雷达强但 trade universe 缺席”的主题需要作为外部机会加入观察池。

### 主题逐项对照

| 雷达主题 | trade universe 代表 | 当前最佳表达 | 事实状态 | 今日结论 |
|---|---:|---:|---|---|
| `utilities-defensive` | `0002.HK`, `0006.HK` | `0002.HK` | 主题均分 `75.47`；`0002.HK` score=`76.08`，但 `symbol_risk_veto` | `watch_only`，仅做防御强度观察 |
| `telecom-dividend` | `0941.HK`, `0728.HK` | `0941.HK` | 主题均分 `75.0`；`0941.HK` score=`81.98`，但 `symbol_risk_veto` | `watch_only`，等待风险记录改善与日期对齐确认 |
| `energy` | `0857.HK`, `0883.HK`, `0386.HK` | `0857.HK` | `0857.HK` score=`84.42`，但 `symbol_risk_veto`；`0386.HK` 无 veto 但非主题 leader 且不在 action list | `watch_only`，不能从低排名 peer 挖替代交易 |
| `financials-bank` | `0005.HK` | `0005.HK` | score=`71.01`，`uptrend`，但 `symbol_risk_veto` | `watch_only` |
| `financials-exchange` | `0388.HK` | `0388.HK` | score=`67.3`，`volume-expansion`，但 `symbol_risk_veto` | `watch_only`，作为风险偏好确认指标 |
| `financials-insurance` | `1299.HK` | `1299.HK` | score=`58.0`，低于行动阈值且有 `symbol_risk_veto` | `watch_only` |
| `hong-kong-broad-market` | `2800.HK` | `2800.HK` | score=`56.6`，低于行动阈值；近期 broad ETF bullish failures | `watch_only`，需 breadth/volume/MA 确认 |
| `hang-seng-tech` | `3033.HK`, `3067.HK` | `3067.HK` | 主题均分 `43.52`，低于 watch 阈值；两个 ETF 均未收复 MA60 | `watch_only`，不升级科技反弹 |
| `internet-platform` | `0700.HK`, `9988.HK`, `3690.HK`, `1024.HK`, `9618.HK` | `9618.HK` | `9618.HK` 分数最高但 `symbol_risk_veto`；`3690.HK` 单日最强但低于 watch 阈值且低于 MA20/MA60 | `watch_only`，需要 ETF 与 peer-relative 重新确认 |
| `consumer-discretionary` | `2020.HK`, `2331.HK`, `9992.HK`, `6862.HK` | `2020.HK` | `2020.HK` score=`55.36` 但成交量比率 `0.5795` 低于流动性/量能门槛 | `watch_only` |
| `consumer-tech` | `1810.HK` | `1810.HK` | score=`0`，`downtrend`，低于 MA20/MA60 | 回避升级，仅观察 |
| `healthcare-biotech` | `2269.HK` | `2269.HK` | score=`0`，`downtrend` | 回避升级，仅观察 |
| `healthcare-pharma` | `1177.HK`, `1093.HK` | `1177.HK` | score=`0`，均弱势或下跌 | 回避升级，仅观察 |

## 3. 市场状态与 ETF 确认

### 事实

- `2800.HK`：收盘 `26.24`，1 日 `+1.74%`，高于 MA20=`25.8446` 与 MA60=`26.1507`，`range_pos_60=0.4981`，`volume_ratio_20=1.1216`，score=`56.6`。
- `3033.HK`：收盘 `4.81`，1 日 `+1.78%`，高于 MA20=`4.7717`，低于 MA60=`4.9835`，`volume_ratio_20=0.6564`，score=`42.65`。
- `3067.HK`：收盘 `10.31`，1 日 `+1.58%`，高于 MA20=`10.2455`，低于 MA60=`10.6875`，`volume_ratio_20=1.0774`，score=`44.39`。
- 科技 ETF 的主题分数仍低于 `min_watch_score=45`，且没有进入 `actionable_candidates`。

### 解读

- 大市 ETF `2800.HK` 有短线修复迹象，但分数仍低于行动阈值 `65`，且后验记录显示 broad-index ETF 近期有多次 bullish failures；因此不能升级。
- 科技 ETF 的反弹仍属于 MA60 下方的修复，`3033.HK` 量能偏弱，`3067.HK` 分数也未过 watch 阈值；这不足以支持互联网平台或科技单名升级。
- ETF 层面给出的结论是：市场可以观察 risk-on 延续，但没有足够证据支持今日开新仓。

## 4. 突出标的：仅作观察，不作升级

### `0857.HK` 中国石油股份

- 事实：score=`84.42`，`uptrend`，高于 MA20 与 MA60，`ma20_above_ma60`，`volume_ratio_20=1.2356`，`range_pos_60=1.1084`。
- 阻断因素：`symbol_risk_veto`；原因包括低 pass_rate、负 avg_return_pct、出现过 adverse breach 与 `symbol_selection_error`。
- 解读：趋势最强，但后验风险记录不允许升级。能源主题若继续强，需先验证是否有非 veto 标的独立进入 `actionable_candidates`，不能直接用 `0386.HK` 替代。
- 状态：`watch_only`。

### `0941.HK` 中国移动

- 事实：score=`81.98`，`uptrend` + `volume-expansion`，高于 MA20 与 MA60，`volume_ratio_20=1.5041`。
- 阻断因素：`symbol_risk_veto`；历史 pass_rate 极低，且有 adverse breach 与 `symbol_selection_error`。
- 解读：高分红电信是强主题，但最高分标的被风险记录阻断，`0728.HK` 作为同主题 peer 也未进入 action list。
- 状态：`watch_only`。

### `0002.HK` 中电控股

- 事实：score=`76.08`，`uptrend`，高于 MA20 与 MA60，`volume_ratio_20=1.2769`。
- 阻断因素：`symbol_risk_veto`，样本虽少但 pass_rate=`0.000`，avg_return 为负。
- 解读：公用事业主题最稳，但并非可交易信号；更适合作为市场防御需求的温度计。
- 状态：`watch_only`。

### `0388.HK` 香港交易所

- 事实：score=`67.3`，1 日 `+2.99%`，`volume_ratio_20=1.5564`，`range` + `volume-expansion`。
- 阻断因素：`symbol_risk_veto`，且未进入 `actionable_candidates`。
- 解读：如果后续成交额与市场风险偏好继续扩张，`0388.HK` 可作为金融风险偏好的确认标的；今日只能观察。
- 状态：`watch_only`。

### `9618.HK` 京东集团-SW

- 事实：互联网平台内 score 最高，score=`72.27`，`uptrend`，高于 MA20 与 MA60，`range_pos_60=0.7952`。
- 阻断因素：`symbol_risk_veto`，且 `volume_ratio_20=0.7545` 不强；主题 ETF 未确认。
- 解读：它是当前互联网平台最好的模型表达，但规则要求 ETF 确认、peer-relative 改善与 action list 入选；今日不能因为主题内部领先而升级。
- 状态：`watch_only`。

## 5. 风险姿态

### 事实

- `actionable_candidates=[]`。
- Top diagnostic candidates 均 `qualified_for_action=false`。
- 多个高分主题 leader 被 `symbol_risk_veto` 阻断。
- 输入存在 `as_of_date` 与行情日期不一致。
- 稳定规则要求：空 action list 阻止升级；诊断候选只能用于观察；日期不一致时只能低置信度条件观察或 `watch_only`。

### 解读

- 今日风险姿态应为：积极观察、谨慎执行、不开新仓建议。
- 市场短线情绪偏强，但确定性交易层没有通过成本、边际、后验风险与日期质量门槛。
- 最容易犯的错误是把高分诊断候选当成行动候选，或在 leader 被 veto 后从低排名 peer 中机械寻找替代标的。今日应避免这两类错误。

## 6. 今日结论

- 市场状态：`risk_on`，但数据日期不一致削弱信号可信度。
- 最强雷达主题：`utilities-defensive`、`telecom-dividend`、`energy`、`financials-bank`、`financials-exchange`。
- ETF 确认：`2800.HK` 有修复但未达行动阈值；`3033.HK` / `3067.HK` 未确认科技升级。
- 可升级候选：无。
- 推荐状态：全部维持 `watch_only`。
- 时间窗口：14-90 天 swing 观察，但需等待下一次日期对齐数据与 action list 信号。
- 置信度：低到中等；低置信度来自日期不一致与后验 veto，高观察价值来自主题分化清晰。

## 7. 今日高优先级研究问题

1. 下一份日期对齐快照中，`2800.HK` 是否能同时维持 MA60 上方、`volume_ratio_20>1.2`，并带动更多行业上涨？
2. `3033.HK` 与 `3067.HK` 能否收复 MA60，并提供足够 ETF 确认来支持互联网平台单名？
3. `0857.HK`、`0941.HK`、`0002.HK` 的高分是否只是后验风险 veto 下的假阳性，还是需要等待风险记录改善后重新评估？
4. 在 `energy` 与 `telecom-dividend` 内，是否有非 veto peer 能独立进入 `actionable_candidates`，并相对 veto leader 与 recent best peer 展示持续强势？
5. `0388.HK` 的 `volume-expansion` 是否能延续，并转化为港股成交额与金融板块的广泛确认？
