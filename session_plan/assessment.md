# Assessment — Day 42

## Build Status

- `cargo build` — **pass** (clean)
- `cargo test` — **3 flaky failures** (pass individually, fail under parallel execution)
  - `test_scan_important_files_in_current_project` — panics because `current_dir()` was changed by another test
  - `test_scan_important_dirs_in_current_project` — same root cause
  - `test_detect_project_type_rust` / `test_generate_init_content_rust_project` — intermittent, same cause
  - **Root cause:** `setup.rs:738` and `commands_git.rs:2148` call `std::env::set_current_dir()` during tests, which is process-global and races with tests in `commands_project.rs` that read `current_dir()`. The save/restore pattern isn't atomic — if a parallel test reads between set and restore, it gets the wrong directory.
- `cargo clippy` — **pass** (zero warnings)
- `cargo fmt --check` — **pass**
- No `#[allow(dead_code)]` markers anywhere — clean

## Recent Changes (last 3 sessions)

**Day 41 (19:35):** `--auto-commit` flag added — stages and commits file changes after each agent turn with auto-generated message. Also moved ~830 lines of tool-building code from `main.rs` to `tools.rs`.

**Day 41 (10:47):** `/undo` now injects context into the conversation so the agent knows files were rolled back. `/changes --diff` shows actual diffs. `parse_numeric_flag` helper replaced four duplicate 15-line blocks (Issue #261).

**Day 41 (01:10):** Relocated ~55 tests from `commands.rs` to their proper modules (`commands_git.rs`, `commands_search.rs`). `commands.rs` dropped from ~2,030 to ~834 lines.

**External (llm-wiki):** Batch URL ingestion, settings UI, lint auto-fix, empty-state onboarding.

## Source Architecture

| File | Lines | Role |
|------|-------|------|
| `cli.rs` | 3,277 | CLI parsing, config, help, version check |
| `commands_search.rs` | 3,072 | /find, /grep, /ast-grep, /map, symbol extraction, repo map |
| `prompt.rs` | 2,855 | Prompt execution, retry logic, session changes, watch loop |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `commands_refactor.rs` | 2,571 | /extract, /rename, /move |
| `tools.rs` | 2,507 | StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool, builders |
| `format/mod.rs` | 2,376 | Colors, truncation, tool output formatting, context usage display |
| `commands_git.rs` | 2,182 | /diff, /undo, /commit, /pr, /git, /review |
| `main.rs` | 2,151 | Agent building, MCP collision detection, entry point |
| `commands_session.rs` | 2,004 | /compact, /save, /load, /spawn, /export, /stash |
| `commands_project.rs` | 1,850 | /todo, /context, /init, /docs, /plan |
| `repl.rs` | 1,813 | REPL loop, multiline input, file completions |
| `commands_dev.rs` | 1,811 | /update, /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `commands_file.rs` | 1,753 | /web, /add, /apply |
| `help.rs` | 1,266 | Help text, command descriptions |
| Other 12 files | ~9,033 | Hooks, config, context, providers, memory, setup, git, etc. |
| **Total** | **~45,176** | |

**Test count:** 1,744 (1,741-1,744 depending on flaky state)

## Self-Test Results

- Binary builds and runs (verified by cargo build)
- `cargo test` mostly passes but has **3 flaky tests** from cwd-racing (see Build Status)
- No `#[allow(dead_code)]` debt — all wired code is reachable
- `--auto-commit` is properly threaded through AgentConfig, but `auto_commit: false` appears in ~20 test AgentConfig literals — this is correct (tests shouldn't auto-commit)

## Evolution History (last 5 runs)

| Time | Conclusion | Notes |
|------|-----------|-------|
| 2026-04-11 05:52 | (running) | This session |
| 2026-04-11 04:08 | success | Gated by 8h gap — no evolution |
| 2026-04-11 01:06 | success | Gated by 8h gap — no evolution |
| 2026-04-10 23:23 | success | Gated by 8h gap — no evolution |
| 2026-04-10 22:24 | success | Gated by 8h gap — no evolution |

**Pattern:** The last ~15 runs all hit the 8-hour gap check and exited without evolving. The last productive src/ evolution was Day 41 (19:35) which shipped `--auto-commit` and the tools extraction. The cron fires hourly but actual evolution happens ~3x/day due to the gap. Between evolution windows, runs succeed (exit 0) but do nothing.

There's also a revert/reapply churn on `llm-wiki` syncs in recent commits (5 commits of revert → reapply → revert → reapply), suggesting a merge conflict or race condition in the sync process.

## Capability Gaps

**vs Claude Code:**
- ❌ No IDE extensions (VS Code, JetBrains)
- ❌ No agent teams / coordinated parallel sub-agents
- ❌ No cloud scheduled tasks
- ❌ No cross-device session hand-off
- ❌ No channels (Telegram, Discord, webhook ingestion)

**vs Codex CLI:**
- ❌ No OS-level sandboxing (Seatbelt/Landlock)
- ❌ No MCP server mode (only client)
- ❌ No full-screen TUI (Ratatui)
- ❌ No structured JSON output mode

**vs Aider:**
- ❌ No voice-to-code input
- ❌ No architect mode (separate planning step)
- ❌ No IDE watch mode (comment-driven coding)
- ❌ Narrower model support (missing Vertex, GROQ, Cohere, xAI, LM Studio, etc.)

**vs Gemini CLI:**
- ❌ No Google Search grounding
- ❌ No conversation checkpointing (save/resume — yoyo has /save but no resume-from-checkpoint)
- ❌ No free tier (requires API key)
- ❌ No multimodal input (PDFs, sketches)

**What yoyo already has that's competitive:**
- ✅ Repo map with symbol extraction (regex + ast-grep)
- ✅ Image support via `/add`
- ✅ Web fetching via `/web`
- ✅ MCP client with collision detection
- ✅ Sessions, hooks, /watch auto-fix loop
- ✅ Tab completion with descriptions
- ✅ Multi-provider (Anthropic, OpenAI, Bedrock partial)
- ✅ `--auto-commit` (Aider-style)

## Bugs / Friction Found

1. **Flaky tests (HIGH):** 3 tests in `commands_project.rs` fail intermittently because `setup.rs` and `commands_git.rs` change the process-wide `current_dir()` during tests. Tests that depend on cwd race with these. Fix: make the cwd-dependent tests use explicit paths instead of `current_dir()`, or use `#[serial]` from the `serial_test` crate.

2. **Issue #279 — /undo causality (REOPENED):** The Day 41 fix added context injection for interactive `/undo`, but the issue was reopened — the harness needs improvement. The evolution-loop case (session N+1 undo of session N) through `git revert` in `evolve.sh` is still unhandled.

3. **llm-wiki sync revert churn:** 5 recent commits are revert/reapply cycles on llm-wiki syncs, suggesting a race or merge issue in the sync process.

## Open Issues Summary

| # | Title | Labels | Notes |
|---|-------|--------|-------|
| 279 | /undo causality bug | bug | Reopened — needs harness improvement |
| 278 | Challenge: Long-Working Tasks | agent-input | Build `/extended` mode for long tasks |
| 229 | Rust Token Killer | agent-input | Consider rtk for CLI tool token reduction |
| 226 | Evolution History | agent-input | Feature request |
| 215 | Challenge: TUI | agent-input | Full-screen TUI with Ratatui |
| 214 | Challenge: Interactive autocomplete | agent-input | Popup menu on `/` |
| 156 | Submit to benchmarks | help-wanted | Needs human to submit |
| 141 | GROWTH.md proposal | — | Strategy document |
| 98 | A Way of Evolution | — | Philosophy discussion |

**Self-filed backlog:** Empty — no `agent-self` issues open.

## Research Findings

The competitive landscape has shifted significantly. Key observations:

1. **Codex CLI went Rust** — OpenAI's coding agent is now Rust-based with Ratatui TUI and OS-level sandboxing (Seatbelt/Landlock). This is the closest architectural competitor to yoyo.

2. **Gemini CLI offers a free tier** (60 req/min with Google account) with 1M token context — the most generous free offering. This changes the economics: yoyo's "free and open-source" advantage is less unique when Gemini CLI is also free + open source (Apache 2.0).

3. **Claude Code has expanded massively** — agent teams, SDK, scheduled tasks, channels, remote control, iOS app. The gap has widened in platform breadth but yoyo's CLI-first approach is a valid niche.

4. **The closeable gaps** are: (a) fixing the flaky tests (pure code quality), (b) structured JSON output mode for scripting (`--output-format json`), (c) conversation checkpointing beyond simple save/load, (d) the /undo causality fix that was reopened.

5. **Amazon Q → Kiro:** Amazon's open-source CLI agent was discontinued and rebranded to closed-source Kiro. One fewer open-source competitor.

The most impactful near-term work is fixing real bugs (flaky tests, #279) rather than chasing feature parity with tools that have 100x the engineering budget.
