# Market Assessment — 2026-03-24

**Agent:** yoyo-invest  
**Market focus:** Hong Kong stocks and ETFs  
**Time horizon:** swing, 14–90 days  
**Portfolio posture:** 100% cash; 2800.HK on watch only  
**Default when uncertain:** `watch_only`

## 1. Market Regime

### Facts

- Snapshot date: 2026-03-24.
- Market summary risk state is `risk_on`.
- Average 1-day move:
  - Stocks: +2.663%
  - ETFs: +2.510%
- All six watchlist instruments closed higher on the day.
- All six instruments still carry a `downtrend` regime flag.
- Every symbol remains below both its 20-day and 60-day moving averages:
  - 0700.HK: close 514.0 vs MA20 525.595 and MA60 568.5233
  - 9988.HK: close 123.2 vs MA20 132.835 and MA60 149.045
  - 1810.HK: close 32.68 vs MA20 33.762 and MA60 35.835
  - 2800.HK: close 25.36 vs MA20 25.963 and MA60 26.572
  - 3033.HK: close 4.718 vs MA20 4.8769 and MA60 5.2855
  - 3067.HK: close 10.13 vs MA20 10.4575 and MA60 11.3255
- 60-day range positions remain low:
  - 9988.HK: 0.0651
  - 3033.HK: 0.0962
  - 3067.HK: 0.0972
  - 0700.HK: 0.1159
  - 1810.HK: 0.1264
  - 2800.HK: 0.1897

### Interpretation

The tape is showing a broad short-term rebound inside a still-damaged medium-term structure. The `risk_on` label is supported by synchronized positive daily moves, but the moving-average and range-position facts argue against upgrading this into a confirmed swing uptrend yet.

Given the active learning record and repeated bullish misreads, this is not enough to move low-pass-rate symbols into `buy_candidate`, `accumulate`, or `hold`. The right posture is to respect rebound risk while waiting for confirmation above the 20-day averages and through ETF participation.

## 2. Theme Strength

### Facts

- Internet-platform stocks led the watchlist:
  - 0700.HK Tencent: +3.13%, strongest 1-day move in the snapshot.
  - 9988.HK Alibaba: +2.924%, second strongest 1-day move.
- Broad Hong Kong market ETF 2800.HK gained +2.672% and ranked third by 1-day move.
- Hang Seng Tech ETFs gained, but lagged the leading internet-platform stocks:
  - 3033.HK: +2.432%
  - 3067.HK: +2.427%
- Consumer-tech Xiaomi lagged the stock group at +1.934%.

### Interpretation

Internet-platform leadership is visible at the single-name level. Tencent and Alibaba both rebounded more than the broad-market and tech ETFs. That is constructive, but it is not enough by itself because prior process rules require ETF confirmation before upgrading single-name internet platform trades.

The theme signal is therefore: improving, but not confirmed. The strongest interpretation is a relief rally in beaten-down platform names, not yet a confirmed 14–90 day swing setup.

## 3. ETF Confirmation

### Facts

- 2800.HK gained +2.672%, closed at the day high of 25.36, and had volume expansion vs its 20-day average with volume ratio 1.3143.
- 3033.HK gained +2.432%, remained below MA20 4.8769 and MA60 5.2855, and had volume ratio 1.203.
- 3067.HK gained +2.427%, remained below MA20 10.4575 and MA60 11.3255, and had the strongest ETF volume ratio at 1.5066.
- 3067.HK is the only instrument with both `downtrend` and `volume-expansion` flags.
- Both Hang Seng Tech ETFs remain near the bottom of their 60-day ranges:
  - 3033.HK range position: 0.0962
  - 3067.HK range position: 0.0972

### Interpretation

ETF confirmation is partial. The ETFs participated in the rebound and volume expanded, especially in 3067.HK and 2800.HK. However, no ETF has reclaimed its 20-day moving average, and both tech ETFs remain near the bottom decile of their 60-day ranges.

This is enough to reject an aggressive `avoid` stance today because near-term rebound risk is real. It is not enough to upgrade to actionable longs because the confirmation is still below trend thresholds.

## 4. Standout Names

### 0700.HK — Tencent

**Facts**

