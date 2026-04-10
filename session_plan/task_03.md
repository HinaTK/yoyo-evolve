Title: Move remaining misplaced tests from commands.rs to their owning modules
Files: src/commands.rs, src/commands_session.rs, src/commands_memory.rs, src/commands_file.rs, src/commands_retry.rs, src/commands_info.rs, src/commands_project.rs
Issue: #260

Move all remaining tests that belong to sibling command modules out of `commands.rs`. After Tasks 1 and 2 moved git (~36) and search (~19) tests, this task moves the rest: session, memory, file, retry, info, and project tests.

**IMPORTANT:** This task should run AFTER tasks 1 and 2. It operates on whatever tests remain in `commands.rs` after those extractions.

## Which tests to move and where

### To `commands_session.rs` (~26 tests):
- `test_save_load_command_matching`
- `test_spawn_command_*` (recognized, matching)
- `test_parse_spawn_*` (task_with_task, task_empty, task_whitespace_only, task_preserves_full_task, args_basic, args_with_output, args_status)
- `test_mark_command_*`, `test_jump_command_*`
- `test_parse_bookmark_name_*`
- `test_bookmarks_*` (create_and_list, overwrite_same_name, nonexistent_returns_none, multiple_entries)
- `test_handle_marks_*`
- `test_arg_completions_save_load_json_files`

### To `commands_memory.rs` (~7 tests):
- `test_remember_command_*` (recognized, matching)
- `test_memories_command_recognized`
- `test_forget_command_*` (recognized, matching)
- `test_memory_crud_roundtrip`
- `test_memory_format_for_prompt_integration`

### To `commands_file.rs` (~8 tests):
- `test_add_command_recognized`
- `test_add_in_help_text`
- `test_handle_add_*` (no_args_returns_empty, with_space_no_args_returns_empty, real_file, with_line_range, glob_pattern, nonexistent_file, multiple_files)

### To `commands_retry.rs` (~2 tests):
- `test_changes_command_recognized`
- `test_changes_command_not_confused_with_other_commands`

### To `commands_info.rs` (~3 tests):
- `test_tokens_display_labels`
- `test_tokens_display_with_large_values`
- `test_tokens_labels_are_clarified`

### To `commands_project.rs` (~4 tests):
- `test_docs_command_recognized`, `test_docs_command_matching`, `test_docs_crate_arg_extraction`
- `test_plan_in_known_commands`, `test_plan_in_help_text`

## How to do it

For each target module:
1. Add `#[cfg(test)] mod tests { use super::*; ... }` if not already present
2. Move the test functions in, adding any needed imports (e.g., `use crate::commands::is_unknown_command;`)
3. Remove the test functions from `commands.rs`
4. Clean up unused imports in `commands.rs`'s test module

After all moves, `commands.rs`'s test module should contain only tests that genuinely test `commands.rs`'s own functions (command dispatch, completions, `is_unknown_command`, `thinking_level_name`, `handle_provider_switch`). That should be roughly 25-35 tests.

## Verification

- `cargo test` — all tests pass
- `cargo clippy --all-targets -- -D warnings` — no warnings
- `commands.rs` total lines should be under 1,500 (target: ~1,100-1,300 after all 3 tasks)
- Each destination module compiles with its new tests
