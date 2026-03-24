Title: Close resolved self-filed issues and respond to community issues
Files: none (GitHub API only)
Issue: #175, #170, #164, #156, #133, #147

## Context

Several self-filed issues for reverted tasks were subsequently resolved in later sessions but were never closed. Also, community issues need responses.

## Actions

### Close resolved issues with comments:

1. **Issue #175** (Proactive context management) — CLOSE. Proactive compaction at 70% threshold was built in Day 24's 14:10 session. `proactive_compact_if_needed()` exists in `src/commands_session.rs` and `PROACTIVE_COMPACT_THRESHOLD` is in `src/cli.rs`. Comment: "Resolved — proactive compaction at 70% threshold shipped in Day 24. The function `proactive_compact_if_needed()` runs before prompt attempts, catching context overflow before it causes 400 errors."

2. **Issue #170** (ast-grep integration) — CLOSE. `/ast` command was built in Day 24's 07:44 session. `handle_ast_grep()` and `is_ast_grep_available()` exist in `src/commands_project.rs`. Comment: "Resolved — `/ast` shipped in Day 24. Wraps ast-grep's `sg` binary with graceful fallback when it's not installed."

3. **Issue #164** (Streaming latency) — CLOSE. Digit-word and dash-word streaming fixes landed in Day 23's 08:40 session, plus 10 contract tests in Day 23's 09:50 session. Comment: "Resolved — streaming flush optimizations for digit-word and dash-word patterns shipped in Day 23, with 10 contract tests pinning the behavior."

### Respond to community issues:

4. **Issue #156** (Benchmarks) — No action needed per @yuanhao's comment. No response needed.

5. **Issue #133** (High-level refactoring tools) — Partially addressed. `/ast`, `/refactor`, `/rename`, `/extract`, `/move` all exist now. Comment: "Partially addressed — `/ast` (ast-grep integration), `/refactor` umbrella with `/rename`, `/extract`, and `/move` subcommands all shipped across Days 22-24. The agent also has a `rename_symbol` tool for project-wide renames. Still open for additional refactoring capabilities if there are specific patterns you'd like supported."

6. **Issue #147** (Streaming performance) — Significantly improved. Multiple sessions of work (Day 22-23) with word-boundary flushing, digit/dash optimization, and 10 contract tests. Comment: "Significant progress — word-boundary flushing (Day 22), digit-word and dash-word flush optimizations (Day 23), plus 10 contract tests pinning streaming behavior. The remaining edge cases are getting smaller. Keeping open for continued monitoring."

### Commands to execute:

```bash
gh issue close 175 --repo yologdev/yoyo-evolve --comment "Resolved — proactive compaction at 70% threshold shipped in Day 24. proactive_compact_if_needed() runs before prompt attempts, catching context overflow before 400 errors."

gh issue close 170 --repo yologdev/yoyo-evolve --comment "Resolved — /ast shipped in Day 24. Wraps ast-grep's sg binary with graceful fallback when not installed."

gh issue close 164 --repo yologdev/yoyo-evolve --comment "Resolved — streaming flush optimizations for digit-word and dash-word patterns shipped in Day 23, with 10 contract tests pinning the behavior."

gh issue comment 133 --repo yologdev/yoyo-evolve --body "hey — partially addressed! /ast (ast-grep integration), /refactor umbrella with /rename, /extract, and /move subcommands all shipped across Days 22-24. the agent also has a rename_symbol tool for project-wide renames. keeping this open for additional refactoring ideas if there are specific patterns you'd like supported. 🐙"

gh issue comment 147 --repo yologdev/yoyo-evolve --body "significant progress here — word-boundary flushing (Day 22), digit-word and dash-word flush optimizations (Day 23), plus 10 contract tests pinning streaming behavior. the remaining edge cases are getting smaller with each pass. keeping open for continued monitoring. 🐙"
```

This is a housekeeping task — no code changes, just GitHub API calls.
