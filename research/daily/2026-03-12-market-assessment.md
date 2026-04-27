# Market Assessment — 2026-03-12

**Agent:** yoyo-invest  
**Market focus:** Hong Kong stocks and ETFs  
**Time horizon:** swing, 14–90 days  
**Portfolio posture:** 100% cash; 2800.HK on watch only  
**Default when uncertain:** `watch_only`

## 1. Market Regime

### Facts

- Snapshot risk state is **neutral**.
- Average 1-day stock move across the watched single names: **-0.772%**.
- Average 1-day ETF move across watched ETFs: **-0.315%**.
- Five of six watched instruments carry a **downtrend** regime flag.
- Tencent, the only non-downtrend name, is flagged as **range**.
- Broad-market ETF 2800.HK closed at **26.04**, below both its 20-day moving average (**26.508**) and 60-day moving average (**26.5847**).
- 2800.HK sits at **0.219** of its 60-day range, with above-average volume at **1.09x** its 20-day average.

### Interpretation

The market is not in outright panic on this snapshot, but the structure is weak. The neutral risk label conflicts with the symbol-level evidence: most instruments are below key moving averages and clustered in the lower quarter of their 60-day ranges. That argues against upgrading exposure today.

The broad ETF is especially important because portfolio cash is 100% and any first allocation should probably start with market confirmation, not single-name conviction. 2800.HK has liquidity and slightly elevated volume, but price remains below both moving averages. That is not enough confirmation for a balanced swing entry.

**Regime stance:** cautious neutral / weak tape.  
**Action bias:** preserve cash; watch for stabilization rather than anticipate reversal.

## 2. Theme Strength

### Facts

| Theme | Instruments | Snapshot condition |
|---|---:|---|
| Internet platform | 0700.HK, 9988.HK | Tencent range; Alibaba downtrend |
| Consumer tech | 1810.HK | Downtrend |
| Hong Kong broad market | 2800.HK | Downtrend |
| Hang Seng Tech | 3033.HK, 3067.HK | Both downtrend |

- Tencent closed at **546.5**, above its 20-day moving average (**527.575**) but below its 60-day moving average (**578.7833**).
- Alibaba closed at **131.6**, below its 20-day moving average (**142.795**) and 60-day moving average (**151.41**), with 60-day range position **0.1123**.
- Xiaomi closed at **33.3**, below its 20-day moving average (**34.616**) and 60-day moving average (**36.7743**), with 60-day range position **0.1511**.
- Hang Seng Tech ETFs 3033.HK and 3067.HK are both below their 20-day and 60-day moving averages.

### Interpretation

No watched theme has clean confirmation today. Internet platforms are mixed: Tencent is the relative-quality name because it remains above the 20-day average, but Alibaba is near the bottom of its 60-day range and still in downtrend. That split weakens the theme read.

Consumer tech has no confirmation. Xiaomi is only down **-0.12%** on the day, making it the best 1-day stock performer in the watchlist, but it remains below both moving averages and near the lower part of its 60-day range. A small daily decline is not the same as strength.

Hang Seng Tech remains weak as a theme. Both ETFs are in downtrend and below moving averages. This blocks an upgrade for the internet-platform and consumer-tech single names under the rule requiring ETF confirmation before upgrading single-stock trades.

**Strongest relative theme:** none; internet-platform is only selectively less weak because Tencent is holding above MA20.  
**Weakest theme:** Hang Seng Tech / growth tech remains structurally unconfirmed.

## 3. ETF Confirmation

### Facts

| ETF | Close | 1D move | MA20 | MA60 | 60D range position | Volume ratio | Regime |
|---|---:|---:|---:|---:|---:|---:|---|
| 2800.HK | 26.04 | -0.230% | 26.508 | 26.5847 | 0.2190 | 1.0900 | downtrend |
| 3033.HK | 4.924 | -0.243% | 5.0369 | 5.3556 | 0.2152 | 0.5775 | downtrend |
| 3067.HK | 10.54 | -0.472% | 10.7925 | 11.4722 | 0.2018 | 0.6394 | downtrend |

- 2800.HK has the highest volume confirmation among ETFs at **1.09x** 20-day volume.
- 3033.HK and 3067.HK both traded on below-average volume.
- All three ETFs are in the lower quarter of their 60-day ranges.

### Interpretation

ETF confirmation is absent. The broad-market ETF has liquidity and some volume, but price has not reclaimed moving averages. The Hang Seng Tech ETFs are weaker: both are below MA20/MA60 with subdued volume.

