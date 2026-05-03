# 2025-12-22 投资复盘反思

时间：2025-12-22 20:52  
会话：historical  
模式：recommendation-only / research-only

## 结论先写

今天不应该给出新的可执行买入。虽然确定性排名把 `0857.HK`、`0941.HK`、`0006.HK` 排在最前，并且它们的分数都超过 action threshold，但 `actionable_candidates` 为空；同时三个最高分候选都被 `symbol_risk_veto` 拦住。按照现有规则，这些只能作为诊断线索，不能升级为 `buy_candidate`、`hold` 或 `accumulate`。

我的建议状态：整体 `watch_only`。

## 事实层

- 市场摘要为 `risk_off`。
- 平均股票日变动为 -0.946%，ETF 平均日变动为 -1.847%，风险偏好偏弱。
- 强势集中在防御/高股息/能源：
  - `0857.HK` 分数 81.90，能源主题第一，价格高于 MA20/MA60，成交量确认，但有 `symbol_risk_veto`。
  - `0941.HK` 分数 76.46，电信高息主题第一，价格高于 MA20/MA60，成交量确认，但有 `symbol_risk_veto`。
  - `0006.HK` 分数 75.51，公用事业主题第一，价格高于 MA20/MA60，成交量确认，但有 `symbol_risk_veto`。
- 互联网平台和恒生科技 ETF 多数仍在下行或弱修复：`0700.HK`、`9988.HK`、`1024.HK`、`3033.HK`、`3067.HK` 均未给出足够升级证据。
- `0883.HK` 是一个值得注意的能源 peer：分数 72.45，趋势强，且没有 `symbol_risk_veto`，但它不是主题分数 leader，成交量未确认，不能机械替代 `0857.HK`。
- 历史回放存在重大数据一致性问题：`as_of_date` 是 2025-12-22，但报价字段为 2026-04-28。这使得所有排名只能作为诊断，不应视为日期对齐的实盘确认。

## 今日建议

### 1. `0857.HK`：`watch_only`

理由：能源主题强，趋势和动量分数最高，价格位于 MA20/MA60 之上，并且成交量确认。  
不能升级的原因：`symbol_risk_veto` 很重，历史样本显示 pass_rate=0.091，avg_return_pct=-13.388，并包含 adverse breach 与 symbol_selection_error。  
触发条件：只有在日期对齐数据中继续站上 MA20/MA60、能源主题仍领先、且 `0857.HK` 相对 `0883.HK` 不再出现 selected-vs-best 式落后时，才可重新评估。  
失效条件：跌回 MA20，或能源主题 ETF/peer 不确认，或 `0883.HK` 明显继续强于 `0857.HK`。  
信心：方向低到中，行动低。

### 2. `0941.HK`：`watch_only`

理由：电信高息主题仍有防御属性，`0941.HK` 价格高于 MA20/MA60，趋势分数满分。  
不能升级的原因：同样被 `symbol_risk_veto` 拦截，历史 pass_rate=0.100，且当前市场是 `risk_off`，防御强不等于短线有足够边际。  
触发条件：继续高于 MA20/MA60，成交量维持，且相对 `0728.HK` 的强度不恶化。  
失效条件：跌破 MA20，或高息防御板块转弱，或出现放量回落。  
信心：防御主题中等，短线行动低。

### 3. `0006.HK`：`watch_only`

理由：公用事业主题平均分最高，`0006.HK` 是主题 leader，趋势完整，价格高于 MA20/MA60。  
不能升级的原因：`symbol_risk_veto` 最严，pass_rate=0.000 over 7 evaluated calls，avg_return_pct=-6.152，并有 adverse breach。  
触发条件：必须看到新的日期对齐证据证明 `0006.HK` 相对 `0002.HK` 的 peer-relative strength 改善，而不是只依赖当前分数第一。  
失效条件：跌破 MA20，或 `0002.HK` 更稳且回撤更小，或防御主题失去相对优势。  
信心：主题中等，标的选择低。

### 4. `0883.HK`、`0002.HK`、`0728.HK`：替代观察，不行动

这些标的没有同等程度的历史风险 veto（或风险更干净），但它们不是各自主题 leader，且部分缺少成交量确认。今天最容易犯的错是：看到 leader 被 veto 后，马上把主题判断迁移到第二名。这仍然是 symbol-selection error 的温床。替代 peer 必须独立通过趋势、成交、相对强度和风险门槛。

## 信心最弱的地方

1. **日期一致性最弱。** `as_of_date` 与报价日期冲突，任何价格、均线、成交量结论都不能当成 2025-12-22 的完整现场证据。
2. **动态选股最弱。** 最高分候选全部被 `symbol_risk_veto` 拦截，说明模型排序和后验风控在冲突。
3. **短线 timing 最弱。** 市场为 `risk_off`，但防御/能源主题强；这可能是持续轮动，也可能是拥挤防御交易的尾段。
4. **主题替代表达最弱。** `0883.HK` 比 `0857.HK` 风险更干净，但不是主题 leader，且成交量不足以证明它能直接替代。

## 仍然缺失的证据

- 日期对齐的 2025-12-22 当日价格、成交量、MA20/MA60 与 60 日区间位置。
- 主题层面的 ETF 或行业指数确认，尤其是能源、电信、公用事业是否同步强于大市。
- `0857.HK` vs `0883.HK`、`0941.HK` vs `0728.HK`、`0006.HK` vs `0002.HK` 的近期 peer-relative performance。
- 是否存在宏观/商品/利率驱动，使能源与防御高息股的强势具备延续性。
- 后续 T+3/T+5 是否继续出现 selected-vs-best miss。

## 今日建议的可能失败模式

1. **symbol-selection error。** 动态排名挑中 `0857.HK`、`0941.HK`、`0006.HK`，但三者都有明确 `symbol_risk_veto`；如果我仍升级它们，最可能重演“分数 leader 不是最佳 peer”的错误。
2. **timing error。** 防御/能源强势可能已经短线拥挤，`range_pos_60` 接近或超过高位，追入容易遇到 T+3/T+5 回撤。
3. **risk-control error。** `actionable_candidates` 为空时仍把 diagnostic candidate 当行动信号，是规则执行失败，不是市场判断失败。

## 动态选择错误分类

今天的候选来自 dynamic symbol selection。若未来表现不佳，我会优先分类为：

- `0857.HK`：symbol-selection error，其次 timing error。能源主题可能是对的，但 `0883.HK` 可能是更干净表达。
- `0941.HK`：symbol-selection error。电信防御主题可能成立，但历史通过率和 peer 替代检查不足。
- `0006.HK`：symbol-selection error + risk-control error。主题强不够，pass_rate=0.000 的 veto 不能被趋势分数覆盖。

## 下一周期优先级调整

1. 先修复证据：要求日期对齐数据，再读取排名。
2. 若 `actionable_candidates` 仍为空，保持全部 `watch_only`，不要从 `diagnostic_candidates` 中硬挑交易。
3. 对每个被 veto 的主题 leader，做同主题 peer 表达检查：只允许风险更干净且趋势、成交、相对强度同时改善的 peer 进入候选。
4. 优先观察 `0883.HK` 相对 `0857.HK`、`0002.HK` 相对 `0006.HK`、`0728.HK` 相对 `0941.HK`，不要只看绝对分数。
5. 对互联网平台和恒生科技继续要求 ETF 确认；在 MA60 未收复、低通过率未改善前，不升级单名。

今天的小章鱼结论：我看见了强主题，但也看见了门禁全关。门禁全关的时候，不要从窗户爬进去。
