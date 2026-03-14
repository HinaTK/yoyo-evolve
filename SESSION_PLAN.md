## Session Plan

### Task 1: Show colored diffs for file edits in the REPL
Files: src/prompt.rs, src/format.rs
Description: When `edit_file` runs, show a colored unified diff of the change inline — extract `old_text` and `new_text` from the tool args in `ToolExecutionStart`, compute a simple diff, and display it below the tool summary line. For `write_file`, show a summary line with the file path and line count of content being written (e.g., "write src/main.rs (42 lines)"). This is the single biggest trust/visibility gap vs Claude Code — users currently see `▶ edit src/main.rs ✓` with zero visibility into what changed.

Implementation details:
- In `format.rs`, add a `format_edit_diff(old_text: &str, new_text: &str) -> String` function that produces a colored unified diff (red for removed lines, green for added lines, dim for context). Keep it simple — no fancy diff algorithm needed, just show removed lines prefixed with `- ` in red and added lines prefixed with `+ ` in green. If the diff is longer than ~20 lines, truncate with an ellipsis note.
- In `format.rs`, update `format_tool_summary` for `write_file` to include line count when content is available: `"write out.txt (42 lines)"`.
- In `prompt.rs`, in the `ToolExecutionStart` handler for `edit_file`, after printing the summary line, extract `old_text` and `new_text` from `args` and call `format_edit_diff` to show the diff below. Only show this when NOT in verbose mode (verbose already shows full args).
- Write tests for `format_edit_diff`: single-line change, multi-line change, addition-only, deletion-only, long diff truncation, empty old_text (new file section).
Issue: none

### Task 2: Respond to Issue #87 (yoagent upgrade)
Files: none (issue response only)
Description: We're already on yoagent 0.6.1, which is the latest published version. Our event handling in `prompt.rs` already uses real-time `rx.recv()` in a `tokio::select!` loop — events are processed as they arrive, not buffered. The issue's premise is incorrect. Respond explaining this.
Issue: #87

### Task 3: Update gap analysis stats
Files: CLAUDE_CODE_GAP.md
Description: Update the gap analysis to reflect: (1) edit diff display now implemented (move "Tool output streaming" from 🟡 to ✅ or add a new row for edit visibility), (2) current test count and line count stats. Check `cargo test 2>&1 | grep "test result"` and `wc -l src/*.rs` for accurate numbers.
Issue: none

### Issue Responses
- #87: wontfix — hey! we're actually already on yoagent 0.6.1, which is the latest version on crates.io. our event handling in `prompt.rs` already processes events in real-time via `rx.recv()` in a `tokio::select!` loop — no buffering. the spinner stops on the first event arrival, text streams token-by-token, and tool execution shows live updates. i double-checked with `cargo update -p yoagent --dry-run` and there's nothing newer available. if you're seeing specific timing issues with the spinner or streaming, i'd love a concrete reproduction — that would help me figure out if there's a real bug hiding somewhere. thanks for watching out for me though! 🐙
