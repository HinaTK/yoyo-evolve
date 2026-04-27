# Market Assessment - 2026-04-09

## Scope
- Market focus: Hong Kong stocks and ETFs
- Time horizon: swing (14-90 days)
- Risk profile: balanced
- Current portfolio posture: 100% cash, with 2800.HK on watch
- Default action when uncertain: `watch_only`

## Facts

### Market regime
- Snapshot date: 2026-04-09
- Market summary risk state: `risk_off`
- Average 1-day move for stocks in scope: -2.341%
- Average 1-day move for ETFs in scope: -1.801%
- 5 of 6 tracked instruments carry a `downtrend` regime flag.
- Only 2800.HK carries a `range` regime flag.

### Theme and instrument data
| Symbol | Name | Theme | 1D % | vs MA20 | vs MA60 | 60D Range Position | Volume Ratio 20 | Regime |
|---|---|---|---:|---:|---:|---:|---:|---|
| 0700.HK | Tencent | internet-platform | +0.098% | -1.78% | -7.74% | 0.1777 | 0.7072 | downtrend |
| 9988.HK | Alibaba | internet-platform | -2.846% | -3.24% | -15.48% | 0.0800 | 0.8611 | downtrend |
| 1810.HK | Xiaomi | consumer-tech | -4.274% | -5.35% | -9.84% | 0.0611 | 0.8418 | downtrend |
| 2800.HK | Tracker Fund of Hong Kong | hong-kong-broad-market | -0.687% | +1.39% | -1.64% | 0.3793 | 0.8775 | range |
| 3033.HK | Hang Seng Tech ETF | hang-seng-tech | -2.402% | -1.49% | -8.66% | 0.1344 | 1.0760 | downtrend |
| 3067.HK | iShares Hang Seng TECH ETF | hang-seng-tech | -2.314% | -1.36% | -8.43% | 0.1323 | 0.5616 | downtrend |

### Leaders and laggards
- Relative leader: 0700.HK at +0.098%, but still below both MA20 and MA60 and flagged `downtrend`.
- Relative ETF leader: 2800.HK at -0.687%, with price above MA20 but still below MA60.
- Laggard: 1810.HK at -4.274%, near the bottom of its 60-day range.
- Other notable weakness: 9988.HK at -2.846%; 3033.HK at -2.402%; 3067.HK at -2.314%.

### ETF confirmation
- Broad-market ETF (2800.HK) is holding better than the tech complex and remains above MA20.
- Both Hang Seng Tech ETFs (3033.HK and 3067.HK) are below MA20 and MA60.
- 3033.HK shows above-average participation by volume ratio (1.076), but the price result was still negative.
- 3067.HK shows weaker participation by volume ratio (0.5616).

### Process and posterior constraints
- Stable rule: when evidence is thin or conflicting, downgrade to `watch_only`.
- Stable rule: prefer theme confirmation through ETFs before upgrading a single-stock thesis.
- Stable rule: after repeated bullish misreads, do not upgrade low-pass-rate symbols to `buy_candidate`, `hold`, or `accumulate` without broad-market and ETF confirmation.
- Stable rule: after repeated defensive misreads, do not issue `avoid` without live downside confirmation and broad/ETF rebound-risk evidence.
- Posterior pass rates in current evaluation set are low across the tracked universe: 0700.HK 8.1%, 2800.HK 10.8%, 3067.HK 18.9%, 1810.HK 24.3%, 3033.HK 29.7%, 9988.HK 32.4%.
- Recent misses include bullish calls on 9988.HK, 2800.HK, 3033.HK, and 3067.HK on 2026-04-08 over T+5.
- Recent misses also include `avoid` calls on 9988.HK, 1810.HK, and 3033.HK on 2026-04-02 over T+20.

## Interpretations

### Market regime assessment
- This is a defensive tape, not a broad momentum tape. The `risk_off` summary aligns with negative average 1-day moves and the fact that nearly every tracked name remains below both intermediate moving averages.
- 2800.HK is the only name showing partial resilience, but its `range` regime and sub-MA60 position do not yet support calling the broad market healthy.
- The current market structure favors patience over aggression for new swing entries.

### Theme strength
- Internet-platform is weak, not confirmed. Tencent is the least-bad name on the day, but Alibaba remains materially weaker, and neither name is above MA20.
- Hang Seng Tech as a theme is weak. Both 3033.HK and 3067.HK remain in downtrends and are positioned near the lower part of their 60-day ranges.
- Consumer-tech is weakest within this watchlist snapshot. Xiaomi is the session laggard and sits near the bottom of its 60-day range.

### ETF confirmation read
- ETF confirmation is negative for tech and incomplete for the broad market.
- Because the tech ETFs are both below MA20 and MA60, there is no ETF-based confirmation for upgrading Tencent or Alibaba to an actionable long setup today.
- Because 2800.HK is holding up better than individual tech names, the broad market appears more stable than the tech theme, but still not strong enough to confirm a risk-on swing regime.

### Standout names
- **0700.HK / Tencent:** Relative strength exists only on a one-day basis. It is standing up better than peers, but the trend backdrop is still weak. That makes it a name to monitor for future leadership, not a confirmed setup.
- **2800.HK / Tracker Fund:** The cleanest defensive read in the set. Above MA20 and less damaged than the rest, but still below MA60 and in a range rather than an uptrend.
- **9988.HK / Alibaba:** Weak relative and absolute posture. Deeply below MA60 and near the bottom decile of its 60-day range.
- **1810.HK / Xiaomi:** Highest fragility in today’s group. Sharp daily loss and weakest range position argue against trying to anticipate a reversal without fresh evidence.
- **3033.HK and 3067.HK:** Useful as theme gauges. Today they confirm pressure in HK tech rather than recovery.

### Risk posture
- Recommended posture for today: `watch_only`.
- Reason: the market is `risk_off`, ETF confirmation for tech is absent, and posterior evidence warns against upgrading low-pass-rate names without broad-market plus ETF support.
- This is not a good session for clustered bearish calls either. Recent evaluation history shows that blunt `avoid` calls in correlated HK tech can be early when rebound risk is not checked explicitly.
- If research later uncovers a catalyst, the first upgrade path should run through ETF stabilization, not single-name enthusiasm.

## What would need to change before posture improves
- 3033.HK and/or 3067.HK reclaiming MA20 with sustained participation.
- 2800.HK improving from range behavior into a clearer trend confirmation, ideally with price holding above MA20 and retesting or reclaiming MA60.
- Internet-platform leaders showing relative strength for more than one session, with Tencent and Alibaba no longer both below MA20.
- Evidence that downside is no longer broad-based across stocks and ETFs in the watchlist.

## High-priority research questions for today
1. What catalyst or macro driver explains the `risk_off` pressure on 2026-04-09, and is it broad-market or sector-specific?
2. Did Hang Seng Tech weakness come from constituent-specific news, or was it a market-wide growth/China-tech de-risking move?
3. Is 2800.HK resilience signaling rotation into broader HK exposure, or is it only relative weakness that still lacks true trend confirmation?
4. Within internet-platform, is Tencent showing genuine relative leadership versus Alibaba, or just a one-day defensive outlier with no follow-through?
5. Are there breadth or index-component signals available for 2026-04-09 that can confirm whether rebound risk is rising before any `avoid` or long upgrade is considered?
