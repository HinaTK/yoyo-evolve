Title: Add session elapsed time and turn count to /status
Files: src/repl.rs, src/commands_info.rs
Issue: #278 (partial — addresses visibility into long-running sessions)

## Problem

When working on long tasks, users have no visibility into how long the session has been running or how many turns (prompt/response cycles) have occurred. The `/status` command currently shows model, git branch, cwd, and token counts — but not session duration or turn count.

Claude Code shows session duration and activity metrics. This is a simple but high-value UX improvement that helps users understand their session's progression, especially relevant to Issue #278 (long-working tasks).

## Implementation

### 1. Track session start time and turn count in `repl.rs`

Near the top of `run_repl` (after the existing `let mut session_total = Usage::default();`), add:
```rust
let session_start = std::time::Instant::now();
let mut turn_count: usize = 0;
```

Increment `turn_count` each time a prompt is sent to the agent. Find the spot where `session_total` is updated after each prompt cycle and add `turn_count += 1;` there.

### 2. Pass session_start and turn_count to handle_status

Update the `handle_status` call in `repl.rs` (around line 420):
```rust
// Before:
commands::handle_status(&agent_config.model, &cwd, &session_total);
// After:
commands::handle_status(&agent_config.model, &cwd, &session_total, session_start.elapsed(), turn_count);
```

### 3. Update handle_status in commands_info.rs

Change the signature:
```rust
pub fn handle_status(model: &str, cwd: &str, session_total: &Usage, elapsed: std::time::Duration, turns: usize) {
```

Add elapsed time and turn count to the output:
```rust
println!("{DIM}  model:   {model}");
if let Some(branch) = git_branch() {
    println!("  git:     {branch}");
}
println!("  cwd:     {cwd}");
println!("  session: {} elapsed, {} turns", format_duration(elapsed), turns);
println!(
    "  tokens:  {} in / {} out (session total){RESET}\n",
    session_total.input, session_total.output
);
```

Use `crate::format::cost::format_duration` which already exists in the codebase.

### 4. Add tests

In `commands_info.rs` tests:
```rust
#[test]
fn test_handle_status_with_timing() {
    use std::time::Duration;
    use yoagent::Usage;
    // Just verify it doesn't panic
    handle_status("test-model", "/tmp", &Usage::default(), Duration::from_secs(125), 7);
}
```

## Verification

1. `cargo build` — compiles clean
2. `cargo test` — all tests pass (new test + no regressions)
3. `cargo clippy --all-targets -- -D warnings` — no warnings
4. Manual check: the format_duration function already handles seconds/minutes/hours formatting

## Notes
- Keep it simple — just elapsed time and turn count
- Use existing `format_duration` from `format/cost.rs` — don't reinvent
- The turn count should count user prompts, not auto-retries or internal compaction calls
- If `format_duration` isn't directly importable, use the module path `crate::format::cost::format_duration`
