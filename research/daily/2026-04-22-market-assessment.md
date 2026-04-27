# Market Assessment — 2026-04-22

## Scope

- Market focus: Hong Kong stocks and ETFs
- Time horizon: swing, 14-90 days
- Portfolio posture entering the day: 100% cash; 2800.HK on watch only
- Risk profile: balanced, no leverage, no inverse ETF, no low-liquidity exposure

## 1. Market Regime

### Facts

- Snapshot risk state: `risk_off`.
- Average 1-day stock move across the watched single names: -2.755%.
- Average 1-day ETF move across the watched ETFs: -1.597%.
- All six watched instruments declined on the day.
- Single-name declines were larger than ETF declines:
  - 9988.HK: -3.522%
  - 0700.HK: -2.890%
  - 1810.HK: -1.852%
  - 2800.HK: -1.121%
  - 3033.HK: -1.977%
  - 3067.HK: -1.693%
- Volume confirmation was not strong:
  - 0700.HK volume ratio vs 20-day average: 0.993
  - 9988.HK: 0.787
  - 1810.HK: 0.490
  - 2800.HK: 0.557
  - 3033.HK: 0.614
  - 3067.HK: 0.545

### Interpretation

This is a risk-off session with broad downside, but not a decisive high-volume capitulation signal. The cleaner reading is not "panic bottom" and not "trend reversal". It is a weak tape where cash remains valuable and new long exposure needs stronger confirmation than usual.

Because several watched names have low posterior pass rates and recent bullish calls have misfired, the default action should remain `watch_only` unless ETF confirmation improves.

## 2. Theme Strength

### Facts

| Theme | Instruments | 1-day move | Position vs MA20 | Position vs MA60 | 60-day range position |
|---|---:|---:|---:|---:|---:|
| Internet platform | 0700.HK | -2.890% | slightly above MA20 | below MA60 | 0.1595 |
| Internet platform | 9988.HK | -3.522% | above MA20 | below MA60 | 0.2364 |
| Consumer tech | 1810.HK | -1.852% | slightly below MA20 | below MA60 | 0.1770 |
| HK broad market | 2800.HK | -1.121% | above MA20 | slightly above MA60 | 0.5057 |
| Hang Seng Tech | 3033.HK | -1.977% | above MA20 | below MA60 | 0.2525 |
| Hang Seng Tech | 3067.HK | -1.693% | above MA20 | below MA60 | 0.2588 |

### Interpretation

The broad-market ETF is the strongest relative area, while internet-platform single names are lagging. Hang Seng Tech ETFs are holding above MA20 but remain below MA60, which is not enough to confirm a durable swing rebound.

The theme signal is defensive rather than constructive: broad HK exposure looks less damaged than tech/internet exposure, but the overall tape is still risk-off.

## 3. ETF Confirmation

### Facts

- 2800.HK closed at 26.46, above MA20 of 25.844 and slightly above MA60 of 26.392.
- 2800.HK 60-day range position: 0.5057, the strongest among the watchlist.
- 3033.HK closed at 4.858, above MA20 of 4.756 but below MA60 of 5.0405.
- 3067.HK closed at 10.45, above MA20 of 10.209 but below MA60 of 10.8077.
- Tech ETF volume ratios were weak: 3033.HK at 0.614 and 3067.HK at 0.545.
- 3067.HK turnover is much lower than 3033.HK in the provided snapshot.

### Interpretation

ETF confirmation is mixed and not strong enough to upgrade single-name tech or internet-platform exposure. 2800.HK is the best relative ETF because it is above both MA20 and MA60, but the recent posterior evaluation shows a failed 2026-04-21 `buy_candidate` call over T+3. That argues for reducing timing confidence today rather than pressing another broad-market long immediately.

For Hang Seng Tech exposure, the ETFs are still below MA60 with weak volume. Under the active rule set, this requires `watch_only`, especially because rebound-prone tech exposure has produced timing errors before.

## 4. Standout Names

### 2800.HK — Tracker Fund of Hong Kong

#### Facts

- Latest close: 26.46
- 1-day move: -1.121%, the least negative move in the watchlist
- MA20: 25.844; MA60: 26.392
- 60-day range position: 0.5057
- Volume ratio vs 20-day average: 0.557
- Current portfolio status: watch
- Recent posterior note: 2026-04-21 `buy_candidate` failed at T+3 with -1.868%

#### Interpretation

2800.HK remains the cleanest relative-strength instrument, but weak volume and the recent failed bullish timing call make an immediate upgrade unattractive. It is the first candidate to revisit if it holds above MA60 while volume improves.

Current state: `watch_only`.

Invalidation for a constructive watch: close back below MA60 with expanding volume, or broad market risk state remaining `risk_off` while 2800.HK loses the 26.0 area.

### 0700.HK — Tencent

#### Facts

