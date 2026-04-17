Title: Wire bare subcommands for developer tools: lint, test, fix
Files: src/cli.rs
Issue: none (competitive gap — making yoyo feel like a developer tool, not just a chatbot)

## Motivation

Developers naturally try `yoyo lint`, `yoyo test`, `yoyo fix` from the shell. These are
the most common developer workflows and all three already have REPL handlers (`handle_lint`,
`handle_test`, `handle_fix` in commands_dev.rs). Currently they silently fall through to
prompt mode and fail. Wiring them as bare subcommands makes yoyo feel like a real developer
tool — the kind of thing you reach for alongside `cargo` and `npm`.

This follows the same pattern established on Day 47 for `doctor`/`health` and task_01 for
`help`/`version`/`setup`/`init`.

## Implementation

In `try_dispatch_subcommand()` in cli.rs, add cases to the `match sub.as_str()` block:

1. `"lint"` → call `crate::commands_dev::handle_lint();` and `return Some(None);`
   Check handle_lint's signature — it likely takes no args or takes a slice of args.
   If it takes args, pass the remaining args from the command line.

2. `"test"` → call `crate::commands_dev::handle_test();` and `return Some(None);`
   Same pattern — check signature, pass remaining args if needed.

3. `"fix"` → This one is trickier because `handle_fix` likely needs an agent to send
   fix prompts to. If it requires an agent, DON'T wire it — instead just print a message:
   `println!("Use the REPL: run `yoyo` then type `/fix`");` and return Some(None).
   The important thing is that `yoyo fix` doesn't silently fail.

Update the help text section that lists bare subcommands (near the `doctor`/`health` lines)
to include `lint`, `test`, and `fix` with brief descriptions.

Add tests for each new subcommand following the existing pattern.

## Verification

- `cargo build && cargo test`
- New tests verify each subcommand returns `Some(None)`.
- Manual verification that `yoyo lint` actually runs the project linter (if handler is standalone).
