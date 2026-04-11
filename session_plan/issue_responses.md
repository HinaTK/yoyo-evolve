# Issue Responses — Day 42

## #279: /undo causality bug
Addressing as Task 2. The Day 41 fix added context injection for interactive `/undo`, which was a good start. This session improves the test harness: verifying context string content (not just existence), ensuring file names and stale-reference warnings appear in the injected context. The evolution-loop case (`git revert` in `evolve.sh`) is outside my modifiable files — that's a human-side change. But the interactive harness will be solid.

## #278: Challenge: Long-Working Tasks
Partially addressing as Task 3. Instead of building a `/extended` command, I'm removing the hardcoded execution limits (`max_turns: 200`, `max_total_tokens: 1_000_000`) that artificially constrain sessions. After this change, the default is unlimited — every session is effectively "extended." Users who want guardrails can set `--max-turns` or `--max-session-tokens` explicitly. This aligns with @yuanhao's comment: "unlimited should be the default."

The full `/extended` concept with RALPH-loop-style autonomous operation is a bigger design question I'll revisit in a future session. The limit removal is the first concrete step.

## #267: Help wanted: Export YOYO_SESSION_BUDGET_SECS (RESOLVED)
Closed by human. The investigation confirmed cancellations weren't cron overlap. The budget plumbing stays inert. No action needed.

## Other open issues
- #229 (Rust Token Killer), #226 (Evolution History), #215 (TUI), #214 (Interactive autocomplete), #156 (Submit to benchmarks), #141 (GROWTH.md), #98 (A Way of Evolution): No action this session. Prioritizing stability (flaky tests) and bug fixes (#279) first.
