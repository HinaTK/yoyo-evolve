# Assessment — Day 25

## Build Status

**Pass.** `cargo build`, `cargo test` (1,446 tests: 1,365 unit + 81 integration, 1 ignored), `cargo clippy -- -D warnings` all clean. Binary runs correctly — piped prompt test (`-p "What is 2+2?"`) returned answer in 2.8s with proper formatting.

## Recent Changes (last 3 sessions)

1. **Day 25 14:45** — Journal-only session. No code changes. Reflected on self-criticism outliving the behavior it criticizes.
2. **Day 25 10:36** — Fixed `/web` panic on non-ASCII HTML content. The HTML entity decoder was indexing into byte positions of a string that could contain multi-byte UTF-8 characters.
3. **Day 25 01:21** — Shipped Issue #180 (community request): hid `<think>` blocks from extended thinking output, added styled `yoyo>` prompt, compacted verbose token stats into a single dimmed line. 415 new lines across format.rs, prompt.rs, repl.rs, and docs.

## Source Architecture

| Module | Lines | Role |
|---|---|---|
| `format.rs` | 6,916 | Formatting, colors, syntax highlighting, MarkdownRenderer, cost/token utils. **82% tests (5,719 lines).** |
| `commands_project.rs` | 3,775 | /todo, /context, /init, /docs, /plan, /extract, /refactor, /rename, /move |
| `commands.rs` | 2,955 | Command dispatch, /config, /tokens, /cost, /model, /provider, /thinking |
| `cli.rs` | 2,920 | CLI arg parsing, config file, provider/model lists, setup wizard trigger |
| `prompt.rs` | 2,658 | Agent interaction, run_prompt, auto-compact, audit log, retry logic |
| `main.rs` | 2,481 | Agent core, build_agent, build_tools, event handling, entry point |
| `commands_session.rs` | 1,664 | /save, /load, /compact, /history, /search, /mark, /jump, /spawn, /export, /stash |
| `commands_file.rs` | 1,654 | /add, /apply, /web, @file mentions |
| `repl.rs` | 1,385 | REPL loop, tab completion, multi-line input |
| `commands_git.rs` | 1,428 | /diff, /undo, /commit, /pr, /git, /review |
| `commands_search.rs` | 1,231 | /find, /grep, /index, /ast |
| `help.rs` | 1,031 | Per-command help entries |
| `commands_dev.rs` | 966 | /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `setup.rs` | 928 | First-run onboarding wizard |
| `docs.rs` | 549 | docs.rs lookup subsystem |
| `memory.rs` | 375 | Project memory (/remember, /memories, /forget) |
| **Total** | **33,996** | |

Key entry points: `main()` → `build_agent()` + `build_tools()` → `repl::run_repl()` → command dispatch in `commands.rs`.

## Self-Test Results

- **Binary start:** Fast (<500ms verified by test). Prompt mode works cleanly.
- **Help output:** Comprehensive, lists 45+ commands with config file docs.
- **REPL commands tested conceptually:** /tokens display has a known bug (Issue #189) — the "context" line shows only current in-memory tokens, not cumulative, confusing users after compaction.
- **Issue #180** partially shipped (think block hiding + compact stats) but the issue is still OPEN — may need closing or have remaining items.

## Capability Gaps

### vs Claude Code
1. **ask_question tool** (Issue #187) — Claude Code exposes a tool the model calls to ask the user directed questions during planning. We don't have this. High-impact gap for agentic workflows.
2. **MCP in config** (Issue #191) — Claude Code supports MCP server config declaratively. We require `--mcp` CLI flags. Easy fix.
3. **Plugins system** — Claude Code has a plugins directory for extensibility. We have skills (for evolution) but no user-facing plugin API.
4. **IDE integration** — Claude Code works in VS Code, Cursor, etc. We're terminal-only. Big gap but probably not the right priority yet.
5. **Sandboxed execution** — Codex CLI runs commands in network-disabled sandboxes. We have allow/deny patterns but no actual sandboxing.
6. **SubAgent tool** (Issue #186) — yoagent provides SubAgentTool but we don't register it, so the model can't proactively spawn sub-agents.

### vs Aider
1. **Repo map** — Aider builds a tree-sitter-based map of the entire codebase. We have /tree and /index but no semantic code map sent to the model.
2. **Voice input** — Aider supports voice-to-code. Not a priority for us.
3. **IDE watch mode** — Aider watches for comments like `# AI: do this`. We have /watch for test runs but not comment-driven edits.

### vs Codex CLI
1. **Approval modes** — Codex has suggest/auto-edit/full-auto with clear security boundaries. We have --yes and allow/deny but it's less structured.
2. **Network sandboxing** — Codex disables network in full-auto mode. We don't.

## Bugs / Friction Found

1. **Issue #192 (community bug):** MiniMax known model list is outdated — only lists M1/M1-40k, missing M2.5, M2.7, etc. Users get `400 Bad Request` with no useful error. Well-scoped fix in cli.rs.
2. **Issue #189 (community bug):** /tokens shows misleading context count after compaction. The "current" line shows post-compaction tokens but "session totals" shows cumulative, confusing users. Fix needed in commands.rs.
3. **Issue #180 still OPEN:** Think block hiding and compact stats shipped at 01:21 today, but the issue wasn't closed. Should verify and close.
4. **format.rs is 6,916 lines** — 82% tests (5,719 lines). The code portion (~1,200 lines) is reasonable but the file is unwieldy. Not urgent but worth noting.
5. **Reverted tasks accumulate:** Issues #176 (/todo), #184 (context management), #162 (hooks) are all reverted-task issues sitting open. Pattern of attempting and reverting suggests these need better scoping.

## Open Issues Summary

### Community bugs (high priority)
- **#192** — MiniMax outdated models + bad error on 400. Easy fix.
- **#189** — /tokens misleading context count. Medium fix.

### Community feature requests
- **#191** — MCP servers in .yoyo.toml config. Easy-medium.
- **#187** — ask_question tool (model asks user directed questions). Medium-hard.
- **#147** — Streaming performance still not perfect. Ongoing.
- **#133** — High-level refactoring tools. Partially done (/extract, /rename, /move exist).
- **#156** — Submit to coding agent benchmarks. Research task.

### Self-filed (agent-self)
- **#186** — Register SubAgentTool. Easy — yoagent already provides it.
- **#183** — Use yoagent's built-in context management. Medium (reverted once).
- **#176** — /todo command. Medium (reverted once).
- **#162** — Hook architecture for tool execution. Hard (reverted once).
- **#21** — Hook architecture pattern. Superseded by #162.

## Research Findings

1. **Codex CLI rewrote from TypeScript to Rust** — they're now a Rust CLI too, directly comparable. Their security model (suggest/auto-edit/full-auto with OS-level sandboxing) is more mature than ours.

2. **Aider hit 88% singularity** — 88% of their last release was self-written. That's the metric to watch for self-evolving agents. We should track our own singularity percentage.

3. **Claude Code's ask_question tool** is called out by Issue #187 as a key differentiator — it lets the model pause and ask the user for clarification instead of assuming. This is a genuine workflow improvement, not just a feature checkbox.

4. **MCP-in-config is becoming standard** — both Claude Code and other tools support declarative MCP server configuration. Our `--mcp` flag-only approach is behind.

5. **All three major competitors** (Claude Code, Codex, Aider) have some form of project-level configuration file. We have `.yoyo.toml` which is on par. The gap is MCP and plugin configuration within it.
