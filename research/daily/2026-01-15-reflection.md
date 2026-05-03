# 2026-01-15 投资复盘反思（historical）

## 结论摘要

今天的回放输入显示表面为 `risk_on`：股票平均涨幅约 1.606%，ETF 平均涨幅约 1.7%，领涨集中在 `3690.HK`、`9988.HK`、`0388.HK`。但本轮不能升级为行动建议，核心原因不是分数不够，而是证据链断裂：

- `actionable_candidates=[]`，直接阻断所有升级。
- 前三名动态诊断候选 `0857.HK`、`0941.HK`、`0002.HK` 均为 `diagnostic_only=true`，且 `qualified_for_action=false`。
- 三者虽然分数高、趋势强，但均被 `symbol_risk_veto` 拦截。
- 回放 `as_of_date=2026-01-15`，但快照内报价日期为 `2026-04-29`，存在明显日期不对齐；这些排名只能作为审计材料，不能当作当日实时确认。
- 参数优化没有晋级 active strategy：样本、改善、胜率、不利波动与样本质量门槛均未共同通过，不能降低现有行动门槛。

因此今日建议状态应保持为：**全市场观察 / veto 审计 / peer-relative 复核，不做 `buy_candidate`、`hold`、`accumulate` 或 `avoid` 升级。**

## 今日证据与解释

### 市场与主题

市场短线表现偏强，防御、公用事业、电信、能源和金融板块排名靠前：

- `energy`：主题均分 69.67，leader `0857.HK` 分数 84.42。
- `telecom-dividend`：主题均分 75.00，leader `0941.HK` 分数 81.98。
- `utilities-defensive`：主题均分 75.47，leader `0002.HK` 分数 76.08。
- `financials-exchange`：`0388.HK` 分数 67.30，且有 `volume-expansion`。

但这些主题强度没有转化为行动候选。`0857.HK`、`0941.HK`、`0002.HK` 都被历史风险否决；`0388.HK`虽然当日表现强、成交放大，但也有 `symbol_risk_veto`，且样本 pass_rate 为 0。低排名的 `0386.HK`、`3690.HK`、`2331.HK`、`9992.HK` 等即使部分没有 veto，也没有进入 `actionable_candidates`，不能被挖出来替代前排被 veto 的 leader。

### 动态选股错误分类

本轮使用了动态 trade universe ranking，因此需要提前分类可能的未来错误：

1. **risk-control error**：如果忽略 `actionable_candidates=[]`、`diagnostic_only=true`、`qualified_for_action=false` 或 `symbol_risk_veto`，把 `0857.HK`、`0941.HK`、`0002.HK` 升级为行动建议，就是风险控制错误。
2. **symbol-selection error**：互联网平台主题的近期 posterior 显示多次 selected-vs-best 错误，尤其 `0700.HK`、`9988.HK` 多次落后 `9618.HK`、`9988.HK`、`3690.HK` 或 `1024.HK` 等同主题 best peer。若下次只因当前分数或熟悉度继续选择旧 leader，而不列出最近 best peer 与 `selected_vs_best_bps`，就是选股错误。
3. **timing error**：若把单日 `risk_on` 反弹等同于 T+3/T+5 可交易窗口已改善，尤其在报价日期不对齐、ETF确认不足、历史 T+3/T+5 失误集中的情况下，容易重复短线时点错误。

## 信心最弱的位置

信心最弱的不是“市场是否短线反弹”，而是以下四点：

- **日期一致性**：`as_of_date` 与实际 `quote_trade_date` 不一致，导致任何技术分数都不能直接解释 2026-01-15 当天环境。
- **行动资格**：所有前排候选只是诊断队列，`actionable_candidates` 为空。
- **风险模型与 posterior 的冲突处理**：不少标的看起来趋势强，但历史 pass_rate 很低或有 repeated symbol-selection errors，不能用当日分数覆盖长期负证据。
- **peer-relative 选择质量**：互联网平台主题近期多次不是主题方向完全错，而是选错同主题表达；如果只降级整个主题，而不要求“证明相对最近 best peer 改善”，学习会不够精确。

## 仍然缺失的证据

升级前仍需补齐：

1. 日期对齐的 2026-01-15 行情、成交量、MA20/MA60、ETF 与个股数据。
2. 非空且日期对齐的 `actionable_candidates`。
3. 对前排被 veto 标的的风险复核：是否有足够新样本推翻 `low_symbol_pass_rate`、`negative_symbol_avg_return`、`recent_symbol_adverse_breach` 或 `repeated_symbol_selection_error`。
4. 同主题 peer-relative 表：至少列出最近 T+3/T+5/T+10 的 best peer、peer median、`selected_vs_best_bps`。
5. ETF 或广义主题确认，特别是互联网平台与恒生科技相关标的，不能只看单一个股反弹。
6. 参数优化的晋级证据：样本质量、改善幅度、胜率和 adverse gate 需要共同改善后，才允许调整门槛。

## 今日建议与失效条件

### 总体状态：`watch_only`

- 理由：`actionable_candidates=[]`，前三诊断候选均被 `symbol_risk_veto`，且报价日期不对齐。
- 时间周期：下一次日期对齐数据与行动清单生成前。
- 失效条件：出现日期对齐的非空 `actionable_candidates`，且候选同时满足无 veto、成交确认、趋势确认、ETF/主题确认和 peer-relative 改善。
- 信心：中等；对“不行动”的信心高于对任何方向判断的信心。

### 审计队列

- `0857.HK`：趋势与动量分数最高，但 pass_rate 低、平均回报为负且有 adverse breach / selection error，不能行动。
- `0941.HK`：趋势强且成交放大，但 pass_rate 极低并有 repeated selection error，不能行动。
- `0002.HK`：防御主题 leader，但样本 pass_rate=0、平均回报为负；只能观察。
- `0388.HK`：量价改善明显，但 posterior pass_rate=0 且有 veto；需要更多日期对齐样本。
- `9618.HK`：互联网平台当前排名 leader，但仍有 `symbol_risk_veto`；若未来要重评互联网主题，必须和最近 best peer 做明确比较。

## 1-3 个最可能失败模式

1. **把诊断分数当行动信号**：看到 `0857.HK`、`0941.HK`、`0002.HK` 高分后忽略 veto 与空行动清单。
2. **用非日期对齐快照解释历史当天**：把 2026-04-29 报价生成的指标错误套到 2026-01-15 的决策环境。
3. **继续重复 selected-vs-best 错误**：互联网平台或其他主题重选时，只看当前 leader，而没有证明相对最近实际 best peer 的改善。

## 下一周期优先级调整

1. **先修数据门槛**：所有升级讨论前先验证 `as_of_date`、`quote_trade_date`、MA来源和成交来源一致。
2. **先看 action list，再看 diagnostic list**：`actionable_candidates=[]` 时，输出审计和等待条件，不挖替代标的。
3. **把 veto 审计排在主题替代之前**：leader 被 veto 后，不自动换同主题 peer；替代者必须进入 action list，并跑赢 veto leader 与最近 best peer。
4. **互联网平台重点做 peer-relative 复盘**：下一轮必须列出 `0700.HK`、`9988.HK`、`9618.HK`、`3690.HK`、`1024.HK` 的近期 best peer 与 `selected_vs_best_bps`。
5. **参数优化保持保守**：challenger 未满足晋级条件前，不降低 cost gate、edge gate 或风险否决标准。
