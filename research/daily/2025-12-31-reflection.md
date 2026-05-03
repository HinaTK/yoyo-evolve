# 2025-12-31 投资复盘反思

时间：2025-12-31 10:21  
Session：historical  
模式：recommendation-only / historical bootstrap replay

## 结论先写

今天不应该给出新的行动型建议。排名系统给出的 `actionable_candidates` 为空，前三个动态候选 `0857.HK`、`0941.HK`、`0006.HK` 都只是 `diagnostic_only`，而且全部被低成交量和/或 `symbol_risk_veto` 拦住。即使市场摘要显示 `risk_on`，这个信号也不能覆盖两个更硬的事实：

1. `as_of_date` 是 `2025-12-31`，但报价字段是 `2026-04-29`，日期不一致；
2. 没有任何标的通过行动门槛，成本门槛也要求预期 swing edge 同时超过 round-trip cost 和 minimum edge gate。

所以今天的建议状态是：以 `watch_only` 为主，把动态排名当成“下一轮验证清单”，不是交易清单。

## 今日证据

### 市场与主题

- 市场摘要为 `risk_on`，股票平均 1 日涨幅约 `1.157%`，ETF 平均 1 日涨幅约 `1.047%`。
- 当日领涨集中在 `3690.HK`、`9992.HK`、`6862.HK`，但它们在排名系统里并没有形成可行动结论：
  - `3690.HK` 虽然 1 日涨幅 `3.05%`，但价格仍低于 MA20 和 MA60，且不是 internet-platform 主题 leader。
  - `9992.HK` 1 日涨幅 `2.87%`，但仍远低于 MA60，主题 leader 是 `2020.HK`。
  - `6862.HK` 1 日涨幅 `2.43%`，但仍在 `downtrend`。
- 主题均分靠前的是 `utilities-defensive`、`financials-bank`、`telecom-dividend`、`energy`，不是高 beta 科技线。这说明所谓 `risk_on` 更像选择性修复，而不是全市场风险偏好扩散。

### 动态候选

系统前三名：

1. `0857.HK`：score `61.85`，energy theme leader，趋势结构强，但 `volume_ratio_20=0.2121`，低于成交量门槛，并且有 `symbol_risk_veto`。历史评估显示 pass_rate 偏低、平均收益为负、存在 adverse breach 和 symbol_selection_error。
2. `0941.HK`：score `58.17`，telecom-dividend theme leader，趋势结构强，但 `volume_ratio_20=0.1898`，也有 `symbol_risk_veto`。历史 pass_rate 极低。
3. `0006.HK`：score `57.38`，utilities-defensive theme leader，趋势结构强，但 `volume_ratio_20=0.3079`，并且有 `symbol_risk_veto`。历史 pass_rate 为 `0.000`。

这三个名字共同的形状是：趋势分数漂亮，但成交量不足，且前两个/三个都被历史风险记录压住。它们适合观察“是否有持续放量确认”，不适合今天升级。

## 今日建议状态

### `0857.HK` — `watch_only`

- 理由：能源主题强、价格高于 MA20/MA60、MA20 高于 MA60，但当前 score 低于 action threshold，且存在 `symbol_risk_veto`。
- 需要的触发：日期对齐数据确认后，继续保持 MA20/MA60 上方，成交量至少恢复到接近 20 日均量，并且同主题内相对 `0883.HK`、`0386.HK` 仍有明确强度优势。
- 失效条件：跌回 MA20 下方，或同主题 peer 明显跑赢而 `0857.HK` 只靠历史分数维持 leader 位置。
- 置信度：低。主要受日期错配、低成交量、历史 symbol risk 影响。

### `0941.HK` — `watch_only`

- 理由：趋势结构强，价格高于 MA20/MA60，但成交量太弱，历史 pass_rate 太低，不能因为 telecom-dividend theme 较稳就越过风险门。
- 需要的触发：放量站稳高位，同时相对 `0728.HK` 继续保持主题内优势；最好有防御/红利主题整体确认。
- 失效条件：跌回 MA20，或高位横盘期间量能不能跟上，或 `0728.HK` 转强使 leader 选择变得不清晰。
- 置信度：低。

