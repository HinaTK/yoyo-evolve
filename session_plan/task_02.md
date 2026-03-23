Title: Add /diff --staged and /diff <file> for targeted diff viewing
Files: src/commands_git.rs, src/help.rs
Issue: none

## Context

Currently `/diff` shows unstaged changes only. Claude Code lets you view staged changes and per-file diffs easily. Developers frequently need to review what they're about to commit (`git diff --staged`) or see changes to a specific file (`git diff src/main.rs`). Adding these two patterns to `/diff` makes the command genuinely useful for pre-commit workflows.

## Implementation

1. **In `src/commands_git.rs`**: Modify `handle_diff()` to parse additional arguments:
   - `/diff` — current behavior (unstaged changes), unchanged
   - `/diff --staged` or `/diff --cached` — shows `git diff --cached` output with colored formatting
   - `/diff <file>` — shows `git diff <file>` for a specific file, with colored formatting
   - `/diff --staged <file>` — shows staged diff for a specific file

   The parsing is simple: check if the first arg after `/diff` is `--staged` or `--cached`, then check if there's a file argument after that.

   Use the existing `colorize_diff()` function from `git.rs` to format the output. Use the existing `parse_diff_stat()` and `format_diff_stat()` for the summary line.

2. **In `src/help.rs`**: Update the `/diff` help entry to document the new `--staged` and `<file>` options with examples.

3. **Tests**:
   - `test_diff_parse_staged_flag`: parsing logic correctly identifies --staged
   - `test_diff_parse_file_arg`: parsing logic correctly identifies file argument
   - `test_diff_parse_staged_with_file`: both flags together
   - `test_diff_parse_plain`: no args returns default behavior

4. **Tab completion**: Add `--staged` and `--cached` to the argument completions for `/diff` in `command_arg_completions()`.

This closes a real workflow gap — developers reviewing changes before committing is one of the most common git operations, and right now they have to drop to bash to see staged diffs.
