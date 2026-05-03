# 2026-01-12 投资复盘反思（historical）

## 结论摘要

今天的历史回放只能形成低置信的诊断结论，不能形成行动建议。表面上市场摘要显示 `risk_on`，ETF 与股票平均单日涨幅分别为 1.70% 和 1.606%，但输入存在关键约束：`as_of_date=2026-01-12`，而报价字段 `quote_trade_date=2026-04-29`。因此，所有排名只能作为回放审计和下一轮观察清单，不能当作当日实时确认。

更重要的是，确定性排名中 `actionable_candidates` 为空。即使 `0857.HK`、`0941.HK`、`0002.HK` 的分数分别达到 84.42、81.98、76.08，且趋势结构较强，它们都被 `symbol_risk_veto` 拦截，只能归类为 `diagnostic_only` / `watch_only`。今天不应把高分诊断候选升级为 `buy_candidate`、`hold` 或 `accumulate`。

## 今日建议状态

- `0857.HK`：`watch_only`。能源主题强，价格高于 MA20/MA60，`volume_ratio_20=1.2356`，但 `symbol_risk_veto=true`，历史 pass_rate=0.182，平均回报为负，并包含 repeated `symbol_selection_error`。不得升级。
- `0941.HK`：`watch_only`。电讯股趋势和放量都较好，`volume_ratio_20=1.5041`，但 `symbol_risk_veto=true`，pass_rate=0.033，近期有 adverse breach 与 selection error。不得升级。
- `0002.HK`：`watch_only`。防御公用事业趋势完整，但样本 pass_rate=0.000、平均回报为负，且被 veto。不得升级。
- `0386.HK`、`3690.HK`、`2331.HK`、`9992.HK`、`6862.HK`、`2269.HK` 等非 veto 或较干净的同主题替代项：仍为 `watch_only`。它们没有进入 `actionable_candidates`，且多数存在非主题 leader、低分、下跌趋势、MA 未收复或缺少相对 veto leader 的新鲜强势证明。

## 信心最弱的地方

1. **日期一致性最弱**：回放日期与报价日期不一致，导致价格、均线、成交量和 regime flags 都不能视为 2026-01-12 的现场证据。
2. **动态选股信心弱**：前排候选全部是动态排名产生的 theme leader，但都被 `symbol_risk_veto` 拦截；高 trend_score 不能抵消低 pass_rate 与 selection error。
3. **替代 peer 信心弱**：例如能源里 `0386.HK` 没有 veto 且放量，但它不是 theme leader，分数仅 50.67，低于行动门槛；不能因为 `0857.HK` 被 veto 就机械切换。
4. **短期时点信心弱**：后验摘要中 `timing_unclear=84`，近期 `2800.HK`、`9988.HK`、科技 ETF 的 T+3/T+5 失败仍多，今天不应假设风险偏好能延续。

## 仍缺少的证据

- 日期对齐的 2026-01-12 收盘价、成交量、MA20/MA60、ETF 位置和市场宽度。
- `2800.HK`、`3033.HK`、`3067.HK` 对风险偏好的同步确认，尤其是是否放量站上关键均线。
- 对 `0857.HK`、`0941.HK`、`0002.HK` 的 veto 复核：低 pass_rate 是否来自错误方向、错误时点，还是系统性选股偏差。
- 同主题 peer-relative 证据：若 leader 被 veto，替代 peer 必须相对被 veto leader 和最近 best peer 展示持续强势，而不是只拥有更少的风险标签。
- T+3/T+5 与 T+10/T+20 分层表现，用来判断今天的问题是 timing error 还是 theme/symbol-selection error。

## 今日最可能的失败模式

1. **risk-control error**：看到 `risk_on` 与高分诊断候选后忽略 `actionable_candidates=[]` 和 `symbol_risk_veto`，把雷达信号误升为行动建议。
2. **symbol-selection error**：动态模型选择 `0857.HK`、`0941.HK`、`0002.HK` 这类 theme leader，但后验显示其历史 pass_rate 很低，未来可能继续输给同主题更合适的 peer 或整体不产生正收益。
3. **timing error**：若风险偏好只是短线反弹，追随高位趋势股（尤其 range_pos_60 接近或超过高位的能源、电讯、防御股）容易在 T+3/T+5 出现回撤。

## 对动态选择错误的分类

- `0857.HK`：主要风险是 `symbol-selection error`，次要是 `timing error`。能源主题强，但该 symbol 历史平均回报和 pass_rate 不支持升级。
- `0941.HK`：主要风险是 `symbol-selection error` 与 `risk-control error`。趋势和放量诱人，但 veto 与低 pass_rate 必须优先。
- `0002.HK`：主要风险是 `risk-control error`。防御趋势看似稳健，但样本 pass_rate=0.000，不能把低波动错当高胜率。
- 互联网平台主题：今天 `9618.HK` 是主题 leader，但也被 veto；近期 selected-vs-best 反复显示 `0700.HK`、`9988.HK` 经常错过 best peer。下一次不能只按当前 leader 或熟悉大票升级，必须点名最近 best peer 并证明相对强势改善。

## 下一周期优先级调整

1. **先做数据门禁**：只有当 `as_of_date` 与报价/均线日期一致时，才允许从诊断转向行动；否则默认 `watch_only`。
2. **先审 veto，再找替代**：前排候选被 `symbol_risk_veto` 拦截时，先复核 veto 原因和历史窗口，不要立刻切到第二名或低风险标签 peer。
3. **ETF 与宽度确认提前**：任何单股升级前，先确认 `2800.HK`、相关主题 ETF、成交量和 MA60 修复；没有 ETF 确认则不升级。
4. **同主题 peer-relative 检查制度化**：每个动态候选都要列出 theme leader、recent best peer、候选相对二者的强弱；缺少这项则只保留雷达。
5. **把行动门槛置于分数之前**：`qualified_for_watch=true` 只代表观察；`diagnostic_only=true`、`qualified_for_action=false` 或 `actionable_candidates=[]` 任何一个出现，都阻止行动升级。

## 记忆更新判断

允许更新长期记忆。后验中 `symbol_selection_error=143`、`timing_unclear=84`、近期多次 selected-vs-best miss，以及今天前排动态候选全部被 `symbol_risk_veto` 拦截，说明需要继续强化“先 veto 审计、再 peer 替代”的规则。已将本次模式以简短、可执行方式补入长期记忆，并在投资日志追加日期条目。
