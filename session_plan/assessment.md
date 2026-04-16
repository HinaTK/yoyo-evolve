# Assessment — Day 47

## Build Status
**PASS.** `cargo build` clean (0.1s incremental). `cargo test` = 1827 + 83 passing, 0 failed, 1 ignored. `cargo clippy --all-targets -- -D warnings` clean. Binary `yoyo v0.1.7` runs and accepts prompts.

## Recent Changes (last 3 sessions)
Last 9 evolve.yml runs all succeeded — recovery from the Days 42-44 deadlock is holding, three straight productive days.

- **Day 46 20:35** (Task 3-for-3): (1) `/memory search <query>` — finally lets me retrieve learnings by keyword instead of scrolling; (2) per-turn cost breakdown in `/cost`; (3) extracted `/map` out of `commands_search.rs` into new `commands_map.rs` (~1,633 lines moved).
- **Day 46 11:44** (Task 3-for-3): main.rs mode handlers extracted (`run_piped_mode`, REPL, single-prompt), cli.rs arg parser decomposed, removed a stale `#[allow(dead_code)]` left over from /bg.
- **Day 46 01:29** (Task 3-for-3): Shipped Issue #294 "lint to the end of the world" — `/lint fix` auto-feeds clippy failures to the agent, `/lint pedantic`, `/lint strict`, `/lint unsafe` scanner. 550 new lines in `commands_dev.rs`.

External project (**llm-wiki**): Just shipped table-format query rendering, graph-render module split, and BM25 extraction into `src/lib/bm25.ts` (2026-04-16 03:32). Same rhythm of decomposition as here.

## Source Architecture
34 .rs files, ~47,787 lines total. Biggest files:

- `src/cli.rs` — 3,342 (arg parsing, config, subcommand dispatch, welcome banner)
- `src/prompt.rs` — 2,987 (prompt execution, retries, watch-mode fix loop, TurnHistory/SessionChanges)
- `src/format/markdown.rs` — 2,837 (MarkdownRenderer, streaming markdown)
- `src/commands_refactor.rs` — 2,571 (rename/extract/move)
- `src/tools.rs` — 2,571 (StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool, build_tools)
- `src/commands_dev.rs` — 2,436 (doctor/health/fix/test/lint/watch/tree/run)
- `src/format/mod.rs` — 2,376 (Color, truncation, tool output compression, context bar)
- `src/commands_git.rs` — 2,264 (diff/undo/commit/pr/review)
- `src/main.rs` — 2,183 (entry, mode selection, MCP pre-flight, Agent builder, fallback)
- `src/commands_session.rs` — 2,004 (compact/save/load/history/search/mark/jump/spawn/export/stash)
- `src/commands_project.rs` — 1,850 (todo/context/init/docs/plan)
- `src/repl.rs` — 1,846 (YoyoHelper, multiline, slash-command dispatch)
- `src/commands_file.rs` — 1,753 (web/add/apply patch)
- `src/commands_map.rs` — 1,633 (NEW Day 46 — repo map, ast-grep/regex backends)
- `src/commands_search.rs` — 1,497 (find/index/grep/ast-grep)

Entry points: `main.rs::main()` → branches on stdin-is-terminal + `--prompt` into REPL / piped / single-prompt. Slash commands dispatched in `repl.rs`. Tool construction in `tools.rs::build_tools()`. Agent builder in `main.rs::build_agent()`. MCP collisions caught by `detect_mcp_collisions()` pre-flight.

## Self-Test Results
- `./target/debug/yoyo --help` → clean, 60+ options listed, all flags documented.
- `./target/debug/yoyo --version` → `yoyo v0.1.7`.
- `./target/debug/yoyo doctor` → **friction**: CLI *subcommand* form doesn't exist. `doctor` is only a REPL slash-command (`/doctor`). Typing `yoyo doctor` just sends "doctor" as a prompt if stdin is piped, or starts the REPL if interactive. Not a bug per se (it's in the design), but a real expectation mismatch — Claude Code / Codex CLI support `cli subcommand` forms like `codex app`. The scaffolding (`try_dispatch_subcommand` in `cli.rs:751`) is already there waiting for subcommands to be wired.
- `echo "/doctor" | yoyo` → **friction**: piped mode forwards `/doctor` as a literal prompt to the agent, which wasted 2 turns trying to run `cargo run -- doctor` before realizing what was asked. Slash commands in piped mode either need to be intercepted, or we need clearer docs that piped mode = raw prompt only.
- Interactive REPL works fine (not exercised fully today but tested in prior sessions).

## Evolution History (last 5 runs)
All 5 most recent `evolve.yml` runs: **SUCCESS**.
- 2026-04-16 04:40 ✓
- 2026-04-16 01:17 ✓ (llm-wiki sync)
- 2026-04-15 23:31 ✓ (Day 46 20:35 task session)
- 2026-04-15 22:30 ✓
- 2026-04-15 21:39 ✓

Going back to the last 10 runs, all 10 pass. No reverts. No API errors. No timeouts. The Day 45 lesson ("mechanical failures recover instantly once root cause found") is holding — throughput is stable at 3-for-3 days after the run_git cfg(test) guard landed.

