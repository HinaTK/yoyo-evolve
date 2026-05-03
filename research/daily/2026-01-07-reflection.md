# 2026-01-07 投资复盘反思（historical）

> 模式：`historical` / `recommendation_only`  
> 时间：2026-01-07 18:10  
> 关键限制：本轮输入存在 `as_of_date=2026-01-07` 与 `quote_trade_date=2026-04-29` 不一致；因此所有排名和候选都只能作为历史回放诊断，不能当作当日已确认信号。

## 1. 今日结论回顾

今天的市场状态被标记为 `risk_on`，股票与 ETF 平均 1 日表现均为正，强势主要集中在 `internet-platform`、金融交易所、能源、电讯及防守公用事业。确定性排名里，`0005.HK` 是唯一 `actionable_candidates`，其余高分标的如 `0857.HK`、`0941.HK`、`0002.HK` 均因 `symbol_risk_veto` 被拦截；`0883.HK`、`0728.HK` 等替代 peer 也未能同时满足主题 leader、风险、相对强度和行动清单要求。

因此，本轮最稳妥的复盘结论不是“积极追随 risk-on”，而是：

- `0005.HK` 可以作为唯一行动清单里的重点审计对象，但由于日期错配，实际建议应降为低置信条件观察，而不是无条件 `buy_candidate`。
- `0857.HK`、`0941.HK`、`0002.HK` 的趋势分数很强，但 `symbol_risk_veto` 与历史低通过率足以阻止升级。
- `0883.HK`、`0728.HK` 这类“看起来更干净”的同主题替代，不因 leader 被 veto 就自动变成可行动；它们必须独立出现在 `actionable_candidates`，并证明相对被 veto leader 的新鲜强势。
- `2800.HK`、`3033.HK`、`3067.HK` 仍需要 MA60、成交和广度确认，不能仅因 risk-on 单日反弹升级。

## 2. 信心最弱的地方

1. **日期一致性最弱**：`as_of_date=2026-01-07`，但行情字段来自 `quote_trade_date=2026-04-29`。这会污染成交量、MA、range position 和排名结论，尤其会让 `0005.HK` 的唯一 action 状态带有未来数据风险。
2. **动态选股的可靠性仍弱**：后验摘要显示 `symbol_selection_error=159`，且互联网平台、能源、电讯、公用事业等主题反复出现 selected-vs-best 问题。今天的高分 leader 大量被 `symbol_risk_veto` 拦截，说明模型的主题 leader 分数与可交易性之间仍有断裂。
3. **短期 timing 信心弱**：近期 T+3/T+5 失败仍集中在 `2800.HK`、`9988.HK`、科技 ETF 等方向。今天虽然是 `risk_on`，但不能推断 T+3/T+5 延续性已经恢复。
4. **ETF 确认不足**：`2800.HK`、`3033.HK`、`3067.HK` 的历史失败率和低通过率要求更高的广度、成交和 MA60 确认；单日上涨不足以支持升级。

## 3. 仍然缺失的证据

- 日期对齐的 2026-01-07 当日收盘快照，而不是 2026-04-29 报价字段。
- `0005.HK` 在真实 2026-01-07 窗口内的成交确认、相对金融同业强弱、以及是否真正满足行动门槛。
- `2800.HK` 的广度扩散、MA60 重新站稳和成交放大证据。
- 科技 ETF `3033.HK` / `3067.HK` 重新站上 MA60，并与 `9618.HK`、`9988.HK`、`3690.HK` 的主题内强弱形成一致确认。
- 对 `0857.HK`、`0941.HK`、`0002.HK` 的 veto 是否仍有效的日期对齐复核；若仍有效，则只能作为 peer-audit 队列。

## 4. 今日建议的可能失败模式

1. **risk-control error**：把未来报价生成的 `actionable_candidates` 当成 2026-01-07 的真实行动信号，尤其是机械升级 `0005.HK`。
2. **symbol-selection error**：继续选择高分 theme leader（如 `0857.HK`、`0941.HK`、`0002.HK`），却忽视其历史低 pass_rate、负平均收益和 repeated symbol_selection_error。
3. **timing error**：在 risk-on 单日后过早判断 T+3/T+5 延续，特别是对 `2800.HK`、科技 ETF 和互联网平台反弹的追随。

## 5. 动态选股错误分类

- `0005.HK`：来自动态 ranking 的唯一 `actionable_candidates`。主要潜在错误是 **risk-control error**，因为行动状态来自日期不一致的数据；次要风险是 **timing error**，因为 1 日涨幅和成交确认不足以证明 swing edge。
- `0857.HK`、`0941.HK`、`0002.HK`：高分但被 `symbol_risk_veto` 拦截。若升级，主要是 **symbol-selection error** 与 **risk-control error**。
- `0883.HK`、`0728.HK`：作为替代 peer 的诱惑较强，但未独立清除行动门槛。若升级，主要是 **symbol-selection error**。
- `2800.HK`、`3033.HK`、`3067.HK`：若因 risk-on 反弹升级，主要是 **timing error** 与 **theme error**，因为 ETF 确认和 MA60 修复仍不足。

## 6. 下一轮优先级调整

1. **先修复数据时间轴**：所有候选必须先通过日期对齐检查；若 `as_of_date` 与 quote 字段冲突，行动清单只作审计，不作交易升级。
2. **把 `0005.HK` 放在第一审计位**：不是直接行动，而是检查真实 2026-01-07 的价格、成交、MA20/MA60 和金融同业确认。
3. **把 veto leader 当作 peer-audit 队列**：`0857.HK`、`0941.HK`、`0002.HK` 的高分只用于寻找主题强度，不用于升级；替代 peer 必须证明相对 leader 的新鲜强势。
4. **ETF 优先于单名**：在 `2800.HK`、`3033.HK`、`3067.HK` 没有 MA60 与成交确认前，互联网、科技和 broad-market 方向保持 `watch_only`。
5. **降低 T+3/T+5 timing 权重**：近期后验显示短窗失败仍多，下一轮应把行动触发条件从“单日 risk-on”提高到“连续确认 + 成交 + peer-relative strength”。

## 7. 记忆更新判断

允许更新长期记忆，且后验中 `symbol_selection_error`、低 pass_rate 标的升级、以及日期错配导致行动信号污染已经反复出现。本次只补充一条更精确的操作化规则：**当 `actionable_candidates` 本身由非日期对齐报价生成时，即使列表非空，也只能作为条件审计清单，不能直接升级为行动建议。**