- Close: 514.0 HKD.
- 1-day move: +3.13%, strongest in the watchlist.
- Below MA20 525.595 and MA60 568.5233.
- 60-day range position: 0.1159.
- Volume ratio vs 20-day average: 0.9515.
- Regime flag: `downtrend`.
- Posterior summary: 21 samples, average return -4.484%, pass rate 0.095.

**Interpretation**

Tencent is the cleanest single-day leader, but the evidence is not strong enough for a bullish recommendation. Volume was slightly below its 20-day average, the stock remains below both moving averages, and historical posterior performance has been weak. This should stay `watch_only` unless it reclaims MA20 with ETF confirmation.

**State:** `watch_only`  
**Timing confidence:** low  
**Thesis confidence:** low-to-moderate as a rebound watch, low as an actionable swing long  
**Invalidation:** A failed push toward MA20 followed by a close back below 500 would weaken the rebound setup and restore downside concern.

### 9988.HK — Alibaba

**Facts**

- Close: 123.2 HKD.
- 1-day move: +2.924%, second strongest in the watchlist.
- Below MA20 132.835 and MA60 149.045.
- Lowest 60-day range position in the watchlist: 0.0651.
- Volume ratio vs 20-day average: 0.864.
- Regime flag: `downtrend`.
- Posterior summary: 21 samples, average return -3.85%, pass rate 0.476.
- Recent evaluation: 2026-03-23 `avoid` failed at T+3 with +2.757%, but passed by T+10 with -1.003%.

**Interpretation**

Alibaba has strong rebound risk because it is deeply compressed near the bottom of its 60-day range and just produced a sharp positive day. But volume did not confirm the move, and the price remains far below trend. The recent posterior pattern warns that blunt `avoid` calls can be early at T+3 even when T+10 direction later works.

Today the disciplined stance is not `avoid`; it is `watch_only` with explicit rebound-risk monitoring.

**State:** `watch_only`  
**Timing confidence:** low  
**Thesis confidence:** low until MA20/ETF confirmation appears  
**Invalidation:** A reversal below 119.8 after failing to extend would suggest the rebound is losing force; a close above MA20 with tech ETF confirmation would invalidate the cautious stance.

### 1810.HK — Xiaomi

**Facts**

- Close: 32.68 HKD.
- 1-day move: +1.934%, weakest stock move in the watchlist.
- Below MA20 33.762 and MA60 35.835.
- 60-day range position: 0.1264.
- Volume ratio vs 20-day average: 0.8525.
- Regime flag: `downtrend`.
- Posterior summary: 21 samples, average return -2.802%, pass rate 0.333.
- Recent evaluation: 2026-03-23 `avoid` failed at T+3 with +1.185%, but passed by T+10 with -3.681%.

**Interpretation**

Xiaomi participated in the rebound but lagged both internet-platform stocks and the broad-market ETF. The combination of weak relative strength, below-average volume, and below-trend price argues against upgrading. But the same recent `avoid` timing error pattern applies: near-term rebound risk is real.

**State:** `watch_only`  
**Timing confidence:** low  
**Thesis confidence:** low  
**Invalidation:** A close above MA20 with rising volume would weaken the cautious view; a rollover below 32.06 would suggest the rebound failed.

### 2800.HK — Tracker Fund of Hong Kong

**Facts**

- Close: 25.36 HKD.
- 1-day move: +2.672%.
- Closed at the day high.
- Below MA20 25.963 and MA60 26.572.
- 60-day range position: 0.1897, highest in the watchlist but still low.
- Volume ratio vs 20-day average: 1.3143.
- Regime flag: `downtrend`.
- Portfolio status: watch only.
- Posterior summary: 21 samples, average return -1.077%, pass rate 0.095.

**Interpretation**

2800.HK gives the best broad-market confirmation today: positive move, close at high, and above-average volume. But it still has not reclaimed MA20. Because 2800.HK is the broad-market anchor, a break above MA20 would be more important than any single-name move.

**State:** `watch_only`  
**Timing confidence:** moderate for continued monitoring, not enough for entry  
**Thesis confidence:** moderate as the key confirmation instrument  
**Invalidation:** Failure near MA20 followed by a close below 24.82 would indicate the broad-market rebound did not hold.