### `0006.HK` — `watch_only`

- 理由：utilities-defensive theme leader，趋势结构强，但历史记录极差，且同样缺少成交量确认。
- 需要的触发：放量突破并维持在 MA20/MA60 上方，同时相对 `0002.HK` 的优势扩大。
- 失效条件：回落到 MA20 下方，或 `0002.HK` 相对表现改善使 `0006.HK` 的 leader 选择失效。
- 置信度：低。

### 其他观察

- `0005.HK` 没有 `symbol_risk_veto`，score `55.12`，但仍被低成交量挡住；它可能比前三名更干净，但不是 actionable，因为也没有通过成交量与 action score。
- `0883.HK` 没有 `symbol_risk_veto`，但不是 energy theme leader；在 `0857.HK` 被 veto 后，它不能自动替代，除非证明新一轮 peer-relative strength 已经超过 `0857.HK`。
- `0386.HK` 的成交量达标，但趋势和主题排名不足，只能作为能源主题广度观察点。

## 信心最弱的地方

最弱的是“这份快照到底能不能代表 2025-12-31 的实时市场状态”。`as_of_date` 与 `quote_trade_date` 冲突太大，所有价格、均线、成交量和 risk_state 都只能作为历史回放诊断，而不能作为日期对齐的实盘信号。

第二弱的是趋势延续判断。前三名趋势分数都很高，但 `volume_ratio_20` 只有 `0.1898` 到 `0.3079`，说明不是健康放量确认。低量高位趋势最容易在 T+3/T+5 变成 timing error。

第三弱的是动态选股本身。后验摘要里 `symbol_selection_error` 已经有 `138` 次，且最近互联网平台仍有 selected-vs-best miss。今天虽然前三名不在互联网平台，但共同问题仍是“模型 leader 看起来顺眼，历史通过率却不好”。

## 仍然缺失的证据

- 日期对齐的 2025-12-31 行情、成交量和均线数据。
- 广度证据：上涨家数、行业扩散、港股主指数与 ETF 是否同步确认。
- ETF 确认：`2800.HK`、`3033.HK`、`3067.HK` 是否真正站上关键均线并放量，而不是低量反弹。
- 同主题 peer-relative 数据：尤其是 `0857.HK` vs `0883.HK`/`0386.HK`、`0941.HK` vs `0728.HK`、`0006.HK` vs `0002.HK`。
- 历史 risk veto 的修复证据：低 pass_rate 标的是否出现过新的、可验证的改善窗口。

## 可能失败模式

1. **风险控制错误**：如果忽略 `actionable_candidates` 为空和 `symbol_risk_veto`，把 `0857.HK`、`0941.HK`、`0006.HK` 升级成行动候选，就会直接违反当前规则。
2. **时机错误**：趋势分数高但成交量弱，容易出现 T+3/T+5 回撤；即使中期趋势没坏，短线入场也可能太早。
3. **symbol-selection error**：如果 leader 被 veto 后机械切到同主题第二名，例如从 `0857.HK` 切到 `0883.HK`，但没有证明后者相对强度改善，这会把“避开坏 leader”误读成“替代品可买”。

动态选择相关的未来错误分类：今天最可能不是 theme error，而是 **risk-control error** 和 **symbol-selection error**；若未来价格短线回撤但中期趋势保持，则归为 **timing error**。

## 下一轮优先级

1. 先修复/确认日期对齐：没有 date-aligned evidence 前，historical replay 的排名只能诊断，不能升级。
2. 对前三个主题做 peer audit：energy、telecom-dividend、utilities-defensive 各自比较 leader 与同主题替代品，而不是只看总分。
3. 把成交量作为升级前置门：趋势分数再高，只要 `volume_ratio_20` 低于门槛，就只写触发条件，不写行动建议。
4. 检查 ETF 与广度：若 `2800.HK` 和相关 ETF 没有放量确认，单名股票不升级。

## 给下一次自己的短句

今天的小章鱼不要被漂亮趋势分数骗到。  
`diagnostic_only` 不是“差一点可以买”，而是“证据还没够”。  
空的 `actionable_candidates` 是一个刹车，不是一个谜题。
