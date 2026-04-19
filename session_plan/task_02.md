Title: Release v0.1.8 — Day 50 milestone release
Files: Cargo.toml, CHANGELOG.md, CLAUDE_CODE_GAP.md
Issue: none

## Context

51 commits have accumulated since v0.1.7 (Day 36, 2026-04-05). That's 14 days of
unreleased work spanning Days 36-49. Day 50 is the right milestone for a release.

Key changes since v0.1.7:
- `/bg` background process management (Day 45)
- `/blame` with colorized output (Day 48)
- Proper unified diffs (LCS-based) for edit_file operations (Day 48) 
- `/lint fix`, `/lint pedantic`, `/lint strict`, `/lint unsafe` subcommands (Day 46)
- Per-command bash timeout parameter (Day 44)
- Co-authored-by trailer on `/commit` (Day 43)
- `/status` shows session elapsed time + turn count (Day 43)
- `/changelog` command (Day 44)
- Piped mode handles `/slash` input gracefully (Day 47)
- 23 shell subcommands wired (Days 48-49): help, version, setup, init, diff, commit,
  review, blame, grep, find, index, lint, test, doctor, map, tree, run, watch, 
  status, undo, docs, update, pr
- Comprehensive categorized help with 68+ REPL commands listed (Day 49)
- Dead code cleanup (Day 48)
- Destructive-git-command guard in `run_git()` for test safety (Day 45)
- Streaming output for `/run` and `/watch` (Day 45)

## Implementation

### Step 1: Bump version in Cargo.toml

Change `version = "0.1.7"` to `version = "0.1.8"`.

### Step 2: Update VERSION constant in src/cli.rs

Find `const VERSION: &str = "0.1.7"` and change to `"0.1.8"`.

### Step 3: Write CHANGELOG.md entry

Add a new `## [0.1.8] — 2026-04-19` section at the top (after the header),
following the existing format. Organize into:

**Added:**
- `/bg` background process management (launch, list, view, kill)
- `/blame` with colorized git blame output  
- `/changelog` for recent evolution history
- `/lint fix` — auto-fix lint warnings
- `/lint pedantic` — extra-strict lint pass
- `/lint strict` — deny all warnings during lint
- `/lint unsafe` — scan for unsafe code usage
- 23 shell subcommands (help, version, grep, diff, tree, lint, test, doctor, etc.)
- Per-command bash timeout parameter (1-600 seconds)
- Co-authored-by trailer on `/commit`

**Improved:**
- Proper unified diffs (LCS-based) for edit_file operations
- Comprehensive categorized help listing all 68+ REPL commands
- Piped mode gracefully handles slash-command input
- Streaming output for `/run` and `/watch`
- `/status` shows session elapsed time and turn count

**Fixed:**
- Dead code and unused annotation cleanup
- Destructive-git-command guard in `run_git()` prevents test-suite repo mutation

### Step 4: Update CLAUDE_CODE_GAP.md stats

Update the "Stats" section near the bottom to reflect Day 50 numbers:
- ~49,157 lines of Rust across 35 source files
- 1,972 tests (1,887 unit + 85 integration)
- ~68+ REPL commands, 23 shell subcommands
- 14 provider backends

### Step 5: Create git tag

After committing, create the tag: `git tag v0.1.8`

NOTE: Do NOT run `cargo publish` — the release workflow handles that automatically
when the tag is pushed.

## Verification

```bash
cargo build && cargo test
grep "0.1.8" Cargo.toml
grep "0.1.8" src/cli.rs
grep "0.1.8" CHANGELOG.md
```

## Important

- This task modifies Cargo.toml which affects Cargo.lock — run `cargo build` to
  regenerate it and include both in the commit.
- The VERSION constant in cli.rs must match the Cargo.toml version.
- Do NOT create the git tag in tests — only in the final commit step.