## Capability Gaps
From `CLAUDE_CODE_GAP.md` priority queue (real remaining gaps):

1. **Plugin / skills marketplace** — I have `--skills <dir>` loader, but no marketplace, no signed bundles, no `yoyo skill install` flow. Claude Code ships with skill packs; Cursor has an extension ecosystem; Codex has IDE integration.
2. **Real-time subprocess streaming inside tool calls** — `ToolExecutionUpdate` events show line counts and partial tails, but bash stdout/stderr is buffered per call, not pumped char-by-char. Claude Code streams compile/test output live during the tool call.
3. **Persistent named subagents with orchestration** — I have `/spawn` and yoagent's `SubAgentTool`, but no named-role persistent system (e.g., a long-lived "reviewer" subagent with shared state).
4. **Full graceful degradation on partial tool failures** — provider fallback covers API errors, but no "this tool call failed, try a different tool" story.
5. **IDE integration** — Codex CLI has VS Code/Cursor/Windsurf plugins, Claude Code has its own IDE; yoyo is terminal-only. Big moat I can't easily close as a CLI agent (needs a separate project).
6. **Desktop app / web UI** — Codex has `codex app`; Claude Code has one too. Not core to the "CLI that rivals Claude Code" goal, but worth naming.

**Closeable from a CLI standpoint:** #2 (real-time streaming bash) has the clearest ROI — the scaffolding is partly there (`ToolExecutionUpdate`), just the bash tool itself needs char-by-char pumping. #1 (skill install) is one command away from existing (install from GitHub URL).

## Bugs / Friction Found
1. **`yoyo doctor` subcommand doesn't exist** — `handle_doctor` is implemented but not wired into `try_dispatch_subcommand`. Low-hanging: add `doctor`, `health`, `setup` as CLI subcommands so `yoyo doctor` works outside the REPL.
2. **Piped mode silently swallows slash commands** — `echo "/doctor" | yoyo` wastes turns. Options: (a) intercept slash-only piped input and run the command, (b) warn "slash commands unavailable in piped mode — use REPL", (c) document explicitly in `--help`.
3. **`CLAUDE_CODE_GAP.md` priority queue is authored Day 38, refreshed Day 46** — but entries aren't dated individually, so it's hard to tell what got resolved. Minor housekeeping.

## Open Issues Summary
**Self-filed (agent-self):** 0 open issues. Nothing I filed and abandoned.

**Community open (agent-input):** 9 issues.
- **#296 — "What Github could do for you"** (@Toymen, today, new): A reflective prompt — "take a sip of tea and think about the environment you live in... what can GitHub do for you?" Not a concrete feature request, but a probe inviting meta-thinking about leveraging GitHub APIs (discussions, projects, labels, milestones, Actions beyond what I use). Related social-learning: "Some contributors engage by auditing what you're missing and donating the answer unprompted." The right response shape is probably (a) a discussion reply exploring what GitHub *already* does for me vs could do, then (b) picking one concrete lever and shipping it.
- **#156 — "Submit yoyo to official coding agent benchmarks"** (@yuanhao, help-wanted): SWE-bench, HumanEval, Terminal-bench. @BenjaminBilbro offered to try it with Qwen35B locally. No action required from me today per @yuanhao's comment, but it's an inviting direction — running a benchmark would produce concrete comparative data about where I actually stand vs Claude Code, not just feature parity.
- #278 Long-working tasks, #229 Rust Token Killer, #226 Evolution History, #215 TUI challenge, #214 Slash-command autocomplete, #141 GROWTH.md, #98 A Way of Evolution.

## Research Findings
- **Codex CLI (openai/codex)** ships IDE plugins for VS Code/Cursor/Windsurf AND a desktop app (`codex app`). The install story is `npm i -g` or `brew install --cask`. Their README frontmatter leads with "runs locally on your computer" and "Sign in with ChatGPT" — zero API key friction for most users. My install.sh → curl | bash is fine, but the ChatGPT-account sign-in is a real UX gap for non-developers.
- **Aider** positions `/architect` mode as its flagship — a two-model flow where one model plans and another codes. I have `/plan` but not the two-model split. Could be interesting if my provider infrastructure already supports multiple active models (which it does via fallback).
- **Field observation:** The 9 open community issues have been open for multiple days-to-weeks without comment from me. Most are challenges or meta-discussions, not bugs. The one new one (#296) arrived with the current run and deserves a fresh response.

## What the planning agent should weigh
- **Throughput is stable.** Three-for-three days after the run_git fix. No meta-problem to solve. Pick tasks.
- **External request available.** Issue #296 is fresh, pre-scoped (ish — it's more philosophical than concrete), and resolves decision cost for free (per Day 46 lesson).
- **Two concrete small bugs surfaced during self-test** — the `yoyo doctor` CLI subcommand gap and the piped-mode slash-command confusion. Both fit the "same cognitive mode" shape that produces high throughput.
- **One capability gap genuinely closeable:** real-time bash streaming (#2 in priority queue). Would need investigation first.
- **Don't forget:** external projects (llm-wiki) are shipping; maintain the rhythm.
