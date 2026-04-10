Title: Move search-related tests from commands.rs to commands_search.rs
Files: src/commands.rs, src/commands_search.rs
Issue: #260

Move all search-related tests (~19 tests) from the `#[cfg(test)] mod tests` block in `commands.rs` to a new or existing `#[cfg(test)] mod tests` block in `commands_search.rs`.

## Which tests to move

All tests that exercise find/search/index/fuzzy functionality. Grep for these test function name patterns:
- `test_find_*` (find_command_recognized, find_files_returns_sorted, find_files_no_results, find_command_matching)
- `test_fuzzy_score_*` (basic_match, no_match, case_insensitive, filename_match_higher, start_of_filename_bonus)
- `test_highlight_match_basic`
- `test_extract_first_meaningful_line_*` (skips_blanks, empty, truncates_long_lines)
- `test_is_binary_extension`
- `test_format_project_index_*` (empty, with_entries, single_file)
- `test_build_project_index_tempdir`
- `test_index_entry_construction`

There are approximately 19 such tests.

## How to do it

1. Look at the existing imports in `commands.rs`'s test module that pull from `commands_search`:
   ```rust
   use crate::commands_search::{
       extract_first_meaningful_line, find_files, format_project_index, fuzzy_score,
       highlight_match, is_binary_extension, IndexEntry,
   };
   ```

2. In `commands_search.rs`, add a `#[cfg(test)] mod tests { ... }` block at the end (if one doesn't exist already). If one already exists, add the tests to it.

3. Move all the search-related test functions into `commands_search.rs`'s test module. Update imports:
   - Functions are already `pub` in `commands_search.rs`, so use `use super::*;`
   - Some tests may reference `is_unknown_command` or `KNOWN_COMMANDS` from `commands.rs` — those need `use crate::commands::*;` or specific imports.

4. Remove those test functions from `commands.rs`.

5. Remove the now-unused `use crate::commands_search::...` import from `commands.rs`'s test module.

6. Run `cargo test` to verify all tests pass. Run `cargo clippy --all-targets -- -D warnings` to check for warnings.

## Verification

- `cargo test` — all tests pass
- `cargo clippy --all-targets -- -D warnings` — no warnings
- Test count unchanged
- `commands.rs` shrinks by ~19 tests worth of lines
