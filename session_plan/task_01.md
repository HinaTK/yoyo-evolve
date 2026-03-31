Title: Extract hook system from main.rs into src/hooks.rs
Files: src/main.rs, src/hooks.rs
Issue: #21 (partial — infrastructure step)

## What to do

Extract the entire hook system (~230 lines of implementation + ~280 lines of tests) from `main.rs` into a new `src/hooks.rs` module. This is a pure mechanical extraction — no behavior changes.

### Code to extract (from main.rs)

**Implementation (lines ~379-605):**
- The comment block "// Hook system — pre/post tool execution pipeline"
- `pub trait Hook: Send + Sync` 
- `pub struct HookRegistry` with all impls (new, register, run_pre_hooks, run_post_hooks, len, is_empty)
- `pub struct AuditHook` and its `impl Hook`
- `struct HookedTool` and its `impl AgentTool`
- `fn maybe_hook()`

**Tests (lines ~3390-3665):**
- All `test_hook_*` tests
- Test helper structs: `BlockingHook`, `CachingHook`, `UppercaseHook`, etc.
- The `test_maybe_hook_*` and `test_build_tools_with_audit_*` tests should stay in main.rs since they test `build_tools()` — only move the pure hook tests.

### Steps

1. Create `src/hooks.rs` with the extracted code
2. Add `pub mod hooks;` to the module declarations in `main.rs`
3. In `hooks.rs`, add necessary imports: `use serde_json`, `use std::sync::Arc`, `use yoagent::types::{AgentTool, ToolContext, ToolResult, ToolError}`, `use async_trait::async_trait`, and `use crate::prompt::is_audit_enabled` and `use crate::prompt::audit_log_tool_call`
4. In `main.rs`, replace the extracted code with `use hooks::{Hook, HookRegistry, AuditHook, maybe_hook};`
5. Keep `build_tools`-related tests in `main.rs` (they depend on `build_tools` which stays in main)
6. Move pure hook tests to `hooks.rs` in a `#[cfg(test)] mod tests` block

### Verification

```bash
cargo build && cargo test && cargo clippy --all-targets -- -D warnings && cargo fmt -- --check
```

All existing tests must pass unchanged. The hook tests should now run from `hooks.rs`.

### Why

main.rs is 3,665 lines — the second largest file. The hook system is a self-contained subsystem with its own trait, registry, wrapper, and tests. Extracting it reduces main.rs by ~500 lines and makes the hook system independently navigable, which is necessary for Task 2 (adding user-configurable shell hooks).
