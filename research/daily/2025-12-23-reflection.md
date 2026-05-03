# 2025-12-23 投资复盘（historical）

> 会话：`historical`  
> 时间：2025-12-23 07:31  
> 模式：`recommendation_only`  
> 周期：4-90 天 swing  
> 重要限制：本次 `as_of_date` 为 `2025-12-23`，但行情字段 `quote_trade_date` 为 `2026-04-28`。因此所有排名只作诊断，不作当日实时确认。

## 1. 今日结论

今天不升级任何标的到 `buy_candidate`、`accumulate` 或 `hold`。组合层面的建议是全体 `watch_only`。

原因很直接：

1. 市场状态是 `risk_off`：股票平均 1 日变动为 -0.946%，ETF 平均 1 日变动为 -1.847%。
2. ETF 没有确认：`2800.HK`、`3033.HK`、`3067.HK` 都在 `downtrend`，且分数为 0。
3. `actionable_candidates` 为空。
4. 动态排名前三名 `0857.HK`、`0941.HK`、`0006.HK` 虽然分数高，但全部被 `symbol_risk_veto` 拦截。
5. 可替代 peer（`0883.HK`、`0002.HK`、`0728.HK`）各自仍有缺口：不是主题分数 leader、部分未通过 `qualified_for_watch`，成交或 MA 结构也不够完整。
6. 历史回放日期和报价日期不一致，不能把 2026-04-28 的报价结构当成 2025-12-23 的现场证据。

所以今天最诚实的输出不是“找一个可以买的”，而是把强主题和缺失条件列成下一轮观察队列。

## 2. 信心最弱的地方

### 2.1 日期错位导致的证据信心最弱

这是今天最大的弱点。`as_of_date` 是 `2025-12-23`，但每个行情项的 `quote_trade_date` 是 `2026-04-28`。这意味着 MA20、MA60、成交量、range position 和最新价格都不能被视为 2025-12-23 当日可用的现场证据。

因此即使 `0857.HK`、`0941.HK`、`0006.HK` 看起来趋势很好，我也不能把这些信号升级为行动建议。它们只能说明：如果当日也存在类似结构，值得进一步验证。

### 2.2 动态选股信心弱

后验摘要显示 `symbol_selection_error` 有 118 次，是最主要的错误类别。今天的高分主题也暴露了相同问题：

- `energy` 的 leader 是 `0857.HK`，但它被 `symbol_risk_veto` 拦截；`0883.HK` 更干净，但不是主题 leader，且 `volume_ratio_20` 只有 0.8064，`qualified_for_watch` 为 false。
- `telecom-dividend` 的 leader 是 `0941.HK`，但被 `symbol_risk_veto` 拦截；`0728.HK` 成交强，但 MA20 仍低于 MA60，不是完整上升趋势。
- `utilities-defensive` 的 leader 是 `0006.HK`，但被 `symbol_risk_veto` 拦截；`0002.HK` 更干净，但成交确认偏弱，且不是主题 leader。

这类情况很容易诱导我犯“leader 被 veto，所以自动买第二名”的错误。今天必须拒绝这个捷径。

### 2.3 防御主题强度的可交易性弱

强主题集中在 `utilities-defensive`、`telecom-dividend`、`energy`。这更像风险偏好下降时的防御/红利/能源相对强，而不是市场广泛风险偏好的恢复。若没有 broad ETF 和技术 ETF 配合，单独追强防御主题的 swing edge 不清楚。

## 3. 仍然缺失的证据

下一轮需要补齐这些证据，才有资格从 `watch_only` 升级：

1. **日期对齐行情**：需要 `2025-12-23` 当日或之前可见的价格、MA、成交量和宽度数据，而不是 2026-04-28 报价。
2. **ETF 确认**：`2800.HK` 至少重新站回 MA20/MA60，并伴随成交或 breadth 改善；`3033.HK` / `3067.HK` 至少修复 MA20，最好能重新接近 MA60。
3. **主题内 peer-relative evidence**：需要证明替代标的相对 leader 和同主题 peers 的近期表现已经改善，而不只是“leader 被 veto”。
4. **成交确认**：`0883.HK`、`0002.HK` 这类替代 peer 需要更强的 `volume_ratio_20`，否则上涨可能只是低量相对强。
5. **成本门槛后的 swing edge**：当前策略要求预期 swing edge 同时超过 35 bps 往返成本和 100 bps 最低 edge。今天没有足够证据证明任何标的满足。

## 4. 今日建议状态

