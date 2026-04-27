# Market Assessment — 2026-03-13

## Scope and process

This assessment covers the HK stocks and ETFs in the active watchlist: Tencent (`0700.HK`), Alibaba (`9988.HK`), Xiaomi (`1810.HK`), Tracker Fund of Hong Kong (`2800.HK`), Hang Seng Tech ETF (`3033.HK`), and iShares Hang Seng TECH ETF (`3067.HK`). Time horizon is swing trading, roughly 14–90 days. Portfolio is currently 100% cash, with `2800.HK` on watch only.

Given the posterior record of repeated bullish and defensive misreads, I am applying the stable rule: do not upgrade low-pass-rate symbols without broad-market and ETF confirmation. Default action when uncertain is `watch_only`.

---

## Facts

### Market regime

- Snapshot risk state: `neutral`.
- Average stock move across watched single names: `+0.309%`.
- Average ETF move across watched ETFs: `-1.123%`.
- 5 of 6 watchlist instruments carry `downtrend` regime flags.
- Tencent is the only non-downtrend item, flagged as `range`.
- Broad HK ETF `2800.HK` closed at `25.72`, down `-1.229%`, below both MA20 (`26.425`) and MA60 (`26.584`).
- `2800.HK` sits near the lower part of its 60-day range, with `range_pos_60 = 0.1022`.
- `2800.HK` volume was above its 20-day average, with `volume_ratio_20 = 1.1645`.

### Theme strength

- Internet platform stocks were the relative leaders:
  - Alibaba (`9988.HK`): `+0.684%`.
  - Tencent (`0700.HK`): `+0.183%`.
- Consumer tech was flat:
  - Xiaomi (`1810.HK`): `+0.060%`.
- Hang Seng Tech ETF exposure was weak:
  - `3033.HK`: `-1.097%`.
  - `3067.HK`: `-1.044%`.
- Broad HK exposure was also weak:
  - `2800.HK`: `-1.229%`.

### ETF confirmation

- Broad-market ETF confirmation is negative today:
  - `2800.HK` is below MA20 and MA60.
  - `2800.HK` closed at the session low (`latest_low = 25.72`, `latest_close = 25.72`).
  - Its 1-day decline occurred on above-average volume.
- Hang Seng Tech ETF confirmation is also negative:
  - `3033.HK` is below MA20 (`5.0141`) and MA60 (`5.3464`).
  - `3067.HK` is below MA20 (`10.743`) and MA60 (`11.4525`).
  - Both tech ETFs are near the low end of their 60-day ranges (`0.1651` and `0.1535`).
- Tech ETF liquidity differs materially:
  - `3033.HK` volume ratio is `1.038` with high turnover.
  - `3067.HK` volume ratio is `0.499`, showing weaker participation.

### Standout names

#### Tencent (`0700.HK`)

- Latest close: `547.5`.
- 1-day move: `+0.183%`.
- Above MA20 (`527.4`) but below MA60 (`577.8833`).
- 60-day range position: `0.3473`.
- Volume ratio: `0.5955`.
- Regime flag: `range`.

#### Alibaba (`9988.HK`)

- Latest close: `132.5`.
- 1-day move: `+0.684%`.
- Below MA20 (`141.395`) and MA60 (`151.1083`).
- 60-day range position: `0.1314`.
- Volume ratio: `0.6314`.
- Regime flag: `downtrend`.

#### Xiaomi (`1810.HK`)

- Latest close: `33.32`.
- 1-day move: `+0.060%`.
- Below MA20 (`34.503`) and MA60 (`36.6267`).
- 60-day range position: `0.1529`.
- Volume ratio: `0.5929`.
- Regime flag: `downtrend`.

---

## Interpretations

### Market regime interpretation

The headline risk state is neutral, but the internal picture is defensive. The strongest fact is not the small positive move in single-name internet stocks; it is the failed ETF confirmation. Broad HK exposure and Hang Seng Tech exposure both sold off, both remain below key moving averages, and the broad ETF closed at its low on above-average volume.

