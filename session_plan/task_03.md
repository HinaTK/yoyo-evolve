Title: Eliminate set_current_dir in test suite (systemic CWD race fix)
Files: src/commands_config.rs, src/commands_session.rs
Issue: none

## Problem

The assessment identified 18+ call sites using `set_current_dir` in tests. This is global mutable 
state shared across all parallel test threads. Even with save/restore patterns, there's a race 
window between set and restore where other tests can observe the wrong CWD.

Task 01 fixes the immediate flaky test in `commands_map.rs`. This task eliminates `set_current_dir` 
from two more files that use the save/restore antipattern.

## Files to fix

### `src/commands_config.rs` (~line 986, 1025)
Tests that use `set_current_dir(&tmp)` + restore. These tests need a temporary directory to test 
config loading. Fix: instead of changing CWD, pass the path explicitly or test the functions with 
absolute paths to the temp dir.

### `src/commands_session.rs` (~lines 773-828)
Tests that use `set_current_dir(&tmp_dir)` + restore. These tests need a working directory for 
session file operations. Fix: use absolute paths to the temp dir instead of changing CWD.

## Approach

For each test:
1. Read the test to understand what it's actually testing
2. Identify which function requires the CWD to be set vs which can work with absolute paths
3. If the function under test requires CWD (e.g., it uses `.` or relative paths internally), 
   wrap the test body in a `std::process::Command::new(env!("CARGO_TARGET_TMPDIR"))` approach, 
   OR refactor the function to accept a root path parameter
4. If the function already accepts path parameters, just pass the absolute temp dir path

The key principle: **never call `set_current_dir` in tests**. Use absolute paths or pass root 
directories as parameters.

## Verification

- `cargo test` full suite passes
- `grep -rn "set_current_dir" src/commands_config.rs src/commands_session.rs` returns 0 results
- `cargo clippy --all-targets -- -D warnings` passes
