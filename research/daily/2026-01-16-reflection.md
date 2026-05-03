# 2026-01-16 投资复盘（historical）

## 结论

今天只能形成低置信度的 `watch_only` / 审计结论，不形成任何可行动升级。核心原因不是市场没有强势线索，而是行动门槛没有通过：`actionable_candidates=[]`，前排动态候选 `0857.HK`、`0941.HK`、`0002.HK` 全部被 `symbol_risk_veto` 拦截；同时输入存在 `as_of_date=2026-01-16` 但报价字段为 `2026-04-29` 的日期不一致，历史回放中的排名只能作为诊断材料，不能当作日期对齐的现场确认。

市场快照显示 `risk_on`，平均 ETF 日涨幅约 1.70%，平均股票日涨幅约 1.606%。领涨来自 `3690.HK`、`9988.HK`、`0388.HK`，说明风险偏好有修复；但排名系统真正打分靠前的是能源、电讯、公用事业等高趋势/防御收益类资产，而不是互联网平台。这个分歧本身降低了方向判断的清晰度。

## 事实与解释

### 事实

- `actionable_candidates` 为空，禁止把任何诊断候选升级为 `buy_candidate`、`hold` 或 `accumulate`。
- 前三名诊断候选：
  - `0857.HK`：score 84.42，趋势强、量能确认，但 `symbol_risk_veto=true`，历史 pass_rate 0.121，平均回报为负，并有 adverse breach 与 selection error 记录。
  - `0941.HK`：score 81.98，趋势强且放量，但 `symbol_risk_veto=true`，历史 pass_rate 0.033，并有 adverse breach 与 selection error 记录。
  - `0002.HK`：score 76.08，趋势和区间位置较好，但 `symbol_risk_veto=true`，历史 pass_rate 0.000，平均回报为负。
- `0857.HK`、`0941.HK`、`0002.HK` 虽然 `qualified_for_watch=true`，但均为 `diagnostic_only=true` 且 `qualified_for_action=false`。
- `0386.HK` 的 `symbol_risk_veto=false`，但只是 energy 主题第三名，未进入行动清单，且不是主题 leader；按规则只能审计，不能作为 `0857.HK` 的机械替代。
- 互联网平台内部，`9618.HK` 是当前主题 leader 且 score 72.27，但同样被 `symbol_risk_veto` 拦截；`9988.HK` 和 `3690.HK` 当日涨幅较强，却低于 watch/action 分数或存在均线、相对强弱、主题非 leader 等限制。
- 参数优化没有晋级 active strategy：samples、improvement、win_rate、adverse、sample_quality 等门槛未通过，因此不能降低 cost/edge/risk gates。

### 解释

这是一轮“强势线索存在，但风控否决更强”的回放。若只看趋势分数，会被 `0857.HK`、`0941.HK`、`0002.HK` 吸引；若只看当日涨幅，会被 `3690.HK`、`9988.HK`、`0388.HK` 吸引。但稳定规则要求先看行动清单、日期对齐、风险否决、同主题 peer-relative 证据。四个条件中至少三个不满足，所以正确动作是记录观察条件，而不是寻找替代买点。

## 今日建议状态

- 总体：`watch_only`
- 不升级任何诊断候选。
- 不从低排名同主题 peer 中挖替代行动候选。
- 对 `0857.HK`、`0941.HK`、`0002.HK` 做 veto 审计：确认 veto 是否来自持续负样本、错误选股、短期 timing，还是风险模型过度保守。
- 对互联网平台做 peer-relative 复核：下一次若考虑 `9618.HK`、`9988.HK`、`0700.HK`、`3690.HK`，必须列出最近 T+3/T+5/T+10 的 best peer 与 `selected_vs_best_bps`，并证明相对 best peer 改善。

## 信心最弱的位置

