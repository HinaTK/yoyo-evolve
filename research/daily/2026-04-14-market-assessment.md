# Market Assessment — 2026-04-14

## Scope
- **Agent:** yoyo-invest
- **Market focus:** HK stocks, ETFs
- **Time horizon:** swing (14-90 days)
- **Risk profile:** balanced
- **Default action when uncertain:** `watch_only`
- **Portfolio starting point:** 100% cash; existing watch status on `2800.HK`

## Facts

### Broad market snapshot
- Market snapshot is labeled **as of 2026-04-14**.
- Market summary risk state: **`risk_on`**.
- Average 1-day move:
  - Stocks: **+0.809%**
  - ETFs: **+0.755%**
- Watchlist names all finished positive on the day.

### Regime by instrument
- `2800.HK` is flagged **`range`**.
- `0700.HK`, `9988.HK`, `1810.HK`, `3033.HK`, and `3067.HK` are flagged **`downtrend`**.

### Distance vs moving averages
- `0700.HK`: close **493.2** vs MA20 **509.5** and MA60 **545.1083**.
- `9988.HK`: close **124.5** vs MA20 **125.76** and MA60 **144.2467**.
- `1810.HK`: close **30.88** vs MA20 **32.742** and MA60 **34.4147**.
- `2800.HK`: close **26.2** vs MA20 **25.663** and MA60 **26.435**.
- `3033.HK`: close **4.75** vs MA20 **4.7564** and MA60 **5.1172**.
- `3067.HK`: close **10.2** vs MA20 **10.2095** and MA60 **10.9698**.

### 60-day range position
- `0700.HK`: **0.0766**
- `9988.HK`: **0.1091**
- `1810.HK`: **0.0301**
- `2800.HK`: **0.4310**
- `3033.HK`: **0.1639**
- `3067.HK`: **0.1595**

### Volume / participation
- `3033.HK` volume ratio vs 20-day average: **1.103**.
- All other names have volume ratios below 1.0:
  - `0700.HK`: **0.6852**
  - `9988.HK`: **0.5577**
  - `1810.HK`: **0.5371**
  - `2800.HK`: **0.7284**
  - `3067.HK`: **0.6132**

### Standout 1-day movers in this universe
- Leaders by 1-day move:
  1. `9988.HK` **+1.055%**
  2. `2800.HK` **+0.924%**
  3. `3067.HK` **+0.791%**
- Laggards by 1-day move:
  1. `3033.HK` **+0.550%**
  2. `0700.HK` **+0.653%**
  3. `1810.HK` **+0.718%**

### Posterior discipline inputs
- Recent evaluations show repeated failures on 2026-04-13 `avoid` calls across `0700.HK`, `9988.HK`, `1810.HK`, `3033.HK`, and `3067.HK` over T+3 and T+10 windows.
- Symbol pass rates remain low:
  - `0700.HK`: **0.07**
  - `1810.HK`: **0.256**
  - `2800.HK`: **0.14**
  - `3033.HK`: **0.256**
  - `3067.HK`: **0.163**
  - `9988.HK`: **0.279**
- Active rules require broad-market plus ETF confirmation before upgrading low-pass-rate symbols and require rebound-risk checks before issuing clustered `avoid` calls.

## Interpretations

### Market regime
The tape is **not bearish enough for fresh defensive calls**, even though most watched names remain below both 20-day and 60-day moving averages. The market-level `risk_on` label and uniformly positive 1-day closes point to a short-term rebound tone inside a still-damaged medium-term structure. For swing trading, that means the regime is **early stabilization / rebound watch**, not confirmed trend reversal.

### Theme strength
- **Hong Kong broad market** is the strongest theme on this list today. `2800.HK` is the only name not flagged downtrend and is the only instrument trading above its 20-day average.
- **Hang Seng Tech** is improving only marginally. Both `3033.HK` and `3067.HK` are still below 20-day and 60-day averages, with low 60-day range positions. This is rebound behavior, not trend recovery.
- **Internet platform stocks** (`0700.HK`, `9988.HK`) participated in the up day, but neither showed strong confirmation through price location or volume. They remain deep in the lower end of their 60-day ranges.
- **Consumer tech** (`1810.HK`) looks weakest on range position. Xiaomi is near the bottom of its 60-day range despite the green close.

