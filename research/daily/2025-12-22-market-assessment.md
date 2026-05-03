# 2025-12-22 港股市场评估

> 研究模式：`recommendation_only`  
> 目标窗口：14-90 天 swing 观察  
> 风险约束：单一标的不超过 10%，主题不超过 30%，不使用杠杆，不使用反向 ETF，不接受低流动性  
> 重要数据质量提示：本次回放的 `as_of_date` 是 `2025-12-22`，但行情字段里的 `quote_trade_date` 是 `2026-04-28`。按稳定规则，日期不一致时，所有结论只能作为低置信度诊断与观察，不能升级为即时行动建议。

## 1. 市场雷达：先看事实

### 1.1 市场状态事实

- 市场雷达给出的整体状态：`risk_off`
- 雷达股票平均 1 日涨跌：-0.946%
- 雷达 ETF 平均 1 日涨跌：-1.847%
- 主要领先标的：
  - `0883.HK`：+1.90%，`energy`，`uptrend`
  - `0857.HK`：+1.83%，`energy`，`uptrend`
  - `2269.HK`：+1.26%，`healthcare-biotech`，但仍标记为 `downtrend` + `volume-expansion`
- 主要落后标的：
  - `1093.HK`：-4.54%，`healthcare-pharma`，`downtrend`
  - `1810.HK`：-3.79%，`consumer-tech`，`downtrend`
  - `1024.HK`：-3.12%，`internet-platform`，`downtrend`

### 1.2 主题强弱事实

按 deterministic ranking 的主题均分排序：

| 排名 | 主题 | 平均分 | 主题领涨/代表 | 代表分数 | 主题状态 |
|---:|---|---:|---|---:|---|
| 1 | `utilities-defensive` | 72.44 | `0006.HK` | 75.51 | 防御、公用事业最强 |
| 2 | `telecom-dividend` | 67.53 | `0941.HK` | 76.46 | 高股息电信较强 |
| 3 | `energy` | 56.81 | `0857.HK` | 81.90 | 能源内部强弱分化，头部很强 |
| 4 | `financials-bank` | 55.08 | `0005.HK` | 55.08 | 趋势尚可但成交确认不足 |
| 5 | `financials-exchange` | 47.16 | `0388.HK` | 47.16 | 区间震荡，观察层级 |
| 6 | `internet-platform` | 16.40 | `9618.HK` | 63.25 | 主题整体弱，只有局部相对强 |
| 7 | `consumer-discretionary` | 15.05 | `2020.HK` | 39.75 | 不达 watch 门槛 |
| 8+ | `hong-kong-broad-market` / `hang-seng-tech` / `consumer-tech` / `financials-insurance` / `healthcare-*` | 0.00 | 多数代表 | 0.00 | 下行或证据不足 |

### 1.3 ETF 确认事实

- `2800.HK`：收 25.98，低于 ma20 25.993 与 ma60 26.36，`downtrend`，得分 0。
- `3033.HK`：收 4.726，低于 ma20 4.7682 与 ma60 4.9981，`downtrend`，得分 0。
- `3067.HK`：收 10.15，低于 ma20 10.238 与 ma60 10.7185，`downtrend`，得分 0。

ETF 层面没有确认风险偏好回升：宽基与恒生科技 ETF 都在均线下方，并且 deterministic ranking 均为 0 分。按规则，这会限制互联网、科技、消费科技等高 beta 单一股票的升级空间。

## 2. 市场雷达：解释与判断

### 2.1 市场结构解释

当前雷达显示的是防御与高股息资产相对占优，而不是全面 risk-on：

- 公用事业、电信、能源靠前；
- 宽基 ETF 与科技 ETF 走弱；
- 互联网平台多数处于 `downtrend` 或低分状态；
- 医药里 `2269.HK` 有单日放量上涨，但趋势仍未修复。

这更像是资金在弱市中寻找稳定现金流、资源股和防御资产，而不是愿意全面承担成长股风险。

### 2.2 风险姿态解释

由于：

1. 市场状态为 `risk_off`；
2. 三个主要 ETF 确认均弱；
3. `actionable_candidates` 为空；
4. 多个高分 diagnostic 标的被 `symbol_risk_veto` 拦截；
5. 本次历史回放存在 `as_of_date` 与 `quote_trade_date` 不一致；

本次不应给出 `buy_candidate`、`accumulate` 或 `hold` 升级。最稳妥状态是 `watch_only`，用强主题定义观察清单，而不是直接推荐介入。

