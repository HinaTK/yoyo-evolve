Title: Improve /undo causality harness for edge cases
Files: src/commands_git.rs
Issue: #279

## Problem

Issue #279 describes a causality violation: `/undo` reverts code but journal entries and
conversation history still reference the reverted code. Day 41 added context injection
(a `[System note]` injected into the agent's next turn) for interactive `/undo`, which was
a good first step. But @yuanhao reopened saying "harness needs improvement."

The current gaps:
1. **`/undo --last-commit` journal awareness:** The context note mentions journal entries
   but doesn't actually check if the reverted commit was journaled. The note is generic.
2. **Test coverage is thin:** The test at line ~2011 (`handle_undo_returns_some_when_files_reverted`)
   only verifies that `handle_undo` returns `Some` when there's history. It doesn't verify
   the CONTENT of the context string — e.g., that it mentions the specific files.
3. **Missing test for `handle_undo_last_commit` context content:** The test at line ~2130
   verifies the revert succeeds but doesn't check the returned context string content.

## Fix

### Improve test harness

Add focused tests that verify the context string CONTENT (not just Some/None):

1. **`test_build_undo_context_mentions_files`:** Verify that `build_undo_context` includes
   each file name in its output. The function is already tested (line 1960) but only checks
   that the string contains "System note" and lists items — add assertions for specific
   file names.

2. **`test_undo_context_warns_about_stale_references`:** Verify the context string includes
   the ⚠️ warning about stale conversation references (this is the causality fix).

3. **`test_handle_undo_context_contains_affected_files`:** Extend the existing
   `handle_undo_returns_some_when_files_reverted` test to unwrap the `Some` and verify
   the context string mentions the specific files that were reverted.

4. **`test_handle_undo_last_commit_context_content`:** Extend the existing
   `handle_undo_last_commit` test to check the returned context string mentions
   the commit hash and the ⚠️ warning.

### Improve context string quality

The `build_undo_context` function (line 395) currently produces a generic note. Enhance it:
- Include a count of affected files
- Add a recommendation to "re-read affected files before making new changes"

The `handle_undo_last_commit` context (line 536) already has good content including the
journal warning. Keep it. Just ensure tests verify it.

## Verification

```bash
cargo test handle_undo -- --nocapture
cargo test build_undo_context -- --nocapture
cargo test undo -- --nocapture
```

All tests should pass. The new tests should verify context string content, not just existence.
