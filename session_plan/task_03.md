Title: Add tool execution retry helper and better error context for failed bash commands
Files: src/prompt.rs, src/format.rs
Issue: none

## Context

When a bash command fails (non-zero exit code), the raw error output gets sent back to the LLM, but there's no structured help. Claude Code is better at this — when a tool fails, it provides clear context about what went wrong and suggests fixes. The LLM already does some of this naturally, but we can improve the signal-to-noise ratio by enriching the error context.

## Implementation

1. **In `src/format.rs`**: Add a `format_tool_error_context()` function that takes a tool name, the arguments, and the error output, and returns enriched context:
   - For bash errors: detect common patterns like "command not found" (suggest installation), "permission denied" (suggest chmod/sudo), "No such file or directory" (suggest checking path), "ECONNREFUSED" (suggest checking if service is running)
   - For file tool errors: detect "file not found" and suggest `/find` or `/tree`
   - The function returns `Option<String>` — None if no useful context can be added
   - These hints are appended to the tool result text that gets sent back to the LLM, prefixed with `[hint: ...]` so the model knows this is supplementary context, not the actual error

2. **In `src/prompt.rs`**: After receiving a ToolResult, if the result indicates failure (`details["success"] == false` for bash, or error text patterns), call `format_tool_error_context()` and append any hints to the result text before it's sent back to the agent.

3. **Also in `src/format.rs`**: Add a `format_error_summary()` function that produces a user-visible one-line summary for failed tool calls. Currently failed bash commands show the full stderr; add a concise `✗ command failed (exit 1): first line of stderr` summary.

4. **Tests** (at least 6):
   - `test_error_context_command_not_found`: "foo: command not found" → suggests installation
   - `test_error_context_permission_denied`: "Permission denied" → suggests chmod
   - `test_error_context_no_such_file`: "No such file or directory" → suggests /find
   - `test_error_context_connection_refused`: "ECONNREFUSED" → suggests service check
   - `test_error_context_no_match`: generic error → returns None
   - `test_error_summary_format`: produces concise one-liner from multi-line stderr

This makes the agent smarter about error recovery without requiring changes to the LLM itself — just better information in the feedback loop.
