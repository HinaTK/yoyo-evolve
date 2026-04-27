# Market Assessment — 2026-03-16

## Scope

- Agent: yoyo-invest
- Market focus: Hong Kong stocks and ETFs
- Horizon: swing, 14–90 days
- Risk profile: balanced
- Portfolio state: 100% cash; 2800.HK on watch only
- Default action when uncertain: `watch_only`

## 1. Market Regime

### Facts

- Snapshot risk state: `risk_on`.
- Average 1-day stock move across the watchlist: +2.928%.
- Average 1-day ETF move across the watchlist: +2.289%.
- All six watched symbols closed positive on the day.
- Two broad/ETF instruments still carry `downtrend` flags or remain below key moving averages:
  - 2800.HK closed at 26.12, below MA20 26.357 and MA60 26.5833; regime flag: `downtrend`.
  - 3033.HK closed at 4.998, essentially at MA20 4.995 but below MA60 5.3378; regime flag: `range`.
  - 3067.HK closed at 10.71, essentially at MA20 10.702 but below MA60 11.434; regime flag: `range`.
- Hang Seng Tech ETF proxies rose +2.628% for 3033.HK and +2.685% for 3067.HK.

### Interpretation

The day is risk-on in price action, but not yet a clean swing confirmation. The rebound is broad enough to matter, yet the main ETFs have not reclaimed MA60 and the broad-market ETF remains in a downtrend. This supports alertness for improving conditions, not aggressive deployment.

**Regime stance:** constructive rebound, incomplete confirmation.

## 2. Theme Strength

### Facts

- Consumer-tech led the watchlist:
  - 1810.HK Xiaomi: +5.642%, close 35.20, above MA20 34.408, below MA60 36.4973, volume ratio 1.4836.
- Hang Seng Tech ETFs participated:
  - 3033.HK: +2.628%, volume ratio 1.0722.
  - 3067.HK: +2.685%, volume ratio 0.8315.
- Internet platforms rose but with weaker confirmation:
  - 0700.HK Tencent: +2.009%, above MA20 527.925, below MA60 576.925, volume ratio 0.8386.
  - 9988.HK Alibaba: +1.132%, below MA20 140.09 and MA60 150.7733, volume ratio 0.6097, regime flag `downtrend`.

### Interpretation

The strongest theme signal is consumer-tech through Xiaomi, helped by above-average volume and a close back above MA20. Internet-platform strength is less convincing: Tencent is technically healthier than Alibaba, but both remain below MA60 and neither has strong volume confirmation. Alibaba is still the weakest large-cap setup because it remains below both moving averages and near the lower part of its 60-day range.

**Theme ranking today:**

1. Consumer-tech rebound: strongest, but still below MA60.
2. Hang Seng Tech ETF rebound: participating, not confirmed above MA60.
3. Internet platforms: mixed; Tencent better than Alibaba, but not enough for upgrade.
4. Broad HK market: positive day, still downtrend.

## 3. ETF Confirmation

### Facts

- 2800.HK broad-market ETF:
  - Close: 26.12
  - 1-day move: +1.555%
  - Below MA20 and MA60
  - 60-day range position: 0.2482
  - Volume ratio: 1.1464
  - Regime flag: `downtrend`
- 3033.HK Hang Seng Tech ETF:
  - Close: 4.998
  - 1-day move: +2.628%
  - Slightly above MA20, below MA60
  - 60-day range position: 0.2839
  - Volume ratio: 1.0722
- 3067.HK iShares Hang Seng TECH ETF:
  - Close: 10.71
  - 1-day move: +2.685%
  - Slightly above MA20, below MA60
  - 60-day range position: 0.2763
  - Volume ratio: 0.8315

### Interpretation

ETF confirmation is partial. Tech ETFs are confirming a short-term rebound back to the MA20 area, but not a medium-term trend repair. The broad-market ETF still argues for caution because it remains below both MA20 and MA60 with a downtrend flag.

Per stable rules, this is not enough confirmation to upgrade rebound-prone tech exposure above `watch_only`, especially with MA60 unreclaimed and mixed volume.

**ETF confirmation grade:** partial / insufficient for new buy candidates.

## 4. Standout Names

### 1810.HK — Xiaomi

#### Facts

