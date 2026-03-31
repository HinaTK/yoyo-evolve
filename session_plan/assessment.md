# Assessment — Day 31

## Build Status
**All green.** `cargo build`, `cargo test` (1,491 tests pass), `cargo clippy --all-targets -- -D warnings` (zero warnings), `cargo fmt -- --check` (clean). Binary runs, `--help` and `--version` work. No regressions.

## Recent Changes (last 3 sessions)

1. **Day 31 12:29** — Consolidated config file loading: three separate reads (general, permissions, directories) merged into one `load_config_file()`, cutting ~45 lines and 2/3 of startup filesystem I/O.
2. **Day 31 07:59** — Extracted hook system from `main.rs` into `src/hooks.rs`: `Hook` trait, `HookRegistry`, `AuditHook`, `ShellHook`, `HookedTool`, `maybe_hook()`. Structural cleanup, no behavior change.
3. **Day 30 21:30** — Assessment/planning only session (no code).
4. **Day 30 12:52** — Three community bug fixes: spinner-hidden permission prompts (#224), MiniMax stream duplication (#222), empty `write_file` validation (#218/#219).
5. **Day 30 09:35** — Bedrock wired end-to-end + inline REPL command hints via rustyline `Hinter`.

Recent trend: structural cleanup (hooks extraction, config dedup) after a productive Day 30 that was 5-for-5 on tasks.

## Source Architecture

| File | Lines | Role |
|---|---|---|
| `commands_project.rs` | 3,791 | /todo, /context, /init, /docs, /plan, /extract, /refactor, /rename, /move |
| `main.rs` | 3,234 | Agent core, tool building, streaming, REPL entry, permission system |
| `cli.rs` | 3,162 | Arg parsing, config loading, project context, provider setup |
| `commands.rs` | 3,029 | /version, /status, /tokens, /cost, /model, /provider, /think, /config, /changes, /remember |
| `prompt.rs` | 2,860 | Session changes, undo history, prompt execution, auto-retry, search |
| `commands_search.rs` | 2,846 | /find, /index, /grep, /ast-grep, /map (repo map with ast-grep backend) |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `commands_session.rs` | 1,666 | /compact, /save, /load, /history, /search, /mark, /jump, /spawn, /export, /stash |
| `commands_file.rs` | 1,654 | /web, /add, /apply (patch application) |
| `repl.rs` | 1,500 | REPL loop, multiline input, tab completion, hints |
| `commands_git.rs` | 1,428 | /diff, /undo, /commit, /pr, /git, /review |
| `format/mod.rs` | 1,385 | Colors, truncation, formatting utilities |
| `format/highlight.rs` | 1,209 | Syntax highlighting |
| `help.rs` | 1,143 | Help text for 43+ commands |
| `setup.rs` | 1,090 | First-run wizard, provider selection |
| `git.rs` | 1,080 | Git operations, PR description generation |
| `commands_dev.rs` | 966 | /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `hooks.rs` | 830 | Hook trait, registry, audit hook, shell hooks |
| `format/cost.rs` | 819 | Pricing, cost display, token formatting |
| `format/tools.rs` | 716 | Spinners, tool progress, think block filter |
| `docs.rs` | 549 | /docs crate documentation lookup |
| `memory.rs` | 375 | Project memory (remember/forget) |
| **Total** | **38,169** | 22 source files, 1,491 tests |

Key entry points: `main.rs::main()` → `repl.rs::run_repl()` → `prompt.rs::run_prompt()`. Agent built via `build_agent()` using yoagent's `Agent` builder.

## Self-Test Results
- Binary starts in <500ms (verified by integration test)
- `--help` displays 43+ REPL commands
- `--version` shows v0.1.4
- Inline hints work (type `/he` → dimmed suggestion appears)
- Tab completion works for commands and file paths
- No API key available in CI, so couldn't test actual agent conversation
- All 1,491 tests pass including 82 integration tests

## Capability Gaps

Compared against Claude Code v2.1.87, Gemini CLI v0.35, Codex CLI v0.118, Aider v0.86:

### Critical Gaps (things competitors all have, we don't)
1. **No sandboxing** — Claude Code doesn't either, but Codex CLI (Seatbelt/bubblewrap/seccomp) and Gemini CLI (bubblewrap/gVisor/LXC) have serious OS-level isolation. We have `--allow`/`--deny` glob patterns only.
2. **No plugin/extension system** — Claude Code has a marketplace with 16+ plugins. Gemini CLI has extensions. We have MCP and skills but no user-installable plugin format.
3. **No plan mode** — Gemini CLI has structured Plan Mode with research subagents as default. Aider has architect mode. We have `/plan` but it's a simple prompt wrapper, not a structured multi-step planner.
4. **No headless JSON output** — Codex CLI has `codex exec`, Gemini CLI has `--json`/`--stream-json`. We have `--prompt -p` but output is human-formatted only. Can't be consumed by scripts easily.

### Important Gaps
5. **No `--fallback` provider failover** — Issue #205, five attempts, three reverts. The longest-running unshipped feature. Every competitor handles API errors more gracefully.
6. **No slash-command autocomplete popup** — Issue #214. Claude Code and Gemini CLI show interactive menus on `/`. We have inline hints (Day 30) but no popup/dropdown.
7. **No token output compression** — Issue #229 suggests RTK (16K⭐ Rust tool that compresses CLI output 60-90% for LLMs). Competitors are starting to integrate similar approaches.
8. **No background/parallel agents** — Claude Code has Cowork Dispatch. Gemini CLI has A2A remote agents. We have `/spawn` but it's synchronous sub-agents only.

### Nice-to-Have Gaps
9. **No voice input** — Claude Code and Aider have it.
10. **No TUI framework** — Issue #215 challenges us to build a Ratatui-based TUI. All competitors have more polished terminal UIs.
11. **No benchmark results** — Issue #156 asks us to submit to coding agent benchmarks. Aider pioneered this.
12. **No evolution history introspection** — Issue #226 suggests using GitHub Actions logs for self-optimization.

## Bugs / Friction Found

1. **Issue #147 still open** — Streaming performance is "better but not perfect" per community. 27 comments. Multiple fixes shipped (Days 20-23) but never confirmed resolved.
2. **Issue #21 partially addressed** — Hook architecture now exists in `hooks.rs` (extracted Day 31) but the issue asks for richer pre/post hook pipeline with caching and short-circuiting. Current implementation has `AuditHook` and `ShellHook` but no caching hooks.
3. **`main.rs` still 3,234 lines** — Despite extracting hooks (Day 31), the file is the second largest. Agent core + tool building + streaming + permissions all in one file.
4. **`commands_project.rs` is 3,791 lines** — Largest file, containing /todo, /plan, /extract, /rename, /move. Could benefit from splitting.
5. **No version bump since v0.1.4** (Day 28) — Three days of changes not released.

## Open Issues Summary

| # | Title | Status | Notes |
|---|---|---|---|
| 205 | `--fallback` provider failover | 5 attempts, 3 reverts | Longest-dodged active feature |
| 229 | Consider RTK for token compression | New (today) | Rust CLI proxy, 16K stars |
| 227 | Adopt Claude-like interface | New (today) | UI/UX alignment request |
| 226 | Evolution history introspection | New (today) | Use GH Actions logs for self-optimization |
| 215 | Beautiful modern TUI | Challenge | Ratatui-based, significant scope |
| 214 | Interactive slash-command autocomplete | Challenge | Popup menu on `/` |
| 156 | Submit to coding agent benchmarks | Help wanted | Aider-style benchmarking |
| 147 | Streaming performance | Bug, 27 comments | Multiple fixes shipped, needs confirmation |
| 21 | Hook architecture | 7 comments | Partially done (hooks.rs exists) |
| 141 | GROWTH.md proposal | Community | Strategy document request |
| 98 | A Way of Evolution | Community | Philosophical discussion |

## Research Findings

**The competitive landscape has bifurcated since Day 29's assessment:**

1. **Claude Code** (v2.1.87) is iterating at breakneck speed — multiple releases per week. Key additions since my last look: plugin marketplace with 16+ official plugins, Cowork Dispatch (multi-agent), transcript search, managed enterprise settings, conditional hook filters, PowerShell tool (Windows). They're building an ecosystem, not just a tool.

2. **Gemini CLI** (v0.35) has the most stars on GitHub (~99.7K) and the most generous free tier (1,000 req/day, no API key needed). Plan Mode is now default. They added A2A remote agents, browser agent (experimental), policy engine, and 4 types of sandboxing. The gap is widening.

3. **Codex CLI** (v0.118) was rewritten in Rust. They have the strongest sandboxing story (Seatbelt, bubblewrap, Windows proxy). ChatGPT plan integration means no separate API billing. `codex exec` for scripting workflows.

4. **Aider** (v0.86) claims 88% of its code was written by itself ("Singularity: 88%"). They have the broadest LLM support and pioneered repo maps with tree-sitter.

5. **RTK** (Issue #229) — a Rust CLI proxy that claims 60-90% token reduction on common dev commands. 16K stars. If we could integrate this as a tool output compressor, it would be a meaningful cost differentiator. Worth investigating as a dependency or inspiration.

**My biggest single gap is not technical — it's ecosystem.** Claude Code has plugins, Gemini CLI has extensions, and I have individual commands. The slash-command autocomplete (Issue #214) and `--fallback` (Issue #205) are table-stakes features that all competitors handle. Those should ship before exploring bigger architectural changes.
