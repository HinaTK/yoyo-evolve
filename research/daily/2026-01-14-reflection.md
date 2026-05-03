# 2026-01-14 投资复盘反思

## 结论摘要

今天这轮历史回放只能给出低置信度的审计结论，不能给出行动升级。核心原因有三点：

1. `actionable_candidates` 为空，直接阻断所有 `buy_candidate`、`hold`、`accumulate` 级别建议。
2. 排名前三的动态诊断候选 `0857.HK`、`0941.HK`、`0002.HK` 虽然分数和趋势形态较强，但全部被 `symbol_risk_veto` 拦截，只能进入 veto 审计队列。
3. 回放 `as_of_date=2026-01-14`，但报价字段显示 `quote_trade_date=2026-04-29`，日期不对齐；这些排名只能作为非实时诊断，不能视作当日确认信号。

因此今日基线建议是：不做行动替代，不从低排名 peer 中挖机会；把本轮作为“veto 审计 + peer-relative 复核”的基线样本。

## 市场与主题观察

- 快照给出的 `market_summary.risk_state` 是 `risk_on`，股票平均 1 日涨幅约 1.606%，ETF 平均约 1.7%。表面上市场偏风险偏好。
- 主题排名显示防守公用事业、通信分红、银行、能源靠前：`utilities-defensive` 平均 75.47，`telecom-dividend` 平均 75.00，`financials-bank` 71.01，`energy` 69.67。
- 但前排主题的可行动性被历史风险记录抵消：`0857.HK`、`0941.HK`、`0002.HK` 都是 theme leader，也都满足多项趋势条件，却全部因低 pass_rate、负平均回报或不利记录被 veto。
- 互联网平台出现日内反弹领涨，例如 `3690.HK` +3.55%、`9988.HK` +3.24%，但主题平均分只有 32.34，且近期 selected-vs-best 错误密集，不能把单日反弹升级为主题确认。

## 今日建议状态

- `0857.HK`：`watch_only` / veto audit。分数 84.42、趋势强、成交确认，但 `symbol_risk_veto=true`，33 次评估 pass_rate 0.152、平均回报 -4.514%，且有 `symbol_selection_error` 记录。不能行动。
- `0941.HK`：`watch_only` / veto audit。分数 81.98，趋势与量能都好，但 30 次评估 pass_rate 0.033、平均回报 -0.960%，并有近期不利破阈和选择错误记录。不能行动。
- `0002.HK`：`watch_only` / veto audit。分数 76.08，公用事业 leader，但样本 pass_rate=0 且平均回报 -2.133%，只可观察。
- 其他同主题 peer：不做行动替代。即使个别 peer 的 `symbol_risk_veto=false`，只要没有进入 `actionable_candidates`，并且没有证明同时跑赢 veto leader 与最近 best peer，都只能留在审计层。

## 信心最弱的位置

1. **日期对齐最弱**：`as_of_date` 与 `quote_trade_date` 明显不一致，这是本轮最大置信度折扣来源。
2. **动态选择信心弱**：前排候选是模型动态选择结果，但历史 posterior 显示 `symbol_selection_error=151`，互联网平台尤其多次错过实际 best peer。
3. **行动门槛信心弱**：`actionable_candidates=[]`，说明即使诊断分数高，也没有候选真正通过行动清单。
4. **参数优化信心弱**：参数优化没有更新 active strategy；原因包括 samples、improvement、win_rate、sample_quality 未过关，说明不能通过调参来放松当前门槛。

## 仍缺少的证据

- 日期对齐的 2026-01-14 当日价格、成交量、MA20/MA60 与 ETF 确认。
- 每个 theme leader 与同主题 peer 的近期相对强弱表，特别是 selected-vs-best bps 是否已改善。
- 对被 veto 符号的人工复核：低 pass_rate 是模型选择错误、时点错误，还是该符号结构性不适合当前策略。
- 若要考虑替代 peer，需要它先进入 `actionable_candidates`，并展示相对 veto leader 与最近 best peer 的新鲜强势。
- 宽基与主题 ETF 的同步确认，尤其是成交量、均线修复和广度，而不只是单日涨幅。

## 可能失败模式

1. **symbol-selection error**：继续选择分数最高的 theme leader，但该 leader 再次跑输同主题实际 best peer。风险最高，已被近期互联网平台 selected-vs-best 记录反复证明。
2. **risk-control error**：把 `qualified_for_watch=true` 或高 `trend_score` 误读为行动信号，忽略 `symbol_risk_veto`、`diagnostic_only=true`、`qualified_for_action=false` 和空行动清单。
3. **timing error**：在风险偏好看似改善时提前升级，但 T+3/T+5 窗口再次被回撤或震荡吞没，尤其是在日期不对齐、缺乏实时 ETF 确认时。

## 动态选择错误分类

本轮推荐来源包含动态 symbol selection，但没有行动候选。若未来沿用今天前排诊断结果，最可能的错误分类如下：

- `0857.HK`：主要是 `risk-control error`，次要是 `symbol-selection error`。趋势分高但 posterior 负证据很重，不能用高分覆盖 veto。
- `0941.HK`：主要是 `risk-control error`。形态与成交看似完整，但历史 pass_rate 极低，且存在近期 adverse breach。
- `0002.HK`：主要是 `risk-control error` 与样本不足风险。样本少但 pass_rate=0，不能因为防守属性就升级。
- 互联网平台候选：主要是 `symbol-selection error`。近期 best peer 在 `9618.HK`、`9988.HK`、`0700.HK`、`3690.HK`、`1024.HK` 间轮动，不能只按当前 leader 或单日涨幅选股。

## 下一周期优先级

1. 先修正日期对齐问题：没有 date-aligned snapshot，不做行动升级。
2. 先审计 veto，再看替代：对 `0857.HK`、`0941.HK`、`0002.HK` 解释 veto 是否仍有效；未解释前只保留观察。
3. 对每个强主题建立 peer-relative 表：列出最近 T+3/T+5/T+10 的 best peer、selected_vs_best_bps、成交与均线差异。
4. 互联网平台只做 ETF-first 复核：必须看到 `3033.HK`/`3067.HK` 或宽基同步确认，再讨论单名。
5. 不降低成本门槛或 edge 门槛；参数优化未通过样本质量和改善门槛，现有保守策略继续有效。

## 记忆更新判断

posterior 显示 repeated `symbol_selection_error`、空行动清单与 top diagnostic veto 的组合仍是主线风险。本次已把“selected-vs-best 必须点名最近 best peer，并用 bps 证明改善”的规则再压实到长期记忆中。今日不新增宽泛主题判断，只新增更可执行的 peer-relative 检查要求。
