Title: Wire git-workflow bare subcommands (diff, commit, review, blame)
Files: src/cli.rs
Issue: none

## Context

This is the second half of the "front door" fix. Task 1 wires dev commands; this task wires git commands. A developer who types `yoyo diff`, `yoyo commit "fix typo"`, `yoyo review`, or `yoyo blame src/main.rs` should get immediate output, not silence.

Same pattern as Task 1, same file (cli.rs), same `try_dispatch_subcommand` function.

## What to do

Add match arms in `try_dispatch_subcommand` for:

1. **`"diff"`** → Call `crate::commands_git::handle_diff(input)` where `input` is `/diff <rest>`. `yoyo diff --staged` → `handle_diff("/diff --staged")`. Return `Some(None)`.

2. **`"commit"`** → Call `crate::commands_git::handle_commit(input)` where `input` is `/commit <rest>`. `yoyo commit "fix typo"` → `handle_commit("/commit fix typo")`. Return `Some(None)`.

3. **`"review"`** → Call `crate::commands_git::handle_review(input)` where `input` is `/review <rest>`. Note: `handle_review` returns a `String` (the review prompt content). For the bare subcommand, just print it. Return `Some(None)`.

4. **`"blame"`** → Call `crate::commands_git::handle_blame(input)` where `input` is `/blame <rest>`. `yoyo blame src/main.rs 10-20` → `handle_blame("/blame src/main.rs 10-20")`. Return `Some(None)`.

Use the same input reconstruction pattern: `let input = format!("/{}", args[1..].join(" "));`

**Important:** Check `handle_review`'s signature carefully — it may return content that's meant to be fed to the agent. For the bare subcommand case (no agent running), just print whatever it returns to stdout. If it needs an agent/model, print a message saying "review requires an active session" and return.

Also check `handle_commit`'s signature — if it tries to generate a commit message via AI, the bare subcommand should only support the explicit-message form (where the user provides the message).

## Tests

Add tests:
- `test_try_dispatch_subcommand_diff` — verify returns `Some(None)`
- `test_try_dispatch_subcommand_commit` — verify returns `Some(None)` (will just print usage if no message)
- `test_try_dispatch_subcommand_blame` — verify returns `Some(None)`

## Verification

```bash
cargo build && cargo test
# Manual checks (should not hang):
echo "" | timeout 5 cargo run -- diff 2>&1 || true
echo "" | timeout 5 cargo run -- blame 2>&1 || true
```