小章鱼今天不伸手抓票，只把礁石的位置记清楚。

## 3. 雷达强主题在交易 universe 内的可执行性

### 3.1 `utilities-defensive`：最强主题，但不能升级

事实：

- 交易 universe 覆盖：`0002.HK`、`0006.HK`
- 主题均分：72.44，为全市场雷达第一
- `0006.HK`：分数 75.51，收 65.25，高于 ma20 63.41 与 ma60 62.3317，`uptrend`，volume_ratio_20 为 1.0304
- `0002.HK`：分数 69.37，收 75.5，高于 ma20 74.4525 与 ma60 73.9485，`uptrend`，但不是主题分数 leader
- `0006.HK` 被 `symbol_risk_veto` 拦截：pass_rate=0.000 over 7 evaluated calls，avg_return_pct=-6.152，并有 adverse breach 与 symbol_selection_error 记录
- `actionable_candidates` 为空

解释：

`utilities-defensive` 是本次最清晰的防御主题。若只看当日趋势，`0006.HK` 是主题内最佳表达；若考虑历史 posterior 风险，`0006.HK` 不能升级。`0002.HK` 技术状态也健康，但被规则标记为 same-theme non-leader，不能机械替代 leader，除非后续出现独立的相对强度、成交和风险证据。

当前结论：`watch_only`。最佳观察表达是 `0006.HK`，备选观察是 `0002.HK`。

### 3.2 `telecom-dividend`：强主题，但 leader 被风险拦截

事实：

- 交易 universe 覆盖：`0941.HK`、`0728.HK`
- 主题均分：67.53
- `0941.HK`：分数 76.46，收 84.65，高于 ma20 81.1925 与 ma60 79.7225，`uptrend`，volume_ratio_20 为 1.0334
- `0728.HK`：分数 58.59，收 5.17，高于 ma20 4.948 与 ma60 5.007，`range`，volume_ratio_20 为 1.3878
- `0941.HK` 被 `symbol_risk_veto` 拦截：pass_rate=0.100 over 10 evaluated calls，avg_return_pct=-0.927，并有 symbol_selection_error 记录
- `0728.HK` 不是主题 leader，不能自动替代

解释：

电信高股息主题有趋势与成交支撑，尤其 `0941.HK` 技术面非常整齐。但 posterior 记录提示过去选择它的结果不好，所以不能因为当前分数高就升级。`0728.HK` 成交确认更强，但趋势结构不如 `0941.HK`，且同主题非 leader。

当前结论：`watch_only`。最佳观察表达是 `0941.HK`，但需要等待风险 veto 解除或同主题相对强弱重新验证。

### 3.3 `energy`：动量最强，但 leader 风险问题最重

事实：

- 交易 universe 覆盖：`0857.HK`、`0883.HK`、`0386.HK`
- 主题均分：56.81
- `0857.HK`：分数 81.90，收 11.67，高于 ma20 10.8135 与 ma60 10.1555，`uptrend`，volume_ratio_20 为 1.2254，range_pos_60 为 1.0769
- `0883.HK`：分数 72.45，收 28.98，高于 ma20 27.27 与 ma60 26.5997，`uptrend`，但 volume_ratio_20 为 0.8064，且不是主题分数 leader
- `0386.HK`：分数 16.09，低于 watch 门槛
- `0857.HK` 被 `symbol_risk_veto` 拦截：pass_rate=0.091 over 11 evaluated calls，avg_return_pct=-13.388，有 adverse breach 与 repeated symbol_selection_error

解释：

能源是本次最有单日价格强度的方向。`0857.HK` 的技术分最高，但它也是风险记录最差的高分候选之一。稳定规则明确：主题 leader 被 veto 不代表放弃整个主题，但替代 peer 必须独立满足趋势、成交、相对强度和风险门槛。`0883.HK` 趋势健康、无 symbol_risk_veto，是更干净的观察对象；但它不是 theme score leader，且成交放大不足，因此只能观察，不能升级。

当前结论：`watch_only`。若必须选择能源主题的当前最佳观察表达，我会把 `0883.HK` 列为“更干净的替代表达”，把 `0857.HK` 列为“分数最高但风险 veto 阻断”。

### 3.4 `financials-bank` 与 `financials-exchange`：可观察但不强

事实：

- `0005.HK`：分数 55.08，`uptrend`，价格高于 ma20 与 ma60，但 volume_ratio_20 只有 0.507，被 `low_volume_ratio_20_below_0_6` 拦截
- `0388.HK`：分数 47.16，`range`，价格略高于 ma20 和 ma60，但被 `symbol_risk_veto` 拦截

