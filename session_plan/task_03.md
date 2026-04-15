Title: Extract /map into commands_map.rs from commands_search.rs
Files: src/commands_map.rs (new), src/commands_search.rs, src/commands.rs
Issue: none

## What

Extract the `/map` section (~2,413 lines) from `commands_search.rs` (3,120 lines) into a new `commands_map.rs` module. This is structural health work flagged by the assessment: "commands_search.rs contains multiple distinct features (find, index, grep, ast-grep, map) that could be separate modules."

After extraction:
- `commands_search.rs`: ~700 lines (find, index, grep, ast-grep)  
- `commands_map.rs`: ~2,413 lines (map, symbol extraction, repo map)

## Implementation

### 1. Create `src/commands_map.rs`

Move everything from line 708 (the `// ── /map` section marker) to the end of `commands_search.rs` (excluding tests for map) into a new file `src/commands_map.rs`.

This includes:
- `SymbolKind` enum
- `Symbol` struct
- `FileSymbols` struct
- `detect_language()` function
- `extract_symbols()` function
- `parse_ast_grep_symbols()` function
- `extract_symbols_ast_grep()` function
- `MapBackend` enum
- `build_repo_map()` function
- `build_repo_map_with_backend()` function
- `format_repo_map_colored()` function
- `format_repo_map()` function
- `generate_repo_map_for_prompt_with_limit()` function
- `generate_repo_map_for_prompt()` function
- `handle_map()` function

Add the necessary imports at the top:
```rust
use crate::format::*;
use regex::Regex;
use std::path::Path;
```

**Dependency:** The `/map` code uses `list_project_files()` which is defined in `commands_search.rs`. Make `list_project_files()` `pub(crate)` in `commands_search.rs` so `commands_map.rs` can import it via `use crate::commands_search::list_project_files;`.

### 2. Update `src/commands_search.rs`

- Remove the entire `/map` section (lines 708 to end of non-test code)
- Make `list_project_files()` `pub(crate)` (change from `fn` to `pub(crate) fn`)
- Move map-related tests to `commands_map.rs`
- Keep find, index, grep, ast-grep sections and their tests

### 3. Update `src/commands.rs`

Change the re-export line:
```rust
pub use crate::commands_search::{
    handle_ast_grep, handle_find, handle_grep, handle_index, handle_map,
};
```
to:
```rust
pub use crate::commands_search::{
    handle_ast_grep, handle_find, handle_grep, handle_index,
};
pub use crate::commands_map::handle_map;
```

Also update any other imports that reference map types from commands_search.

### 4. Add mod declaration (one-line change)

Add `mod commands_map;` to `src/main.rs` alongside the other module declarations. This is a required wiring change — just one line.

### Tests

All existing tests for /map functionality should be moved to `commands_map.rs` and must pass unchanged. Run `cargo test` and `cargo clippy --all-targets -- -D warnings` to verify.

Key map-related tests to look for in the test module at the bottom of `commands_search.rs`:
- Tests for `detect_language`
- Tests for `extract_symbols`
- Tests for `build_repo_map`
- Tests for `format_repo_map`
- Tests for `generate_repo_map_for_prompt`

### Verification

```bash
cargo build && cargo test && cargo clippy --all-targets -- -D warnings
```

After extraction, verify:
- `commands_search.rs` is ~700 lines (find + index + grep + ast-grep)
- `commands_map.rs` is ~2,400 lines (map + symbols)
- All tests pass
- No clippy warnings

### Notes

This is a pure mechanical extraction — no behavioral changes. The only API change is making `list_project_files()` pub(crate). No docs updates needed since no user-facing behavior changes.