Because the posterior evaluation summary shows repeated bullish misreads and low pass rates for several symbols, I should not use single-name resilience as a substitute for ETF confirmation. Today that means Tencent cannot be upgraded just because it is above MA20; the ETF layer does not support it.

**ETF signal:** no upgrade.  
**Preferred stance:** `watch_only` across ETFs unless follow-through appears above MA20 with improving breadth.

## 4. Standout Names

## 0700.HK — Tencent

### Facts

- Close: **546.5** HKD.
- 1-day move: **-0.996%**.
- Above MA20 (**527.575**) but below MA60 (**578.7833**).
- 60-day range position: **0.3397**, highest among the watchlist.
- Volume ratio: **0.6676**, below average.
- Regime flag: **range**.

### Interpretation

Tencent is the relative standout, but not an actionable long setup today. It is the only watched name above its 20-day average and the only one not flagged as downtrend. However, it remains below MA60, declined nearly 1% on the day, and traded on low relative volume.

The key problem is confirmation. Hang Seng Tech ETFs are still in downtrend, and Alibaba is weak. Tencent may be a better-quality watch candidate, but the theme is not confirming.

**State:** `watch_only`  
**Time horizon:** 14–90 days  
**Confidence:** medium for watchlist priority; low for entry timing  
**Invalidation for constructive watch:** close back below MA20 with continued weak ETF confirmation, or a break toward the lower half of its recent range on rising volume.

## 9988.HK — Alibaba

### Facts

- Close: **131.6** HKD.
- 1-day move: **-1.201%**, worst among watched names.
- Below MA20 (**142.795**) and MA60 (**151.41**).
- 60-day range position: **0.1123**, lowest among the watchlist.
- Volume ratio: **0.702**, below average.
- Regime flag: **downtrend**.

### Interpretation

Alibaba is the weakest single-name setup today. It is near the bottom of its 60-day range, under both moving averages, and lagging Tencent within the same theme.

However, a blunt `avoid` call should separate near-term rebound risk from medium-term weakness. Because Alibaba is already stretched toward the bottom of its range and volume is not capitulation-level in this snapshot, a short-term bounce is possible. The medium-term thesis remains weak unless it reclaims MA20 and theme ETFs confirm.

**State:** `watch_only` with defensive bias; not an entry candidate  
**Time horizon:** 14–90 days  
**Confidence:** medium that setup is weak; low on near-term timing because rebound risk exists  
**Invalidation for defensive bias:** reclaim of MA20 with improving volume plus Hang Seng Tech ETF confirmation.

## 1810.HK — Xiaomi

### Facts

- Close: **33.3** HKD.
- 1-day move: **-0.120%**, best single-stock 1-day performance in the watchlist.
- Below MA20 (**34.616**) and MA60 (**36.7743**).
- 60-day range position: **0.1511**.
- Volume ratio: **0.5124**, low.
- Regime flag: **downtrend**.

### Interpretation

Xiaomi looks superficially stable on the day, but the setup is not confirmed. It is still below both moving averages, near the low end of its 60-day range, and trading on low relative volume.

The posterior summary flags recent failed `accumulate` calls on Xiaomi. That posterior evidence should reduce confidence, not become current-session confirmation. The live snapshot does not justify another bullish upgrade.

**State:** `watch_only`  
**Time horizon:** 14–90 days  
**Confidence:** low for entry; medium that patience is warranted  
**Invalidation for watch-only caution:** reclaim of MA20 with rising volume and confirmation from 3033.HK/3067.HK.

## 2800.HK — Tracker Fund of Hong Kong

### Facts

- Close: **26.04** HKD.
- 1-day move: **-0.230%**.
- Below MA20 (**26.508**) and MA60 (**26.5847**).
- 60-day range position: **0.2190**.
- Volume ratio: **1.09**, strongest ETF volume confirmation in the watchlist.
- Regime flag: **downtrend**.

### Interpretation

2800.HK is the cleanest instrument for broad-market monitoring because it is liquid and directly reflects Hong Kong market beta. But the current price action is still weak. Elevated volume below moving averages can mean institutional interest, but it can also mean distribution. The snapshot does not distinguish those outcomes.

Because the portfolio is 100% cash, this remains the first ETF to research for a potential starter allocation, but not an automatic buy today.

**State:** `watch_only`  
**Time horizon:** 14–90 days  
**Confidence:** medium for monitoring priority; low for immediate entry  
**Invalidation for neutral watch:** further downside on rising volume without reclaiming MA20; constructive upgrade requires reclaim of MA20 and stabilization above MA60 or clear higher-low structure.

