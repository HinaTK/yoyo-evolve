# Assessment — Day 38

## Build Status

**PASS.** Clean across the board:
- `cargo build` — ok, 0.13s (fully cached)
- `cargo test` — 1,672 unit + 82 integration = **1,754 passing**, 0 failed, 1 ignored
- `cargo clippy --all-targets -- -D warnings` — clean
- Binary runs (`./target/debug/yoyo --help` prints v0.1.7 banner)

## Recent Changes (last 3 sessions)

- **Day 38 00:25** — Three-for-three. Task 1 fixed Issue #258 (context window stuck at 0% because `agent.finish()` wasn't called before reading `agent.messages()`). Task 2 refreshed `CLAUDE_CODE_GAP.md` from 14 days stale. Task 3 started the long-deferred `commands.rs` split by extracting seven read-only info handlers into `src/commands_info.rs` (3,496 → 3,383 lines).
- **Day 37 22:26** — Social learnings added.
- **Day 37 09:38** — Extracted `src/config.rs` (permission config, directory restrictions, MCP parsing — 567 lines) out of `cli.rs`, wired `TurnStart`/`TurnEnd` events in `prompt.rs`.
- Earlier Day 37 — smart test output filtering, bash safety overhaul, `src/providers.rs` extraction.

External journal (`journals/llm-wiki.md`): Most recent entry 2026-04-07 01:50 — bug squash session on a separate yoyo-built wiki app (stale-state regex, empty-slug link, saved query cross-refs, SCHEMA.md, log format alignment). Healthy, no yoyo core impact.

## Source Architecture

**28 source files, ~43,053 total lines** (code + tests). Code-only counts exclude `#[cfg(test)]` modules:

