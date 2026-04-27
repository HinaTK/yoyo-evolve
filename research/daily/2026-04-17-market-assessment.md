# Market Assessment — 2026-04-17

## Scope
- Market focus: HK stocks and ETFs
- Time horizon: swing (14-90 days)
- Risk profile: balanced
- Default action when uncertain: `watch_only`
- Portfolio state: 100% cash; existing watch position only in `2800.HK`

## Facts

### Market regime
- Snapshot as of `2026-04-17`.
- Market summary risk state: `risk_off`.
- Average 1-day move for stocks in scope: `-0.334%`.
- Average 1-day move for ETFs in scope: `-1.085%`.
- No data failures were reported in the snapshot.

### Broad market / ETF facts
- `2800.HK` closed at `26.44`, down `0.974%` on the day.
  - Above `MA20` (`25.73`)
  - Slightly above `MA60` (`26.402`)
  - 60-day range position: `0.5000`
  - Volume ratio vs 20-day average: `0.6709`
  - Regime flag: `range`
- `3033.HK` closed at `4.936`, down `1.161%` on the day.
  - Above `MA20` (`4.7503`)
  - Below `MA60` (`5.076`)
  - 60-day range position: `0.3164`
  - Volume ratio vs 20-day average: `1.0267`
  - Regime flag: `range`
- `3067.HK` closed at `10.59`, down `1.12%` on the day.
  - Above `MA20` (`10.197`)
  - Below `MA60` (`10.882`)
  - 60-day range position: `0.3137`
  - Volume ratio vs 20-day average: `0.5679`
  - Regime flag: `range`

### Single-name facts
- `0700.HK` (Tencent) closed at `510.5`, down `1.257%`.
  - Above `MA20` (`503.025`)
  - Below `MA60` (`539.175`)
  - 60-day range position: `0.2058`
  - Volume ratio: `0.5361`
  - Regime flag: `range`
- `9988.HK` (Alibaba) closed at `136.4`, up `0.442%`.
  - Above `MA20` (`125.745`)
  - Below `MA60` (`142.7017`)
  - 60-day range position: `0.3255`
  - Volume ratio: `0.8310`
  - Regime flag: `range`
- `1810.HK` (Xiaomi) closed at `32.0`, down `0.187%`.
  - Below `MA20` (`32.296`)
  - Below `MA60` (`34.1037`)
  - 60-day range position: `0.2081`
  - Volume ratio: `0.6061`
  - Regime flag: `downtrend`

### Leadership / laggard facts from the snapshot
- Leaders: `9988.HK`, `1810.HK`, `2800.HK`
- Laggards: `0700.HK`, `3033.HK`, `3067.HK`

### Posterior-evaluation facts relevant to today
- Recent misfires: `3033.HK hold` and `3067.HK hold` on `2026-04-16` both failed over `T+5`.
- Symbol pass rates remain low across the universe:
  - `0700.HK`: `6.5%`
  - `1810.HK`: `23.9%`
  - `2800.HK`: `17.0%`
  - `3033.HK`: `23.4%`
  - `3067.HK`: `14.9%`
  - `9988.HK`: `25.5%`
- Active learnings require ETF confirmation before upgrading single-name internet-platform trades.
- Stable rules say to stay at `watch_only` when evidence is thin/conflicting, especially in `risk_off` and momentum-dependent setups.

## Interpretations

### Market regime assessment
The live snapshot supports a cautious `risk_off` read. Stocks were mixed-to-soft, while ETFs were uniformly weaker. That matters because ETF weakness is broad confirmation of softer tape, not just single-name noise. For a 14-90 day swing process, this is not a clean trend-following entry backdrop.

### Theme strength
- **Internet-platform theme:** mixed internally, but not strong enough at the theme level.
  - Alibaba outperformed on the day.
  - Tencent underperformed on the day.
  - Both remain below `MA60`.
  - That means the theme does not yet show broad medium-term trend recovery.
- **Hang Seng Tech theme:** weak confirmation.
  - Both tech ETFs were down more than 1%.
  - Both remain below `MA60`.
  - Only `3033.HK` had near-average volume, but price still failed to reclaim the longer moving average.
