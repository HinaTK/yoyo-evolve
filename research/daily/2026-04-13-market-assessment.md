# Market Assessment — 2026-04-13

## Scope
- **Agent:** yoyo-invest
- **Market focus:** HK stocks, ETFs
- **Time horizon:** swing (14-90 days)
- **Risk profile:** balanced
- **Current portfolio posture:** 100% cash, existing `2800.HK` on watch only

## Facts

### Market regime
- Snapshot `as_of_date`: **2026-04-13**
- Market summary risk state: **risk_off**
- Average 1-day move, watched stocks: **-1.828%**
- Average 1-day move, watched ETFs: **-0.755%**

### Price/trend state by symbol
- **0700.HK Tencent**
  - Close: **490.0**
  - 1D change: **-2.874%**
  - vs MA20: **below** (`490.0 < 512.165`)
  - vs MA60: **below** (`490.0 < 547.2717`)
  - 60-day range position: **0.0555**
  - Regime flag: **downtrend**
- **9988.HK Alibaba**
  - Close: **123.2**
  - 1D change: **-1.833%**
  - vs MA20: **below** (`123.2 < 126.115`)
  - vs MA60: **below** (`123.2 < 144.7433`)
  - 60-day range position: **0.0855**
  - Regime flag: **downtrend**
- **1810.HK Xiaomi**
  - Close: **30.66**
  - 1D change: **-0.777%**
  - vs MA20: **below** (`30.66 < 32.863`)
  - vs MA60: **below** (`30.66 < 34.5457`)
  - 60-day range position: **0.0**
  - Regime flag: **downtrend**
- **2800.HK Tracker Fund of Hong Kong**
  - Close: **25.96**
  - 1D change: **-0.765%**
  - vs MA20: **above** (`25.96 > 25.655`)
  - vs MA60: **below** (`25.96 < 26.445`)
  - 60-day range position: **0.3621**
  - Regime flag: **range**
- **3033.HK Hang Seng Tech ETF**
  - Close: **4.724**
  - 1D change: **-0.715%**
  - vs MA20: **below** (`4.724 < 4.7651`)
  - vs MA60: **below** (`4.724 < 5.1337`)
  - 60-day range position: **0.1426**
  - Regime flag: **downtrend**
- **3067.HK iShares Hang Seng TECH ETF**
  - Close: **10.12**
  - 1D change: **-0.784%**
  - vs MA20: **below** (`10.12 < 10.2265`)
  - vs MA60: **below** (`10.12 < 11.0045`)
  - 60-day range position: **0.1284**
  - Regime flag: **downtrend**

### Theme strength
- **Internet-platform theme** (`0700.HK`, `9988.HK`)
  - Both names closed lower on the day.
  - Both are below MA20 and MA60.
  - Both sit in the bottom ~9% of their 60-day ranges.
- **Hang Seng Tech theme** (`3033.HK`, `3067.HK`)
  - Both ETFs closed lower on the day.
  - Both are below MA20 and MA60.
  - Both are in the lower ~13-14% of their 60-day ranges.
- **Consumer-tech theme** (`1810.HK`)
  - Xiaomi closed lower on the day.
  - It is below MA20 and MA60.
  - It is at the bottom of its 60-day range.
- **Hong Kong broad market theme** (`2800.HK`)
  - Closed lower on the day.
  - Slightly above MA20 but below MA60.
  - Range position is mid-lower rather than extreme low.

### ETF confirmation
- The broad-market ETF **2800.HK** is not in a confirmed uptrend; it is flagged **range**, above MA20 but below MA60.
- The tech ETFs **3033.HK** and **3067.HK** both remain in **downtrends** and both trade below MA20 and MA60.
- There is **no positive ETF confirmation** for upgrading single-name Hong Kong tech or internet-platform trades today.

### Standout names by snapshot
- **Relative resilience:** `3033.HK` had the smallest decline among the watched list at **-0.715%**, but it still remains in a downtrend below both moving averages.
- **Broad-market relative stability:** `2800.HK` held above MA20 and lost **-0.765%**, making it less weak than the single-name tech names.
- **Weakest single-name pressure:** `0700.HK` fell **-2.874%** and sits near the bottom of its 60-day range.
- **Most extended downside position:** `1810.HK` has a 60-day range position of **0.0**, meaning it closed at the bottom of the observed 60-day range.

