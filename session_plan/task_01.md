Title: Fix flaky cwd-racing tests across 3 files
Files: src/setup.rs, src/commands_project.rs, src/commands_search.rs
Issue: none

## Problem

Tests fail intermittently because `std::env::set_current_dir()` is process-global.
Two test sites change cwd during execution:

1. `setup.rs:738` — `test_save_config_to_file` changes cwd to a temp dir, runs the test, then restores. If another test reads `current_dir()` between set and restore, it gets the wrong directory.

2. `commands_git.rs:2148` — `test_handle_undo_last_commit` has a mutex but tests in other modules don't hold the same mutex.

Victim tests (in `commands_project.rs`):
- `test_scan_important_files_in_current_project` (line 1543) — reads `current_dir()`, expects Cargo.toml
- `test_scan_important_dirs_in_current_project` (line 1581) — reads `current_dir()`, expects src/
- `test_detect_project_type_rust` (line 1461) — reads `current_dir()`, expects Rust project
- `test_generate_init_content_rust_project` (line 1691) — reads `current_dir()`, expects Rust project

Victim test (in `commands_search.rs`):
- `build_repo_map_with_regex_backend` (line 2818) — passes `Some("src/")` as root filter but `list_project_files()` (line 82) uses `git ls-files` which is cwd-relative. When cwd changes, git runs in wrong dir and finds no files.

## Fix Strategy

**For `setup.rs::test_save_config_to_file`:** Don't use `set_current_dir`. Instead, write the config file using an explicit path. The `save_config_to_file` function writes to `.yoyo.toml` in cwd — change the test to write to a specific temp path. If `save_config_to_file` doesn't accept a path, either:
- Use the existing `save_config_to_user_file` which takes a path, OR
- Create the temp dir, write `.yoyo.toml` directly to test the content, OR
- Add a path parameter to the internal function

The simplest approach: rewrite the test to call `save_config_to_user_file(provider, model, base_url, &temp_path)` if it exists and tests the same thing, or just manually construct the expected content and verify it matches `generate_config_contents()` output without touching the filesystem at all. Check what `save_config_to_user_file` does — if it writes to a specific file, use it.

**For `commands_project.rs` tests:** Replace `std::env::current_dir().unwrap()` with an explicit path to the project root. Use `env!("CARGO_MANIFEST_DIR")` which is a compile-time constant pointing to the project root — it's immune to cwd changes. Change:
```rust
let cwd = std::env::current_dir().unwrap();
```
to:
```rust
let project_root = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"));
```

This applies to:
- `test_scan_important_files_in_current_project` (line 1544)
- `test_scan_important_dirs_in_current_project` (line 1582)
- `test_detect_project_type_rust` (line 1463)
- `test_generate_init_content_rust_project` (line 1692 area)

**For `commands_search.rs::build_repo_map_with_regex_backend`:** The test calls `build_repo_map_with_backend(Some("src/"), true, true)` but `list_project_files()` internally runs `git ls-files` relative to cwd. Fix: change the test to use the full path `Some(&format!("{}/src/", env!("CARGO_MANIFEST_DIR")))` or restructure the assertion. Actually the issue is that `git ls-files` is cwd-dependent. The simplest fix: if the test returns empty results (because cwd was wrong), use `env!("CARGO_MANIFEST_DIR")` to construct the path. But actually `list_project_files` doesn't accept a root — it always uses cwd. So the fix here is different: we can't change the function signature easily. Instead, add a guard at the start of the test that verifies cwd is correct, or skip if not:

```rust
// Ensure we're in the project root (cwd can race with other tests)
let manifest = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
if std::env::current_dir().unwrap_or_default() != manifest {
    // Another test changed cwd — skip gracefully
    return;
}
```

Or better: just don't assert non-empty if the real fix is in setup.rs (removing the cwd mutation). With the setup.rs fix, the race goes away and this test becomes stable.

## Verification

Run `cargo test` 5 times in a row. All should pass. The previously-flaky tests should be stable:
```bash
for i in $(seq 5); do cargo test 2>&1 | tail -3; echo "---"; done
```
