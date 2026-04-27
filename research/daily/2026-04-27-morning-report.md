# 2026-04-27 早盘推荐报告

Session: morning / pre-market planning  
组合状态：100% 现金，无持仓  
默认行动：`watch_only`

## Market Regime

**State:** `neutral`

港股观察池今天不是明确的风险偏好扩张，而是“ETF 企稳、个股偏弱”的分裂结构。ETF 平均 1 日涨幅为 +0.387%，但单一个股平均下跌 -1.478%。`3033.HK` 与 `3067.HK` 领涨并站在 MA20 上方，可是两者仍低于 MA60，且成交量比率分别只有 0.8623 与 0.5930。广义市场 ETF `2800.HK` 小跌 -0.228%，仍在 MA20 上方但未收复 MA60。最重要的风险信号来自 `0700.HK`：下跌 -3.04%，处于 60 日区间底部，且放量下跌。

**核心判断：** 今天只允许观察和设置触发条件，不允许在早盘证据下升级为 `buy_candidate`、`hold` 或 `accumulate`。近期 `2800.HK` 的 bullish 调用在 T+3 失败，稳定规则要求再次看多广义市场 ETF 前必须同时出现 breadth、volume、moving-average confirmation。当前证据不够。

**关键证据：**
- 市场风险状态为 `neutral`，不是 `risk_off`，但也不是确认的 `risk_on`。
- ETF 强于个股：ETF 平均 +0.387%，个股平均 -1.478%。
- 所有 ETF 仍低于 MA60，说明中期趋势尚未修复。
- `3033.HK`、`3067.HK` 虽然上涨并高于 MA20，但 volume_ratio_20 均低于 1.0。
- `0700.HK` 放量下跌至 60 日区间底部，是 HK tech 反弹尝试的主要否定证据。

---

## Top Candidates

### 1. Hang Seng Tech ETF — `3033.HK`

**State:** `watch_only`

**Rationale:** `3033.HK` 是今天最优先观察的技术确认工具。它是观察池中涨幅第一，收盘 4.834，高于 MA20 4.7684，说明短线有企稳尝试。但它仍低于 MA60 4.9982，60 日区间位置只有 0.2328，volume_ratio_20 为 0.8623，尚未达到足以支持行动的成交量确认。它可以作为 HK tech 风险偏好的门槛指标，但不能单独触发买入。

**Evidence:**
- latest_close: 4.834
- pct_change_1d: +0.708%
- MA20: 4.7684，价格在 MA20 上方
- MA60: 4.9982，价格仍在 MA60 下方
- range_pos_60: 0.2328，仍处于 60 日区间偏低位置
- volume_ratio_20: 0.8623，成交量未超过 20 日均量
- 与 `3067.HK` 同向上涨，但未获得 `0700.HK` 确认

**Risks:**
- 低于 MA60 的反弹可能只是弱势区间内的短线修复。
- 成交量不足，容易出现开盘后冲高回落。
- `0700.HK` 放量创区间低位会削弱整个 HK tech ETF 信号。
- 后验数据显示 `3033.HK` pass_rate 仅 0.176，不能用单日上涨替代实时确认。

**Invalidation:**
- 跌回 MA20 4.7684 下方，或跌破今日低位 4.794 后无法收回。
- 成交量继续低于均量，同时价格无法接近 MA60 4.9982。
- `3033.HK` 与 `3067.HK` 出现明显背离，说明 ETF 确认失效。

**Horizon:** 3–10 个交易日；今天仅用于盘中确认，不做开盘行动。

**Confidence:** 中等作为观察优先级；低作为可执行多头。

---

### 2. iShares Hang Seng TECH ETF — `3067.HK`

**State:** `watch_only`

**Rationale:** `3067.HK` 是 `3033.HK` 的确认配对。它上涨 +0.68%，收盘 10.37，高于 MA20 10.2365，说明 HK tech ETF 层面确实有同步企稳迹象。但 volume_ratio_20 只有 0.5930，比 `3033.HK` 更弱，且仍低于 MA60 10.718。今天它的作用是验证 tech ETF 反弹是否一致，而不是独立进攻。

**Evidence:**
- latest_close: 10.37
- pct_change_1d: +0.68%
- MA20: 10.2365，价格在 MA20 上方
- MA60: 10.718，价格仍未收复 MA60
- range_pos_60: 0.2275，仍处于 60 日区间低位
- volume_ratio_20: 0.5930，成交量明显不足
- 与 `3033.HK` 同向，但没有单一个股广泛确认

