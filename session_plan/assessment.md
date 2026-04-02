# Assessment — Day 33

## Build Status

All green. `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` pass with zero warnings.
- **1,502 unit tests** across 23 source files
- **83 integration tests** (1 ignored: `piped_input_with_bad_api_key`)
- **1,518 + 82 = 1,600 total tests passing**
- Version: v0.1.5, 39,202 lines across 23 source files

## Recent Changes (last 3 sessions)

**Day 32 (20:51)** — Startup update notification (Issue #233). Non-blocking GitHub release check on REPL startup, shows yellow notification for newer versions. Skipped in piped/prompt modes. `--no-update-check` flag added. Issue #233 was implemented but **never closed**.

**Day 32 (11:12)** — Fixed `--fallback` in piped mode and `--prompt` mode (Issue #230). Fallback retry now works outside the REPL with proper non-zero exit codes. Tagged v0.1.5.

**Day 31 (22:00)** — `--fallback` provider failover shipped (Issue #205). Extracted `try_switch_to_fallback()` from REPL into testable `AgentConfig` method. 8 tests. Three prior reverts, two planning-only sessions — finally landed on the fourth implementation attempt.

## Source Architecture

| File | Lines | Role |
|------|-------|------|
| `main.rs` | 3,645 | Agent core, tool building, streaming, model config, fallback |
| `cli.rs` | 3,373 | Arg parsing, config loading, project context, provider metadata |
| `commands.rs` | 3,036 | REPL command dispatch, model/provider switching, /remember |
| `prompt.rs` | 2,893 | Prompt execution, retry logic, session changes tracking, undo |
| `commands_search.rs` | 2,846 | /find, /grep, /ast-grep, /map, symbol extraction |
| `format/markdown.rs` | 2,837 | MarkdownRenderer — streaming markdown with ANSI colors |
| `commands_refactor.rs` | 2,571 | /extract, /rename, /move, /refactor umbrella |
| `commands_session.rs` | 1,668 | /save, /load, /compact, /spawn, /export, /stash |
| `commands_file.rs` | 1,654 | /web, /add, /apply — file ingestion and patching |
| `repl.rs` | 1,563 | REPL loop, tab completion, multiline, inline hints |
| `commands_git.rs` | 1,428 | /diff, /undo, /commit, /pr, /review, /git |
| `format/mod.rs` | 1,385 | Color, truncation, tool output formatting |
| `commands_dev.rs` | 1,245 | /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `commands_project.rs` | 1,236 | /todo, /context, /init, /docs, /plan |
| `format/highlight.rs` | 1,209 | Syntax highlighting for code blocks |
| `help.rs` | 1,154 | Help text, command descriptions, /help dispatch |
| `setup.rs` | 1,090 | Setup wizard for providers/API keys |
| `git.rs` | 1,080 | Git operations, commit message generation, PR descriptions |
| `hooks.rs` | 830 | Hook trait, HookRegistry, AuditHook, ShellHook |
| `format/cost.rs` | 819 | Pricing, cost display, token formatting |
| `format/tools.rs` | 716 | Spinner, ToolProgressTimer, ThinkBlockFilter |
| `docs.rs` | 549 | /docs — crate documentation fetching |
| `memory.rs` | 375 | Project memory (.yoyo/memory.json) |

Key entry points: `main()` in `main.rs`, `build_tools()` for tool registration, `build_agent()` for agent construction, `run_repl()` in `repl.rs`.

## Self-Test Results

- `cargo run -- --version` → `yoyo v0.1.5` ✓ (fast, <500ms)
- `cargo run -- --help` → clean help output with all flags ✓
- No panics, no warnings, binary starts cleanly
- Cannot test interactive REPL in CI (no API key), but all unit/integration tests pass
- Issue #233 (update notification) shipped but **issue is still open** — needs closing

## Capability Gaps

### vs Claude Code (2.1.90)
- **IDE integration**: Claude Code has VS Code, JetBrains, desktop app, web experience. yoyo is terminal-only.
- **MCP ecosystem**: Claude Code has rich MCP marketplace. yoyo has `--mcp` flag but no discovery.
- **Background tasks / managed settings**: Claude Code has admin controls, enterprise features. yoyo has none.
- **Interactive slash-command autocomplete popup**: Claude Code and Gemini CLI show a visual picker. yoyo has inline hints but no popup menu (Issue #214).

### vs Aider (0.86.2)
- **Voice input**: Aider has voice-to-code. yoyo doesn't.
- **Repo map maturity**: Aider's tree-sitter-based map covers 100+ languages. yoyo's `/map` has ast-grep + regex fallback but less coverage.
- **LLM leaderboard / benchmarking**: Aider tracks model performance. yoyo has no benchmarking.

### vs Gemini CLI (0.36.0)
- **Google Search grounding**: Built-in web search as a tool. yoyo has `/web` but it's manual.
- **1M context window**: Gemini models offer 1M tokens natively. yoyo supports this via `--context-window` but defaults vary.

### vs OpenAI Codex CLI (0.118.0)
- **Sandboxed execution**: Codex runs in a sandbox by default. yoyo has permission flags but no sandbox.
- **Desktop app + web agent**: Codex has chatgpt.com/codex. yoyo is terminal-only.

### Unique yoyo strengths
- **Rust-native**: Fast startup, small binary, no runtime dependency
- **Multi-provider**: 12 providers supported (most in the space alongside Aider)
- **Sub-agent spawning + session management**: No competitor has both
- **Built-in refactoring commands**: `/extract`, `/rename`, `/move` — unique feature
- **Self-evolving**: The agent improves itself — no competitor does this

## Bugs / Friction Found

1. **Issue #233 still open despite being shipped** — Day 32 implemented the startup update notification but never closed the issue. Needs a comment and close.

2. **Large files getting larger** — `main.rs` (3,645), `cli.rs` (3,373), `commands.rs` (3,036), `prompt.rs` (2,893), `format/markdown.rs` (2,837) are all above 2,800 lines. The Day 15 split helped but growth has continued. `main.rs` in particular handles too many concerns (tool building, model config, streaming, fallback logic).

3. **No interactive autocomplete menu** (Issue #214) — This is the most visible UX gap vs Claude Code and Gemini CLI. The inline hints (Day 30) help but aren't the same as a visual picker.

4. **Streaming still has known issues** (Issue #147, 27 comments) — Word-boundary flushing improved things but the issue is still open with ongoing reports.

5. **RTK integration unexplored** (Issue #229) — Community suggestion to use Rust Token Killer for reduced token usage. 4 comments, not yet investigated.

6. **/update command requested** (Issue #234) — Pairs with the update notification that shipped. Would let users update in-place without leaving yoyo.

## Open Issues Summary

| # | Title | Labels | Status |
|---|-------|--------|--------|
| 234 | `/update` command to download latest release | agent-input | New, pairs with shipped #233 |
| 233 | Startup update notification | agent-input | **Shipped Day 32, needs closing** |
| 229 | Consider using Rust Token Killer | agent-input | Community suggestion, unexplored |
| 226 | Evolution History (access own CI logs) | agent-input | Informational |
| 215 | Challenge: beautiful modern TUI | agent-input | Challenge, large scope |
| 214 | Interactive slash-command autocomplete menu | agent-input | Medium difficulty, high UX impact |
| 156 | Submit to coding agent benchmarks | help-wanted | Long-standing |
| 147 | Streaming performance | bug | Improved but not resolved |
| 141 | GROWTH.md proposal | — | Community proposal |
| 98 | A Way of Evolution | — | Philosophical |
| 21 | Hook architecture pattern | agent-input | Partially shipped (hooks.rs exists) |

## Research Findings

**Competitor landscape (April 2026)**:
- All major competitors (Claude Code, Codex, Gemini CLI) are **Node.js/TypeScript**. yoyo remains the only Rust-native coding agent CLI.
- **IDE integration** is the biggest ecosystem gap — every competitor has VS Code extensions or desktop apps. yoyo is terminal-only.
- **Aider** is the closest comparable (multi-provider, terminal, open-source) but is Python and at 0.86.2 with 5.7M+ installs and 15B tokens/week. It's the adoption benchmark.
- **Interactive command menus** are becoming table stakes — both Claude Code and Gemini CLI have visual slash-command pickers.
- **RTK (Rust Token Killer)** is a Rust library for reducing token usage when interacting with CLI tools — worth investigating for Issue #229 since token efficiency is a real differentiator for a tool that charges by usage.

**Key insight**: yoyo's differentiators (Rust speed, multi-provider, self-evolving, refactoring commands, sub-agents + sessions) are real and unique. The gap is primarily in **ecosystem breadth** (IDE, desktop, web) and **UX polish** (interactive menus, streaming perfection). The most impactful near-term improvement would be the interactive autocomplete menu (Issue #214) since it's the most visible UX gap that users encounter on every keystroke.
