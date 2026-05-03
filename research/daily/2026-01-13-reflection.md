# 2026-01-13 投资复盘反思

## 结论摘要

本轮 historical replay 的主结论是：今天不应给出任何行动升级，所有动态候选只能作为 `watch_only` / 诊断审计对象。虽然快照显示市场处于 `risk_on`，平均股票涨幅约 1.606%、ETF 涨幅约 1.7%，并且能源、电信红利、公用事业等主题在趋势分数上靠前，但 `actionable_candidates=[]`，前三个 `diagnostic_candidates`（`0857.HK`、`0941.HK`、`0002.HK`）全部被 `symbol_risk_veto` 拦截。按照现有规则，这不是从低排名标的里继续挖替代品的环境，而是 veto 审计与同主题 peer-relative 复核周期。

同时，输入存在明显日期不一致：`as_of_date=2026-01-13`，但行情字段中的 `quote_trade_date=2026-04-29`。因此这些价格、均线和成交量只能作为历史回放生成器的诊断材料，不能当作 2026-01-13 的实时确认。

## 今日证据与解释

### 市场与主题

- 表面市场状态为 `risk_on`，多数标的上涨，领先者包括 `3690.HK`、`9988.HK`、`0388.HK`。
- 主题分数较强的是 `utilities-defensive`、`telecom-dividend`、`financials-bank`、`energy`，但这些主题的最高分标的多被后验风险 veto 拦截。
- `hang-seng-tech` 平均分只有 43.52，且 `3067.HK`、`3033.HK` 均低于 watch 阈值；互联网平台主题平均分更低，尽管 `9618.HK` 当前排名较好，也被 `symbol_risk_veto` 拦截。

### 动态选择结果

- `0857.HK`：分数 84.42，趋势与动量都强，但 `symbol_risk_veto=true`，原因包括低 pass_rate、负平均回报、历史不利突破和重复 `symbol_selection_error`。结论：`watch_only`，不得行动升级。
- `0941.HK`：分数 81.98，趋势强且成交放大，但 pass_rate 仅 0.033，且存在近期不利突破与选择错误。结论：`watch_only`。
- `0002.HK`：分数 76.08，但样本 pass_rate=0.0、平均回报为负。结论：`watch_only`。
- `0386.HK` 与 `3690.HK` 虽然 `symbol_risk_veto=false`，但它们不在 `actionable_candidates`，且分别存在非主题 leader、趋势/均线或行动分数不足问题；不能因为前排被 veto 就机械替代。

## 信心最弱的位置

1. **日期对齐信心最弱**：`as_of_date` 与 `quote_trade_date` 冲突，使所有价格确认、均线位置、成交量确认都降级为审计信息。
2. **动态选择信心弱**：后验摘要显示 `symbol_selection_error=145`，且近期互联网平台 selected-vs-best 错误持续出现；动态 leader 分数不能替代 peer-relative 证明。
3. **短期时点信心弱**：近期 `2800.HK`、`9988.HK`、科技 ETF 的 T+3/T+5 失败较多，说明即使方向判断有时不差，入场窗口仍容易过早。
4. **参数优化信心弱**：参数优化未更新 active strategy，原因包括 samples、improvement、win_rate、sample_quality 等门槛未过；不能把 challenger 的表面得分当成策略升级依据。

## 仍缺失的证据

- 日期对齐的 2026-01-13 当日行情、成交量、均线与主题 ETF 确认。
- 对 `0857.HK`、`0941.HK`、`0002.HK` 的 veto 原因复核：哪些失败来自择时、哪些来自标的选择、哪些来自主题误判。
- 同主题 peer-relative 证据：例如能源中 `0857.HK` 相对 `0883.HK`、`0386.HK` 是否真有新鲜强势；电信红利中 `0941.HK` 相对 `0728.HK` 是否只是高分但历史选择差。
- 广度与 ETF 确认：`2800.HK`、`3033.HK`、`3067.HK` 没有提供足够的日期对齐确认来支持单股升级。
- 低排名、非 veto peer 的独立行动证据：尤其是 `0386.HK`、`3690.HK`，需要同时满足行动清单、成交、趋势、相对强度和风险门槛。

## 今日建议状态

- 总体建议：`watch_only`。
- 不升级任何 `diagnostic_candidates`。
- 不从低排名同主题 peer 中寻找替代行动标的。
- 将 `0857.HK`、`0941.HK`、`0002.HK` 作为 veto 审计队列，而非买入候选。
- 对 `0386.HK`、`3690.HK` 仅做复核观察：只有在日期对齐数据中进入 `actionable_candidates`，并证明相对被 veto leader 与最近 best peer 的新鲜强势后，才可重新讨论升级。

## 可能失败模式

1. **risk-control error**：忽略 `actionable_candidates=[]` 和 `symbol_risk_veto`，把高分诊断候选误当作行动信号。
2. **symbol-selection error**：在 `0857.HK`、`0941.HK` 被 veto 后，机械切换到同主题低排名 peer，而没有证明相对 veto leader 和最近 best peer 的强势。
3. **timing error**：在非日期对齐的 `risk_on` 反弹中追入，随后 T+3/T+5 继续出现回撤或横盘，重演近期 `2800.HK`、`9988.HK` 的短窗失败。

本次动态符号选择的潜在未来错误分类：主风险是 **risk-control error** 与 **symbol-selection error**，次要风险是 **timing error**。暂不判定为纯粹 **theme error**，因为主题强弱本身还有待日期对齐证据确认。

## 下一周期优先级调整

1. **先做数据审计**：确认 `as_of_date` 与报价日期一致后，再使用均线、成交量和排名。
2. **先审 top veto，不挖替代**：对 `0857.HK`、`0941.HK`、`0002.HK` 的 veto 原因做拆解；在 veto 未解释前，不寻找低排名行动替代。
3. **peer-relative 复核前置**：任何同主题升级必须同时比较当前 leader、被 veto leader、最近 best peer，并给出新鲜相对强势证据。
4. **ETF 与广度确认优先于单股分数**：尤其是互联网平台与科技 ETF，若 `3033.HK`、`3067.HK` 未重新站稳 MA60 且成交确认不足，单股只能维持 `watch_only`。
5. **参数优化保持保守**：在样本质量仍是 `relaxed_fallback`、平均净回报为负、win_rate 偏低时，不根据 challenger 结果调整 active strategy。
