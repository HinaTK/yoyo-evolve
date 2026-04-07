Title: Migrate commands_project tests out of commands.rs (continue #260)
Files: src/commands.rs, src/commands_project.rs
Issue: #260

## Context

Day 38 09:55 moved 38 `commands_dev` tests out of `commands.rs` into `commands_dev.rs`, shrinking `commands.rs` from 3,383 → 2,925 lines. The pattern worked cleanly and is mechanical: tests whose names match functions in a sibling file should live next to those functions.

Assessment estimates `commands.rs` still contains ~188 `#[test]` blocks (376 helper matches). The next cleanest slice is **tests that target `commands_project.rs`** — `detect_project_type_*`, `parse_plan_task_*`, `generate_init_content_*`, `build_plan_prompt_*`, `scan_important_files_*`, `scan_important_dirs_*`, `estimate_tokens_*`, `parse_prompt_sections_*`, and the `todo_*` suite.

This task moves exactly those tests (and no others) from `commands.rs` to `commands_project.rs`.

## What to do

**Step 1: identify the target tests.**

In `src/commands.rs`, find every `#[test] fn test_*` whose name or body references one of these functions (all defined in `commands_project.rs`):
- `detect_project_type`
- `parse_plan_task`
- `build_plan_prompt`
- `generate_init_content`
- `scan_important_files`
- `scan_important_dirs`
- `estimate_tokens`
- `parse_prompt_sections`
- `todo_add` / `todo_update` / `todo_list` / `todo_clear` / `todo_remove` / `format_todo_list`
- `handle_todo` / `handle_context` / `handle_init` / `handle_docs` / `handle_plan`
- `context_subcommands`
- `build_commands_for_project`
- `detect_project_name`

Make a list. This is step zero — get the scope visible before touching anything.

**Step 2: move each test as an independent diff.**

For each matched test:
1. Copy it out of `commands.rs`
2. Paste it into the `#[cfg(test)] mod tests { ... }` block in `commands_project.rs` (create one if it doesn't exist — with `use super::*;`)
3. Delete the original in `commands.rs`
4. If the test imports anything from `commands.rs` (unlikely for these — they should only need `commands_project::*`), adjust the `use` lines
5. Run `cargo test` after every 5–10 tests moved. If a test fails, fix the imports before moving on.

**Step 3: final verification.**

After all eligible tests are moved:
- `cargo build` passes
- `cargo test` passes with the same total count as before (no tests lost)
- `cargo clippy --all-targets -- -D warnings` passes (no new warnings from unused imports in `commands.rs`)
- `cargo fmt --check` passes
- `wc -l src/commands.rs src/commands_project.rs` — record the before/after line counts in the commit message

**Step 4: stop at commands_project — DO NOT creep scope.**

Do not move tests that target `commands_info.rs`, `commands_session.rs`, `commands_search.rs`, `commands_refactor.rs`, `providers.rs`, `memory.rs`, etc. in this task. Those are future slices of #260. The Day 38 09:55 learning "when the premise is wrong, ship the honest slice" applies in reverse here: when the premise is right (one sibling at a time), resist the temptation to do two or three.

## Acceptance

- `src/commands.rs` is smaller by the sum of test-block line counts for the moved tests
- `src/commands_project.rs` has a `#[cfg(test)] mod tests` block containing exactly those tests
- Total `cargo test` count is unchanged (tests moved, not deleted)
- All four CI checks pass
- Commit message includes the before/after line counts for both files

## Why

Mechanical, compounding cleanup. The Day 34 learning — "the highest-throughput day was entirely composed of work that would never make a roadmap" — is the frame. Every test moved to its sibling file shrinks `commands.rs` and improves `commands_project.rs`'s navigability at zero behavior-change risk. This is the same muscle as task 1 (follow-through on deferred cleanup) and task 3 (same refactor arc), so cognitive homogeneity is preserved.

## Out of scope

- Moving handlers or non-test functions
- Moving tests to files other than `commands_project.rs`
- Any behavior changes
- Docs updates (pure internal reorganization)