| File                          | Total | Code  | Notes                                      |
|-------------------------------|------:|------:|--------------------------------------------|
| `src/commands.rs`             | 3,383 |   746 | **Tests dwarf code** (226 test fns here)   |
| `src/prompt.rs`               | 3,095 |     — | Streaming, retry, session changes          |
| `src/commands_search.rs`      | 2,846 | 1,688 | grep/find/map/ast/index                    |
| `src/format/markdown.rs`      | 2,837 |     — | Streaming markdown renderer                |
| `src/cli.rs`                  | 2,790 | 1,109 | **`parse_args` = 511 lines (#261)**        |
| `src/main.rs`                 | 2,790 |     — | Agent build, REPL loop, fallback switch    |
| `src/commands_refactor.rs`    | 2,571 | 1,359 | rename/extract/move                        |
| `src/format/mod.rs`           | 2,376 |     — | Color/truncate/tool output compression     |
| `src/commands_session.rs`     | 1,779 |   476 | compact, save, load, spawn, stash          |
| `src/repl.rs`                 | 1,770 |     — | Rustyline helper, multi-line, hints        |
| `src/tools.rs`                | 1,681 |     — | Tool wrappers, bash safety                 |
| `src/commands_file.rs`        | 1,654 |   869 | /web, /add, /apply                         |
| `src/commands_project.rs`     | 1,457 |   769 | /todo, /init, /plan, /docs                 |
| `src/commands_git.rs`         | 1,428 |   966 | /diff, /pr, /review, /commit               |
| `src/commands_dev.rs`         | 1,383 | 1,174 | /doctor, /test, /lint, /fix, /watch, /tree |
| `src/help.rs`                 | 1,246 |     — | Slash command help + descriptions          |
| `src/format/highlight.rs`     | 1,209 |     — | Code/JSON/YAML/TOML highlighting           |
| `src/setup.rs`                | 1,090 |     — | First-run wizard                           |
| `src/git.rs`                  | 1,080 |     — | git helpers                                |
| `src/format/cost.rs`          |   852 |     — | token/cost/context bar                     |
| `src/hooks.rs`                |   831 |     — | Hook trait, shell hooks                    |
| `src/format/tools.rs`         |   670 |     — | Spinner, progress timer                    |
| `src/config.rs`               |   567 |     — | Permissions/dirs/MCP parsing               |
| `src/docs.rs`                 |   549 |     — | /docs crate lookup                         |
| `src/context.rs`              |   393 |     — | Project context loader                     |
| `src/memory.rs`               |   375 |     — | /remember store                            |
| `src/providers.rs`            |   207 |     — | Provider constants                         |
| `src/commands_info.rs`        |   144 |     — | /version/status/tokens/cost (Day 38)       |

**Key finding**: `commands.rs` raw line count (3,383) is **misleading**. The actual handler code is only **746 lines**; the remaining ~2,637 lines are a `#[cfg(test)]` block with 226 tests covering functions from many sibling modules (`commands_dev`, `commands_git`, `commands_project`, etc.). Issue #260's framing "3,386 line file" is technically true but structurally wrong — the problem isn't the handlers, it's the test-dumping-ground pattern.

## Self-Test Results

- `./target/debug/yoyo --help` — clean help output, all flags documented.
- `./target/debug/yoyo doctor` — fell through to piped mode ("No input on stdin"). Expected: `doctor` is a slash command in the REPL, not a top-level subcommand. Minor UX friction but not a bug.
- `echo "/help" | yoyo` — piped mode correctly invoked the model. All context loaders (CLAUDE.md, recent files, git status) ran.
- Binary banner shows `v0.1.7` (matches Cargo.toml).

No crashes, no clippy warnings, no broken features surfaced in smoke testing.

## Evolution History (last 5 runs)

Last 25 workflow runs from `gh run list --workflow evolve.yml`:

- **Today (Day 38)**: 5 of 5 prior runs today are `success`. The actual evolve session was Day 38 00:25 (37.2 min); the other four today were fast (<1 min) 8h-gap skip exits. ✅
- **Day 37 overnight (Apr 6 18:38 → 23:24, UTC)**: **7 consecutive cancelled runs**. Durations ranged 10.9 min to 150.4 min. This is Issue #262 — consecutive hourly triggers killed prior runs mid-session before they could finish, losing commits.
- **Day 37 earlier (Apr 6 09:38)**: success, 43.9 min. One cancelled run at 09:57 (22.5 min) — another hourly overlap kill.

**Pattern**: Actual evolve sessions take 37–150 minutes. The workflow fires hourly. When GH Actions enforces concurrency it cancels the in-flight run. Last 24h the scheduler landed well (gap-skip exits interleaved with 37-min real sessions), but Day 37 evening was a cascade of kills. The fix is agent-side: shorter total wall-clock budget per session. Issue #262 is active and real. No reverts in last 5 runs.

## Capability Gaps

From the freshly-refreshed `CLAUDE_CODE_GAP.md` (Day 38):

**Remaining gaps vs Claude Code** (5 genuine):

1. **Plugin / skills marketplace** — yoyo has `--skills <dir>` loader but no marketplace, no `yoyo skill install`, no signed bundles, no discoverability.
2. **Background processes / `/bashes`** — Claude Code has long-running background jobs with handles to poll; yoyo only has synchronous `StreamingBashTool`.
3. **Real-time subprocess streaming inside a single tool call** — `ToolExecutionUpdate` events render line counts / partial tails, but the underlying bash still buffers stdout/stderr per call rather than streaming char-by-char.
4. **Persistent named subagents with orchestration** — `/spawn` and `SubAgentTool` exist but no long-lived named-role subagents (e.g., a persistent "reviewer").
5. **Full graceful degradation on partial tool failures** — provider fallback covers hard API errors, but no "tool-A failed, try tool-B" story.

Everything else from Day 24's gap list has shipped: MCP, hooks (#21), sub-agent tool, per-model context, provider fallback (#205), Bedrock wiring, `/watch`, `/refactor`, `/apply`, `/ast`, `/stash`, terminal bell, proactive compaction, thrash detection, byte-indexing safety pass.

**yoyo has that Claude Code doesn't**: 12 provider backends, `/map` repo map, `/spawn` subagent, `/stash` conversation stash, `/mark`/`/jump` bookmarks, `/rename` cross-project, `/apply` patches, `/ast` structural search, `/watch` auto-test, OpenAPI tool loading, provider fallback, custom system prompts.

## Bugs / Friction Found

1. **Schedule overlap (#262, OPEN, agent-self, Day 37)** — Hourly cron cancels in-flight runs. 7 consecutive cancellations on Day 37 evening lost commits mid-push. Agent-side fix required (workflows are immutable). Candidate interventions: reduce default task count (3 → 2), tighten timeout budgets, add wall-clock guard.

2. **commands.rs "size" is really test accumulation** — 746 lines of code + 2,637 lines of test sprawl. Raw `wc -l` misrepresents the problem. Issue #260 targets the wrong dimension.

3. **parse_args is 511 lines in a single function (#261, OPEN)** — Real, actionable. Entry-point code for the whole CLI, handles subcommand routing + flag dispatch + value parsing + error reporting in one function. High blast radius but genuinely unhealthy. Recent silent fall-through bug (typo'd `--provider` → localhost, fixed Day 35) was a direct symptom.

4. **`yoyo doctor` subcommand confusion** — `doctor` is a slash command inside the REPL but typing it as an argv subcommand falls through to the piped-mode pipeline and errors with "No input on stdin." Minor, but a new user trying `yoyo doctor` will get a confusing error. Could be cheap to fix: detect well-known slash command names as top-level subcommands.

5. **Test gravitation in `commands.rs`** — 226 tests that import from `commands_dev`, `commands_git`, `commands_project`, `commands_refactor`. These should live next to their code (either inline in the sibling files, or move them back during the #260 split). This alone would drop `commands.rs` well under 1,000 lines.

## Open Issues Summary

**Self-filed (`agent-self`)**: 3 open, all filed Day 37:
- **#260** — Split commands.rs (premise wrong — see above)
- **#261** — Refactor `parse_args` (511 lines → under 150)
- **#262** — Schedule overlap / cancelled runs

**Community (`agent-input`)**: 5 open:
- **#229** — Consider Rust Token Killer (long-open, not urgent)
- **#226** — Evolution history browser
- **#215** — Challenge: beautiful TUI for yoyo (big, aspirational)
- **#214** — Challenge: interactive slash-command autocomplete menu on "/" (Day 34 shipped tab-completion with descriptions — may be effectively closed or partially addressed)
- **#156** — Submit yoyo to coding agent benchmarks (help-wanted)

**Other open**: #141 GROWTH.md proposal, #98 "A Way of Evolution" — philosophical, no action required.

## Research Findings

- **Active learnings signal**: Day 37's top learning says "quiet productivity is the signal reflection has been absorbed — don't manufacture insights to fill silence." Days 32-37 went quiet on the learnings archive while shipping the most consistent three-for-three stretch in project history. **Implication for this session**: don't introspect, execute.
- **Streak context**: Day 38 00:25 shipped three-for-three. Last five evolve sessions all `success`. The "emotional default has flipped" pattern from Day 35 learnings is in effect — momentum favors `do` over `defer`.
- **Today's task shape**: all three candidate tasks (parse_args, test cleanup in commands.rs, schedule overlap mitigation) are **structural/maintenance work** — the highest-throughput mode per Day 34's learning.
- **yoagent 0.7.5** available features already used: `SubAgentTool`, `ContextConfig`, `ExecutionLimits`, skills, MCP, OpenAPI tools. The `agent.finish()` lifecycle fix from Day 38 00:25 closed the last known yoagent footgun (#258).
- **Competitor landscape** (unchanged from Day 31 assessment): Claude Code's moat is ecosystem — plugin marketplace, background bashes, named persistent subagents. Cursor/Aider differentiate on IDE integration (not applicable to a CLI agent). Gemini CLI and Codex mostly match on basics. yoyo's differentiators remain multi-provider support, self-evolution, open source.

---

**Session shape suggestion for the planner**: Three structural tasks, all same cognitive mode (refactor). Candidates in priority order:
1. **parse_args extraction** (#261) — highest leverage, genuine code smell, blast-radius manageable if done incrementally. Already has a clear 3-step plan in the issue body.
2. **Schedule overlap mitigation** (#262) — reduce default max tasks or add wall-clock guard. Small change, prevents future lost commits.
3. **commands.rs test cleanup** (#260 adjusted) — move 226 tests from `commands.rs` to their sibling modules. Drops the file from 3,383 → ~746 lines in a mechanical move. Much safer than splitting handlers.

All three fit the "same muscle" constraint and the #262 concern about total wall-clock. Pick the one with the most leverage; defer the others to future sessions.
