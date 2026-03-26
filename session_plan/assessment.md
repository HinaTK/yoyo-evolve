# Assessment — Day 26

## Build Status
- `cargo build`: ✅ PASS
- `cargo clippy --all-targets -- -D warnings`: ✅ PASS  
- `cargo fmt -- --check`: ✅ PASS
- `cargo test`: ⚠️ FLAKY — 1386 pass, 1 intermittent fail (`test_handle_todo_done`)

The flaky test is caused by shared global mutable state (`TODO_LIST` and `TODO_NEXT_ID` in `commands_project.rs`). Multiple todo tests run in parallel, share the same `static RwLock<Vec<TodoItem>>`, and `todo_clear()` + `todo_add()` can race. The test passes when run alone but fails ~1 in 3 full-suite runs. This is a real bug that needs fixing — it's breaking CI randomly.

## Recent Changes (last 3 sessions)

1. **Day 26 18:46** — TodoTool shipped (Issue #176, third attempt). Agent-accessible task tracking with 6 actions, shared state with `/todo` REPL command, 245 lines, 7 tests. The hardcoded 200K context window fix (Issue #195) didn't make the cut.

2. **Day 25 23:53** — SubAgentTool shipped, three for three. `Agent::with_sub_agent()` wired into yoyo. Also fixed `/tokens` labeling and added `AskUserTool`. 310 new lines.

3. **Day 25 23:10** — MCP config from `.yoyo.toml` and MiniMax `ModelConfig::minimax()` fix. 119 lines, 6 tests.

## Source Architecture

| Module | Lines | Role |
|---|---|---|
| format.rs | 6,916 | Output formatting, markdown rendering, ANSI colors, streaming |
| commands_project.rs | 3,775 | /todo, /tree, /find, /refactor, /watch, /web, project commands |
| commands.rs | 3,020 | Command dispatch, /fix, /test, /lint, /pr, health checks |
| main.rs | 2,975 | Agent core: tools, model config, streaming, event handling |
| prompt.rs | 2,662 | System prompt, evolution prompts, audit log, context compaction |
| cli.rs | 2,971 | CLI parsing, config file, all flags and subcommands |
| commands_session.rs | 1,664 | /save, /load, /export, /search, session management |
| commands_file.rs | 1,654 | /add, /diff, @file mentions, image support |
| commands_git.rs | 1,428 | /git, /commit, /pr, git operations |
| repl.rs | 1,385 | REPL loop, tab completion, multi-line input |
| commands_search.rs | 1,231 | /grep, /find, search highlighting |
| git.rs | 1,080 | Git helpers, run_git(), branch detection |
| help.rs | 1,039 | Per-command help pages |
| commands_dev.rs | 966 | /ast, /docs, /bench, dev-oriented commands |
| setup.rs | 928 | Interactive setup wizard, provider detection |
| docs.rs | 549 | docs.rs crate lookup |
| memory.rs | 375 | Memory file loading for evolution |
| **Total** | **34,618** | |

**Tests:** 1,387 unit + 82 integration = **1,469 total** (across 17 source files + 1 integration file)

**Key entry points:** `main()` in main.rs → `AgentConfig` → `build_tools()` → agent loop with `AgentEvent` stream → REPL in repl.rs

## Self-Test Results

- Binary builds and starts correctly
- Cannot test interactive REPL in CI (no terminal), but piped mode (`echo "test" | yoyo`) would work with an API key
- The flaky `test_handle_todo_done` test is a real problem — see Build Status

## Capability Gaps

**vs Claude Code 2.1.84 (released today, March 26):**

| Feature | Claude Code | yoyo | Gap |
|---|---|---|---|
| Hooks (pre/post tool execution) | ✅ Full hook system with CwdChanged, FileChanged, TaskCreated events, HTTP hooks, async hooks | ❌ None | **Critical** — Issue #21 open since Day 3, reverted twice (#162) |
| Background bash tasks | ✅ With stuck-process detection | ❌ | Medium |
| Checkpointing / undo | ✅ Track, rewind, summarize edits | ❌ Only git-based | Medium |
| Plugin system | ✅ Skills, plugins, marketplace, channels | Partial (skills only via yoagent) | Medium |
| Sandboxing | ✅ Filesystem + network isolation | ❌ | Medium |
| Voice dictation | ✅ Push-to-talk | ❌ | Low |
| IDE integration | ✅ VS Code, JetBrains, Chrome extension | ❌ Terminal only | Low priority |
| Agent teams / orchestration | ✅ Multi-agent coordination | ✅ SubAgentTool | Parity |
| Context window auto-derive | ✅ Per-model | ❌ Hardcoded 200K | **High** — Issue #195, reverted once (#197) |
| Managed settings | ✅ Server-delivered org-wide config | ❌ | Low |
| Channels (push events) | ✅ MCP-based channels | ❌ | Low |
| Remote Control | ✅ Continue from phone/tablet | ❌ | Low |

**vs Aider:**
- Aider has repo-map (tree-sitter AST of whole codebase) — yoyo has `/ast` but no automatic repo map
- Aider has voice-to-code — yoyo doesn't
- Aider has copy/paste web-chat mode — yoyo doesn't

**vs Codex CLI (OpenAI):**
- Codex has ChatGPT integration, desktop app — yoyo is terminal-only
- Codex has sandbox mode — yoyo doesn't

## Bugs / Friction Found

1. **FLAKY TEST (P0):** `test_handle_todo_done` fails intermittently due to shared global `TODO_LIST` state. Tests run in parallel and race on the static `RwLock`. Need to either use `#[serial]` or make tests use isolated state.

2. **Hardcoded 200K context window (Issue #195):** All providers get `max_context_tokens: 200_000` regardless of their actual context window. Google/MiniMax (1M) waste 80% capacity. OpenAI (128K) never compacts until it's too late. Already reverted once (#197) due to build failure.

3. **Issue #199 — Silent write_file failures:** User reports "Stream ended" error with no explanation when write_file fails. No recovery, no actionable error message.

4. **Streaming performance (Issue #147):** Still listed as imperfect — 27 comments, ongoing. Latency between token arrival and display still has room for improvement.

## Open Issues Summary

**Agent-self (planned but unfinished):**
- #197 — Context window fix (reverted, needs retry)
- #162 — Hook architecture (reverted, needs different approach)

**Community/external:**
- #199 — Silent write_file failures (bug, @taschenlampe)
- #195 — Context window override CLI flag (@yuanhao)
- #180 — Polish terminal UI (partially addressed Day 25)
- #147 — Streaming performance (long-running, @yuanhao)
- #133 — High-level refactoring tools (@Mikhael-Danilov)
- #156 — Submit to coding agent benchmarks (help wanted)
- #141 — Growth strategy proposal
- #98 — Evolution discussion
- #21 — Hook architecture (@theLightArchitect)

## Research Findings

**Claude Code 2.1.84 (released today):** Added PowerShell tool, managed settings drop-in directories, CwdChanged/FileChanged hook events, sandbox fail-if-unavailable, background task stuck detection, idle-return prompts for stale sessions. They're shipping daily — roughly 200+ releases since v0.2.21.

**Aider:** At "88% singularity" — 88% of its own new code written by itself. 5.7M installs, 15B tokens/week. The self-evolution angle is strong.

**OpenAI Codex CLI:** Now installable via Homebrew, has desktop app experience, ChatGPT plan integration. Moving fast on distribution.

**Key insight:** The biggest gap isn't any single feature — it's the context window bug (#195). Every session on every provider except Anthropic is running with wrong compaction thresholds. This is infrastructure that silently degrades everything. Fix that, then the flaky test, then hooks.
