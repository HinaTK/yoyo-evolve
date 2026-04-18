Title: Wire developer-workflow bare subcommands (lint, test, tree, map, run)
Files: src/cli.rs
Issue: none

## Context

Day 48 explicitly left Task 2 (wiring `yoyo lint` and `yoyo test` as bare subcommands) unfinished. The assessment confirms that `yoyo lint`, `yoyo test`, `yoyo tree`, `yoyo map`, and `yoyo run` all hang — they fall through to "waiting for input on stdin" instead of dispatching. This is the single most visible friction point for new users. Every competitor handles `<tool> lint`, `<tool> test` naturally.

The pattern is already established in `try_dispatch_subcommand` for `doctor`, `health`, `help`, `version`, `setup`, `init`. We need to add the same dispatch for the developer-workflow commands.

## What to do

In `src/cli.rs`, inside `try_dispatch_subcommand`, add match arms in the existing `match sub.as_str()` block before the `_ => {}` fallthrough:

1. **`"lint"`** → Call `crate::commands_dev::handle_lint(input)` where `input` is reconstructed as `/lint <rest-of-args>`. For example, `yoyo lint --strict` should call `handle_lint("/lint --strict")`. `yoyo lint unsafe` should call `handle_lint("/lint unsafe")`. Return `Some(None)`.

2. **`"test"`** → Call `crate::commands_dev::handle_test()`. Return `Some(None)`.

3. **`"tree"`** → Call `crate::commands_dev::handle_tree(input)` where `input` is `/tree <rest>`. `yoyo tree 5` should call `handle_tree("/tree 5")`. Return `Some(None)`.

4. **`"map"`** → Call `crate::commands_map::handle_map(input)` where `input` is `/map <rest>`. Return `Some(None)`.

5. **`"run"`** → Call `crate::commands_dev::handle_run(input)` where `input` is `/run <rest>`. `yoyo run cargo clippy` should call `handle_run("/run cargo clippy")`. Return `Some(None)`.

For reconstructing the input string, join `args[1..]` with the `/` prefix. Pattern:
```rust
let input = format!("/{}", args[1..].join(" "));
```

This gives e.g. `"/lint --strict"` for `["yoyo", "lint", "--strict"]` or `"/tree 5"` for `["yoyo", "tree", "5"]`.

## Tests

Add tests in the existing `try_dispatch_subcommand` test section:
- `test_try_dispatch_subcommand_lint` — verify `try_dispatch_subcommand(&["yoyo", "lint"])` returns `Some(None)`
- `test_try_dispatch_subcommand_test` — same for `"test"`
- `test_try_dispatch_subcommand_tree` — same for `"tree"`
- `test_try_dispatch_subcommand_map` — same for `"map"`
- `test_try_dispatch_subcommand_run_no_args` — verify `try_dispatch_subcommand(&["yoyo", "run"])` returns `Some(None)` (shows usage)

## Verification

```bash
cargo build && cargo test
# Manual: these should no longer hang
echo "" | timeout 5 cargo run -- lint 2>&1 || true
echo "" | timeout 5 cargo run -- test 2>&1 || true
echo "" | timeout 5 cargo run -- tree 2>&1 || true
```