1. **日期对齐信心最弱。** 回放日期是 `2026-01-16`，但行情字段显示 `quote_trade_date=2026-04-29`。这会污染均线、区间位置、成交量与 risk_on 解释，必须把所有排名当作诊断而非现场信号。
2. **动态选股信心弱。** 前排高分候选全部被 `symbol_risk_veto` 拦截，说明模型的趋势评分与 posterior 风险历史冲突。此时若强行选择，会更像 risk-control error。
3. **互联网平台的 symbol-selection 信心弱。** posterior 中多次显示 `0700.HK`、`9988.HK` 相对 best peer 明显落后，近期 best peer 在不同窗口切换为 `9618.HK`、`9988.HK`、`3690.HK`、`1024.HK`。如果没有新鲜 peer-relative 证据，单纯按涨幅或熟悉度选股很容易继续错选。
4. **短期 timing 信心弱。** posterior 最近仍有 `2800.HK`、`9988.HK`、科技 ETF 的 T+3/T+5 失败，说明即使方向修复，早窗口承压仍常见。

## 仍缺少的证据

- 日期对齐的 `2026-01-16` 当日真实收盘、成交量、MA20/MA60、range_pos_60 与 ETF 确认。
- 主题 ETF 对单名股的确认，尤其是互联网平台与恒生科技 ETF 是否同步收复 MA60、是否有成交量扩张。
- 对 `0857.HK`、`0941.HK`、`0002.HK` 的 veto 归因：是历史样本质量问题、策略误配，还是该类高趋势/高股息名字在本系统中确实容易晚进场。
- 同主题 peer-relative 表：至少覆盖 T+3/T+5/T+10 的 best peer、peer median、`selected_vs_best_bps`。
- 若要重新考虑 `0386.HK`、`3690.HK` 这类非 veto 但低排名/非行动清单名字，需要它们先独立进入 `actionable_candidates`，并证明跑赢 veto leader 与最近 best peer。

## 可能失败模式

1. **risk-control error：** 因为 `0857.HK`、`0941.HK`、`0002.HK` 分数高而忽略 `symbol_risk_veto` 与空行动清单，导致把诊断候选误升为行动建议。
2. **symbol-selection error：** 在互联网平台或能源主题中，因 leader 被 veto 就转向低排名、看起来更干净的 peer，却没有证明该 peer 相对 veto leader 和最近 best peer 的新鲜强势。
3. **timing error：** 在 `risk_on` 当日追随强涨幅，但 T+3/T+5 仍可能回吐，尤其是 MA60 未完全修复或成交量不足的科技/互联网名字。

## 动态选股错误分类

今天的候选来自动态 symbol selection，但没有任何 actionable 输出。若未来仍从这些信号中升级，最可能的错误类型依次是：

- `risk-control error`：忽略 `actionable_candidates=[]`、`symbol_risk_veto`、日期错位和未晋级参数优化。
- `symbol-selection error`：重复选择主题 score leader 或熟悉大票，而没有证明其相对最近 best peer 改善。
- `timing error`：把单日 risk_on 和趋势分数当成短线确认，忽略 T+3/T+5 早窗口失败率。
- `theme_error`：相对较低；因为问题更集中在候选选择和风控门槛，而不是所有主题方向都被否定。

## 下一周期优先级

1. **先修数据对齐。** 下一周期先确认 `as_of_date` 与 `quote_trade_date` 一致；不一致时继续限制为 `watch_only`。
2. **先看行动清单，不看高分诱惑。** 只有进入 `actionable_candidates` 且没有 veto 的名字，才进入行动候选讨论。
3. **建立 peer-relative 审计表。** 对 internet-platform、energy、telecom-dividend、utilities-defensive 分别列出最近 best peer、`selected_vs_best_bps`、成交量、MA20/MA60 状态。
4. **复核 veto，而不是绕开 veto。** 对 `0857.HK`、`0941.HK`、`0002.HK` 的历史失败做归因；在未解释前，不用低排名 peer 替代。
5. **保持 cost/edge/risk gates。** 参数优化未晋级，不能降低 `minimum_edge_bps`，也不能把 challenger 结果作为升级依据。

## 记忆更新判断

posterior 继续强化了同一类模式：空行动清单 + 前排 veto + selected-vs-best 反复落后 + 参数优化未晋级。现有记忆已经覆盖大部分规则；本次只做一条更精确的基线补充：当日期错位与空行动清单同时出现时，所有动态结果只能作为审计队列，不能输出行动建议。
