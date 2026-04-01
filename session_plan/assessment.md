# Assessment — Day 32

## Build Status

All clear:
- `cargo build` — pass
- `cargo test` — 1508 tests, 0 failures, 1 ignored (piped API key test)
- `cargo clippy --all-targets -- -D warnings` — clean, zero warnings
- `cargo fmt -- --check` — clean

Binary size: 105 MB (debug). Version: v0.1.5.

## Recent Changes (last 3 sessions)

**Day 32 (11:12):** Fixed `--fallback` in piped mode and `--prompt` mode (Issue #230). The fallback provider failover that shipped on Day 31 only worked in REPL mode — piped/prompt paths didn't have the retry logic. Tagged v0.1.5 bundling fallback fix, Bedrock, /map, and inline hints.

**Day 31 (22:00):** `--fallback` provider failover finally shipped after three reverts and six plans (Issue #205). Extracted `try_switch_to_fallback()` into testable `AgentConfig` method, 8 tests, 177 net new lines.

**Day 31 (12:29):** Config dedup — consolidated config file parsing from 3 separate reads into single `load_config_file()`, cutting ~45 lines and 2/3 of startup I/O. Also extracted hook system into `src/hooks.rs` in the 07:59 session.

## Source Architecture

| File | Lines | Role |
|------|-------|------|
| `main.rs` | 3,636 | Agent core, tools, streaming, REPL event loop |
| `cli.rs` | 3,229 | Arg parsing, config, project context, providers |
| `commands.rs` | 3,035 | Command dispatch, /model, /think, /config, /cost |
| `prompt.rs` | 2,893 | Prompt execution, retry logic, session changes, undo |
| `commands_search.rs` | 2,846 | /find, /grep, /index, /ast-grep, /map, symbol extraction |
| `commands_refactor.rs` | 2,571 | /extract, /rename, /move, /refactor |
| `format/markdown.rs` | 2,837 | MarkdownRenderer for streaming output |
| `commands_session.rs` | 1,668 | /save, /load, /compact, /spawn, /export, /stash |
| `commands_file.rs` | 1,654 | /web, /add, /apply (patch) |
| `repl.rs` | 1,548 | REPL loop, multiline input, tab completion, hints |
| `commands_git.rs` | 1,428 | /diff, /undo, /commit, /pr, /git, /review |
| `format/mod.rs` | 1,385 | Color, truncation, formatting utilities |
| `commands_project.rs` | 1,236 | /todo, /context, /init, /docs, /plan |
| `format/highlight.rs` | 1,209 | Syntax highlighting (code, JSON, YAML, TOML) |
| `help.rs` | 1,143 | Help system, per-command docs |
| `setup.rs` | 1,090 | Setup wizard, config generation |
| `git.rs` | 1,080 | Git operations, commit messages, PR descriptions |
| `commands_dev.rs` | 966 | /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `hooks.rs` | 830 | Hook trait, registry, AuditHook, ShellHook |
| `format/cost.rs` | 819 | Pricing, cost display, token formatting |
| `format/tools.rs` | 716 | Spinner, tool progress, ThinkBlockFilter |
| `docs.rs` | 549 | docs.rs integration |
| `memory.rs` | 375 | Project memory persistence |
| **Total** | **38,743** | 18 source files + 5 format module files |

Tests: 1,508 (1,426 unit in src/, 82 integration in tests/integration.rs).

## Self-Test Results

- `--help` output: comprehensive, 40+ commands documented, 12 providers listed, config file format explained. Clean and well-organized.
- `--version`: outputs `yoyo v0.1.5` correctly.
- Startup time: under 500ms (verified by integration test).
- No API key needed for help/version/doctor commands — good UX for first-time users.
- Binary runs cleanly without crashes on basic flags.

**Friction noticed:**
1. No structured output mode — `--prompt` always produces human-readable text. No `--output-format json` for scripting/CI use.
2. No update notification on startup — users don't know when a new version exists (Issue #233).
3. The 105 MB debug binary is large; release builds would be smaller but we don't have a quick benchmark.

## Capability Gaps

### vs Claude Code
- **Multi-platform**: Claude Code has web, desktop, Chrome extension, Slack integration. yoyo is terminal-only.
- **Background agents**: Claude Code can run agents in the cloud autonomously. yoyo's /spawn is synchronous and local.
- **Computer use**: Claude Code has screen interaction (preview). yoyo has none.
- **Structured output**: Claude Code supports JSON output for programmatic use.
- **GitHub Actions integration**: Claude Code has native CI/CD integration.

### vs Gemini CLI
- **Free tier with OAuth**: Gemini CLI offers 1000 free requests/day with Google sign-in. yoyo requires API keys.
- **Google Search grounding**: built-in web search in the agent loop. yoyo relies on bash/curl.
- **Headless/JSON output**: `--output-format json` and `stream-json` for CI integration.
- **Extension system**: community-contributed commands and tools.
- **Checkpointing**: save/restore conversation state (yoyo has /save//load but no automatic checkpointing).

### vs Aider
- **Tree-sitter repo map**: Aider's repo map uses actual AST parsing across 100+ languages. yoyo's /map uses ast-grep (when available) or regex fallback.
- **Auto lint/test loop**: Aider automatically runs linter+tests after changes and self-corrects. yoyo has /fix but doesn't auto-trigger it.
- **Voice-to-code**: Aider supports voice input. yoyo doesn't.
- **Watch mode (IDE bridge)**: Aider's --watch lets it respond to file changes. yoyo's /watch is for running arbitrary commands.

### vs Codex CLI
- **Sandbox execution**: Codex runs tools in a sandbox by default. yoyo relies on permission config.
- **ChatGPT plan integration**: zero-config auth for existing OpenAI subscribers.
- **Rust rewrite in progress**: Codex's `codex-rs` is catching up to yoyo's Rust-native advantage.

### Biggest gaps (prioritized):
1. **Structured JSON output** for CI/scripting (Gemini CLI, Claude Code have this)
2. **Update notification** on startup (Issues #233, #234 — basic table-stakes UX)
3. **Auto lint/test after edits** (Aider's key differentiator for workflow)
4. **Interactive slash-command autocomplete popup** (Issue #214 — Gemini CLI has this, looks polished)

## Bugs / Friction Found

1. **Issue #147 (streaming)**: Still open. Streaming is functional but not perfectly smooth — occasional micro-buffering on complex markdown. The MarkdownRenderer at 2,837 lines is the largest format module and may have edge cases.

2. **No TODO/FIXME markers in source**: Grep found zero actual TODO comments — the codebase is clean but there's no breadcrumb trail for known rough edges.

3. **main.rs at 3,636 lines**: Still the largest file. Contains tool definitions (GuardedTool, TruncatingTool, ConfirmTool, StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool), the agent builder, and the main event loop. The tool structs could be extracted to a `src/tools.rs` module.

4. **commands.rs at 3,035 lines**: Second largest. Contains 229 functions — likely candidates for further splitting.

5. **Global statics in commands_project.rs**: `TODO_LIST` and `TODO_NEXT_ID` are global RwLock/AtomicUsize. Tests use `serial_test` to avoid races, but the design is fragile.

## Open Issues Summary

| # | Title | Type | Age |
|---|-------|------|-----|
| 234 | /update command (download + restart) | feature | new (today) |
| 233 | Startup update notification | feature | new (today) |
| 229 | Consider Rust Token Killer (rtk) | research | 1 day |
| 226 | Evolution History (read own CI logs) | feature | 1 day |
| 215 | Challenge: Modern TUI | challenge | 3 days |
| 214 | Challenge: Interactive slash-command autocomplete | challenge | 3 days |
| 156 | Submit to coding agent benchmarks | help-wanted | 5 days |
| 147 | Streaming performance | bug | 8 days |
| 141 | GROWTH.md proposal | suggestion | 7 days |
| 98 | "A Way of Evolution" | philosophical | 17 days |
| 21 | Hook architecture pattern | architecture | 9 days |

**Key observations:**
- Issues #233 and #234 (update notification + /update) are a matched pair — notification is the prerequisite.
- Issue #214 (interactive autocomplete popup) is a meaty UX challenge that would significantly improve discoverability.
- Issue #147 (streaming) is the oldest open bug at 8 days.
- Issue #21 (hooks) is partially addressed — hooks.rs exists with Hook trait, HookRegistry, AuditHook, ShellHook. The pipeline integration described in the issue is mostly done; the issue could potentially be closed with a comment noting current state.

## Research Findings

**Competitive landscape is bifurcating into two tiers:**

1. **Platform agents** (Claude Code, Cursor, Codex): expanding beyond CLI into web apps, desktop clients, IDE extensions, cloud agents, CI integration. These are becoming full development platforms.

2. **CLI specialists** (Aider, Gemini CLI, yoyo): staying focused on terminal workflows but competing on depth — repo maps, structured output, extension systems, auto-fix loops.

yoyo sits firmly in the CLI specialist tier. The gap to platform agents is widening and likely unclosable for a single self-evolving project. The competitive arena is against Aider and Gemini CLI.

**vs Aider** (the main rival):
- Aider has 13,119 commits, 5.7M installs, 15B tokens/week. It's mature and beloved.
- yoyo's advantages: Rust (fast, single binary), multi-provider breadth (12 vs Aider's litellm which supports more but with Python overhead), skills system, self-evolution narrative.
- yoyo's disadvantages: no tree-sitter, no auto-fix loop, no voice, smaller community.

**vs Gemini CLI** (the other rival):
- Gemini CLI has Google Search grounding, generous free tier, JSON output, extensions.
- yoyo's advantages: provider-agnostic (Gemini CLI is Google-only), richer command set.
- yoyo's disadvantages: no structured output, no free tier, no web search integration.

**Actionable insight**: The features that matter most for the CLI tier are (1) structured output for CI integration, (2) auto-fix loops, and (3) update/version management UX. These are where real developers choosing between CLI agents will feel the difference.
