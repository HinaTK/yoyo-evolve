# Issue Responses

## #185: Add --context-strategy flag: checkpoint-restart as alternative to compaction
Implementing as Task 2 this session. Wiring `on_before_turn` to monitor context usage, exit code 2 when checkpoint triggers, and the CLI flag. Task 1 is the prerequisite — getting `with_context_config` wired so yoagent knows the context budget.

## #183: Use yoagent's built-in context management instead of manual compaction
Implementing as Task 1 this session. This is a retry of the Day 25 revert (Issue #184). Being more surgical this time — ONLY adding `with_context_config()` and `with_execution_limits()` calls without removing any existing code. The manual compaction stays as a safety net until we verify the built-in compaction works well.

## #156: Submit yoyo to official coding agent benchmarks
@yuanhao said "for your information only. No action required." — acknowledged. This is a community-driven effort; I can't run benchmarks myself but I'd love to see results if someone tries it. No action this session.
