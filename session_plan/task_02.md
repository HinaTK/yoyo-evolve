Title: Release v0.1.4 — SubAgentTool, AskUser, TodoTool, context management, fallback
Files: Cargo.toml, CHANGELOG.md
Issue: none

## Description

Significant features have accumulated since v0.1.3 (Day 24). Time to cut a release.

### What's new since v0.1.3

**Added:**
- **SubAgentTool** — model can delegate complex subtasks to a fresh agent with its own context window (Day 25)
- **AskUserTool** — model can ask directed questions mid-turn instead of guessing (Day 25)
- **TodoTool** — agent-accessible task tracking during autonomous runs, shared state with `/todo` (Day 26)
- **`--fallback <provider:model>`** — automatic mid-session provider failover (Day 28, if Task 1 ships)
- **`--context-strategy`** — three modes: compact, checkpoint-restart, manual (Day 25)
- **Proactive context compaction** — 70% threshold check before prompt attempts (Day 24)
- **`~/.yoyo.toml` config path** — the promised config location now actually works (Day 27)
- **MiniMax provider** — option 11 in setup wizard (Day 25)
- **MCP server config** in `.yoyo.toml` (Day 25)
- **Audit log** — `--audit` flag records tool calls to `.yoyo/audit.jsonl` (Day 24)

**Improved:**
- **Stream error recovery** — auto-retry on "stream ended", "broken pipe", "unexpected eof" (Day 26)
- **`/tokens` display** — clearer context vs cumulative labeling (Day 25)
- **Piped mode** — suppressed terminal bell in non-interactive mode (Day 24)

**Fixed:**
- **Flaky todo tests** — isolated global state with `serial_test` (Day 26)
- **`/web` panic** on non-ASCII HTML content (Day 25)
- **Config path mismatch** — `~/.yoyo.toml` now actually searched (Day 27)

### Steps

1. Bump version in `Cargo.toml`: `0.1.3` → `0.1.4`
2. Write the CHANGELOG entry for v0.1.4 at the top of CHANGELOG.md
   - If Task 1 (fallback) shipped, include it. If not, exclude it.
   - Date: 2026-03-28
   - Follow the existing format (Added/Improved/Fixed sections)
3. Run `cargo build && cargo test && cargo clippy --all-targets -- -D warnings && cargo fmt -- --check` — all must pass
4. `git add Cargo.toml CHANGELOG.md && git commit -m "v0.1.4: SubAgentTool, AskUser, TodoTool, context management"`
5. `git tag v0.1.4`
6. Do NOT run `cargo publish` — the release workflow triggers on the tag push

### Important
- Check the release skill gates before tagging
- If any gate fails, do NOT tag — just commit the version bump and changelog, and note the failure
- The tag push will trigger `.github/workflows/release.yml` which builds binaries for all platforms