| 标的 / 主题 | 建议 | 理由 | 升级触发 | 失效条件 |
|---|---|---|---|---|
| `energy` | `watch_only` | 主题相对强，但 leader `0857.HK` 被 `symbol_risk_veto`；替代 `0883.HK` 不是 leader 且成交未充分确认 | 日期对齐证据显示 `0883.HK` 持续强于 `0857.HK`，成交放大至 1.0 以上，并保持 MA20 > MA60 | `0883.HK` 跌回 MA20 下方，或能源主题相对强消失 |
| `telecom-dividend` | `watch_only` | `0941.HK` 高分但被 veto；`0728.HK` 有成交但 MA20 仍低于 MA60 | `0728.HK` MA20 上穿 MA60，继续放量，并证明相对 `0941.HK` 的 peer strength | `0728.HK` 跌破 MA60 或成交放大后价格不跟随 |
| `utilities-defensive` | `watch_only` | `0006.HK` 高分但被 veto；`0002.HK` 较干净但成交偏弱，不可自动替代 | `0002.HK` 成交改善并继续守住 MA20/MA60，同时相对 `0006.HK` 改善 | `0002.HK` 跌破 MA20，或防御主题失去相对优势 |
| `9618.HK` / `internet-platform` | `watch_only` | `9618.HK` 是互联网中少数 `uptrend`，但 ETF 与多数 peers 仍弱，且有 `symbol_risk_veto` | `3033.HK` / `3067.HK` 修复趋势，`9618.HK` 放量站稳 MA20 且 peers 不再拖累 | `9618.HK` 跌回 MA20 下方，或互联网 ETF 继续破位 |
| `2800.HK` | `watch_only` | broad ETF `downtrend`，score 0，不能做 broad-market bullish upgrade | 重新站回 MA20/MA60，成交和 breadth 同步改善 | 继续低于 MA20/MA60，或 broad ETF 弱于个股修复 |
| `3033.HK` / `3067.HK` | `watch_only` | 技术 ETF 仍在 MA20/MA60 下方，score 0 | 先修复 MA20，再观察 MA60 与成交确认 | 下跌延续或反弹无量 |
| `1810.HK` | `watch_only`，偏 `avoid` 观察 | -3.79%，`downtrend`，range_pos_60 为 -0.1149；但后验显示 `avoid` 容易早，不能缺少反弹风险检查 | 只有在 broad/ETF 同步弱、且自身继续放量下破时才考虑 `avoid` | 若出现技术反弹或 ETF 修复，避免追空 |

## 5. 可能的失败模式

### 5.1 `symbol-selection error`

最可能的失败模式是：主题判断对了，但选错表达。今天 `energy`、`telecom-dividend`、`utilities-defensive` 都有类似结构：leader 高分但被 veto，第二名更干净却没有独立通过所有门槛。如果下一轮我为了“不错过主题”而自动切到第二名，就很容易再次犯 symbol-selection error。

### 5.2 `timing error`

在 `risk_off` 中追相对强防御/能源，短期可能已经拥挤。`0857.HK`、`0941.HK`、`0006.HK` 的 `range_pos_60` 都接近或超过 1，说明位置偏高。即便中期主题没错，T+3/T+5 也可能先回撤。

### 5.3 `risk-control error`

最大的风险控制错误是无视 `actionable_candidates` 为空和 `symbol_risk_veto`。如果把 diagnostic score 当成 action score，就会违反已有规则：空行动列表阻止升级；低通过率标的不能靠单日强势升级。

## 6. 动态选择错误分类

今天的候选来自动态 trade universe ranking，因此需要显式分类未来可能错误：

- `0857.HK`：主要风险是 `symbol-selection error` + `risk-control error`。它是 `energy` leader，但历史通过率极低且被 veto。
- `0883.HK`：主要风险是 `symbol-selection error`。它更干净，但不是 leader，也没有成交确认；若自动替代 `0857.HK`，就是 peer 替代错误。
- `0941.HK`：主要风险是 `risk-control error`。趋势强但被 veto，不能因红利防御主题强而忽略低通过率。
- `0728.HK`：主要风险是 `timing error` + `symbol-selection error`。成交强，但 MA20 仍未站上 MA60，可能只是防御 bid 的早期波动。
- `0006.HK`：主要风险是 `risk-control error`。score 高但 pass_rate 为 0，不能升级。
- `0002.HK`：主要风险是 `symbol-selection error`。比 `0006.HK` 风险记录干净，但成交不足，不能只因 leader veto 就替代。
- `9618.HK`：主要风险是 `theme error`。个股强于互联网 peers，但主题内部和 tech ETF 没确认。

## 7. 下一周期优先级调整

1. **先做日期对齐，再看排名**：historical replay 中只要 `as_of_date` 与 `quote_trade_date` 不一致，就先寻找 date-aligned evidence；找不到就默认 `watch_only`。
2. **把 veto 后的 peer audit 作为主任务**：下一轮不要问“哪个主题最强”，而要问“leader 被 veto 后，第二名是否独立满足趋势、成交、相对强度和风险门槛”。
3. **ETF 修复前不升级互联网和 broad ETF**：`2800.HK`、`3033.HK`、`3067.HK` 仍是市场确认闸门；它们不修复，单名强势只能观察。
4. **防御主题只记录触发条件，不抢跑**：`energy`、`telecom-dividend`、`utilities-defensive` 都值得继续看，但下一轮必须等成交和 peer-relative evidence，而不是因为 risk_off 中它们相对强就行动。
5. **把空 `actionable_candidates` 视为硬门槛**：只要为空，报告可以有观察队列和失效条件，但不能产生实际买入/持有升级。

## 8. 今日给自己的记录

今天的重点不是“没有机会”，而是“机会筛选器在工作”。

以前我容易把高分榜当成答案。现在更像一只小章鱼先摸到三块发亮的石头，再停下来确认：这是不是当日的石头？是不是已经被历史证明会割手？旁边那块更干净的石头，是不是只是因为我不敢碰第一块而显得安全？

今天的答案是：还不能拿。先观察。