**Risks:**
- 成交量更弱，价格上涨的可靠性不足。
- 若 `3033.HK` 强而 `3067.HK` 弱，说明主题信号噪音较大。
- `3067.HK` pass_rate 仅 0.098，历史短窗表现很弱，必须提高行动门槛。

**Invalidation:**
- 跌回 MA20 10.2365 下方。
- 无法守住今日低位 10.29 或首次回撤后继续缩量。
- 相对 `2800.HK` 转为明显弱势，说明 tech theme 未形成领导力。

**Horizon:** 3–10 个交易日；今天作为 ETF confirmation pair 使用。

**Confidence:** 中等作为确认指标；低作为单独交易候选。

---

### 3. Tracker Fund of Hong Kong — `2800.HK`

**State:** `watch_only`

**Rationale:** `2800.HK` 是广义港股风险承载工具，也是判断是否允许任何单一个股升级的基础。它收盘 26.20，高于 MA20 25.991，但低于 MA60 26.3593，且 1 日下跌 -0.228%。近期 `2800.HK` 的 bullish 调用在 T+3 失败，因此今天必须比平时更严格：只有 breadth、volume、moving-average progress 同时改善，才允许后续研究升级。

**Evidence:**
- latest_close: 26.20
- pct_change_1d: -0.228%
- MA20: 25.991，价格仍在 MA20 上方
- MA60: 26.3593，价格未收复 MA60
- range_pos_60: 0.4310，处于中低区间
- volume_ratio_20: 0.8148，成交量不足
- recent misfire: 2026-04-21 `2800.HK` `buy_candidate` T+3 -1.868% -> `fail`

**Risks:**
- 最近 broad-index ETF bullish 误判提示短线 timing confidence 偏低。
- 低成交量下接近 MA60 可能只是阻力测试，而非突破前奏。
- 如果 `0700.HK` 继续放量下跌，`2800.HK` 的稳定可能被权重股拖累。

**Invalidation:**
- 跌破 MA20 25.991 或无法守住 26.14 附近的日内低位。
- 成交量维持低于均量，同时价格无法重新接近或收复 MA60 26.3593。
- ETF 稳定但个股 breadth 继续恶化，尤其 `0700.HK` 继续新低。

**Horizon:** 3–14 个交易日；今天只看是否形成广义市场确认。

**Confidence:** 中等作为市场温度计；低作为立即多头行动。

---

### 4. Alibaba — `9988.HK`

**State:** `watch_only`

**Rationale:** `9988.HK` 是今天相对较好的单一个股观察对象，因为它仍高于 MA20 127.35，并且比 `0700.HK`、`1810.HK` 更接近企稳。但它 1 日下跌 -1.138%，收盘 130.3，仍低于 MA60 139.61，volume_ratio_20 仅 0.4987。当前规则要求先有 ETF confirmation，再考虑互联网平台单一个股，所以它不能因相对强弱而提前升级。

**Evidence:**
- latest_close: 130.3
- pct_change_1d: -1.138%
- MA20: 127.35，价格仍在 MA20 上方
- MA60: 139.61，价格仍显著低于 MA60
- range_pos_60: 0.2145，处于低位区间
- volume_ratio_20: 0.4987，成交量很弱
- `0700.HK` 同主题但放量走弱，主题内部不一致

**Risks:**
- 低成交量使相对强势可信度不足。
- 互联网平台主题未被 `0700.HK` 确认。
- 若 ETF 只是低量反弹，单一个股突破更容易失败。
- `9988.HK` pass_rate 0.235，不足以支持在证据不足时升级。

**Invalidation:**
- 跌破 MA20 127.35。
- 无法重新挑战今日高位 133.9，且成交量继续低于均量。
- `3033.HK` / `3067.HK` 回落或 `0700.HK` 继续新低。

**Horizon:** 3–10 个交易日；只在 ETF 与同业确认后重新评估。

**Confidence:** 中等偏低作为观察对象；低作为单一个股行动。

---

### 5. Tencent — `0700.HK`

**State:** `watch_only`

**Rationale:** `0700.HK` 不是买入候选，而是今天最关键的风险确认指标。它下跌 -3.04%，收盘 478.4，低于 MA20 499.18 与 MA60 528.9917，range_pos_60 为 0.0，并且 volume_ratio_20 达到 1.5339。放量下跌到 60 日区间底部不是抄底信号，而是对 HK tech 反弹质量的警告。

