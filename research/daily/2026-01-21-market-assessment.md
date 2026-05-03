# 2026-01-21 港股市场评估

> 会话：historical  
> 研究员：yoyo-invest  
> 模式：recommendation_only  
> 适用周期：14-90 天 swing 观察  
> 结论状态：`watch_only` / veto audit

## 0. 数据与决策边界

### 事实
- 输入的 `as_of_date` 是 `2026-01-21`。
- 快照内多数字段的 `quote_trade_date` / `quote_trade_time` 显示为 `2026-04-29`，与本次历史回放日期不一致。
- 确定性排名的 `actionable_candidates` 为空：`[]`。
- 排名前三的 `diagnostic_candidates` 是 `0857.HK`、`0941.HK`、`0002.HK`，但三者均为 `diagnostic_only=true`，且 `qualified_for_action=false`，并带有 `symbol_risk_veto`。
- 稳定规则要求：非日期对齐报价、`actionable_candidates=[]`、`symbol_risk_veto` 均不能被 `risk_on` 覆盖。

### 解读
- 本报告只能作为历史回放下的市场雷达与风控审计，不应升级为即时买入建议。
- 今日没有确定性层面可升级的交易候选；所有候选最多进入观察、相对强弱复核或后续研究问题。

## 1. 市场雷达概览：先按主题强弱排序

### 事实
- 市场摘要显示 `risk_state` 为 `risk_on`。
- 雷达样本中，股票平均 1 日涨幅为 `1.606%`，ETF 平均 1 日涨幅为 `1.7%`。
- 当日雷达领涨：
  1. `3690.HK` 美团-W：`+3.55%`，theme=`internet-platform`，`regime_flags=["range"]`
  2. `9988.HK` 阿里巴巴-W：`+3.24%`，theme=`internet-platform`，`regime_flags=["range"]`
  3. `0388.HK` 香港交易所：`+2.99%`，theme=`financials-exchange`，`regime_flags=["range", "volume-expansion"]`
- 当日雷达落后：
  1. `1093.HK` 石药集团：`-0.59%`，theme=`healthcare-pharma`，`regime_flags=["downtrend"]`
  2. `0006.HK` 电能实业：`-0.38%`，theme=`utilities-defensive`，但仍为 `uptrend`
  3. `1177.HK` 中国生物制药：`-0.36%`，theme=`healthcare-pharma`，`regime_flags=["downtrend"]`

### 事实：确定性主题排名
| 排名 | theme | avg_score | leader | leader_score | leader_qualified |
|---:|---|---:|---|---:|---|
| 1 | `utilities-defensive` | 75.47 | `0002.HK` | 76.08 | true |
| 2 | `telecom-dividend` | 75.00 | `0941.HK` | 81.98 | true |
| 3 | `financials-bank` | 71.01 | `0005.HK` | 71.01 | true |
| 4 | `energy` | 69.67 | `0857.HK` | 84.42 | true |
| 5 | `financials-exchange` | 67.30 | `0388.HK` | 67.30 | true |
| 6 | `financials-insurance` | 58.00 | `1299.HK` | 58.00 | true |
| 7 | `hong-kong-broad-market` | 56.60 | `2800.HK` | 56.60 | true |
| 8 | `hang-seng-tech` | 43.52 | `3067.HK` | 44.39 | false |
| 9 | `internet-platform` | 32.34 | `9618.HK` | 72.27 | true |
| 10 | `consumer-discretionary` | 27.02 | `2020.HK` | 55.36 | false |
| 11 | `consumer-tech` | 0.00 | `1810.HK` | 0.00 | false |
| 12 | `healthcare-biotech` | 0.00 | `2269.HK` | 0.00 | false |
| 13 | `healthcare-pharma` | 0.00 | `1177.HK` | 0.00 | false |

### 解读
- 表面风险偏好偏强，但强势结构主要集中在防御现金流、运营商、银行、能源与交易所，而不是高 beta 科技 ETF。
- `internet-platform` 的日内涨幅亮眼，但主题均分只有 32.34；其内部强弱分化很大，不能用 `3690.HK`、`9988.HK` 单日反弹来代表整个互联网平台主题可交易。
- 医药与生物科技主题处于最弱层，多个成员仍在 `downtrend`，不适合逆势提前布局。

## 2. 哪些雷达主题在交易宇宙中可表达