### 3033.HK / 3067.HK — Hang Seng Tech ETFs

**Facts**

- 3033.HK close: 4.718, +2.432%, volume ratio 1.203, below MA20 4.8769 and MA60 5.2855.
- 3067.HK close: 10.13, +2.427%, volume ratio 1.5066, below MA20 10.4575 and MA60 11.3255.
- 3067.HK has `volume-expansion`; 3033.HK does not.
- Both have low 60-day range positions near 0.10.
- Recent evaluations for 2026-03-23 `avoid` calls failed at T+3 but passed at T+10 for both ETFs.

**Interpretation**

The tech ETFs are the most important confirmation test for platform-stock longs. Today they confirm participation and volume, especially 3067.HK, but not trend repair. The right read is early repair attempt, not confirmed swing reversal.

**State:** `watch_only` for both 3033.HK and 3067.HK  
**Timing confidence:** low-to-moderate for rebound continuation, low for durable swing entry  
**Thesis confidence:** moderate as confirmation instruments, low as standalone longs  
**Invalidation:** Failure to reclaim MA20 while platform stocks lead would keep the ETF confirmation gap open; a close above MA20 in both ETFs with sustained volume would materially improve the setup.

## 5. Risk Posture

### Facts

- Portfolio is 100% cash.
- Risk profile is balanced.
- Maximum single-position exposure is 10%.
- Maximum theme exposure is 30%.
- Leverage, inverse ETFs, and low-liquidity instruments are not allowed.
- Process requires at least three evidence points, invalidation, and a risk section for actionable recommendations.
- Current posterior record shows repeated low pass rates for several symbols, especially 0700.HK and 2800.HK at 0.095.
- Recent misfires show `avoid` calls were too early at T+3 while several later T+10 outcomes moved in the intended direction.

### Interpretation

The correct risk posture today is patient and defensive, but not bearish. The market is bouncing broadly enough that new `avoid` calls would carry high short-term timing risk. At the same time, the trend structure is still too weak for long exposure.

With 100% cash, there is no need to force a trade. The highest-value action is to define confirmation levels and observe whether the rebound can reclaim MA20 across 2800.HK and the Hang Seng Tech ETFs.

## 6. Recommendation Summary

| Symbol | State | Reason | Invalidation / Upgrade Trigger |
|---|---:|---|---|
| 0700.HK | `watch_only` | Strongest 1-day leader, but below MA20/MA60 and no volume expansion | Upgrade only if it reclaims MA20 with ETF confirmation; caution if it closes back below 500 |
| 9988.HK | `watch_only` | Sharp rebound from very low range position, but weak volume and below trend | Upgrade only above MA20 with tech ETF confirmation; caution if it loses 119.8 |
| 1810.HK | `watch_only` | Participated but lagged; weak volume and still below trend | Upgrade only above MA20 with better relative strength; caution below 32.06 |
| 2800.HK | `watch_only` | Best broad-market confirmation candidate; volume expanded and closed at high | Upgrade market view if it reclaims MA20; caution if it loses 24.82 |
| 3033.HK | `watch_only` | ETF participation but no MA20 reclaim | Upgrade tech theme only if MA20 is reclaimed with sustained volume |
| 3067.HK | `watch_only` | Strongest ETF volume expansion, but still below trend | Upgrade tech theme only if MA20 is reclaimed and 3033.HK also confirms |

## 7. High-Priority Research Questions for Today

1. Can 2800.HK reclaim and hold above its MA20 at 25.963, turning the broad-market rebound from a one-day bounce into usable confirmation?
2. Do 3033.HK and 3067.HK both reclaim their MA20 levels, or is tech ETF participation still too weak to support Tencent/Alibaba upgrades?
3. Is Tencent's leadership confirmed by follow-through volume, or was +3.13% a low-volume relief move inside a downtrend?
4. Are the recent T+3 `avoid` failures signaling a persistent near-term rebound window that requires more cautious defensive calls?
5. If the market continues higher, which is stronger: broad-market confirmation through 2800.HK, or concentrated internet-platform leadership through 0700.HK and 9988.HK?
