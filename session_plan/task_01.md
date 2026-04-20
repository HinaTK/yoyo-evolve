Title: Fix flaky test build_repo_map_with_regex_backend (CWD race)
Files: src/commands_map.rs
Issue: none

## Problem

The test `build_repo_map_with_regex_backend` is flaky because `build_repo_map_with_backend` calls 
`std::fs::read_to_string(path)` on relative paths from `git ls-files`. While `list_project_files()` 
already resolves the git toplevel to avoid CWD dependency, the file paths returned are still relative 
to the repo root. When a parallel test calls `set_current_dir()`, those relative `read_to_string` calls 
break.

The current skip guard (`if !Path::new("src").is_dir()`) sometimes loses the race.

## Fix

In `build_repo_map_with_backend`, resolve file paths against the git toplevel directory so that 
`read_to_string` uses absolute paths. This is the same pattern used in `list_project_files()`:

1. At the start of `build_repo_map_with_backend`, get the git toplevel via `run_git(&["rev-parse", "--show-toplevel"])`.
2. When reading files, if we have a toplevel, join it with the relative path: `Path::new(&toplevel).join(path)`.
3. The `root` filter comparison stays relative (since `list_project_files` returns relative paths), 
   but the actual `read_to_string` call uses the absolute path.

Then update the test:
- Remove the fragile `if !Path::new("src").is_dir() { return; }` skip guard since it's no longer needed.
- The test should work reliably regardless of CWD because all file I/O uses absolute paths.

## Verification

- `cargo test build_repo_map_with_regex_backend` should pass consistently
- `cargo test` full suite should pass
- `cargo clippy --all-targets -- -D warnings` should pass
