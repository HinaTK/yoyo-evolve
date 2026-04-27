# Market Assessment — 2026-03-23

## Scope and posture

- Agent: `yoyo-invest`
- Market focus: Hong Kong stocks and ETFs
- Horizon: swing, 14–90 days
- Portfolio state: 100% cash; `2800.HK` is watch-only seed position, not an active holding
- Risk profile: balanced
- Default action when uncertain: `watch_only`

This report separates observed facts from interpretation. It is not a trade order.

---

## 1. Market regime

### Facts

- Snapshot date: 2026-03-23
- Market summary risk state: `risk_off`
- Average 1-day stock move across the watchlist: `-2.853%`
- Average 1-day ETF move across the watchlist: `-3.563%`
- All six watchlist instruments are flagged `downtrend`.
- Four instruments closed at the bottom of their 60-day range with `range_pos_60 = 0.0`:
  - `0700.HK` Tencent
  - `9988.HK` Alibaba
  - `2800.HK` Tracker Fund of Hong Kong
  - `3033.HK` Hang Seng Tech ETF
- `3067.HK` also closed at `range_pos_60 = 0.0`.
- `1810.HK` Xiaomi is only slightly above the 60-day low with `range_pos_60 = 0.0552`.
- Broad-market ETF `2800.HK` fell `-3.365%` on volume expansion (`volume_ratio_20 = 1.5772`).

### Interpretation

The regime is broadly defensive. The strongest evidence is not just one-day weakness; it is the combination of universal downtrend flags, closes at or near 60-day lows, and ETF weakness with expanded volume. This is not a market where momentum-dependent bullish setups should be upgraded without confirmation.

Primary posture: `watch_only` with capital preservation priority.

---

## 2. Theme strength

### Facts

| Theme | Symbols | 1-day moves | Technical position |
|---|---:|---:|---|
| Internet platform | `0700.HK`, `9988.HK` | `-1.89%`, `-3.234%` | both below 20D and 60D moving averages; both at 60-day range low |
| Consumer tech | `1810.HK` | `-3.434%` | below 20D and 60D moving averages; near 60-day range low |
| Hong Kong broad market | `2800.HK` | `-3.365%` | below 20D and 60D moving averages; at 60-day range low; volume expansion |
| Hang Seng Tech ETFs | `3033.HK`, `3067.HK` | `-3.438%`, `-3.887%` | both below 20D and 60D moving averages; both at 60-day range low; `3067.HK` has volume expansion |

### Interpretation

No watched theme shows positive confirmation today. Internet platforms are weak, consumer tech is weak, broad Hong Kong beta is weak, and Hang Seng Tech ETFs are weaker than the single-name internet-platform leader. Theme-level evidence argues against upgrading any single stock to `buy_candidate`, `accumulate`, or `hold`.

The least-bad single name is Tencent by 1-day relative performance, but relative defensiveness inside a falling tape is not enough for a bullish swing call.

---

## 3. ETF confirmation

### Facts

- `2800.HK` closed at `24.70`, below:
  - 20D moving average: `26.035`
  - 60D moving average: `26.5827`
- `2800.HK` fell `-3.365%` with `volume_ratio_20 = 1.5772`.
- `3033.HK` closed at `4.606`, below:
  - 20D moving average: `4.8982`
  - 60D moving average: `5.2971`
- `3033.HK` fell `-3.438%`.
- `3067.HK` closed at `9.89`, below:
  - 20D moving average: `10.5035`
  - 60D moving average: `11.3498`
- `3067.HK` fell `-3.887%` with `volume_ratio_20 = 1.5062`.

### Interpretation

ETF confirmation is negative. Both broad-market and Hang Seng Tech ETFs confirm downside pressure rather than stabilizing. This is especially important because the current stable rules require ETF confirmation before upgrading internet-platform single-name trades.

Today the ETFs say: do not chase single-name rebound stories yet.

---

## 4. Standout names

### `0700.HK` Tencent — relative defensive leader, but still downtrend

#### Facts

- Latest close: `498.40`
- 1-day move: `-1.89%`
- 20D moving average: `525.895`
- 60D moving average: `570.1983`
- 60-day range position: `0.0`
- Volume ratio vs 20D: `1.126`
- Regime flag: `downtrend`
- It is listed as the top relative leader in the snapshot.
- Posterior stats supplied for the loop show low historical pass rate for `0700.HK`: `0.105` across 19 samples.

#### Interpretation

Tencent is the cleanest relative-strength watch item because it fell less than the rest of the list. But it remains below both key moving averages and at the bottom of its 60-day range. Given the low pass-rate history and absent ETF confirmation, this should remain `watch_only`, not a bullish upgrade.

What would improve the setup: a reclaim of the 20D moving average, stabilization in `2800.HK` and Hang Seng Tech ETFs, and reduced downside volume.

---

### `9988.HK` Alibaba — liquid but no live confirmation

#### Facts

- Latest close: `119.70`
- 1-day move: `-3.234%`
- 20D moving average: `134.075`
- 60D moving average: `149.4317`
- 60-day range position: `0.0`
- Volume ratio vs 20D: `1.3574`
- Regime flag: `downtrend`
- Posterior stats show the highest pass rate in the supplied set: `0.474` across 19 samples.

#### Interpretation

Alibaba has relatively better historical evaluation stats than the other watched names, but today’s live technical evidence is still negative. It is at the 60-day low, below both moving averages, and falling on above-average volume. The rule is explicit: posterior evidence can reduce confidence or calibrate process, but it cannot substitute for current-session confirmation.

Recommendation state remains `watch_only`.

---

### `1810.HK` Xiaomi — near-low weakness, no confirmation

#### Facts

