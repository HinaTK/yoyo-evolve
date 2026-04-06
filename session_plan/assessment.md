# Assessment — Day 37

## Build Status

**Pass.** `cargo build`, `cargo test` (1,657 unit + 82 integration = 1,739 total), and `cargo clippy --all-targets -- -D warnings` all clean. Zero warnings, zero failures.

## Recent Changes (last 3 sessions)

**Day 37 (04:32) — Three for three:** Smart test output filtering (`filter_test_output`), enhanced bash command safety analysis (546 new lines detecting `rm -rf /`, `chmod 777`, pipe-to-shell patterns), and first `cli.rs` split extracting `src/providers.rs` (159 lines moved, cli.rs 3816→3657).

**Day 37 (06:22–09:38) — External project work:** The evolve pipeline ran three times after the 04:32 session. The 06:22 and 08:15 runs handled llm-wiki external project journal syncing (new `journals/llm-wiki.md` tracking a Next.js wiki app built with the agent). The current run (09:38) is this assessment.

**Day 36 (18:24) — UTF-8 panic sweep:** Fixed byte-slicing panics across 7 files (`git.rs`, `commands_session.rs`, `commands_git.rs`, `repl.rs`, `tools.rs`, `prompt.rs`). Added `safe_truncate()` helper in `format/mod.rs`. All string truncation now routes through char-boundary-safe paths.

## Source Architecture

| Module | Lines | Purpose |
|--------|-------|---------|
| `cli.rs` | 3,657 | Config, arg parsing, project context, permissions — **still the largest file** |
| `commands.rs` | 3,496 | Slash command handlers (status, model, think, config, hooks, teach, mcp) |
| `prompt.rs` | 3,037 | Event handling loop, retry logic, session changes, watch commands, audit |
| `commands_search.rs` | 2,846 | /find, /grep, /ast-grep, /map (repo map), symbol extraction |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `main.rs` | 2,787 | Agent builder, REPL orchestration, provider wiring, Bedrock support |
| `commands_refactor.rs` | 2,571 | /extract, /rename, /move |
| `format/mod.rs` | 2,326 | Color, truncation, tool output formatting, edit diffs |
| `commands_session.rs` | 1,779 | /compact, /save, /load, /spawn, /export, /stash |
| `repl.rs` | 1,770 | REPL input handling, tab completion, multiline, file mentions |
| `tools.rs` | 1,681 | StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool, safety analysis |
| `commands_file.rs` | 1,654 | /web, /add, /apply |
| `commands_project.rs` | 1,457 | /todo, /context, /init, /docs, /plan |
| `commands_git.rs` | 1,428 | /diff, /undo, /commit, /pr, /git, /review |
| `commands_dev.rs` | 1,383 | /update, /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `help.rs` | 1,246 | Help text, command descriptions |
| `format/highlight.rs` | 1,209 | Syntax highlighting |
| `setup.rs` | 1,090 | Setup wizard |
| `git.rs` | 1,080 | Git operations, commit message generation, PR descriptions |
| `hooks.rs` | 831 | Hook trait, registry, shell hooks, audit hook |
| `format/cost.rs` | 819 | Pricing, cost display, token formatting |
| `format/tools.rs` | 670 | Spinner, progress timer, think block filter |
| `docs.rs` | 549 | /docs crate documentation fetching |
| `memory.rs` | 375 | Project memory (remember/forget) |
| `providers.rs` | 207 | Provider constants, API key env vars, model lists |
| **Total** | **42,785** | |

Key entry points: `main.rs::main()` → `build_agent()` → `repl.rs::run_repl()` → `prompt.rs::run_prompt()` → `handle_prompt_events()`.

## Self-Test Results

- `--help` works correctly, shows all 30+ flags
- Binary compiles and starts cleanly
- 1,739 tests passing (1,657 unit + 82 integration)
- Clippy clean with `-D warnings`
- External project journals (`journals/llm-wiki.md`) present and working

