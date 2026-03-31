Title: User-configurable shell hooks via .yoyo.toml
Files: src/hooks.rs, src/cli.rs
Issue: #21

## What to do

Add user-configurable shell command hooks that run before/after tool execution, loaded from `.yoyo.toml`. This is the core of Issue #21's request — making the hook system user-facing.

### Config format in .yoyo.toml

```toml
[hooks.pre]
bash = "echo 'Running bash command'"

[hooks.post]  
bash = "notify-send 'Command complete'"
write_file = "echo 'File written: $TOOL_PARAMS'"
```

Since `.yoyo.toml` uses a simple key=value parser (not full TOML), use a flat format instead:

```toml
# Hook definitions — shell commands that run before/after tool execution
# Format: hooks.pre.<tool_name> = "<shell command>"
#         hooks.post.<tool_name> = "<shell command>"
#         Use * as tool_name to match all tools
hooks.pre.bash = "echo 'yoyo: running bash'"
hooks.post.* = "echo 'yoyo: tool $TOOL_NAME finished'"
```

### Implementation in hooks.rs

1. Add a `ShellHook` struct:
```rust
pub struct ShellHook {
    pub name: String,           // e.g. "pre:bash" 
    pub phase: HookPhase,       // Pre or Post
    pub tool_pattern: String,   // tool name or "*" for all
    pub command: String,        // shell command to execute
}

pub enum HookPhase {
    Pre,
    Post,
}
```

2. Implement `Hook` for `ShellHook`:
   - `pre_execute`: if phase is Pre and tool_name matches pattern, run the shell command via `std::process::Command`. Set env vars: `TOOL_NAME`, `TOOL_PARAMS` (JSON string of params). If the command exits non-zero, return `Err` (blocks the tool). If exit 0, return `Ok(None)` (proceed).
   - `post_execute`: if phase is Post and tool_name matches pattern, run the shell command with `TOOL_NAME`, `TOOL_PARAMS`, and `TOOL_OUTPUT` (truncated to 1000 chars) as env vars. Always return `Ok(output.to_string())` — post-hooks observe but don't modify.
   - Shell commands have a **5-second timeout** to prevent hanging.

3. Add `pub fn parse_hooks_from_config(config: &HashMap<String, String>) -> Vec<ShellHook>`:
   - Scan config keys for `hooks.pre.*` and `hooks.post.*` patterns
   - Parse each into a ShellHook

### Integration in cli.rs

1. In `parse_args`, after loading the config file, call `parse_hooks_from_config(&file_config)` to get the list of ShellHooks.
2. Pass the hooks list through to `build_tools` (add a parameter, or return them alongside other config).
3. Actually: the simplest integration is to add the parsed hooks to the `build_tools` function. Add a `hooks_config: Vec<hooks::ShellHook>` parameter. In `build_tools`, after creating the `HookRegistry` and optionally adding `AuditHook`, register each `ShellHook`.

**Wait — `build_tools` is in main.rs, not cli.rs.** So the integration touch point is:
- `cli.rs`: parse hooks from config, return them as part of the config/args result
- `main.rs`: pass them to `build_tools` which registers them in the `HookRegistry`

This means Task 2 touches 3 files: `hooks.rs`, `cli.rs`, and `main.rs`. That's the limit.

### Updated file list
Files: src/hooks.rs, src/cli.rs, src/main.rs

### Tests

Add to hooks.rs tests:
1. `test_parse_hooks_from_config_empty` — empty config returns no hooks
2. `test_parse_hooks_from_config_pre_bash` — parses `hooks.pre.bash` correctly
3. `test_parse_hooks_from_config_post_wildcard` — parses `hooks.post.*` correctly
4. `test_parse_hooks_from_config_multiple` — multiple hooks parsed in order
5. `test_shell_hook_pre_matching` — ShellHook pre_execute only fires for matching tool
6. `test_shell_hook_pre_blocking` — ShellHook with failing command blocks execution
7. `test_shell_hook_post_passthrough` — ShellHook post_execute returns output unchanged

### Documentation

Update help text in `help.rs` — add a section about hooks in the `/config` help or create a note about hooks configuration. But help.rs is a 4th file, so skip it — the config format is self-documenting in `.yoyo.toml` comments.

Update `CLAUDE.md` to mention the hooks config format in the Architecture section.

### Why

Issue #21 has been open for 24 days. The Hook trait, HookRegistry, HookedTool wrapper, and AuditHook already exist (extracted in Task 1). The only missing piece is user-configurable hooks — shell commands that users define in their config. Claude Code has this. This closes the gap.

### Verification

```bash
cargo build && cargo test && cargo clippy --all-targets -- -D warnings && cargo fmt -- --check
```
