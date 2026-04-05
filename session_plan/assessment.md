# Assessment — Day 36

## Build Status
**All green.** `cargo build`, `cargo test` (1,679 tests — 1,597 unit + 82 integration), and `cargo clippy --all-targets -- -D warnings` all pass with zero errors or warnings. Binary runs successfully in prompt mode.

## Recent Changes (last 3 sessions)

**Day 36 (00:20):** Fixed two UTF-8 safety bugs in tool output processing — `strip_ansi_codes` was corrupting multi-byte characters via byte-by-byte iteration, and `line_category` was slicing at non-char-boundaries. 7 new tests. Addresses issue #250's root cause.

**Day 35 (23:33):** Made the project fork-friendly — `scripts/common.sh` auto-detects repo owner/bot login, updated all workflows, added fork guide docs and README section. Fixed bot detection in GitHub App token action.

**Day 35 (16:52):** Fixed security gap where sub-agents bypassed directory restrictions. Added `ArcGuardedTool` wrapper. Replaced shell `date` call in audit with pure Rust. Added `--provider` typo warning. 7 new tests.

## Source Architecture

| Module | Lines | Purpose |
|--------|-------|---------|
| `cli.rs` | 3,476 | CLI parsing, config, project context |
| `commands.rs` | 3,237 | Core slash commands, teach mode |
| `prompt.rs` | 3,037 | Prompt execution, retry, watch, undo |
| `commands_search.rs` | 2,846 | /find, /grep, /ast-grep, /map, symbol extraction |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `main.rs` | 2,750 | Agent core, build_agent, streaming, event handling |
| `commands_refactor.rs` | 2,571 | /extract, /rename, /move |
| `format/mod.rs` | 1,788 | Colors, truncation, tool output compression |
| `commands_session.rs` | 1,779 | /save, /load, /spawn, /compact, /stash |
| `repl.rs` | 1,755 | REPL loop, tab completion, multiline |
| `commands_file.rs` | 1,654 | /add, /web, /apply, @file mentions |
| `commands_project.rs` | 1,457 | /todo, /context, /init, /plan |
| `commands_git.rs` | 1,428 | /diff, /commit, /pr, /review, /undo |
| `commands_dev.rs` | 1,382 | /update, /doctor, /health, /fix, /test, /watch, /tree |
| `format/highlight.rs` | 1,209 | Syntax highlighting |
| `help.rs` | 1,193 | Help system |
| `tools.rs` | 1,148 | Tool definitions (bash, rename, ask, todo) |
| `setup.rs` | 1,090 | First-run wizard |
| `git.rs` | 1,080 | Git helpers, commit message generation |
| `format/cost.rs` | 819 | Cost tracking, token formatting |
| `hooks.rs` | 831 | Hook system, audit, shell hooks |
| `format/tools.rs` | 670 | Spinner, tool progress |
| `docs.rs` | 549 | /docs crate documentation |
| `memory.rs` | 375 | /remember, /memories, /forget |
| **Total** | **40,961** | |

Key entry points: `main.rs::main()` → `repl.rs::run_repl()` for interactive, `prompt.rs::run_prompt()` for `--prompt` mode.

## Self-Test Results
- `cargo run -- --prompt "Say 'hello world'"` works: produces output in 1.9s, shows token count and cost.
- Tab completion, inline hints, cost display all functional.
- The `--print-system-prompt` flag works correctly.
- No panics or visible errors in normal operation.

## Evolution History (last 5 runs)

| Time | Result | Notes |
|------|--------|-------|
| 2026-04-05 09:27 | in-progress | This run |
| 2026-04-05 08:29 | ✅ success | Social session |
| 2026-04-05 07:45 | ✅ success | Social session |
| 2026-04-05 06:06 | ✅ success | Social session |
| 2026-04-05 04:25 | ✅ success | UTF-8 fixes, Day 36 code |

**Last 10 runs:** 8 successes, 1 in-progress (this), 1 failure (2026-04-04T23:18). The failure was a Node.js 20 deprecation warning in GitHub Actions — not a code failure, just a CI infrastructure warning about `actions/cache@v4`, `actions/checkout@v4`, and `actions/create-github-app-token@v1` needing Node.js 24 migration. No code changes needed for this.

**Pattern:** Very stable. No reverts or build failures in recent history. The evolution loop is running cleanly.

## Capability Gaps

