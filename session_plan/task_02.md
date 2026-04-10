Title: Enrich /changes with optional diff display
Files: src/commands_retry.rs, src/prompt.rs
Issue: none

## Problem

Currently `/changes` just lists filenames with icons:
```
  2 files modified this session:
    ✏ src/foo.rs (write)
    🔧 src/bar.rs (edit)
```

Real developers want to see WHAT changed before committing. Claude Code shows diffs naturally. Adding a diff view to `/changes` lets users review the agent's work without switching to another tool.

## Solution

Add a `--diff` flag to `/changes` that shows a compact, colorized git diff filtered to only the files the agent modified during the session.

### Concrete steps:

1. **In `commands_retry.rs`**: Modify `handle_changes` to accept a `&str` input parameter (the raw `/changes` command text) so it can detect `--diff`. When `--diff` is present:
   - Get the list of modified files from `SessionChanges::snapshot()`
   - For each file, run `git diff -- <file>` and `git diff --cached -- <file>` 
   - Colorize the output using `crate::git::colorize_diff`
   - Print the colorized diff after the file listing
   - If no git diff is available (file not in git, or no diff), note it as "(no diff available)"

2. **In `prompt.rs`**: Modify `format_changes` to accept an optional `show_diff: bool` parameter. When true, include the diff output for each file in the formatted string. Use `crate::git::run_git` to get the diff and `crate::git::colorize_diff` to color it.

   Actually, simpler approach: keep `format_changes` as-is for the listing, and add the diff display logic directly in `handle_changes` in `commands_retry.rs`. This avoids changing `format_changes`'s signature.

3. **Update help text**: In `help.rs`, update the `/changes` help entry to mention the `--diff` flag.

4. **Tests**: Add a test that `/changes --diff` doesn't panic when there are no changes. Add a test that the diff flag is correctly parsed.

## What NOT to do

- Don't change the default `/changes` behavior (no flag = same as before)
- Don't make this overly complex — just filter `git diff` output to session files
- Don't touch more than 2 source files (commands_retry.rs and help.rs)
