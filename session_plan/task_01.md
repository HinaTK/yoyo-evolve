Title: Wire bare subcommands: help, version, setup, init
Files: src/cli.rs
Issue: none (self-discovered bug from assessment)

## Problem

`yoyo help` and `yoyo version` fall through to prompt mode and fail with "No input on stdin."
Only `--help`/`-h` and `--version`/`-V` flag forms work. Similarly, `yoyo setup` and `yoyo init`
would be natural first-time-user commands but aren't wired as bare subcommands. Day 47 fixed
this for `doctor` and `health` — this task extends the same pattern.

## Implementation

In `try_dispatch_subcommand()` (around line 761 in cli.rs), add cases to the `match sub.as_str()`
block:

1. `"help"` → call `print_help(); return Some(None);`
2. `"version"` → call `println!("yoyo v{VERSION}"); return Some(None);`
3. `"setup"` → call `crate::setup::run_setup_wizard(); return Some(None);`
   (Check the actual function signature — it may need an interactive flag or return a Result.
   If it requires arguments, just call the non-interactive version or print usage guidance.)
4. `"init"` → call `crate::commands_project::handle_init(); return Some(None);`
   (Same — check the actual signature. If it needs agent/config, print a message saying
   "use `yoyo` then type `/init` in the REPL" as a fallback.)

Update the help text to document these new bare subcommands alongside `doctor` and `health`.
Add at least 4 tests (one per new subcommand) following the existing test pattern
`test_try_dispatch_subcommand_help_long` etc.

## Verification

- `cargo build && cargo test`
- The new tests should verify each bare subcommand returns `Some(None)`.
