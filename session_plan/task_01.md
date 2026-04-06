Title: Extract config.rs from cli.rs — permissions, directory restrictions, MCP config parsing
Files: src/config.rs (new), src/cli.rs, src/main.rs
Issue: none

## What

Extract the configuration parsing subsystem from `cli.rs` into a new `src/config.rs` module. This is the second step in the cli.rs split (after `providers.rs` was extracted in the previous session).

## Why

`cli.rs` is 3,657 lines — still the largest file. The config parsing section (permissions, directory restrictions, MCP server config, TOML parsing helpers) is a self-contained ~440-line block that has no business living in the CLI argument parser. Extracting it improves navigability and follows the same pattern used for the `providers.rs` extraction.

## What to extract

Move these items from `cli.rs` to `src/config.rs`:

1. **`PermissionConfig` struct + impl** (~120 lines) — the struct, its `check()` and `is_empty()` methods
2. **`DirectoryRestrictions` struct + impl** (~90 lines) — the struct, `is_empty()`, `check_path()`, helper fns `resolve_path()` and `path_is_under()`
3. **`McpServerConfig` struct** (~10 lines)
4. **`glob_match()` function** (~40 lines)
5. **`parse_toml_array()` function** (~25 lines)
6. **`parse_permissions_from_config()` function** (~30 lines)
7. **`parse_directories_from_config()` function** (~40 lines)
8. **`parse_mcp_servers_from_config()` function** (~95 lines) — including helper fns `strip_quotes()` and `parse_inline_table()`

## What stays in cli.rs

- `Config` struct (it references `PermissionConfig`, `DirectoryRestrictions`, `McpServerConfig` — just import them)
- `parse_args()` — it calls the config parsing functions
- `parse_config_file()` — general key-value config parsing
- Everything else (context loading, help, banner, etc.)

## Implementation steps

1. Create `src/config.rs` with the extracted items
2. Add `pub mod config;` to `src/main.rs`
3. In `cli.rs`, replace the moved code with `pub use crate::config::*;` re-exports (same pattern as providers.rs extraction) so all existing `use crate::cli::` imports throughout the codebase continue working
4. Remove the moved function bodies from `cli.rs` (keep the re-exports)
5. Run `cargo build && cargo test` to verify
6. Run `cargo clippy --all-targets -- -D warnings` to verify no warnings

## Key constraint

Use the SAME re-export pattern as the providers.rs extraction:
```rust
// In cli.rs, replace the moved items with:
pub use crate::config::{
    PermissionConfig, DirectoryRestrictions, McpServerConfig,
    glob_match, parse_toml_array, parse_permissions_from_config,
    parse_directories_from_config, parse_mcp_servers_from_config,
};
```

This ensures zero breakage for any file that does `use crate::cli::PermissionConfig` etc.

## Update CLAUDE.md

Add `config.rs` to the Architecture section's module list with description:
`config.rs` — permission config, directory restrictions, MCP server config, TOML parsing helpers
