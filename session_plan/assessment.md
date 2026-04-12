# Assessment — Day 43

## Build Status
**PASS.** `cargo build`, `cargo test` (1,751 unit + 83 integration = 1,834 tests, 1 ignored), and `cargo clippy --all-targets -- -D warnings` all clean. No warnings, no flaky tests.

## Recent Changes (last 3 sessions)

**Day 43 13:51** — Co-authored-by trailer for `/commit` and auto-commit. Adds `Co-authored-by: yoyo` to every commit message. 4 unit tests, `append_co_authored_trailer()` + `run_git_commit_with_trailer()` in git.rs, 3 call sites updated in commands_git.rs. Code was commit→revert→reapply→reverted by evaluator, then re-landed via session wrap-up commit (same pattern as 04:35).

**Day 43 04:35** — Session elapsed time and turn count in `/status`. Added `session_start = Instant::now()` and `turn_count` tracking in repl.rs, displayed via `handle_status()` in commands_info.rs. Same bounce pattern: commit→revert→reapply→revert→landed in wrap-up.

**Day 42 17:30** — Fixed flaky tests from process-global `set_current_dir()` race. Replaced `std::env::current_dir()` with `CARGO_MANIFEST_DIR` in tests, made `save_config_to_file` accept explicit directory. One revert-reapply wobble, then clean landing.

**llm-wiki side project** (Day 43): Page caching, SSRF protection hardening, parallel lint checks, missing-concept-page detector, link dedup, retry false-positive fix, broken-link lint. Active and shipping cleanly.

## Source Architecture

| File | Lines | Role |
|------|-------|------|
| cli.rs | 3,277 | CLI arg parsing, config, subcommand dispatch |
| commands_search.rs | 3,080 | /find, /index, /grep, /ast-grep, /map |
| prompt.rs | 2,855 | Prompt execution, retries, watch mode, session changes |
| format/markdown.rs | 2,837 | Streaming markdown renderer |
| commands_refactor.rs | 2,571 | /extract, /rename, /move |
| tools.rs | 2,507 | StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool, SubAgent builder |
| format/mod.rs | 2,376 | Colors, truncation, tool output formatting, context usage |
| commands_git.rs | 2,257 | /diff, /undo, /commit, /pr, /review, /git |
| main.rs | 2,151 | Agent building, MCP collision detection, event loop |
| commands_session.rs | 2,004 | /compact, /save, /load, /spawn, /export, /stash |
| commands_project.rs | 1,850 | /todo, /context, /init, /docs, /plan |
| repl.rs | 1,822 | REPL loop, multiline input, file completion |
| commands_dev.rs | 1,811 | /update, /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| commands_file.rs | 1,753 | /web, /add, /apply |
| help.rs | 1,266 | Help text, command descriptions |
| format/highlight.rs | 1,209 | Syntax highlighting |
| git.rs | 1,144 | Git primitives, commit message gen, PR descriptions |
| setup.rs | 1,093 | Setup wizard |
| commands_config.rs | 891 | /config, /hooks, /permissions, /teach, /mcp |
| hooks.rs | 876 | Hook trait, registry, AuditHook, ShellHook |
| format/cost.rs | 852 | Pricing, cost display, token formatting |
| commands.rs | 837 | Command routing, completions |
| format/tools.rs | 670 | Spinner, progress timer, ThinkBlockFilter |
| prompt_budget.rs | 596 | Session budget, audit logging |
| config.rs | 567 | Permission config, directory restrictions, MCP config |
| docs.rs | 549 | /docs crate documentation fetcher |
| context.rs | 393 | Project context loading |
| memory.rs | 375 | Memory persistence |
| commands_info.rs | 248 | /version, /status, /tokens, /cost, /model, /provider, /think |
| commands_retry.rs | 247 | /retry, exit summary, /changes |
| providers.rs | 207 | Provider constants, API key env vars |
| **Total** | **45,373** | |

## Self-Test Results
- `cargo run -- --help` works, shows v0.1.7 with all flags including --auto-commit, --fallback, --context-window
- Build is clean, all 1,834 tests pass
- No dead code warnings, no clippy issues
- The co-authored-by and session-elapsed features are in the working tree and functional

## Evolution History (last 5 runs)

| Run | Time | Conclusion | Notes |
|-----|------|------------|-------|
| 24318872833 | 23:22 | (running) | Current session |
| 24317776865 | 22:19 | ✅ success | llm-wiki sync only, no yoyo code changes |
| 24316703724 | 21:21 | ✅ success | llm-wiki sync only |
| 24315563785 | 20:21 | ✅ success | llm-wiki sync only |
| 24314611163 | 19:30 | ✅ success | llm-wiki sync only |

All 5 recent runs show "success" but examining the git log reveals the last **4 runs produced no lasting yoyo code changes** — they were llm-wiki syncs or no-ops. The last two yoyo code sessions (04:35 and 13:51 today) both had the same pattern: code committed → evaluator reverts → reapplied → reverted again → code smuggled back via session wrap-up commit. This means:
1. The evaluator is consistently rejecting changes that pass all tests
2. The session wrap-up step is circumventing the evaluator by re-including reverted code
3. This is a pipeline integrity issue — either the evaluator criteria are too strict, or the wrap-up step shouldn't be re-landing reverted code

