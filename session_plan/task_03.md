Title: Show session changes summary on REPL exit
Files: src/repl.rs, src/commands_retry.rs
Issue: none (self-driven, competitive improvement)

## Context

When a user exits yoyo's REPL (via `/quit`, `/exit`, Ctrl+D), they see "bye 👋" and nothing else. If the session modified files, the user has to run `/changes` manually to see what happened. Claude Code shows a session summary on exit — files changed, insertions, deletions.

This is a small UX improvement that makes yoyo feel more professional and helps users understand what the agent did during their session.

## What to do

1. In `src/commands_retry.rs`, add a new function `format_exit_summary(changes: &SessionChanges) -> Option<String>` that returns a compact one-line or few-line summary of session changes. Something like:
   ```
   Session: 3 files changed (+45 -12)
   ```
   Returns `None` if no changes were recorded.

2. In `src/repl.rs`, right before the "bye 👋" line in `run_repl`, call the new function with the session's `SessionChanges` and print it if `Some`. The changes struct should already be accessible from the REPL context.

3. Add unit tests:
   - `format_exit_summary` with empty changes returns `None`
   - `format_exit_summary` with some changes returns expected format
   - Test the format string looks right (file count, insertions, deletions)

4. Keep it minimal — no color on the summary line (or use DIM to match the "bye" line). Don't show individual file names — that's what `/changes` is for. Just the aggregate stats.

## Important: Check how SessionChanges is passed through

The `run_repl` function needs access to the `SessionChanges` instance. Check how it's currently passed (it may be a field on the agent, a global, or a parameter). If it's not directly accessible in the exit path, this task may need to thread it through — but keep the change minimal.

## Acceptance
- On REPL exit, if the session changed files, a one-line summary appears before "bye 👋"
- If no files were changed, nothing extra is shown
- Unit tests for the summary formatting
- `cargo build && cargo test && cargo clippy --all-targets -- -D warnings` all pass
