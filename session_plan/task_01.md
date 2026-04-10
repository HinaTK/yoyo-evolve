Title: Fix /undo causal consistency — inject undo context into next agent turn
Files: src/commands_git.rs, src/repl.rs
Issue: #279

## Problem

When a user runs `/undo`, the turn's file changes are reverted (via TurnSnapshot::restore), but the agent's conversation history still contains messages referencing the now-reverted code. The agent doesn't know that files were rolled back, so it may continue referencing code that no longer exists. This is a semantic integrity issue reported in Issue #279.

## Solution

Make `handle_undo` return a structured summary of what was undone (files restored, files deleted) as an `Option<String>`. The REPL loop already dispatches `/undo` — after the call, if a summary is returned, store it as "pending context" that gets prepended to the user's NEXT prompt as a system-injected note.

### Concrete steps:

1. **In `commands_git.rs`**: Change `handle_undo` signature from `fn handle_undo(input: &str, history: &mut TurnHistory)` to `fn handle_undo(input: &str, history: &mut TurnHistory) -> Option<String>`. The returned string should be a compact markdown note like:
   ```
   [System note: /undo reverted the following changes from the last turn:
   - restored src/foo.rs (to pre-turn state)  
   - deleted src/bar.rs (was created during the turn)
   The code referenced in my previous response may no longer exist. Please verify current file state before continuing.]
   ```
   Similarly update `handle_undo_all` to return `Option<String>`.

2. **In `repl.rs`**: In the REPL loop where `/undo` is dispatched, capture the return value. If `Some(context)`, store it in a variable (e.g., `undo_context: Option<String>`). When the next user prompt is being built, prepend this context to the user's message so the agent is aware of what changed. Clear the variable after use.

   Look for where `/undo` is dispatched in the REPL (likely a match arm). The pattern is:
   - Call handle_undo, get Option<String>
   - Store in a mutable variable accessible to the prompt-building code
   - When building the next prompt, if undo_context.is_some(), prepend it

3. **Tests**: Add a test in `commands_git.rs` that verifies `handle_undo` returns a non-None summary when there are turns to undo. Add a test that verifies the summary mentions the restored file paths.

## What NOT to do

- Don't modify the journal system — the journal is append-only by rule
- Don't try to remove messages from the agent's conversation history — that's complex and fragile
- Don't touch prompt.rs — keep changes to commands_git.rs and repl.rs only
