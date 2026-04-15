Title: /lint unsafe — scan for unsafe blocks and suggest safety attributes
Files: src/commands_dev.rs, src/help.rs
Issue: #294

## What

Issue #294 specifically mentions `#![forbid(unsafe_code)]` as part of Rust's static analysis ecosystem. No other CLI coding agent offers project-wide unsafe code detection as part of its lint pipeline. This is a differentiating feature.

Add `/lint unsafe` subcommand that:
1. Scans all `.rs` files in the project for `unsafe` blocks/functions
2. Checks whether `#![deny(unsafe_code)]` or `#![forbid(unsafe_code)]` is set in the crate root
3. Reports findings with file:line references
4. Suggests adding the appropriate attribute if missing

## Changes

### 1. Add `handle_lint_unsafe` function in commands_dev.rs

Create a function that:
- Finds all `.rs` files in `src/` (using `walkdir` or simple glob via `std::fs`)
- Scans each file for lines containing `unsafe {` or `unsafe fn` (simple text search, not full parsing)
- Checks `src/main.rs` and `src/lib.rs` for `#![deny(unsafe_code)]` or `#![forbid(unsafe_code)]`
- Prints a report:
  - If no unsafe found and attribute present: "✓ No unsafe code, #![forbid(unsafe_code)] active"
  - If unsafe found: lists each occurrence with file:line
  - If no attribute set: suggests adding `#![deny(unsafe_code)]`
- Returns `Option<String>` summary for agent context

Important: Use only `std::fs` for file scanning — no new dependencies.

### 2. Wire into the REPL

The `/lint unsafe` subcommand should be handled in the same dispatch as `/lint`, `/lint fix`, `/lint pedantic`, etc. (from task 2's subcommand parsing).

### 3. Update help text in help.rs

Add `/lint unsafe` to the help entry:
```
/lint unsafe       Scan for unsafe code blocks and suggest safety attributes
```

### 4. Tests

- Test scanning a mock directory with known unsafe blocks
- Test detection of `#![deny(unsafe_code)]` attribute
- Test the case where no unsafe code exists

## Why (self-driven)

This is a differentiating feature. No other CLI agent (Claude Code, Codex, Aider) offers built-in unsafe code auditing as part of linting. It demonstrates deep Rust understanding and gives users a unique reason to choose yoyo for Rust projects. It directly fulfills the spirit of Issue #294's request for deeper static analysis integration.

## Verification

- `cargo build && cargo test`
- Running `/lint unsafe` on yoyo's own codebase should find the `unsafe` blocks in tests and main.rs
