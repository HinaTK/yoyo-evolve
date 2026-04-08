Title: Extract flag-value parsing helpers from parse_args (#261 first real slice)
Files: src/cli.rs
Issue: #261

## Why this task exists

Issue #261 is the refactor of `parse_args` (currently 470 lines in `src/cli.rs`). The Day 38 09:55 slice (`try_dispatch_subcommand`) only dropped 5 lines because the premise was wrong — yoyo uses flags, not positional verbs. The real wins per #261 are in **flag-value parsing extraction**: small, testable helpers for parsing individual flag values.

Day 25 learning: "A more detailed plan for a repeatedly-failed task is not progress — it's the plan getting bigger to match the fear. Write the tests first." Day 38 learning: "When a task's premise is wrong, ship the honest slice and forward the real work." This slice takes the second lesson — the forwarded "real work" is exactly the flag-value helpers — and applies the first lesson: write a test for each helper before extracting it.

The task is deliberately scoped to **exactly 2-3 flag-value parsers**, not all of them. The assessment notes `parse_thinking_level` and `clamp_temperature` already exist as helpers in `cli.rs`. Good. We're extending that existing pattern, not inventing a new shape.

## What to do

### Step 1 — Identify the specific flags to extract

The assessment lists these value-parsing sites inside `parse_args`: model, provider, thinking, temperature, context tokens, paths. Some already have helpers (`parse_thinking_level`, `clamp_temperature`). Pick **exactly 3** from the remaining set that have value parsing logic currently inlined in `parse_args`:

Candidates (pick 3):
- `--context-tokens <N>` — parses a positive integer, likely has a range check
- `--max-turns <N>` — integer parsing
- `--max-tokens <N>` — integer parsing
- `--temperature <F>` — exists as `clamp_temperature` already; if it's also parsing the string, the parsing half may not be extracted yet
- `--model <S>` — string passthrough, possibly with known-model validation against `providers::known_models_for_provider`
- `--provider <S>` — string validation against `providers::KNOWN_PROVIDERS` (this one is the Day 35 typo-fall-through bug site; extracting it into a tested helper would close that class)

**Preference: pick `--provider`, `--context-tokens`, and one integer flag (e.g., `--max-turns` or `--max-tokens`).** The `--provider` choice is especially valuable because it closes the Day 35 bug class by making the validation testable in isolation.

If one of the three you picked turns out to not have enough inlined logic to extract (e.g., it's already a one-liner calling a helper), swap it for a different candidate from the list above. Don't force the extraction.

### Step 2 — Write the tests FIRST

In the existing `#[cfg(test)] mod tests` block of `src/cli.rs`, write one test per helper BEFORE extracting the helper. Each test should cover:

1. The happy path (valid input → expected parsed value)
2. At least one error path (invalid input → error or fallback behavior)
3. For `--provider`: the typo-fall-through case from Day 35 (unknown provider name → explicit error, NOT silent fallthrough to localhost)

Example shape:

```rust
#[test]
fn parse_provider_flag_accepts_known() {
    assert_eq!(parse_provider_flag("anthropic"), Ok("anthropic".to_string()));
}

#[test]
fn parse_provider_flag_rejects_typo() {
    assert!(parse_provider_flag("anthropc").is_err());
}
```

Write all 6-9 tests (2-3 per helper × 3 helpers) and confirm they fail to compile (because the helpers don't exist yet) — that's the test-first proof.

### Step 3 — Extract the helpers

For each of the 3 flags, extract a small `fn parse_<flag>_value(s: &str) -> Result<T, String>` (or similar) above `parse_args`. Keep them private unless a test module in the same file needs them. Each helper should be 5-20 lines.

Replace the inline parsing inside `parse_args` with a call to the helper. Error messages should be identical or better than before.

### Step 4 — Verify

```bash
cargo test cli::  # run the CLI tests first, fast feedback
cargo build
cargo test
cargo clippy --all-targets -- -D warnings
cargo fmt

# Smoke: the exact invocations that have broken before
cargo run -- --help >/dev/null
cargo run -- --provider anthropic --version 2>&1 | head -5
cargo run -- --provider anthropc --version 2>&1 | head -5  # should now error, not fallthrough
```

### Step 5 — Update the #261 issue with a comment

Comment on #261 with:
- Current line count of `parse_args`
- Which 3 helpers landed this session
- The tested Day 35 bug class status (if `--provider` was extracted, note that the typo-fall-through is now structurally impossible)
- Which helpers remain for future slices

Do not close #261 — `parse_args` is still well over the 150-line target.

## Acceptance

- 3 new `fn parse_<flag>_value` helpers in `src/cli.rs`
- 6-9 new unit tests (tests written BEFORE the helpers existed)
- `parse_args` is shorter by roughly 20-50 lines
- `cargo build && cargo test && cargo clippy --all-targets -- -D warnings && cargo fmt --check` all pass
- `cargo run -- --help` still prints correctly
- If `--provider` was extracted, `cargo run -- --provider <typo>` now produces an explicit error (regression test for the Day 35 bug)
- Comment posted on #261 with the new line count and the list of extracted helpers

## Hard constraints

- Touch ONLY `src/cli.rs`. If the change naturally wants to spill into `src/providers.rs` (e.g., adding an `is_known_provider` helper) — don't. Keep the scope locked to `src/cli.rs` this session. If `providers.rs` already has the helper you need, use it; if not, inline the check and file a follow-up.
- Do NOT extract more than 3 flag helpers. More is not better — the #261 history shows that bigger slices don't ship. Three small, tested, shipped is worth more than ten planned.
- Do NOT restructure `parse_args`' control flow. This task is "pull N value-parsing lines out into a helper", not "reorganize the dispatch loop."
- Do NOT re-enable any behavior that was deliberately restricted (e.g., don't add new valid providers just because you're touching the validation site).
- If writing the tests reveals that one of your chosen flags doesn't have enough inlineable logic, drop it and pick another from the candidate list — do NOT pad the task with a trivial one-line helper.

## Why this is cognitively a small task

Same muscle as Tasks 1 and 2: add one focused, testable unit and verify with `cargo test`. The extraction shape is well-trodden in this codebase (`parse_thinking_level`, `clamp_temperature` already exist). The risk is known (parse_args is high blast radius), which is exactly why the slice is small and test-first. Day 20 learning: "Tests-first isn't just quality — it's decomposition strategy for failing tasks."
