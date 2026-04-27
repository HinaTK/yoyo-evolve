# Market Assessment — 2026-04-24 09:18

## Scope

- Market focus: Hong Kong stocks and ETFs.
- Time horizon: swing, 14–90 days.
- Portfolio posture: 100% cash; 2800.HK is watch-listed only.
- Risk profile: balanced; no leverage, no inverse ETFs, no low-liquidity trades.
- Default action when evidence is thin or conflicting: `watch_only`.
- Data note: market snapshot is marked `backfilled: true` and is as of 2026-04-24.

## Facts

### Market regime

- Snapshot date: 2026-04-24.
- Market summary risk state: `neutral`.
- Average stock move, 1 day: +0.258%.
- Average ETF move, 1 day: +0.632%.
- Five of six watchlist instruments closed higher; Tencent was the only 1-day decliner.
- All six instruments remain below their MA60.
- Four instruments are flagged `range`; Tencent and Xiaomi are flagged `downtrend`.

### Theme and symbol facts

| Symbol | Name | Theme | Close | 1D Move | vs MA20 | vs MA60 | 60D Range Position | Volume Ratio 20D | Regime Flags |
|---|---|---|---:|---:|---|---|---:|---:|---|
| 0700.HK | Tencent | internet-platform | 493.40 | -0.363% | below | below | 0.0840 | 0.8355 | downtrend |
| 9988.HK | Alibaba | internet-platform | 131.80 | +1.074% | above | below | 0.2418 | 0.7664 | range |
| 1810.HK | Xiaomi | consumer-tech | 31.20 | +0.064% | below | below | 0.0839 | 0.4960 | downtrend |
| 2800.HK | Tracker Fund of Hong Kong | HK broad market | 26.26 | +0.229% | above | below | 0.4483 | 0.8191 | range |
| 3033.HK | Hang Seng Tech ETF | Hang Seng Tech | 4.800 | +0.883% | above | below | 0.2049 | 0.5391 | range |
| 3067.HK | iShares Hang Seng TECH ETF | Hang Seng Tech | 10.30 | +0.783% | above | below | 0.2000 | 0.6629 | range |

### Leaders and laggards

- Relative leaders by 1-day move: 9988.HK (+1.074%), 3033.HK (+0.883%), 3067.HK (+0.783%).
- Relative laggards by 1-day move: 0700.HK (-0.363%), 1810.HK (+0.064%), 2800.HK (+0.229%).
- Alibaba is the strongest single-stock move in the snapshot.
- Hang Seng Tech ETFs outperformed the broad HK ETF on a 1-day basis.

### ETF confirmation facts

- Broad HK ETF 2800.HK closed above MA20 but below MA60, with volume ratio 0.8191.
- Tech ETFs 3033.HK and 3067.HK both closed above MA20 but below MA60.
- Tech ETF volume ratios are below average: 3033.HK at 0.5391 and 3067.HK at 0.6629.
- Tech ETFs remain in the lower quarter of their 60-day ranges: 3033.HK at 0.2049 and 3067.HK at 0.2000.
- 3067.HK turnover is much lower than 3033.HK in the snapshot, so 3033.HK is the cleaner liquidity reference among the two tech ETFs.

### Posterior-risk facts to respect

- Recent bullish broad-index ETF calls have failed: 2800.HK `hold` on 2026-04-20 failed at T+3 (-1.725%); 2800.HK `buy_candidate` on 2026-04-21 failed at T+3 (-1.868%).
- Current posterior pass rates are low across the watchlist: 0700.HK 0.04, 3067.HK 0.098, 2800.HK 0.137, 3033.HK 0.176, 9988.HK 0.235, 1810.HK 0.28.
- Active rules require broad-market plus ETF confirmation before upgrading low-pass-rate symbols to `buy_candidate`, `hold`, or `accumulate`.
- Active rules also say selective risk-on days with weak volume and prices still below MA60 should keep rebound-prone tech ETFs and single names at `watch_only`.

## Interpretations

### Market regime interpretation

The regime improved from defensive to repair-watch, but it is not yet a clean swing-entry regime. The factual positives are broad 1-day stabilization, a `neutral` risk state, and MA20 reclaims by 9988.HK, 2800.HK, 3033.HK, and 3067.HK. The factual negatives are just as important: every symbol remains below MA60, volume is below average across the whole watchlist, and the strongest rebounds are still low in their 60-day ranges.

This is a short-term relief setup inside an unrepaired medium-term tape. For a 14–90 day swing process, that argues for patience rather than immediate risk deployment.

### Theme strength interpretation

- **Internet platforms:** mixed. Alibaba is showing relative strength and has reclaimed MA20, while Tencent remains in downtrend below MA20 and MA60. The theme is not uniformly healthy.
- **Consumer tech:** weak. Xiaomi barely rose, remains below both moving averages, has one of the lowest 60-day range positions, and traded on very weak relative volume.
- **Hang Seng Tech ETFs:** improving at the margin but not confirmed. Both tech ETFs reclaimed MA20 and outperformed the broad ETF on the day, but both remain below MA60 with weak volume and low range position.
- **Broad HK market:** stable but not compelling. 2800.HK is above MA20 and has the best 60-day range position in the watchlist, but volume is below average and MA60 remains unreclaimed. Recent bullish misfires on 2800.HK make this evidence insufficient for another upgrade.

