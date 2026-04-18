Title: Complete REPL command listing in help text
Files: src/help.rs, src/cli.rs
Issue: none

## Problem

The help text (`yoyo help` and `/help`) lists ~40 REPL commands but there are 70+. Missing commands include: `/add`, `/apply`, `/ast`, `/bg`, `/blame`, `/changelog`, `/changes`, `/export`, `/grep`, `/index`, `/map`, `/mark`/`/jump`/`/marks`, `/mcp`, `/move`, `/permissions`, `/plan`, `/refactor`, `/rename`, `/spawn`, `/stash`, `/teach`, `/todo`, `/watch`, `/web`. A new user cannot discover most of what yoyo can do.

## Fix

### 1. Audit all REPL commands

The canonical list of REPL commands is in `src/repl.rs` (the match arms in `run_repl`) and `src/commands.rs` (`KNOWN_COMMANDS`). Cross-reference these against what's in the help text.

### 2. Add missing commands to help text

In `src/help.rs`, add the missing commands organized into the existing category groups. The help text already has categories like "Session", "Search & Navigation", "Git & Code", "Info", etc. Add new groups as needed:

- **Files & Content**: `/add`, `/apply`, `/web`
- **Search & Navigation**: `/grep`, `/find`, `/index`, `/ast` (if not already listed)
- **Git & Code**: `/blame`, `/commit`, `/diff`, `/review`, `/pr`, `/undo` (some may already be there)
- **Code Intelligence**: `/map`, `/rename`, `/refactor`, `/move`, `/extract`
- **Project**: `/todo`, `/plan`, `/init`, `/watch`
- **Session Management**: `/mark`, `/jump`, `/marks`, `/stash`, `/export`, `/spawn`, `/bg`
- **Configuration**: `/mcp`, `/permissions`, `/teach`
- **Info**: `/changelog`, `/changes`

Each command should have a one-line description. Keep descriptions short (under 60 chars).

### 3. Update `print_help` in cli.rs if needed

If the bare `yoyo help` output (from `cli.rs::print_help`) has a separate command listing section, update it too. The two help outputs should be consistent.

### Tests

- Verify the help text compiles (it's a string literal, so `cargo build` suffices)
- If there's an existing test that checks help text content, update it
- Grep for `KNOWN_COMMANDS` in commands.rs and verify every entry appears in the help text
