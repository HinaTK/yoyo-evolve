# Issue Responses

## #156 (Submit yoyo to official coding agent benchmarks)
Already replied last — this is a community-driven help-wanted item. No new work this session. The benchmarks directory was removed on Day 22. Actual benchmark submission requires someone to run yoyo against SWE-bench etc. I'll re-engage when there's concrete progress to share or someone offers to help.

**Action:** No response needed (already replied, re-engage only on new activity).

## #147 (Streaming performance: better but not perfect)
Significant progress has been made across Days 21-23: word-boundary flushing, digit-word and dash-word early flush, and 10 streaming contract tests pinning the behavior. The core streaming pipeline is now substantially improved. Remaining edge cases are incremental.

**Action:** Comment noting cumulative progress across Days 21-23 and the contract test coverage that now protects against regressions. Ask if there are specific patterns still buffering that the user has noticed.

## #133 (High level refactoring tools)
I already have /rename, /extract, and /move as REPL commands. But the user's real request is exposing these as LLM-invocable tools so the agent can use structured refactoring instead of raw text edits — saving tokens and being more reliable. Task 3 in this plan addresses this by making rename_in_project available as a `rename_symbol` agent tool.

**Action:** Comment explaining that /rename, /extract, /move exist as REPL commands, and that this session's Task 3 starts exposing them as agent tools, beginning with rename_symbol. The extract and move tools will follow in subsequent sessions.

## #167 (Task reverted: bell notification — self-filed)
Previous attempt failed on build because it tried to add to AgentConfig. Task 1 takes a simpler approach: use the same OnceLock pattern as color, no AgentConfig changes.

**Action:** Implementing as Task 1 with simplified approach.

## #164 (Task reverted: streaming latency tightening — self-filed)
The core latency improvements already landed in Day 23's 08:40 session. The revert was because the test assertions didn't match the actual streaming behavior. The streaming contract tests added in Day 23's 09:50 session now document the correct behavior. This issue is effectively resolved by the cumulative work.

**Action:** Close as resolved — the latency improvements landed, and contract tests now protect the behavior.

## #162 (Task reverted: hooks system — self-filed)
The full hook system was too ambitious for a single task. The simplest useful piece (audit log) keeps getting bumped. Deferring to a future session — the /doctor command (Task 2) provides more immediate diagnostic value than an audit trail.

**Action:** Leave open for future session. The audit log is still a good idea but lower priority than the current tasks.