### 事实
本次强主题均已在交易宇宙中有代表标的：
- `utilities-defensive`：`0002.HK`、`0006.HK`
- `telecom-dividend`：`0941.HK`、`0728.HK`
- `financials-bank`：`0005.HK`
- `energy`：`0857.HK`、`0883.HK`、`0386.HK`
- `financials-exchange`：`0388.HK`
- `financials-insurance`：`1299.HK`
- `hong-kong-broad-market`：`2800.HK`
- `hang-seng-tech`：`3033.HK`、`3067.HK`
- `internet-platform`：`0700.HK`、`9988.HK`、`3690.HK`、`1024.HK`、`9618.HK`

未发现“强雷达主题但不在交易宇宙中”的外部主题机会；因此今日不需要把任何主题标记为外部待加入机会。

### 解读
- 虽然多个强主题可在交易宇宙中表达，但可表达不等于可行动。
- 今日的确定性升级层为空；因此所有主题表达只能作为观察对象，而不是买入候选。

## 3. ETF 确认

### 事实
| ETF | theme | latest_close | pct_change_1d | ma20 | ma60 | range_pos_60 | volume_ratio_20 | score | 状态 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `2800.HK` | `hong-kong-broad-market` | 26.24 | +1.74% | 25.8446 | 26.1507 | 0.4981 | 1.1216 | 56.60 | `qualified_for_watch=true`, `qualified_for_action=false` |
| `3033.HK` | `hang-seng-tech` | 4.81 | +1.78% | 4.7717 | 4.9835 | 0.2131 | 0.6564 | 42.65 | below watch score |
| `3067.HK` | `hang-seng-tech` | 10.31 | +1.58% | 10.2455 | 10.6875 | 0.2039 | 1.0774 | 44.39 | below watch score |

### 解读
- `2800.HK` 对大盘有温和确认：价格站上 ma20 与 ma60，量能略高于 20 日均量，分数高于 watch 线但低于 action 线。
- 恒生科技 ETF 的确认不足：`3033.HK` 与 `3067.HK` 均低于 `min_watch_score=45`，且仍低于 ma60，说明科技反弹尚未形成足够的主题确认。
- 按“优先通过 ETF 确认主题”的规则，今日不支持把单只互联网或消费科技股升级为行动建议。

## 4. 强主题内部比较与最佳当前表达

> 注意：以下“最佳当前表达”只表示相对观察对象，不代表 `buy_candidate`。确定性层面的 `actionable_candidates=[]` 已将所有升级封顶为 `watch_only` / audit。

### 4.1 `energy`

#### 事实
| symbol | score | latest_close | pct_change_1d | ma20 | ma60 | range_pos_60 | volume_ratio_20 | 关键限制 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `0857.HK` | 84.42 | 11.98 | +2.66% | 10.853 | 10.2045 | 1.1084 | 1.2356 | `symbol_risk_veto`, `diagnostic_only=true` |
| `0883.HK` | 73.93 | 29.38 | +1.38% | 27.258 | 26.6937 | 0.8462 | 0.9994 | 非主题分数第一，`symbol_risk_veto` |
| `0386.HK` | 50.67 | 4.70 | +2.40% | 4.5865 | 4.9833 | 0.1864 | 2.2023 | 非主题分数第一，低于 ma60 |

#### 解读
- 最佳当前表达：`0857.HK`，但仅限观察。它是主题分数第一，趋势与动量都强，且价格高于 ma20/ma60。
- 不能行动的原因：`0857.HK` 有 `symbol_risk_veto`，历史评估显示 pass_rate=0.091、avg_return_pct=-1.658，并有 adverse breach 与 selection error 记录。
- `0386.HK` 虽然量能扩张显著，但趋势质量不如 `0857.HK`，且不是主题 leader；不能作为绕开 veto 的替代行动标的。

### 4.2 `telecom-dividend`

#### 事实
| symbol | score | latest_close | pct_change_1d | ma20 | ma60 | range_pos_60 | volume_ratio_20 | 关键限制 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `0941.HK` | 81.98 | 85.45 | +0.95% | 81.55 | 79.82 | 1.1119 | 1.5041 | `symbol_risk_veto`, `diagnostic_only=true` |
| `0728.HK` | 68.01 | 5.27 | +1.93% | 4.9625 | 5.0065 | 0.7656 | 1.6770 | 非主题分数第一，`symbol_risk_veto` |

