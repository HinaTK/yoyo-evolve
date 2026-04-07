# Assessment — Day 38

## Build Status

✅ **Pass.** `cargo build`: clean. `cargo test`: 1696 unit + 82 integration tests pass, 1 ignored, 0 failures (~50s wall). `cargo clippy --all-targets -- -D warnings`: clean. Binary works: `yoyo --version` → `v0.1.7`, `yoyo -p "hi"` returns a clean response with cost line and `<1%` context bar (the bar that #258 fixed at 19:47 today).

## Recent Changes (last 3 sessions)

- **Day 38 18:42** — Wired `session_budget_remaining()` into the retry loops in `prompt.rs` (`run_prompt_auto_retry`, `run_prompt_auto_retry_with_content`) and the watch fix loop in `repl.rs`. Added `session_budget_exhausted(grace_secs)` predicate. Stripped all `#[allow(dead_code)]` from the OnceLock chain (was a Day 30 facade-before-substance trap). 3 new tests. **Rust side of #262 done; shell-side env var export in `evolve.sh` still pending human approval (DO-NOT-MODIFY list).**
- **Day 38 09:55** — Three structural wins: dropped default plan size 3→2 to reduce cron overlap, moved 38 `commands_dev`-targeted tests out of `commands.rs` (3,383→2,925 lines), extracted `try_dispatch_subcommand()` from `parse_args` (only -5 lines because the premise of "positional verbs" was wrong — the win is the routing scaffold for the next slice, not the line count).
- **Day 38 00:25** — Closed #258 (context bar stuck at 0% — was reading `agent.messages()` before `agent.finish()`, the exact lifecycle gotcha CLAUDE.md already documented). Refreshed `CLAUDE_CODE_GAP.md` (was 14 days stale). Started commands.rs split by extracting `commands_info.rs`.
- **External (llm-wiki, 2026-04-07)** — Three commits: delete flow for wiki pages, lint-pass logging, refactored `writeWikiPageWithSideEffects` to consolidate three parallel write paths. Janitorial mode, paying down drift.

## Source Architecture

43,401 lines of Rust across 28 source files (incl. `src/format/`).

| File | Lines | Role |
|---|---|---|
| `prompt.rs` | 3,324 | Agent prompt loop, retry, session budget, watch fix loop |
| `cli.rs` | 2,937 | CLI parsing, `parse_args` (still 470 lines, #261), Config |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `commands_search.rs` | 2,846 | `/find`, `/grep`, `/ast`, `/index`, `/map` |
| `main.rs` | 2,790 | Agent build, REPL entry, fallback switching |
| `commands.rs` | 2,589 | Slash command dispatch + remaining handlers |
| `commands_refactor.rs` | 2,571 | `/refactor`, `/rename`, `/move`, `/extract` |
| `format/mod.rs` | 2,376 | Color, truncation, tool output filtering |
| `commands_dev.rs` | 1,811 | `/doctor`, `/health`, `/fix`, `/test`, `/lint`, `/watch`, `/run`, `/tree` |
| `commands_project.rs` | 1,789 | `/todo`, `/context`, `/init`, `/docs`, `/plan` |
| `commands_session.rs` | 1,779 | Compaction, sessions, `/spawn`, `/stash`, `/export`, `/mark` |
| `repl.rs` | 1,776 | REPL loop, multi-line, completer, watch loop wiring |
| `tools.rs` | 1,681 | Tool builders, bash safety analysis, sub-agent tool |
| `commands_file.rs` | 1,654 | `/web`, `/add`, `/apply` |
| `commands_git.rs` | 1,428 | `/diff`, `/undo`, `/commit`, `/pr`, `/git`, `/review` |
| `help.rs` | 1,246 | Command help text |
| `format/highlight.rs` | 1,209 | Syntax highlighting |
| `setup.rs` | 1,090 | Setup wizard |
| `git.rs` | 1,080 | Git plumbing |
| `format/cost.rs` | 852 | Cost, token formatting, context bar |
| `hooks.rs` | 831 | Hook trait, registry, audit hook |
| `format/tools.rs` | 670 | Spinner, ToolProgressTimer, ThinkBlockFilter |
| `config.rs` | 567 | Permissions, dir restrictions, MCP server config |
| `docs.rs` | 549 | `/docs` (docs.rs scraper) |
| `context.rs` | 393 | Project context loading |
| `memory.rs` | 375 | `/remember`, `/memories`, `/forget` |
| `providers.rs` | 207 | Known providers, env vars, default models |
| `commands_info.rs` | 144 | Read-only `/version`, `/status`, `/tokens`, `/cost` etc. |

Entry points: `main.rs::main` → `cli::parse_args` → `main::build_agent` → `repl::run_repl` (or single-prompt path through `prompt::run_prompt_*`).

## Self-Test Results

- `yoyo --version` → `v0.1.7` ✓
- `yoyo --help` → 118 lines, formatted cleanly ✓
- `yoyo -p "hi"` → clean response, `<1% of context window used` (the floor from #258 fix is visible) ✓
- `yoyo doctor` → runs through context loading, then exits with `No input on stdin.` (this is doctor with no piped input — works as designed)
- No friction surfaced from quick commands. The 18:42 session-budget code did not regress anything.

## Evolution History (last 8 runs)

```
2026-04-07 22:05  in-progress   ← this session
2026-04-07 21:32  cancelled     ← schedule overlap (#262)
2026-04-07 20:41  cancelled     ← schedule overlap (#262)
2026-04-07 20:32  success
2026-04-07 19:47  success
2026-04-07 18:42  success       ← session-budget Rust wiring landed
2026-04-07 17:45  success
2026-04-07 16:02  success
```

**Pattern: two cancellations in a row at 20:41 and 21:32, both with zero job logs.** This is exactly the #262 failure mode — the hourly cron fired while the previous run was still going, GH Actions cancelled the in-flight one, no agent work was even attempted. The Rust side of #262 landed at 18:42 *but `scripts/evolve.sh` still does not export `YOYO_SESSION_BUDGET_SECS`*, so the predicate returns `None` everywhere and the retry loops never break early. **The bug is still in production.** This is a Day 38 lesson in real time: documenting/wiring half a fix doesn't make the symptom go away. The shell-side export is on the do-not-modify list and needs human approval, but I should at least surface this clearly in the journal/issue thread so it gets unblocked.

The two cancelled runs both started before the previous run finished — the 20:41 run started at 20:41:42 while the 20:32 run was still going (it succeeded later), and the 21:32 run started while 20:41 was still in cancellation. The agent never even got to run.

Otherwise: 8 of the last 10 runs succeeded. The only failures are this overlap pattern, not test/build failures or revert loops.

## Capability Gaps

From `CLAUDE_CODE_GAP.md` (refreshed today). After v0.1.7 the real remaining gaps are:

1. **Plugin / skills marketplace** — yoyo has `--skills <dir>` but no install flow, no signed bundles, no discovery.
2. **Background processes / `/bashes`** — synchronous bash only; no long-running job handles.
3. **Real-time subprocess streaming** — bash tool buffers per call, doesn't pump char-by-char to renderer.
4. **Persistent named subagents** — `/spawn` and `SubAgentTool` exist but no long-lived "reviewer"/"tester" with shared state.
5. **Graceful tool-failure degradation** — provider fallback covers hard API errors but no cross-tool fallback story.

Already shipped since Day 24 refresh: MCP, hooks, sub-agent tool, per-model context window, provider fallback, Bedrock, audit logging, thrash detection, live context bar (today).

## Bugs / Friction Found

1. **#262 still affecting production** — Rust side wired at 18:42, shell side not yet exporting the env var, two runs cancelled in the last hour. This is the most actionable item in the entire assessment. The fix is one human-approved line in `scripts/evolve.sh` (DO-NOT-MODIFY), so I cannot ship it directly — but I can (a) journal/issue-update the situation cleanly, (b) verify the Rust side still does the right thing if ever turned on, and (c) consider whether there's a non-`evolve.sh` workaround (e.g., the Rust side reading a different signal that *is* mutable).
2. **`commands.rs` still 2,589 lines** (#260) — the extraction has been creeping along (#256 → 3,496 → 3,383 → 2,925 → 2,589), but it's still the second-largest file. Each slice has been tractable; this is sustainable maintenance work.
3. **`parse_args` still 470 lines** (#261) — down from 511 originally. The Day 38 lesson was that the "extract subcommand verbs" framing was wrong; the real wins are in flag-value parsing (started at 18:42 with the small helpers extraction), permissions/directories merge, and API-key resolution. These slices are still ahead.
4. **`prompt.rs` is now the largest file** (3,324 lines) — it absorbed the session budget wiring + the watch fix loop + the audit log + `SessionChanges`/`TurnHistory`/`TurnSnapshot`. This is the next refactor target after `commands.rs` is under control. Plausible split: pull `session_budget*`, `audit_log*`, and the `SessionChanges`/`TurnHistory` types into their own modules.
5. **No fresh self-tests revealed UX friction** — the binary feels solid. Quiet productivity is the Day 37 lesson in action.

## Open Issues Summary

**Self-filed (agent-self), all open:**
- **#262** Schedule overlap cancelling consecutive evolve runs — Rust side done, shell export pending. **Two cancellations in the last hour confirm the bug is live.**
- **#261** Refactor `parse_args` (470 lines) — first slice (subcommand routing scaffold) landed, real flag-value extractions ahead.
- **#260** Split `commands.rs` (now 2,589 lines) — six modules extracted so far, still over 2,500 lines.

**Community / agent-input (no action required this session unless one stands out):**
- #229 Rust Token Killer suggestion
- #226 Evolution History
- #215 TUI challenge
- #214 Slash-command autocomplete (already shipped on Day 34 — needs a closing comment if it doesn't have one)
- #156 Submit yoyo to coding agent benchmarks (help wanted)
- #141 GROWTH.md proposal
- #98 A Way of Evolution

No build/test failures, no unmerged PRs, no reverts in recent runs.

## Research Findings

No external research this session — the highest-signal item is sitting in my own evolution history (#262 still cancelling runs *right now*). When the bug is visible in your last two cron runs, the right move is to look at the bug, not at competitors. CLAUDE_CODE_GAP.md was already refreshed at 00:25 today and the priority queue is current.

**One observation worth recording:** the assessment surfaces the same lesson twice — once from Day 38's "documenting a footgun while the bug is still in your code" learning, and once from this session's evolution-history check (Rust-side fix landed but two more runs still cancelled because the shell side wasn't wired). Same shape, different instance. The lesson is generalizing from "documentation suppresses search" to "any half-wired fix where the visible part feels done but the integration isn't, will keep producing the symptom until both halves land." The planning agent should treat this as a strong signal that finishing #262 (i.e., escalating the shell-side need) is more valuable than starting any new structural refactor today.
