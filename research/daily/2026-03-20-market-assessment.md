# Market Assessment — 2026-03-20

**Role:** yoyo-invest  
**Market focus:** Hong Kong stocks and ETFs  
**Time horizon:** swing, 14–90 days  
**Portfolio state:** 100% cash; 2800.HK remains watch-only seed position with no cost basis.

## 1. Market Regime

### Facts

- Snapshot date: 2026-03-20.
- Market summary risk state: `risk_off`.
- Average stock move across watched single names: **-5.284%**.
- Average ETF move across watched ETFs: **-1.552%**.
- All six watched instruments carry a `downtrend` regime flag.
- Three instruments also show `volume-expansion`: 9988.HK, 1810.HK, and 2800.HK.
- Every watched symbol closed below both its 20-day and 60-day moving averages.

### Interpretation

This is not a constructive swing-entry regime. The broad pattern is synchronized downside, not isolated weakness. The fact that ETFs are also below both moving averages means single-name rebounds need to be treated as tactical bounces unless confirmed by the broader market.

Given the stable rule after repeated bullish misreads, I should not upgrade low-pass-rate symbols to `hold`, `accumulate`, or `buy_candidate` without broad-market and ETF confirmation. Today does not provide that confirmation.

**Market posture:** defensive / watch-only.

## 2. Theme Strength

### Facts

| Theme | Symbols | 1D move | Position vs trend |
|---|---:|---:|---|
| Internet platform | 0700.HK | -0.975% | Below MA20 and MA60; range_pos_60 0.0458 |
| Internet platform | 9988.HK | -6.288% | Below MA20 and MA60; range_pos_60 0.0000; volume ratio 2.1492 |
| Consumer tech | 1810.HK | -8.590% | Below MA20 and MA60; range_pos_60 0.1808; volume ratio 2.1176 |
| Hong Kong broad market | 2800.HK | -0.776% | Below MA20 and MA60; range_pos_60 0.0224; volume ratio 1.6568 |
| Hang Seng Tech | 3033.HK | -2.254% | Below MA20 and MA60; range_pos_60 0.0724 |
| Hang Seng Tech | 3067.HK | -1.625% | Below MA20 and MA60; range_pos_60 0.0921 |

### Interpretation

Theme strength is weak across the whole watchlist. Internet platforms are split at the single-name level: Tencent is relatively resilient, while Alibaba is breaking to the bottom of its 60-day range on expanded volume. Consumer tech is the weakest observed theme because Xiaomi has the largest one-day decline and expanded volume.

The Hang Seng Tech ETF pair is not confirming a bullish technology setup. Both ETFs are below their 20-day and 60-day moving averages and near the lower end of their 60-day ranges. That matters because the rules explicitly prefer ETF confirmation before upgrading a single-stock thesis.

## 3. ETF Confirmation

### Facts

- 2800.HK closed at **25.56**, below MA20 **26.165** and MA60 **26.6027**.
- 2800.HK range_pos_60 is **0.0224**, near the bottom of its 60-day range.
- 2800.HK volume ratio is **1.6568**, showing volume expansion on a down day.
- 3033.HK closed at **4.77**, below MA20 **4.9325** and MA60 **5.3097**.
- 3067.HK closed at **10.29**, below MA20 **10.573** and MA60 **11.3765**.
- 3033.HK and 3067.HK both have `downtrend` flags; neither has a bullish confirmation flag.

### Interpretation

ETF confirmation is negative. The broad-market ETF is near the bottom of its 60-day range with expanded volume, while both Hang Seng Tech ETFs remain in downtrends. This blocks bullish upgrades in internet-platform and technology names even if individual stocks show relative strength.

For swing timing, this is especially important: a single-name bounce inside weak ETF structure has elevated failure risk over T+3/T+5 windows, which has already been a recurring error pattern.

## 4. Standout Names

### 0700.HK — Tencent

**Facts**

- Latest close: **508.0**.
- One-day move: **-0.975%**.
- Below MA20 **527.875** and MA60 **572.125**.
- range_pos_60: **0.0458**.
- Volume ratio: **0.816**, below 20-day average volume.
- Regime flag: `downtrend`.

**Interpretation**

Tencent is the relative-strength standout among single stocks because its one-day loss is modest and volume did not expand. But relative strength inside a downtrend is not enough for a bullish call. Its low 60-day range position and lack of ETF confirmation keep it at `watch_only`.

**High-priority trigger to monitor:** reclaim of MA20 with ETF confirmation from 3033.HK/3067.HK.  
**Invalidation for any bullish watch thesis:** continued failure below MA20 plus new 60-day lows or volume expansion on downside.

### 9988.HK — Alibaba

**Facts**

- Latest close: **123.7**.
- One-day move: **-6.288%**.
- Below MA20 **135.7** and MA60 **149.8583**.
- range_pos_60: **0.0000**, bottom of 60-day range.
- Volume ratio: **2.1492**, expanded volume.
- Regime flags: `downtrend`, `volume-expansion`.

**Interpretation**

Alibaba is a downside standout. The combination of a large one-day decline, 60-day range low, and expanded volume is distribution-like. However, because blunt `avoid` calls can be early at T+3/T+5, the near-term bounce risk must be stated separately: after a sharp high-volume drop, oversold rebounds are possible even while the medium-term swing structure remains poor.

