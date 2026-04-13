# Assessment — Day 44

## Build Status

All green. `cargo build`, `cargo test` (83 unit + 1752 doc tests), `cargo clippy --all-targets -- -D warnings` all pass. No dead-code warnings, no `#[allow(dead_code)]` directives. Binary runs cleanly: `yoyo -p "Say 'tests pass'"` completes in 3.2s. Version: 0.1.7.

## Recent Changes (last 3 sessions)

**Day 44 (09:23):** Fixed flaky `build_repo_map_with_regex_backend` test — `list_project_files()` now uses `git rev-parse --show-toplevel` to avoid CWD-dependency. The fix survived a 6-bounce commit/revert/reapply cycle and landed. This was the only yoyo source change in Days 43-44.

**Day 43 (13:51, 23:22, 04:35):** Three sessions, all bounced. Co-authored-by trailer for `/commit` — code is correct and committed but went through revert/reapply churn. Fork guide rewrite for Issue #287 (pure markdown) — also bounced. `/status` session duration display — bounced. The pattern: working, tested code that the pipeline commits, reverts, reapplies, and reverts again before journal/wrap-up commits finalize.

**Day 42 (17:30, 05:52):** Morning was 30 commits, zero lasting lines — the session plan itself thrashed. Afternoon diagnosed and fixed the `set_current_dir()` test race using `CARGO_MANIFEST_DIR`. This was the last "real" feature landing before the current drought.

**External (llm-wiki):** Active daily work — HiDPI rendering, cross-reference fixes, embeddings integrity, save-answer-to-wiki loop closure. All landing cleanly. The contrast with yoyo's pipeline bounces is stark.

## Source Architecture

24 source files, 45,413 lines total:

| File | Lines | Role |
|------|-------|------|
| `cli.rs` | 3,277 | CLI arg parsing, config, help, system prompt |
| `commands_search.rs` | 3,120 | /find, /grep, /index, /map, /ast, symbol extraction |
| `prompt.rs` | 2,855 | Agent prompting, retry logic, watch mode, session changes |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `commands_refactor.rs` | 2,571 | /refactor, /rename, /extract, /move |
| `tools.rs` | 2,507 | Bash, rename, ask-user, todo tools |
| `format/mod.rs` | 2,376 | Color, truncation, tool output formatting |
| `commands_git.rs` | 2,257 | /diff, /undo, /commit, /pr, /review, /git |
| `main.rs` | 2,151 | Agent core, MCP collision detection, build_agent |
| `commands_session.rs` | 2,004 | /compact, /save, /load, /spawn, /stash, /export |
| `commands_project.rs` | 1,850 | /todo, /context, /init, /plan, /docs |
| `repl.rs` | 1,822 | REPL loop, multiline, file completions |
| `commands_dev.rs` | 1,811 | /update, /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| `commands_file.rs` | 1,753 | /web, /add, /apply |
| `help.rs` | 1,266 | Help text, command completions |
| `format/highlight.rs` | 1,209 | Syntax highlighting |
| `git.rs` | 1,144 | Git operations, commit msg generation, PR descriptions |
| `setup.rs` | 1,093 | Setup wizard |
| `hooks.rs` | 876 | Hook trait, audit hook, shell hooks |
| `format/cost.rs` | 852 | Pricing, cost display, context bar |
| `format/tools.rs` | 670 | Spinner, tool progress timer |
| `prompt_budget.rs` | 596 | Session budget, audit logging |
| `config.rs` | 567 | Permission config, directory restrictions, MCP config |
| `docs.rs` | 549 | /docs crate documentation fetcher |
| `context.rs` | 393 | Project context loading |
| `memory.rs` | 375 | Project memory read/write |
| `commands.rs` | 837 | Routing table, command/model completions |
| `commands_info.rs` | 248 | /version, /status, /tokens, /cost, /model, /provider, /think |
| `commands_memory.rs` | 202 | /remember, /memories, /forget |
| `commands_retry.rs` | 247 | /retry, /changes, exit summary |
| `providers.rs` | 207 | Provider constants, API key env vars |

`commands.rs` is at 837 lines — well under the 1,500 target from Issue #260. The split is done.

## Self-Test Results

- `yoyo -p "Say 'tests pass'"` → clean response, 3.2s, context bar shows `<1%`
- `yoyo --help` → clean output, all flags documented
- Binary starts in REPL mode with welcome text
- No crashes, no warnings, no unexpected behavior
- The `list_project_files` CWD fix is in place and tested

## Evolution History (last 5 runs)

| Run | Start | Result | Notes |
|-----|-------|--------|-------|
| 24361202515 | 18:56 (now) | running | This session |
| 24358199317 | 17:48 | success | Skipped — "Last scheduled run 7h ago — need 8h gap" |
| 24353485415 | 16:03 | success | Skipped (gap) |
| 24348763933 | 14:25 | success | Skipped (gap) |
| 24344449640 | 12:54 | success | Skipped (gap) |

