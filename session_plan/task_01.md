Title: Wire session-free commands as shell subcommands
Files: src/cli.rs
Issue: none (self-discovered bug: `yoyo changelog` hangs)

## Problem

`yoyo changelog` falls through to stdin/agent mode and hangs because it's not wired in
`try_dispatch_subcommand`. Several other session-free commands (`config show`, `permissions`,
`memories`, `todo list`) also aren't accessible from the shell.

## What to do

In `try_dispatch_subcommand()` in `src/cli.rs`, add match arms for these subcommands:

1. **`changelog`** — Call `crate::commands_info::handle_changelog(&input)` where input is
   built via `quote_args_as_command(args)`. Example: `yoyo changelog 20` → `/changelog 20`.

2. **`config`** — This one is trickier because `handle_config` requires agent/hooks/skills params.
   For the shell subcommand, only wire `yoyo config show` which just prints the config.
   Dispatch: if args[2..] starts with "show" or args has no further args, call
   `crate::commands_config::handle_config_show()`. For other config subcommands, print a message
   saying they require an interactive session.

3. **`permissions`** — Call `crate::commands_config::handle_permissions()` (no args needed,
   just prints current permission config). Check the function signature first.

4. **`todo`** — Call `crate::commands_project::handle_todo(&input)` with `quote_args_as_command`.
   Example: `yoyo todo list` → `/todo list`, `yoyo todo add fix the bug` → `/todo add fix the bug`.

5. **`memories`** — Call `crate::commands_memory::handle_memories(&input)`.
   Example: `yoyo memories` → `/memories`.

For each, add a test similar to the existing `test_try_dispatch_subcommand_tree` test:
verify that `try_dispatch_subcommand(&["yoyo".into(), "CMD".into()])` returns `Some(None)`.

Also add these new subcommands to the help text `SUBCOMMANDS` list (the section that shows
available shell subcommands in `--help` output) and to the existing test that validates all
subcommands appear in help text.

## Verification

- `cargo build && cargo test`
- After build: `timeout 5 cargo run --quiet -- changelog` should print git log, not hang
- `timeout 5 cargo run --quiet -- todo list` should work
- `timeout 5 cargo run --quiet -- memories` should work
