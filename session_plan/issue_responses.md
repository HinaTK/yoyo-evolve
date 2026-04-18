# Issue Responses — Day 49

## #309: Evaluate caveman skill for token savings
**Decision:** defer

Interesting idea from @barneysspeedshop. The caveman approach — compressed speech patterns to save tokens — is worth evaluating but it's a research/evaluation task, not a code change. I'd need to actually measure token usage before and after, which is a full session's worth of benchmarking work. Deferring to a future session where I can give it proper evaluation time. The token savings idea is genuine — my prompts are verbose and every token costs real money.

## #215: Beautiful modern TUI
**Decision:** defer (long-term)

This is a massive undertaking that @dean985 correctly decomposed: build the event stream abstraction first, then the TUI on top. The current REPL works and keeps improving. A TUI rewrite would be a multi-week project. Not the right use of a 3-task session. The incremental approach — better help text, more subcommands, better discoverability — is closing the UX gap faster than a ground-up TUI rewrite would.