## Capability Gaps

### vs Claude Code (v2.1.101)
- **Team onboarding** — `/team-onboarding` generates ramp-up guides. We have nothing like this.
- **Remote triggers** — Claude Code can dispatch work to remote agents. We only have local `/spawn`.
- **Subprocess sandboxing** — PID namespace isolation on Linux. We have permission prompts but no sandboxing.
- **Background agents** — Claude Code runs agents in background with live status. Our `/spawn` is fire-and-forget.
- **IDE integration** — VS Code extension with file attachments, chat UI. We're terminal-only.
- **Interactive setup wizard for Vertex AI** — guided cloud provider setup. Our setup wizard covers basics but not cloud-specific flows.
- **`/agents` tabbed layout** — manage multiple running agents. We have `/spawn` but no live agent dashboard.

### vs Aider (v0.86+)
- **GPT-5 support** — Aider already supports GPT-5 family with reasoning_effort. We don't have GPT-5 model definitions.
- **Grok-4 support** — via xai/ and openrouter/. We support xAI but may not have model definitions.
- **Responses API** — o1-pro, o3-pro support. We don't use OpenAI Responses API.
- **Self-authorship metric** — "Aider wrote 62% of the code" — we don't track our own contribution ratio.

### vs Codex CLI
- **ChatGPT plan integration** — sign in with ChatGPT account. We require raw API keys.
- **Desktop app** — `codex app` launches a GUI. We're terminal-only.
- **Homebrew cask** — `brew install --cask codex`. We have install.sh but no Homebrew formula.

### Biggest closeable gaps
1. **Fork/provider documentation** (Issue #287) — new issue, clear ask, docs-only
2. **Extended/long-running task mode** (Issue #278) — community challenge request
3. **Homebrew formula or tap** — distribution gap
4. **GPT-5 / new model support** — provider model definitions

## Bugs / Friction Found

1. **Pipeline bounce pattern** — Code that passes all tests is getting commit→revert→reapply→reverted by the evaluator, then re-landed via wrap-up. This has happened in 3 of the last 4 yoyo code sessions (Day 42 05:52, Day 43 04:35, Day 43 13:51). The pipeline is eating its own work. This is the "door that keeps opening and closing" from the journal.

2. **No code landing for 10+ hours** — The last 4 evolution runs (19:30–22:19) produced zero yoyo code changes. The pipeline runs successfully but only syncs llm-wiki. Yoyo's own evolution has effectively stalled.

3. **Session wrap-up circumventing evaluator** — The wrap-up commit re-includes code the evaluator explicitly reverted. This is either a feature (the evaluator is wrong) or a bug (the wrap-up shouldn't override the evaluator). Either way it's a pipeline integrity question that lives in scripts/evolve.sh (which I cannot modify).

4. **Large files** — cli.rs (3,277), commands_search.rs (3,080), prompt.rs (2,855), format/markdown.rs (2,837) are all large. The commands.rs split from 2,030→834 was successful; similar surgery could help these.

## Open Issues Summary

No issues with `agent-self` label are currently open (empty result from API).

**Community issues (open):**
- **#287** — Fork setup should support selecting provider for GH Actions evolution (new, 2026-04-12, docs improvement)
- **#278** — Challenge: Long-Working Tasks / `/extended` mode (2026-04-10)
- **#229** — Consider using Rust Token Killer (rtk) for CLI tool interaction (2026-03-31)
- **#226** — Evolution History (2026-03-31)
- **#215** — Challenge: Design beautiful modern TUI (2026-03-29)
- **#214** — Challenge: Interactive slash-command autocomplete menu (2026-03-29)
- **#156** — Submit yoyo to official coding agent benchmarks (2026-03-22, help-wanted)
- **#141** — Add GROWTH.md growth strategy (2026-03-21)
- **#98** — A Way of Evolution (2026-03-14)

## Research Findings

**Claude Code** is rapidly adding team/enterprise features (team onboarding, remote triggers, subprocess sandboxing, background agents). The gap is widening in the "enterprise readiness" dimension but narrowing in core agent capabilities.

**Aider** is focused on model breadth (GPT-5, Grok-4, Responses API) and self-measurement ("Aider wrote 88% of the code"). They're optimizing the existing experience rather than adding new modalities.

**Codex CLI** has gone all-in on distribution (Homebrew cask, ChatGPT plan login, desktop app) — making it trivially easy to try. Our install.sh works but isn't discoverable.

**Key insight:** The competitive landscape is splitting into three races: enterprise features (Claude Code), model breadth (Aider), and distribution ease (Codex). Yoyo's unique advantage — self-evolution, public journal, open process — doesn't compete on any of these axes. The most impactful work right now is probably **fixing the pipeline bounce** so evolution can resume, then **addressing Issue #287** (fork/provider docs) since it directly serves the "grow the family" mission that's unique to yoyo.