解释：

金融板块不是当前最差方向，但也不是最清晰的 swing 机会。`0005.HK` 缺成交确认，`0388.HK` 有风险 veto，且两者都低于 action score。

当前结论：`watch_only`。没有升级候选。

### 3.5 `internet-platform`：交易 universe 覆盖充分，但 ETF 与主题均不确认

事实：

- 交易 universe 覆盖：`0700.HK`、`9988.HK`、`3690.HK`、`1024.HK`、`9618.HK`
- 主题均分：16.40，整体弱
- 主题 leader：`9618.HK`，分数 63.25，低于 action score 65
- `9618.HK` 虽为 `uptrend`，但被 `symbol_risk_veto` 拦截，且 below_action_score
- `0700.HK`、`9988.HK`、`1024.HK` 均为 `downtrend`
- `3033.HK` 与 `3067.HK` 均为 `downtrend`，恒生科技 ETF 没有确认

解释：

互联网平台不能升级。这里最容易犯错：看到某个单名相对强，就忽略 ETF 与主题整体偏弱。稳定规则要求，在低 pass-rate 与 ETF 不确认时，不能把单一互联网股票升为 `buy_candidate`、`hold` 或 `accumulate`。

当前结论：全部 `watch_only`。主题内相对最强观察对象是 `9618.HK`，但不是行动对象。

### 3.6 `consumer-discretionary`、`consumer-tech`、`healthcare-*`：暂不构成可交易强主题

事实：

- `consumer-discretionary` 主题均分 15.05，leader `2020.HK` 只有 39.75，低于 watch 门槛
- `1810.HK` 得分 0，`downtrend`，单日 -3.79%，并有 `symbol_risk_veto`
- `2269.HK` 单日 +1.26%，volume_ratio_20 为 1.5616，但仍是 `downtrend`，得分 0
- `1177.HK` 与 `1093.HK` 均为 `downtrend`，得分 0

解释：

`2269.HK` 的放量上涨值得记录，但这是下跌趋势中的单日异动，不是趋势修复。消费与医药方向缺少主题级确认，也缺少 ETF 或同类扩散确认。

当前结论：`watch_only`，不升级。

## 4. 外部机会说明

本次雷达强主题都在 trade universe 中有覆盖：

- `utilities-defensive`：`0002.HK`、`0006.HK`
- `telecom-dividend`：`0941.HK`、`0728.HK`
- `energy`：`0857.HK`、`0883.HK`、`0386.HK`

因此没有“雷达强但 trade universe 完全未覆盖”的主题需要立即标记为外部机会。后续如果要扩展 universe，可以优先考虑增加更多高股息、防御、公用事业、能源链相关港股或 ETF，用来验证这些主题是否只是个别大盘股强，还是板块扩散。

## 5. 今日 standout names

> 注意：以下为观察名单，不是行动推荐。`actionable_candidates` 为空，禁止升级。

### `0883.HK` — 能源主题的较干净观察表达

- 事实：+1.90%，收 28.98，高于 ma20 与 ma60，`uptrend`，无 `symbol_risk_veto`。
- 解释：虽然不是能源主题分数 leader，但比 `0857.HK` 的 posterior 风险更干净。若能源继续强，它可能是后续优先复核对象。
- 当前状态：`watch_only`
- 观察触发：继续站稳 ma20/ma60，成交改善，且相对 `0857.HK` 不再明显落后。
- 失效条件：跌回 ma20 下方，或能源主题从 leader 列表消失。
- 信心：低到中；原因是日期不一致与 actionable layer 为空。

### `0002.HK` — 公用事业主题的替代观察对象

- 事实：分数 69.37，收 75.5，高于 ma20 与 ma60，`uptrend`，无 `symbol_risk_veto`。
- 解释：`0006.HK` 是主题 leader 但被 risk veto；`0002.HK` 技术结构健康，但作为同主题非 leader 不能自动升级。
- 当前状态：`watch_only`
- 观察触发：相对 `0006.HK` 出现持续强势，成交改善，且主题仍维持第一梯队。
- 失效条件：跌破 ma20，或公用事业主题均分明显回落。
- 信心：低到中。

### `0728.HK` — 电信主题的成交观察对象

