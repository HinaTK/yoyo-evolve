# Market Assessment — 2026-03-26

Generated for: `yoyo-invest`  
Market focus: HK stocks and ETFs  
Time horizon: swing, 14–90 days  
Portfolio posture: 100% cash, no active positions

## 1. Facts

### Market Regime

- Snapshot date: `2026-03-26`.
- Market summary risk state: `risk_off`.
- Every tracked symbol carries a `downtrend` regime flag.
- Average 1-day stock move across the watchlist: `-2.26%`.
- Average 1-day ETF move across the watchlist: `-2.843%`.
- All six watchlist instruments closed below both their 20-day and 60-day moving averages.

### Symbol Snapshot

| Symbol | Name | Kind | Theme | Close | 1D Move | MA20 | MA60 | 60D Range Position | Volume Ratio 20D | Regime |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| 0700.HK | Tencent | Stock | internet-platform | 495.60 | -1.958% | 523.925 | 565.125 | 0.0000 | 0.7197 | downtrend |
| 9988.HK | Alibaba | Stock | internet-platform | 123.00 | -4.577% | 130.865 | 148.3567 | 0.0613 | 0.8324 | downtrend |
| 1810.HK | Xiaomi | Stock | consumer-tech | 32.44 | -0.246% | 33.471 | 35.6107 | 0.0989 | 0.9471 | downtrend |
| 2800.HK | Tracker Fund of Hong Kong | ETF | hong-kong-broad-market | 25.14 | -2.027% | 25.825 | 26.5527 | 0.1264 | 0.4877 | downtrend |
| 3033.HK | Hang Seng Tech ETF | ETF | hang-seng-tech | 4.656 | -3.402% | 4.8437 | 5.2642 | 0.0430 | 0.5079 | downtrend |
| 3067.HK | iShares Hang Seng TECH ETF | ETF | hang-seng-tech | 10.00 | -3.101% | 10.3865 | 11.2805 | 0.0445 | 0.7498 | downtrend |

### Relative Leaders and Laggards

Facts from the provided market summary:

- Relative leaders:
  - `1810.HK` Xiaomi: `-0.246%` 1D.
  - `0700.HK` Tencent: `-1.958%` 1D.
  - `2800.HK` Tracker Fund of Hong Kong: `-2.027%` 1D.
- Relative laggards:
  - `9988.HK` Alibaba: `-4.577%` 1D.
  - `3033.HK` Hang Seng Tech ETF: `-3.402%` 1D.
  - `3067.HK` iShares Hang Seng TECH ETF: `-3.101%` 1D.

### ETF Confirmation

- Broad HK ETF `2800.HK` closed at `25.14`, below MA20 `25.825` and MA60 `26.5527`.
- Hang Seng Tech ETF `3033.HK` closed at `4.656`, below MA20 `4.8437` and MA60 `5.2642`.
- Hang Seng Tech ETF `3067.HK` closed at `10.00`, below MA20 `10.3865` and MA60 `11.2805`.
- `3033.HK` and `3067.HK` sit near the bottom of their 60-day ranges, with range positions `0.0430` and `0.0445`.
- ETF volume ratios are below 1.0 for all tracked ETFs:
  - `2800.HK`: `0.4877`.
  - `3033.HK`: `0.5079`.
  - `3067.HK`: `0.7498`.

### Posterior Evaluation Context

- Recent posterior review shows repeated bullish misreads.
- Recent failed or weak bullish calls include:
  - `9988.HK` `buy_candidate` from 2026-03-25: `-6.517%` over T+5 and `-3.413%` over T+20.
  - `3067.HK` `buy_candidate` from 2026-03-25: `-4.554%` over T+5 and `-1.163%` over T+20.
  - `2800.HK` `hold` from 2026-03-25: `-2.572%` over T+5 but `+2.104%` over T+20.
- Symbol pass rates in posterior summary are low across the watchlist:
  - `0700.HK`: `0.08`.
  - `2800.HK`: `0.16`.
  - `3067.HK`: `0.24`.
  - `1810.HK`: `0.32`.
  - `3033.HK`: `0.36`.
  - `9988.HK`: `0.40`.

## 2. Interpretations

### Market Regime Interpretation

This is a risk-off tape, not a confirmed dip-buying environment. The broad ETF, tech ETFs, and single-name internet/consumer-tech stocks are all below their 20-day and 60-day moving averages. That means there is no broad-market confirmation for upgrading single-name long setups today.

The watchlist is clustered near the lower end of its 60-day ranges. That can create short-term bounce risk, but it is not the same as confirmed reversal. Because all tracked ETFs remain in downtrend, the default action under the stable rules is `watch_only`.

### Theme Strength Interpretation

- **Internet platforms:** Weak. Tencent is at the bottom of its 60-day range, and Alibaba is one of the weakest names on the day. Both are below MA20 and MA60. No theme-level long confirmation.
- **Hang Seng Tech:** Weak. Both `3033.HK` and `3067.HK` fell more than 3% and remain near the bottom of their 60-day ranges. ETF confirmation is negative.
- **Consumer tech:** Xiaomi is the relative standout because it fell only `-0.246%`, but it is still below MA20 and MA60 and remains in a downtrend. Relative strength exists, but absolute trend confirmation is absent.
- **Broad HK market:** Weak. `2800.HK` fell `-2.027%`, remains below MA20 and MA60, and has a low 20-day volume ratio. Broad-market confirmation is not present.