**Current state:** `watch_only` / defensive avoid for new entries, not a fresh short or inverse expression.  
**Invalidation of defensive view:** reclaim of MA20 with falling downside volume and ETF confirmation.

### 1810.HK — Xiaomi

**Facts**

- Latest close: **33.2**.
- One-day move: **-8.590%**, worst in watchlist.
- Below MA20 **34.14** and MA60 **36.095**.
- range_pos_60: **0.1808**.
- Volume ratio: **2.1176**, expanded volume.
- Regime flags: `downtrend`, `volume-expansion`.
- Posterior evaluation notes recent 2026-03-19 `buy_candidate` misfires over T+5 and T+20.

**Interpretation**

Xiaomi is the clearest recent error-control name. The prior bullish call has been contradicted by both price and evaluation evidence. I should not repair that thesis by averaging down or reframing it as longer-term. Today’s data says the swing setup failed.

**Current state:** `watch_only`; no upgrade.  
**Invalidation of bearish/failed-setup view:** stabilization above MA20, reduction in sell-volume pressure, and confirmation from Hang Seng Tech ETFs.

### 2800.HK — Tracker Fund of Hong Kong

**Facts**

- Latest close: **25.56**.
- One-day move: **-0.776%**, best relative move in the watchlist.
- Below MA20 **26.165** and MA60 **26.6027**.
- range_pos_60: **0.0224**.
- Volume ratio: **1.6568**, expanded volume.
- Regime flags: `downtrend`, `volume-expansion`.

**Interpretation**

2800.HK is the broad-market confirmation instrument, and it is not confirming risk-on exposure. Even though it is the relative leader by one-day return, it remains near the 60-day low with expanded volume. That makes the whole market backdrop fragile.

**Current state:** `watch_only`.  
**Invalidation of defensive market view:** reclaim of MA20 and improvement in range position without renewed volume-heavy selling.

### 3033.HK and 3067.HK — Hang Seng Tech ETFs

**Facts**

- 3033.HK one-day move: **-2.254%**; close **4.77**, below MA20 and MA60.
- 3067.HK one-day move: **-1.625%**; close **10.29**, below MA20 and MA60.
- 3033.HK range_pos_60: **0.0724**.
- 3067.HK range_pos_60: **0.0921**.
- Both carry `downtrend` flags.
- Recent evaluations show 2026-03-19 `avoid` calls on both passed over T+5 and T+20 windows.

**Interpretation**

The Hang Seng Tech ETF pair supports caution. They are not collapsing as hard as Alibaba or Xiaomi, but they are not confirming a rebound either. For today, they are best used as gatekeepers: no bullish single-name technology upgrade until at least one, preferably both, begin reclaiming short-term trend levels.

## 5. Risk Posture

### Facts

- Portfolio is 100% cash.
- Risk profile is balanced.
- Max single position is 10%.
- Max theme exposure is 30%.
- Leverage, inverse ETFs, and low-liquidity instruments are not allowed.
- Default action when uncertain is `watch_only`.
- Current market regime is `risk_off`.
- Posterior evaluation shows weak recent pass rates for several watched symbols, especially 0700.HK, 1810.HK, and 2800.HK at 0.133 pass rate each.

### Interpretation

Cash is an appropriate position today. The watchlist offers falling prices, but not enough confirmation. Because the regime is risk-off and ETF confirmation is negative, dip-buying would be a momentum-dependent setup in a hostile tape. That is exactly where the active learnings say to default to `watch_only`.

If any action is taken later, sizing should remain below normal until broad ETF confirmation improves. No single-name position should be initiated merely because the price is lower.

## 6. Assessment Summary

| Area | Assessment |
|---|---|
| Market regime | Risk-off; all watched symbols in downtrend |
| Theme strength | Weak across internet platforms, consumer tech, broad HK, and Hang Seng Tech |
| ETF confirmation | Negative; 2800.HK, 3033.HK, and 3067.HK all below MA20/MA60 |
| Relative strength | Tencent and 2800.HK declined least, but remain technically weak |
| Downside standouts | Xiaomi and Alibaba: large declines on expanded volume |
| Risk posture | Preserve cash; watch-only; require confirmation before upgrading |

**Primary conclusion:** Today is a capital-preservation day, not an entry day. The cleanest edge is patience: wait for broad-market and ETF confirmation before treating single-name weakness as opportunity.

## High-Priority Research Questions for Today

1. Did any macro, policy, earnings, or sector-specific headline explain the volume-expanded selloff in Alibaba and Xiaomi, or was the move mostly market-wide de-risking?
2. Are 2800.HK, 3033.HK, and 3067.HK seeing outflows or abnormal creation/redemption activity that would confirm institutional risk reduction?
3. Is Tencent’s relative resilience supported by company-specific news or fundamentals, or is it only lower beta inside a broad selloff?
4. What price/volume behavior would mark a real Hang Seng Tech ETF reversal rather than another short-lived oversold bounce?
5. Given recent bullish misreads, should Xiaomi be temporarily demoted from candidate generation until it shows at least one confirmed stabilization window?
