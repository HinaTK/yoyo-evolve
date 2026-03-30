Title: Minimal hook architecture for tool execution pipeline (Issue #21)
Files: src/main.rs
Issue: #21

## Goal

Add a minimal pre/post hook system for tool execution — the #1 strategic gap identified in the assessment. This is the foundation that separates "coding tool" from "coding agent" (hooks, automation, extensibility).

## What to build

### 1. Hook trait (~20 lines)

```rust
/// Hook that runs before/after tool execution.
pub trait Hook: Send + Sync {
    fn name(&self) -> &str;
    
    /// Pre-execute: return Err to block, Ok(None) to proceed, Ok(Some(result)) to short-circuit.
    fn pre_execute(&self, tool_name: &str, params: &serde_json::Value)
        -> Result<Option<String>, String> {
        Ok(None)
    }
    
    /// Post-execute: can inspect/log the result. Return modified output or pass through.
    fn post_execute(&self, tool_name: &str, params: &serde_json::Value, output: &str)
        -> Result<String, String> {
        Ok(output.to_string())
    }
}
```

### 2. HookRegistry (~30 lines)

```rust
pub struct HookRegistry {
    hooks: Vec<Box<dyn Hook>>,
}

impl HookRegistry {
    pub fn new() -> Self { Self { hooks: vec![] } }
    pub fn register(&mut self, hook: Box<dyn Hook>) { self.hooks.push(hook); }
    
    pub fn run_pre_hooks(&self, tool_name: &str, params: &serde_json::Value) 
        -> Result<Option<String>, String> { ... }
    
    pub fn run_post_hooks(&self, tool_name: &str, params: &serde_json::Value, output: &str)
        -> Result<String, String> { ... }
}
```

### 3. AuditHook — refactor existing audit logging (~30 lines)

Move the audit logging logic from the ad-hoc `audit_log_tool_call()` calls into a proper `AuditHook` that implements the `Hook` trait. The `post_execute` method logs to `.yoyo/audit.jsonl` — same format, same gating on `is_audit_enabled()`, but now it's a hook in the pipeline rather than scattered calls.

### 4. HookedTool wrapper (~50 lines)

A generic wrapper that wraps any `yoagent::Tool` and runs hooks before/after execution:

```rust
struct HookedTool<T: yoagent::Tool> {
    inner: T,
    hooks: Arc<HookRegistry>,
}
```

The `execute` method:
1. Calls `hooks.run_pre_hooks()` — if blocked, returns error; if short-circuited, returns cached result
2. Calls `inner.execute()` 
3. Calls `hooks.run_post_hooks()` on the result
4. Returns the (possibly modified) result

### 5. Wire into build_tools()

In `build_tools()`, if `--audit` is enabled (or hooks are configured), wrap each tool in `HookedTool`. The hook registry is shared (via `Arc`) across all wrapped tools.

Keep `StreamingBashTool` as-is (it already has its own wrapping logic for streaming + confirmation). The `HookedTool` wraps the StreamingBashTool, not the inner bash tool — hooks run at the outermost layer.

### 6. Tests

- Test that `HookRegistry::new()` starts empty
- Test that `run_pre_hooks` with no hooks returns `Ok(None)`  
- Test that `run_post_hooks` with no hooks passes through output unchanged
- Test that a blocking pre-hook returns Err
- Test that a short-circuiting pre-hook returns Ok(Some(...))
- Test that a post-hook can modify output
- Test that `AuditHook` implements the trait correctly
- Test that hook ordering is preserved (pre: first-to-last, post: first-to-last)

### What NOT to do

- Don't add config-file hook loading (that's a later task)
- Don't add CLI flags for hooks beyond `--audit` (which already exists)
- Don't modify `StreamingBashTool`'s confirmation logic
- Don't touch any files other than `main.rs`

### Verification

```bash
cargo build && cargo test && cargo clippy --all-targets -- -D warnings
```

The existing audit tests should still pass. The new hook tests should pass. The tool count in `build_tools` stays the same (tools are wrapped, not added).

### Docs

Update the help text for `--audit` to mention it uses the hook system. No CLAUDE.md or README changes needed yet — this is infrastructure, not a user-facing feature beyond what audit already provides.
