Title: Add /blame command for git blame with colorized output
Files: src/commands_git.rs, src/help.rs
Issue: none

## What to do

Add a `/blame` command that wraps `git blame` with colored output and optional line-range support.
This is a common developer workflow — "who changed this line?" — that Claude Code supports
naturally through bash but yoyo doesn't have as a first-class command.

## Implementation

1. In `src/commands_git.rs`, add `pub fn handle_blame(input: &str)`:
   - Parse: `/blame <file>` or `/blame <file>:<start>-<end>` (line range)
   - Run `git blame <file>` (or with `-L start,end` for ranges)
   - Colorize the output:
     - Commit hash: DIM
     - Author name: CYAN  
     - Date: DIM
     - Line number: YELLOW
     - Code content: default
   - Handle errors (not in git repo, file not found, invalid range)

2. In `src/help.rs`:
   - Add `/blame` to the git section of help text with a short description
   - Add usage example: `/blame src/main.rs` and `/blame src/main.rs:10-20`

3. Wire it up:
   - Add "blame" to KNOWN_COMMANDS in `src/commands.rs`
   - Add the dispatch case in `src/repl.rs` wherever `/diff`, `/commit`, `/git` are dispatched

4. Tests (in `commands_git.rs`):
   - Parse test: `/blame src/main.rs` → file="src/main.rs", range=None
   - Parse test: `/blame src/main.rs:10-20` → file="src/main.rs", range=Some(10,20)
   - Parse test: `/blame` (no args) → error message
   - Colorize test: verify blame output gets ANSI codes applied
   - At least 4-5 unit tests

## Why

`git blame` is one of the most common developer commands. Having it as a first-class `/blame`
command with colorized output and line-range syntax makes yoyo more useful for actual code
investigation workflows. It's small, self-contained, and immediately useful.
