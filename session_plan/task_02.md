Title: Extract /spawn subsystem from commands_session.rs into commands_spawn.rs
Files: src/commands_session.rs, src/commands_spawn.rs (new), src/commands.rs
Issue: none

## What to do

`commands_session.rs` is 2004 lines and contains the entire `/spawn` subsystem alongside
session management (save/load/history/compact/stash/export/bookmarks). The spawn code is
self-contained and accounts for ~300-400 lines. Extract it into its own file.

## Implementation

1. Create `src/commands_spawn.rs` containing:
   - `SpawnStatus` enum
   - `SpawnTask` struct
   - `SpawnTracker` struct with all methods (new, register, complete, fail, snapshot, count_by_status, get, len, is_empty)
   - `SpawnArgs` struct
   - `parse_spawn_args` function
   - `parse_spawn_task` function
   - `spawn_context_prompt` function
   - `summarize_conversation_for_spawn` function
   - `format_spawn_result` function
   - `handle_spawn_status` function
   - `handle_spawn` function
   - All associated tests

2. In `commands_session.rs`:
   - Remove all the moved code
   - Add `pub use commands_spawn::*;` or update imports as needed

3. In `src/commands.rs` (or wherever spawn is re-exported):
   - Update imports to point to `commands_spawn` if needed
   - Make sure `handle_spawn` and `SpawnTracker` are accessible from `repl.rs`

4. Run `cargo build && cargo test` — all existing tests must pass unchanged.

## Why

Module splitting has been the backbone of keeping the codebase navigable (12 commands_*.rs files
already). The spawn subsystem is a complete, self-contained feature with its own types, parser,
and handler — it deserves its own home. This also makes commands_session.rs easier to navigate
for session-specific work (save/load/compact/stash/export).
