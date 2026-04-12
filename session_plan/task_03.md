Title: Wire co-authored-by trailer into auto-commit path in REPL
Files: src/repl.rs
Issue: none

## What

Follow-up to Task 1. Wire the `run_git_commit_with_trailer()` function (added in Task 1) into the auto-commit code path in `src/repl.rs`, so that `--auto-commit` also gets the co-authored-by attribution.

## Why

Task 1 adds the trailer to `/commit` (interactive commits). This task completes the feature by adding it to `--auto-commit` (automatic commits after each agent turn). Both paths should have attribution.

## Implementation

In `src/repl.rs`, find the auto-commit section (around line 1113-1122):

```rust
if agent_config.auto_commit && files_modified {
    let _ = run_git(&["add", "-A"]);
    if let Some(diff) = get_staged_diff() {
        if !diff.trim().is_empty() {
            let msg = generate_commit_message(&diff);
            let (ok, output) = run_git_commit(&msg);
```

Change `run_git_commit(&msg)` to `run_git_commit_with_trailer(&msg)`.

That's it — one function call change. Add the import for `run_git_commit_with_trailer` from `crate::git`.

## Tests

No new tests needed — the underlying `append_co_authored_trailer` and `run_git_commit_with_trailer` are tested in Task 1. This is purely a wiring change.

## Dependencies

This task MUST run after Task 1 (which creates `run_git_commit_with_trailer` in `src/git.rs`).
