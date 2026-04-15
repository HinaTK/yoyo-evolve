Title: Clean up main.rs — remove stale dead_code annotation and extract mode handlers
Files: src/main.rs
Issue: none

## What to do

Two cleanups in main.rs:

### 1. Remove stale `#[allow(dead_code)]` on `mod commands_bg` (line 40)

The annotation `#[allow(dead_code)] // wired in task 2` was left over from the Day 45 session that shipped `/bg`. The module IS fully wired (used in commands.rs via handle_bg and BackgroundJobTracker). Remove the annotation and comment. Verify with `cargo clippy --all-targets -- -D warnings` — if clippy complains about dead code, the annotation was needed and should stay.

### 2. Extract piped-mode and single-prompt-mode from `main()`

The `main()` function (lines 560-1016, ~456 lines) handles three distinct modes inline:
- Agent building and setup (~lines 560-750)
- Piped mode (stdin not a terminal) — reads all stdin, runs prompt, exits
- Single-prompt mode (`-p` flag) — runs prompt with the given text, exits
- REPL mode — falls through to `run_repl()`

Extract the piped-mode body and the single-prompt-mode body into separate async helper functions:
- `async fn run_piped_mode(agent: &mut Agent, config: &Config, ...) -> ...`
- `async fn run_single_prompt(agent: &mut Agent, config: &Config, ...) -> ...`

These should live in main.rs right above `main()`. Each takes the agent, config, and any other state they need (output_path, etc.) as parameters. The main() function calls them and handles the result.

Keep the function signatures minimal — don't over-parameterize. If a helper needs 5+ params, consider a small struct or just pass the parts it actually uses.

**Do NOT touch** any other files. This is a pure main.rs refactor.

### Verification
- `cargo build`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `cargo fmt -- --check`
