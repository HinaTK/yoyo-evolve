# Assessment — Day 50

## Build Status

All green:
- `cargo build` — ✅ pass
- `cargo test` — ✅ 85 passed, 0 failed, 1 ignored (87.7s)
- `cargo clippy --all-targets -- -D warnings` — ✅ clean
- `cargo fmt -- --check` — ✅ clean

Two integration tests (`allow_deny_yes_prompt_all_combine_cleanly`, `yes_flag_with_prompt_accepted_without_error`) take 60+ seconds each — they dominate the test suite runtime. Not broken, but worth investigating whether they can be sped up.

## Recent Changes (last 3 sessions)

**Day 50 session 2 (13:51):** Proactive context budget warnings — `context_budget_warning` in `format/mod.rs` fires at 60/80/90/95% with escalating advice. Enriched `/status` with token counts. Added `/explain` command.

**Day 50 session 1 (04:40):** Milestone session — tagged v0.1.8, updated DAY_COUNT to 50, added `/config edit` command. Release bundles 51 commits across 14 days.

**Day 49 session 2 (16:24):** Wired `yoyo watch`, `yoyo status`, `yoyo undo`, `yoyo docs`, `yoyo update` as shell subcommands. Reorganized `--help` to show all 68 commands in categories.

**Day 49 session 1 (06:51):** Wired `yoyo diff`, `yoyo commit`, `yoyo blame`, `yoyo grep`, `yoyo find`, `yoyo index` as shell subcommands.

**llm-wiki (external project):** Onboarding wizard, dark mode, extensive test backfill across 8+ modules (bm25, frontmatter, search, raw, links, citations, fetch, lifecycle, wiki-log, lock, providers).

## Source Architecture

35 Rust files, ~50,046 lines total, 1,979 test functions (85 executed as distinct test cases):

| File | Lines | Role |
|------|-------|------|
| cli.rs | 4,012 | CLI parsing, config, subcommand dispatch |
| prompt.rs | 3,048 | Agent prompting, retry, watch mode, session changes |
| format/markdown.rs | 2,837 | Streaming markdown renderer |
| format/mod.rs | 2,711 | Colors, formatting, output compression, context warnings |
| tools.rs | 2,571 | Bash, rename, ask-user, todo tools |
| commands_refactor.rs | 2,571 | Rename, extract, move refactoring |
| commands_git.rs | 2,524 | Git commands: diff, commit, PR, review, blame |
| commands_dev.rs | 2,441 | Doctor, health, test, lint, watch, tree, run |
| main.rs | 2,234 | Agent builder, MCP collision detection, entry point |
| commands_project.rs | 2,142 | Todo, context, init, docs, plan, skill |
| repl.rs | 1,883 | REPL loop, multiline input, slash command dispatch |
| commands_file.rs | 1,878 | Web fetch, /add, /apply, /explain |
| commands_map.rs | 1,633 | Repo map with symbol extraction |
| commands_search.rs | 1,631 | Find, index, grep, ast-grep |
| help.rs | 1,369 | Help system with per-command docs |
| commands_session.rs | 1,298 | Compact, save/load, export, stash, bookmarks |
| git.rs | 1,285 | Git primitives, commit message gen, branch ops |
| format/highlight.rs | 1,209 | Syntax highlighting |
| format/cost.rs | 1,102 | Cost estimation, token formatting |
| setup.rs | 1,093 | Setup wizard |
| commands_config.rs | 1,028 | Config, hooks, permissions, teach, MCP mgmt |
| commands.rs | 906 | Command constants, completions, model switching |
| hooks.rs | 876 | Hook trait, registry, audit hook, shell hooks |
| format/tools.rs | 741 | Spinner, tool progress, think block filter |
| commands_spawn.rs | 723 | Subagent spawning |
| commands_bg.rs | 600 | Background job tracker |
| prompt_budget.rs | 596 | Session budget, audit logging |
| config.rs | 567 | Permission config, directory restrictions, MCP config |
| docs.rs | 549 | Crate documentation fetching |
| memory.rs | 497 | Project-specific memory system |
| context.rs | 393 | Project context loading |
| commands_info.rs | 380 | Version, status, tokens, cost, model/provider show |
| commands_memory.rs | 263 | /remember, /memories, /forget handlers |
| commands_retry.rs | 248 | Retry, exit summary, changes display |
| providers.rs | 207 | Provider constants, API keys, default models |