#### 解读
- 最佳当前表达：`0941.HK`，但仅限观察。它是主题 leader，价格强于 ma20/ma60，量能扩张，range_pos_60 已高于 1。
- 风险：range_pos_60 高于 1 表示短线位置偏高，追价风险上升。
- 不能行动的原因：`0941.HK` 有 `symbol_risk_veto`，历史 pass_rate=0.000，且有 adverse breach 与 selection error 记录。

### 4.3 `utilities-defensive`

#### 事实
| symbol | score | latest_close | pct_change_1d | ma20 | ma60 | range_pos_60 | volume_ratio_20 | 关键限制 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `0002.HK` | 76.08 | 75.85 | +0.46% | 74.5825 | 73.9937 | 0.9407 | 1.2769 | `symbol_risk_veto`, `diagnostic_only=true` |
| `0006.HK` | 74.86 | 65.00 | -0.38% | 63.6225 | 62.4233 | 0.9524 | 1.3544 | 非主题分数第一，`symbol_risk_veto` |

#### 解读
- 最佳当前表达：`0002.HK`，但仅限观察。它是主题 leader，趋势结构完整。
- `0006.HK` 与 `0002.HK` 分数接近，但当日下跌且不是 leader；不能作为替代买入。
- 不能行动的原因：`0002.HK` 历史样本虽少但 pass_rate=0.000、avg_return_pct=-0.242，并被 `symbol_risk_veto` 阻断。

### 4.4 金融：`financials-bank`、`financials-exchange`、`financials-insurance`

#### 事实
| theme | symbol | score | pct_change_1d | range_pos_60 | volume_ratio_20 | 状态 |
|---|---|---:|---:|---:|---:|---|
| `financials-bank` | `0005.HK` | 71.01 | +0.28% | 0.8805 | 0.7907 | `symbol_risk_veto`, watch only |
| `financials-exchange` | `0388.HK` | 67.30 | +2.99% | 0.6766 | 1.5564 | `symbol_risk_veto`, watch only |
| `financials-insurance` | `1299.HK` | 58.00 | +2.16% | 0.4828 | 1.2945 | `symbol_risk_veto`, below action score |

#### 解读
- 最强的金融表达按分数是 `0005.HK`，但动量一般且被 veto。
- `0388.HK` 的单日表现更突出，并有 `volume-expansion`，但历史 pass_rate=0.000，不能升级。
- `1299.HK` 只适合作为保险板块回暖观察，尚未达到行动分数。

### 4.5 `internet-platform`

#### 事实
| symbol | score | latest_close | pct_change_1d | ma20 | ma60 | range_pos_60 | volume_ratio_20 | 状态 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `9618.HK` | 72.27 | 117.50 | +1.91% | 115.5027 | 107.9074 | 0.7952 | 0.7545 | 主题 leader，但 `symbol_risk_veto` |
| `9988.HK` | 44.75 | 130.60 | +3.24% | 127.52 | 138.9633 | 0.2200 | 0.7696 | below watch score，非 leader，`symbol_risk_veto` |
| `3690.HK` | 44.67 | 83.15 | +3.55% | 84.80 | 84.3275 | 0.3589 | 1.0194 | below watch score，低于 ma20/ma60 |
| `0700.HK` | 0.00 | 479.20 | +1.14% | 498.10 | 526.90 | 0.0364 | 0.8487 | `downtrend`，低 range，`symbol_risk_veto` |
| `1024.HK` | 0.00 | 43.52 | +2.93% | 45.25 | 58.3908 | 0.0305 | 0.8671 | `downtrend`，低 range，`symbol_risk_veto` |

#### 解读
- 最佳当前表达：`9618.HK`，但仅限观察。它是互联网平台主题中唯一分数超过 action 线的相对强者。
- 不能行动的原因：`9618.HK` 有 `symbol_risk_veto`，且没有进入 `actionable_candidates`。
- `9988.HK` 与 `3690.HK` 日涨幅更高，但分数低于 watch 线；这更像超跌或区间反弹，而不是确定性 swing 信号。
- 后验评估显示互联网平台近期存在明显 selected-vs-best 问题，过去多次 `0700.HK`、`9988.HK` 落后 `9618.HK`、`3690.HK` 或 `1024.HK`。因此今日不能用单日反弹重新升级 `0700.HK` 或 `9988.HK`。

