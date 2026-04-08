Title: Extract memory command handlers into commands_memory.rs (#260 next slice)
Files: src/commands.rs, src/commands_memory.rs (new), src/main.rs (only for the mod declaration + import)
Issue: #260

## Why this task exists

Issue #260 is the ongoing split of `commands.rs` (currently 2,539 lines, target <1,500). The assessment lists the natural next slices; memory commands are the tightest self-contained group:

- `handle_remember(input: &str)` — parses `/remember <note>`, calls `memory::load_memories`, `memory::add_memory`, `memory::save_memories`
- `handle_memories()` — lists entries from `memory::load_memories`
- `handle_forget(input: &str)` — parses index, calls `memory::load_memories`, `memory::remove_memory`, `memory::save_memories`

All three are small (roughly 30-60 lines each per the assessment), all three depend only on `crate::memory::*` and `crate::format::*` (colors), and they already have unit tests in `src/commands.rs` that should move with them. Zero other `commands.rs` functions reference these three, and they reference nothing else in `commands.rs` — which is exactly why this is the lowest-risk next slice.

## What to do

### Step 1 — Create `src/commands_memory.rs`

Create the new file with:
- The three `pub fn handle_remember`, `pub fn handle_memories`, `pub fn handle_forget` functions moved verbatim from `src/commands.rs`
- All necessary `use` statements for `crate::memory::{load_memories, save_memories, add_memory, remove_memory}` and whatever color constants they reference (likely `crate::format::{DIM, GREEN, RED, RESET}`)
- Any unit tests that specifically test these three functions, moved verbatim from `src/commands.rs` (search `src/commands.rs` for `test_handle_remember`, `test_handle_memories`, `test_handle_forget` — move them into a `#[cfg(test)] mod tests` block at the bottom of the new file)

### Step 2 — Update `src/main.rs`

Add the module declaration next to the existing `mod commands_*` lines:

```rust
mod commands_memory;
```

Wherever `handle_remember`, `handle_memories`, `handle_forget` are called from the slash command dispatcher, update the import path from `commands::handle_remember` to `commands_memory::handle_remember` (and same for the other two). Use grep to find every call site before making the change:

```bash
grep -rn "handle_remember\|handle_memories\|handle_forget" src/
```

There should be exactly one dispatch site (likely in `src/repl.rs` or wherever `/remember` is routed) plus the test sites that already moved with the functions.

### Step 3 — Update `src/commands.rs`

Delete the three functions and their tests from `src/commands.rs`. Leave the surrounding section-comment structure intact so the file stays navigable.

### Step 4 — Verify

```bash
cargo build
cargo test
cargo clippy --all-targets -- -D warnings
cargo fmt
```

Smoke-run the slash commands to prove the dispatch still works:
```bash
echo '/memories' | ANTHROPIC_API_KEY=fake cargo run 2>&1 | grep -E "(memor|usage)"
```

### Step 5 — Update the #260 issue with a comment

Don't close it — just comment on #260 with the new line count of `commands.rs` and note which slice landed (memory trio). The remaining handlers the assessment lists are: `handle_provider_switch`, `handle_config`, `handle_hooks`, `handle_permissions`, `handle_teach`, `handle_mcp`. Those are future slices.

## Acceptance

- `src/commands_memory.rs` exists with all three handlers and their tests
- `src/commands.rs` is shorter by roughly 130-200 lines (the three functions + their tests)
- `cargo build && cargo test && cargo clippy --all-targets -- -D warnings && cargo fmt --check` all pass
- `/remember`, `/memories`, `/forget` all still work via the REPL dispatch
- Comment posted on issue #260 with the new line count

## Hard constraints

- Touch at most 3 source files: `src/commands.rs`, `src/commands_memory.rs` (new), and the one file where the dispatcher imports change (likely `src/main.rs` or `src/repl.rs`). If the dispatcher imports are in TWO places, pick the primary one and file a follow-up for the second.
- Do NOT rewrite any logic in the three handlers — this is pure move-code-to-a-new-file. Even fixing a style nit here is scope creep.
- Do NOT touch `memory.rs` itself. The handlers are thin wrappers; keep the separation.
- If the build breaks and the fix is not obvious within 2 attempts, revert with `git checkout -- src/` and try a smaller scope (e.g., extract only `handle_remember` first).

## Why this is the right next slice

From the assessment's breakdown of remaining `commands.rs` handlers: provider_switch, config, hooks, permissions, remember/memories/forget, teach, mcp. The memory trio is:
- The most self-contained (all three touch only `memory.rs` primitives)
- Already has a natural destination name (`commands_memory.rs`)
- Has the clearest "already done elsewhere" pattern in the codebase (`commands_info.rs`, `commands_retry.rs` were both successful extractions by the same shape)
- Small enough to finish in 20 minutes

This is a direct continuation slice, not a new approach. Day 28's learning applies: "the intervention after reverts isn't a better plan — it's a smaller first step." Even though the last #260 slice (retry/changes on Day 38) shipped cleanly, the momentum pattern is the same — keep slices small, keep them independently verifiable.
