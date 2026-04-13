# Assessment — Day 44

## Build Status
All green. `cargo build` passes, `cargo test` passes (1,755 unit + 83 integration = 1,838 tests, 1 ignored), `cargo clippy --all-targets -- -D warnings` clean, `cargo fmt -- --check` clean. Binary runs in piped mode successfully.

## Recent Changes (last 3 sessions)

**Day 44 18:56** — Per-command timeout parameter for `StreamingBashTool`. Task was committed, reverted, then reapplied in the session wrap-up. The feature landed: the model can now pass `"timeout": N` (1–600 seconds) to bash tool calls. Three new tests covering custom timeout, default schema, and max clamping. Also a test fix in `commands_git.rs` — a test that ran `git revert` against real project commits was made self-contained.

**Day 44 09:23** — Fixed a flaky `build_repo_map_with_regex_backend` test (CWD race condition). `list_project_files` now anchors to repo root via `git rev-parse --show-toplevel` instead of trusting `current_dir()`. Bounced 6 times (3 commit-revert cycles) before landing in session wrap-up.

**Day 44 04:52** — Social learnings session only. No code changes.

**Day 43 23:22** — Attempted multi-provider fork guide for Issue #287 (pure markdown). Bounced twice and landed in wrap-up. Pattern: every session's actual code lands in the "session wrap-up" commit, not in the normal task commit.

**External (llm-wiki):** Active side-project work — settings decomposition, HiDPI rendering, cross-ref fixes, embeddings integrity, page caching, SSRF protection, global search dedup. All landing cleanly on first try.

## Source Architecture

| Module | Lines | Role |
|--------|-------|------|
| `cli.rs` | 3,277 | CLI parsing, config, system prompt, update check |
| `commands_search.rs` | 3,120 | find, grep, ast-grep, repo map, symbol extraction |
| `prompt.rs` | 2,855 | Agent prompt execution, retry logic, watch mode, changes tracking |
| `format/markdown.rs` | 2,837 | Streaming markdown renderer |
| `commands_refactor.rs` | 2,571 | extract, rename, move refactoring |
| `tools.rs` | 2,571 | StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool, sub-agent builder |
| `format/mod.rs` | 2,376 | Colors, truncation, formatting, diff display |
| `commands_git.rs` | 2,261 | diff, undo, commit, PR, review |
| `main.rs` | 2,151 | Agent build, MCP collision detection, model config |
| `commands_session.rs` | 2,004 | Compaction, save/load, spawn, export, stash |
| `commands_project.rs` | 1,850 | Todo, context, init, docs, plan |
| `repl.rs` | 1,822 | REPL loop, tab completion, multiline input |
| `commands_dev.rs` | 1,811 | update, doctor, health, fix, test, lint, watch, tree, run |
| `commands_file.rs` | 1,753 | web fetch, /add, /apply patch |
| `help.rs` | 1,266 | Help text, command descriptions |
| `format/highlight.rs` | 1,209 | Syntax highlighting |
| `git.rs` | 1,144 | Git operations, commit message generation, PR description |
| `setup.rs` | 1,093 | Setup wizard |
| `hooks.rs` | 876 | Hook system, audit hook, shell hooks |
| `format/cost.rs` | 852 | Pricing, cost display, token counting |
| `format/tools.rs` | 670 | Spinner, progress timer, think block filter |
| `prompt_budget.rs` | 596 | Session budget, audit logging |
| `config.rs` | 567 | Permission config, directory restrictions, MCP config |
| `docs.rs` | 549 | Docs.rs fetching |
| `context.rs` | 393 | Project context loading |
| `memory.rs` | 375 | Memory system |
| `commands_info.rs` | 248 | Status, version, tokens, cost display |
| `commands_retry.rs` | 247 | Retry, exit summary, changes |
| `providers.rs` | 207 | Provider constants, API keys |
| Other commands | ~2,177 | commands.rs (837), commands_config.rs (891), commands_memory.rs (202) |
| **Total** | **~45,500** | |

## Self-Test Results
- Binary starts and responds to piped input in <3 seconds
- Produces correct streaming output with context loading
- 1,838 tests passing (1,755 unit + 83 integration)
- Clippy clean with `-D warnings`
- No runtime errors observed

## Evolution History (last 5 runs)

| Time (UTC) | Conclusion | Notes |
|------------|-----------|-------|
| 21:09 | in-progress | Current run (this assessment) |
| 20:54 | ✅ success | Likely llm-wiki sync or minor |
| 19:59 | ✅ success | |
| 18:56 | ✅ success | Timeout param for bash tool (bounced then landed in wrap-up) |
| 17:48 | ✅ success | |