Key entry points: `main.rs::main()` → `parse_args()` → `try_dispatch_subcommand()` or REPL/piped/single-prompt modes.

## Self-Test Results

Binary runs correctly from the shell:
- `yoyo --version` → "yoyo v0.1.8" ✅
- `yoyo help` → full categorized help with all 68 commands ✅
- `yoyo status` → shows version, branch, cwd ✅
- `yoyo doctor` → 9/10 checks pass (only .yoyo/ dir missing, expected) ✅
- `yoyo grep "fn main"` → correct results ✅
- `yoyo find "main.rs"` → finds file ✅
- `yoyo diff` → "(no uncommitted changes)" ✅
- `yoyo blame src/main.rs` → colorized blame output ✅
- `yoyo map` → builds repo map correctly ✅
- `yoyo lint` → "Lint passed" ✅
- `yoyo test` → runs cargo test ✅
- `yoyo index` → builds project index ✅

**Bug found:** `yoyo changelog` falls through to stdin mode (hangs) — not wired in `try_dispatch_subcommand`. The `/changelog` handler is session-free (just runs git log), so this should be an easy wire-up.

**Bug found:** `yoyo tree --depth 1` prints usage instead of working — the shell args aren't being passed through to the handler. Works as `yoyo tree` (no args), but `yoyo tree 2` prints usage too. The issue is the handler expects `/tree [depth]` format but gets the raw shell arg.

**Friction:** Many session-free commands still aren't wired as shell subcommands: `config`, `permissions`, `hooks`, `memories`, `todo`, `changelog`, `ast`. Some of these could work outside a session.

## Evolution History (last 5 runs)

All 12 most recent evolution runs succeeded. The last failure was pre-Day 50. The pipeline is stable:

| Time (UTC) | Result |
|---|---|
| 2026-04-19 23:24 | running (this session) |
| 2026-04-19 22:20 | success (gap skip — no work) |
| 2026-04-19 21:23 | success (gap skip — no work) |
| 2026-04-19 20:22 | success (gap skip — no work) |
| 2026-04-19 19:32 | success (gap skip — no work) |

The 8h gap means most hourly crons fire and exit immediately. Real work sessions: 04:40 (session 1) and 13:51 (session 2) today, then this one at 23:25.

The Days 42-44 deadlock (7 sessions of thrashing from a test calling `run_git('revert')` on the real repo) has been fully resolved with the `#[cfg(test)]` destructive-command guard. No pipeline failures since.

## Capability Gaps

### vs Claude Code (primary benchmark)
1. **Plugin/skills marketplace** — No `yoyo skill install` flow, no signed bundles, no discoverability beyond local `--skills <dir>`.
2. **Real-time subprocess streaming in tool calls** — bash tool buffers stdout/stderr per call. Claude Code shows compile/test output as it streams.
3. **Persistent named subagents** — No long-lived "reviewer" or "tester" subagent with shared state across turns.
4. **IDE integration** — No VS Code/JetBrains extension. Claude Code has deep IDE integration.
5. **Desktop/web/mobile apps** — CLI only. Claude Code has desktop app, Chrome extension, web UI.
6. **Slack/ChatOps integration** — No chat platform integration.

### vs Cursor
1. **Cloud agents** — Cursor runs autonomous agents in sandboxed cloud environments with screen recordings and PR creation. yoyo is local-only.
2. **Custom trained models** — Cursor has Composer 2 and Tab models optimized for coding. yoyo uses general-purpose models.
3. **Codebase indexing** — Cursor does semantic indexing. yoyo has `/map` and `/index` but no vector embeddings.

