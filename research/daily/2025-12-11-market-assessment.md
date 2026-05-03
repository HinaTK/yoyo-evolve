# 2025-12-11 港股/ETF市场评估（historical）

> 生成时间：2025-12-11 16:09  
> 用途：历史回放基线研究；仅作推荐研究，不代表真实持仓管理。  
> 风险设定：balanced；单一标的建议上限 10%；单一主题建议上限 30%；不使用杠杆、不使用反向 ETF；不确定时默认 `watch_only`。

## 1. 市场雷达事实摘要

### 1.1 市场状态

**事实：**
- 市场雷达给出的整体风险状态为 `risk_off`。
- 雷达样本中，股票平均 1 日涨跌幅为 **-0.949%**，ETF 平均 1 日涨跌幅为 **-1.82%**。
- 主要指数/ETF表现偏弱：
  - `2800.HK` 收 **26.00**，1 日 **-0.91%**，接近 ma20 **25.993**，低于 ma60 **26.36**，`regime_flags` 为 `range`。
  - `3033.HK` 收 **4.726**，1 日 **-2.15%**，低于 ma20 **4.7682** 与 ma60 **4.9981**，`regime_flags` 为 `downtrend`。
  - `3067.HK` 收 **10.15**，1 日 **-2.40%**，低于 ma20 **10.238** 与 ma60 **10.7185**，`regime_flags` 为 `downtrend`。

**解读：**
- 当前不是全面风险偏好扩张的盘面。广义港股 ETF 横盘，恒生科技 ETF 处于下跌结构，说明成长/科技Beta缺少确认。
- 在 `risk_off` 背景下，动量型单一股票需要更高证据门槛；优先考虑趋势明确、现金流/股息/资源类支撑更强的主题。

### 1.2 主题强弱排序（雷达层）

**事实：按确定性排序模型的 theme_summary：**

| 排名 | 主题 | 平均分 | 主题领先标的 | 领先分数 | 领先标的是否合格 |
|---:|---|---:|---|---:|---|
| 1 | telecom-dividend | 67.92 | `0941.HK` | 76.59 | 是 |
| 2 | utilities-defensive | 62.16 | `0006.HK` | 71.33 | 是 |
| 3 | energy | 56.22 | `0857.HK` | 79.93 | 是 |
| 4 | financials-bank | 55.34 | `0005.HK` | 55.34 | 否 |
| 5 | financials-exchange | 47.73 | `0388.HK` | 47.73 | 是 |
| 6 | hong-kong-broad-market | 44.67 | `2800.HK` | 44.67 | 否 |
| 7 | consumer-discretionary | 14.78 | `2020.HK` | 39.71 | 否 |
| 8 | internet-platform | 13.81 | `9618.HK` | 63.03 | 是 |
| 9 | hang-seng-tech | 0.00 | `3033.HK` | 0.00 | 否 |
| 10 | consumer-tech | 0.00 | `1810.HK` | 0.00 | 否 |
| 11 | financials-insurance | 0.00 | `1299.HK` | 0.00 | 否 |
| 12 | healthcare-biotech | 0.00 | `2269.HK` | 0.00 | 否 |
| 13 | healthcare-pharma | 0.00 | `1177.HK` | 0.00 | 否 |

**解读：**
- 最强主题集中在 **高股息/防御/能源**：`telecom-dividend`、`utilities-defensive`、`energy`。
- 科技和互联网整体仍弱。即使 `internet-platform` 内部有 `9618.HK` 相对强，但主题平均分只有 13.81，说明它更像局部相对强，而不是板块共振。
- `hang-seng-tech`、`consumer-tech`、医疗相关主题均未形成可行动趋势。

## 2. 雷达主题在交易宇宙中的可操作性

本次雷达主题均在交易宇宙内有代表标的；没有需要标记为“外部机会、后续考虑加入”的强雷达主题。以下比较只把 `actionable_candidates` 作为可升级候选层；`diagnostic_candidates` 只用于解释和观察。

### 2.1 energy：当前最强可操作主题

**交易宇宙内标的：** `0857.HK`、`0883.HK`、`0386.HK`

**事实：**
- `0857.HK` 是唯一进入 `actionable_candidates` 的标的：
  - 分数 **79.93**，主题排名 1/3；
  - 收 **11.63**，1 日 **+1.48%**；
  - ma20 **10.8135**，ma60 **10.1555**，价格高于 ma20 与 ma60，且 ma20 高于 ma60；
  - `volume_ratio_20` **1.0735**，成交量确认；
  - `range_pos_60` **1.0623**，处在 60 日区间上沿/突破区；
  - `regime_flags` 为 `uptrend`；
  - `qualified_for_action` 为 true。
- `0883.HK` 分数 **73.00**，1 日 **+2.11%**，同为 `uptrend`，但被标记为 `diagnostic_only`，原因是 `not_theme_score_leader`。
- `0386.HK` 分数 **15.72**，低于观察门槛，且低于 ma60，主题内明显落后。

