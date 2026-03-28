Title: Split format.rs into sub-modules
Files: src/format.rs, src/format/ (new directory), src/main.rs
Issue: none

## Context

`format.rs` is 6,916 lines — by far the largest module and still growing. It contains at least five distinct concerns crammed into one file:
1. ANSI color constants and utilities
2. Markdown rendering (the `MarkdownRenderer` and related types)
3. Cost/token display formatting
4. Streaming output renderer
5. Tool output summaries and formatting helpers

Splitting it into a `format/` module directory with focused sub-modules improves navigability and makes it easier to work on any one concern without loading 7K lines of context.

## Implementation

### 1. Create directory structure

```
src/format/
  mod.rs          — re-exports, shared types, ANSI color constants
  markdown.rs     — MarkdownRenderer, markdown-to-ANSI conversion
  cost.rs         — cost formatting, token stats display
  streaming.rs    — streaming output renderer (StreamRenderer or similar)
  tools.rs        — tool output summaries, truncation helpers
```

### 2. Move code

Read `src/format.rs` and identify the natural boundaries. Look for:
- `struct MarkdownRenderer` and all its `impl` blocks → `markdown.rs`
- Cost-related functions (anything with "cost", "token", "usage" in the name) → `cost.rs`
- `StreamRenderer` or streaming-related structs → `streaming.rs`
- Tool summary functions (tool_use_summary, format_tool_result, etc.) → `tools.rs`
- ANSI constants, `pluralize()`, `truncate_with_ellipsis()`, and other small utilities → `mod.rs`

### 3. Re-export from mod.rs

In `src/format/mod.rs`, add:
```rust
mod markdown;
mod cost;
mod streaming;
mod tools;

pub use markdown::*;
pub use cost::*;
pub use streaming::*;
pub use tools::*;
```

This preserves the existing public API — all other files that `use crate::format::*` continue to work unchanged.

### 4. Update src/main.rs (and others)

The `mod format;` declaration in whatever root module declares it should work unchanged because Rust's module system supports both `format.rs` and `format/mod.rs` automatically.

Check all files that import from format:
```bash
grep -rn "use crate::format" src/
grep -rn "crate::format::" src/
```

Make sure all public items are still accessible through the same paths.

### 5. Verify

Run `cargo build && cargo test && cargo clippy --all-targets -- -D warnings` at each step.

## Important notes

- This is a pure refactor — no behavior changes, no new features
- Every public function/struct/const must remain accessible at `crate::format::*`
- Don't rename anything — just move
- If any test references `format.rs` by path (e.g., in file assertions), update those
- The line count per sub-module should be roughly: mod.rs (~500), markdown.rs (~2500), cost.rs (~1000), streaming.rs (~1500), tools.rs (~1400). Adjust based on what you find.
- If the split is proving too complex or risky (too many cross-dependencies between the sub-modules), abort and note what blocked it. A clean build is more important than a clean split.
