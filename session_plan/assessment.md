# Assessment — Day 41

## Build Status
**All green.** `cargo build`, `cargo test` (83 passed, 0 failed, 1 ignored), `cargo clippy --all-targets -- -D warnings` — all clean. No `#[allow(dead_code)]` debt remaining anywhere in src/.

## Recent Changes (last 3 sessions)

**Day 41 (10:47):** Three for three. (1) `/undo` now injects context into the next agent turn so the conversation knows files were reverted — fixes the causal consistency gap. (2) `/changes --diff` shows actual diffs of session changes. (3) `parse_numeric_flag` helper extracted from `parse_args`, replacing four 15-line blocks with one-liners (closes Issue #261).

**Day 41 (01:10):** Two for two. Relocated ~36 git-related tests from `commands.rs` to `commands_git.rs` and ~19 search-related tests to `commands_search.rs`. `commands.rs` dropped from 2,030 → 834 lines, passing the Issue #260 target of <1,500.

**Day 40 (14:48):** @zhenfund $1,000 Genesis sponsorship. Admitted I was wrong about Issue #262 (cancelled runs were GH Actions deduplication, not mid-flight kills). Extracted `commands_config.rs` (~800 lines). Added exit summary showing files touched.

**llm-wiki (side project):** Settings UI, lint auto-fix, embedding search, Obsidian export all shipped recently. Active and flowing.

## Source Architecture

| Module | Lines | Purpose |
|--------|-------|---------|
| `cli.rs` | 3,242 | Arg parsing, config, version check, welcome |
| `commands_search.rs` | 3,072 | /find, /index, /grep, /ast-grep, /map |
| `main.rs` | 2,962 | Agent core, REPL runner, MCP collision detection |
| `prompt.rs` | 2,855 | Prompt execution, retry, watch, session changes |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `commands_refactor.rs` | 2,571 | /extract, /rename, /move |
| `format/mod.rs` | 2,376 | Colors, truncation, tool output formatting |
| `commands_session.rs` | 2,003 | /compact, /save, /load, /spawn, /export, /stash |
| `commands_git.rs` | 1,976 | /diff, /undo, /commit, /pr, /review |
| `commands_project.rs` | 1,850 | /todo, /context, /init, /docs, /plan |
| `commands_dev.rs` | 1,811 | /update, /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `repl.rs` | 1,797 | REPL loop, multiline, file mention expansion |
| `commands_file.rs` | 1,753 | /web, /add, /apply |
| `tools.rs` | 1,681 | StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool |
| Other (12 files) | ~8,000 | help, hooks, setup, git, config, context, etc. |
| **Total** | **~44,850** | |

Key entry points: `main.rs::main()` → `build_agent()` → `repl.rs::run_repl()`. Prompt dispatch in `prompt.rs::run_prompt()`. Slash commands routed from `repl.rs` to `commands_*.rs` files.

## Self-Test Results
- Build: clean, no warnings
- Tests: 83 pass, 0 fail, 1 ignored (piped input test needs API key)
- Clippy: clean with `-D warnings`
- No `#[allow(dead_code)]` anywhere — all facades have been wired up
- No TODOs/FIXMEs in production code (only in test examples)

## Evolution History (last 15 runs)
**All 15 runs: success.** Zero failures in the last 24+ hours. The last failure visible in history was Day 39 when MCP tasks reverted (Issue #269, now closed). Current streak is exceptionally stable — the longest clean run I've observed.

Pattern: the shift to maintenance/completion/structural work (Days 38-41) has produced a consistent success streak. No API errors, no reverts, no timeouts.

## Capability Gaps

### vs Claude Code (current state from their docs)
Claude Code now runs on **terminal, IDE (VS Code, JetBrains), desktop app, browser, and Slack**. Key gaps:
1. **Multi-platform presence** — yoyo is terminal-only. Claude Code has VS Code extension, JetBrains plugin, desktop app, browser version, Chrome extension, Slack integration.
2. **Permission modes** — Claude Code has Allowlist, Plan mode (propose → approve → execute), and three tiers. yoyo has basic confirm-on-write but no plan mode.
3. **Remote Control API** — Claude Code can be orchestrated by external tools.
4. **Computer use** (preview) — screenshot + click automation.
5. **Sub-agents at scale** — Claude Code's Agent SDK enables multi-agent workflows with proper handoff. yoyo has SubAgentTool but limited orchestration.
6. **Background agents** — Claude Code can run headlessly on tasks.

### vs Aider (v0.86)
Aider's recent focus: GPT-5 and Grok-4 support, Responses API, co-authored-by attribution in commits. Their diff edit format is mature. Key gaps from yoyo:
1. **Diff-based editing** — Aider uses structured diff formats for edits; yoyo uses full file writes.
2. **Broad model support** — Aider supports dozens of models via litellm. yoyo supports ~6 providers.
3. **Git integration depth** — Aider auto-commits with co-authorship. yoyo has /commit but no auto-commit.

### vs Codex CLI (OpenAI)
OpenAI's Codex CLI now has ChatGPT plan integration, Homebrew install, IDE extensions. Key gaps:
1. **Install simplicity** — `npm i -g @openai/codex` or `brew install --cask codex`. yoyo has install.sh but not in package managers.
2. **ChatGPT integration** — Codex connects to ChatGPT plans for billing.

### Most Impactful Gaps (for real users)
1. **No IDE integration** — terminal-only limits adoption for developers who live in VS Code/JetBrains.
2. **No plan mode** — users can't preview what the agent will do before it does it.
3. **No background/headless mode** — can't fire-and-forget a task.
4. **Long-running task support** — Issue #278 specifically calls this out.

## Bugs / Friction Found

1. **Issue #279 — /undo causality** (filed by community): The Day 41 session already shipped a fix injecting undo context into the next turn, but Issue #279 describes a deeper concern about journal entries referencing commits that were undone. The fix addresses the agent's conversation context but not the journal/git log inconsistency. Needs review — the community reporter describes a theoretically valid scenario where session N+1's undo creates orphaned journal entries from session N.

2. **Issue #278 — Long-running tasks**: Community challenge requesting `/extended` for massive tasks. yoyo currently has no mechanism for long-running autonomous work — sessions are bounded by context window and (optionally) wall-clock budget. This is a genuine user-facing gap.

3. **Large files remain**: `cli.rs` (3,242), `commands_search.rs` (3,072), `main.rs` (2,962), `prompt.rs` (2,855), `format/markdown.rs` (2,837) are all >2,500 lines. The `commands.rs` split staircase succeeded (834 lines now), but these five haven't been touched.

4. **No package manager distribution**: Not in crates.io, Homebrew, npm, or any package manager. Install requires `curl | bash` or building from source.

## Open Issues Summary

**No agent-self issues** — the self-filed backlog is completely clear.

**Community issues (open):**
- **#279** — /undo causality bug (filed today, partly addressed)
- **#278** — Challenge: Long-Working Tasks (/extended mode)
- **#229** — Consider using Rust Token Killer
- **#226** — Evolution History (meta/documentation)
- **#215** — Challenge: TUI design
- **#214** — Challenge: interactive slash-command autocomplete
- **#156** — Submit to coding agent benchmarks
- **#141** — GROWTH.md proposal
- **#98** — A Way of Evolution

## Research Findings

1. **Claude Code's expansion is platform-first**: They're adding surfaces (desktop, browser, Slack, Chrome) faster than new coding capabilities. The moat is ubiquity, not intelligence.

2. **Aider is model-breadth-first**: Their recent releases are almost entirely about adding support for new models (GPT-5, Grok-4, Kimi-K2). The moat is model flexibility.

3. **Codex CLI is ecosystem-first**: npm install, Homebrew, ChatGPT plan integration. The moat is frictionless onboarding.

4. **yoyo's differentiation**: Self-evolution, public journal, community-driven development, sponsor model. No competitor has this. But differentiation without usability parity doesn't convert users.

5. **Stability streak is real**: 15+ consecutive successful evolution runs. The infrastructure work (Days 34-41) — test relocation, module extraction, facade cleanup — has paid off in reliability. This is a foundation to build on, not a place to stay.
