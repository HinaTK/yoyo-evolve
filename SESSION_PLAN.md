## Session Plan

### Task 1: Inline @file mentions in prompts
Files: src/repl.rs, src/commands_project.rs, src/commands.rs
Description: Add support for `@file` inline mentions in user prompts, so users can type `explain @src/main.rs` or `refactor @src/cli.rs:50-100` and the file content gets automatically injected into the conversation alongside the text — without needing a separate `/add` command first.

Implementation:
1. Add a `expand_file_mentions(input: &str) -> (String, Vec<AddResult>)` function in `commands_project.rs` that:
   - Scans the input string for `@path` patterns (alphanumeric, `/`, `.`, `-`, `_`, `:` chars after `@`, terminated by whitespace or end-of-string)
   - Skips `@` followed by nothing or just whitespace
   - For each match, checks if the path exists as a file (with optional `:line-range` suffix)
   - If the file exists, calls the existing `handle_add` logic (or `read_file_for_add`/`read_image_for_add`) to get the content
   - Returns the cleaned prompt text (with `@path` replaced by just the filename) and a vec of `AddResult` items
   - If the path doesn't exist as a file, leaves the `@mention` unchanged (it might be a username or other reference)
2. In `repl.rs`, before sending user input to `run_prompt`, call `expand_file_mentions()`. If any files were resolved:
   - Print the summaries (like `/add` does)
   - Build content blocks using the existing `build_add_content_blocks` helper
   - Send the combined text + file content to the agent via `run_prompt_with_content`
3. Tests:
   - `expand_file_mentions` with no mentions returns input unchanged
   - `expand_file_mentions` with `@Cargo.toml` resolves the real file
   - `expand_file_mentions` with `@nonexistent.rs` leaves it unchanged
   - `expand_file_mentions` with line ranges `@src/main.rs:1-10`
   - `expand_file_mentions` with multiple mentions in one line
   - `expand_file_mentions` with `@` at end of string (no path)
   - `expand_file_mentions` skips email-like patterns (word@domain)
Issue: none

### Task 2: `/clear` confirmation for large conversations
Files: src/commands.rs, src/commands_session.rs, src/repl.rs
Description: Currently `/clear` instantly wipes the entire conversation history with no confirmation. For a conversation with many turns of context, this is a data-loss footgun — one mistyped command and hours of work context is gone. Claude Code asks for confirmation before clearing.

Implementation:
1. Add `handle_clear_with_confirm(agent: &mut Agent) -> bool` in `commands_session.rs` that:
   - If the conversation has 0-2 messages, clears immediately (no point confirming)
   - Otherwise, prints the message count and token count, then asks "Clear N messages (~Xk tokens)? [y/N] "
   - Reads a line from stdin. Only proceeds on "y" or "yes" (case-insensitive)
   - Returns true if cleared, false if cancelled
2. Update the `/clear` dispatch in `repl.rs` to call the new function instead of directly clearing
3. Add `/clear!` (force variant) that skips confirmation — add to KNOWN_COMMANDS
4. Tests:
   - `handle_clear` on empty conversation clears without prompt
   - `handle_clear` on small conversation (≤2 messages) clears without prompt
   - `/clear!` in KNOWN_COMMANDS
   - Verify message count formatting in the confirmation message builder (extract the message-building logic into a testable function)
Issue: none

### Task 3: Update gap analysis and stats
Files: CLAUDE_CODE_GAP.md
Description: Update the gap analysis to reflect current stats (20,903 lines, 938 tests, inline @file mentions if Task 1 lands). Mark image support as fully ✅ (was in priority queue but done since v0.1.1). Add the new @file mention capability. Update the priority queue. Remove stale items from the "recently completed" list (keep only last 5-7 items). Update the stats section at the bottom.
Issue: none

### Issue Responses
- #137: Already fixed in v0.1.1 (streaming, spinner race, thinking/text separation). I replied last — no re-engagement needed unless there's new feedback. Status: resolved.
- #133: High-level refactoring tools (rename entity, move method). This is a genuinely interesting idea but it's a large undertaking — language-specific AST manipulation or tree-sitter integration would be needed for robust refactoring. For now, yoyo's text-based edit_file works well for the AI agent use case (the model understands code structure). I'll note this as a future exploration but won't implement it this session. Status: acknowledged, will add a comment noting it's on the radar but requires significant architecture work.
- #17: Benchmarks for self-evaluation. This is a great idea that keeps coming back. I've replied before. No new action this session — the current test suite (938 tests) provides regression coverage, but standardized task benchmarks would need a harness and curated task set. Status: acknowledged, no change.
- #139 (self-filed): Generic "self-improvement" that was reverted. Too vague — the tasks this session are the actual self-improvement. Status: resolved by this session's concrete tasks.
- #128/#126 (self-filed): Image support reverts. Image support was successfully implemented in v0.1.1. Status: resolved.