## 3033.HK / 3067.HK — Hang Seng Tech ETFs

### Facts

- 3033.HK close: **4.924**, down **-0.243%**, below MA20 (**5.0369**) and MA60 (**5.3556**).
- 3067.HK close: **10.54**, down **-0.472%**, below MA20 (**10.7925**) and MA60 (**11.4722**).
- Both are near the lower fifth of their 60-day ranges.
- Both have below-average volume ratios: **0.5775** for 3033.HK and **0.6394** for 3067.HK.
- Both are flagged **downtrend**.

### Interpretation

The Hang Seng Tech ETF pair confirms weakness, not recovery. This is the main blocker for upgrading Tencent, Alibaba, or Xiaomi. Between the two, 3033.HK has much higher turnover in this snapshot, so it is the better vehicle to monitor for confirmation; 3067.HK is useful as a cross-check but less liquid here.

**State:** `watch_only`  
**Time horizon:** 14–90 days  
**Confidence:** medium that ETF confirmation is absent  
**Invalidation for bearish/neutral ETF read:** reclaim of MA20 by both ETFs, preferably with volume ratios above 1.0 and improving single-name breadth.

## 5. Risk Posture

### Facts

- Portfolio is **100% cash**.
- Risk profile is **balanced**.
- Maximum single-position size is **10%**.
- Maximum theme exposure is **30%**.
- Leverage, inverse ETFs, and low-liquidity instruments are not allowed.
- Current watchlist has concentrated exposure to Hong Kong broad beta and technology/growth themes.
- Posterior evaluation shows repeated bullish misreads and low pass rates for several watched symbols:
  - 0700.HK pass rate: **0.2**.
  - 1810.HK pass rate: **0.2**.
  - 2800.HK pass rate: **0.2**.
  - 3033.HK pass rate: **0.3**.
  - 3067.HK pass rate: **0.3**.
  - 9988.HK pass rate: **0.5**.

### Interpretation

The correct risk posture today is defensive patience. Cash is not a problem; it is useful optionality while the ETF layer remains weak.

The main risk is not missing the exact bottom. The main risk is repeating the documented error pattern: upgrading single names before ETF and broad-market confirmation. Given the current snapshot, that would be especially dangerous in Tencent and Xiaomi, where relative resilience could tempt an early bullish call.

If any position is considered after further research, sizing should start below the maximum 10% single-position cap because timing confidence is low. Theme exposure should remain well below 30% until both broad-market and Hang Seng Tech ETFs confirm.

## 6. Recommendation Summary

| Symbol | State | Priority | Rationale |
|---|---|---:|---|
| 0700.HK | `watch_only` | High | Best relative single-name structure, but no ETF confirmation and below MA60. |
| 9988.HK | `watch_only` | Medium | Weakest internet-platform name; rebound risk prevents blunt avoid, but no long setup. |
| 1810.HK | `watch_only` | Medium | Stable 1-day move, but downtrend, low range position, low volume, and recent bullish misfires. |
| 2800.HK | `watch_only` | High | Best broad-market monitor; volume is notable, but price remains below MA20/MA60. |
| 3033.HK | `watch_only` | High | Primary Hang Seng Tech confirmation vehicle; currently weak. |
| 3067.HK | `watch_only` | Medium | Confirms 3033.HK weakness; lower turnover makes it secondary. |

**Overall action:** stay in cash and watch.  
**No new buy/accumulate/hold upgrade today.**  
**Short-term timing confidence:** low.  
**Medium-term thesis confidence:** neutral-to-cautious until ETF confirmation improves.

## 7. High-Priority Research Questions for Today

1. **Is 2800.HK showing accumulation or distribution?** Examine intraday/volume context around the above-average volume day while price remains below MA20 and MA60.
2. **What would confirm a real Hang Seng Tech reversal?** Define concrete trigger levels for 3033.HK and 3067.HK: MA20 reclaim, MA60 reclaim, volume threshold, and breadth across Tencent/Alibaba/Xiaomi.
3. **Is Tencent's relative strength durable or just defensive rotation?** Compare Tencent against 3033.HK and 9988.HK over 5–20 trading days without treating single-name resilience as theme confirmation.
4. **Does Alibaba have rebound risk from oversold conditions despite medium-term weakness?** Separate tactical bounce indicators from swing-trend repair signals.
5. **What initial allocation rule should apply when moving from 100% cash?** Draft a staged entry plan that respects the 10% single-name cap and requires ETF confirmation before technology theme exposure rises.
