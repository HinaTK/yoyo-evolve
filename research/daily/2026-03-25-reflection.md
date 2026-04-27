# Investment Reflection — 2026-03-25 14:39

## Input quality

Today's market assessment, daily plan, and daily report are empty. That makes this a thin-evidence session. I should not infer a current market regime, theme strength, ETF confirmation, or symbol-level setup from posterior evaluation alone.

The only usable evidence is the posterior summary. It is useful for calibrating my process, not for confirming today's trades.

## Weakest confidence

Confidence is weakest in four places:

1. **Current regime** — no live index, breadth, volume, macro, or tape read is provided.
2. **ETF/theme confirmation** — no current ETF follow-through data is available, and the latest `2800.HK` / `3067.HK` `buy_candidate` calls failed at T+3.
3. **Short-term timing** — the repeated pattern remains: early windows fail even when longer windows sometimes improve. `2800.HK` passed by T+20 after failing T+3; `3067.HK` failed T+3 and was only mixed by T+20.
4. **Bullish upgrades on low-pass-rate symbols** — symbol stats remain weak, especially `0700.HK` with a 0.087 pass rate and `2800.HK` with 0.13. Any upgrade without broad-market and ETF confirmation would be process drift.

## Missing evidence

Before any actionable upgrade, I still need:

- Current Hang Seng / HSCEI / Hang Seng Tech direction and breadth.
- ETF confirmation from `2800.HK`, `3033.HK`, and `3067.HK`, including follow-through rather than one-session headline movement.
- Volume confirmation and support/resistance levels for each candidate.
- A horizon-separated setup: T+3/T+5 timing evidence distinct from T+10/T+20 thesis evidence.
- Explicit invalidation levels for every recommendation.

Without those, the correct state remains `watch_only`.

## Likely failure modes for today's recommendations

Because today's recommendation posture is effectively `watch_only`, the main risks are process failures rather than trade failures:

1. **Posterior substitution** — treating T+20 outcomes as if they prove today's live setup. They do not.
2. **Timing complacency** — accepting medium-window improvement while ignoring repeated T+3/T+5 weakness.
3. **ETF overconfidence** — assuming ETF-level trades are safer than single-name trades even when recent ETF `buy_candidate` timing has failed.

## Recommendation posture

- Market regime: `unknown`
- Theme strength: `unconfirmed`
- ETF confirmation: `missing`
- Symbol-level recommendations: `watch_only`
- Timing confidence: `low`
- Thesis confidence: `low to moderate only where posterior direction improved, but not actionable without live confirmation`

No `buy_candidate`, `accumulate`, `hold`, `sell_candidate`, or `avoid` call is justified from today's inputs.

## Priority shifts for next cycle

1. **Start with horizon separation.** Before judging any symbol, write separate T+3/T+5 timing confidence and T+10/T+20 thesis confidence.
2. **Require live ETF confirmation before single-name upgrades.** Especially for `0700.HK`, `1810.HK`, and `9988.HK`, where pass rates remain poor or mixed.
3. **Treat ETF buy candidates with the same timing discipline as single names.** The recent `2800.HK` and `3067.HK` misses show that ETF structure does not remove early-window risk.
4. **Keep defensive calls rebound-aware.** `3067.HK` recently failed as an `avoid` at T+3 but passed at T+10, so near-term bounce risk must be explicit before any future `avoid`.

## Memory update decision

No memory files changed today. The repeated posterior patterns are already encoded in active learnings, stable rules, and error patterns: thin/conflicting evidence defaults to `watch_only`, posterior data cannot substitute for live confirmation, low-pass-rate upgrades require broad-market plus ETF confirmation, and repeated T+3/T+5 misses require downgraded timing confidence.
