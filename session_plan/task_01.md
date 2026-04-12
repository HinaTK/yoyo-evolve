Title: Add session elapsed time and turn count to /status
Files: src/repl.rs, src/commands_info.rs
Issue: #284

## Problem

The `/status` command shows model, git branch, cwd, and token counts — but not session duration or turn count. This was attempted on Day 42 but reverted due to a test failure (`build_repo_map_with_regex_backend`). That test failure was caused by a `set_current_dir` race condition that was **fixed in Day 42's Task 1**. The blocking issue is gone.

## Implementation (smaller scope than last attempt)

### 1. Add session tracking variables in repl.rs

Near line 361, right after `let mut session_total = Usage::default();`, add:

```rust
let session_start = std::time::Instant::now();
let mut turn_count: usize = 0;
```

### 2. Increment turn_count on each user prompt

Find the spot where `run_prompt_auto_retry` and `run_prompt_auto_retry_with_content` are called in the main REPL loop (around lines 940-960). Right before calling the prompt function, add `turn_count += 1;`. There are two call sites:
- The `@file` expansion path (around line 945, `run_prompt_auto_retry_with_content`)
- The normal prompt path (around line 955, `run_prompt_auto_retry`)

Only increment for user-initiated prompts, NOT for internal operations like compaction, auto-retry, or /fix.

### 3. Update handle_status signature and call site

In `src/repl.rs`, change the `/status` handler (around line 420):
```rust
// Before:
commands::handle_status(&agent_config.model, &cwd, &session_total);
// After:
commands::handle_status(&agent_config.model, &cwd, &session_total, session_start.elapsed(), turn_count);
```

In `src/commands_info.rs`, update the function signature:
```rust
pub fn handle_status(model: &str, cwd: &str, session_total: &Usage, elapsed: std::time::Duration, turns: usize) {
```

Add the session line between cwd and tokens:
```rust
println!("  cwd:     {cwd}");
println!("  session: {} elapsed, {turns} turn{}", format_duration(elapsed), if turns == 1 { "" } else { "s" });
```

Import `format_duration` from `crate::format::cost::format_duration`.

### 4. Add test

In `src/commands_info.rs` tests section:
```rust
#[test]
fn test_handle_status_with_timing() {
    use std::time::Duration;
    // Just verify it doesn't panic with various inputs
    handle_status("test-model", "/tmp", &Usage::default(), Duration::from_secs(0), 0);
    handle_status("test-model", "/tmp", &Usage::default(), Duration::from_secs(125), 1);
    handle_status("test-model", "/tmp", &Usage::default(), Duration::from_secs(7200), 42);
}
```

### 5. Update the commands.rs re-export if needed

Check that `handle_status` is re-exported through `commands.rs`. Since the function signature changes, the call in `repl.rs` going through `commands::handle_status(...)` will need to match.

## Verification

1. `cargo build` — compiles clean
2. `cargo test` — all pass including the new test AND `build_repo_map_with_regex_backend` (the one that blocked last time)
3. `cargo clippy --all-targets -- -D warnings` — zero warnings

## Why this is smaller than last time

Last attempt bundled this into a multi-task session and the test race condition caused a cascading failure. This time: the race is fixed, the task is standalone, and the test is a simple no-panic check.
