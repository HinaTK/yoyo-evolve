Title: Enrich git status context with changed file names and diff stat
Files: src/context.rs
Issue: none

## Problem

When the agent starts a session, `get_git_status_context()` in `context.rs` tells it:
- Branch name
- Number of uncommitted changes (e.g., "Uncommitted changes: 3 files")
- Number of staged files

But it does NOT tell the agent WHICH files changed. The agent sees "3 files changed" but
doesn't know if it's `src/main.rs`, `README.md`, or `Cargo.toml`. This means the agent
can't proactively reference the user's recent work without first running `git status`.

Claude Code and Aider both provide this context automatically. This is a concrete UX gap
for real developers who start a session mid-work.

## Fix

Enhance `get_git_status_context()` to include:

1. **List of changed file names** from `git status --porcelain`, parsed to show just the
   file paths with their status (M=modified, A=added, D=deleted, ?=untracked).
   Limit to 20 files max to avoid bloating the system prompt.

2. **Staged diff stat** from `git diff --cached --stat` when there are staged files.
   This is a compact one-line-per-file summary showing insertions/deletions.

The output should look like:

```
## Git Status

Branch: main
Uncommitted changes: 3 files
  M src/context.rs
  M src/main.rs
  ? tests/new_test.rs
Staged: 1 file
  M src/cli.rs (+15, -3)
```

## Implementation

In `get_git_status_context()` (around line 40 of context.rs):

After the existing `uncommitted` count, add the actual file list:

```rust
// Show which files are modified (limit to 20 to keep prompt compact)
if uncommitted > 0 {
    if let Ok(status_output) = crate::git::run_git(&["status", "--porcelain"]) {
        let file_lines: Vec<&str> = status_output
            .lines()
            .filter(|l| !l.is_empty())
            .take(20)
            .collect();
        for line in &file_lines {
            result.push_str(&format!("  {}\n", line.trim()));
        }
        if uncommitted > 20 {
            result.push_str(&format!("  ... and {} more\n", uncommitted - 20));
        }
    }
}
```

For staged files, add diff stat:
```rust
if staged > 0 {
    if let Ok(stat_output) = crate::git::run_git(&["diff", "--cached", "--stat", "--stat-width=60"]) {
        // Include just the per-file lines, not the summary
        for line in stat_output.lines() {
            let trimmed = line.trim();
            if !trimmed.is_empty() && trimmed.contains('|') {
                result.push_str(&format!("  {}\n", trimmed));
            }
        }
    }
}
```

## Tests

Add tests verifying:
1. `get_git_status_context()` includes file names when there are uncommitted changes
2. The output format is parseable (contains "M " or "A " or "?" prefixes)
3. The 20-file limit is respected (create a mock scenario or test the truncation logic)
4. Existing tests still pass

Update CLAUDE.md architecture section for context.rs if the description changes.

## Token budget consideration

The git status section adds ~50 chars per changed file. For a typical session with 5-10
changed files, this is 250-500 chars (~60-125 tokens) — negligible compared to the 16K
repo map. The 20-file cap ensures it never exceeds ~1K chars.
