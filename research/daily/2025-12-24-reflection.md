# 2025-12-24 投资复盘反思

## 一句话结论

今天不能把任何信号当成高置信行动。最重要的约束不是单个分数，而是三件事同时存在：`as_of_date=2025-12-24` 与 `quote_trade_date=2026-04-29` 明显错位、成交量字段大量为 0 或极低、后验记录反复显示动态选股与低通过率标的容易产生 `symbol_selection_error`。因此今日基线应以 `watch_only` 和条件观察为主；即使 deterministic ranking 给出 `2020.HK` 作为唯一 `actionable_candidates`，也只能把它视为低置信候选，而不是自动升级。

## 今日信号如何解读

市场状态标为 `neutral`，但结构并不均衡。宽基 `2800.HK` 仍只是 range，价格略高于 MA20、低于 MA60；科技 ETF `3033.HK`、`3067.HK` 仍在 downtrend；互联网平台、消费科技、医药大多还没有修复 MA20/MA60。真正能看见趋势结构的地方集中在少数防御/红利/周期/消费个股，但其中多个 leader 被 `symbol_risk_veto` 或流动性门槛拦住。

今天输入里有一个特别需要警惕的冲突：人工计划和市场评估把 `0005.HK` 描述成主要行动候选，但 deterministic ranking 的实际 `actionable_candidates` 只有 `2020.HK`，而 `0005.HK` 在最新 ranking 中只有 56.83 分，并带有 `low_volume_ratio_20_below_0_6`，没有达到 action threshold。这说明我不能用叙事覆盖机器输出，也不能用机器输出覆盖日期错位。正确做法是把两者都降级为诊断：`2020.HK` 是当前唯一机械候选，`0005.HK` 是趋势尚可但成交/评分不足的观察对象。

## 推荐与置信度

### `2020.HK`：低置信 `buy_candidate` / 实际执行前仍偏 `watch_only`

`2020.HK` 是 deterministic ranking 中唯一 `actionable_candidates`：score 67.98，价格在 MA20 与 MA60 上方，MA20 高于 MA60，`regime_flags=["uptrend"]`，且没有 `symbol_risk_veto`。这是今天最干净的机械信号。

但我的置信度仍弱，原因有三点：第一，`quote_trade_date` 与回放日期不一致；第二，`volume_ratio_20=null`，无法确认真实成交支持；第三，同主题 peer 分化很大，`2331.HK`、`9992.HK`、`6862.HK` 均没有同步确认。若要升级为真实行动，下一步必须看到日期对齐后的成交恢复、价格继续守住 MA20/MA60，以及消费可选主题内部至少有一个 peer 同步改善。

失效条件：跌回 MA20 下方、同主题 peer 继续恶化、或补齐日期对齐数据后成交仍无法支持，则降回纯 `watch_only`。

### `0005.HK`：`watch_only`

`0005.HK` 的结构并不差：价格在 MA20/MA60 上方，MA20 高于 MA60，属于 financials-bank 主题 leader。但最新 ranking 分数只有 56.83，低于 action threshold，并且成交量门槛失败。它可以作为银行方向的观察对象，但不能因为早前叙事里出现过“行动候选”就升级。

缺失证据：日期对齐报价、正常成交量、以及宽基 `2800.HK` 重新站上 MA60 的确认。

### `2269.HK`：`watch_only`

`2269.HK` 有短线弹性，且当日涨幅突出，但最新分数只有 39.89，低于 watch threshold，仍未站回 MA60，成交也极弱。它更像一个需要 follow-through 的 headline/rebound setup，而不是已确认趋势。若后续不能站上 MA60 并保持 1-2 日延续，不能追。

### `0883.HK` / `0857.HK`：能源主题只做 peer audit，不行动

`0857.HK` 是能源 leader，但被 `symbol_risk_veto` 拦截，且有严重负后验：pass_rate=0.059，avg_return_pct=-15% 左右，并有 adverse breach。`0883.HK` 看起来更干净，没有 veto，趋势也在 MA20/MA60 上方，但它不是 theme score leader，且没有证明自己相对 `0857.HK` 出现 fresh peer-relative strength。按现有规则，它只能进入观察和对照队列。

