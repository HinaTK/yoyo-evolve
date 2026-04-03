Title: Extract tool definitions from main.rs into src/tools.rs
Files: src/main.rs, src/tools.rs (new)
Issue: none

## What

Extract all tool-related structs and implementations from main.rs (lines ~89-955) into a new `src/tools.rs` module. This is the biggest structural debt item — main.rs is 3,645 lines and the tool definitions alone are ~870 lines.

## Why

main.rs is the largest file in the codebase at 3,645 lines. Every edit to main.rs requires reading/navigating this massive file. The tool definitions (GuardedTool, TruncatingTool, ConfirmTool, StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool, and their helper functions) are self-contained and have no reason to live in main.rs. Extracting them makes the codebase easier to navigate and every future evolution faster.

## Exactly what to move

Move these items from main.rs to a new src/tools.rs:
- `struct GuardedTool` and `impl AgentTool for GuardedTool`
- `struct TruncatingTool`, `fn truncate_result`, `impl AgentTool for TruncatingTool`, `fn with_truncation`
- `fn maybe_guard`
- `struct ConfirmTool`, `impl AgentTool for ConfirmTool`, `fn maybe_confirm`
- `pub fn describe_file_operation`, `pub fn confirm_file_operation`
- `pub struct StreamingBashTool`, `impl Default for StreamingBashTool`, `impl StreamingBashTool`, `fn emit_update`, `impl AgentTool for StreamingBashTool`
- `struct RenameSymbolTool`, `impl AgentTool for RenameSymbolTool`
- `pub struct AskUserTool`, `impl AgentTool for AskUserTool`
- `pub struct TodoTool`, `impl AgentTool for TodoTool`
- `pub fn build_tools` (the function that assembles the tool list)
- `fn build_sub_agent_tool`
- `fn with_confirm` (the closure wrapper)

## In main.rs after extraction

- Add `mod tools;` declaration
- Add `use tools::build_tools;` (and any other pub items needed by main.rs)
- Keep `AgentConfig`, `build_agent`, `create_model_config`, and `main()` in main.rs
- Keep `fn yoyo_user_agent()` and `fn insert_client_headers()` in main.rs (they're used by create_model_config/build_agent)

## Visibility rules

- Items called from main.rs need `pub` or `pub(crate)` visibility in tools.rs
- Items only used within tools.rs stay private
- `build_tools` needs to be `pub` since it's called from main.rs
- `describe_file_operation` and `confirm_file_operation` are already `pub` — keep them pub in tools.rs
- `StreamingBashTool`, `AskUserTool`, `TodoTool` are already `pub` — keep them pub in tools.rs

## Verification

- `cargo build` must pass
- `cargo test` must pass (all 1,615 tests)
- `cargo clippy --all-targets -- -D warnings` must pass
- No functional changes — pure refactor, move only

## What NOT to do

- Don't change any logic or behavior
- Don't rename anything
- Don't modify any other files beyond main.rs and tools.rs
- Don't forget to move the relevant `use` imports to tools.rs
- Don't forget `#[cfg(test)] mod tests` sections that test tool-related functions (move those too)

## Doc updates

Update CLAUDE.md's Repository Structure section to add `src/tools.rs` with its line count and purpose. Update main.rs description to note tools were extracted.