**解读：**
- `energy` 是今天最清晰的可行动主题，最佳表达是 `0857.HK`，不是涨幅更大的 `0883.HK`。原因是确定性排序选择了主题领先、成交确认、均线结构完整的 `0857.HK`。
- `0883.HK` 可作为同主题强度确认，但不能在本报告中越过 `0857.HK` 成为升级标的，因为它只是诊断候选。
- 风险点是 `0857.HK` 的 `range_pos_60` 已高于 1，短线存在追高和回撤风险；如果后续跌回 60 日区间内且成交放大，需要降低行动等级。

### 2.2 telecom-dividend：强防御主题，但今日不是唯一可升级层

**交易宇宙内标的：** `0941.HK`、`0728.HK`

**事实：**
- `0941.HK` 分数 **76.59**，主题排名 1/2；收 **84.75**，1 日 **+0.41%**；价格高于 ma20 **81.1925** 与 ma60 **79.7225**，ma20 高于 ma60，`regime_flags` 为 `uptrend`。
- `0941.HK` 出现在 `diagnostic_candidates` 与 `top_candidates` 中，`qualified_for_action` 为 true，但不在唯一的 `actionable_candidates` 列表内。
- `0728.HK` 分数 **59.26**，成交量较强（`volume_ratio_20` **1.3464**），但主题排名 2/2，且 `qualified_for_action` 为 false。

**解读：**
- `telecom-dividend` 主题强度高，适合在 `risk_off` 环境中作为防御观察主线。
- 交易宇宙内最佳表达是 `0941.HK`；`0728.HK` 更适合作为主题广度确认。
- 由于输出规则要求只有 `actionable_candidates` 才能进入升级考虑，而 `0941.HK` 不在该层，本报告不把它升级为当日主推，只列为高优先级观察。

### 2.3 utilities-defensive：防御强，但成交与排序层限制使其偏观察

**交易宇宙内标的：** `0006.HK`、`0002.HK`

**事实：**
- `0006.HK` 分数 **71.33**，主题排名 1/2；价格高于 ma20 **63.41** 与 ma60 **62.3317**，`regime_flags` 为 `uptrend`。
- `0006.HK` 的 `volume_ratio_20` 为 **0.7579**，没有成交量异常放大。
- `0002.HK` 分数 **52.98**，但 `volume_ratio_20` 只有 **0.3866**，并有 `low_volume_ratio_20_below_0_6` 与 `not_theme_score_leader` disqualifiers。
- `0006.HK` 不在 `actionable_candidates`，只在 `all_ranked` 中显示 `qualified_for_action` 为 true。

**解读：**
- `utilities-defensive` 是强防御主题，但今天不是确定性升级层的一号候选。
- 最佳表达是 `0006.HK`，`0002.HK` 只能作为低成交防御背景参考。
- 若市场继续 `risk_off`，该主题值得在后续会话中跟踪是否进入 `actionable_candidates`。

### 2.4 internet-platform：内部有相对强者，但缺少板块/ETF确认

**交易宇宙内标的：** `9618.HK`、`3690.HK`、`0700.HK`、`9988.HK`、`1024.HK`

**事实：**
- 主题平均分仅 **13.81**，但 `9618.HK` 是主题领先，分数 **63.03**。
- `9618.HK` 价格略高于 ma20 **115.2223** 与 ma60 **107.8539**，`regime_flags` 为 `uptrend`，但低于行动分数 65，`qualified_for_action` 为 false。
- `0700.HK`、`9988.HK`、`1024.HK` 均处于 `downtrend` 或低分状态；其中 `0700.HK` 与 `9988.HK` 还有后验风控 veto，历史 pass_rate 较低且出现过 symbol_selection_error。
- 恒生科技 ETF `3033.HK`、`3067.HK` 均为 `downtrend`，分数为 0，并带有 symbol_risk_veto。

**解读：**
- 交易宇宙内最佳互联网平台表达是 `9618.HK`，但它只是观察候选，不满足升级门槛。
- 由于科技 ETF 没有确认，且稳定规则要求低通过率/反复误读标的必须有广义市场和 ETF 确认，今天不应升级 `0700.HK`、`9988.HK` 或科技 ETF。
- 该主题当前更适合记录“相对强者是谁”，而不是发出进攻性推荐。

### 2.5 broad-market 与 hang-seng-tech：ETF确认偏弱

**交易宇宙内标的：** `2800.HK`、`3033.HK`、`3067.HK`

**事实：**
- `2800.HK` 分数 **44.67**，低于 watch 门槛 45，且带有 `symbol_risk_veto`：pass_rate=0.127 over 55 evaluated calls。
- `3033.HK` 与 `3067.HK` 分数均为 **0**，`regime_flags` 均为 `downtrend`，且均有 `symbol_risk_veto`。
- `3033.HK` 低于 ma20 与 ma60；`3067.HK` 也低于 ma20 与 ma60。

**解读：**
- 广义市场 ETF未提供足够确认，恒生科技 ETF明确不支持科技/互联网主题升级。
- 在后验规则约束下，今天不应把 ETF 弱反弹或单日波动当成趋势确认。
- ETF层面的结论是：**不支持提高整体风险暴露**。

### 2.6 其他主题：消费、保险、医疗暂不行动

