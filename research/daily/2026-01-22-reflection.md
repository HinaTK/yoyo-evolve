# 2026-01-22 投资复盘（historical）

## 结论

今天的输出应保持为 `watch_only` / audit-only，不应给出新的 `buy_candidate`。虽然快照里的市场状态是 `risk_on`，平均股票与 ETF 单日表现均为正，且能源、电讯股息、公用事业等主题分数靠前，但决定性约束更强：`actionable_candidates=[]`、排名来自非日期对齐 quote、且前三个 diagnostic candidates（`0857.HK`、`0941.HK`、`0002.HK`）全部被 `symbol_risk_veto` 阻断。因此本轮更像一次风控审计与同主题相对强弱复核，而不是交易升级窗口。

## 事实与解释

### 事实

- 市场摘要为 `risk_on`，ETF 平均单日涨幅约 1.7%，股票平均单日涨幅约 1.606%。
- `actionable_candidates=[]`。
- top diagnostic candidates：
  - `0857.HK`：score 84.42，趋势与动量强，但 `symbol_risk_veto=true`，33 次评估 pass_rate=0.091，平均回报为负，并有 adverse breach 与 `symbol_selection_error` 记录。
  - `0941.HK`：score 81.98，趋势强且放量，但 `symbol_risk_veto=true`，30 次评估 pass_rate=0.000，平均回报为负，并有 adverse breach 与 `symbol_selection_error`。
  - `0002.HK`：score 76.08，但 `symbol_risk_veto=true`，3 次评估 pass_rate=0.000，平均回报为负。
- `2800.HK` 只达到 watch 分数，且近期有多次 T+3/T+5 失效；不能作为被 veto 个股后的默认 fallback。
- 互联网平台内部仍存在严重 selected-vs-best 问题：`0700.HK`、`9988.HK` 多次落后 `9618.HK`、`3690.HK`、`1024.HK` 等同主题 best peer。
- 参数优化没有通过 samples、improvement、win_rate、sample_quality 等 gate，active strategy 不应切换。

### 解释

今天的强势更偏“局部顺周期与高股息/防守主题的技术延续”，但已有后验记录显示这些高分 leader 并不可靠：高分不能抵消历史胜率低、平均收益为负、adverse breach、以及反复选错同主题标的。当前最重要的研究任务不是寻找替代交易，而是识别为什么模型在主题 leader、ETF fallback 与互联网平台内部选择上持续失真。

## 今日建议状态

- 总体状态：`watch_only` / audit-only。
- 不升级任何 diagnostic candidate。
- 不从低排名同主题 peer 中挖替代行动标的。
- 不把 `2800.HK` 作为风险较低的默认替代。
- 若下一周期考虑升级，必须先满足：日期对齐 quote、进入 `actionable_candidates`、`qualified_for_action=true`、通过 cost/edge/risk gates，并给出相对近期 best peer 的 fresh relative strength。

## 信心最弱的位置

1. **非日期对齐数据造成的判断偏差**：当前 snapshot 的 `as_of_date` 是 2026-01-22，但 quote 字段显示 2026-04-29；因此所有价格结构只能作为条件审计，不能作为当日交易确认。
2. **高分但被 veto 的 leader 是否真的不可用**：`0857.HK`、`0941.HK`、`0002.HK` 的技术分数很高，但后验表现很弱；目前只能相信 veto，不能用单日形态覆盖长期错误记录。
3. **互联网平台主题的最佳表达不稳定**：近期 best peer 在 `9618.HK`、`9988.HK`、`3690.HK`、`1024.HK` 间切换，单纯选择分数 leader 仍可能继续产生 symbol-selection error。

## 仍缺失的证据

- 2026-01-22 当日真正日期对齐的 OHLCV、成交量与均线数据。
- top diagnostic candidates 在 T+3/T+5 的同主题 peer-relative 表现，尤其是 high-score leader 是否继续落后第二梯队。
- `0857.HK`、`0941.HK`、`0002.HK` 被 veto 后，是否存在独立进入 `actionable_candidates` 且相对近期 best peer 改善的同主题替代品。
- `2800.HK` 在最近失效后是否重新通过 date-aligned edge gate，而不是只因市场 `risk_on` 被动升级。
- 参数 challenger 的高质量样本与真实改善证据；当前 relaxed_fallback 样本不足以支持策略切换。

## 可能失败模式

1. **risk-control error**：看到 `risk_on` 和高分 leader 后忽略 `actionable_candidates=[]`、`diagnostic_only=true`、`qualified_for_action=false` 与 `symbol_risk_veto`。
2. **symbol-selection error**：在 leader 被 veto 后，从同主题低排名 peer 中选择“看起来干净”的替代品，却没有证明它相对 veto leader 与近期 best peer 有 fresh relative strength。
3. **timing error**：把非日期对齐 quote 当成 2026-01-22 的当日确认，导致在历史回放里提前或滞后升级。

## 动态选股错误分类

本轮排名来自动态 trade universe selection，但没有任何标的进入 `actionable_candidates`。若仍强行推荐，最可能的未来错误分类为：

- `symbol-selection error`：尤其是能源、电讯、公用事业 leader 被高分吸引，但后验 pass_rate 与平均收益不支持行动。
- `timing error`：非日期对齐 quote 使入场时点失真。
- `risk-control error`：忽略 veto 与 action gate，把 radar-only 信号误读为行动信号。

## 下一周期优先级调整

1. **先做 veto audit**：逐一检查 `0857.HK`、`0941.HK`、`0002.HK` 的 veto 是否由可复现的后验劣势驱动，避免高分重复诱导。
2. **强化同主题 best peer 规则**：任何互联网平台升级必须明确近期 best peer，并证明相对 `9618.HK`、`3690.HK`、`1024.HK` 或当前滚动 best peer 的 fresh relative strength。
3. **ETF 只做确认，不做 fallback**：`2800.HK` 与恒科 ETF 必须重新通过日期对齐 edge gate；不得因为单日 risk-on 或个股 veto 自动降级为 ETF 交易。
4. **暂停参数切换**：在 samples、improvement、win_rate、sample_quality 未通过前，保持 `l5_mvp_conservative_v1`，并把 challenger 仅作为离线诊断。
