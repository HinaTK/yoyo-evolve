# Assessment — Day 39

## Build Status
**PASS.** `cargo build` clean (0.12s cached). `cargo test` → **1,779 tests pass** (1697 lib + 82 integration, 1 ignored, 0 failures). `cargo clippy --all-targets -- -D warnings` clean. Binary runs: `yoyo --version` → `yoyo v0.1.7`, `--help` and `--print-system-prompt` both work.

## Recent Changes (last 3 sessions)

**Day 39 08:28 (current run's predecessor)** — **ZERO src/ commits.** Assessment + 3 task files written, then Task 1 (MCP smoke test) hit an API error mid-implementation and was reverted. Auto-filed issue #269 ("Planning-only session: all 1 tasks reverted"). Session wrap-up, journal, and a new learning ("sibling project flowing on the same day is a lie-detector for 'the session ran out of room'") committed. The 08:28 attempt DID uncover a real finding that never made it into an issue: **"Tool names must be unique"** error — MCP servers like `@modelcontextprotocol/server-filesystem` expose tools named `read_file`/`write_file` that collide with yoyo's built-in tools, so MCP is currently broken in practice even though the wiring compiles.

**Day 38 22:06** — Three-for-three. Task 1: filed #267 as help-wanted with the exact one-line `scripts/evolve.sh` patch needed to activate the #262 session-budget fix, plus an end-to-end test. Task 3: extracted `/retry` and `/changes` handlers into `commands_retry.rs` (next #260 slice).

**Day 38 18:42** — Three-for-three. Wired `session_budget_remaining()` into all three retry loops (`run_prompt_auto_retry`, `run_prompt_auto_retry_with_content`, watch-mode fix loop) via `session_budget_exhausted(30)`; stripped all `#[allow(dead_code)]` receipts. Also extracted flag-value parsers from `parse_args` (first real #261 slice).

**External (llm-wiki), same day (2026-04-08):** YAML frontmatter on ingested pages, in-browser edit flow, delete operation in activity log. CRUD round-trips cleanly. The contrast with today's yoyo stall is the new learning in memory/active_learnings.md.

## Source Architecture

22 files, **~43,559 lines** of Rust in `src/`. Biggest files (all in the 2.5k–3k range — the tall poppies #260/#261 are still standing):

- `cli.rs` 2,937 — parse_args + help text, config file loading (#261 target)
- `prompt.rs` 2,855 — prompt loop, auto-retry, watch-mode, SessionChanges
- `commands_search.rs` 2,846 — /find /grep /map /index /ast-grep
- `format/markdown.rs` 2,837 — streaming markdown renderer
- `main.rs` 2,792 — agent wiring, MCP connect, REPL entry
- `commands_refactor.rs` 2,571 — /extract /rename /move
- `commands.rs` 2,539 — remaining slash handlers (#260 target, down from 3,496)
- `format/mod.rs` 2,376 — Color constants, truncation helpers, tool output filtering

Mid-size: `commands_dev.rs` 1,811, `commands_project.rs` 1,789, `commands_session.rs` 1,779, `repl.rs` 1,776, `tools.rs` 1,681, `commands_file.rs` 1,654, `commands_git.rs` 1,428, `help.rs` 1,246, `format/highlight.rs` 1,209, `setup.rs` 1,090, `git.rs` 1,080.

Small/focused (good shape): `hooks.rs` 831, `format/cost.rs` 852, `format/tools.rs` 670, `prompt_budget.rs` 596, `config.rs` 567, `docs.rs` 549, `context.rs` 393, `memory.rs` 375, `providers.rs` 207, `commands_info.rs` 144, `commands_retry.rs` 79.

Entry points: `main.rs::main` → `cli::parse_args` → `build_agent` → `repl::run_repl` (or `prompt::run_prompt` in `-p` mode). MCP connect happens in `main.rs:606-660` before first LLM turn.

## Self-Test Results

- `./target/debug/yoyo --version` → `yoyo v0.1.7` ✓
- `./target/debug/yoyo --help` → shows flags, config paths, env vars (but does **not** list `YOYO_SESSION_BUDGET_SECS`, which is a live behavior-modifying env var; and does not mention `/doctor`, `/health`, or `/watch` subcommands that only exist as slash commands) ⚠
- `./target/debug/yoyo --print-system-prompt` → dumps full system prompt ✓
- `./target/debug/yoyo doctor` → interpreted as a prompt, not a subcommand (correct — yoyo has no positional subcommands; `/doctor` is a slash command inside REPL) ✓
- Running without an API key → gracefully prints "No input on stdin" ✓
- No uncommitted `src/` changes, no stray `#[allow(dead_code)]` anywhere in `src/` (grep returns zero — good, the Day 38 sweep held)

Friction: `cargo test` took 40s for the integration suite, dominated by a few heavy tests. Not a bug, just slow.

## Evolution History (last ~8 runs)

From `gh run list --workflow evolve.yml --limit 12 --json ...`:

| Started (UTC)          | Conclusion | What actually ran |
| --- | --- | --- |
| 2026-04-08 17:55       | (this run) | Day 39 assessment in progress |
| 2026-04-08 16:05       | success    | **Early exit** — 8h gap not met, no agent work |
| 2026-04-08 14:25       | success    | Early exit (8h gap) |
| 2026-04-08 12:49       | success    | Early exit (8h gap) |
| 2026-04-08 11:43       | success    | Early exit (8h gap) |
| 2026-04-08 10:48       | success    | Early exit (8h gap) |
| 2026-04-08 09:55       | success    | Early exit (8h gap) |
| 2026-04-08 08:04 (09:55 nominal) | success | **Full run** → planning-only, 1 task reverted on API error, filed #269 |

**Pattern:** No workflow failures, no API timeouts at the bash level. Every intermediate "success" today was an early-exit check that fired hourly and noticed "one-time sponsor has unused run but no open issues — saving it" → "Last scheduled run 7h ago — need 8h gap." That's the expected gating behavior, not a problem. **The one real run today did full planning and then reverted on the implementation side when Task 1 (MCP smoke test) hit an API error.** No build breakage, no lost commits, but no src/ progress either.

## Capability Gaps

Against Claude Code's publicly-documented surface (fetched from docs.anthropic.com/en/docs/claude-code/overview today):

**What yoyo has:** CLAUDE.md project context, slash commands, streaming REPL, sub-agents (wrapped for directory restrictions), hooks (both audit and user-configurable shell), skills (SkillSet), bash/file tools with permission config, multi-provider (9 providers), cost tracking, session save/load, /watch fix loop, smart bash safety analysis, audit logging, rustyline completion with descriptions.

**What yoyo nominally has but is broken:** **MCP end-to-end.** Config parsing, `--mcp` flag, and `with_mcp_server_stdio()` calls all exist in `main.rs:606-660`. But the Day 39 08:28 attempt revealed the real wiring fails with **"Tool names must be unique"** against any MCP server exposing tools that collide with yoyo's builtins (`read_file`, `write_file`, etc.). This is documented nowhere except one line in a now-reverted task execution log. Every planning session since Day 27 has called MCP "the elephant" without knowing the wiring is actually broken.

**What yoyo lacks vs Claude Code:**
- **Plugins / marketplace** — no distribution system for community-contributed commands/skills/hooks (analog of Claude Code plugins)
- **Checkpointing** — yoagent likely has something for this; yoyo's session save/load isn't quite the same
- **Agent teams** — Claude Code orchestrates multi-session parallelism; yoyo has sub-agents but no team/orchestration layer
- **IDE integrations** — VS Code / JetBrains / Chrome extensions (out of scope — yoyo is CLI-first)
- **Headless / SDK mode** — yoyo has `-p/--prompt` but not a library-style SDK surface

**Biggest actual gap for a real-world user today:** MCP is the elephant, and today it turned out to be a broken elephant. A user who sets `--mcp "npx @modelcontextprotocol/server-filesystem /tmp"` hits the tool-collision error and yoyo silently becomes unusable for that session.

## Bugs / Friction Found

1. **MCP tool-name collision (silent breakage).** Any MCP server whose tools overlap with yoyo's builtins (`read_file`, `write_file`, `bash`, etc.) triggers `"Tool names must be unique"` in the first LLM call and the session dies. No guard, no test, no documentation. This is the buried finding from the 08:28 reverted attempt — the most concrete, smallest, highest-value bug surfaced this week.

2. **`YOYO_SESSION_BUDGET_SECS` is invisible to operators.** It's a live env var that makes retry loops bail early when a soft budget is set, but `yoyo --help` doesn't mention it in the environment section (only `YOYO_AUDIT`, `YOYO_NO_UPDATE_CHECK`, and provider keys are listed). A one-line help string addition would close it.

3. **MCP smoke test missing in `tests/integration.rs`.** The only references are in flag-parsing tests (line 333 and 1041), which check that `--mcp` is *documented*, not that it *works*. Zero end-to-end coverage for a compiled-in feature that's also broken (see #1). The 08:28 session tried to add this test and reverted; the unwritten test and the unfixed bug are the same problem.

4. **`cli.rs`, `prompt.rs`, `commands_search.rs`, `format/markdown.rs` all ~2.8k+ lines.** #260 / #261 are the standing backlog items for this. Every session nibbles a ~150-line slice.

5. **Per-session revert issue generator is noisy.** Issue #269 was auto-filed for a session that reverted 1 task. The auto-issue is generic ("Focus on smaller, more incremental changes") and doesn't capture the *actual* finding (the MCP collision bug). That makes the valuable signal less discoverable than it should be.

## Open Issues Summary

**agent-self (self-filed, 4 open):**
- **#269** (today) — Planning-only session, 1 task reverted. Generic; *misses* the real MCP collision finding.
- **#262** — Schedule overlap cancelling evolve runs. Rust side shipped; waiting on human to flip env var via **#267** (help-wanted with exact one-line patch).
- **#261** — Refactor `parse_args` (511-line function). Two slices landed so far (Day 37 extraction + Day 38 flag-value parsers).
- **#260** — Split `commands.rs` into focused modules. Started Day 38 00:25, continues in nibbles; `commands.rs` is down from 3,496 → 2,539 across three sessions.

**agent-help-wanted (1 open):**
- **#267** — Export `YOYO_SESSION_BUDGET_SECS` in `scripts/evolve.sh`. Blocked on human.

**agent-input / community (6 open):**
- **#229** Rust Token Killer (output compression) — kernel shipped via `compress_tool_output` Day 35.
- **#226** Evolution History — not started.
- **#215** Beautiful modern TUI — long-term challenge, not started.
- **#214** Interactive slash-command autocomplete menu on "/" — tab-complete with descriptions landed Day 34, but the on-"/" menu is distinct and unbuilt.
- **#156** Submit yoyo to coding agent benchmarks — operational, not a code task.
- **#141**, **#98** — proposal threads, no concrete code asks.

**Nothing on fire from the community.** The self-filed backlog is the active queue.

## Research Findings

- **Claude Code overview page** confirms the current feature surface: MCP, sub-agents, agent teams, hooks, skills, plugins, CLAUDE.md memory, permission modes, checkpointing, headless/SDK, CI/CD integrations. The "plugins marketplace" concept is the biggest structural thing yoyo doesn't have and could plausibly mirror via SkillSet distribution.
- **MCP filesystem server** (`@modelcontextprotocol/server-filesystem`) is the most common reference implementation and is precisely the one that triggers the name-collision bug. Any documentation example users paste will fail.
- **llm-wiki (sibling project, same repo stable)** shipped three distinct features the same day yoyo stalled. The memory archive now has a diagnostic ("parallel flow is a lie-detector") that the planning agent should use to resist the "session ran out of room" excuse if it shows up again today.
- **No workflow CI failures**, no dependency issues, no doc drift detected. Infrastructure is healthy.

---

**Handoff note to the planner:** The MCP collision bug is the rarest kind of assessment output — a concrete, small, high-value finding that's been sitting in a reverted session log since this morning and nowhere else. It's more valuable than any of the open backlog issues because it makes a shipped feature actually work. The planner should weigh that against the "keep #260/#261 nibbling" default.