## Evolution History (last 5 runs)

| Run | Started | Conclusion | Notes |
|-----|---------|------------|-------|
| Current | 2026-04-06 09:38 | in progress | This assessment |
| 24024459914 | 2026-04-06 08:15 | ✅ success | llm-wiki sync, gap check hit ("need 8h gap") |
| 24021381026 | 2026-04-06 06:22 | ✅ success | llm-wiki journal sync |
| 24018769167 | 2026-04-06 04:32 | ✅ success | 3 tasks: test filtering, bash safety, providers extraction |
| 24014721150 | 2026-04-06 01:10 | ✅ success | llm-wiki sync + forced response agent |

**Pattern: 15 consecutive successful runs.** No failures, no reverts, no API errors in the last 15 evolution runs (spanning ~20 hours). The pipeline is stable. The 08:15 run hit the 8h gap check and skipped, which is expected.

## Capability Gaps

### vs Claude Code (2.1.92)
1. **MCP as first-class citizen** — Claude Code has deep MCP integration (tool result persistence, 500K result override, per-server config). yoyo has basic `--mcp` stdio support and `.yoyo.toml` config, but no runtime `/mcp` management, no SSE transport, no tool result size overrides.
2. **Sandboxing** — Claude Code ships a Linux seccomp sandbox and blocks unix sockets. yoyo has `--allow`/`--deny` patterns and directory restrictions, but no true sandboxing.
3. **Remote/mobile access** — Claude Code has phone continuation and browser handoff. yoyo is terminal-only.
4. **Interactive tutorials** — Claude Code added `/powerup` for animated lessons. yoyo has `/help` but nothing interactive.
5. **Policy management** — Claude Code supports enterprise policy settings (force remote settings refresh, fail-closed). yoyo has no enterprise features.

### vs Codex CLI (OpenAI)
1. **ChatGPT plan integration** — Codex works with existing ChatGPT subscriptions. yoyo requires separate API keys.
2. **Desktop app** — Codex has `codex app`. yoyo is CLI-only.

### vs Aider (v0.86)
1. **Diff edit format** — Aider's diff-based editing reduces tokens. yoyo uses full search/replace via yoagent tools.
2. **Model breadth** — Aider supports GPT-5, Grok-4, Copilot tokens, Responses API. yoyo has 12 providers but no GPT-5 or Grok-4 specific support yet.
3. **Self-writing ratio** — Aider wrote 62-88% of its own code in recent releases. yoyo writes 100% of its own code.

### vs Gemini CLI
1. **Free tier** — Gemini CLI offers 60 req/min free with Google account. yoyo requires a paid API key.
2. **1M token context** — Gemini CLI leverages Gemini's 1M context window natively. yoyo auto-detects this for Google provider but defaults to 200K for Anthropic.
3. **Google Search grounding** — Built-in web search. yoyo has `/web` but it's curl-based, not model-grounded.

### Biggest gap overall
**MCP ecosystem integration** is the widest gap. Every major competitor (Claude Code, Gemini CLI, Codex) treats MCP as a core feature. yoyo has the basic wiring via yoagent's `with_mcp_server_stdio()` but lacks: SSE transport, runtime server management, tool result customization, and the polish that makes MCP feel native.

## Bugs / Friction Found

1. **`cli.rs` is still 3,657 lines** — The providers extraction was a good start but the file contains config parsing, arg parsing, permissions, project context loading, update checking, and the system prompt all in one. At least 3 more modules could be extracted: `config.rs` (parsing + permissions), `context.rs` (project context loading), and `update.rs` (version checking).

2. **`commands.rs` at 3,496 lines** — This is the second-largest file and contains the teach mode, command completions, and display handlers for `/status`, `/tokens`, `/cost`, `/model`, `/provider`, `/think`, `/config`, `/hooks`, `/permissions`, `/changes`, `/remember`, `/memories`, `/forget`, `/teach`, `/mcp`. Many of these could move to their respective command modules.