### ETF confirmation interpretation

ETF confirmation is partial, not decisive. The constructive part is that both Hang Seng Tech ETFs are now above MA20 and posted stronger 1-day gains than 2800.HK. The blocking part is that neither tech ETF reclaimed MA60, neither showed above-average volume, and both remain near the lower fifth of their 60-day ranges.

Under the stable rules, this is enough to keep watching tech rebound candidates, but not enough to upgrade Alibaba, Tencent, Xiaomi, 3033.HK, or 3067.HK above `watch_only`. The broad ETF also does not clear the stricter post-misfire threshold because breadth, volume, and moving-average confirmation are still incomplete.

### Standout names

- **9988.HK / Alibaba:** the clearest relative-strength name today. Evidence: largest 1-day gain, above MA20, range flag rather than downtrend. Blocking factors: below MA60, volume ratio below 1.0, weak historical pass rate, and only partial ETF confirmation.
- **3033.HK / Hang Seng Tech ETF:** the better tech ETF confirmation instrument today. Evidence: +0.883%, above MA20, higher liquidity/turnover than 3067.HK. Blocking factors: below MA60, weak volume ratio, low 60-day range position.
- **3067.HK / iShares Hang Seng TECH ETF:** confirms the same direction as 3033.HK but is less useful as the primary signal because turnover is much lower in the snapshot.
- **2800.HK / Tracker Fund:** still the broad-market reference, but today's evidence is not strong enough to overcome recent failed bullish calls. It is above MA20, but below MA60 with below-average volume.
- **0700.HK / Tencent:** the main internet-platform laggard. It declined on a day when Alibaba and the tech ETFs rose, remains below MA20 and MA60, and sits near the bottom of its 60-day range.
- **1810.HK / Xiaomi:** no actionable improvement. The tiny positive move does not change the downtrend flag, low range position, weak volume, or lack of MA20/MA60 repair.

## Risk posture

Current posture: **neutral watch-only / repair-watch**.

Reasons:

1. The market state improved to `neutral`, but every instrument remains below MA60.
2. The rebound is selective and low-volume rather than broad and forceful.
3. Tech ETF confirmation is only partial: MA20 reclaimed, MA60 not reclaimed, volume still weak.
4. Recent posterior evaluation shows repeated bullish misreads, especially in 2800.HK.
5. Low symbol pass rates require stricter confirmation before actionable upgrades.
6. The portfolio is 100% cash, so there is no need to force exposure before confirmation improves.

No new `buy_candidate`, `accumulate`, or `hold` upgrade is justified from this snapshot alone. No `avoid` call is justified either: the day shows rebound risk, and the rules require live downside confirmation plus broad/ETF rebound-risk checks before defensive calls on rebound-prone tech exposure. The disciplined action is to preserve optionality and define the confirmation thresholds.

## Candidate states for today

| Symbol | State | Rationale | Invalidation / Upgrade Trigger | Timing Confidence |
|---|---|---|---|---|
| 0700.HK | `watch_only` | Lags Alibaba and tech ETFs; below MA20/MA60; downtrend flag; near 60D range low. | Constructive watch invalidates if it keeps making relative lows while 3033/3067 improve. Upgrade only after reclaiming MA20 with ETF confirmation; stronger upgrade requires MA60 repair. | Low |
| 9988.HK | `watch_only` | Best single-name relative strength and above MA20, but below MA60 with weak volume and low posterior pass rate. | Upgrade only if volume improves, 3033/3067 confirm with stronger breadth, and price advances toward/reclaims MA60. Constructive watch weakens if it loses MA20 on rising volume. | Low-to-medium |
| 1810.HK | `watch_only` | Barely positive, below MA20/MA60, downtrend flag, weak volume, low range position. | Upgrade only after reclaiming MA20 with broad tech ETF confirmation; avoid call would require live downside confirmation and rebound-risk check. | Low |
| 2800.HK | `watch_only` | Broad ETF is above MA20 with the best range position, but below MA60, weak volume, and recent bullish calls failed. | Upgrade only if breadth, volume, and MA60 confirmation improve together. Constructive watch weakens if it loses MA20. | Low |
| 3033.HK | `watch_only` | Tech ETF rebound leader and above MA20, but below MA60 with weak volume and low range position. | Upgrade only after stronger volume and follow-through toward MA60; MA60 reclaim needed for higher-confidence swing exposure. | Low |
| 3067.HK | `watch_only` | Confirms 3033.HK directionally, but lower turnover makes it a secondary confirmation signal. | Upgrade only after 3033.HK also confirms, volume improves, and MA60 repair begins. | Low |

## High-priority research questions for today

1. Is today's rebound supported by breadth across Hang Seng Tech constituents, or concentrated in a few large names such as Alibaba?
2. Did 3033.HK and 3067.HK reclaim MA20 on improving intraday participation, or was the rebound low-conviction given weak volume ratios?
3. What level and volume threshold would make Alibaba's relative strength actionable without violating the ETF-confirmation rule?
4. Is 2800.HK's position above MA20 showing broad-market accumulation, or just a weak bounce still capped below MA60?
5. Are Tencent and Xiaomi lagging for stock-specific reasons, or are they warning that the tech rebound is too narrow to trust?
