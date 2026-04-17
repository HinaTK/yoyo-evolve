Title: Clean up #[allow(unused_*)] annotations and dead code
Files: src/cli.rs, src/commands.rs, src/commands_dev.rs
Issue: none (self-discovered code hygiene from assessment)

## Problem

The assessment found 3 `#[allow(unused_*)]` annotations that may indicate dead code:

1. `src/cli.rs` line 55: `#[allow(unused_imports)]`
2. `src/commands.rs` line 16: `#[allow(unused_imports)]`
3. `src/commands_dev.rs` line 634: `#[allow(unused_mut)]`

These annotations silence compiler warnings. If the code they protect is actually unused,
the annotation is hiding dead code that should be removed. If the code IS used (e.g., used
only under certain cfg conditions), the annotation may be legitimate but should be narrowed
to the specific item rather than blanket-suppressing.

## Implementation

For each annotation:

1. **Remove the `#[allow(...)]` annotation temporarily** and run `cargo build` to see the
   actual warning. This tells you exactly what's unused.

2. **If the import/variable IS unused:**
   - Remove the unused import or dead code entirely.
   - Don't add the allow back.

3. **If the import/variable IS used** (e.g., only in tests, or only under cfg):
   - Narrow the allow to just the specific item: `#[allow(unused_imports)]` on the specific
     `use` line, or use `#[cfg(test)]` if it's test-only.
   - Or restructure so the allow isn't needed (e.g., move test-only imports inside `#[cfg(test)]`
     blocks).

4. After cleaning all three, run `cargo clippy --all-targets -- -D warnings` to verify
   no new warnings are introduced.

## Verification

- `cargo build && cargo test`
- `cargo clippy --all-targets -- -D warnings` (must be clean)
- `cargo fmt -- --check` (must be clean)
- No `#[allow(unused_*)]` annotations remain unless they're genuinely necessary with a
  comment explaining why.
