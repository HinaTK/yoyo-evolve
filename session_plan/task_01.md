Title: Fix flaky tests caused by process-global set_current_dir race condition
Files: src/setup.rs, src/commands_project.rs, src/commands_search.rs
Issue: none

## Problem

Three test files have race conditions due to `std::env::set_current_dir()` being process-global. When `cargo test` runs tests in parallel, any test that calls `set_current_dir()` can break any other test that reads `current_dir()` or uses relative paths.

**Confirmed CI failures:** Run 24285461898 had `detect_project_name_from_cargo_toml` and `build_repo_map_with_regex_backend` fail due to this race.

### Affected tests

1. **`setup.rs` line ~735: `test_save_config_to_file`** — Calls `set_current_dir()` to a temp dir, writes `.yoyo.toml`, then restores cwd. No mutex protection. This is a WRITER of the race.

2. **`commands_project.rs` line ~1641: `test_detect_project_name_rust`** — Calls `current_dir()` and asserts it finds "yoyo-agent". This is a READER that races with the writer above.

3. **`commands_search.rs` line ~2818: `build_repo_map_with_regex_backend`** — Calls `build_repo_map_with_backend(Some("src/"), ...)` which resolves `src/` relative to cwd. This is a READER that races with the writer above.

4. **`commands_project.rs` lines 1463, 1544, 1582, 1643, 1692** — Other tests that call `current_dir()`. Check each one.

### Fix Strategy

**For the WRITER (`setup.rs`):** Refactor `save_config_to_file` to accept a `dir: &Path` parameter instead of writing to cwd. Change the function to write to `dir.join(".yoyo.toml")` instead of just `".yoyo.toml"`. Update all callers (search for `save_config_to_file(` across entire codebase — likely in `run_wizard_interactive` and the test itself). The test then passes a `TempDir` directly — no `set_current_dir` needed at all.

**Important:** Check if `run_wizard_interactive` or `run_setup_wizard` calls `save_config_to_file`. If so, update those callers to pass `std::env::current_dir()?` or `&std::env::current_dir().unwrap_or_default()`. The public API change is safe because this is an internal function.

**For the READERS (`commands_project.rs`, `commands_search.rs`):** Replace `std::env::current_dir().unwrap()` with `std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))` in test functions that need to reference the project root. `CARGO_MANIFEST_DIR` is set at compile time by Cargo and always points to the correct project root regardless of runtime cwd.

Specifically:
- `test_detect_project_name_rust`: Change `let cwd = std::env::current_dir().unwrap()` to `let cwd = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))`
- `build_repo_map_with_regex_backend`: Change `build_repo_map_with_backend(Some("src/"), ...)` to use an absolute path: `let src = format!("{}/src/", env!("CARGO_MANIFEST_DIR")); build_repo_map_with_backend(Some(&src), ...)`
- Check ALL other `current_dir()` calls in test functions in `commands_project.rs` (lines 1463, 1544, 1582, 1692) and fix any that assume project-root cwd.

## Verification

1. `cargo build` — must compile clean
2. `cargo test` — all tests pass  
3. `cargo clippy --all-targets -- -D warnings` — no warnings
4. Stress test: run `cargo test -j1 -- test_save_config_to_file test_detect_project_name_rust build_repo_map_with_regex_backend` multiple times
5. Verify no `set_current_dir` remains in `setup.rs` test code (grep for it)

## Notes
- Do NOT delete any existing tests
- Do NOT change any non-test code unless strictly required (the `save_config_to_file` signature change is required)
- The `commands_git.rs` test at line ~2200 already has a CWD_MUTEX pattern — it's fine, leave it alone
- If `save_config_to_file` has too many callers to safely change, use the CWD_MUTEX approach in `setup.rs` instead — but the refactor is preferred because it eliminates the race entirely rather than serializing it
