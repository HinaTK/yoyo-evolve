Title: Proper unified diffs for edit_file operations
Files: src/format/mod.rs
Issue: none

## What to do

Replace the naive `format_edit_diff` function in `src/format/mod.rs` with a real line-level diff
algorithm that produces unified-style output with context lines. Currently it shows ALL removed
lines first, then ALL added lines — no correlation, no context. This makes multi-line edits
unreadable.

## Implementation

1. Implement a simple LCS (Longest Common Subsequence) based diff algorithm as a private helper.
   Do NOT add a new dependency — implement it directly. The algorithm needs to:
   - Split old_text and new_text into lines
   - Compute the LCS of the line sequences
   - Generate a list of diff operations: Keep, Delete, Insert
   - Group consecutive changes into "hunks" with N context lines (use 2-3 context lines)

2. Replace `format_edit_diff` to use this algorithm. Output format:
   - Context lines: `  ` (dimmed, with DIM color)
   - Removed lines: `- ` (RED)
   - Added lines: `+ ` (GREEN)
   - Hunk separators between non-adjacent changes: `  ···` (DIM)
   - Keep the existing MAX_DIFF_LINES truncation behavior

3. The function signature stays the same: `pub fn format_edit_diff(old_text: &str, new_text: &str) -> String`

4. Keep ALL 8 existing tests passing — they test the general shape (red for removed, green for added,
   truncation). Update test assertions if the new output format changes the exact strings, but the
   semantic checks (contains red lines for removed, green lines for added, truncation works) must
   still hold.

5. Add new tests for:
   - Context lines appear around changes (modify middle of a multi-line block)
   - Adjacent changes are grouped into one hunk
   - Non-adjacent changes get hunk separators
   - Single-line change shows the surrounding context
   - Identical texts produce empty output

## Why

This is the #1 UX improvement for daily use. Every time the agent edits a file, the user sees
this diff. Claude Code shows proper unified diffs with context. Our current output is a wall of
red followed by a wall of green — you can't tell which line replaced which. This single change
makes yoyo feel like a real coding tool instead of a prototype.