### Posterior discipline inputs
- Recent evaluation summary shows repeated **defensive misread** and **bullish misread** patterns.
- Symbol pass rates remain weak:
  - `0700.HK`: **0.073**
  - `2800.HK`: **0.146**
  - `3067.HK`: **0.171**
  - `1810.HK`: **0.268**
  - `3033.HK`: **0.268**
  - `9988.HK`: **0.293**
- Active process rules require:
  - ETF confirmation before upgrading single-name internet-platform trades.
  - `watch_only` when regime is `risk_off` and setup is momentum-dependent.
  - extra rebound-risk caution before issuing clustered `avoid` calls.

## Interpretations

### Market regime interpretation
The live snapshot supports a **risk-off to cautious-neutral** stance, not a risk-seeking one. Most watched names are below both short- and medium-term moving averages, and most sit near the bottom of their 60-day ranges. The only partial stabilizer is `2800.HK`, but it is still below MA60 and therefore does not yet confirm a durable broad-market uptrend.

### Theme strength interpretation
- **Internet-platform:** weak. Both Tencent and Alibaba show the same structure: below MA20, below MA60, and compressed near the low end of the 60-day range. That is not the backdrop for upgrading into swing buys.
- **Hang Seng Tech:** weak, but important to monitor for stabilization before the single names. The ETFs are cleaner proxies for theme confirmation, and both still point down.
- **Consumer-tech:** weakest chart position in this list belongs to Xiaomi, which is at the 60-day range low. That can produce sharp rebounds, but the current evidence does not yet distinguish a durable reversal from simple oversold conditions.
- **Broad-market HK exposure:** less weak than tech, but still not strong enough to treat as confirmed trend recovery.

### ETF confirmation interpretation
Today’s ETF evidence argues for restraint. The stable rules explicitly prefer theme confirmation through ETFs before upgrading a single-stock thesis, and that confirmation is absent. Because both Hang Seng Tech ETFs remain below MA20 and MA60, any bullish read on Tencent or Alibaba would be premature under the current process.

### Standout names interpretation
- **2800.HK** is the closest thing to a constructive watch candidate because it is above MA20 and is not in a formal downtrend flag, but the lack of MA60 recovery keeps it below action threshold.
- **0700.HK** and **9988.HK** look weak enough for caution, but recent process rules warn against clustered `avoid` calls in correlated names without explicit rebound-risk evidence. That means restraint is better than an aggressive bearish call.
- **1810.HK** is statistically the most washed-out name in the snapshot. That increases rebound risk in the short window, which lowers confidence in any near-term bearish recommendation.

## Risk posture for today
- **Default posture:** `watch_only`
- **Reason:** risk-off regime, weak ETF confirmation, and posterior evidence that both bullish upgrades and defensive calls have been mistimed in this universe.
- **Capital deployment stance:** preserve cash and wait for confirmation rather than anticipate reversal.
- **What would improve posture:**
  1. `2800.HK` holding above MA20 and reclaiming MA60,
  2. at least one Hang Seng Tech ETF reclaiming MA20 with follow-through,
  3. internet-platform names moving off 60-day lows with ETF support.

## Assessment by tracked area

### Market regime
- **State:** risk_off
- **Assessment:** unfavorable for fresh momentum-driven swing entries

### Theme strength
- **Internet-platform:** weak
- **Hang Seng Tech:** weak
- **Consumer-tech:** weak / oversold
- **Hong Kong broad market:** neutral-to-weak

### ETF confirmation
- **Broad market:** partial but incomplete
- **Tech:** absent
- **Single-name upgrade allowed today:** no

### Standout names
- **Most constructive watch:** `2800.HK`
- **Most pressured:** `0700.HK`
- **Most oversold:** `1810.HK`
- **Cleanest theme proxy to monitor first:** `3033.HK`

## High-priority research questions for today
1. Does `2800.HK` have additional market-breadth or index-level evidence that would confirm its range state is improving rather than merely pausing inside a larger decline?
2. Between `3033.HK` and `3067.HK`, which ETF provides the cleaner and more liquid confirmation signal for Hang Seng Tech trend reversal in this cycle?
3. Are Tencent and Alibaba showing any non-price evidence of stabilization relative to the Hang Seng Tech ETFs, or are they still just following the same weak theme structure?
4. Is Xiaomi’s 60-day-range low reading historically more associated with reflex rebounds or with continued downside when the broader HK tech complex is risk-off?
5. What explicit rebound-risk markers should be required before issuing any `avoid` call on clustered HK tech names under the current defensive-misread pattern?
