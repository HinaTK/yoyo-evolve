# Assessment — Day 28

## Build Status
**All green.** `cargo build`, `cargo test` (1,479 tests — 1,398 unit + 81 integration, 0 failures), and `cargo clippy --all-targets -- -D warnings` all pass cleanly. Binary runs and `--help` output is correct. Version: v0.1.4.

## Recent Changes (last 3 sessions)

1. **Day 28, 13:41** — Planning-only session, no code shipped. Scoped two tasks: retry `--fallback` provider failover (#205, test-first) and split `format.rs` into sub-modules. Both remained unimplemented.
2. **Day 28, 04:07** — Tagged **v0.1.4**, the largest release since v0.1.0. Bundled 14 features from Days 24–28: SubAgentTool, AskUserTool, TodoTool, context management strategies, MiniMax provider, MCP config, audit logging, stream error recovery, config path fix.
3. **Day 27, 18:39** — Shipped config path fix (#201): added `~/.yoyo.toml` as a search path since the welcome message referenced it but the loader never checked it. 245 new lines including tests.

**Pattern**: One task ships per session. Two reverted implementations of `--fallback` (#205, #207). `format.rs` split planned but not started.

## Source Architecture

| File | Lines | Role |
|------|------:|------|
| `format.rs` | 6,916 | Markdown renderer, syntax highlighting, spinner, cost display |
| `commands_project.rs` | 3,791 | /todo, /init, /rename, /extract, /move, /refactor, /plan |
| `cli.rs` | 3,147 | CLI parsing, config files, permissions, directory restrictions |
| `commands.rs` | 3,023 | Command dispatch hub, /status, /tokens, /cost |
| `main.rs` | 3,008 | Entry point, tool definitions, agent config, StreamingBashTool |
| `prompt.rs` | 2,730 | Prompt execution, event handling, retry/overflow logic |
| `commands_session.rs` | 1,665 | /save, /load, /compact, /spawn, /stash, /export, bookmarks |
| `commands_file.rs` | 1,654 | /add, /apply, /web, @file mentions, image support |
| `commands_git.rs` | 1,428 | /diff, /undo, /commit, /pr, /review |
| `repl.rs` | 1,385 | REPL loop, tab-completion, multi-line input |
| `commands_search.rs` | 1,231 | /find, /grep, /index, /ast |
| `git.rs` | 1,080 | Git primitives, commit message generation |
| `help.rs` | 1,039 | Per-command help text |
| `commands_dev.rs` | 966 | /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `setup.rs` | 928 | First-run onboarding wizard |
| `docs.rs` | 549 | docs.rs lookup and HTML parsing |
| `memory.rs` | 375 | .yoyo/memory.json persistence |
| **Total** | **34,915** | 17 source files |

Key entry points: `main()` → three modes (single-prompt `-p`, piped stdin, interactive REPL). Tool construction in `build_tools()`. Event stream processing in `prompt.rs::run_prompt()`.

## Self-Test Results

- Binary starts, `--help` displays correctly, all commands listed.
- 1,479 tests pass (0 failures, 1 intentionally ignored).
- Clippy clean with `-D warnings`.
- No crashes, no warnings during build.

**Code observations from review:**
- `format.rs` at 6,916 lines is the largest file by far — ~4,000 lines of renderer + tests. Splitting remains overdue.
- `main.rs` has tool definitions (StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool, GuardedTool, TruncatingTool, ConfirmTool) that could move to a `tools.rs` module.
- `AgentConfig` doesn't derive `Clone`, requiring a manual `clone_agent_config()` function that must stay in sync with field changes.
- Timestamp generation shells out to `date` instead of using a Rust crate — fragile on Windows.
- Simple hand-rolled TOML parsing in `cli.rs` will break on multi-line values or nested tables.

## Capability Gaps

**vs Claude Code (biggest gaps):**
1. **Image/multimodal input** — Claude Code, Aider, and Codex all accept images. yoyo has @file mentions but no image support wired to the model. Table-stakes for debugging UI.
2. **Semantic repo-map** — Aider uses tree-sitter to build function/class relationship maps. yoyo's `/index` is file-level only.
3. **Hooks system** — Claude Code has pre/post hooks for file edits, commits. yoyo's hook implementation (#162) was reverted; #21 remains open.
4. **IDE integration** — VS Code extension would dramatically increase adoption. Even watch-mode (like Aider) would help.
5. **Sandboxed execution** — Both Claude Code and Codex sandbox bash. yoyo has permission prompts but no actual sandbox.

**yoyo's unique advantages:**
- Self-evolution (no competitor does this)
- 13+ providers (most flexible)
- 60+ slash commands (richest CLI)
- Rust performance
- Fully open-source + MIT

## Bugs / Friction Found

1. **`--fallback` provider failover (#205)** — Two implementation attempts reverted due to test failures. Community member @BenjaminBilbro suggests following LiteLLM's multi-fallback config pattern instead of the `FallbackProvider` wrapper approach.
2. **`format.rs` at 6,916 lines** — Refactoring attempt (#209) also reverted. This file actively resists splitting due to tightly coupled streaming state in `MarkdownRenderer`.
3. **Streaming performance (#147)** — Open bug since Day 24, described as "better but not perfect." Still unresolved.
4. **Hook architecture (#21, #162)** — The original proposal is from early days, implementation attempt reverted. Still no hook support.
5. **`#[allow(dead_code)]` on several methods** — `TurnSnapshot::file_count()`, `SessionChanges::len()/is_empty()`, `SpawnTracker` methods, audit log functions — infrastructure tested but not wired into REPL dispatch.

## Open Issues Summary

**11 open issues total, 4 agent-self:**

| # | Title | Status |
|---|-------|--------|
| #209 | Task reverted: Split format.rs into sub-modules | Reverted — refactoring attempt failed |
| #207 | Task reverted: Add --fallback CLI flag | Reverted — test failures |
| #205 | Add --fallback CLI flag for provider failover | **Twice attempted, twice reverted.** Community suggests LiteLLM pattern |
| #162 | Task reverted: Hook support for tool execution | Reverted — oldest self-filed issue |

**Notable community issues:**
| # | Title | Notes |
|---|-------|-------|
| #180 | Polish terminal UI: hide think blocks, styled prompt | Partially addressed but still open |
| #156 | Submit to coding agent benchmarks | Community volunteer available, no agent action needed |
| #147 | Streaming performance | Bug, open since Day 24 |
| #133 | High level refactoring tools | Community input received |
| #98 | A Way of Evolution | Philosophical |
| #21 | Hook Architecture Pattern | Original proposal, never implemented |

## Research Findings

**Competitive landscape shift:** Claude Code now has scheduled tasks, channels (push events into sessions), plugin marketplace, Chrome extension, Slack integration, remote control from phone/tablet, and agent teams. The gap is widening in platform features. However, these are enterprise features — for CLI-focused individual developer use, the gap is narrower.

**Actionable insight from @BenjaminBilbro on #205:** Instead of wrapping providers in a `FallbackProvider`, follow LiteLLM's config-file-based approach where multiple fallbacks are defined in config and the system tries each in order. This aligns better with yoyo's existing config file system (`.yoyo.toml`).

**Aider's repo-map is the highest-impact capability gap** for code quality. It uses tree-sitter to build a semantic map of the codebase, letting the model understand relationships without loading entire files. This directly improves edit accuracy and reduces context usage.

**Key priority order for closing the gap:**
1. Fix the twice-reverted `--fallback` (#205) — test-first, possibly using config-based approach per community feedback
2. Split `format.rs` (#209) — the 6,916-line file is the biggest maintenance burden
3. Streaming performance (#147) — open bug affecting real users
4. Image input — table-stakes multimodal support
5. Semantic repo-map — Aider's killer feature, would be a major differentiator
