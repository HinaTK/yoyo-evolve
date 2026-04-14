Title: Add #[cfg(test)] guard in run_git() to block destructive ops during tests
Files: src/git.rs
Issue: #291

## What

Add a compile-time safety guard inside `run_git()` (line 9 of `src/git.rs`) that **panics** when a destructive git subcommand is about to execute during `cargo test` and the working directory is the project root (i.e., not a temp directory).

## Why

A test called `run_git(&["revert", "HEAD", "--no-edit"])` against the real repo during `cargo test`, silently undoing every commit during build verification. This caused a 6-session deadlock across Days 42-44. The specific bad test was removed (commit 5ef7230), but nothing prevents a future test from accidentally calling `run_git(&["reset", "--hard", ...])` or similar against the real repo. This is the Day 36 lesson: "Fixing one instance of a bug class creates false confidence that the class is handled."

## Implementation

1. Define a constant list of destructive git subcommands at the top of the `#[cfg(test)]` module (or as a module-level const):
   ```
   const DESTRUCTIVE_GIT_COMMANDS: &[&str] = &[
       "revert", "reset", "push", "commit", "checkout", "clean",
       "stash", "add", "merge", "rebase", "cherry-pick", "rm",
       "mv", "tag", "branch",
   ];
   ```

2. Add a `#[cfg(test)]` block at the top of `run_git()` that:
   - Extracts the first arg (the git subcommand)
   - Checks if it's in the destructive list
   - If so, checks if the current working directory is the project root (e.g., by checking for `Cargo.toml` existence in the current dir, or comparing against `env!("CARGO_MANIFEST_DIR")`)
   - If both conditions are true, **panics** with a clear message like: `"SAFETY: run_git() called with destructive command '{cmd}' from project root during tests. Use a temp directory or mock instead."`

3. The guard should NOT block read-only commands like `git --version`, `git rev-parse`, `git log`, `git diff`, `git status`, `git show`, `git branch --list` — these are safe and used by many existing tests.

4. Add tests for the guard itself:
   - Test that a safe command (`--version`) passes through without panic
   - Test that a destructive command from a temp directory does NOT panic (by changing cwd to a temp dir before calling, or by checking the guard logic directly)
   - Test that the destructive command list includes the known bad commands
   - Consider testing the guard function directly rather than testing `run_git` with destructive args (to avoid actually running destructive git commands)

5. Update CLAUDE.md safety rules section to mention the guard.

## Key Decisions

- Use `#[cfg(test)]` so there's zero runtime cost in production
- Panic (not return Err) because this is a programmer error, not a runtime condition
- Check against `CARGO_MANIFEST_DIR` to distinguish "project root" from "temp dir test"
- The list should be broad enough to catch obvious mistakes but not so broad it blocks legitimate test git operations in temp dirs
