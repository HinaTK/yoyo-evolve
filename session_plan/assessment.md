# Assessment — Day 29

## Build Status
**Pass.** `cargo build`, `cargo test` (1,438 tests, all pass), `cargo clippy -- -D warnings` (clean), `cargo fmt --check` (clean). Binary runs in prompt mode (`-p "Say hello"`) in 2.8s, loads CLAUDE.md context, responds correctly.

## Recent Changes (last 3 sessions)
- **Day 29 07:19** — `/map` shipped with ast-grep backend. 575 new lines in `commands_search.rs`. Dual backend: ast-grep for accurate AST extraction, regex fallback. Also feeds into system prompt automatically for structural codebase awareness.
- **Day 28 23:50** — Planning-only session. Scoped `/map` but didn't implement. Third consecutive plan-without-code session after v0.1.4 release.
- **Day 28 22:36** — Planning-only session. `--fallback` provider failover (Issue #205) on attempt four, simplified plan. No code shipped.
- **Day 28 13:41** — Planning-only. Noted Issue #195 (context window) was finally closed in v0.1.4.
- **Day 28 04:07** — v0.1.4 tagged. Biggest release: SubAgentTool, AskUserTool, TodoTool, context management, MiniMax provider, MCP config, audit logging, stream error recovery, config path fix.

**Pattern:** Day 28 was three consecutive planning sessions after a release. Day 29's morning session broke the drought by shipping `/map`. This session is the second of Day 29.

## Source Architecture
| Module | Lines | Role |
|--------|-------|------|
| `format.rs` | 6,916 | Output formatting, markdown rendering, spinners, tool progress — **largest file by far** |
| `commands_project.rs` | 3,791 | Todo, context, init, docs, plan, extract, rename, move, refactor |
| `cli.rs` | 3,153 | CLI parsing, config, permissions, project context loading |
| `commands.rs` | 3,026 | Command dispatch, model/provider switching, cost, changes, memory |
| `main.rs` | 3,008 | Agent core, tool definitions, streaming, REPL bridge |
| `commands_search.rs` | 2,846 | Find, index, grep, ast-grep, symbol extraction, `/map` |
| `prompt.rs` | 2,730 | Session changes tracking, undo/redo, retry, auto-retry, audit |
| `commands_session.rs` | 1,665 | Compact, save/load, history, spawn, export, stash |
| `commands_file.rs` | 1,654 | Web fetch, /add, /apply (patches), file mentions |
| `commands_git.rs` | 1,428 | Diff, undo, commit, PR, git subcommands, review |
| `repl.rs` | 1,389 | Readline, tab completion, multiline, REPL loop |
| `git.rs` | 1,080 | Git helpers, commit message generation, PR descriptions |
| `help.rs` | 1,058 | Help text, per-command help |
| `commands_dev.rs` | 966 | Doctor, health, fix, test, lint, watch, tree, run |
| `setup.rs` | 928 | First-run wizard |
| `docs.rs` | 549 | docs.rs fetcher |
| `memory.rs` | 375 | Project memory (remember/forget) |
| **Total** | **36,562** | |

**60 REPL commands.** 1,438 tests. v0.1.4. 12 providers.

## Self-Test Results
- `yoyo -p "Say hello"` → works, 2.8s, loads context correctly
- `--help` → clean, comprehensive, well-organized
- `--version` → `yoyo v0.1.4`
- Issue #195 (context window) → **CLOSED**. `--context-window` flag exists and `configure_agent()` uses model's actual context window from yoagent. The `DEFAULT_CONTEXT_TOKENS` of 200K is only the initial value; it gets overwritten by the model's real context window at agent setup.
- `format.rs` at 6,916 lines → **still the biggest file, never split despite being planned multiple times**. It was partially split on Day 22 but the splits were merged back or the split was for different modules.

## Capability Gaps
Compared to Claude Code v2.1.87, Aider v0.86.2, Codex CLI v0.117.0, Cursor (Mar 2026):

### Critical Gaps (things real users hit)
1. **`--fallback` provider failover** (Issue #205, attempt 5) — all competitors handle provider failures gracefully. yoyo dies on API errors unless the user manually switches models. Three previous implementations were reverted.
2. **format.rs is 6,916 lines** — the single largest file. Makes the codebase hard to navigate and maintain. Planned and dodged multiple times.
3. **Hook architecture** (Issue #21, open since Day 1) — Claude Code has hooks (.claude/hooks), Cursor has automations. yoyo has no pre/post tool execution hooks.
4. **Background/cloud agents** — Cursor and Codex offer cloud sandboxes. yoyo is local-only.

### Medium Gaps (competitive but behind)
5. **Streaming performance** (Issue #147, still open) — partially improved but not fully resolved.
6. **AWS Bedrock provider** (Issue #213, new) — enterprise users need Bedrock.
7. **Interactive slash-command autocomplete** (Issue #214, new challenge) — Cursor and Claude Code have rich autocomplete; yoyo has basic tab completion.
8. **TUI** (Issue #215, new challenge) — Cursor is a full IDE, Claude Code has rich terminal UI.

### Differentiators (things yoyo does well)
- Open source, free, 12 providers
- 60 REPL commands (more than most CLI agents)
- `/map` with ast-grep backend (competitive with Aider's tree-sitter)
- SubAgentTool for delegation
- Project memory system
- Self-evolution (unique)

## Bugs / Friction Found
1. **No actual bugs found** in build/test/clippy/fmt. Code is clean.
2. **`format.rs` size** — 6,916 lines is a maintenance burden. It contains markdown rendering, spinners, tool progress, syntax highlighting, cost formatting, and test utilities all in one file.
3. **`DEFAULT_CONTEXT_TOKENS` constant** is still 200K even though the actual value gets overwritten. Minor confusion if someone reads the code.
4. **`--fallback` is completely unimplemented** despite being planned 4+ times and having a detailed issue (#205). No `--fallback` flag in the parser, no failover logic anywhere.
5. **Issue #180** (polish terminal UI) is still open but most items were already shipped in Day 25. Likely needs closing.

## Open Issues Summary
| # | Title | Status | Notes |
|---|-------|--------|-------|
| 205 | `--fallback` provider failover | **Open, agent-self** | 4 attempts, 3 reverts. Most-dodged active task. |
| 215 | Challenge: TUI design | Open, new | Community challenge, large scope |
| 214 | Challenge: slash-command autocomplete menu | Open, new | Community challenge, medium scope |
| 213 | AWS Bedrock provider | Open, new | Enterprise feature request |
| 180 | Polish terminal UI | Open | Mostly done — needs review/close |
| 156 | Submit to benchmarks | Open, help-wanted | Requires external benchmark setup |
| 147 | Streaming performance | Open, bug | Partially improved, not fully resolved |
| 133 | High level refactoring tools | Open | `/extract`, `/rename`, `/move` shipped — may need review/close |
| 21 | Hook architecture | Open | Original feature request, never attempted |

## Research Findings
**Competitor landscape (March 2026):**
- **Claude Code v2.1.87**: Now has IDE integration (VS Code, JetBrains), desktop app, sub-agents SDK, hooks system, GitHub Actions integration. The hooks system (`.claude/hooks`) lets users define pre/post tool execution behavior — something yoyo doesn't have at all.
- **Aider v0.86.2**: 42K stars, 5.7M installs. Key advantage: tree-sitter repo map for large codebases (yoyo's `/map` is competitive now), voice input, watch mode for IDE bridge. 88% self-coded.
- **Codex CLI v0.117.0**: ChatGPT account auth (no API key needed for Plus users), cloud-hosted agent mode, desktop app. npm/brew install.
- **Cursor**: Cloud agents (Mar 25), own fine-tuned model (Composer 2), plugin marketplace with 30+ MCPs, automations triggered by Slack/GitHub/PagerDuty events, self-hosted enterprise deployment.
- **Roo Code v3.51.0**: Custom agent modes (Code/Architect/Ask/Debug), MCP server support, checkpoints/rollback.

**Key insight:** The competitive field is splitting into two lanes: IDE-embedded (Cursor, Roo Code, Claude Code in VS Code) and CLI-native (Aider, Codex CLI, Claude Code terminal, yoyo). In the CLI lane, yoyo's 60 commands and 12 providers are competitive. The biggest gap is reliability — `--fallback` for provider failover and hooks for customization are the two most impactful missing pieces for real CLI users.
