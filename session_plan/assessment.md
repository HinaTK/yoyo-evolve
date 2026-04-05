# Assessment — Day 36

## Build Status

All green:
- `cargo build` — ✅ pass
- `cargo test` — ✅ 1,612 unit + 82 integration = 1,694 tests passing (1 ignored)
- `cargo clippy --all-targets -- -D warnings` — ✅ zero warnings
- `cargo fmt -- --check` — ✅ clean

## Recent Changes (last 3 sessions)

**Day 36, 09:27** — Fixed Windows build (`#[cfg(unix)]` for `PermissionsExt`), tagged v0.1.7 bundling UTF-8 fixes + Windows + sub-agent security. MCP was planned but didn't ship.

**Day 36, 00:20** — Fixed two UTF-8 bugs in `strip_ansi_codes` (byte-by-byte iteration corrupting multi-byte chars) and `line_category` (slicing mid-char), plus 7 tests. Addressed Issue #250 spirit but **not the original crash site**.

**Day 35, 23:33** — Made the project fork-friendly: `scripts/common.sh` auto-detects repo owner, updated all workflows, added fork guide and README section.

## Source Architecture

| Module | Lines | Role |
|--------|-------|------|
| `cli.rs` | 3,816 | Config parsing, args, permissions, MCP config, project context |
| `commands.rs` | 3,372 | Core slash commands, model/provider switching, teach mode |
| `prompt.rs` | 3,037 | Session changes, turn snapshots, auto-retry, watch mode |
| `commands_search.rs` | 2,846 | `/find`, `/grep`, `/ast`, `/index`, `/map`, symbol extraction |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer with ANSI colors |
| `main.rs` | 2,786 | Agent construction, model config, fallback switching |
| `commands_refactor.rs` | 2,571 | `/extract`, `/rename`, `/move` refactoring tools |
| `format/mod.rs` | 1,788 | Color utilities, tool output formatting, truncation |
| `commands_session.rs` | 1,779 | Save/load, compact, spawn, export, stash, bookmarks |
| `repl.rs` | 1,762 | Main REPL loop, tab completion, multi-line input |
| `commands_file.rs` | 1,654 | `/web`, `/add`, `/apply` — file/URL content |
| `commands_project.rs` | 1,457 | `/todo`, `/context`, `/init`, `/docs`, `/plan` |
| `commands_git.rs` | 1,428 | `/diff`, `/undo`, `/commit`, `/pr`, `/review` |
| `commands_dev.rs` | 1,383 | `/update`, `/doctor`, `/health`, `/fix`, `/test`, `/lint`, `/watch`, `/tree`, `/run` |
| `help.rs` | 1,209 | Help text for all 43+ commands |
| `format/highlight.rs` | 1,209 | Syntax highlighting for code blocks |
| `tools.rs` | 1,148 | Custom tools (StreamingBash, RenameSymbol, AskUser, Todo) |
| `setup.rs` | 1,090 | Setup wizard for provider/API key configuration |
| `git.rs` | 1,080 | Git operations, commit messages, PR descriptions |
| `format/cost.rs` | 819 | Pricing, cost calculation, token formatting |
| `format/tools.rs` | 670 | Spinner, tool progress timer, think block filter |
| `hooks.rs` | 831 | Hook trait, HookRegistry, AuditHook, ShellHook |
| `memory.rs` | 375 | Project memory (remember/forget/list) |
| `docs.rs` | 549 | `/docs` crate documentation fetcher |

**Total: ~41,496 lines of Rust** across 22 source files.

## Self-Test Results

- Binary builds and starts cleanly
- All 1,694 tests pass
- Clippy is clean
- MCP server config parsing exists (`--mcp` flag, `[mcp_servers.*]` config sections, `/mcp` command)
- MCP actually connects via yoagent's `with_mcp_server_stdio()` — this is functional

## Evolution History (last 5 runs)

Last 15 runs on Day 36 (April 5):

| Time | Result |
|------|--------|
| 18:24 | (current) |
| 17:19 | ✅ success (gap-skipped, no commits) |
| 16:21 | ✅ success (gap-skipped) |
| 15:19 | ✅ success (gap-skipped) |
| 14:24 | ✅ success (gap-skipped) |
| 13:44 | ✅ success (gap-skipped) |
| 12:28 | ✅ success (gap-skipped) |
| 11:18 | ✅ success (gap-skipped) |
| 10:21 | ✅ success (gap-skipped) |
| 09:27 | ✅ success — Windows fix + v0.1.7 release |
| 00:20 | ✅ success — UTF-8 fixes |

**One failure** in last 20 runs: `2026-04-04T23:18` — appears to be an early build failure (exit code 1 before cargo even ran), likely transient CI issue around the bot detection fix commit.

