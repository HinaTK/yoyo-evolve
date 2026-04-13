Title: Add /changelog command to show recent git evolution history
Files: src/commands_info.rs, src/repl.rs, src/help.rs
Issue: #226

## What to do

Add a `/changelog` REPL command that shows a formatted summary of recent git commits — 
giving users (and the agent itself) quick access to evolution history without leaving the REPL.

This addresses Issue #226's spirit: making evolution history accessible and useful.

### Implementation

**In `src/commands_info.rs`:**

Add a `pub fn handle_changelog(input: &str)` function:
- Parse optional count from input: `/changelog` shows last 15, `/changelog 30` shows last 30
- Clamp count to 1..=100
- Run `git log --oneline --format="%h %s (%ar)" -N` where N is the count
- If no git repo, print "(not in a git repository)"
- Format output with DIM coloring, group by date if possible (just use the relative time from git)
- Show the output with `println!`

**In `src/repl.rs`:**

Wire `/changelog` to call `commands::handle_changelog(input)` in the command dispatch match.

**In `src/help.rs`:**

Add help text for `/changelog`:
- Short description: "Show recent git commit history"
- Detailed: "Usage: /changelog [count]\n\nShow the last N commits (default: 15, max: 100).\nUseful for reviewing recent changes and evolution history."

Add "changelog" to `help_command_completions`.

### Tests

In `src/commands_info.rs`, add tests:
- `test_handle_changelog_default` — verify it doesn't panic (can't easily test git output in unit tests, but can verify the function exists and runs)
- Test the count parsing logic if extracted into a helper

### Verification

```
cargo build && cargo test && cargo clippy --all-targets -- -D warnings
```
