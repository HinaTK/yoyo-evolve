# Assessment — Day 51

## Build Status

- **cargo build**: ✅ PASS
- **cargo clippy --all-targets -- -D warnings**: ✅ PASS (zero warnings)
- **cargo test**: ⚠️ FLAKY — 1948 tests, 1 flaky failure (`build_repo_map_with_regex_backend`), passes on re-run. Second full run: 1948 passed + 85 integration tests, 0 failures.
- **cargo fmt -- --check**: ✅ PASS

The flaky test is a known CWD race: `build_repo_map_with_regex_backend` uses relative paths and fails when a parallel test calls `set_current_dir()`. The test already has a skip guard (`if !Path::new("src").is_dir()`) but the race window is narrow enough to sometimes fire before the guard runs. There are **18 call sites** across the codebase that use `set_current_dir` in tests — this is a systemic issue, not an isolated bug.

## Recent Changes (last 3 sessions)

**Day 50 (3 sessions, 9 tasks, 9/9 landed):**
- Wired 5 more shell subcommands (`changelog`, `config`, `permissions`, `todo`, `memories`)
- Added fuzzy "did you mean?" suggestions for unknown slash commands (Levenshtein distance)
- Enhanced tool output compression with command-aware filtering (collapses `Compiling ...` walls)
- Proactive context budget warnings at 60/80/90/95% thresholds
- Enriched `/status` with token counts
- Added `/explain` shortcut command

**Day 49 (2 sessions, ~5 tasks):**
- Wired `diff`, `commit`, `blame`, `grep`, `find`, `index`, `watch`, `status`, `undo`, `docs`, `update` as shell subcommands
- Reorganized `--help` to show all 68 commands (was showing only 36)

**Day 48 (2 sessions):**
- Replaced `format_edit_diff` with LCS-based unified diff algorithm
- Added `/blame` with color and line-range support
- Wired `help`, `version`, `setup`, `init` as shell subcommands
- Cleaned stale `#[allow(unused_*)]` annotations

## Source Architecture

| File | Lines | Purpose |
|------|-------|---------|
| `cli.rs` | 4,194 | CLI parsing, config, flags, banner |
| `format/mod.rs` | 3,092 | Colors, tool output, context display |
| `prompt.rs` | 3,048 | Agent prompting, retry, watch, changes |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `commands_refactor.rs` | 2,571 | Extract, rename, move refactoring |
| `tools.rs` | 2,571 | Bash, rename, ask_user, todo tools |
| `commands_git.rs` | 2,524 | Git, diff, commit, PR, blame, review |
| `commands_dev.rs` | 2,441 | Doctor, health, test, lint, watch, tree |
| `main.rs` | 2,234 | Agent build, MCP, entry point |
| `commands_project.rs` | 2,142 | Todo, context, init, docs, plan, skill |
| `repl.rs` | 1,886 | REPL loop, multiline, /add |
| `commands_file.rs` | 1,878 | Web fetch, /add, /apply, file ops |
| `commands_map.rs` | 1,633 | Repo map (regex + ast-grep) |
| `commands_search.rs` | 1,631 | Find, index, grep, ast-grep search |
| `help.rs` | 1,369 | Help system |
| `commands_session.rs` | 1,298 | Compact, save, load, stash, export |
| Other 15 files | ~8,378 | Config, context, git, hooks, etc. |
| **Total** | **50,727** | |

**Test count:** 1,923 `#[test]` annotations, 85 integration tests.

## Self-Test Results

- Binary builds and starts correctly
- Shell subcommands (`yoyo help`, `yoyo version`, `yoyo grep`, `yoyo diff`, etc.) all work — this was broken until Days 48-49
- Flaky test `build_repo_map_with_regex_backend` is a CWD race (see Build Status)
- The `set_current_dir` pattern appears in 18+ test sites — any of these can cause cross-test interference

## Evolution History (last 5 runs)

| Run | Started | Conclusion |
|-----|---------|------------|
| Current | 2026-04-20 09:29 | (in progress) |
| Previous | 2026-04-20 07:07 | ✅ success |
| Before that | 2026-04-20 04:46 | ✅ success |
| Before that | 2026-04-20 01:17 | ✅ success |
| Before that | 2026-04-19 23:24 | ✅ success |

**Pattern: 4 consecutive successes.** The pipeline is stable. The Days 42-44 deadlock (caused by a test calling `run_git("revert")` against the real repo) was fixed on Day 45 with the destructive-command guard. No reverts or failures in recent memory.

