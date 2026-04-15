Title: Configurable clippy lint strictness — /lint pedantic and /lint strict
Files: src/commands_dev.rs, src/help.rs
Issue: #294

## What

Issue #294 specifically mentions clippy's lint groups and `#![forbid(unsafe_code)]` as areas for deeper integration. Currently `/lint` always runs `cargo clippy --all-targets -- -D warnings` — the default strictness. Power users want stricter analysis.

Add lint strictness subcommands:
- `/lint` — default (existing behavior: `-D warnings`)
- `/lint pedantic` — runs with `-W clippy::pedantic` added
- `/lint strict` — runs with `-W clippy::pedantic -W clippy::nursery` added
- `/lint fix` — (from task 1) auto-fix mode

## Changes

### 1. Add lint strictness levels in commands_dev.rs

Add a `LintStrictness` enum:
```rust
enum LintStrictness {
    Default,    // -D warnings (existing)
    Pedantic,   // -D warnings -W clippy::pedantic  
    Strict,     // -D warnings -W clippy::pedantic -W clippy::nursery
}
```

Modify `lint_command_for_project` to accept a strictness parameter. For Rust projects, the base command stays `cargo clippy --all-targets --` and the flags vary by strictness.

For non-Rust projects, strictness is ignored (eslint, flake8 etc. don't have equivalent clippy groups).

### 2. Parse subcommands in handle_lint

Modify `handle_lint` to accept an optional argument string. Parse:
- No arg → `Default`
- "pedantic" → `Pedantic`
- "strict" → `Strict`
- "fix" → handled separately (task 1)

Pass the strictness to the lint command builder.

### 3. Update repl.rs dispatch

The REPL `/lint` handler needs to pass the argument string through. Change:
```rust
"/lint" => { ... }
```
to check for subcommands by examining the full input after `/lint`.

### 4. Update help text in help.rs

Update the `/lint` help entry to document the new subcommands:
```
/lint              Run project linter (clippy for Rust)
/lint fix          Run linter and auto-fix issues via AI
/lint pedantic     Run with pedantic clippy lints
/lint strict       Run with pedantic + nursery clippy lints
```

### 5. Tests

- Test `lint_command_for_project` with each strictness level
- Verify pedantic adds `-W clippy::pedantic`
- Verify strict adds both pedantic and nursery flags
- Verify non-Rust projects ignore strictness

## Verification

- `cargo build && cargo test`
- Help text shows the new subcommands
- Lint strictness enum is tested