For a 14–90 day swing process, this is not enough evidence to lean risk-on. It is also not enough to issue broad `avoid` calls, because the snapshot lacks explicit rebound-risk evidence beyond one daily bar. The disciplined posture is defensive watchfulness: preserve cash, require confirmation, and avoid upgrading single names just because they outperformed for one day.

### Theme strength interpretation

Internet-platform stocks showed relative strength against weak ETFs. That makes Tencent and Alibaba worth watching, but not actionable yet. The theme is not confirmed because the tech ETFs fell more than 1% and remain in downtrends.

Xiaomi does not stand out. It was only marginally positive while remaining below MA20 and MA60 with weak relative volume. Consumer-tech exposure has no current confirmation from this snapshot.

### ETF confirmation interpretation

ETF confirmation is the main veto today. Both the broad HK ETF and Hang Seng Tech ETFs argue against upgrading individual internet-platform names. This matters because the active rules specifically warn against single-name upgrades when broad-market and ETF confirmation are absent.

The most important distinction is between relative strength and actionable strength. Tencent and Alibaba are relatively stronger than the ETFs, but the ETF layer says the broader trade is still fragile.

### Standout-name interpretation

- Tencent is the cleanest watchlist name because it is above MA20 and not formally in downtrend. But it remains below MA60 and volume is light. This is a watchlist improvement, not a buy signal.
- Alibaba had the best 1-day performance, but it remains deeply below both moving averages, close to the bottom of its 60-day range, and in downtrend. Treat the move as a possible bounce attempt, not trend repair.
- Xiaomi remains weak. The flat day does not change the downtrend structure.
- `2800.HK` is the most important risk barometer. Its weak close on above-average volume makes broad-market confirmation absent.
- `3033.HK` is the better Hang Seng Tech ETF proxy than `3067.HK` today because participation is stronger, but both structures remain weak.

---

## Risk posture

Portfolio posture: **cash-preserving / watch-only**.

Reasons:

1. The portfolio is already 100% cash, so there is no need to force exposure.
2. Broad ETF confirmation is negative.
3. Hang Seng Tech ETF confirmation is negative.
4. Most watchlist symbols remain below MA20 and MA60.
5. Posterior evaluation shows low pass rates across the watched symbols, especially `0700.HK` (`0.06`), `3067.HK` (`0.137`), and `2800.HK` (`0.176`).
6. Recent bullish calls on broad-index exposure have failed, so new bullish exposure needs breadth, volume, and moving-average confirmation.

Risk controls for any future upgrade:

- Do not exceed 10% single-position exposure.
- Do not exceed 30% theme exposure across internet-platform / Hang Seng Tech names.
- No leverage, no inverse ETFs, no low-liquidity trades.
- Require ETF confirmation before upgrading Tencent, Alibaba, or Xiaomi.

---

## Recommendation states

### `2800.HK` — Tracker Fund of Hong Kong

- State: `watch_only`.
- Rationale: Broad-market ETF is weak and below MA20/MA60; recent broad-index bullish calls have had failures.
- Evidence:
  - Down `-1.229%` today.
  - Closed at session low.
  - Below MA20 and MA60.
  - Above-average volume on the decline.
- Risks:
  - A near-term rebound is possible from a low 60-day range position.
  - One-day weakness may overstate downside if the next session recovers quickly.
- Invalidation for watch-only caution: reclaim MA20 with improving breadth and volume, then stabilize above it.
- Time horizon: 14–90 days.
- Confidence: medium for caution, low for directional downside timing.

### `3033.HK` — Hang Seng Tech ETF

- State: `watch_only`.
- Rationale: Tech ETF confirmation is negative despite some single-name relative strength.
- Evidence:
  - Down `-1.097%` today.
  - Below MA20 and MA60.
  - Downtrend flag.
  - Near lower part of 60-day range.
- Risks:
  - Rebound risk exists because range position is low.
  - High trading volume can precede either capitulation or further distribution; this snapshot alone does not resolve which.