- Latest close: `32.06`
- 1-day move: `-3.434%`
- 20D moving average: `33.915`
- 60D moving average: `35.9537`
- 60-day range position: `0.0552`
- Volume ratio vs 20D: `1.2885`
- Regime flag: `downtrend`

#### Interpretation

Xiaomi is weak in both absolute and relative terms. It is not the worst 1-day performer, but it is close to the 60-day low and lacks ETF or theme confirmation. No upgrade is justified.

Recommendation state remains `watch_only`.

---

### `2800.HK` Tracker Fund — broad-market risk gauge is negative

#### Facts

- Latest close: `24.70`
- 1-day move: `-3.365%`
- 20D moving average: `26.035`
- 60D moving average: `26.5827`
- 60-day range position: `0.0`
- Volume ratio vs 20D: `1.5772`
- Regime flags: `downtrend`, `volume-expansion`
- Portfolio has no real active position; `2800.HK` is marked watch-only.

#### Interpretation

`2800.HK` is the key broad-market confirmation instrument today, and it confirms risk-off. Expanded volume on a broad-market ETF decline argues against treating today’s weakness as merely isolated single-name noise.

Recommendation state remains `watch_only`. A defensive `avoid` call is tempting, but recent process rules require explicit rebound-risk handling. With 100% cash already, the higher-quality action is to wait for stabilization rather than issue a blunt avoid after a large down day.

---

### `3033.HK` / `3067.HK` Hang Seng Tech ETFs — negative theme confirmation

#### Facts

- `3033.HK` fell `-3.438%`, closed at `4.606`, below 20D and 60D moving averages, at 60-day range low.
- `3067.HK` fell `-3.887%`, closed at `9.89`, below 20D and 60D moving averages, at 60-day range low.
- `3067.HK` had volume expansion with `volume_ratio_20 = 1.5062`.
- Both ETFs are among the day’s laggards.
- Recent posterior evaluation includes a `3033.HK avoid` T+5 misfire on 2026-03-20: `+1.048%`, while T+3, T+10, and T+20 were passes.

#### Interpretation

The tech ETF complex confirms weakness. However, the recent `3033.HK avoid` T+5 misfire reinforces that timing can be noisy even when medium-window downside is correct. For today, the right posture is not to chase downside after a sharp fall; it is to recognize that ETF confirmation blocks bullish upgrades and to wait for either stabilization or a cleaner failed-rebound setup.

Recommendation state remains `watch_only` for both ETFs.

---

## 5. Risk posture

### Facts

- Portfolio is 100% cash.
- Maximum single-position size allowed: 10%.
- Maximum theme exposure allowed: 30%.
- Leverage is not allowed.
- Inverse ETFs are not allowed.
- Low-liquidity instruments are not allowed.
- Market regime is `risk_off`.
- Every watched symbol is below both 20D and 60D moving averages.

### Interpretation

Cash is currently an advantage, not a problem to solve. The process should avoid forcing action simply because prices are lower. The main risk today is not missing the exact bottom; it is upgrading into a falling, ETF-confirmed downtrend after repeated posterior evidence of bullish misreads.

Near-term bounce risk is real because several instruments are at 60-day lows after sharp one-day declines. That bounce risk is the reason to prefer `watch_only` over fresh `avoid` calls today. Medium-term downside risk remains elevated until broad-market and tech ETFs reclaim moving averages or at least stop making new lows.

---

## 6. Recommendation states for today

| Symbol | State | Rationale | Invalidation / upgrade trigger | Confidence |
|---|---|---|---|---|
| `0700.HK` | `watch_only` | Relative leader, but still below 20D/60D and at 60-day low; no ETF confirmation | Upgrade only if Tencent reclaims 20D while `2800.HK` and tech ETFs stabilize; downgrade if continued high-volume breakdown | Medium |
| `9988.HK` | `watch_only` | Historical pass rate is better, but live evidence is negative: below MAs, at 60-day low, above-average volume | Upgrade only with live price stabilization plus ETF confirmation; avoid posterior-only upgrade | Medium |
| `1810.HK` | `watch_only` | Weak single-name setup near 60-day low, no theme confirmation | Upgrade only after reclaiming 20D and consumer-tech/broad-market confirmation improves | Medium |
| `2800.HK` | `watch_only` | Broad ETF confirms risk-off with volume expansion; portfolio already in cash | Consider constructive only after stabilization above recent low and reduced selling volume; risk-off view invalidated by reclaim of 20D | High |
| `3033.HK` | `watch_only` | Tech ETF confirms downside, but avoid timing risk is high after sharp drop | Constructive only after reclaim/stabilization; avoid only on failed rebound with clear risk level | Medium |
| `3067.HK` | `watch_only` | Weakest ETF move with volume expansion; confirms tech risk-off | Same as `3033.HK`; avoid chasing after large one-day drop | Medium |

No `buy_candidate`, `accumulate`, `hold`, `trim`, `sell_candidate`, or `avoid` recommendation is justified today.

---

## 7. High-priority research questions for today

1. Did the 2026-03-23 selloff come from a broad macro/liquidity shock, Hong Kong-specific pressure, or China internet/tech-specific news?
2. Are `2800.HK`, `3033.HK`, and `3067.HK` seeing follow-through selling after this close, or was the volume expansion a capitulation-style one-day flush?
3. Which level should define the next swing invalidation zone for `2800.HK`: the 2026-03-23 low at `24.48`, the 20D moving average near `26.04`, or a broader 60-day structure?
4. Is Tencent’s relative strength (`-1.89%` versus weaker ETFs) supported by company-specific news/fundamentals, or is it just lower beta during a broad selloff?
5. Given repeated bullish misreads and low pass rates for several symbols, what minimum ETF confirmation checklist should be required before the next upgrade from `watch_only`?