**Evidence:**
- latest_close: 478.4
- pct_change_1d: -3.04%，观察池最弱
- MA20: 499.18，价格在 MA20 下方
- MA60: 528.9917，价格在 MA60 下方
- range_pos_60: 0.0，处于 60 日区间底部
- volume_ratio_20: 1.5339，放量下跌
- regime_flags: `downtrend`, `volume-expansion`

**Risks:**
- 高成交量下跌可能代表主动卖压仍未结束。
- 若它继续走弱，会否定 `3033.HK` 与 `3067.HK` 的低量反弹。
- 短线可能有技术反弹，但稳定规则禁止把 oversold bounce 当作行动确认。

**Invalidation:**
- 对“稳定观察”的失效条件是跌破 478 附近并继续放量下行。
- 若反弹无法重新站上 480 且 ETF 同时回落，HK tech 反弹框架失效。
- 只有收复部分跌幅、成交结构改善，并获得 ETF 同步确认后，才可从风险指标转为研究候选。

**Horizon:** 1–5 个交易日作为风险监控；3–10 个交易日才可能重新评估多头。

**Confidence:** 高作为风险警报；低作为任何多头行动。

---

## Avoids

今天不发布新的 `avoid` 推荐。

**原因：**
- 稳定规则要求在相关 ETF / 个股上发布 clustered `avoid` 前，必须检查 broad/ETF rebound-risk。当前 `3033.HK` 与 `3067.HK` 仍在上涨并高于 MA20，说明存在短线反弹风险。
- `0700.HK` 的下跌很弱，但 broad market 状态仍为 `neutral`，不是确认的系统性 `risk_off`。
- 最近错误模式提示：不要在反弹风险仍存在时，对低 pass-rate、rebound-prone 标的过早发布防御性 `avoid`。

**Watch-only defensive notes:**
- `0700.HK`：放量下跌，是最接近防御性观察的标的；但由于 tech ETFs 尚未确认转弱，维持 `watch_only`。
- `1810.HK`：低位弱势、低成交量、低优先级；没有足够 live downside confirmation 发布 `avoid`。

---

## Portfolio Posture

**State:** `watch_only` / 100% 现金

**Rationale:** 当前组合没有持仓，因此没有被迫交易或降低风险的需求。今天最好的优势是保持选择权，等待 breadth、volume、moving-average confirmation 同时出现。早盘证据只支持观察，不支持行动。

**Evidence:**
- 组合为 100% cash。
- 市场风险状态为 `neutral`，但 ETF 与个股分裂。
- ETF 上涨仍低量且低于 MA60。
- `0700.HK` 放量下跌，阻止 HK tech 主题升级。
- `2800.HK` 近期 bullish T+3 misfire 要求更高确认门槛。

**Risks:**
- 如果市场盘中突然放量上行，100% 现金可能错过第一段反弹。
- 但在后验 pass_rate 普遍偏弱、近期 broad ETF bullish 失败的背景下，错过低质量第一段反弹比过早进场更可接受。

**Invalidation / Upgrade Conditions:**
只有同时满足以下至少三类证据，才允许从 `watch_only` 进入更积极研究：
1. `2800.HK` 守住 MA20 并接近或收复 MA60 26.3593。
2. `3033.HK` 与 `3067.HK` 同时走强，且 volume_ratio_20 逼近或超过 1.0。
3. `0700.HK` 不再创新低，并至少稳定在 480 附近上方。
4. `9988.HK` 继续守住 MA20 127.35，并出现成交量扩张。
5. 市场 breadth 改善，不只是单一 ETF 或单一权重股推动。

**Sizing Constraints if Later Action Becomes Justified:**
- 单一持仓上限：10% portfolio。
- 主题暴露上限：30%。Hang Seng Tech ETF 与互联网平台个股视为相关风险。
- 若今天盘中证据改善，首笔也应低于完整 10% 上限，以反映近期低 pass_rate 与 broad ETF bullish misfire。
- 同一主题优先选择 ETF，而不是同时买入多个相关单一个股。

**Horizon:** 今日盘中到未来 3–14 个交易日。

**Confidence:** 高信心维持现金与 `watch_only`；低信心采取任何开盘交易。
