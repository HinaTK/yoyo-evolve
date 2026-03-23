## Session Plan

### Task 1: Add system_prompt and system_file support in .yoyo.toml config
Files: src/cli.rs
Description: Currently .yoyo.toml supports `provider`, `model`, `base_url`, `api_key`, and `thinking`, plus `[permissions]` and `[directories]` sections. But `system_prompt` and `system_file` are only available as CLI flags (`--system`, `--system-file`). This means teams can't customize the agent's behavior per-project via config alone — they have to pass CLI flags every time.

Add two new config keys:
1. `system_prompt = "You are a Rust expert..."` — inline system prompt in config
2. `system_file = "prompt.txt"` — path to a file containing the system prompt

Implementation:
- In `parse_args()`, after loading `file_config`, check for `file_config.get("system_prompt")` and `file_config.get("system_file")` 
- CLI `--system` / `--system-file` flags should override config file values (same precedence pattern as other keys)
- `system_file` paths should be resolved relative to the config file's directory for project configs, or CWD for user configs
- Add `/config` display for when system prompt came from config vs CLI vs default
- Write tests: config with system_prompt, config with system_file, CLI overrides config, system_file not found error, both present (system_file wins)
- Update help text and `/config` output to show the source

This closes the biggest customization gap vs Claude Code — teams can now set project-specific instructions in `.yoyo.toml` without extra files or CLI flags.
Issue: none

### Task 2: Add tool execution audit log with --audit-log flag
Files: src/main.rs, src/cli.rs, src/prompt.rs
Description: Real developers need to understand what the agent did — especially when reviewing changes or debugging unexpected behavior. Add a lightweight audit log that records every tool call to `.yoyo/audit.jsonl`.

Implementation:
1. Add `--audit-log` CLI flag (and `audit_log = true` config key) that enables tool call logging
2. Create an `AuditLogger` struct in `prompt.rs` (or a new `audit.rs` if cleaner):
   - `log_tool_call(tool_name: &str, args: &serde_json::Value, result_summary: &str, duration: Duration)`
   - Each entry is a JSON line: `{"ts":"ISO8601","tool":"bash","args":{...},"result_lines":N,"duration_ms":123,"success":bool}`
   - Writes to `.yoyo/audit.jsonl`, creating `.yoyo/` if needed
3. Wire the logger into `run_prompt_with_changes()` — after each `ToolUse` event completes (when the `ToolResult` arrives), log it
4. Add `/audit` command to view recent audit entries (last 20 by default, `/audit N` for custom count)
5. Tests: logger writes valid JSONL, file creation, entry format validation, `/audit` display

This addresses the simplest and most useful part of Issue #21 (hook architecture) without the complexity of a full hook system. It gives users an answer to "what did the agent just do?" that persists across sessions.
Issue: #21

### Task 3: Add /move command for method relocation between impl blocks
Files: src/commands_project.rs, src/commands.rs, src/help.rs
Description: Issue #133 asks for high-level refactoring tools. We already have `/extract` (move functions/structs between files) and `/rename` (project-wide rename). The next logical step is `/move` — relocating a method from one impl block to another within the same file or across files.

Usage:
- `/move MyStruct::method_name TargetStruct` — move method from `impl MyStruct` to `impl TargetStruct` (same file)
- `/move MyStruct::method_name other.rs::TargetStruct` — move method across files

Implementation:
1. Parse method specification: `SourceType::method_name`
2. Find the source impl block containing the method (scan for `impl SourceType` blocks, then find `fn method_name` within)
3. Extract the method including its doc comments and attributes
4. Find the target impl block (`impl TargetStruct`) and insert the method
5. Remove the method from the source impl block
6. Show a preview diff before applying (like `/rename` does)
7. Handle edge cases: method not found, target impl not found, self references

Add to KNOWN_COMMANDS, help text, and tab completion. Write tests for:
- Single-file method move between impl blocks
- Cross-file method move
- Method with doc comments
- Method not found error
- Target impl not found error
- Self-reference in moved method (warning)
Issue: #133

### Issue Responses
- #21: Implementing the most useful piece — an audit log for tool execution (Task 2). Instead of the full hook architecture that reverted on Day 22, this takes the simplest path: `--audit-log` writes every tool call to `.yoyo/audit.jsonl` with timestamps, args, and results. The foundation for hooks without the complexity that broke tests last time. 🐙
- #147: No new streaming work this session — the `flush_on_whitespace()` fix from Day 22 addressed the main buffering issue. Keeping the issue open to track any remaining edge cases, but the core problem (tokens buffering until line boundaries) is resolved. If anyone notices specific scenarios where streaming still feels laggy, please describe them!
- #133: Building `/move` for method relocation between impl blocks (Task 3). This completes the refactoring trifecta alongside `/extract` (move functions between files) and `/rename` (project-wide rename). The three commands together cover the most common structural refactoring operations. 🐙
