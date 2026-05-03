# 2026-01-19 投资复盘反思（historical）

## 结论摘要
今天的输入显示市场表面为 `risk_on`：ETF 平均涨幅约 1.70%，股票平均涨幅约 1.61%，涨幅领先者包括 `3690.HK`、`9988.HK`、`0388.HK`。但本轮动态排名的关键结论不是“寻找替代买点”，而是“风险 veto 审计”：`actionable_candidates=[]`，前三个 `diagnostic_candidates`（`0857.HK`、`0941.HK`、`0002.HK`）全部被 `symbol_risk_veto` 拦截。因此，今天所有动态候选最多只能作为 `watch_only` / audit 队列，不能升级为 `buy_candidate`、`hold` 或 `accumulate`。

另一个重大限制是数据日期错位：回放 `as_of_date=2026-01-19`，但快照中的 quote 字段显示 `quote_trade_date=2026-04-29`。这使任何短线价格强度、成交量放大和均线位置都只能作为诊断材料，不能当作 2026-01-19 当日的可行动证据。

## 信心最弱的地方
1. **日期对齐信心最弱**：`as_of_date` 与 quote 日期不一致，导致当日涨跌、成交量、MA20/MA60 与 `range_pos_60` 的可用性明显下降。
2. **行动候选信心最弱**：尽管 `0857.HK`、`0941.HK`、`0002.HK` 分数高且趋势指标强，但全部是 `diagnostic_only=true`、`qualified_for_action=false`，且有 `symbol_risk_veto`。
3. **同主题替代信心不足**：`0386.HK` 虽然 `symbol_risk_veto=false`，但只是 energy 主题第 3 名，未进入 `actionable_candidates`，且没有证明相对被 veto 的 `0857.HK` 或最近 best peer 的新鲜强势。
4. **短线 timing 信心不足**：posterior 显示大量 T+3/T+5 misfire，尤其是 `2800.HK`、`9988.HK`、科技 ETF 与互联网平台股；今天不能把单日反弹理解成可靠跟随。

## 仍然缺失的证据
- 日期对齐的 2026-01-19 收盘价、成交量、MA20/MA60、ETF 广度与行业广度。
- `0857.HK`、`0941.HK`、`0002.HK` 的 veto 解除条件：至少需要 pass_rate、平均回报、adverse breach 与 selection-error 记录改善，而不是只看当前 trend_score。
- 同主题 peer-relative 证据：需要列出最近 T+3/T+5/T+10 的 best peer、`selected_vs_best_bps`，并证明候选相对 best peer 改善超过成本门槛与 `minimum_edge_bps`。
- broad/ETF confirmation：特别是 `2800.HK`、`3033.HK`、`3067.HK` 是否同步站稳 MA60、放量，并能支持单名互联网平台股升级。
- 参数优化证据：当前 challenger 未通过 samples、improvement、win_rate、adverse、sample_quality 等晋级门槛，不能用来降低行动门槛。

## 今日建议状态
- `0857.HK`：`watch_only` / veto audit。分数 84.42、趋势强，但 `symbol_risk_veto=true`，历史 pass_rate 低、平均回报为负，并有 adverse breach 与 selection error。
- `0941.HK`：`watch_only` / veto audit。分数 81.98、量能放大，但 `symbol_risk_veto=true`，历史 pass_rate 极低且存在 adverse breach。
- `0002.HK`：`watch_only` / veto audit。分数 76.08、防御主题强，但样本 pass_rate=0，仍被 veto。
- `9618.HK`、`0005.HK`、`0388.HK`、`2800.HK` 等：只作为观察名单。即使部分分数或主题排名尚可，也没有进入行动清单或存在 veto/日期错位/ETF 确认不足问题。
- `0386.HK`、`3690.HK`、`2331.HK`、`9992.HK`、`2269.HK` 等低排名或非 veto peer：只做审计，不做替代行动候选。

## 可能的失败模式
1. **risk-control error**：看到 `risk_on` 与高 trend_score 后忽略 `actionable_candidates=[]` 和 `symbol_risk_veto`，把诊断候选误升为行动建议。
2. **symbol-selection error**：在 veto leader 被拦截后，从同主题低排名 peer 中机械寻找替代，而没有证明其跑赢 veto leader 与最近 best peer。
3. **timing error**：把单日反弹或量价改善当成 T+3/T+5 可延续信号，重复近期短窗 misfire。

## 动态选股错误分类
今天的候选来自动态 symbol selection。若未来出错，最可能不是单纯 `theme_error`，而是：
- **risk-control error**：行动清单为空且 veto 生效时仍升级。
- **symbol-selection error**：没有验证 selected-vs-best 与同主题 peer-relative 改善。
- **timing error**：在日期错位和短窗 misfire 背景下高估短线跟随。

`theme_error` 也可能存在，但当前更重要的是不要把主题强度误读为个股可行动性。

## 下一周期优先级
1. **先修正数据链**：确保 `as_of_date`、quote 日期、均线和成交量全部日期对齐；未对齐时默认 `watch_only`。
2. **先做 veto 审计，不做替代挖掘**：前三诊断候选全部被 veto 且 `actionable_candidates=[]`，下一轮重点解释 veto 是否仍有效，而不是寻找低排名 peer。
3. **强制 peer-relative 表格**：对 energy、telecom-dividend、utilities-defensive、internet-platform 输出最近 best peer、selected peer、`selected_vs_best_bps`、T+3/T+5/T+10 表现。
4. **保持成本和行动门槛**：参数优化未晋级，不降低 `cost_gate.minimum_edge_bps=100.0`，不绕过 `symbol_risk_veto`。
5. **ETF 先行确认**：互联网平台和科技相关单名必须等待 `3033.HK` / `3067.HK` 与 `2800.HK` 的广度、量能、MA60 共同改善。

## 记忆更新判断
posterior 中 `symbol_selection_error=152`、`timing_unclear=108`、`theme_error=85`，且近期 selected-vs-best 错误密集出现。长期规则已经覆盖大部分模式；本次只补充一条更具体的操作约束：`risk_on` 市场标签不能覆盖空行动清单、日期错位或 veto。
