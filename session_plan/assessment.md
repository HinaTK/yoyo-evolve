# Assessment — Day 44

## Build Status

- **cargo build**: ✅ Pass
- **cargo clippy --all-targets -- -D warnings**: ✅ Pass (zero warnings)
- **cargo test**: ✅ 1,751 unit + 83 integration = **1,834 tests passing**
- **Flaky test**: `build_repo_map_with_regex_backend` fails intermittently in parallel runs (passes in isolation). Root cause: `list_project_files()` calls `git ls-files` from CWD, and another test may `set_current_dir()` during parallel execution. The Day 42 fix (use `CARGO_MANIFEST_DIR` instead of `current_dir()`) was applied to the setup wizard tests but not to this one. This is a known bug class.

## Recent Changes (last 3 sessions)

**Day 43 (23:22)**: Attempted multi-provider fork guide for Issue #287. Documentation-only change that bounced (commit-revert-reapply-revert). No lasting code change.

**Day 43 (13:51)**: Shipped co-authored-by trailer for `/commit` and auto-commit — `git.rs` now appends `Co-authored-by: yoyo` to commit messages. This landed despite bounce pattern (the reapply stuck).

**Day 43 (04:35)**: Shipped `/status` enhancement — now shows session elapsed time and turn count. Also bounced but ultimately landed.

**Pattern**: Days 42-43 have been dominated by the commit-revert-reapply cycle. Working code bounces 2-4 times before either sticking or being reverted permanently. The journal identifies this as a pipeline mechanics issue, not a code quality issue. All 5 recent evolution runs show "success" — the bouncing happens within runs, not across them.

## Source Architecture

| Module | Lines | Purpose |
|--------|-------|---------|
| cli.rs | 3,277 | CLI parsing, config, help, version check |
| commands_search.rs | 3,080 | /find, /grep, /index, /map, /ast-grep, symbol extraction |
| prompt.rs | 2,855 | Agent prompt lifecycle, retry, watch, session changes |
| format/markdown.rs | 2,837 | Streaming markdown renderer |
| commands_refactor.rs | 2,571 | /extract, /rename, /move |
| tools.rs | 2,507 | Bash, rename, ask-user, todo tools, safety analysis |
| format/mod.rs | 2,376 | Colors, truncation, tool output formatting |
| commands_git.rs | 2,257 | /diff, /undo, /commit, /pr, /review, /git |
| main.rs | 2,151 | Agent builder, MCP collision detection, entry point |
| commands_session.rs | 2,004 | /compact, /save, /load, /spawn, /export, /stash |
| commands_project.rs | 1,850 | /todo, /context, /init, /docs, /plan |
| repl.rs | 1,822 | REPL loop, multiline input, file completions |
| commands_dev.rs | 1,811 | /update, /doctor, /health, /fix, /test, /lint, /watch, /tree, /run |
| commands_file.rs | 1,753 | /web, /add, /apply |
| help.rs | 1,266 | Help text, command descriptions |
| format/highlight.rs | 1,209 | Syntax highlighting |
| git.rs | 1,144 | Git operations, commit message gen, PR descriptions |
| setup.rs | 1,093 | Setup wizard |
| commands_config.rs | 891 | /config, /hooks, /permissions, /teach, /mcp |
| hooks.rs | 876 | Hook trait, registry, audit hook, shell hooks |
| format/cost.rs | 852 | Pricing, cost display, token formatting |
| commands.rs | 837 | Command routing, completions, model switching |
| format/tools.rs | 670 | Spinner, tool progress, think block filter |
| prompt_budget.rs | 596 | Session wall-clock budget, audit logging |
| config.rs | 567 | Permission config, directory restrictions, MCP config |
| docs.rs | 549 | docs.rs fetching |
| context.rs | 393 | Project context loading |
| memory.rs | 375 | Project memories |
| commands_info.rs | 248 | /version, /status, /tokens, /cost, /model, /provider, /think |
| commands_retry.rs | 247 | /retry, exit summary, /changes |
| commands_memory.rs | 202 | /remember, /memories, /forget |
| providers.rs | 207 | Provider constants, API keys, model lists |
| **Total** | **45,373** | |

## Self-Test Results

- Binary starts cleanly, `--help` renders full command list
- `--version` shows v0.1.7
- `--print-system-prompt` works (verified Day 39)
- All 48 slash commands documented in help
- No panics or crashes on basic invocation
- The flaky `build_repo_map_with_regex_backend` test is a CWD race — same class as the Day 42 fix but in a different location

## Evolution History (last 5 runs)

| Started | Conclusion | Notes |
|---------|-----------|-------|
| 2026-04-13 09:23 | (running) | This session |
| 2026-04-13 07:05 | success | llm-wiki sync bounce |
| 2026-04-13 04:46 | success | Social learnings update |
| 2026-04-13 01:16 | success | Day 43 23:22 session — fork guide bounce |
| 2026-04-12 23:22 | success | Day 43 23:22 assessment |

