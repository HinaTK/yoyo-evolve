Title: Poison-proof mutex/rwlock handling in production code
Files: src/commands_bg.rs, src/commands_spawn.rs
Issue: none

## What

Replace all `.lock().unwrap()`, `.read().unwrap()`, and `.write().unwrap()` calls in
`commands_bg.rs` (13 occurrences) and `commands_spawn.rs` (5 occurrences) with
poison-recovering variants.

## Why

These are the two modules that use `std::sync::Mutex` in multi-threaded contexts
(background jobs and spawn tasks). If a spawned thread panics while holding a lock,
the mutex becomes "poisoned" and all subsequent `.lock().unwrap()` calls will panic,
cascading the failure to the entire process. This is the most likely place for
mutex poisoning to occur in production.

## How

Create a small helper function (or use inline `.unwrap_or_else(|e| e.into_inner())`):

```rust
/// Acquire a mutex lock, recovering from poison if a thread panicked.
fn lock_or_recover<T>(mutex: &std::sync::Mutex<T>) -> std::sync::MutexGuard<'_, T> {
    mutex.lock().unwrap_or_else(|e| e.into_inner())
}
```

Replace each `.lock().unwrap()` with either:
- The helper function, OR
- Inline `.lock().unwrap_or_else(|poisoned| poisoned.into_inner())` if the helper
  doesn't fit the context.

For `commands_bg.rs`:
- Lines 73, 77, 86, 93, 104, 120, 127, 130, 143, 149, 188, 265, 269

For `commands_spawn.rs`:
- Lines 64, 78, 87, 96, 101

## Tests

- Existing tests should continue to pass (no behavioral change in non-poisoned case)
- Add a test that verifies a poisoned mutex still allows recovery
- `cargo build && cargo test && cargo clippy --all-targets -- -D warnings`