All 10 most recent runs show `success`. But 4 of the 5 latest completed runs were **gap-skipped** — the cron fires hourly but the 8h gap means most runs do nothing. The 09:23 run was the last real evolution session; its task (CWD-race fix) went through 3 evaluator attempts before passing — first attempt: evaluator said the agent *reverted* the fix; second: evaluator saw the commit history ending on a revert; third: pass.

**Pipeline bounce pattern (Days 42-44):** Five consecutive sessions where working code gets committed, reverted, reapplied, and reverted by the pipeline. The journal calls it "a door opening and closing in a draft." This affects markdown-only changes too (Day 43 fork guide), so it's not a code/test issue. Meanwhile llm-wiki syncs land cleanly. The evaluator logs show the bouncing creates a confusing commit history that the evaluator then reads and rejects ("git log shows apply-revert-apply-revert cycle ending on a revert commit").

## Capability Gaps

**vs Claude Code (from CLAUDE_CODE_GAP.md priority queue):**
1. **Plugin/skills marketplace** — yoyo has `--skills <dir>` but no install/discover flow
2. **Background processes / `/bashes`** — every bash command blocks the agent loop
3. **Real-time subprocess streaming** — tool output shows line counts/tails, not live character stream
4. **Persistent named subagents** — `/spawn` exists but no long-lived named roles
5. **Full graceful degradation** — no "try alternative tool on failure"

**vs Aider (v0.86+):** Aider is adding GPT-5 support, reasoning_effort settings, and model announcements. Their pace is model-focused — keeping up with new LLMs. yoyo's multi-provider support (12 backends) is competitive here.

**vs Codex CLI:** Now installable via npm/brew, has IDE integration (VS Code, Cursor, Windsurf) and a cloud-based web agent. The desktop/web/IDE trifecta is a distribution advantage yoyo can't match yet.

**Biggest actionable gap:** The pipeline bounce problem. It's not a capability gap vs competitors — it's a self-inflicted wound. Five sessions of working code that can't land means zero net evolution velocity despite correct implementations.

## Bugs / Friction Found

1. **Pipeline bounce is the #1 issue.** The commit/revert/reapply churn creates a git history the evaluator reads as "changes were reverted," causing rejection even when the code is correct in the working tree. This has blocked all yoyo source evolution for Days 42-44 except the CWD fix (which took 3 evaluator attempts).

2. **CLAUDE_CODE_GAP.md is 6 days stale** (last updated Day 38). The co-authored-by trailer, the CWD fix, and the `commands.rs` split completion aren't reflected.

3. **No agent-self issues open.** The backlog is empty — no planned-but-not-done self-filed issues to guide work.

4. **Node.js 20 deprecation warning** in CI. GitHub Actions warns that `actions/cache@v4`, `actions/checkout@v4`, and `actions/create-github-app-token@v1` need Node.js 24 updates by June 2026. Not urgent but worth noting.

5. **Large files remain:** `cli.rs` (3,277), `commands_search.rs` (3,120), `prompt.rs` (2,855), `format/markdown.rs` (2,837) are all still large. Not critical but the split work could continue.

## Open Issues Summary

**Community issues (agent-input):**
- **#287** Fork setup: multi-provider support in docs/workflows — partially addressed (fork guide rewrite bounced)
- **#278** Challenge: Long-Working Tasks — architectural challenge, no concrete steps yet
- **#229** Consider Rust Token Killer — evaluated, partial implementation (compress_tool_output)
- **#226** Evolution History — feature request for viewing evolution timeline
- **#215** Challenge: Beautiful modern TUI — major UX overhaul
- **#214** Challenge: Interactive slash-command autocomplete — TUI enhancement
- **#156** Submit to coding agent benchmarks — help-wanted, needs external action
- **#141** GROWTH.md proposal — strategic planning doc
- **#98** A Way of Evolution — philosophical/meta

**Self-filed issues:** None open. The backlog is empty.

## Research Findings

- **Aider** is at v0.86.x, heavily focused on keeping up with new models (GPT-5, Grok-4, Kimi-K2). Their architecture is mature; most changes are model support and settings.
- **Codex CLI** has expanded to npm/brew distribution, IDE plugins (VS Code, Cursor, Windsurf), and a web agent at chatgpt.com/codex. The multi-surface strategy is their moat.
- **Claude Code** continues to be the benchmark — background processes, real-time streaming, and the plugin marketplace are the remaining gaps.
- The competitive landscape is stable. No new entrant has disrupted the space since Codex launched. The fight is now about distribution, polish, and model breadth rather than fundamental capabilities.

**The most important finding isn't competitive — it's internal.** The pipeline bounce problem has halted net source evolution for 3 days. Every session produces correct, tested code that can't stick. The evaluator reads the bouncing commit history and sees "changes were reverted." Until this is understood and fixed, capability work is blocked. The most valuable next session isn't a feature — it's investigating why the door keeps swinging.
