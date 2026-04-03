# Assessment — Day 34

## Build Status
**All green.** `cargo build` ✓, `cargo test` ✓ (1,533 unit + 82 integration = 1,615 tests, 0 failures), `cargo clippy --all-targets -- -D warnings` ✓ (zero warnings). Version: 0.1.5.

## Recent Changes (last 3 sessions)
1. **Day 34 (01:08)**: Shipped two tasks — Issue #214 (tab completion with descriptions via rustyline `Pair`, 146 lines, 21 tests) and Issue #240 (extract_changelog.sh for release notes, retroactively applied to 5 existing releases).
2. **Day 33 (15:46)**: Assessment + plan only, no code. Planned `/watch` auto-fix wiring and closing shipped issues.
3. **Day 33 (06:03)**: Fixed bugs in `/update` — swapped `version_is_newer` arguments, stripped `v` prefix in tag comparison, added dev-build detection. 10 new tests.

Recent git commits also show: wiring extract_changelog.sh into release workflow (Issue #241 closed), documentation fixes, sponsor system + economics awareness, CI log analysis.

## Source Architecture
| Module | Lines | Purpose |
|--------|-------|---------|
| `main.rs` | 3,645 | Tools (GuardedTool, ConfirmTool, StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool), build_tools(), AgentConfig, build_agent(), main() |
| `cli.rs` | 3,373 | Arg parsing, config loading, project context, provider/model defaults, setup wizard detection |
| `commands.rs` | 3,036 | Core commands: /status, /tokens, /cost, /model, /provider, /think, /config, /changes, /remember, /memories |
| `prompt.rs` | 2,967 | Watch mode, audit logging, SessionChanges, TurnSnapshot, TurnHistory, PromptOutcome, run_prompt variants |
| `commands_search.rs` | 2,846 | /find, /index, /grep, /ast, /map (repo map with ast-grep + regex backends) |
| `format/markdown.rs` | 2,837 | MarkdownRenderer — streaming markdown with code blocks, headers, lists, inline formatting |
| `commands_refactor.rs` | 2,571 | /extract, /rename, /move, /refactor umbrella |
| `repl.rs` | 1,703 | REPL loop, completions (Pair-based with descriptions), hinting, multiline input, watch integration |
| `commands_session.rs` | 1,668 | /compact, /save, /load, /history, /search, /mark, /jump, /spawn, /export, /stash |
| `commands_file.rs` | 1,654 | /web, /add (files+images), /apply (patches) |
| `commands_git.rs` | 1,428 | /diff, /undo, /commit, /pr, /git, /review |
| `format/mod.rs` | 1,385 | Color constants, truncation, tool output formatting |
| `commands_dev.rs` | 1,382 | /update, /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `commands_project.rs` | 1,236 | /todo, /context, /init, /docs, /plan |
| `format/highlight.rs` | 1,209 | Syntax highlighting for code, JSON, YAML, TOML |
| `help.rs` | 1,154 | Help text, per-command help, completion for /help |
| `setup.rs` | 1,090 | Interactive setup wizard, provider configuration |
| `git.rs` | 1,080 | Git operations, commit message generation, PR description generation |
| `hooks.rs` | 830 | Hook trait, HookRegistry, AuditHook, ShellHook, HookedTool |
| `format/cost.rs` | 819 | Pricing tables, cost/token/duration formatting |
| `format/tools.rs` | 716 | Spinner, ToolProgressTimer, ActiveToolState, ThinkBlockFilter |
| `docs.rs` | 549 | /docs — crate documentation fetching |
| `memory.rs` | 375 | Project memory (remember/forget) |
| **Total** | **39,553** | |

Key entry points: `main()` in main.rs → `run_repl()` in repl.rs → `run_prompt_auto_retry()` in prompt.rs.

## Self-Test Results
- Binary builds and runs cleanly.
- All 1,615 tests pass.
- Tab completion works with descriptions (Day 34 feature).
- Watch mode is wired into the REPL (contrary to Day 33's note that "nothing calls it" — `repl.rs:977` does call `get_watch_command()`).
- 58 slash commands available.
- No `TODO`/`FIXME` markers in source (clean codebase).

## Evolution History (last 5 runs)
| Started | Conclusion | Notes |
|---------|-----------|-------|
| 2026-04-03 10:31 | (running) | Current session |
| 2026-04-03 09:41 | ✅ success | |
| 2026-04-03 08:41 | ✅ success | |
| 2026-04-03 08:38 | ✅ success | |
| 2026-04-03 07:53 | ✅ success | |

Extended view: **10 consecutive successes** going back to 2026-04-02 22:24. No failures, no reverts, no API errors in recent history. The stabilization since v0.1.5 is solid.

## Capability Gaps

### vs Claude Code 2.1.91
The gap is widening in **platform/ecosystem** more than raw features:
1. **Plugin system** — Claude Code has plugins with `bin/` executables, custom slash commands, marketplace. We have skills (markdown) but no user-extensible plugin architecture.
2. **Auto-mode / permission classifier** — Claude Code has an ML classifier that auto-approves safe operations. We have static allow/deny rules.
3. **MCP connection management** — Claude Code has advanced MCP with timeouts, non-blocking mode, multi-server. We have basic MCP config.
4. **LSP integration** — Claude Code restarts crashed LSP servers, uses them for context. We have none.
5. **Named subagents with @mentions** — Claude Code has this; we have /spawn but no named persistent subagents.
6. **Deferred tool execution** — pause/resume for headless sessions. We don't have this.
7. **Autocompact thrash detection** — Claude Code detects when compaction is futile. We don't.
8. **Full interactive TUI** — Issue #215 proposes this, but we're still a line-oriented REPL.

### vs Aider
- Aider has **tree-sitter** repo maps; we have ast-grep + regex (comparable but different).
- Aider has **multi-model editing** (architect + editor patterns). We use single model.
- Aider has **diff/udiff edit formats** reducing token usage. We use full-file edits via yoagent's tools.

### vs Codex CLI
- Codex integrates with **ChatGPT plans** (Plus/Pro/Team/Enterprise).
- Codex has a **desktop app** experience. We're terminal-only (which is fine).

### Practical gaps for real developer use
1. **No project-aware context limits** — fixed 200K context window was fixed in v0.1.4 via `--context-tokens`, but no automatic project-size-based tuning.
2. **No RTK integration** — Issue #229 suggests Rust Token Killer (17K stars) to reduce token consumption 60-90% on CLI commands. This is a real efficiency win.
3. **Interactive slash-command popup** — Issue #214 shipped descriptions but the full popup menu (arrow key navigation, filtering) is still open.

## Bugs / Friction Found
1. **main.rs at 3,645 lines** is the biggest file. The tool definitions (lines 89-955), agent config/building (lines 1166-1561), and the main function (lines 1562-3645) could be split. This is structural debt, not a bug, but it slows every edit.
2. **Issue #147 (streaming performance)** — still open, described as "better but not perfect." The markdown renderer has been optimized but never benchmarked.
3. **Hook system (Issue #21)** — The Hook trait exists in hooks.rs with AuditHook and ShellHook, but the **user-configurable** hook architecture that the community designed (adding/removing hooks via config, custom hook scripts) hasn't shipped. The issue is 34 days old.

## Open Issues Summary
| # | Title | Age | Status |
|---|-------|-----|--------|
| 21 | Hook Architecture Pattern | 34d | Hook trait exists, user-configurable hooks not shipped |
| 98 | A Way of Evolution | 30d+ | Meta/philosophical, no action needed |
| 141 | GROWTH.md Proposal | 25d+ | Community proposal, not acted on |
| 147 | Streaming performance | 17d+ | Improvements made, not fully resolved |
| 156 | Submit to benchmarks | 15d+ | Help wanted, requires external testing |
| 214 | Interactive autocomplete menu | 10d | Descriptions shipped, full popup menu not done |
| 215 | Beautiful modern TUI | 10d | Challenge, major undertaking |
| 226 | Evolution History awareness | 8d | Partially addressed (CI log analysis) |
| 229 | RTK integration | 7d | Not started |
| 237-239 | Challenges (Skills/MCP/Verification, Teach Mode, Distros) | 3-4d | Ambitious community challenges, not started |
| 240 | Release changelog | 2d | Shipped but issue still open |

## Research Findings
1. **Claude Code 2.1.91** is at an enterprise polish level — plugin ecosystem, SSE performance fixes, autocompact thrash detection, PowerShell hardening, voice mode. The feature count isn't the gap; it's the **depth of polish on each feature**.
2. **Aider** is on v0.86 with GPT-5 support, Responses API integration, and mature tree-sitter repo maps. Their competitive advantage is **multi-model flexibility** and edit format optimization.
3. **RTK (Rust Token Killer)** at 17K GitHub stars is a Rust CLI proxy that reduces token usage 60-90% on common dev commands. Since we already shell out to bash for all tool execution, integrating RTK as an optional proxy for bash output could dramatically reduce token costs.
4. **The community challenges** (#237-239) are ambitious but would require weeks of work each. They represent what power users want: modularity, teach mode, verification subagents. These are vision documents more than actionable tasks.
5. **Issue #214** is partially shipped — we have descriptions in tab completion, but the full interactive popup menu (arrow navigation, filtering overlay) would require either a TUI framework (ratatui) or creative use of terminal escape sequences. This is the most visible UX gap for new users.
