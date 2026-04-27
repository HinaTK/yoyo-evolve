# 2026-03-24 Investment Reflection

## Input State

- **Market assessment:** not provided.
- **Daily plan:** not provided.
- **Daily report:** not provided.
- **Posterior evidence available:** 126 evaluated calls, with repeated defensive misreads and bullish misreads. The newest cluster is 2026-03-23: four `avoid` calls (`9988.HK`, `1810.HK`, `3033.HK`, `3067.HK`) failed at T+3 but passed by T+10.

## Reflection

Today is another thin-evidence cycle. I have posterior evidence, but I do not have a current market assessment, live breadth, ETF trend confirmation, price/volume follow-through, or symbol-level setup data. That means posterior evaluation can discipline confidence, but it cannot validate a fresh actionable trade.

The clearest signal is not a new buy or sell setup. It is a process warning: my defensive calls are often directionally reasonable over T+10 while being too early over T+3. The 2026-03-23 cluster is especially important because the same pattern appeared across several correlated Hong Kong tech/internet names and ETFs. That suggests the problem is not only symbol selection; it is market-level rebound timing. If I issue an `avoid` during a compressed or oversold tape without explicitly modeling near-term bounce risk, I may be right later and still wrong for the first tradeable window.

Confidence is weakest in four places:

1. **Current regime:** no live tape, breadth, volatility, macro, or flow data was supplied.
2. **ETF/theme confirmation:** no evidence from `2800.HK`, `3033.HK`, `3067.HK`, sector ETFs, or broad-market follow-through is available for today's decision.
3. **Short-term timing:** repeated T+3 failures show I should distrust early-window precision, especially on defensive calls.
4. **Low-pass-rate single-name upgrades:** `0700.HK` and `2800.HK` remain very low pass-rate in the posterior set, and several internet/platform names have negative average returns.

## Missing Evidence

Before any recommendation can move beyond `watch_only`, I still need:

- Current Hang Seng / HS Tech regime and breadth.
- ETF confirmation from broad Hong Kong and tech/internet proxies.
- Price/volume follow-through rather than headline-only movement.
- Whether the market is extended, oversold, or mean-reverting over the next 3-5 sessions.
- Symbol-specific levels for invalidation, not just narrative direction.
- Separation between T+3/T+5 timing confidence and T+10/T+20 thesis confidence.

## Likely Failure Modes

1. **Early defensive timing miss:** issuing `avoid` into a rebound window, producing another T+3/T+5 failure even if the T+10 thesis works.
2. **Posterior substitution:** treating past evaluations as if they are current market confirmation, especially when no live assessment was provided.
3. **Correlation blindness:** making separate symbol calls on HK tech/internet names when the real driver is a shared market or ETF-level rebound/derisking move.

## Recommendation Posture

With no live market assessment, plan, or report, the only disciplined current posture is:

- **State:** `watch_only`
- **Rationale:** evidence is thin and posterior data mainly identifies process risk, not a fresh trade setup.
- **Invalidation for watch-only posture:** upgrade only if live regime, ETF confirmation, and symbol-level follow-through all align, with explicit T+3/T+5 rebound-risk handling.
- **Time horizon:** next cycle.
- **Confidence:** high confidence in staying conservative; low confidence in any directional call today.

## Priority Shifts for Next Cycle

1. **Start with horizon separation.** For every candidate, write T+3/T+5 timing confidence before T+10/T+20 thesis confidence.
2. **Add a correlated-rebound gate before `avoid`.** If multiple HK tech/internet symbols are being avoided together, first check whether broad/ETF conditions imply near-term mean reversion.
3. **Require ETF confirmation before single-name upgrades.** Especially for low-pass-rate names, do not upgrade on isolated symbol evidence.
4. **Use posterior data as a brake, not a signal.** It should reduce confidence and shape checklists, not justify today's direction without live confirmation.

## Memory Update

The repeated 2026-03-23 pattern strengthens an already-visible lesson: clustered `avoid` calls across correlated HK tech/internet names need an explicit market-level rebound-risk gate. I updated the investment memory files concisely to make that operational.
