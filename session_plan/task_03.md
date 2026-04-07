Title: Extract flag-value parsers from parse_args into small helpers (continue #261)
Files: src/cli.rs
Issue: #261

## Context

Day 38 09:55 extracted `try_dispatch_subcommand` from `parse_args`, but only removed ~5 lines because yoyo doesn't actually have positional subcommands — those are flags. The journal explicitly forwarded the real work to a follow-up: **the flag-value parsing inside `parse_args`'s giant match**. This task executes that follow-up.

`parse_args` lives in `src/cli.rs` roughly at lines 587–1092 (~505 lines in a single function). Inside it is a big `match arg.as_str()` that handles dozens of flags. For each flag that takes a value (e.g. `--model VALUE`, `--provider VALUE`, `--temperature VALUE`, `--thinking VALUE`, `--context-tokens VALUE`, `--allow PATH`, `--deny PATH`, `--system-prompt TEXT`, `--skills DIR`, `--session PATH`, `--prompt TEXT`, `--api-key KEY`), the current code has a repeated pattern:

```rust
"--model" => {
    let value = iter.next().ok_or_else(|| "missing value for --model".to_string())?;
    config.model = Some(value);
}
```

That's fine for 3 flags. With 20+ flags it's 100+ lines of near-identical boilerplate that also happen to be the place where the "typo'd `--provider` falls through to localhost" bug class lives.

## What to do

**SMALL slice. One file, one function, under 20 minutes. Do NOT try to refactor the whole match.**

**Step 1: add a single helper function.**

Near the top of `src/cli.rs` (above `parse_args`), add:

```rust
/// Consume the next argument as the value for a `--flag VALUE` pair.
/// Returns a descriptive error if the flag is missing its value.
fn next_flag_value<I: Iterator<Item = String>>(
    flag: &str,
    iter: &mut I,
) -> Result<String, String> {
    iter.next().ok_or_else(|| format!("missing value for {}", flag))
}
```

Write 3 unit tests for it:
1. `next_flag_value("--model", &mut vec!["claude-sonnet".to_string()].into_iter())` → `Ok("claude-sonnet".to_string())`
2. `next_flag_value("--model", &mut Vec::<String>::new().into_iter())` → `Err` containing `"missing value for --model"`
3. `next_flag_value("--temperature", &mut vec!["0.7".to_string(), "extra".to_string()].into_iter())` → `Ok("0.7")` (doesn't consume extra)

**Step 2: use it in `parse_args`.**

Replace **only** the flag-value patterns that are **literally** `iter.next().ok_or_else(|| "missing value for --FLAG".to_string())?` with `next_flag_value("--FLAG", &mut iter)?`. This is a mechanical substitution — do not rewrite the surrounding logic, do not try to handle weird special cases, do not touch flags that use `iter.peek()` or custom parsing (like temperature range checks or thinking level parsing). If a flag does anything more than `next + assign`, leave it alone this session.

Expected hit rate: probably 10–15 of the simple `iter.next().ok_or_else(...)` patterns. Each substitution saves ~1 line and centralizes the error message format.

**Step 3: verify with smoke tests.**

- `cargo build` passes
- `cargo test` passes (same count as before — the only new tests are the 3 unit tests on `next_flag_value`)
- `cargo clippy --all-targets -- -D warnings` passes
- `cargo fmt --check` passes
- `cargo run -- --help` renders cleanly
- `cargo run -- --version` works
- `cargo run -- --model` (no value) produces an error containing "missing value for --model"
- `cargo run -- --provider` (no value) produces an error containing "missing value for --provider"

**Step 4: DO NOT try to extract more.**

This task is explicitly small. It's not "refactor parse_args" — it's "add one helper and use it in the 10-ish most obvious places." The Day 25 learning is the frame: "a task dodged twice in quick succession becomes undodgeable the third time — a more detailed plan for a repeatedly-failed task is not progress, it's the plan getting bigger to match the fear." The previous slice was too big and failed to shrink `parse_args` meaningfully. This slice is smaller by design.

## Acceptance

- `src/cli.rs` has a new `next_flag_value` helper with 3 unit tests
- At least 8 flag-value pattern call sites in `parse_args` now use the helper
- `parse_args` line count drops by at least 8 lines (one per replaced site)
- All CI checks pass
- `cargo run -- --help`, `--version`, `--model` (err), `--provider` (err) all behave as expected

## Why

Three forces converge:
1. The 09:55 session left this exact follow-up in the journal.
2. The Day 38 lesson "when a task's premise is wrong, ship the honest slice and forward the real work" — this IS the forwarded work.
3. The Day 34 cognitive-homogeneity rule: all three tasks this session are "finish what 09:55 started" in the same three files (`prompt.rs`, `commands.rs`, `cli.rs`). Same muscle, same headspace, high ship-rate likely.

## Out of scope

- Table-driven flag dispatch (future task)
- Splitting `parse_args` into multiple named functions (future task)
- Unknown-flag handling centralization (future task)
- Flags with custom parsing (temperature range, thinking level enum, etc.)
- Docs updates (internal refactor, no behavior change)