### ETF confirmation
ETF confirmation is **mixed and incomplete**:
- `2800.HK` gives some confirmation that the broad Hong Kong market is stabilizing.
- The tech ETFs do **not** yet confirm a durable risk-on rotation into growth/tech. Both remain below key moving averages and near the lower end of their 60-day ranges.
- Because stable rules say to prefer ETF confirmation before upgrading single-stock theses, the current ETF picture is enough to block aggressive bullish upgrades on `0700.HK`, `9988.HK`, and `1810.HK`.

### Standout names
- **`2800.HK`** is the cleanest watchlist name today. It has the best regime label, a positive day, and a close above MA20. That does not yet make it actionable, but it is the closest thing to constructive confirmation in the set.
- **`9988.HK`** had the strongest 1-day move, but it lacks follow-through evidence: still below MA20/MA60, low range position, and weak relative volume. This is a bounce candidate, not a confirmed swing long.
- **`3033.HK`** had the only above-average volume ratio, which matters, but price remains below both moving averages. Increased activity without reclaiming trend levels is not enough on its own.
- **`0700.HK` and `1810.HK`** remain technically weak despite green closes. Their low 60-day range positions argue against treating this session as a regime change.

### Risk posture
Given the combination of:
1. positive short-term tape,
2. weak medium-term trend structure,
3. incomplete ETF confirmation for tech,
4. recent posterior evidence showing defensive misreads,

the correct posture is **cautious, non-defensive, and still mostly observational**.

That means:
- do **not** issue clustered `avoid` calls on HK tech/internet after the recent rebound-related misses,
- do **not** upgrade low-pass-rate single names to `buy_candidate` without stronger ETF and broad-market confirmation,
- keep the book defensive through **cash preservation**, not through bearish calls.

## Assessment by symbol

### `2800.HK` — Tracker Fund of Hong Kong
- **State:** `watch_only`
- **Why:** Best broad-market confirmation in the set; above MA20 and not flagged downtrend.
- **What is missing:** Clear reclaim of MA60 and stronger follow-through volume.
- **Invalidation for constructive watch:** Loss of recent stabilization and renewed weakness back below MA20 with deteriorating broad-market tone.

### `3033.HK` / `3067.HK` — Hang Seng Tech ETFs
- **State:** `watch_only`
- **Why:** These are the correct confirmation instruments for any tech/internet upgrade, but both still show downtrend structure.
- **What is missing:** Sustained closes above MA20, then evidence of pressure toward MA60, ideally with continued volume support.
- **Invalidation for constructive watch:** Failure to build on the bounce and renewed downside that keeps them pinned in the lower part of the 60-day range.

### `0700.HK` / `9988.HK` — Internet platform
- **State:** `watch_only`
- **Why:** Positive day, but still no broad enough confirmation to overcome weak trend structure and low pass-rate history.
- **What is missing:** Tech ETF confirmation plus improvement in price location versus MA20 and 60-day range.
- **Invalidation for constructive watch:** Tech ETFs rolling over again before these names reclaim trend levels.

### `1810.HK` — Xiaomi
- **State:** `watch_only`
- **Why:** The weakest range position among the single stocks; bounce is insufficient evidence.
- **What is missing:** Relative strength versus both the tech ETFs and the broad market, plus reclaim of MA20.
- **Invalidation for constructive watch:** Continued inability to leave the bottom of the 60-day range.

## Today’s operating conclusion
No symbol earns an actionable upgrade today. The best interpretation is that **the broad market is attempting stabilization while tech and internet remain in unconfirmed rebound mode**. Under the current rules and recent posterior misfires, the disciplined output is **all names remain `watch_only`**, with `2800.HK` as the lead confirmation instrument and `3033.HK` / `3067.HK` as the gatekeepers for any later tech upgrade.

## High-priority research questions for today
1. Can `2800.HK` hold above its 20-day average for multiple sessions and start challenging the 60-day average, or is this still a range-bound bounce?
2. Do `3033.HK` and `3067.HK` show follow-through above MA20 in the next few sessions, giving real ETF confirmation for HK tech risk?
3. If internet-platform names keep bouncing, is the move being led by ETF/broad-market confirmation or only by single-name mean reversion?
4. Which watchlist name first shows improving volume **and** price-location confirmation together, rather than just a green day?
5. Does the current `risk_on` market summary persist long enough to justify moving from defensive cash posture to selective swing entry watchlists?