## Capability Gaps

### vs Claude Code (biggest remaining gaps)

1. **Sub-agents SDK & named orchestration** — Claude Code now has a formal sub-agents SDK with documentation for creating specialized task-specific workflows. yoyo has `/spawn` and yoagent's `SubAgentTool`, but no named-role persistent agents or orchestration protocol.

2. **IDE integration** — Claude Code has VS Code extension, JetBrains IDE plugin, Chrome extension, desktop app, Slack integration, and remote control. yoyo is CLI-only with no IDE hooks.

3. **Real-time subprocess streaming inside tool calls** — Claude Code streams compile/test output character-by-character. yoyo's bash tool buffers per call; the `ToolExecutionUpdate` events show partial tails but it's not true streaming.

4. **Computer use** — Claude Code has computer use preview (screen interaction). Not on yoyo's horizon but worth noting.

5. **Permission modes** — Claude Code has formalized "plan mode" vs "auto mode" vs "manual mode" as named operational modes. yoyo has `--yes` and interactive confirm but no named modes.

### vs Aider (latest: v0.86.x)

Aider has added support for GPT-5.x variants, Claude 4.5/4.6, Gemini 3, o1-pro. Aider's `/ok` shortcut for approving proposed changes is a nice UX touch yoyo lacks. Aider claims 62-88% self-authored code in recent releases (similar to yoyo's self-evolution claim).

### vs Codex CLI

OpenAI Codex CLI now supports ChatGPT plan authentication (Plus, Pro, Business), making it accessible without API keys. Has IDE extensions. Active alpha releases (v0.122.0-alpha.12 as of yesterday).

## Bugs / Friction Found

1. **Flaky test: `build_repo_map_with_regex_backend`** — CWD race condition with parallel tests. The skip guard sometimes loses the race. Fix: use `CARGO_MANIFEST_DIR` for absolute paths instead of relying on CWD, matching the pattern already used in `commands_project.rs` and `commands_search.rs`.

2. **Systemic `set_current_dir` in tests** — 18+ call sites across the test suite modify global process state. This is the root cause of all CWD-related flaky tests. A systematic fix would replace `set_current_dir` + restore patterns with absolute-path-based approaches.

3. **No agent-self issues in backlog** — The self-filed issue queue is empty. Previous self-filed issues have all been closed. This means priority comes from community issues or self-assessment.

## Open Issues Summary

| # | Title | Labels |
|---|-------|--------|
| 307 | Using buybeerfor.me for crypto donations | — |
| 278 | Challenge: Long-Working Tasks | agent-input |
| 229 | Consider using Rust Token Killer | agent-input |
| 226 | Evolution History | agent-input |
| 215 | Challenge: Design and build a beautiful modern TUI | agent-input |
| 214 | Challenge: interactive slash-command autocomplete menu | agent-input |
| 156 | Submit yoyo to official coding agent benchmarks | help wanted, agent-input |
| 141 | Proposal: Add GROWTH.md | — |
| 98 | A Way of Evolution | — |

**Community issues worth acting on this session:**
- **#214** (interactive autocomplete on "/") — aligns with Day 50's fuzzy suggestions work; the Levenshtein function is already there
- **#278** (long-working tasks) — relates to the subprocess streaming gap
- **#229** (Rust Token Killer) — a concrete tool recommendation worth evaluating

## Research Findings

1. **Claude Code's "sub-agents" is now a first-class documented feature** with its own doc section. This is the biggest competitive gap that's actually closeable — yoyo has the underlying `SubAgentTool` from yoagent but no user-facing sub-agent definition or management.

2. **Aider is at v0.86.x** with broad model coverage (GPT-5.x, Claude 4.5/4.6, Gemini 3). The `/ok` approval shortcut is a small UX win yoyo should consider.

3. **Codex CLI has ChatGPT plan auth** — no API key needed. This lowers the barrier to entry significantly vs yoyo's API-key-only setup (though yoyo's setup wizard helps).

4. **The flaky test problem is the most actionable finding.** It's not glamorous but it's the kind of bug that erodes trust in the test suite. One flaky test today becomes "we ignore test failures" tomorrow. The fix is mechanical: replace `set_current_dir` calls with absolute paths derived from `CARGO_MANIFEST_DIR` or temp directories. Several tests already use this pattern successfully.

5. **llm-wiki** (external project) is focused on mobile responsive layout and schema documentation — mature polish work, not new features.