- Close: 35.20
- 1-day move: +5.642%
- Above MA20 34.408
- Below MA60 36.4973
- 60-day range position: 0.3528
- Volume ratio: 1.4836
- Latest high/low: 35.28 / 33.40
- Regime flag: `range`

#### Interpretation

Xiaomi is the clearest positive standout. It has the strongest price move and the best volume expansion in the watchlist. The constraint is that it remains below MA60, so the move is still a rebound inside a damaged or range-bound structure rather than a confirmed swing uptrend.

**State:** `watch_only`

**What would improve it:** follow-through above MA60 with continued volume support and ETF confirmation from 3033.HK/3067.HK.

**Invalidation for constructive watch:** failure back below MA20, especially if tech ETFs also lose MA20.

### 0700.HK — Tencent

#### Facts

- Close: 558.50
- 1-day move: +2.009%
- Above MA20 527.925
- Below MA60 576.925
- 60-day range position: 0.4313
- Volume ratio: 0.8386
- Regime flag: `range`

#### Interpretation

Tencent is technically better than Alibaba because it is above MA20 and sits higher in its 60-day range. But volume is below average and MA60 is still overhead. Given weak historical pass rate in posterior evaluation and no full ETF confirmation, it should not be upgraded on this single-day rebound.

**State:** `watch_only`

**Invalidation for constructive watch:** loss of MA20 or failure to follow through while tech ETFs roll back below MA20.

### 9988.HK — Alibaba

#### Facts

- Close: 134.00
- 1-day move: +1.132%
- Below MA20 140.09
- Below MA60 150.7733
- 60-day range position: 0.1631
- Volume ratio: 0.6097
- Regime flag: `downtrend`

#### Interpretation

Alibaba remains the weakest major single-name setup. The positive day looks like a rebound within a downtrend, not a confirmed reversal. Low volume and low range position argue against chasing.

**State:** `watch_only`

**Invalidation for constructive watch:** continued rejection below MA20 while ETFs fail to hold MA20.

## 5. Risk Posture

### Facts

- Portfolio is 100% cash.
- Max single-position limit is 10%.
- Max theme exposure limit is 30%.
- Leverage, inverse ETFs, and low-liquidity positions are not allowed.
- Posterior evaluation shows repeated bullish misreads and low pass rates across several watchlist symbols, especially 0700.HK, 2800.HK, and 3067.HK.
- Current stable rules require broad-market and ETF confirmation before upgrading low-pass-rate symbols or broad-index ETFs.

### Interpretation

The correct posture is patient and selective. The market offered a risk-on bounce, but the evidence is not strong enough to overcome the process constraints. The portfolio being all cash is acceptable today; there is no need to force exposure before MA60 and breadth confirmation improve.

**Risk posture:** preserve optionality; no new position yet.

## 6. Candidate Actions

| Symbol | Assessment | Action State | Timing Confidence | Reason |
|---|---:|---|---|---|
| 1810.HK | strongest rebound | `watch_only` | medium-low | Best price/volume signal, but still below MA60 and needs ETF confirmation. |
| 0700.HK | constructive but unconfirmed | `watch_only` | low | Above MA20 but below MA60 with weak volume and poor posterior pass rate. |
| 9988.HK | weak rebound | `watch_only` | low | Still below MA20/MA60, low range position, weak volume. |
| 2800.HK | broad market not repaired | `watch_only` | low | Positive day but still below MA20/MA60 and flagged downtrend. |
| 3033.HK | tech ETF rebound | `watch_only` | medium-low | Reclaimed MA20 by a small margin but remains below MA60. |
| 3067.HK | tech ETF rebound | `watch_only` | medium-low | Similar to 3033.HK, but volume confirmation is weaker. |

No `buy_candidate`, `accumulate`, or `hold` upgrade today.

## 7. High-Priority Research Questions for Today

1. Did 3033.HK and 3067.HK hold above MA20 after this rebound, and did either begin closing the gap to MA60 with improving volume?
2. Is Xiaomi’s +5.642% move supported by company-specific news, sector flow, or only short-covering/rebound mechanics?
3. Does 2800.HK show breadth improvement beyond a single positive close, or is the broad market still lagging the tech rebound?
4. Can Tencent reclaim MA60 with volume, or does weak volume make this another low-confidence rebound?
5. Is Alibaba forming a base near the lower part of its 60-day range, or does its failure to reclaim MA20 confirm continued relative weakness?
