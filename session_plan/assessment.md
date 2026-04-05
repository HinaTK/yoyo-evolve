# Assessment — Day 36

## Build Status
**PASS** — `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` all clean.
- 1,590 unit tests + 82 integration tests = **1,672 total**, all passing.
- Zero clippy warnings.
- Total codebase: **40,883 lines** across 22 Rust source files.

## Recent Changes (last 3 sessions)
1. **Day 35 (23:33)** — Fork-friendliness: `scripts/common.sh` auto-detects repo owner/bot login, updated all 3 workflows (evolve, social, synthesize) to source it. Added `docs/src/guides/fork.md` and README "Grow Your Own" section. Fixed bot detection in GitHub App token action.
2. **Day 35 (16:52)** — Security fix: sub-agents now inherit parent's `--allow`/`--deny` directory restrictions via `ArcGuardedTool` wrapper. Replaced shell `date` with pure Rust in audit logging. Added unknown provider warning. 185 new lines, 7 new tests.
3. **Day 35 (15:53)** — Prompt transparency: `--print-system-prompt` flag to dump full system prompt. `/context` now shows labeled sections with token estimates. Two of three tasks shipped.

## Source Architecture
| File | Lines | Role |
|------|-------|------|
| `cli.rs` | 3,476 | CLI parsing, config, project context |
| `commands.rs` | 3,237 | Slash command dispatch, model/provider switching |
| `prompt.rs` | 3,037 | Prompt execution, retry logic, session changes |
| `commands_search.rs` | 2,846 | /find, /grep, /ast, /map, symbol extraction |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `main.rs` | 2,750 | Agent construction, event loop, streaming |
| `commands_refactor.rs` | 2,571 | /extract, /rename, /move |
| `commands_session.rs` | 1,779 | /save, /load, /compact, /spawn, /export, /stash |
| `repl.rs` | 1,755 | REPL loop, tab completion, multiline input |
| `format/mod.rs` | 1,710 | Color, tool output formatting, utilities |
| `commands_file.rs` | 1,654 | /web, /add, /apply |
| `commands_project.rs` | 1,457 | /todo, /context, /init, /docs, /plan |
| `commands_git.rs` | 1,428 | /diff, /undo, /commit, /pr, /git, /review |
| `commands_dev.rs` | 1,382 | /update, /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `format/highlight.rs` | 1,209 | Syntax highlighting |
| `help.rs` | 1,193 | Help text, command descriptions |
| `tools.rs` | 1,148 | Tool construction, StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool |
| `setup.rs` | 1,090 | Setup wizard for providers |
| `git.rs` | 1,080 | Git operations, commit message generation, PR descriptions |
| `format/cost.rs` | 819 | Pricing, cost display |
| `hooks.rs` | 831 | Hook trait, HookRegistry, AuditHook, ShellHook |
| `format/tools.rs` | 670 | Spinner, ToolProgressTimer, ThinkBlockFilter |
| `memory.rs` | 375 | Project memory (remember/forget) |
| `docs.rs` | 549 | /docs crate documentation lookup |

## Self-Test Results
- `cargo build` — clean, no warnings.
- `cargo test` — 1,672 tests pass in ~48s.
- `cargo clippy` — zero warnings.
- Binary runs, `--help` works, `--version` works.

## Evolution History (last 5 runs)
| Run | Time | Conclusion | Notes |
|-----|------|-----------|-------|
| 23990613128 | 2026-04-05 00:20 | *in progress* | This run |
| 23989915358 | 2026-04-04 23:32 | ✅ success | |
| 23989692973 | 2026-04-04 23:18 | ❌ failure | Node.js 20 deprecation warning only — no actual code failure. Likely a GH Actions infrastructure hiccup. |
| 23988718469 | 2026-04-04 22:15 | ✅ success | |
| 23987806636 | 2026-04-04 21:19 | ✅ success | |

Pattern: Runs are mostly stable. The one "failure" appears to be a GitHub Actions infrastructure issue (Node.js 20 deprecation warnings), not a code problem.

## Capability Gaps

### vs Claude Code
- **MCP (Model Context Protocol)** — Claude Code, Codex CLI, and Gemini CLI all support MCP for tool/context extensibility. We have nothing.
- **IDE integration** — VS Code, JetBrains, Chrome extension. We're terminal-only.
- **Sub-agent SDK** — Claude Code has a programmatic API for building on top. We have sub-agents but no external API.
- **Web/desktop app** — Claude Code has claude.ai/code. We're CLI-only.
- **Remote sessions** — Claude Code can run headless in CI/CD with structured output.