- **Broad Hong Kong market:** more stable than tech, but still not strong.
  - `2800.HK` held above both `MA20` and `MA60`, which is the cleanest technical fact in the set.
  - But its volume ratio was weak, and the market summary still labeled the session `risk_off`.

### ETF confirmation
ETF confirmation is insufficient for upgrading risk.
- For internet-platform single names, the required ETF confirmation is not there because the relevant tech ETFs (`3033.HK`, `3067.HK`) were both weak on the day and both remain below `MA60`.
- For a broader Hong Kong exposure thesis, `2800.HK` is better behaved than the tech ETFs, but it is still range-bound rather than clearly trending.
- Given recent failed `hold` calls on both tech ETFs, there is extra reason to avoid aggressive upgrades on the same theme without clearer confirmation.

### Standout names
- **Most resilient name:** `9988.HK`
  - Only stock in scope that closed green.
  - Still below `MA60`, so resilience is not yet trend confirmation.
- **Most technically stable ETF:** `2800.HK`
  - Above both `MA20` and `MA60`.
  - Mid-range positioning suggests less extension than a momentum breakout.
  - This makes it more defensible than the tech ETFs, but still not a high-conviction buy signal.
- **Weakest setup:** `1810.HK`
  - Only name with an explicit `downtrend` regime flag.
  - Below both moving averages and sitting near the lower end of its 60-day range.
- **Low-confidence heavyweight:** `0700.HK`
  - Low range position, below `MA60`, weak volume, and the worst pass rate in posterior evaluation.
  - Even though it remains above `MA20`, the evidence does not support upgrading it.

### Risk posture
Recommended posture for today: **defensive, watch-first, no new aggressive risk**.

Why:
1. Market regime is explicitly `risk_off`.
2. ETF confirmation is weak, especially in tech.
3. Most names remain below `MA60`, which argues against calling a durable trend reversal.
4. Posterior evaluation warns against upgrading low-pass-rate symbols or rebound-prone tech exposure without broad-market and ETF confirmation.
5. Recent T+5 failures in the tech ETFs argue for lower timing confidence even if a medium-term rebound thesis eventually works.

### Practical stance by symbol
- `2800.HK`: **watch_only / highest-quality watchlist name today**
  - Cleaner than the rest, but still range-bound and not strong enough for automatic upgrade.
- `9988.HK`: **watch_only**
  - Relative strength exists, but theme and ETF confirmation are insufficient.
- `0700.HK`: **watch_only**
  - Too weak on posterior pass rate and still below `MA60`.
- `3033.HK`: **watch_only**
  - Better volume than peers, but recent failed `hold` call plus sub-`MA60` structure keep confidence low.
- `3067.HK`: **watch_only**
  - Similar thesis to `3033.HK` with weaker volume support.
- `1810.HK`: **watch_only`, leaning defensive**
  - Explicit downtrend prevents upgrade.

## Invalidation / What Would Change This Read
This cautious assessment would weaken if one or more of the following appears in fresh data:
- `2800.HK` holds above `MA60` and starts showing stronger-than-average volume expansion.
- `3033.HK` and/or `3067.HK` reclaim `MA60` with follow-through rather than a one-day bounce.
- Internet-platform names improve together, not selectively, with both `0700.HK` and `9988.HK` confirming.
- The market risk state shifts away from `risk_off` and ETF performance starts leading rather than lagging single names.

## High-Priority Research Questions for Today
1. Is `2800.HK` beginning a legitimate broad-market base above `MA60`, or is this still just a low-volume range with poor follow-through odds?
2. Can `3033.HK` provide real theme confirmation for HK tech by reclaiming `MA60`, or is current strength still a sub-`MA60` rebound trap?
3. Does `9988.HK`'s relative strength persist when measured against weak ETF confirmation, or is it just isolated single-name resilience?
4. Is `0700.HK` showing any early accumulation signal despite weak volume and poor posterior pass rate, or should it remain deprioritized until broader confirmation appears?
5. Does Xiaomi (`1810.HK`) show any evidence of downtrend stabilization, or is it still a name to avoid upgrading until it retakes at least `MA20` and improves breadth/volume context?
