Title: Move git-related tests from commands.rs to commands_git.rs
Files: src/commands.rs, src/commands_git.rs
Issue: #260

Move all git-related tests (~36 tests) from the `#[cfg(test)] mod tests` block in `commands.rs` to a new `#[cfg(test)] mod tests` block in `commands_git.rs`.

## Which tests to move

All tests that exercise git/PR/review/diff functionality. Grep for these test function name patterns:
- `test_pr_*` (pr_command_recognized, pr_command_matching, pr_number_parsing, pr_subcommand_*)
- `test_review_*` (review_command_recognized, review_command_matching, review_content_*, review_prompt_*, review_help_text_*)
- `test_parse_diff_stat_*`, `test_format_diff_stat_*`
- `test_build_review_*`

There are approximately 36 such tests.

## How to do it

1. Look at the existing imports in `commands.rs`'s test module that pull from `commands_git`:
   ```rust
   use crate::commands_git::{
       build_review_content, build_review_prompt, format_diff_stat, parse_diff_stat,
       parse_pr_args, DiffStatEntry, DiffStatSummary, PrSubcommand,
   };
   ```

2. In `commands_git.rs`, add a `#[cfg(test)] mod tests { ... }` block at the end (if one doesn't exist already).

3. Move all the git-related test functions into `commands_git.rs`'s test module. Update the imports:
   - Functions like `parse_pr_args`, `format_diff_stat`, etc. are already `pub` in `commands_git.rs`, so in the new test module use `use super::*;`
   - Some tests may reference `is_unknown_command` or `KNOWN_COMMANDS` from `commands.rs` — those need `use crate::commands::*;` or specific imports.

4. Remove those test functions from `commands.rs`.

5. Remove the now-unused `use crate::commands_git::...` import from `commands.rs`'s test module (unless some remaining tests still use them).

6. Run `cargo test` to verify all tests pass. Run `cargo clippy --all-targets -- -D warnings` to check for warnings.

## Verification

- `cargo test` — all 1,725+ tests pass
- `cargo clippy --all-targets -- -D warnings` — no warnings
- The test count should be identical before and after
- `commands.rs` should shrink by roughly the number of lines occupied by these tests
