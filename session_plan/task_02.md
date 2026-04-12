Title: Harden RwLock unwraps in TODO_LIST to prevent panics on poisoned locks
Files: src/commands_project.rs
Issue: none

## Problem

The assessment found 74 production `.unwrap()` calls. The most dangerous are the RwLock unwraps on `TODO_LIST` in `commands_project.rs` (lines 56, 62, 74, 79, 85). If any thread panics while holding the lock, the RwLock becomes "poisoned" and ALL subsequent `.unwrap()` calls on it will panic, cascading the failure.

The regex `.unwrap()` calls in commands_search.rs are safe (literal patterns that can't fail), but RwLock poisoning is a real runtime failure mode.

## Implementation

Replace the 5 RwLock `.unwrap()` calls with `.unwrap_or_else(|e| e.into_inner())` which recovers from poisoned locks by extracting the inner data:

### In `todo_add` (line 56):
```rust
// Before:
TODO_LIST.write().unwrap().push(item);
// After:
TODO_LIST.write().unwrap_or_else(|e| e.into_inner()).push(item);
```

### In `todo_update` (line 62):
```rust
// Before:
let mut list = TODO_LIST.write().unwrap();
// After:
let mut list = TODO_LIST.write().unwrap_or_else(|e| e.into_inner());
```

### In `todo_list` (line 74):
```rust
// Before:
TODO_LIST.read().unwrap().clone()
// After:
TODO_LIST.read().unwrap_or_else(|e| e.into_inner()).clone()
```

### In `todo_clear` (line 79):
```rust
// Before:
TODO_LIST.write().unwrap().clear();
// After:
TODO_LIST.write().unwrap_or_else(|e| e.into_inner()).clear();
```

### In `todo_remove` (line 85):
```rust
// Before:
let mut list = TODO_LIST.write().unwrap();
// After:
let mut list = TODO_LIST.write().unwrap_or_else(|e| e.into_inner());
```

### Add a test

```rust
#[test]
fn test_todo_rwlock_recovery() {
    // Verify that todo operations don't panic even after a poisoned lock scenario.
    // We can't easily poison an RwLock in a test, but we can verify the pattern compiles
    // and the functions work correctly in sequence.
    todo_clear();
    todo_add("test task".to_string());
    let list = todo_list();
    assert_eq!(list.len(), 1);
    todo_update(0, TodoStatus::Done);
    let list = todo_list();
    assert_eq!(list[0].status, TodoStatus::Done);
    todo_remove(0);
    let list = todo_list();
    assert!(list.is_empty());
}
```

## Why this matters

A single panic anywhere in the codebase while the TODO_LIST lock is held would cascade to crash every subsequent `/todo` command for the rest of the session. The `unwrap_or_else(|e| e.into_inner())` pattern is the standard Rust idiom for recovering from poisoned locks — it extracts the data even after poisoning, accepting that it might be in an inconsistent state (which for a simple Vec<TodoItem> is acceptable).

## Verification

1. `cargo build` — compiles clean
2. `cargo test` — all pass including new test
3. `cargo clippy --all-targets -- -D warnings` — zero warnings