- Latest close: 504.0
- 1-day move: -2.890%
- MA20: 501.725; MA60: 534.4583
- 60-day range position: 0.1595
- Volume ratio vs 20-day average: 0.993
- Posterior summary pass rate: 0.06, the weakest in the tracked set

#### Interpretation

Tencent is near MA20 but still far below MA60 and low in its 60-day range. Volume is near normal, so the decline has more confirmation than the lower-volume declines elsewhere. Given the very low historical pass rate, there is no basis to upgrade without broad-market and ETF confirmation.

Current state: `watch_only`.

Invalidation for a constructive watch: failure to hold MA20 after a rebound attempt, or continued underperformance versus 3033.HK/3067.HK.

### 9988.HK — Alibaba

#### Facts

- Latest close: 131.5
- 1-day move: -3.522%, weakest in the watchlist
- MA20: 126.315; MA60: 141.3433
- 60-day range position: 0.2364
- Volume ratio vs 20-day average: 0.787
- Posterior summary pass rate: 0.235

#### Interpretation

Alibaba is the day’s laggard, but the close remains above MA20. That makes it a poor long candidate and also a risky fresh `avoid`: a near-term bounce can happen from above-MA20 support, and the rules require explicit rebound-risk checks before defensive clustered calls. No action beyond watch.

Current state: `watch_only`.

Invalidation for a constructive watch: close below MA20 with rising volume, especially if 3033.HK and 3067.HK also lose MA20.

### 1810.HK — Xiaomi

#### Facts

- Latest close: 31.8
- 1-day move: -1.852%
- MA20: 31.889; MA60: 33.8947
- 60-day range position: 0.1770
- Volume ratio vs 20-day average: 0.490
- Regime flag: `downtrend`
- Posterior summary pass rate: 0.24

#### Interpretation

Xiaomi is below both MA20 and MA60 and explicitly flagged as downtrend. The low volume reduces confidence in making a fresh aggressive defensive call, but it also means there is no long setup. It should stay on watch only until it reclaims MA20 and the broader tech ETFs confirm.

Current state: `watch_only`.

Invalidation for a constructive watch: continued closes below MA20, or a lower low with volume expansion.

### 3033.HK and 3067.HK — Hang Seng Tech ETFs

#### Facts

- 3033.HK latest close: 4.858; -1.977%; above MA20; below MA60; volume ratio 0.614.
- 3067.HK latest close: 10.45; -1.693%; above MA20; below MA60; volume ratio 0.545.
- Both have 60-day range positions near the lower quartile: 0.2525 and 0.2588.
- Posterior pass rates are low: 3033.HK at 0.216, 3067.HK at 0.137.

#### Interpretation

The tech ETF pair is not confirming a durable tech rebound. Above-MA20 positioning keeps them from being clean `avoid` candidates, but below-MA60 positioning and weak volume prevent upgrades. 3033.HK is preferable to 3067.HK for observation because the snapshot shows much higher turnover.

Current state: `watch_only`.

Invalidation for a constructive watch: loss of MA20 by both ETFs, especially if accompanied by rising volume and continued single-name weakness.

## 5. Risk Posture

### Facts

- Portfolio is 100% cash.
- Market regime is `risk_off`.
- All watchlist instruments declined.
- ETFs fell less than single stocks.
- No watched tech ETF has reclaimed MA60.
- Recent posterior evaluations include failed bullish calls on 2800.HK over short windows.

### Interpretation

The correct posture today is capital preservation and evidence collection. I should not force a trade because cash is already aligned with the risk state. The main mistake to avoid is upgrading a single-stock rebound idea before the ETFs confirm it.

Recommended posture: remain 100% cash / watch only.

Timing confidence: low for new longs over T+3/T+5; moderate only for observing whether 2800.HK can keep relative strength over T+10/T+20.

## 6. Assessment Summary

### Facts

- Risk state: `risk_off`.
- Best relative instrument: 2800.HK.
- Weakest single-name move: 9988.HK.
- Lowest 60-day range position: 0700.HK.
- Only broad-market ETF is above both MA20 and MA60.
- Tech ETFs are above MA20 but below MA60 with weak volume.

### Interpretation

No high-conviction buy candidate is present. The market is not broken enough to justify broad `avoid` calls, and not strong enough to justify accumulation. The disciplined choice is to wait for either ETF confirmation or clearer downside follow-through.

## High-Priority Research Questions for Today

1. Can 2800.HK hold above MA60 for multiple sessions, or was the reclaim a weak-volume false start?
2. Do 3033.HK and 3067.HK reclaim MA60 with volume, or do they lose MA20 and confirm renewed tech weakness?
3. Is Alibaba’s sharp decline a single-name laggard event, or is it the first sign of broader internet-platform underperformance versus the tech ETFs?
4. Does Tencent hold the MA20 area around 501-502, or does near-normal sell volume turn into follow-through selling?
5. Are there macro or HK/China policy headlines explaining the risk-off move, and do prices confirm those headlines after the first reaction?
