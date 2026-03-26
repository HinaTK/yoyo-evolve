Title: Fix flaky todo tests — isolate shared global state
Files: src/commands_project.rs, Cargo.toml
Issue: none (P0 CI stability)

## Problem

`test_handle_todo_done` (and all todo tests) share a global `TODO_LIST: RwLock<Vec<TodoItem>>` and `TODO_NEXT_ID: AtomicUsize`. When `cargo test` runs tests in parallel, multiple todo tests call `todo_clear()` + `todo_add()` concurrently, racing on the same statics. The test passes alone but fails ~1 in 3 full-suite runs.

## Fix

Add the `serial_test` crate as a dev-dependency and mark all todo tests with `#[serial]` so they run sequentially. This is the simplest, most reliable fix — no need to refactor the global state (which is shared with the REPL `/todo` command and `TodoTool` by design).

### Step 1: Add serial_test dependency

In `Cargo.toml`, add under `[dev-dependencies]`:
```toml
serial_test = "3"
```

### Step 2: Import and annotate todo tests

In `src/commands_project.rs`, at the top of the `#[cfg(test)] mod tests` block, add:
```rust
use serial_test::serial;
```

Then add `#[serial]` attribute to ALL todo-related test functions:
- `test_handle_todo_add`
- `test_handle_todo_show_empty`
- `test_handle_todo_done`
- `test_handle_todo_wip`
- `test_handle_todo_remove_via_command`
- `test_handle_todo_clear_via_command`
- `test_handle_todo_unknown_subcommand`
- `test_handle_todo_add_empty_description`
- `test_todo_in_known_commands` (if it touches todo state)

Each test should look like:
```rust
#[test]
#[serial]
fn test_handle_todo_done() {
    todo_clear();
    // ...
}
```

### Step 3: Also check for any TodoTool tests in main.rs

Search `src/main.rs` for `todo` tests. If the `TodoTool` tests also use the shared global state, they need `#[serial]` too. Check with:
```
grep -n "test.*todo\|TodoTool" src/main.rs
```

### Step 4: Verify

Run `cargo test` at least 3 times to confirm the flaky test is fixed:
```bash
cargo test && cargo test && cargo test
```

Also verify:
```bash
cargo clippy --all-targets -- -D warnings
cargo fmt -- --check
```

This is the hardest-first task: it's small but it's P0 because it breaks CI randomly.
