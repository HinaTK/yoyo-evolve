Title: Extract context.rs from cli.rs — project context loading, file listing, git status
Files: src/context.rs (new), src/cli.rs, src/main.rs
Issue: none

## What

Extract the project context loading subsystem from `cli.rs` into a new `src/context.rs` module. This is the third step in the cli.rs split (after `providers.rs` and `config.rs`).

## Why

After task 1 extracts config.rs (~440 lines), cli.rs will be ~3,200 lines. The project context section is another self-contained block (~195 lines) that handles scanning the working directory for project files, git status, recently changed files, and assembling the project context string. This has nothing to do with CLI argument parsing.

## What to extract

Move these items from `cli.rs` to `src/context.rs`:

1. **`MAX_PROJECT_FILES` constant** — `pub const MAX_PROJECT_FILES: usize = 200;`
2. **`get_project_file_listing()` function** (~20 lines) — runs `git ls-files` or `find` to get file listing
3. **`get_git_status_context()` function** (~35 lines) — runs `git status`, `git branch`, formats context
4. **`get_recently_changed_files()` function** (~25 lines) — git log to find recently changed files
5. **`MAX_RECENT_FILES` constant** — `pub const MAX_RECENT_FILES: usize = 20;`
6. **`load_project_context()` function** (~80 lines) — reads CLAUDE.md/YOYO.md etc, assembles full context
7. **`list_project_context_files()` function** (~15 lines) — lists which context files exist
8. **`PROJECT_CONTEXT_FILES` constant** — `pub const PROJECT_CONTEXT_FILES: &[&str] = &["YOYO.md", "CLAUDE.md", ".yoyo/instructions.md"];`

## What stays in cli.rs

Everything else — Config struct, parse_args, help, banner, update check, etc.

## Important

**This task runs AFTER task 1** which extracts config.rs. The cli.rs you see will already have the config section removed and replaced with re-exports. Work with the file as you find it — don't assume the original line numbers.

## Implementation steps

1. Create `src/context.rs` with the extracted items. It will need:
   - `use std::collections::HashMap;` (if load_project_context uses it)
   - Any filesystem imports the functions need
   - Check what imports the moved functions actually use
2. Add `pub mod context;` to `src/main.rs`
3. In `cli.rs`, replace the moved code with re-exports:
```rust
pub use crate::context::{
    PROJECT_CONTEXT_FILES, MAX_PROJECT_FILES, MAX_RECENT_FILES,
    get_project_file_listing, get_git_status_context,
    get_recently_changed_files, load_project_context, list_project_context_files,
};
```
4. Remove the moved function bodies from `cli.rs`
5. Run `cargo build && cargo test`
6. Run `cargo clippy --all-targets -- -D warnings`

## Update CLAUDE.md

Add `context.rs` to the Architecture section's module list with description:
`context.rs` — project context loading, file listing, git status, recently changed files
