Title: Dead code cleanup — remove 17 #[allow(dead_code)] annotations
Files: src/prompt.rs, src/commands_session.rs, src/format/tools.rs
Issue: none

The codebase has 17 `#[allow(dead_code)]` annotations across 4 files. These represent either
genuinely unused code or premature abstractions that should be cleaned up. This task handles
15 of them in 3 files (the remaining 2 in hooks.rs are handled in task 3).

**Analysis of each annotation:**

### prompt.rs (8 annotations)

1. `enable_audit_log()` (line 82) — NOW USED after task 1 wires up --audit. Remove the annotation.

2. `read_audit_log()` (line 172) — Only used in one test (line 2809). This is useful API surface
   for future commands like `/audit`. Keep it, remove annotation, verify test still uses it.

3. `clear_audit_log()` (line 187) — Never called anywhere, not even in tests. Remove the function
   entirely — it can be added back if needed.

4. `SessionChanges::len()` (line 255) — Part of the SessionChanges API. It's reasonable API surface
   (len/is_empty pattern). Remove annotation — clippy won't warn on pub methods of pub structs.
   Actually check: if clippy still warns, add a simple test using it.

5. `SessionChanges::is_empty()` (line 261) — Same as above. Remove annotation.

6. `TurnSnapshot::file_count()` (line 315) — Useful API but never called. Remove annotation,
   add a test that uses it OR remove the function if truly unneeded.

7. `TurnHistory::pop()` (line 379) — Part of the stack API. `undo_last()` exists but `pop()`
   is useful for future undo refinements. Remove annotation.

8. `PromptOutcome::was_overflow` (line 423) — Field on a struct. Remove annotation; the field
   is set in run_prompt code and is useful for callers.

### commands_session.rs (4 annotations)

9. `SpawnTracker::get()` (line 459) — Lookup by ID. Used by `handle_spawn_status`? Check.
   If not used, remove. If useful API, remove annotation.

10. `SpawnTracker::len()` (line 470) — Standard API surface. Remove annotation.

11. `SpawnTracker::is_empty()` (line 476) — Standard API surface. Remove annotation.

12. `parse_spawn_task()` (line 547) — Legacy compat wrapper. If truly never called outside tests,
    remove the function. It just delegates to parse_spawn_args.

### format/tools.rs (3 annotations)

13. `ActiveToolState` struct (line 199) — The struct and its methods. Check if it's used anywhere
    in the event loop. If not used at all, remove the entire struct + impl.

14. `ActiveToolState::new()` (line 209) — Constructor. Remove with struct if unused.

15. `ActiveToolState::update_partial()` (line 220) — Update method. Remove with struct if unused.

**What to do:**
- For each annotation, check if the item is used anywhere (grep for it)
- If used: remove `#[allow(dead_code)]`
- If not used and not useful: remove the function/struct entirely
- If not used but useful API surface: remove annotation and add a test
- Run `cargo build && cargo test && cargo clippy --all-targets -- -D warnings` after all changes
- If clippy complains about any items, either use them in tests or make them `pub(crate)` with `#[cfg(test)]` visibility