- Invalidation for caution: reclaim MA20 first, then show follow-through toward MA60 with volume support.
- Time horizon: 14–90 days.
- Confidence: medium for watch-only.

### `3067.HK` — iShares Hang Seng TECH ETF

- State: `watch_only`.
- Rationale: Same weak structure as `3033.HK`, with even weaker participation today.
- Evidence:
  - Down `-1.044%` today.
  - Below MA20 and MA60.
  - Volume ratio only `0.499`.
  - Downtrend flag.
- Risks:
  - Lower volume makes signal quality weaker.
  - May rebound with the theme if larger tech ETFs stabilize.
- Invalidation for caution: volume expands while price reclaims MA20 and holds above it.
- Time horizon: 14–90 days.
- Confidence: medium for watch-only, low for timing.

### `0700.HK` — Tencent

- State: `watch_only`.
- Rationale: Best-quality single-name setup, but ETF confirmation is absent and volume is light.
- Evidence:
  - Positive 1-day move.
  - Above MA20.
  - Only watchlist item flagged as `range` rather than `downtrend`.
  - Still below MA60 with volume ratio `0.5955`.
- Risks:
  - Could outperform before ETF confirmation arrives.
  - Low historical pass rate argues against upgrading early.
- Invalidation for watch-only: reclaim MA60 or show strong follow-through with tech ETF confirmation; without ETF confirmation, do not upgrade.
- Time horizon: 14–90 days.
- Confidence: medium for relative strength watch, low for entry timing.

### `9988.HK` — Alibaba

- State: `watch_only`.
- Rationale: Best 1-day leader, but still structurally weak.
- Evidence:
  - Up `+0.684%` today.
  - Below MA20 and MA60.
  - Low 60-day range position.
  - Downtrend flag.
  - Volume ratio `0.6314`.
- Risks:
  - Bounce attempt may continue briefly from depressed range position.
  - Downtrend structure remains intact.
- Invalidation for watch-only: reclaim MA20 with ETF confirmation and improving volume; stronger invalidation would be sustained move toward MA60.
- Time horizon: 14–90 days.
- Confidence: medium for watch-only.

### `1810.HK` — Xiaomi

- State: `watch_only`.
- Rationale: No actionable evidence; flat price action inside downtrend.
- Evidence:
  - Up only `+0.060%`.
  - Below MA20 and MA60.
  - Low range position.
  - Weak volume ratio `0.5929`.
- Risks:
  - Could rebound with broader tech beta.
  - Current snapshot does not show independent strength.
- Invalidation for watch-only: reclaim MA20 with volume above average and ETF confirmation from Hang Seng Tech exposure.
- Time horizon: 14–90 days.
- Confidence: medium for watch-only.

---

## Bottom line

Today is a **watch-only day**. Single-name internet-platform strength is visible, especially in Alibaba and Tencent, but ETF confirmation is negative. The broad market ETF and Hang Seng Tech ETFs remain below moving averages and near the lower end of their 60-day ranges. With the portfolio fully in cash and recent posterior evidence warning against premature bullish upgrades, the correct move is patience.

The first upgrade candidate, if conditions improve, would be Tencent because it is above MA20 and not in downtrend. But the gate is external: Hang Seng Tech ETF confirmation and broad-market stabilization must improve first.

---

## High-priority research questions for today

1. Did `2800.HK` weakness reflect broad market breadth deterioration, or was it concentrated in a few index-heavy names?
2. Are `3033.HK` and `3067.HK` showing follow-through below their March 13 lows, or was this a short-term washout near the bottom of the 60-day range?
3. Is Tencent’s relative strength supported by company-specific catalysts, or is it only defensive rotation inside a weak tech tape?
4. Can Alibaba reclaim MA20 with volume, or is the `+0.684%` move just a low-volume bounce inside a downtrend?
5. Which is the better confirmation instrument for Hang Seng Tech exposure today: the more liquid `3033.HK` or the cleaner but lower-volume `3067.HK`?