### `2800.HK`、`3033.HK`、`3067.HK`：全部 `watch_only`

宽基 `2800.HK` 仍未收复 MA60，且后验对 broad-index ETF bullish calls 的通过率低；科技 ETF 仍处 downtrend。这里最容易犯的错是把单日反弹或低位波动当成趋势修复。下一周期必须先看 breadth、volume、MA60，再谈升级。

## 信心最弱的地方

1. **日期一致性最弱**：`as_of_date=2025-12-24`，但报价与 MA 数据来自 `2026-04-29`，这会污染所有短线判断。
2. **成交确认最弱**：大量 `latest_volume=0`、`volume_ratio_20=null/0`，不能验证突破是否真实。
3. **动态选股置信度弱**：后验 450 次评估中 `symbol_selection_error=124`，这是最大的重复错误类型；今天 `2020.HK` 虽然是唯一 actionable，但仍必须经过同主题 peer confirmation。
4. **宽基确认不足**：`2800.HK` 未收复 MA60，科技 ETF 仍 downtrend，单个股票的上行不能被解读为市场整体确认。

## 仍然缺失的证据

- 日期对齐的 2025-12-24 当日收盘、成交、MA 数据。
- `2020.HK` 与 `2331.HK`、`9992.HK`、`6862.HK` 的同主题相对强弱连续比较。
- `2800.HK` 是否能重新站上 MA60，并伴随 breadth 与 volume 改善。
- 科技 ETF `3033.HK` / `3067.HK` 是否至少重新站上 MA20，避免把弱反弹误认为趋势反转。
- 被 veto leader 的替代 peer 是否真的相对 leader 改善，而不只是风险历史更干净。

## 今日推荐的 1-3 个 likely failure modes

1. **symbol-selection error**：`2020.HK` 被动态选为唯一 actionable，但同主题 peer 没有同步确认，未来可能不是消费可选主题里的最佳表达。
2. **timing error**：日期错位和成交缺失可能让看似站上 MA20/MA60 的信号在真实 2025-12-24 环境下并不存在，短线窗口尤其容易错。
3. **risk-control error**：若忽略 `symbol_risk_veto` 和 low pass-rate 后验，可能会重新升级 `0857.HK`、`0941.HK`、`2800.HK` 这类历史低通过率标的。

## 动态选择错误分类

今日实际动态行动候选是 `2020.HK`。若未来失败，优先分类为 **symbol-selection error**，其次才是 theme error。原因是 consumer-discretionary 主题内部高度分化：`2020.HK` 独强，peer 没有同步确认。如果 `2020.HK` 回落而同主题其他 peer 表现更好，错误不是“消费主题不可做”，而是“选错了主题表达”。若整个主题一起走弱，则再归为 theme error。若方向最终正确但 T+3/T+5 先回撤，则归为 timing error。

## 下一周期优先级

1. **先修数据一致性**：在任何升级前，优先拿到日期对齐的快照；若仍错位，所有 recommendation capped at `watch_only` 或低置信条件候选。
2. **对 `2020.HK` 做 peer-relative audit**：比较 `2020.HK` 相对 `2331.HK`、`9992.HK`、`6862.HK` 的 3/5/10 日表现、MA 修复和成交恢复，确认它不是孤立假突破。
3. **宽基确认优先于单股扩仓**：`2800.HK` 必须先重新站上 MA60，并且 breadth/volume 改善，否则单股信号只能小仓或观察。
4. **veto leader 只做诊断**：`0941.HK`、`0857.HK`、`0006.HK` 继续作为风险案例，不因高分或趋势好而升级；替代 peer 必须证明 fresh relative strength。
5. **科技链保持防守观察**：`3033.HK`、`3067.HK`、`0700.HK`、`9988.HK`、`1810.HK` 在 MA60 未修复前不升级。

## 是否更新长期记忆

后验重复模式仍然是 `symbol_selection_error`、低通过率标的误升、以及日期错位污染判断。现有 `memory/active_investment_learnings.md`、`memory/investment_rules.md`、`memory/investment_error_patterns.md` 已经包含这些规则，今天没有新增更精确且未覆盖的规则。只追加 journal，记录本次历史回放的具体执行约束。
