Title: Prep v0.1.9 release — version bump and CHANGELOG
Files: Cargo.toml, CHANGELOG.md
Issue: none

## What

Bump version from 0.1.8 to 0.1.9 in Cargo.toml and write a CHANGELOG.md entry
covering all changes since v0.1.8 (40 commits across Days 49-52).

## Why

40 commits since the last release is substantial. Having the version bump and
changelog ready means the next session can tag and publish if all gates pass.
This also makes `yoyo --version` report accurate information about what's
actually in the binary.

## Changes to document in CHANGELOG

Run `git log --oneline v0.1.8..HEAD` to get the full list. Key changes:

### New features
- `/profile` command — session statistics in a bordered box
- Fuzzy command suggestion (Levenshtein distance) for mistyped slash commands
- Tool output compression — collapses `Compiling` noise into summaries
- Increased live bash output from 3 to 6 trailing lines with hidden line count header

### Shell subcommand wiring
- 5 more shell subcommands: `changelog`, `config`, `permissions`, `todo`, `memories`

### Bug fixes
- Fixed integration tests burning 2.5 minutes per CI run (switched to --print-system-prompt)
- Fixed CWD race condition in repo map tests (eliminated set_current_dir from test suite)
- Fixed flaky test build_repo_map_with_regex_backend

### How

1. Edit `Cargo.toml` line 3: change `version = "0.1.8"` to `version = "0.1.9"`
2. Add a new section at the top of CHANGELOG.md for v0.1.9
3. Verify: `cargo build && cargo test` (version is picked up via env!("CARGO_PKG_VERSION"))

### Verification

- `cargo build` must succeed
- `cargo test` must pass (no tests hardcode the version string)
- After build, `./target/debug/yoyo --version` should show 0.1.9
