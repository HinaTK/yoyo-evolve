Title: /lint agent integration — feed lint output to AI and add /lint fix
Files: src/commands_dev.rs, src/repl.rs
Issue: #294

## What

Currently `/lint` runs clippy and prints results, but the REPL ignores the return value:

```rust
"/lint" => {
    commands::handle_lint();  // return value is DROPPED
    continue;
}
```

Meanwhile `/fix` properly feeds failures to the agent via `last_input`. This means `/lint` is a dead-end — the user sees errors but the agent doesn't. Issue #294 asks for deeper lint integration, and the first concrete step is making lint results flow into the agent.

## Changes

### 1. Wire `/lint` return value in repl.rs

Change the `/lint` dispatch to capture the return value and set it as `last_input` when there are failures, similar to how `/fix` works:

```rust
"/lint" => {
    if let Some(lint_result) = commands::handle_lint() {
        last_input = Some(lint_result);
    }
    continue;
}
```

### 2. Add `/lint fix` subcommand in commands_dev.rs

Add a new function `handle_lint_fix` that:
1. Runs the lint command (same as `handle_lint`)
2. If lint fails, builds a fix prompt from the lint output (reuse `build_fix_prompt` pattern)
3. Sends the fix prompt to the agent

The `/lint fix` subcommand should be parsed from the input in `repl.rs`. When the user types `/lint fix`, it runs lint and auto-sends failures to the AI for correction.

Add the subcommand parsing in repl.rs:
- `/lint` — run lint, feed summary to agent context if failures
- `/lint fix` — run lint, if failures send to AI for auto-fixing (like `/fix` but lint-only)

### 3. Improve lint failure output format

When `/lint` fails, the summary returned should include the actual clippy error messages (truncated to a reasonable size), not just "Lint FAILED". Currently `handle_lint` already captures stderr — make sure the full error context flows into the agent prompt so it can reason about fixes.

### 4. Add `/lint fix` to help text

Update the `/lint` entry in `src/help.rs` to mention the `fix` subcommand.

### 5. Tests

Add a test for the lint fix prompt building — verify that when lint output contains clippy warnings, the prompt includes them in a structured format the agent can act on.

## Verification

- `cargo build && cargo test`
- The `/lint` command now returns useful context to the agent
- `/lint fix` is documented in help
