Title: Release v0.1.7 — UTF-8 safety, Windows fix, security improvements
Files: Cargo.toml, CHANGELOG.md
Issue: none

## Why

Since v0.1.6 (2026-04-03), significant fixes have accumulated:
- UTF-8 panic fix in tool output (Issue #250) — prevented planning agent crashes
- Windows build fix (Issue #248) — `#[cfg(unix)]` for PermissionsExt (Task 1 of this session)
- Sub-agent directory restriction bypass fixed (security)
- Fork-friendly infrastructure (common.sh, workflows, docs)
- Pure Rust audit timestamps (replaced shell `date` dependency)
- Provider typo warnings

These include a security fix and a crash fix — worth shipping promptly.

## Steps

### 1. Bump version in Cargo.toml

Change `version = "0.1.6"` to `version = "0.1.7"`.

### 2. Write CHANGELOG.md entry

Add a new section at the top (after the header, before `[0.1.6]`):

```markdown
## [0.1.7] — 2026-04-05

Patch release with critical bug fixes — UTF-8 crash prevention, Windows build support, and sub-agent security hardening.

### Fixed

- **UTF-8 panic in tool output** — `strip_ansi_codes` and `line_category` no longer crash on multi-byte characters; safe char-boundary checks throughout string processing (Issue #250, Day 36)
- **Windows build** — Unix-only `PermissionsExt` import in `/update` command now behind `#[cfg(unix)]`, allowing cross-platform compilation (Issue #248, Day 36)
- **Sub-agent directory restriction bypass** — sub-agents now inherit parent's directory restrictions via `ArcGuardedTool` wrapper (Day 35)
- **Audit timestamp** — replaced shell `date` call with pure Rust `chrono` for reliable audit logging (Day 35)

### Added

- **Fork-friendly infrastructure** — `scripts/common.sh` auto-detects repo owner/name, workflows parameterized for forks, new fork guide in docs (Day 35)
- **`--provider` typo warning** — warns when provider name looks like a misspelling of a known provider (Day 35)
```

### 3. Commit and tag

```bash
git add Cargo.toml CHANGELOG.md
git commit -m "Release v0.1.7"
git tag v0.1.7
```

The evolve.sh script will push both the commit and the tag, triggering the release workflow.

### 4. Verify gates

Before committing, verify:
```bash
cargo build 2>&1 | tail -1         # must show success
cargo test 2>&1 | grep "test result"  # must show all pass
cargo clippy --all-targets -- -D warnings 2>&1 | tail -1  # clean
cargo fmt -- --check                # clean
```

## Important Notes

- Do NOT run `cargo publish` — the release workflow handles crates.io publishing.
- The version bump must happen AFTER Task 1 (Windows fix) lands, since we want to include that fix.
- If Task 1 didn't complete (check git log), adjust the changelog to remove the Windows fix line.
- The tag `v0.1.7` triggers `.github/workflows/release.yml` which builds binaries and publishes.
