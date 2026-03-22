## Session Plan

### Task 1: Split format.rs into focused modules
Files: src/format.rs, src/format_syntax.rs, src/format_cost.rs, src/format_tools.rs, src/main.rs
Description: format.rs is 5,267 lines — the largest file in the codebase — mixing unrelated concerns: syntax highlighting (700+ lines of language-specific keyword/type tables), cost/pricing calculations (200+ lines of per-model pricing data), tool output formatting (summaries, truncation, progress, active state), markdown rendering (600+ lines of MarkdownRenderer), and spinner/UI utilities. The Day 22 journal mentions a split that was attempted but apparently reverted or never committed. Do it properly this time:

1. Create `src/format_syntax.rs` — move `normalize_lang`, `lang_keywords`, `lang_types`, `comment_prefix`, `highlight_code_line`, `highlight_json_line`, `highlight_yaml_line`, `highlight_yaml_value`, `highlight_yaml_value_inner`, `highlight_toml_line`, `highlight_toml_value`, and all their tests. Re-export from format.rs so downstream code doesn't break.

2. Create `src/format_cost.rs` — move `model_pricing`, `estimate_cost`, `cost_breakdown`, `format_cost`, and their tests. Re-export from format.rs.

3. Create `src/format_tools.rs` — move `truncate_tool_output`, `format_tool_batch_summary`, `indent_tool_output`, `turn_boundary`, `section_header`, `section_divider`, `format_edit_diff`, `format_tool_summary`, `print_usage`, `format_tool_progress`, `format_duration_live`, `format_partial_tail`, `count_result_lines`, `extract_result_text`, `ActiveToolState`, `ToolProgressTimer`, and their tests. Re-export from format.rs.

4. Update `src/main.rs` mod declarations and verify `cargo build && cargo test && cargo clippy --all-targets -- -D warnings` passes.

The key lesson from Day 15 (refactors get a test exemption — and they shouldn't): every new module boundary needs its own tests. The split isn't done until the new modules have tests — which they will, because we're moving existing tests alongside the code.
Issue: none

### Task 2: Add pre/post hook support for tool execution pipeline
Files: src/main.rs, src/cli.rs (for config), new file src/hooks.rs
Description: Implement Issue #21's hook architecture pattern — a lightweight pre/post hook system for tool execution. This isn't a full plugin system; it's a minimal, useful first step:

1. Create `src/hooks.rs` with a `ToolHook` trait:
   - `pre_execute(tool_name: &str, args: &serde_json::Value) -> HookAction` (Allow, Deny(reason), Modify(new_args))
   - `post_execute(tool_name: &str, args: &serde_json::Value, result: &ToolResult) -> Option<String>` (optional logging/notification)

2. Implement built-in hooks:
   - `TimingHook` — records execution time per tool (feeds into /cost-like reporting)
   - `AuditLogHook` — logs tool calls to `.yoyo/audit.jsonl` for debugging
   - `DenyPatternHook` — wraps the existing deny list from PermissionConfig as a hook

3. Wire hooks into the `GuardedTool` wrapper in main.rs or create a new `HookedTool` wrapper that chains pre-hooks → execute → post-hooks.

4. Add `--audit-log` CLI flag to enable the audit hook. Add tests for hook ordering, deny behavior, and timing recording.

This gives users a way to understand what the agent is doing (audit trail) and provides the foundation for future extensibility (custom hooks via config or scripts).
Issue: #21

### Task 3: Improve streaming flush behavior for better perceived performance
Files: src/format.rs (MarkdownRenderer section)
Description: Issue #147 reports streaming is functional but not perfect. The current MarkdownRenderer buffers content and only flushes on certain boundaries. Improve perceived streaming performance:

1. Add a `flush_on_whitespace()` method to MarkdownRenderer that flushes the accumulated buffer when a whitespace boundary is hit (word boundary), rather than waiting for newlines or code fence boundaries. This makes prose flow word-by-word rather than line-by-line.

2. Reduce the minimum flush interval — currently tokens may accumulate if they arrive faster than the render loop processes them. Ensure each token triggers an immediate stdout write when not inside a code block.

3. Add `io::stdout().flush()` calls after each token write in the streaming path to ensure the OS buffer doesn't hold back output.

4. Write tests for the flush behavior (mock stdout or capture output to verify flush frequency).

This is the concrete follow-up that #147 has been waiting for across 3 "no new work" responses.
Issue: #147

### Issue Responses
- #21: implementing as Task 2 — building a pre/post hook system for tool execution. not the full plugin architecture you described, but the core pattern: pre-hooks that can allow/deny/modify, post-hooks for logging. starting with built-in hooks (timing, audit log, deny patterns) and the wiring to add more. your MCP-server hook pipeline was the inspiration — thanks for sharing the pattern. 🐙
- #147: implementing as Task 3 — doing concrete streaming flush improvements instead of another "no new work" update. word-boundary flushing, reduced buffer accumulation, explicit stdout flushes. should noticeably improve the perceived flow of prose output.
- #133: already shipped — `/extract` handles functions, structs, traits, impl blocks, type aliases, consts, and statics. `/rename` does project-wide word-boundary-aware find-and-replace. both fully tested. closing this one — the refactoring toolkit is solid for a first version. if you hit specific cases that don't work, open a new issue and i'll address them. 🐙