### 4.6 `hong-kong-broad-market` 与科技 ETF

#### 事实
- `2800.HK`：score=56.60，`qualified_for_watch=true`，但 `symbol_risk_veto`，低于 action 分数。
- `3067.HK`：score=44.39，below watch score，且 `symbol_risk_veto`。
- `3033.HK`：score=42.65，below watch score，且 `symbol_risk_veto`。

#### 解读
- `2800.HK` 是大盘观察的最佳 ETF 表达，但不是交易候选。
- `3033.HK` 与 `3067.HK` 不能确认科技主题，今天只用于观察科技 beta 是否继续修复。

## 5. 风险姿态

### 事实
- 组合输入为 recommendation-only，未提供真实持仓；现金 100% 只是推荐模式背景，不代表真实资产配置指令。
- 风险规则：单一仓位上限 10%，主题上限 30%，不允许杠杆，不允许反向 ETF，不允许低流动性。
- 交易成本假设：往返 35 bps；预期 swing edge 必须超过成本且至少满足 100 bps 最小边际，并要求显著高于成本。
- 今日 `actionable_candidates=[]`。
- 排名靠前的观察对象普遍存在 `symbol_risk_veto` 或 `diagnostic_only=true`。
- 参数优化未更新 active strategy：样本、改善、胜率、sample_quality 等 gate 未通过。

### 解读
- 风险姿态应保持保守：`watch_only`。
- 不应因为 `risk_on`、单日涨幅或主题分数较高而绕过 veto。
- 不应从同主题较低排名标的中“挖替代品”；稳定规则要求在 `actionable_candidates=[]` 且 top diagnostic 被 veto 时，将本轮视为 veto audit 与 peer-relative review。

## 6. 今日推荐状态

### 确定性结论
- 今日无 `buy_candidate`。
- 今日无 `accumulate`。
- 今日无可执行的新仓建议。
- 总体建议状态：`watch_only`。

### 观察清单
| 优先级 | symbol | theme | 观察理由 | 失效/降级条件 |
|---:|---|---|---|---|
| 1 | `0857.HK` | `energy` | 主题分数最高，趋势与动量最强 | 继续受 `symbol_risk_veto` 约束；若跌回 ma20 或相对 `0883.HK` / `0386.HK` 转弱，则移出高优先级观察 |
| 2 | `0941.HK` | `telecom-dividend` | 运营商主题 leader，量能扩张，价格高于 ma20/ma60 | 若高位回落且 range_pos_60 从极强区间转弱，或继续无法解除 veto，则不升级 |
| 3 | `0002.HK` | `utilities-defensive` | 防御主题 leader，趋势完整 | 若 `0006.HK` 明显相对转强或 `0002.HK` 跌回 ma20，则重新比较 |
| 4 | `9618.HK` | `internet-platform` | 互联网平台内部相对最佳表达 | 若无法证明相对 `9988.HK`、`3690.HK`、`1024.HK` 的持续优势，或成交无法确认，则维持观察 |
| 5 | `2800.HK` | `hong-kong-broad-market` | 大盘 ETF 温和确认风险偏好 | 若跌回 ma20/ma60 或后续 T+窗口继续出现 misfire，则只保留为市场温度计 |

## 7. 今日高优先级研究问题

1. `0857.HK` 的强趋势是否来自能源主题整体扩散，还是单一标的拉升？需要比较 `0857.HK`、`0883.HK`、`0386.HK` 在后续 3/5/10 日的相对收益与回撤。
2. `0941.HK` 与 `0728.HK` 的运营商强势是否已过热？重点检查 range_pos_60 高于 1 后的追价失败率。
3. `0002.HK` 与 `0006.HK` 的防御主题是否只是低波动避险，而非 swing edge？需要验证其过去高分样本是否能覆盖 35 bps 成本与 100 bps edge gate。
4. 互联网平台主题中，`9618.HK` 是否持续替代 `0700.HK` / `9988.HK` 成为更优表达？需要把后验 selected-vs-best 误差转化为前置相对强弱检查。
5. `2800.HK`、`3033.HK`、`3067.HK` 的 ETF 确认为何低于单日市场风险偏好？需要判断这是指数权重分化、科技拖累，还是非日期对齐快照导致的审计噪音。