### ETF Confirmation Interpretation

ETF confirmation argues against new long exposure today. Both tech ETFs are weak and near 60-day lows. The broad ETF is also below trend. Under the current rules, this blocks upgrades of low-pass-rate single names to `buy_candidate`, `hold`, or `accumulate` unless there is exceptional single-name evidence. The provided snapshot does not contain that exceptional evidence.

### Standout Names

#### 1810.HK — Xiaomi

Xiaomi is the cleanest relative-strength watch because it barely declined while the broader ETF and Hang Seng Tech ETFs sold off more sharply. But the setup is still only relative strength inside a downtrend. It is not an actionable long signal without ETF stabilization or a reclaim of short-term trend.

Current state: `watch_only`.

Invalidation for constructive watch: close materially below the recent low area implied by the current 60-day range position, or continued underperformance versus `3033.HK`/`3067.HK` on the next rebound attempt.

#### 0700.HK — Tencent

Tencent is less damaged than Alibaba on the day but closed at the bottom of its 60-day range and below both moving averages. The posterior pass rate for `0700.HK` is especially weak at `0.08`, so a bullish upgrade would require broad-market and ETF confirmation. That confirmation is absent.

Current state: `watch_only`.

Invalidation for constructive watch: failure to reclaim the MA20 area near `523.925`, or continued lower lows while tech ETFs remain weak.

#### 9988.HK — Alibaba

Alibaba is the weakest single stock in the snapshot, down `-4.577%`. Recent posterior evaluation also flags failed `buy_candidate` calls from 2026-03-25. This combination argues against trying to catch the falling move today.

Current state: `watch_only`; avoid new long initiation until evidence improves.

Near-term bounce risk: elevated, because the stock is already near the bottom of its 60-day range and declined sharply today. A defensive view should not be expressed as a fresh aggressive `avoid` without acknowledging possible T+3/T+5 rebound risk.

#### 2800.HK — Tracker Fund of Hong Kong

`2800.HK` is the broad-market confirmation instrument. It is below MA20 and MA60, down `-2.027%`, and volume ratio is only `0.4877`. That does not confirm accumulation. Because the portfolio is 100% cash, there is no need to force a broad-market entry.

Current state: `watch_only`.

Constructive trigger to research: stabilization above MA20 with improving volume and better breadth across tech ETFs.

#### 3033.HK / 3067.HK — Hang Seng Tech ETFs

Both Hang Seng Tech ETFs are weak and near 60-day lows. `3033.HK` has stronger liquidity in the snapshot, while `3067.HK` has much lower turnover. Since liquidity matters and low liquidity is disallowed by the profile, `3033.HK` is the better ETF proxy for theme confirmation.

Current state: `watch_only` for both.

Constructive trigger to research: reclaim of MA20 on improving volume, with single-name leaders such as Tencent, Alibaba, or Xiaomi also stabilizing.

## 3. Risk Posture

### Portfolio Risk

- Current portfolio is 100% cash.
- No action is required to reduce existing exposure.
- Given `risk_off` regime and absent ETF confirmation, cash is an acceptable position today.

### Actionability

No symbol should be upgraded to `buy_candidate`, `accumulate`, or `hold` today based only on the provided snapshot.

Primary reason: the market regime, ETF confirmation, and posterior learning all point in the same direction — reduce confidence in bullish swing entries until broad or ETF evidence improves.

### Timing Confidence

Short-term timing confidence for bullish entries is low. Several names are oversold or near range lows, so a T+3/T+5 bounce is possible, but that is rebound risk rather than a confirmed swing setup. Medium-term thesis confidence is also low for new longs because the ETF layer has not confirmed.

### Recommended Stance

- Overall stance: `watch_only`.
- Cash posture: maintain.
- Max new exposure today: `0%` unless intraday or next-session evidence shows broad ETF stabilization that is not present in this snapshot.
- Theme exposure: keep below limits by taking no new theme exposure today.

## 4. High-Priority Research Questions for Today

1. Did `2800.HK` and `3033.HK` show any intraday reversal structure after the close-level weakness, or did they close near lows with no follow-through buying?
2. Is Xiaomi's relative strength supported by company-specific news, sector rotation, or merely lower beta during a broad selloff?
3. Are Tencent and Alibaba seeing fundamental/news catalysts behind the selloff, or is the move mostly ETF/theme de-risking?
4. Which ETF is the best liquid confirmation vehicle for Hang Seng Tech exposure right now: `3033.HK` or `3067.HK`, given turnover and spread considerations?
5. What exact evidence would be required to move from `watch_only` to `buy_candidate` — MA20 reclaim, volume expansion above 1.0x, broad ETF confirmation, or single-name relative strength sustained for multiple sessions?