**事实：**
- `consumer-discretionary` 平均分 **14.78**，主题领先 `2020.HK` 分数 **39.71**，低于 watch 门槛。
- `consumer-tech` 的 `1810.HK` 分数 **0**，1 日 **-3.60%**，低于 ma20 与 ma60，并有 symbol_risk_veto。
- `financials-insurance` 的 `1299.HK` 分数 **0**，处于 `downtrend`。
- `healthcare-biotech`、`healthcare-pharma` 主题分数为 **0**；尽管 `2269.HK` 1 日 **+0.84%**，但仍低于 ma20 与 ma60，`regime_flags` 为 `downtrend`。

**解读：**
- 这些主题缺少趋势、ETF或主题内部确认，不适合今日升级。
- 对 `1810.HK` 尤其需要保持纪律：它既处于下跌结构，又有后验负收益/ adverse breach 记录，不能因单日成交量或波动直接转多。

## 3. 今日突出标的

### 3.1 可升级考虑层：`0857.HK`

**事实：**
- `0857.HK` 是唯一 `actionable_candidates`：score **79.93**，`qualified_for_action` true。
- 具备 7 项正面 flags：`score_meets_watch_threshold`、`price_above_ma20`、`price_above_ma60`、`ma20_above_ma60`、`volume_confirmed`、`constructive_range_position`、`score_meets_action_threshold`。
- 没有 disqualifiers。

**解读：**
- 若必须从今日交易宇宙中选一个最清晰的 swing 候选，`0857.HK` 是当前最佳表达。
- 但它处于 60 日区间高位，买点质量需要用回撤承接或继续放量突破来确认；不适合在没有触发条件的情况下盲目追价。

### 3.2 观察层：`0941.HK`、`0883.HK`、`0006.HK`、`9618.HK`

**事实：**
- `0941.HK`：score **76.59**，强防御主题领先，但不在 `actionable_candidates`。
- `0883.HK`：score **73.00**，能源同主题确认，但因不是主题分数领先而 `diagnostic_only`。
- `0006.HK`：score **71.33**，防御公用事业领先，但未进入 `actionable_candidates`。
- `9618.HK`：score **63.03**，互联网平台相对强者，但低于 action 阈值，且缺少科技 ETF确认。

**解读：**
- 这些标的有研究价值，但今天只作为主题确认或后续候选池，不做升级。
- `0941.HK` 与 `0006.HK` 可用于监测防御资金是否继续抱团；`0883.HK` 用于确认能源主题不是单一股票现象；`9618.HK` 用于观察互联网平台是否出现同主题扩散。

## 4. 风险姿态与执行纪律

**事实：**
- 市场状态为 `risk_off`。
- 科技 ETF `3033.HK`、`3067.HK` 均为 `downtrend` 且有后验风控 veto。
- `2800.HK` 低于 watch 分数且有 symbol_risk_veto。
- 今日只有一个确定性 `actionable_candidates`，即 `0857.HK`。

**解读：**
- 今日风险姿态应为：**低仓位、选择性、只接受强趋势确认，不扩大主题暴露**。
- 不应因为能源/电信/公用事业强，就判断全市场转强；当前更像防御与资源局部占优。
- 对科技、互联网、消费、医疗的反弹应先当作观察，不当作趋势恢复。
- 成本门槛要求预期 swing edge 明显超过 35 bps 往返成本与 100 bps 最小边际；因此弱信号不值得交易。

## 5. 今日结论

**事实结论：**
1. 市场雷达为 `risk_off`，股票和 ETF 平均日表现均为负。
2. 最强主题是 `telecom-dividend`、`utilities-defensive`、`energy`。
3. 交易宇宙内唯一确定性可升级候选是 `0857.HK`。
4. 恒生科技 ETF 与主要科技/互联网权重缺少确认，不能支持科技主题升级。
5. 广义 ETF `2800.HK` 未达 watch 门槛，且有后验风控 veto。

**操作解释：**
- 今日的主线不是全面进攻，而是从 `risk_off` 盘面中寻找少数趋势完整的防御/资源标的。
- `0857.HK` 是当前最佳行动候选；`0941.HK`、`0006.HK`、`0883.HK` 是高优先级观察；科技与消费继续保持 `watch_only`。

## 6. 今日高优先级研究问题

1. `0857.HK` 的能源强势是否由油价、人民币资产偏好、股息重估或行业政策驱动？这些驱动中哪一个最可能持续 14-90 天？
2. `0857.HK` 相对 `0883.HK` 的优势是否只是模型排序结果，还是在成交、回撤控制、基本面或资金流上也更优？
3. `0941.HK` 与 `0006.HK` 的防御强势是否代表资金真正转向高股息，还是只是 `risk_off` 当日避险轮动？
4. `3033.HK`、`3067.HK` 何时才算重新提供科技 ETF确认：收复 ma20、收复 ma60、成交放大，还是相对 `2800.HK` 转强？
5. 在 `2800.HK` 有后验风控 veto 的情况下，是否需要增加更适合衡量港股广度的确认指标，以避免单一 ETF 历史误差压制整体市场判断？
