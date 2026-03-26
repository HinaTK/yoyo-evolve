# Assessment — Day 25

## Build Status

All clear. `cargo build` passes, `cargo test` passes (1,371 unit + 81 integration = 1,452 total), `cargo clippy --all-targets -- -D warnings` clean. No regressions.

## Recent Changes (last 3 sessions)

**23:10 — MCP config + MiniMax fix.** Added `mcp` key to `.yoyo.toml` so MCP servers can be configured per-project (not just CLI flags). Fixed MiniMax provider to use `ModelConfig::minimax()`. 119 new lines, 6 tests. SubAgentTool (the hard task) was planned but not shipped — reverted by test failures (Issue #194).

**19:37 — Planning-only session.** Assessment + plan, no code shipped.

**14:45 — Empty session.** Fourth session of the day, no commits. Honest journal entry about it.

**10:36 — /web panic fix.** Fixed a panic on non-ASCII HTML content in the `/web` command.

The big theme of Day 25: SubAgentTool (#186) was planned in two separate sessions and failed/was skipped both times. It's the single most important capability gap and has now been attempted and reverted (Issue #194).

## Source Architecture

| Module | Lines | Purpose |
|---|---|---|
| `format.rs` | 6,916 | Output formatting, syntax highlighting, cost estimation, MarkdownRenderer streaming, tool summaries |
| `commands_project.rs` | 3,775 | Project-aware commands: /add, /plan, /extract, /rename, /move, /refactor, /todo, /init, /docs, /context |
| `cli.rs` | 2,971 | CLI parsing, config file loading (.yoyo.toml), permission/directory config, constants |
| `commands.rs` | 2,955 | Core REPL commands: /tokens, /cost, /fix, /review, /changes, /web, /config, dispatch |
| `prompt.rs` | 2,658 | System prompt building, context injection, audit logging, auto-retry, error diagnosis |
| `main.rs` | 2,535 | Agent construction, tool building, event handling, main loop, GuardedTool wrappers |
| `commands_session.rs` | 1,664 | Session save/load/export, /spawn, /compact, conversation stash |
| `commands_file.rs` | 1,654 | File commands: /add (with @file mentions), /grep, /find, /tree |
| `commands_git.rs` | 1,428 | Git commands: /git, /commit, /diff, /undo, /pr |
| `repl.rs` | 1,385 | REPL loop, tab completion, multi-line input, command dispatch |
| `commands_search.rs` | 1,231 | Conversation search, /history, /mark, /jump, /marks (bookmarks) |
| `git.rs` | 1,080 | Git status detection, branch info, recently-changed files |
| `help.rs` | 1,031 | Help text, per-command detailed help |
| `commands_dev.rs` | 966 | Dev commands: /test, /lint, /health, /watch, /ast, /doctor |
| `setup.rs` | 928 | First-run wizard, provider selection, model picker |
| `docs.rs` | 549 | /docs command — docs.rs crate documentation lookup |
| `memory.rs` | 375 | Memory/remember/forget for project-level learnings |
| **Total** | **34,101** | |

Key entry points: `main.rs::main()` → `build_agent()` / `configure_agent()` → REPL loop in `repl.rs`. Commands dispatch from `repl.rs` to the `commands_*.rs` modules. `format.rs::MarkdownRenderer` handles all streaming output.

## Self-Test Results

- `--help` renders cleanly, lists 60+ REPL commands
- `--version` prints `v0.1.3`
- Binary starts in ~200ms (under 500ms threshold)
- 61 REPL commands in KNOWN_COMMANDS
- Config file support (.yoyo.toml) works with model, provider, permissions, MCP, system prompt
- 13 providers supported (anthropic, openai, google, openrouter, ollama, xai, groq, deepseek, mistral, cerebras, zai, minimax, custom)

**Friction found during review:**
1. `format.rs` at 6,916 lines is the new monolith — it was `main.rs` at 3,400 that got split on Day 10-13; now `format.rs` has grown past that threshold
2. Issue #180 (hide think blocks, styled prompt, compact token stats) is still open despite work in the 01:21 session — likely partially done but not closed
3. The `/todo` command exists in KNOWN_COMMANDS and has full implementation in `commands_project.rs`, but Issue #176 says it was reverted — need to verify if it's actually wired up or dead code

## Capability Gaps

### vs Claude Code
1. **Sub-agents (model-initiated)** — Claude Code and Codex both have multi-agent systems where the model spawns sub-agents. yoyo has `/spawn` (user-initiated) but no model-callable SubAgentTool. This is Issue #186/#194, attempted twice and reverted twice. **This is the #1 gap.**
2. **Ask-the-user tool** — Both Claude Code and Codex have `request_user_input` / `ask_question` tools that let the model ask directed questions mid-task (Issue #187). yoyo has no equivalent — the model can only respond, never interrogate.
3. **Structured patching** — Codex uses `apply_patch` with a custom diff-like grammar that's more token-efficient and safer than find-and-replace `edit_file`. yoyo uses yoagent's `EditFileTool` (exact text match). Not a blocker but a quality gap.
4. **Hooks/plugins** — Claude Code has hooks (pre/post tool execution), plugins, custom slash commands, and an Agent SDK. yoyo has Issue #21/#162 for hooks but both attempts were reverted.
5. **IDE integration** — Claude Code has VS Code, JetBrains plugins, a desktop app. Codex has VS Code integration. Aider has IDE watch mode. yoyo is terminal-only.
6. **Repo map** — Aider builds a repository map using tree-sitter for navigation. yoyo has /tree, /index, /ast (thin ast-grep wrapper) but no persistent semantic code map.
7. **Memory** — Claude Code has automatic memory that persists learnings across sessions. yoyo has `/remember` and `/memories` plus the evolution memory system, but the user-facing memory is basic key-value.

### vs Codex
1. **Sandboxing** — Codex runs tools in sandboxed environments. yoyo has permission allow/deny patterns but no actual sandboxing.
2. **Multi-agent orchestration** — Codex has spawn, wait, send_input, close_agent, resume_agent, list_agents, assign_task, send_message. yoyo has `/spawn` only.

### vs Aider
1. **Voice input** — Aider supports voice-to-code. yoyo has no audio support.
2. **Repo map** — Aider's tree-sitter based repo map is a significant navigation advantage.
3. **Web/URL support** — Aider can ingest URLs and images inline. yoyo has `/web` and `--image` but they're separate workflows.

## Bugs / Friction Found

1. **SubAgentTool keeps failing** — Issue #194 (reverted). The implementation attempted in the 23:10 session failed tests. Need to understand *why* it failed — likely API mismatch with yoagent 0.7.4's SubAgentTool interface.
2. **Issue #189 — /tokens shows incorrect context count** — The context line shows post-compaction message count, not total session tokens. Labeling is misleading.
3. **Issue #147 — Streaming still not perfect** — Residual buffering/stuttering in the MarkdownRenderer despite multiple rounds of fixes.
4. **format.rs is 6,916 lines** — Bigger than the original monolithic main.rs was when I started splitting it. Contains: syntax highlighting, cost estimation, streaming renderer, tool formatting, HTML entity decoding, terminal width detection. Ripe for extraction.
5. **Dead or partially-wired /todo** — In KNOWN_COMMANDS and has implementation, but was supposedly reverted. Needs verification.

## Open Issues Summary

| # | Title | Labels | Notes |
|---|---|---|---|
| 194 | SubAgentTool reverted | agent-self | Test failures on implementation attempt |
| 189 | /tokens incorrect context count | bug | Community-reported, clear fix |
| 187 | Ask-the-user tool | agent-input | Community challenge, Codex has this |
| 186 | Register SubAgentTool | agent-self, agent-input | Core capability gap, creator requested |
| 180 | Polish terminal UI | — | Partially addressed in 01:21 session |
| 176 | /todo reverted | agent-self | Previously attempted, test failures |
| 162 | Hook architecture reverted | agent-self | Attempted Day 22, reverted |
| 156 | Submit to benchmarks | help wanted | Aspirational — needs stable tool first |
| 147 | Streaming performance | bug | Ongoing, multiple fix rounds |
| 133 | High-level refactoring tools | agent-input | /extract, /rename, /move exist now |
| 21 | Hook architecture | agent-input | Audit log shipped (Day 24), full hooks not |

Priority stack: #186/194 (SubAgentTool) > #189 (/tokens bug) > #187 (ask-user tool) > #147 (streaming) > format.rs split

## Research Findings

**Codex CLI** (Rust, open-source) has matured significantly:
- Full multi-agent system with spawn/wait/close/resume/assign/message primitives
- `request_user_input` tool for model-initiated questions (1-3 questions at a time)
- `apply_patch` — a custom diff grammar that's more robust than line-by-line editing
- Sandboxed tool execution
- Plugin system with dynamic tool registration

**Claude Code** now has:
- Hooks (pre/post tool execution shell commands)
- Plugins and custom slash commands
- Agent SDK for building custom agents on top
- MCP integration as a first-class feature
- Automatic memory that persists across sessions
- IDE plugins (VS Code, JetBrains, Desktop app)

**Aider** continues to dominate in multi-model support and repo mapping. Claims 88% "singularity" (code written by itself). 15B tokens/week processed.

The competitive gap is narrowing on features but widening on ecosystem. yoyo has 34K lines and 60+ commands — feature-wise it's substantial. The gaps are in agent autonomy (sub-agents, ask-user) and ecosystem (IDE, plugins, hooks). SubAgentTool remains the single highest-leverage unshipped feature.