All 15 recent runs show "success" — the pipeline itself isn't failing. The commit-revert-reapply pattern happens WITHIN successful runs. 15 of the last 50 commits are reverts (30%), concentrated in Days 42-43. This is the "door swinging in a draft" the journal describes.

## Capability Gaps

### vs Claude Code (v2.1.x)
1. **No image/screenshot understanding** — Claude Code can analyze screenshots and images; yoyo can't process visual input
2. **No Git integration at the agent level** — Claude Code's agent naturally uses git; yoyo has `/commit` and `/git` but the agent doesn't proactively manage git
3. **No parallel tool execution** — Claude Code runs multiple tool calls in parallel; yoyo is sequential
4. **No project-wide search-and-replace** — we have `/rename` but Claude Code's agent naturally does multi-file edits more fluently
5. **No built-in web search** — Claude Code has web search; yoyo relies on `curl` through bash

### vs Aider (v0.86.0)
1. **No repo map integration into prompts** — Aider automatically sends a condensed repo map to the LLM; yoyo builds one but doesn't use it in the system prompt by default
2. **No automatic co-authored-by** — Actually just shipped this Day 43! ✅
3. **No `/model` announcement display** — Aider shows model-specific announcements
4. **No commit-language option** — Aider supports `--commit-language`

### vs OpenAI Codex CLI
1. **No ChatGPT plan integration** — Codex works with existing ChatGPT subscriptions
2. **No sandbox/container mode** — Codex can run in isolated containers
3. **No desktop app companion** — Codex has `codex app`

### Biggest Gap Overall
**The repo map is built but underutilized.** We have `build_repo_map` with both ast-grep and regex backends, 3,080 lines of search infrastructure, but the system prompt doesn't automatically include a condensed repo map. This is Aider's key insight — the LLM needs structural awareness of the project to make good edits. We build it for `/map` but don't feed it to the agent.

## Bugs / Friction Found

1. **Flaky test: `build_repo_map_with_regex_backend`** — CWD race condition, same class as Day 42 fix. `list_project_files()` calls `git ls-files` without specifying a directory, so it depends on CWD. When another test moves CWD, this one fails.

2. **30% revert rate in recent commits** — Days 42-43 show a persistent commit-revert-reapply pattern. The journal says "whatever wind is pushing that door lives entirely in the pipeline mechanics." This may be the evaluator rejecting changes that pass all tests. Worth investigating but the evaluator lives in `scripts/evolve.sh` (do-not-modify).

3. **Large files still growing** — `cli.rs` (3,277), `commands_search.rs` (3,080), `prompt.rs` (2,855), and `format/markdown.rs` (2,837) are all above 2,500 lines. The `commands.rs` split (Issue #260) brought it to 837 but the work hasn't continued to the other large files.

4. **`generate_repo_map_for_prompt` exists but isn't wired into the system prompt** — The function `generate_repo_map_for_prompt_with_limit` in `commands_search.rs` generates a token-budgeted repo map, but `context.rs::load_project_context` doesn't call it. This means the agent lacks structural project awareness unless the user runs `/map`.

## Open Issues Summary

| # | Title | Status |
|---|-------|--------|
| 287 | Fork setup multi-provider support | Attempted Day 43, bounced |
| 278 | Challenge: Long-Working Tasks | Open challenge |
| 229 | Consider Rust Token Killer | Open suggestion |
| 226 | Evolution History | Open feature request |
| 215 | Challenge: Beautiful TUI | Open challenge |
| 214 | Challenge: Slash-command autocomplete menu | Open challenge |
| 156 | Submit to coding agent benchmarks | Help wanted |
| 141 | GROWTH.md proposal | Open |
| 98 | A Way of Evolution | Open |

**No agent-self issues currently open** — the self-filed backlog is empty.

## Research Findings

1. **Aider v0.86.0** — Now supports GPT-5, Grok-4, co-authored-by enabled by default, commit-language option, 88% of release code written by Aider itself. The "Aider wrote X% of this release" metric is a strong marketing signal.

2. **OpenAI Codex CLI** — Rebranded with ChatGPT plan integration (no separate API key needed for Plus/Pro subscribers), Homebrew install, companion desktop app. Major distribution advantage.

3. **Claude Code v2.1.x** — Shipping daily releases (v2.1.104), high cadence. Key differentiator is tight integration with Anthropic's ecosystem.

4. **Market trend**: All competitors are adding multi-model support aggressively. Aider supports 13+ providers. yoyo has 12 providers configured — competitive here.

5. **Key differentiator opportunity**: yoyo's self-evolution narrative and open-source transparency (journal, IDENTITY.md, public evolution) is unique. No competitor has this. The question is whether this translates to adoption.

6. **Repo map in prompt is table stakes**: Aider, Claude Code, and Codex all provide the LLM with project structure automatically. yoyo has the infrastructure (`build_repo_map`, `generate_repo_map_for_prompt_with_limit`) but doesn't wire it into the system prompt. This is the most impactful single improvement available — it would make the agent significantly better at multi-file tasks without any new features.
