Title: Enhance tool output compression with command-aware filtering
Files: src/format/mod.rs
Issue: #229 (spirit of the request — reduce token waste on CLI output)

## Problem

Our `compress_tool_output` function does generic compression (strip ANSI, filter test output,
collapse repetitive lines) but doesn't recognize common CLI output patterns that waste tokens.
Issue #229 suggested RTK (Rust Token Killer) which does command-aware output filtering. RTK is
binary-only (no lib.rs), so we can't use it as a dependency. But we can implement the most
impactful filters ourselves.

## What to do

In `src/format/mod.rs`, enhance the compression pipeline by adding a new phase to
`compress_tool_output` that runs command-agnostic pattern filters. Add a function
`filter_noisy_patterns(s: &str) -> String` that strips:

1. **Cargo build metadata lines** — Lines matching:
   - `Compiling <crate> v<version>` (keep the first and last, collapse middle with count)
   - `Downloading <crate> v<version>` (same treatment)
   - `Downloaded N crates (X.X MB) in X.Xs` (keep this summary line)
   - `Blocking waiting for file lock on package cache` (remove entirely)

2. **Progress bars and spinners** — Lines containing:
   - Repeated `━`, `█`, `▓`, `░` characters (>5 in a row → remove the line)
   - `\r` carriage returns followed by overwrite content (keep only the last state)

3. **npm/pip verbose install lines** — Lines matching:
   - `npm warn` (remove unless it contains "deprecated" or "vulnerability")
   - `pip` lines containing "already satisfied" (remove)

4. **Git decoration noise** — In git log output:
   - `commit <40-char-hash>` lines → keep abbreviated `commit <7-char>...`
   - `Author: ...` and `Date: ...` lines → keep but consolidate whitespace

5. **Empty line runs** — Collapse 3+ consecutive empty lines to 2.

Implementation approach:
- Add `filter_noisy_patterns` as a new function
- Call it in `compress_tool_output` between `filter_test_output` and `collapse_repetitive_lines`
- Process line by line with a state machine that tracks "compiling" sequences

Add tests for each pattern:
- Test that 20 `Compiling` lines collapse to first + "... (18 more)" + last
- Test that progress bar lines are stripped
- Test that "already satisfied" pip lines are removed
- Test that 5+ empty lines collapse to 2
- Test that non-matching lines pass through unchanged

## Verification

- `cargo build && cargo test`
- Run: `cargo test filter_noisy` to verify the new tests pass
- The existing `compress_tool_output` tests must still pass