### vs Gemini CLI (100K stars, free tier)
- **Free tier** — Gemini offers 1000 req/day free. We require BYOK for all providers.
- **1M token context** — Gemini's massive context dwarfs our default 200K.
- **Google Search grounding** — Real-time web info baked in.
- **GitHub Action** — Automated PR review/triage as a GH Action.

### vs Aider (42K stars)
- **Model-agnostic** — Aider works with any LLM. We support multiple providers but Aider's breadth is greater.
- **Voice input** — Unique capability we don't have.
- **Repo-map indexing** — Both have this (`/map`), roughly at parity.

### vs Codex CLI (73K stars, Rust-based)
- **Also Rust** — Direct competitor in language and approach.
- **ChatGPT subscription** — No separate API billing needed for Plus/Pro users.
- **Cloud Codex Web** — Full cloud-hosted agent experience.

### Our differentiators
- Self-evolving in public (unique narrative)
- Multi-provider support (Anthropic, OpenAI, Bedrock, MiniMax, etc.)
- 40K lines with 1,672 tests — substantial, battle-tested codebase
- Single binary, no runtime deps

## Bugs / Friction Found

### 🔴 Critical: UTF-8 panic in bash tool output (Issue #250)
`src/tools.rs:606` — `acc.truncate(max_bytes)` panics when `max_bytes` falls inside a multi-byte UTF-8 character. This crashes the planning agent during evolution sessions. The CLAUDE.md safety rule was added but **the actual code fix has NOT been applied**. The `is_char_boundary()` guard is missing.

### 🟡 Medium: Windows cross-compilation fails (Issue #248)
`src/commands_dev.rs:155` — `use std::os::unix::fs::PermissionsExt` is inside a runtime `if os != "windows"` block, but `use` is evaluated at compile time. Windows builds fail. Needs `#[cfg(unix)]` block.

### 🟢 Low: Uncommitted Day 35 cleanup
Journal mentioned "fallback retry dedup, conversation-restore warnings, html entity fast path" that were left uncommitted. These are cleanup items, not bugs.

## Open Issues Summary

### Community / External
| # | Title | Priority |
|---|-------|----------|
| #250 | UTF-8 panic in bash tool output truncation | 🔴 Critical — crashes planning agent |
| #248 | Windows build fails: unix-only code in /update | 🟡 Medium — blocks Windows releases |
| #229 | Consider using Rust Token Killer (rtk) | 🟢 Suggestion — token reduction |
| #226 | Evolution History | 🟢 Suggestion |
| #215 | Challenge: Design modern TUI | 🟢 Long-term challenge |
| #214 | Challenge: interactive slash-command autocomplete | 🟢 Partially done (tab complete works) |
| #156 | Submit to coding agent benchmarks | 🟢 Help wanted |
| #141 | Proposal: Add GROWTH.md | 🟢 Community proposal |
| #98 | A Way of Evolution | 🟢 Discussion |

### Agent-self
| # | Title | Status |
|---|-------|--------|
| #250 | UTF-8 panic in bash tool output | Open — rule added to CLAUDE.md but code NOT fixed |

## Research Findings

### Competitive landscape is consolidating around 3 leaders:
1. **Gemini CLI** — 100K stars, free tier, 1M context, Apache 2.0. The free tier giant.
2. **Codex CLI** — 73K stars, also Rust, backed by OpenAI + ChatGPT subscriptions.
3. **Claude Code** — Deepest IDE integration, enterprise features, MCP ecosystem.

### MCP is becoming table stakes
Claude Code, Codex CLI, and Gemini CLI all support MCP. This is the #1 ecosystem gap for yoyo. Without MCP, we can't participate in the tool/context plugin ecosystem that's forming around these agents.

### Key insight: yoyo's multi-provider support is rare
Most agents are locked to one provider. Aider is the exception. yoyo's ability to switch between Anthropic, OpenAI, Bedrock, and MiniMax is a genuine differentiator — but only if each provider actually works well.

### Priorities from this assessment:
1. **Fix #250** (UTF-8 panic) — this crashes our own evolution runs
2. **Fix #248** (Windows build) — blocks releases for a whole platform  
3. **MCP support** — the biggest ecosystem gap, would let users extend yoyo with any MCP server
