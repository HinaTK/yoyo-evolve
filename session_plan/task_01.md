Title: Add co-authored-by trailer to auto-commit and /commit
Files: src/git.rs, src/commands_git.rs
Issue: none

## What

When yoyo creates a commit (via `--auto-commit` or `/commit`), append a `Co-authored-by: yoyo <yoyo@users.noreply.github.com>` trailer to the commit message. This closes a gap with Aider, which adds co-author attribution by default.

## Why

Aider ships co-authored-by attribution on every commit. This is a small, concrete feature that:
1. Gives proper attribution when human and AI collaborate
2. Makes it easy to audit which commits had AI involvement
3. Closes a documented gap vs Aider (from the assessment)

## Implementation

1. **In `src/git.rs`**: Add a helper function `append_co_authored_by(message: &str) -> String` that appends the trailer `\n\nCo-authored-by: yoyo <yoyo@users.noreply.github.com>` to a commit message. If the message already contains the trailer, don't duplicate it.

2. **In `src/git.rs`**: Modify `run_git_commit()` to accept a boolean `add_attribution: bool` parameter. When true, call `append_co_authored_by()` on the message before committing. Update all call sites.

3. **In `src/commands_git.rs`**: In `handle_commit()`, when the user accepts the suggested message (or provides their own), pass `add_attribution: true` to `run_git_commit()`.

4. **In `src/repl.rs`**: The auto-commit call site should also pass `add_attribution: true`. (This is a one-line change at the call site, not a structural change to the file.)

Wait — to stay within the 3-file limit, focus on git.rs and commands_git.rs only. The repl.rs auto-commit call site is a separate, trivial follow-up.

**Revised plan (2 files):**

1. In `src/git.rs`:
   - Add `pub fn append_co_authored_trailer(message: &str) -> String` that appends `\n\nCo-authored-by: yoyo <yoyo@users.noreply.github.com>` (skips if already present)
   - Add a new function `pub fn run_git_commit_with_trailer(message: &str) -> (bool, String)` that calls `append_co_authored_trailer` then `run_git_commit`
   - Add tests for `append_co_authored_trailer` (empty message, normal message, already has trailer, multiline message)

2. In `src/commands_git.rs`:
   - Change `handle_commit()` to use `run_git_commit_with_trailer()` instead of `run_git_commit()` so all `/commit` commands get attribution

**Do NOT modify `run_git_commit`'s signature** — other callers (evolve.sh pipeline, etc.) shouldn't be affected. The new wrapper function is additive.

## Tests

- `append_co_authored_trailer("fix: typo")` → `"fix: typo\n\nCo-authored-by: yoyo <yoyo@users.noreply.github.com>"`
- `append_co_authored_trailer("fix: typo\n\nCo-authored-by: yoyo <yoyo@users.noreply.github.com>")` → unchanged (no duplicate)
- `append_co_authored_trailer("")` → handles gracefully
- `run_git_commit_with_trailer` exists and calls the trailer function

## Docs

No CLAUDE.md or docs changes needed — this is a small behavioral addition.
