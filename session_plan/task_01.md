Title: Fix flaky build_repo_map_with_regex_backend test (CWD race)
Files: src/commands_search.rs
Issue: none

## Problem

The test `build_repo_map_with_regex_backend` intermittently fails during parallel test runs.
Root cause: `list_project_files()` calls `run_git(&["ls-files"])` which inherits the process CWD.
When another test calls `set_current_dir()`, the CWD moves and `git ls-files` runs in the wrong directory.

This is the same bug class as the Day 42 fix for setup wizard tests (which used `CARGO_MANIFEST_DIR`).

## Fix

The test itself should be hardened. The approach:

1. In the test `build_repo_map_with_regex_backend`, before calling `build_repo_map_with_backend`,
   set the current directory to `CARGO_MANIFEST_DIR` to ensure we're in the project root.
   Use a guard pattern or just `std::env::set_current_dir` at the start.

   BUT — setting CWD in a test is exactly what causes the race for OTHER tests.
   
   Better approach: The test should verify the function works by checking that when we ARE
   in the right directory, it produces results. The current guard (`manifest_src.is_dir()`)
   already handles the "wrong CWD" case by skipping. The real fix is:

   Option A: Use `#[serial]` from the `serial_test` crate (if available) to prevent parallel execution.
   
   Option B (preferred, no new deps): Change `list_project_files()` to accept an optional
   directory parameter. When `None`, it behaves as today (uses CWD). When `Some(dir)`, it runs
   `git -C <dir> ls-files`. Then the test can pass `CARGO_MANIFEST_DIR` explicitly.
   
   However, Option B changes a function signature used in 4 places and may be too broad for
   one task.
   
   Option C (simplest): Change `list_project_files()` to use `git -C <dir> ls-files` where
   `<dir>` comes from the `CARGO_MANIFEST_DIR` env var at runtime if available, falling back
   to CWD. This makes the function more robust without changing its signature.

   Actually, the cleanest minimal fix: In `list_project_files()`, change the `run_git` call
   to use `git ls-files` with the `-C` flag pointing to the git toplevel. Get the git toplevel
   via `git rev-parse --show-toplevel` and use that. This way the function always operates from
   the repo root regardless of CWD.

## Implementation

In `list_project_files()` (around line 82 of commands_search.rs):

```rust
fn list_project_files() -> Vec<String> {
    // Use git toplevel to avoid CWD-dependency (prevents flaky tests when
    // another test calls set_current_dir during parallel execution).
    if let Ok(toplevel) = crate::git::run_git(&["rev-parse", "--show-toplevel"]) {
        if let Ok(text) = std::process::Command::new("git")
            .args(["-C", &toplevel, "ls-files"])
            .output()
            .map(|o| String::from_utf8_lossy(&o.stdout).to_string())
        {
            let files: Vec<String> = text
                .lines()
                .filter(|l| !l.is_empty())
                .map(|l| l.to_string())
                .collect();
            if !files.is_empty() {
                return files;
            }
        }
    }
    // Fallback: original behavior
    if let Ok(text) = crate::git::run_git(&["ls-files"]) {
        return text
            .lines()
            .filter(|l| !l.is_empty())
            .map(|l| l.to_string())
            .collect();
    }
    walk_directory(".", 8)
}
```

Also add a test that explicitly verifies `list_project_files()` returns results even when
called from a non-repo directory (by comparing against a known file like "Cargo.toml").

Run `cargo test build_repo_map_with_regex_backend -- --test-threads=1` to verify it passes,
then run the full test suite to check for regressions.
