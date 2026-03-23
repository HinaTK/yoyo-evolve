Title: Add git status context to system prompt for persistent awareness
Files: src/cli.rs
Issue: none

## Context

Claude Code automatically includes git context (current branch, uncommitted changes) in its system prompt so the agent always knows the state of the working tree. yoyo already injects project files, recently changed files, and project memories into the system prompt via `load_project_context()`. But it doesn't include the current git branch or whether there are uncommitted changes. This means the agent has to run `git status` as a tool call every time it needs to know git state, wasting a turn.

## Implementation

1. **Add `get_git_status_context()` function** in `src/cli.rs`:
   ```rust
   /// Get a brief git status summary for system prompt injection.
   /// Returns None if not in a git repo.
   fn get_git_status_context() -> Option<String> {
   ```
   This function should:
   - Get current branch via `git rev-parse --abbrev-ref HEAD`
   - Get count of uncommitted changes via `git status --porcelain` (count non-empty lines)
   - Get count of staged changes via `git diff --cached --name-only` (count non-empty lines)
   - Format as a brief string like:
     ```
     ## Git Status
     
     Branch: main
     Uncommitted changes: 3 files
     Staged: 1 file
     ```
   - If no changes, just show the branch name
   - Return None if git commands fail (not in a repo)

2. **Call it from `load_project_context()`** — add the git status section after the recently changed files section but before project memories. It should be concise (3-4 lines max).

3. **Add a log line** like the others: `context: git status (branch: main)`

4. **Tests**:
   - `test_get_git_status_context_in_repo` — since we're in a git repo, this should return Some with a string containing "Branch:"
   - `test_get_git_status_context_contains_branch` — verify the output contains the branch name
   - `test_git_status_context_format` — verify the format includes "## Git Status" header
   - `test_load_project_context_includes_git_status` — verify `load_project_context()` result contains "Git Status" when in a git repo

This is a small change (maybe 40 lines) but it means the agent always knows what branch it's on and whether there are pending changes, without needing a tool call. Real developers expect this awareness from their coding tools.