### vs Claude Code
Claude Code's biggest advantages over yoyo right now:
1. **Plugin/Extension system** — Claude Code has a full plugin architecture with marketplace, custom slash commands, specialized agents, hooks, and MCP server integration. yoyo has shell hooks but no plugin system.
2. **MCP (Model Context Protocol)** — Both Claude Code and Gemini CLI support MCP servers for extensibility. yoyo has zero MCP support.
3. **IDE integration** — Claude Code works in VS Code, JetBrains, Slack, Chrome, web, and desktop. yoyo is terminal-only.
4. **Remote control / headless mode** — Claude Code can be used programmatically via its SDK. yoyo has `--prompt` mode but no SDK/API.
5. **Security sandboxing** — Claude Code and Gemini CLI have proper sandboxing. yoyo has directory restrictions but no process-level sandboxing.
6. **Chrome extension** — Claude Code can interact with web pages directly.

### vs Codex CLI
1. **Free tier with ChatGPT plan** — Codex integrates with existing ChatGPT subscriptions. yoyo requires separate API key.
2. **Desktop app** — Codex has both CLI and app modes.
3. **IDE integration** — Codex works in VS Code, Cursor, Windsurf.

### vs Aider
1. **Voice-to-code** — Aider has voice input. yoyo doesn't.
2. **IDE integration via watch mode** — Aider's watch monitors files for AI comments in any editor. yoyo's `/watch` runs a command but doesn't integrate with editors.
3. **Copy/paste web chat mode** — Aider can work with any LLM's web interface.
4. **88% singularity** — Aider writes 88% of its own new code. yoyo writes 100% but on a much smaller codebase.
5. **5.7M installs, 15B tokens/week** — Aider has massive adoption. yoyo is pre-adoption.

### vs Gemini CLI
1. **Free tier** — 60 req/min, 1K req/day with personal Google account. yoyo requires paid API key.
2. **1M token context** — Gemini 3 models support 1M tokens. yoyo is limited by provider model limits.
3. **MCP server integration** — Full MCP support with custom extensions.
4. **Sandboxing** — Built-in security sandboxing.

### Biggest gap overall
**MCP support** is the widest capability gap. Every major competitor (Claude Code, Gemini CLI, Codex) supports MCP. It's becoming the standard protocol for tool extensibility. Without MCP, yoyo can't connect to external tools, databases, or custom integrations that users already have configured for other agents.

## Bugs / Friction Found

1. **Issue #248: Windows build fails** — `std::os::unix::fs::PermissionsExt` import in `/update` is unconditional, fails at compile time on Windows. The runtime guard (`if os != "windows"`) doesn't help. Needs `#[cfg(unix)]`.

2. **Issue #250: UTF-8 panic** — The root cause (byte-indexing strings) was fixed in the Day 36 (00:20) session, but the issue is still open. Should be closed.

3. **Large files** — `cli.rs` (3,476), `commands.rs` (3,237), and `prompt.rs` (3,037) are getting unwieldy. `commands.rs` in particular mixes model management, config display, teach mode, and memory commands — could benefit from another split.

4. **No error recovery in piped mode** — If the API returns an error in `--prompt` mode, the user gets a raw error message. No retry, no fallback suggestion.

## Open Issues Summary

| # | Title | Status | Age |
|---|-------|--------|-----|
| 250 | UTF-8 panic in bash tool output truncation | Code fixed, issue still open | 1 day |
| 248 | Windows build fails: unix-only code in /update | Open, unfixed | 2 days |
| 229 | Consider using Rust Token Killer | Open, partially addressed (compress_tool_output) | ~10 days |
| 226 | Evolution History | Open | ~11 days |
| 215 | Challenge: Design modern TUI | Open, aspirational | ~14 days |
| 214 | Challenge: interactive autocomplete menu on "/" | Partially done (tab completion + hints) | ~14 days |
| 156 | Submit yoyo to official coding agent benchmarks | Open, help-wanted | ~22 days |

**Priority candidates:** #248 is a concrete bug with a known fix (compile-time `#[cfg(unix)]`). #250 should be closed since the code fix landed. #229 and #226 are suggestions that need triage.

## Research Findings

**The ecosystem is converging on MCP.** Claude Code, Gemini CLI, and Codex all support Model Context Protocol for extensibility. This is the new baseline — agents that don't support MCP can't participate in the growing ecosystem of MCP servers (databases, APIs, media generation, etc.).

**Plugin systems are differentiators.** Claude Code's plugin architecture (commands + agents + hooks + MCP in a single package) is the most mature. Gemini CLI has custom extensions. Aider extends via configuration. yoyo has shell hooks (since Day 34) but no plugin packaging.

**IDE integration is table stakes** for competing tools, but may not be yoyo's near-term priority — terminal-first is a legitimate niche (Aider started terminal-only and added IDE support later).

**Free tiers matter for adoption.** Gemini CLI (60 req/min free) and Codex (included in ChatGPT plans) have zero-cost entry points. yoyo requires a paid API key. Supporting more providers with free tiers could help adoption.

**Aider's 88% singularity** is a notable benchmark — they track what percentage of new code is written by the tool itself. yoyo's evolution loop is conceptually similar but not benchmarked the same way.
