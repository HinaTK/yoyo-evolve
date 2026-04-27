# Market Assessment — 2026-04-15

## Scope
- **Agent:** yoyo-invest
- **Market focus:** Hong Kong stocks and ETFs
- **Time horizon:** swing (14–90 days)
- **Portfolio starting point:** 100% cash; existing watch status on `2800.HK`
- **Process stance:** balanced risk; default to `watch_only` when uncertainty is high

## Facts

### Market regime
- Snapshot date: **2026-04-15**
- Market summary risk state: **risk_on**
- Average 1-day move:
  - Stocks: **+1.511%**
  - ETFs: **+0.892%**
- No snapshot failures were reported.

### Symbol facts
| Symbol | Name | 1D % | vs MA20 | vs MA60 | 60d Range Pos | Vol Ratio 20 | Regime Flag |
|---|---|---:|---:|---:|---:|---:|---|
| 0700.HK | Tencent | +1.176% | -1.59% | -8.10% | 0.1149 | 0.7749 | downtrend |
| 9988.HK | Alibaba | +3.293% | +2.42% | -10.52% | 0.1836 | 0.9908 | range |
| 1810.HK | Xiaomi | +0.065% | -5.28% | -9.90% | 0.0333 | 0.5193 | downtrend |
| 2800.HK | Tracker Fund of Hong Kong | +0.153% | +2.15% | -0.69% | 0.4425 | 0.4815 | range |
| 3033.HK | Hang Seng Tech ETF | +1.347% | +1.27% | -5.64% | 0.2164 | 0.7338 | range |
| 3067.HK | iShares Hang Seng TECH ETF | +1.176% | +1.14% | -5.64% | 0.2062 | 0.7787 | range |

### Theme and ETF confirmation facts
- **Internet-platform theme**
  - `9988.HK` was the strongest stock in the snapshot at **+3.293%**.
  - `0700.HK` gained **+1.176%**, but remains below both MA20 and MA60 with a `downtrend` flag.
- **Hang Seng Tech ETF confirmation**
  - `3033.HK` and `3067.HK` both closed above MA20.
  - Both remain below MA60.
  - Both ETFs sit low in their 60-day ranges: **0.2164** and **0.2062**.
- **Broad Hong Kong market ETF confirmation**
  - `2800.HK` closed above MA20 and slightly below MA60.
  - `2800.HK` sits near the middle of its 60-day range at **0.4425**.
- **Consumer-tech theme**
  - `1810.HK` closed nearly flat at **+0.065%**.
  - It remains below MA20 and MA60, with the weakest 60-day range position in the set at **0.0333**.

### Posterior evaluation facts relevant to today
- Overall evaluation summary:
  - Pass: **51**
  - Fail: **75**
  - Informational: **136**
  - Mixed: **8**
- Learning candidates most frequent:
  - `defensive_misread`: **29**
  - `bullish_misread`: **26**
  - `overconfidence`: **20**
- Symbol pass rates:
  - `0700.HK`: **0.067**
  - `1810.HK`: **0.244**
  - `2800.HK`: **0.156**
  - `3033.HK`: **0.244**
  - `3067.HK`: **0.156**
  - `9988.HK`: **0.267**
- Recent misfires included `avoid` calls on `1810.HK` and tech ETFs that were early or wrong over short windows.

## Interpretations

### Market regime
- The tape is **risk-on for the day**, but not yet broadly strong enough to call a durable trend reversal.
- Breadth within this small universe is positive, yet most names are still below MA60. That argues for **short-term improvement inside medium-term caution**.
- The setup is better described as **rebound/range behavior** than clean trend resumption.

### Theme strength
- **Internet-platform** is the strongest theme on this snapshot because both major names were up and Alibaba materially outperformed.
- But theme quality is **mixed rather than confirmed**: Alibaba is above MA20, while Tencent is still flagged `downtrend` and remains well below MA60.
- **Consumer-tech** is weak. Xiaomi shows little participation and remains near the bottom of its 60-day range.

### ETF confirmation
- ETF evidence is **constructive but incomplete**.
- This matters because stable rules require preferring ETF confirmation before upgrading single-stock theses.
- The two Hang Seng Tech ETFs confirming above MA20 is a positive sign for the tech/internet complex.
- The missing piece is stronger medium-term confirmation: both tech ETFs are still below MA60 and still trading in the lower part of their 60-day ranges.
- Broad-market confirmation from `2800.HK` is steadier than single-name internet action, but volume participation is soft.

### Standout names
- **9988.HK (Alibaba)** is the clearest relative-strength name today.
  - Strongest 1-day move in the set.
  - Closed above MA20.
  - Volume ratio was near normal at **0.9908**, which is better than a low-participation bounce.
  - Still below MA60, so the move looks like **improving structure inside a larger range**, not a completed breakout.
- **0700.HK (Tencent)** improved on the day but still looks structurally weaker than Alibaba.
  - Below both moving averages.
  - Low 60-day range position.
  - Posterior pass rate is very weak, which argues against upgrading it on single-day strength.
- **1810.HK (Xiaomi)** remains the weakest chart in the list.
  - However, recent posterior mistakes on `avoid` calls mean weakness alone is **not enough** to issue a fresh defensive call without broader downside confirmation.

## Risk posture
- **Recommended posture today: `watch_only` bias across the watchlist.**
- Reason:
  1. The market snapshot is risk-on, but medium-term trend confirmation is still missing for most names.
  2. ETF confirmation exists at the MA20 level, not yet at the MA60 level.
  3. Posterior evidence warns against overconfident bullish upgrades and against blunt defensive calls on rebound-prone names.
  4. The portfolio is 100% cash, so there is no pressure to force exposure.
- If research later today uncovers stronger live confirmation, the first place to revisit would be **internet-platform via ETF-first framing**, not direct single-name conviction.
- Under current evidence, **no symbol should be upgraded beyond `watch_only` from this snapshot alone**.

## What matters most today
1. Determine whether the risk-on reading is a **one-day rebound** or the start of a broader swing recovery.
2. Test whether **Hang Seng Tech ETF strength persists** beyond a single session and begins to reclaim MA60 territory.
3. Check whether Alibaba’s leadership is **theme-backed** or just a stronger single-name bounce.
4. Avoid fresh `avoid` calls on weak charts unless downside confirmation improves materially.

## High-priority research questions
1. Do `3033.HK` and `3067.HK` show follow-through over the next few sessions, especially on volume, or is this only a low-range bounce?
2. Can `2800.HK` strengthen enough to provide broad-market confirmation for risk exposure, or does it remain a soft range-bound backdrop?
3. Is Alibaba’s outperformance being matched by Tencent and the tech ETFs, or is the internet-platform move still too narrow for a higher-conviction swing setup?
4. Does Xiaomi show any evidence of downside continuation with participation, or is it becoming another case where a weak chart still rebounds enough to punish an `avoid` call?
5. Which level is reclaimed first across the tech complex—recent swing highs or MA60—and does that change the action from `watch_only` to candidate generation?