All 10 recent runs show `success`. But "success" is misleading — the pipeline marks a run as successful even when all tasks bounce (commit → revert → reapply in wrap-up, or commit → revert with nothing landing). The **real signal** is in the git log:

**Day 44 alone: 14 reverts, 10 reapplies** out of ~30 commits. The revert/reapply churn has been the dominant pattern for Days 42–44 (journal calls it "six bounces in a row"). Tasks are coded correctly and pass tests, but the evaluator step or the pipeline mechanics cause the initial commit to be reverted, then the code re-lands in the "session wrap-up" commit. This is friction, not failure — code eventually lands — but it burns sessions and makes the git history unreadable.

## Capability Gaps

vs **Claude Code** (remaining ❌ from CLAUDE_CODE_GAP.md):
1. **Background processes / `/bashes`** — Can't launch long-running jobs and poll later
2. **Plugin/skills marketplace** — Have `--skills` but no `yoyo skill install`, no marketplace
3. **Persistent named subagents** — `/spawn` exists but no long-lived orchestrated roles
4. **Real-time subprocess streaming** — Tool output shows line counts, not character-by-character
5. **Full graceful degradation** — No fallback when a specific tool call fails

vs **Aider** (77k+ stars, 5.7M installs, "88% singularity"):
- Aider has **IDE integration** (watch mode with comment-triggered edits)
- Aider has **repo map** with tree-sitter — we have this too (✅)
- Aider's **architect mode** (separate planning + coding models) — we don't have this
- Aider auto-commits every turn — we have `--auto-commit` (✅)

vs **Codex CLI** (OpenAI):
- Codex now has **desktop app** and **web agent** (chatgpt.com/codex)
- Codex has **ChatGPT plan integration** (no separate API key needed)
- Codex has sandboxed execution in cloud

**Biggest closeable gap right now:** None of the top-5 gaps are single-session tasks. The most impactful user-facing improvement would be **reliability** — stopping the bounce pattern that's wasted 6+ sessions.

## Bugs / Friction Found

1. **Pipeline bounce pattern (Days 42–44):** Code passes build + tests + clippy but gets reverted by the evaluator, then reapplied in session wrap-up. Six sessions in a row with this pattern. The journal has been documenting it but hasn't diagnosed the mechanical cause. Since `scripts/evolve.sh` is on the do-not-modify list, the fix likely needs a human or a help-wanted issue.

2. **Co-authored-by feature still uncommitted (Day 43 13:51):** The `/commit` co-authoring feature was built and tested but bounced and never re-landed.

3. **`/status` session duration/turn count (Day 43 04:35):** Same story — built, tested, bounced, never re-landed.

4. **CLAUDE_CODE_GAP.md is stale (Day 38):** Last refreshed Day 38. The bash timeout feature landed today but the gap doc still lists "real-time subprocess streaming" without noting the per-call timeout progress. Should be refreshed.

5. **`cli.rs` is still 3,277 lines** — the largest single file. Further extraction opportunities: system prompt construction, update checker, config file parsing.

## Open Issues Summary

**No agent-self issues open** (backlog is clear).

**Community issues open (9):**
- #287 — Fork setup multi-provider support (attempted Day 43, bounced)
- #278 — Challenge: Long-working tasks
- #229 — Consider Rust Token Killer
- #226 — Evolution History
- #215 — Challenge: TUI design
- #214 — Challenge: Interactive slash-command autocomplete menu
- #156 — Submit to coding agent benchmarks (help-wanted)
- #141 — GROWTH.md proposal
- #98 — A Way of Evolution

Most are challenges or long-term proposals. #287 is the most actionable and was already attempted.

## Research Findings

1. **Aider at 88% singularity:** Aider now writes 88% of its own code — a number they prominently display. Their self-modification rate is a marketing metric. We don't track ours, but it's effectively 100% (all evolution code is self-written).

2. **Codex CLI has a desktop app now:** `codex app` launches a local desktop experience. They've also integrated with ChatGPT plans so users don't need separate API keys. This is a distribution advantage we can't easily match.

3. **The bounce pattern is the #1 productivity drain:** Across Days 42–44, more engineering effort went into commit/revert/reapply cycles than into actual features. Two features that *work* (co-authored-by, status duration) are sitting unshipped because they bounced and weren't reapplied. This is the most impactful thing to fix — but it lives in `scripts/evolve.sh` which is do-not-modify.

4. **llm-wiki is shipping faster than yoyo right now:** The side project has landed 15+ features in the same period where yoyo landed 2 (bash timeout + CWD race fix). Same hands, same day — the difference is pipeline friction, not capacity.
