Title: Wire yoagent's built-in context management and handle missing agent events
Files: src/main.rs, src/prompt.rs, src/cli.rs
Issue: #183

## Context

This is a retry of the previously reverted Task 1 from Day 25 (Issue #184). The previous attempt failed because it tried to do too much — removing manual compaction functions and all callers simultaneously. This time: **only add what's needed, don't remove anything**.

yoyo's `configure_agent()` never calls `with_context_config()`, so yoagent's built-in compaction (which runs automatically before each LLM turn) doesn't know the context budget. We also don't wire `max_total_tokens` in `ExecutionLimits`, so there's no clean budget-based stopping.

Additionally, `MessageStart` and `MessageEnd` events from yoagent are silently dropped in `handle_prompt_events()` (src/prompt.rs). This means agent stop messages (e.g., from ExecutionLimits or when the agent is aborted) are invisible to the user.

## Implementation

### 1. Wire `ContextConfig` in `configure_agent()` (src/main.rs)

In the `configure_agent()` method, add context config wiring. Add the import at the top of main.rs:
```rust
use yoagent::context::ContextConfig;
```

Then in `configure_agent()`, after the existing `with_tools()` call and before the `if let Some(max)` block, add:
```rust
// Tell yoagent the context window size so its built-in compaction knows the budget
agent = agent.with_context_config(ContextConfig {
    max_context_tokens: 200_000,
    system_prompt_tokens: 4_000,
    keep_recent: 10,
    keep_first: 2,
    tool_output_max_lines: 50,
});
```

Also update the `ExecutionLimits` block. Currently it only sets `max_turns` when the user passes `--max-turns`. Change the block so it always sets limits:
```rust
agent = agent.with_execution_limits(ExecutionLimits {
    max_turns: self.max_turns.unwrap_or(200),
    max_total_tokens: 1_000_000,
    ..ExecutionLimits::default()
});
```

Remove the `if let Some(turns)` guard — always set limits.

### 2. Handle `MessageStart` and `MessageEnd` events (src/prompt.rs)

In the `handle_prompt_events()` function's event match block, add handlers for the two missing events. Add these cases before or after the existing `AgentEvent::AgentEnd` case:

```rust
AgentEvent::MessageStart { message } => {
    // Agent started a new message — nothing to render yet, but
    // stop the spinner so it doesn't overlap with output
    if let Some(ref s) = spinner {
        s.stop();
        spinner = None;
    }
}
AgentEvent::MessageEnd { message } => {
    // Agent finished a message — check for stop reason info
    // (This is where ExecutionLimits stop messages appear)
    // For now, just ensure any pending text is flushed
    if in_text {
        md_renderer.end_streaming();
        println!();
        in_text = false;
    }
}
```

### 3. DO NOT remove any existing code

The manual compaction functions (`auto_compact_if_needed`, `proactive_compact_if_needed`, `compact_agent`) stay exactly as they are. The existing callers stay. This task ONLY adds the `with_context_config()` and `with_execution_limits()` calls and the event handlers.

The manual compaction functions serve as a safety net alongside yoagent's built-in compaction. A future task can remove them once we've verified the built-in compaction works well.

### 4. Tests

Add these tests to the existing test module in `src/main.rs`:

- `test_configure_agent_sets_context_config` — verify that `configure_agent` produces an agent (can't easily check the config, but we can verify the agent builds successfully with it)
- `test_execution_limits_always_set` — verify that even without `--max-turns`, `configure_agent` sets execution limits

### 5. Verify

Run `cargo build && cargo test && cargo clippy --all-targets -- -D warnings` to ensure everything compiles and passes.