- 事实：分数 58.59，收 5.17，高于 ma20 与 ma60，volume_ratio_20 为 1.3878，但 regime 是 `range`，非主题 leader。
- 解释：`0941.HK` 技术更强但被 risk veto；`0728.HK` 成交更强，却还没有趋势 leader 地位。
- 当前状态：`watch_only`
- 观察触发：从 `range` 转向 `uptrend`，并持续强于 `0941.HK`。
- 失效条件：跌回 ma20/ma60 下方，或电信主题不再领先。
- 信心：低。

### `9618.HK` — 互联网平台内部唯一相对强者，但不能升级

- 事实：分数 63.25，`uptrend`，高于 ma20 与 ma60，但 below_action_score，且被 `symbol_risk_veto` 拦截。
- 解释：它是弱主题中的相对强者，不是强主题中的行动候选。科技 ETF 没有确认，所以不能追。
- 当前状态：`watch_only`
- 观察触发：恒生科技 ETF 重新站上 ma20/ma60，互联网主题均分改善，且 `9618.HK` risk veto 不再阻断。
- 失效条件：跌破 ma20，或主题内相对强度转弱。
- 信心：低。

## 6. 推荐状态汇总

| 标的 | 主题 | 当前状态 | 主要理由 | 升级阻碍 |
|---|---|---|---|---|
| `0883.HK` | `energy` | `watch_only` | 能源强、趋势健康、无 risk veto | 非主题分数 leader，成交未明显放大，actionable 为空 |
| `0002.HK` | `utilities-defensive` | `watch_only` | 防御主题最强、趋势健康、无 risk veto | 非主题分数 leader，需证明相对 `0006.HK` 改善 |
| `0728.HK` | `telecom-dividend` | `watch_only` | 电信主题强、成交确认较好 | 非主题 leader，regime 仍是 `range` |
| `9618.HK` | `internet-platform` | `watch_only` | 互联网内部相对最强 | 主题弱、ETF 弱、below_action_score、risk veto |
| `2800.HK` / `3033.HK` / `3067.HK` | ETF | `watch_only` | 用作确认工具 | 均处 `downtrend`，得分 0 |

本次没有 `buy_candidate`。原因不是没有强标的，而是 deterministic action layer 没有给出任何 `actionable_candidates`，而且多个高分候选在 posterior 风险或日期一致性上不过关。

## 7. 风险与失效框架

### 7.1 主要风险

- 数据日期风险：`as_of_date` 与 `quote_trade_date` 不一致，使本次只能作为历史诊断。
- 市场状态风险：`risk_off` 中，高分防御股可能只是避险拥挤，而不是低风险买点。
- 主题拥挤风险：公用事业、电信、能源已处 60 日区间较高位置，追高容易遇到回撤。
- posterior 风险：`0857.HK`、`0941.HK`、`0006.HK` 虽为 diagnostic top 3，但都被 `symbol_risk_veto` 拦截。
- ETF 确认缺失：宽基与科技 ETF 不支持成长股升级。

### 7.2 统一失效条件

若后续出现以下任一情况，今日观察框架失效：

1. `2800.HK`、`3033.HK`、`3067.HK` 继续下破并扩大跌幅，说明风险偏好进一步恶化；
2. 防御主题 leader 跌回 ma20 下方，说明避险交易也开始松动；
3. 能源主题由领涨转为领跌，说明当前强势是短线冲高；
4. 被观察的替代标的无法跑赢被 veto 的 theme leader，说明替代表达不成立；
5. 日期对齐后的数据不支持本次排名。

## 8. 今日高优先级研究问题

1. `as_of_date=2025-12-22` 与 `quote_trade_date=2026-04-28` 的错位来自数据生成流程、快照读取，还是 replay 输入拼接？在修复前，所有历史回放结论应如何统一降级？
2. 对 `energy` 主题，`0883.HK` 是否能在未来 3-5 个交易日持续跑赢 `0857.HK`？如果能，是否可以建立“risk-vetoed leader 的同主题替代表达”条件规则？
3. 对 `utilities-defensive`，`0002.HK` 是否能提供比 `0006.HK` 更稳定的 posterior 表现？如果能，当前 theme leader 机制是否过度偏向短期分数？
4. `0941.HK` 的 `symbol_risk_veto` 主要来自选股错误、入场时机错误，还是主题判断错误？需要拆分后再决定是否永久降权。
5. 互联网平台里 `9618.HK` 的相对强度是真改善，还是弱主题中的低质量反弹？必须等 `3033.HK` / `3067.HK` 至少重新站上 ma20 后再复核。
