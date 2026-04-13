Title: Improve tool progress display with command name and elapsed formatting
Files: src/format/tools.rs, src/prompt.rs
Issue: none

## What to do

Currently, the tool progress timer shows `⠋ bash (3s, 42 lines)` during command execution.
Improve this to also show the actual command being run (truncated), making it much easier
for users to understand what the agent is doing at a glance.

This closes competitive ground on Claude Code's tool output display, which shows the 
command being executed.

### Implementation

**In `src/format/tools.rs`:**

1. Add a `set_label(&self, label: String)` method to `ToolProgressTimer` that updates an
   internal `Arc<Mutex<Option<String>>>` field (similar to how `set_line_count` works with
   `Arc<AtomicUsize>`).

2. Update `format_tool_progress` to include the label if set:
   - Without label: `⠋ bash (3s, 42 lines)` (current)
   - With label: `⠋ bash: ls -la src/ (3s, 42 lines)`
   
3. Truncate the label to ~40 chars using `safe_truncate` to prevent long commands from 
   wrapping the terminal.

**In `src/prompt.rs`:**

In the `ToolExecutionStart` event handler for bash tools, extract the command from the
tool input parameters and pass it to the timer via `set_label()`:
- Look at `tool_input` for the "command" key
- If present, extract it as a string, truncate to ~50 chars, set as label
- Only do this for bash tool calls (not other tools)

### Tests

In `src/format/tools.rs`:
- `test_format_tool_progress_with_label` — verify the label appears in output
- `test_format_tool_progress_label_truncation` — verify long labels get truncated

### Verification

```
cargo build && cargo test && cargo clippy --all-targets -- -D warnings
```