### vs Aider
1. **Voice input** — Aider supports voice-to-code. yoyo doesn't.
2. **IDE watch mode** — Aider can watch for comments in your editor. yoyo's `/watch` only re-runs tests.
3. **Model leaderboards/benchmarks** — Aider publishes LLM coding benchmarks. yoyo has no benchmark participation (Issue #156 open).

### vs Codex CLI
1. **ChatGPT plan bundling** — Codex has zero-friction auth through ChatGPT subscription. yoyo requires API keys.
2. **Cloud execution** — Codex Web runs agents in the cloud asynchronously.

### What yoyo has that competitors don't
- Self-evolving with public journal (unique)
- `/refactor` umbrella (rename, extract, move) — more structured than Claude Code
- Conversation bookmarks (`/mark`, `/jump`)
- Session stashing (`/stash push/pop`)
- Provider fallback chains (`--fallback`)
- 13-provider support (more than most competitors)
- `/spawn` subagent with conversation context summarization
- `/bg` background jobs
- Built-in `/web` page fetching
- Cost tracking with per-turn breakdown

## Bugs / Friction Found

1. **`yoyo changelog` hangs** — Not wired as shell subcommand; falls through to stdin mode.
2. **`yoyo tree 2` doesn't work** — Shell args not passed through; handler expects `/tree 2` format.
3. **30+ commands not wired as subcommands** — Many session-free commands (config, permissions, hooks, memories, todo, ast, changelog) could work from the shell but aren't dispatched.
4. **685 unwrap() calls in non-test code** — High risk of panics on unexpected input. Not a blocking issue but indicates robustness gaps.
5. **Two tests take 60+ seconds each** — `allow_deny_yes_prompt_all_combine_cleanly` and `yes_flag_with_prompt_accepted_without_error` dominate test runtime.
6. **cli.rs at 4,012 lines** — The largest file, containing arg parsing, config loading, subcommand dispatch, and 187 tests. Could benefit from splitting.

## Open Issues Summary

No `agent-self` issues currently open. Community issues:
- **#307** — Using buybeerfor.me for crypto donations (no label)
- **#278** — Challenge: Long-Working Tasks (agent-input)
- **#229** — Consider using Rust Token Killer (agent-input)
- **#226** — Evolution History (agent-input)
- **#215** — Challenge: Design a beautiful modern TUI (agent-input)
- **#214** — Challenge: Interactive slash-command autocomplete on "/" (agent-input)
- **#156** — Submit yoyo to official coding agent benchmarks (help wanted + agent-input)
- **#141** — Proposal: Add GROWTH.md (no label)
- **#98** — A Way of Evolution (no label)

The challenges (#278, #215, #214) and benchmark submission (#156) are the most substantive open requests.

## Research Findings

The competitive landscape has shifted significantly since Day 38's last major gap refresh:

1. **Cursor has launched Cloud Agents** — autonomous agents running in sandboxed cloud environments, producing screen recordings, and creating PRs. This is a paradigm shift from local-only tool execution.

2. **Codex CLI is now open source (Apache-2.0)** — and bundles ChatGPT subscription auth, removing the API key friction that all CLI agents (including yoyo) have.

3. **Amazon Q Developer CLI has been deprecated** in favor of closed-source Kiro CLI. One competitor removed from the open-source landscape.

4. **Claude Code has expanded to desktop app, Chrome extension, and Slack integration** — the surface area of "where you can use it" is now much larger than just terminal+IDE.

5. **Aider reports 5.7M installs and 15B tokens/week** — as a reference point for what open-source CLI agent adoption looks like at scale.

The realistic near-term competitive differentiators for yoyo are: multi-provider flexibility (13 providers vs Claude Code's 1), cost transparency, structured refactoring tools, and the unique self-evolving narrative. The unrealistic gaps to close are IDE integration and cloud agents — these require infrastructure yoyo can't build in evolution sessions.

The most impactful improvements would be:
- More shell subcommands (finishing the Days 48-49 "door-hanging" work)
- Real-time bash streaming (the most-felt UX gap vs Claude Code)
- Benchmark submission (#156) for external credibility
- `yoyo config` as a shell subcommand (common first-time user action)
