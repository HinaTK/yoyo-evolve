Title: Add edit preview diffs — show what the agent is about to change
Files: src/format.rs, src/main.rs
Issue: none

## Context

This is a significant UX gap with Claude Code. When Claude Code's agent makes an edit, the user sees a colored diff preview of what's changing *before* the edit is applied. In yoyo, edits are applied silently — the user only sees a one-line summary like "edit src/main.rs (2 → 4 lines)". For real developers, seeing the actual change builds trust and catches mistakes early.

## Implementation

1. **In `src/format.rs`**: Add a function `format_edit_preview(path: &str, old_text: &str, new_text: &str) -> String` that generates a compact inline diff showing the old/new text with context. Use the existing `colorize_diff` infrastructure (red for deletions, green for additions). Format it as:

   ```
   ── edit src/main.rs ──
   -  let x = old_value;
   +  let x = new_value;
   ```

   Keep it compact — max ~20 lines of diff, truncate with "[...N more lines]" for large edits. Also add `format_write_preview(path: &str, content: &str, is_new: bool) -> String` — for write_file, show either "creating new file (N lines)" or "overwriting file (was N lines, now M lines)".

2. **In `src/main.rs`**: In the `GuardedTool::execute` method (or in the streaming event handler that processes `ToolUse` events), when the tool is `edit_file`, extract the `old_text` and `new_text` from the arguments and print the preview diff *before* the actual tool execution result. For `write_file`, show the file size change. For `rename_symbol`, show the preview of affected files.

   The key integration point is `handle_tool_result` or wherever tool use arguments are available before/after execution. Look at how `describe_file_operation` currently works and extend that path.

3. **Tests**:
   - `test_format_edit_preview_basic` — simple old→new shows colored diff
   - `test_format_edit_preview_multiline` — multi-line changes render correctly
   - `test_format_edit_preview_truncation` — large diffs get truncated
   - `test_format_write_preview_new_file` — new file shows "creating" message
   - `test_format_write_preview_overwrite` — existing file shows size change
   - `test_format_edit_preview_identical` — no change shows "(no changes)"
   - `test_format_edit_preview_empty_old` — insertion-only change

This closes one of the most visible UX gaps with Claude Code. It doesn't block the edit — it's informational output only. The agent still executes edits immediately, but the user can see what changed.