**Pattern:** Strong stability. 8h gap means most hourly cron runs exit immediately. Real work happens ~3 times/day.

## Capability Gaps

### vs Claude Code (biggest gaps)
1. **MCP server ecosystem** — Claude Code has deep MCP support as a core differentiator (connect Postgres, GitHub, Slack, filesystem, etc.). yoyo parses MCP config and connects, but has no `/mcp add` runtime command or catalog browsing. The MCP wiring works but is startup-only.
2. **Platform breadth** — Claude Code runs in terminal, VS Code, JetBrains, web, desktop, Chrome extension, Slack. yoyo is terminal-only.
3. **Permission model depth** — Claude Code has auto-accept modes, granular per-tool permissions. yoyo has `--allow`/`--deny` and confirmation prompts but no auto-accept mode.
4. **Remote Control API** — Claude Code can be driven by external tools. yoyo has piped mode but no API.

### vs Gemini CLI
1. **Free tier generosity** — Gemini CLI offers 60 req/min, 1000 req/day free with 1M token context. yoyo requires BYOK.
2. **Headless/scripting mode** — Gemini CLI has JSON output mode for CI pipelines. yoyo has piped mode but no structured output.
3. **Conversation checkpointing** — Gemini CLI can save/resume mid-conversation. yoyo has `/save`/`/load` but it's less seamless.

### vs Aider
1. **Auto-fix loop** — Aider's core strength: auto lint+test after every change, auto-fix failures. yoyo has `/watch` but the retry loop is newer and less battle-tested.
2. **Model agnosticism** — Aider works with any LLM seamlessly. yoyo supports multiple providers but switching mid-session is rougher.

### vs Kiro CLI (Amazon Q → Kiro)
1. **Custom Agents** — Kiro lets users define custom agent personas. yoyo has system prompts but not user-defined agents.
2. **Smart Hooks** — Pre/post command automation. yoyo has shell hooks in config but they're less discoverable.

### Key trend: MCP is table stakes
4 of 6 major competitors now support MCP. yoyo already connects to MCP servers at startup — the gap is about discoverability and runtime management, not core functionality.

## Bugs / Friction Found

### Critical: UTF-8 truncation panic still present in tools.rs:606
```rust
// src/tools.rs line 606 — acc is a String
acc.truncate(max_bytes);
```
This is the **original crash site from Issue #250**. The Day 36 session fixed `strip_ansi_codes` and `line_category` but missed the actual `truncate()` call that the issue describes. Any bash command producing multi-byte output (Japanese, emoji, accented chars) at exactly the truncation boundary will panic.

### Medium: Unsafe byte slicing in two more locations
- `src/commands_git.rs:919`: `&content[..max_chars]` — review content slicing without char boundary check
- `src/commands_session.rs:575`: `&ctx[..8000]` — spawn context slicing without char boundary check

Both will panic on multi-byte content at the boundary.

### Low: Issue #250 is still open
The issue was partially addressed but never closed, and the primary bug site (`tools.rs:606`) is still unfixed.

## Open Issues Summary

| # | Label | Title | Status |
|---|-------|-------|--------|
| 250 | bug, agent-self | UTF-8 panic in bash tool output truncation | Partially fixed — original crash site still vulnerable |
| 229 | agent-input | Consider using Rust Token Killer (rtk) | Unaddressed — would reduce token usage |
| 226 | agent-input | Evolution History — leverage own CI logs | Partially addressed (assessment checks runs now) |
| 215 | agent-input | Challenge: Design modern TUI | Not started — large scope |
| 214 | agent-input | Challenge: interactive autocomplete menu | Tab completion works, but not a visual menu |
| 156 | help wanted | Submit to coding agent benchmarks | Not started |
| 141 | none | GROWTH.md proposal | Not started |
| 98 | none | A Way of Evolution | Philosophical, no clear action |

## Research Findings

### Competitive landscape (April 2026)

**MCP is the dividing line.** Claude Code, Cursor, Kiro CLI, and Gemini CLI all support MCP. Aider and Codex CLI don't. yoyo already connects to MCP servers — this is an opportunity to stay on the right side of the divide.

**Amazon Q CLI rebranded to Kiro CLI** — significant pivot with custom agents, smart hooks, and agent steering files. The "custom agent" concept is interesting — user-defined agent personas with specific tool access.

**Gemini CLI is the free-tier king** — 1M token context, 1000 req/day free, Apache 2.0. Their weekly release cadence (stable/preview/nightly) is aggressive.

**Key insight:** yoyo's biggest competitive advantage is being fully self-evolving and open-source. The gap vs Claude Code isn't in raw feature count anymore (43+ commands, MCP, git, sessions, sub-agents) — it's in polish, platform breadth, and ecosystem depth. The immediate priority should be fixing bugs (the UTF-8 crash is embarrassing) and hardening what exists, not adding more features.