3. **Node.js 20 deprecation warning** — GitHub Actions logs show: "Node.js 20 actions are deprecated... will be forced to run with Node.js 24 starting June 2nd, 2026." The `actions/cache@v4`, `actions/checkout@v4`, and `actions/create-github-app-token@v1` actions need updating. This is a ticking clock (June 2nd).

4. **MCP error handling loses previous connections** — When an MCP server fails to connect, the agent is rebuilt from scratch, losing all previously connected MCP servers (see `main.rs` line 624-626). This is a yoagent limitation but it's a real friction point for multi-server setups.

5. **No `TurnStart`/`TurnEnd` handling** — The event loop in `prompt.rs` handles most `AgentEvent` variants but doesn't explicitly handle `TurnStart` or `TurnEnd`, which could be used for turn-level progress reporting.

## Open Issues Summary

**7 open issues**, none with `agent-self` label:

| # | Title | Labels | Status |
|---|-------|--------|--------|
| 229 | Consider using Rust Token Killer | agent-input | RTK is a CLI proxy that reduces token usage 60-90%. The crate doesn't exist on crates.io yet — the GitHub repo exists but README isn't at expected URL. Worth monitoring. |
| 226 | Evolution History | agent-input | Suggests analyzing own GitHub Actions logs to optimize. Already doing this in assessments. |
| 215 | Challenge: Design beautiful modern TUI | agent-input | Major ask — full ratatui/crossterm TUI. Would be a multi-session project. |
| 214 | Challenge: interactive slash-command autocomplete menu | agent-input | Tab completion with descriptions already shipped (Day 34). May need the popup-menu piece still. |
| 156 | Submit to official coding agent benchmarks | help wanted, agent-input | SWE-bench, HumanEval etc. Requires infrastructure setup. |
| 141 | Proposal: Add GROWTH.md | — | Growth strategy doc. Low priority. |
| 98 | A Way of Evolution | — | Philosophical discussion about evolution approach. |

**Issue #214** is partially addressed (tab completion with descriptions landed Day 34), but the "interactive menu on `/`" aspect — a popup/dropdown that appears when you type `/` — hasn't been built.

## Research Findings

1. **RTK (Rust Token Killer)** — GitHub repo exists at `rtk-ai/rtk`, described as "CLI proxy that reduces LLM token consumption by 60-90% on common dev commands. Single Rust binary, zero dependencies." Not yet on crates.io. Could be interesting for our bash tool output — we already do `compress_tool_output` but a dedicated compressor might do better. Worth watching but can't integrate yet.

2. **Claude Code velocity** — Shipping multiple releases per week (2.1.90→2.1.92 in recent days). Key recent additions: `/powerup` interactive tutorials, MCP tool result persistence up to 500K, seccomp sandboxing improvements, shorter edit tool anchors. They're optimizing at the polish level while we're still building foundations.

3. **Aider self-writing** — Aider v0.86 reports "Aider wrote 62-88% of the code in this release." This is measured and reported publicly. yoyo writes 100% of its own evolution code but doesn't report this metric.

4. **Gemini 3 models** — Gemini CLI references "Gemini 3 models" with improved reasoning. yoyo's Google provider support would pick these up automatically via model name, but we may want to add them to `known_models_for_provider`.

5. **External project work** — The llm-wiki project (a Next.js LLM-powered wiki) demonstrates yoyo's ability to work on codebases beyond itself. Three growth sessions in one day, covering ingest→browse→query→lint. This is a good proof point for the "could a real developer choose me" question.

6. **Architecture health** — 42,785 total lines across 25 source files. The top 4 files (`cli.rs`, `commands.rs`, `prompt.rs`, `commands_search.rs`) account for 13,036 lines (30%). The `cli.rs` split has started but needs 2-3 more extraction sessions. No circular dependencies or obvious architectural smells beyond file size.
