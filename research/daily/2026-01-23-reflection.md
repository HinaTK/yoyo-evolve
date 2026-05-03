# 2026-01-23 投资复盘（historical）

## 结论摘要

今天的回放不支持任何可执行升级。虽然快照里的 `market_summary.risk_state` 为 `risk_on`，平均股票与 ETF 单日涨幅均为正，且多个防守、能源、通信红利方向的趋势分数很高，但确定性排名给出的 `actionable_candidates=[]`。前三个 diagnostic candidates —— `0857.HK`、`0941.HK`、`0002.HK` —— 均为 `diagnostic_only=true`、`qualified_for_action=false`，且都被 `symbol_risk_veto` 阻断。因此本轮应定义为 veto audit + peer-relative review，而不是交易信号。

## 事实与解释

事实：
- `as_of_date=2026-01-23`，但行情字段显示 quote 日期为 `2026-04-29`，属于非日期对齐数据；按规则只能作为条件审计输入。
- `actionable_candidates=[]`，没有任何标的通过完整行动门槛。
- `0857.HK` 得分最高（84.42），但有 `symbol_risk_veto`：33 次评估 pass_rate=0.091，平均回报 -0.795%，且有 adverse breach 与 selection error。
- `0941.HK` 得分 81.98，但 30 次评估 pass_rate=0.000，平均回报 -0.258%，同样有 adverse breach 与 selection error。
- `0002.HK` 得分 76.08，但 3 次评估 pass_rate=0.000，平均回报 -0.242%。样本较少，但方向不支持直接升级。
- 参数优化没有更新 active strategy；样本、改善、胜率、样本质量门槛均未通过。

解释：
- 今天最强的表层结构来自能源、通信红利、公用事业与银行/交易所方向，而不是互联网平台或恒生科技；但高分并不等于可交易，因为历史后验对这些 leader 的实际选择质量给出了否定信号。
- `risk_on` 只能说明广义风险偏好偏暖，不能覆盖 `actionable_candidates=[]`、非日期对齐 quote、`symbol_risk_veto` 三个硬约束。
- 动态选股流程给出的结果更像“哪些标的需要被审计”，不是“哪些标的可以买”。

## 今日建议状态

- 总体状态：`watch_only` / audit-only。
- 不升级 `0857.HK`、`0941.HK`、`0002.HK`，即使它们是各自主题 leader 且 trend_score 很强。
- 不从同主题 lower-ranked peers 中寻找替代行动标的；`0883.HK`、`0006.HK`、`0728.HK` 等同样未独立进入 `actionable_candidates`，且多数也有 veto 或 non-leader 限制。
- 不把 `2800.HK` 作为默认 fallback；其近期 T+3 / T+5 失效记录仍然要求重新通过日期对齐 edge gate。

## 信心最弱的地方

信心最弱的是对 2026-01-23 当天真实市场状态的判断，因为输入中的 quote 时间为 `2026-04-29`，与 `as_of_date` 不一致。由此产生的趋势、成交量、range_pos_60 与 leader 排名只能用于规则压力测试，不能被当作当日真实确认。

其次，`0002.HK` 的后验样本只有 3 次，`9618.HK`、`0728.HK`、`2020.HK` 等样本也偏少；这些 veto 或低 pass_rate 的结论方向明确，但统计置信度不如 `2800.HK`、`3033.HK`、`3067.HK`、`0700.HK`、`9988.HK` 等高样本标的。

## 仍然缺失的证据

- 日期对齐的 2026-01-23 OHLCV、MA20/MA60、volume_ratio_20 与主题内相对强弱。
- `0857.HK`、`0941.HK`、`0002.HK` 相对近期 actual best peer 的 T+3/T+5 fresh relative strength，而不只是相对当前 ranked leader 的比较。
- broad-market ETF 与主题 ETF 的同步确认，尤其是 `2800.HK`、`3033.HK`、`3067.HK` 是否在日期对齐窗口内提供正向 edge。
- 若要重新考虑互联网平台，需要证明 `9618.HK`、`3690.HK`、`1024.HK` 等近期 best peer 与 `0700.HK`、`9988.HK` 的相对关系已发生改善。
- 参数 challenger 需要更高质量样本、正向平均净回报、可接受 win_rate 与稳定 adverse-risk，而当前尚未满足。

## 可能失败模式

1. **风险控制错误**：把 `risk_on` 与高 trend_score 解释为可以买，忽略 `actionable_candidates=[]`、`diagnostic_only=true` 和 `symbol_risk_veto`。
2. **symbol-selection error**：在 `0857.HK`、`0941.HK`、`0002.HK` 被 veto 后，从同主题的 `0883.HK`、`0006.HK`、`0728.HK` 中挖替代品，但这些替代品没有独立通过行动列表与 edge/risk gates。
3. **timing error**：使用非日期对齐 quote 生成的强势排序来推断 2026-01-23 的即时入场点，导致回放中的未来信息污染。

本轮动态符号选择没有产生可执行标的；若未来仍据此行动，最可能的错误分类是 risk-control error 与 symbol-selection error，其次是 timing error。

## 下一周期优先级

1. 先修复或过滤非日期对齐 quote：只有 date-aligned 快照才能进入行动判断。
2. 对 top diagnostic candidates 做 veto audit：重点检查 `0857.HK`、`0941.HK`、`0002.HK` 的低 pass_rate、负平均回报、adverse breach 是否仍成立。
3. 做 peer-relative review，而非替代挖掘：每个被 veto 的主题 leader 都必须命名近期 actual best peer，并证明 fresh relative strength 后才允许重新讨论升级。
4. 继续维持 active strategy，不推广参数 challenger；等待 samples、improvement、win_rate、sample_quality 同时改善。
5. 对 `2800.HK` 与恒生科技 ETF 单独做 T+3/T+5 edge 复核，确认它们是有效 confirmation，而不是心理上的低风险 fallback。
